from dotenv import dotenv_values

config = dotenv_values(".env")

# declaration of LLM for langchain
from langchain_openai import AzureChatOpenAI
from dotenv import dotenv_values

API_ENDPOINT=config.get("AZURE_OPENAI_API_BASE")
API_KEY=config.get("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT_NAME=config.get("AZURE_DEPLOYMENT_NAME")

# Initialize the LLM
# explore langchain documentaiton to use other models in the link below
# https://docs.langchain.com/oss/python/integrations/providers/all_providers
llm = AzureChatOpenAI(
                model="gpt-4.1", 
                azure_deployment=AZURE_DEPLOYMENT_NAME, 
                openai_api_version="2024-12-01-preview",
                temperature=0,
                api_key=API_KEY,
                azure_endpoint=API_ENDPOINT,
                )

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

# Document Intelligence
ADI_KEY=config.get("ADI_KEY")
ADI_ENDPOINT=config.get("ADI_ENDPOINT")

# Azure Document Intelligence
document_intelligence_client = DocumentIntelligenceClient(
    endpoint=ADI_ENDPOINT, credential=AzureKeyCredential(ADI_KEY)
)


