"""
Unified LLM Clients: Groq + Gemini
"""

import os
import json
import logging
from dotenv import load_dotenv
from groq import Groq
from google import genai

load_dotenv()
logger = logging.getLogger(__name__)

# =========================
# GROQ SETUP
# =========================
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# GEMINI SETUP
# =========================
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)




# =========================
# GROQ CALL
# =========================
def call_groq(prompt: str, model="llama-3.1-8b-instant") -> str:
    try:
        res = groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return res.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return ""


# =========================
# GEMINI CALL
# =========================
def call_gemini(prompt: str) -> str:
    try:
        res = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return res.text
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return ""


# =========================
# SAFE JSON PARSER
# =========================
def safe_json_parse(text: str):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        return None