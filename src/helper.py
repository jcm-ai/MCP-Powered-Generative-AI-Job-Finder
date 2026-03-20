import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

client = genai.Client(api_key="GEMINI_API_KEY")


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


def ask_gemini(prompt, max_tokens=500):
    """
    Sends a prompt to the Gemini API and returns the response.
    
    Args:
        prompt (str): The prompt to send to the Gemini API.
        max_tokens (int): The maximum number of tokens in the response.
        
    Returns:
        str: The response from the Gemini API.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": prompt}],
        generation_config=genai.types.GenerationConfig(
            temperature=0.5,
            max_output_tokens=max_tokens
        )
    )
    return response.choices[0].message.content
