from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import *

llm = ChatGoogleGenerativeAI(
    model=GOOGLE_GEMINI_MODEL_NAME,
    api_key=GOOGLE_GEMINI_API_KEY,
	temperature=GOOGLE_GEMINI_TEMPERATURE
)