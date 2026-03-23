import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    
    Args:
        uploaded_file (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_gemini(prompt: str, max_tokens: int = 500) -> str:
    """Send prompt to Gemini and return response text."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",   # ✅ working model
        contents=prompt,            # ✅ pass plain string, not messages=[]
        config={
            "max_output_tokens": max_tokens,
            "temperature": 0.5
        }
    )
    return response.text.strip()