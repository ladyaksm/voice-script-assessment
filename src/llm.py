import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_insight(report):
    prompt = f"""
    You are an audio quality analyst for legal deposition recordings.
    
    Your role is to interpret measured audio signals.
    Do not invent measurements.
    
    Base all conclusions strictly on the provided analysis.
    Given the following structured audio analysis:
    {json.dumps(report, indent=2)}
    
    Generate a concise report containing:
    1. Overall Assessment
    2. Potential Risks for transcription
    3. Recommended Actions
    4. Suitability for downstream ASR
    
    Keep the tone professional and practical."""

    response = model.generate_content(prompt)

    return response.text