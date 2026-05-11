# import json
# import os
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env")


# def extract_missing_tests(report_text, already_found_tests):
#     api_key = os.getenv("GROQ_API_KEY")

#     if not api_key:
#         print("⚠️ GROQ_API_KEY missing → skipping LLM")
#         return {"tests": []}

#     client = Groq(api_key=api_key)

#     existing_tests = [t.get("test_name", "") for t in already_found_tests]

#     prompt = f"""
# You are a strict medical lab report parser.

# TASK:
# Extract ONLY lab tests that are NOT already listed.

# DO NOT extract these tests:
# {existing_tests}

# STRICT RULES:
# - Output ONLY valid JSON
# - No explanation
# - No markdown
# - No duplicate tests
# - Skip uncertain values
# - value MUST be a number
# - Do NOT guess values
# - Do NOT invent tests

# FORMAT:
# {{
#   "tests": [
#     {{
#       "test_name": "string",
#       "value": number,
#       "unit": "string or null",
#       "reference_range": "string or null",
#       "status": "string or null"
#     }}
#   ]
# }}

# TEXT:
# {report_text}
# """

#     try:
#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )

#         output = response.choices[0].message.content.strip()

#         # 🔥 clean markdown if exists
#         output = output.replace("```json", "").replace("```", "").strip()

#         data = json.loads(output)

#         # 🔥 post-cleaning
#         clean_tests = []
#         for t in data.get("tests", []):
#             name = t.get("test_name")
#             value = t.get("value")

#             if not name:
#                 continue

#             if not isinstance(value, (int, float)):
#                 continue

#             if value < 0:
#                 continue

#             clean_tests.append({
#                 "test_name": name.strip(),
#                 "value": value,
#                 "unit": t.get("unit"),
#                 "reference_range": t.get("reference_range"),
#                 "status": t.get("status")
#             })

#         return {"tests": clean_tests}

#     except Exception as e:
#         print("❌ LLM ERROR:", e)
#         return {"tests": []}


import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def structure_report(text: str):
    prompt = f"""
You are an expert medical laboratory report extraction assistant.

TASK:
Extract ALL laboratory tests from the report text and return structured JSON only.

IMPORTANT RULES:
1. Output ONLY valid JSON
2. Do NOT explain anything
3. Do NOT skip tests
4. Do NOT invent missing values
5. Preserve exact test names
6. value can be numeric or text (Positive, Negative, Reactive, etc.)

STATUS DETECTION RULES:
- If value is BELOW reference range → status = "Low"
- If value is ABOVE reference range → status = "High"
- If value is WITHIN reference range → status = "Normal"

SPECIAL CASES:
- If report already mentions status like:
  Borderline High, Positive, Reactive, Critical,
  use that exact status.
- If reference range is non-numeric like:
  "<200", ">40", "Negative"
  interpret correctly.
- If status cannot be determined, return "".

EXAMPLES:

Example 1:
Value: 19
Reference Range: 20 - 40
Status: Low

Example 2:
Value: 168
Reference Range: <150
Status: High

Example 3:
Value: 14.5
Reference Range: 13 - 16
Status: Normal

OUTPUT FORMAT:
{{
  "tests": [
    {{
      "test_name": "",
      "value": "",
      "unit": "",
      "reference_range": "",
      "status": ""
    }}
  ]
}}

REPORT TEXT:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    output = response.choices[0].message.content

    # clean markdown if any
    output = output.replace("```json", "").replace("```", "").strip()

    return json.loads(output)