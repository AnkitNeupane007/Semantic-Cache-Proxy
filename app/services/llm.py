from app.core.config import settings
from groq import Groq
from app.core.exceptions import ServiceException

try:
    client = Groq(api_key=settings.GENAI_API_KEY)
except Exception as e:
    client = None

def generate_response(prompt:str) -> str:
    if not client:
        raise ServiceException("LLM", "Groq client failed to initialize or missing API key.")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except Exception as e:
        raise ServiceException("LLM", f"Failed to generate response: {str(e)}")

if __name__ == "__main__":
    print(generate_response("What is the capital of France?"))
