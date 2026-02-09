# PDF to Synthetic Q&A Dataset Generator

This repository provides a pipeline to **extract text from PDF documents** and **generate synthetic question–answer (Q&A) datasets** using a Large Language Model (LLM).
(The Words in the red boxes are the command-line arguments used to run the script!)

<img width="3240" height="971" alt="image" src="https://github.com/user-attachments/assets/65e9890d-c009-40b3-8062-59771615e6ce" />

---

## Overview

The pipeline works as follows:

1. **Input PDF**  
   A PDF file path is provided via the command line.

2. **Text Extraction (`--method`)**  
   Text is extracted using one of the following methods:
   - `pypdf2`
   - `pymupdf`
   - `docintel` (Azure Document Intelligence)

3. **Text Chunking (`--chunk_size`)**  
   The extracted text is split into fixed-size character chunks.

4. **Prompt-Based Q&A Generation (`--prompt_style`)**  
   Each chunk is sent to an LLM with a configurable system prompt: (these can be further refined in the prompts.py file)
   - `short`: concise, fact-based Q&A
   - `long`: more descriptive Q&A

5. **JSON Output**  
   The generated questions and answers are saved as a structured JSON file.

---

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Configure a Large Language Model (LLM) in config.py using LangChain.

Refer to the [LangChain's documentation](https://docs.langchain.com/oss/python/integrations/providers/all_providers) for supported providers and setup examples. 
And also ensure that any required API keys or credentials are properly set before running the script.

## Usage

Run the script from the command line:

```python
pyhton generate_Dataset.py \
  --file ./dataset/example.pdf \
  --method docintel \
  --chunk_size 1000 \
  --prompt_style short
```

## Output Format

The output is saved as a JSON file with the same base name and file location path as the input PDF.

Example:

```python
{
  "dataset": [
    {
      "question": "Which Legendary Pok\u00e9mon can be found at the top of the Sky Pillar in Pok\u00e9mon Emerald?",
      "answer": "Rayquaza"
    }
  ],
  "model": "the-llm-model-used",
  "chunk_size": 1000,
  "prompt_style": "short"
}
```

---

## Further Exploration
- Evaluate the quality of the generated dataset by checking the validity of the generated question–answer pairs.
- Explore the effectiveness of the dataset by training a model on it and comparing performance against other datasets.
- Explore improved question generation strategies, such as using a sliding context window or incorporating a summary of the entire PDF as additional context for each question–answer generation step.

## Acknowledgements

Adapted and inspired by:
https://github.com/nalinrajendran/synthetic-LLM-QA-dataset-generator


