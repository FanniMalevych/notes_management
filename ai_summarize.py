import os
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def summarize_note_with_gemini(content: str | Any) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(content)
    return response.text
