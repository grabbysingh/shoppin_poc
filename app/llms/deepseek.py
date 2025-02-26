from langchain_openai import ChatOpenAI
from app.core.config import *

llm = ChatOpenAI(
	openai_api_key = OPENROUTER_API_KEY,
	openai_api_base = OPENROUTER_BASE_URL,
	model_name = OPENROUTER_MODEL_NAME,
)