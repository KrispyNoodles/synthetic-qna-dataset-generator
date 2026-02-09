# use to generate short answers
system_prompt_short = """
    You are generating fact-based question–answer pairs for training a Large Language Model.

    Convert the given text into EXACTLY ONE question and ONE answer.

    QUESTION REQUIREMENTS:
    - The question must ask for a specific fact, entity, name, or short phrase.
    - The question may involve comparison, selection, attribution, or ordering.
    - The question should be answerable with a concise factual response.
    - The question must be clear and unambiguous.

    ANSWER REQUIREMENTS:
    - The answer must be short and factual.
    - The answer should typically be a name, entity, date, title, or yes/no.
    - Do NOT include explanations or reasoning.
    - Do NOT include full sentences unless necessary.

    AVOID:
    - Open-ended or explanatory questions.
    - “Why” or “How” questions that require reasoning.
    - Multi-sentence answers.
    - Subjective or opinion-based questions.

    PREFERRED QUESTION STYLES:
    - “Which …?”
    - “Who …?”
    - “What …?”
    - “Which of the following …?”
    - “Was … yes or no?”
    - “Which was released first …?”
    - “Between X and Y, which …?”

    Return only the question and the answer.
    """

# use to generate longer answers with explanation
system_prompt_long = """ 
    You are generating training data for a Large Language Model. 

    Convert the given text into EXACTLY ONE question and ONE answer. 

    DATA QUALITY REQUIREMENTS: 
    - PREFERRED QUESTION FORMS: 
    - "Why is … required?" 
    - "What is the purpose of …?" 
    - "How does … affect …?" 
    - "Under what conditions … and why?" PREFERRED QUESTION FORMS: 
    - "Why is … required?" - "What is the purpose of …?" 
    - "How does … affect …?" 
    - "Under what conditions … and why?
    """
