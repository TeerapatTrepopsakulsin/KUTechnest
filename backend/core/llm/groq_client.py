from langchain_groq import ChatGroq
from ...config import settings


def get_llm():
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE
    )
