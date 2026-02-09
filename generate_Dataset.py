import os
import sys
import json
from typing import List
from tqdm import tqdm
import subprocess
import argparse

from config import llm, document_intelligence_client
import PyPDF2
import pymupdf
from azure.ai.documentintelligence.models import AnalyzeResult

from config import llm
from pydantic import BaseModel

from langchain.schema import HumanMessage, SystemMessage
from prompt import system_prompt_short, system_prompt_long

# calling the function
# python generate_Dataset.py --file ./dataset/pokemon_emerald.pdf --method docintel

# adapted & inspired from 
# https://github.com/nalinrajendran/synthetic-LLM-QA-dataset-generator

# declaration of Schema for the output
class QuestionAnswer(BaseModel):
    """Question and Answer Template"""
    question: str
    answer: str 

def generate_questions_answers(text_chunk, system_prompt):

    # ensuring the output of the llm
    structured_llm = llm.with_structured_output(QuestionAnswer)    

    message = [
        # change here to decide what kind of questions/ answers do you want to be generated from the system prompt in the prompts.py
        SystemMessage(content=system_prompt),
        HumanMessage(content="This is the text chunk" + text_chunk)
    ]

    # using invoke
    try:
        result = structured_llm.invoke(message)
    
    # to catch for situations where there is an openai.BadRequestError
    except Exception as e:
        print(f"An error occurred: {e}")
        
        return None

    return {
        "question": result.question,
        "answer": result.answer
    }
    
# extracting text from the pdf, 3 different options
# using PyPDF2 to extract
def extract_with_pypdf2(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    pdf_file_obj.close()
        
    return text

# using PyMuPDF to extract the text
def extract_with_pymupdf(file_path):

    doc = pymupdf.open(file_path) # open a document
    text = ''

    for page in doc: # iterate the document pages
        text += page.get_text() # get plain text (is in UTF-8)

    return text

# using Microsoft Doc Intel to extract the text
## Document Intelligence
def extract_with_docintel(file_path):
    try:
        with open(file_path, "rb") as f:
            poller = document_intelligence_client.begin_analyze_document("prebuilt-layout", body=f)
            
        result: AnalyzeResult = poller.result()

    except Exception as e:

        # returning a dataframe contianing the error
        error_string = f"❌ Unexpected error: {e}"

        print(error_string)

    # putting the text together into a single variable
    text = ''

    for x in result.paragraphs:
        text += x.content

    return text

# chunk size is the one that determines how many different questions that can be generated
def process_text(text: str, chunk_size: int, system_prompt) -> List[dict]:
    
    # creating text chunks based on the chunk size
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # final question bank
    question_bank = []

    # TQDM wraps the for loop processing into a progress bar
    for chunk in tqdm(text_chunks, desc="Generating Questions", unit="chunk"):
        response = generate_questions_answers(chunk, system_prompt)

        # for situation where the llm encounters an error
        if response is None:
            continue

        # add the response to the question_bank
        question_bank.append({'question': response['question'], 'answer': response['answer']})
    
    print(f"Generated {len(question_bank)} Questions and Answers!")

    return question_bank

# Check if correct number of arguments are provided
parser = argparse.ArgumentParser(
    description="Generate JSON dataset from a PDF file"
)

# argument for file choice
parser.add_argument(
    "--file",
    required=True,
    help="Path to the source PDF file"
)

# argument for method of text extraction
parser.add_argument(
    "--method",
    choices=["pypdf2", "pymupdf", "docintel"],
    required=True,
    help="PDF extraction method"
)

# argument for chunk size
parser.add_argument(
    "--chunk_size",
    type=int,
    default=1000,
    help="Chunk Size (Integer)"
)

# argument for question answer
parser.add_argument(
    "--prompt_style",
    choices=["short", "long"],
    default="short",
    help="Prompt style to use for QA generation"
)

# creating maps for short, long prompt

question_answer_map = {
    "short": system_prompt_short,
    "long": system_prompt_long
}


def main():
    args = parser.parse_args()

    pdf_filepath = args.file

    # checking if the pdf file path exist
    if not os.path.exists(pdf_filepath):
        print(f"Error: PDF file '{pdf_filepath}' not found.")
        sys.exit(1)
        
    print(f"Processing PDF: {pdf_filepath}")

    # extracting the text
    try:

        # retrieving the maps for the prompt and extraction method
        system_prompt =  question_answer_map[args.prompt_style]

        # extracting text, 3 different methods
        if args.method == 'pypdf2':
            text = extract_with_pypdf2(pdf_filepath)

        elif args.method == 'pymupdf':
            text = extract_with_pymupdf(pdf_filepath)

        elif args.method == 'docintel':
            text = extract_with_docintel(pdf_filepath)  
    
    except Exception as e:
        print(f"Unexpected error while reading PDF: {str(e)}")

    # creating the questions and answers
    responses = {"dataset": process_text(text, args.chunk_size, system_prompt), "model": llm.model_name, "chunk_size": args.chunk_size, "prompt_style": args.prompt_style}

    # Save responses to JSON file
    # strip the .pdf extension from the pdf file name
    pdf_filepath = os.path.splitext(pdf_filepath)[0]

    with open(f'{pdf_filepath}.json', 'w') as f:
        json.dump(responses, f, indent=2)
        print(f"Saved responses to: {pdf_filepath}.json")

    print("Process carried out successfully.")


# Install requirements when run main python file
if __name__ == '__main__':
    main()