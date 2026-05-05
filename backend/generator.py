import os
import time
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PRIMARY_MODEL = "models/gemini-flash-latest"
FALLBACK_MODEL = "models/gemini-2.0-flash-001"

def extract_text(response):
    try:
        if response.text:
            return response.text
        return response.candidates[0].content.parts[0].text
    except:
        return "No response generated"

def generate(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=PRIMARY_MODEL,
                contents=prompt
            )
            return extract_text(response)

        except Exception as e:
            print(f"[Retry {attempt+1}] Primary failed: {e}")
            time.sleep(2 ** attempt)

    try:
        print("Switching to fallback model...")
        response = client.models.generate_content(
            model=FALLBACK_MODEL,
            contents=prompt
        )
        return extract_text(response)

    except Exception as e:
        return f"Generator failed completely: {e}"