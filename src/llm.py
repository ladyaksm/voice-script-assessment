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
You are an audio quality analyst assisting legal transcription workflows.

Your role is to interpret measured audio analysis results.

IMPORTANT:
- Use ONLY the provided measurements.
- Do NOT invent facts or assumptions.
- Avoid absolute statements.
- Use cautious language such as:
  "may impact", "could affect", "recommend review".
- Do not estimate transcription accuracy.
- Do not claim speech is unintelligible unless explicitly indicated.

Given the following structured analysis:

{json.dumps(report, indent=2)}

Generate a concise report containing:

1. Overall Assessment
2. Potential Risks for Transcription
3. Recommended Actions
4. Suitability for Downstream ASR

Keep the tone professional, practical, and evidence-based.
"""

    response = model.generate_content(prompt)

    return response.text