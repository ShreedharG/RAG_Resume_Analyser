import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class Generator:
    def __init__(self, model_name="gemini-1.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, query, context):
        prompt = f"""
        You are an expert HR and Career Consultant. 
        Use the following retrieved context from a candidate's resume and a job description to answer the user's question.
        
        Context:
        {context}
        
        Question: {query}
        
        Provide a professional, concise, and insightful answer. If the answer isn't in the context, say you don't have enough information but offer related advice.
        """
        response = self.model.generate_content(prompt)
        return response.text
