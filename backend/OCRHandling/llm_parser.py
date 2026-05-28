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


# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# def structure_report(text: str):
#     prompt = f"""
# You are an expert medical laboratory report extraction assistant.

# TASK:
# Extract ALL laboratory tests from the report text and return structured JSON only.

# IMPORTANT RULES:
# 1. Output ONLY valid JSON
# 2. Do NOT explain anything
# 3. Do NOT skip tests
# 4. Do NOT invent missing values
# 5. Preserve exact test names
# 6. value can be numeric or text (Positive, Negative, Reactive, etc.)

# STATUS DETECTION RULES:
# - If value is BELOW reference range → status = "Low"
# - If value is ABOVE reference range → status = "High"
# - If value is WITHIN reference range → status = "Normal"

# SPECIAL CASES:
# - If report already mentions status like:
#   Borderline High, Positive, Reactive, Critical,
#   use that exact status.
# - If reference range is non-numeric like:
#   "<200", ">40", "Negative"
#   interpret correctly.
# - If status cannot be determined, return "".

# EXAMPLES:

# Example 1:
# Value: 19
# Reference Range: 20 - 40
# Status: Low

# Example 2:
# Value: 168
# Reference Range: <150
# Status: High

# Example 3:
# Value: 14.5
# Reference Range: 13 - 16
# Status: Normal

# OUTPUT FORMAT:
# {{
#   "tests": [
#     {{
#       "test_name": "",
#       "value": "",
#       "unit": "",
#       "reference_range": "",
#       "status": ""
#     }}
#   ]
# }}

# REPORT TEXT:
# {text}
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )

#     output = response.choices[0].message.content

#     # clean markdown if any
#     output = output.replace("```json", "").replace("```", "").strip()

#     return json.loads(output)


# import os
# import json
# import logging

# from groq import Groq
# from dotenv import load_dotenv

# # Configure logging
# logger = logging.getLogger(__name__)

# load_dotenv()

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )


# # =====================================
# # STRUCTURE REPORT
# # =====================================


# def structure_report(text: str):
#     """
#     Extract laboratory tests from medical report with status determination.
    
#     Args:
#         text: Cleaned OCR text from medical report
        
#     Returns:
#         Dict with list of structured test data including status for each test
#     """

#     prompt = f"""
# You are an expert medical report parser. Your task is to extract ALL laboratory tests with accurate status determination.

# CRITICAL RULES:
# 1. Output ONLY valid JSON - no explanation, no markdown
# 2. Extract ALL tests found in the report
# 3. Preserve values and units exactly as written
# 4. Calculate status for EVERY single test
# 5. Return empty string "" only if data is truly missing

# STATUS DETERMINATION RULES (Apply to EVERY test):
# ================================

# Rule 1: If reference range is provided (e.g., "20-40")
#   - Value < minimum → status = "Low"
#   - Value > maximum → status = "High"  
#   - Minimum ≤ Value ≤ maximum → status = "Normal"

# Rule 2: If reference range uses comparison operators
#   - Value: 250, Range: "<200" → status = "High"
#   - Value: 35, Range: ">40" → status = "Low"
#   - Value: 120, Range: "<150" → status = "Normal"

# Rule 3: If report explicitly mentions status
#   - Use exact status: "Positive", "Negative", "Reactive", "Critical", etc.

# Rule 4: If NO reference range provided
#   - Try to infer from common medical values
#   - If cannot infer → status = ""

# IMPORTANT: Apply status determination to ALL tests consistently, not just the first one.

# EXAMPLES:
# Test 1: Hemoglobin 14.5 g/dL, Range: 13.5-17.5 → status: "Normal"
# Test 2: WBC 3.0 K/uL, Range: 4.5-11.0 → status: "Low"
# Test 3: Glucose 180 mg/dL, Range: 70-100 → status: "High"
# Test 4: Platelets 450, Range: 150-400 → status: "High"

# OUTPUT FORMAT (for ALL tests):
# {{
#   "tests": [
#     {{
#       "test_name": "string - exact test name from report",
#       "value": "string or number - exactly as reported",
#       "unit": "string - unit of measurement or empty string",
#       "reference_range": "string - normal range or empty string",
#       "status": "Low/High/Normal/Positive/Negative/Reactive/Critical/or empty string"
#     }}
#   ]
# }}

# MEDICAL REPORT TO PARSE:
# {text}
# """

#     try:
#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0
#         )

#         output = response.choices[0].message.content

#         # Clean markdown code blocks
#         output = output.replace("```json", "").replace("```", "").strip()

#         # Parse JSON
#         data = json.loads(output)
        
#         return data

#     except json.JSONDecodeError as e:
#         logger.error(f"Failed to parse LLM response as JSON: {e}")
#         return {"tests": []}
#     except Exception as e:
#         logger.error(f"LLM structure_report failed: {e}")
#         return {"tests": []}

# import logging
# from llm_clients import call_groq, call_gemini, safe_json_parse

# logger = logging.getLogger(__name__)


# # =====================================
# # STRUCTURE REPORT (ENSEMBLE)
# # =====================================

# def structure_report(text: str):
#     """
#     Extract medical tests using Groq + Gemini ensemble
#     """

#     prompt = f"""
# You are an expert medical report parser.

# Extract ALL lab tests and return ONLY valid JSON.

# FORMAT:
# {{
#   "tests": [
#     {{
#       "test_name": "",
#       "value": "",
#       "unit": "",
#       "reference_range": "",
#       "status": ""
#     }}
#   ]
# }}

# RULES:
# - No explanation
# - No markdown
# - Preserve values exactly
# - Include all tests

# TEXT:
# {text}
# """

#     # ---------------------
#     # MODEL 1: GROQ
#     # ---------------------
#     groq_output = call_groq(prompt)
#     groq_data = safe_json_parse(groq_output)

#     # ---------------------
#     # MODEL 2: GEMINI
#     # ---------------------
#     gemini_output = call_gemini(prompt)
#     gemini_data = safe_json_parse(gemini_output)

#     # ---------------------
#     # MERGE LOGIC
#     # ---------------------
#     def extract_tests(data):
#         return data.get("tests", []) if isinstance(data, dict) else []

#     groq_tests = extract_tests(groq_data)
#     gemini_tests = extract_tests(gemini_data)

#     all_tests = groq_tests + gemini_tests

#     # fallback if both fail
#     if not all_tests:
#         logger.warning("Both LLMs failed")
#         return {"tests": []}

#     return {"tests": all_tests}

# import logging

# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)

# # Load HF processor once
# hf_processor = HFLLMProcessor()


# # =====================================
# # STRUCTURE REPORT
# # =====================================

# def structure_report(text: str):
#     """
#     Extract medical tests using Hugging Face model
#     """

#     try:
#         result = hf_processor.parse_tests(text)

#         if not result:
#             return {"tests": []}

#         return result

#     except Exception as e:
#         logger.error(f"LLM parsing failed: {e}")

#         return {
#             "tests": []
#         }

# """
# LLM Parser Module
# Routes text structuring requests to the cloud-hosted Gemini engine
# """

# import logging
# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)

# # Reuses the updated Gemini-backed processor instance
# gemini_processor = HFLLMProcessor()


# # =====================================
# # STRUCTURE REPORT
# # =====================================

# def structure_report(text: str):
#     """
#     Extract and structure medical tests using the Google Gemini engine
#     """
#     try:
#         # Routes directly to your updated gemini.client code
#         result = gemini_processor.parse_tests(text)

#         if not result:
#             return {"tests": []}

#         return result

#     except Exception as e:
#         logger.error(f"Gemini structuring failed: {e}")
#         return {"tests": []}

# """
# LLM Parser Module
# Routes text structuring requests to the cloud-hosted Gemini engine
# utilizing production-hardened Few-Shot prompting patterns.
# """

# import logging
# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)

# # Reuses the updated Gemini-backed processor instance
# gemini_processor = HFLLMProcessor()


# # =====================================
# # STRUCTURE REPORT
# # =====================================

# # In LLM/llm_parser.py

# def structure_report(text: str) -> dict:
#     if not text:
#         return {"tests": []}

#     few_shot_prompt = f"""
# You are a precision medical-data parser engine. Your task is to extract unstructured clinical laboratory OCR strings into strict JSON structures. 

# CRITICAL PARSING STRATEGIES FOR MESSY TEXT:
# 1. QUANTITATIVE METRICS (e.g., Hemoglobin, WBC Count, Cholesterol, Triglycerides):
#    - Only capture numeric values in the "value" field.
#    - For complex ranges (like Lipid profiles), extract only the standard numerical cutoff limit threshold (e.g., "< 200" or "< 150"). Do not map entire text blocks into the range fields.
#    - Accurately evaluate "status" ("Normal", "High", "Low") based strictly on the extracted value relative to that numeric boundary.

# 2. QUALITATIVE FINDINGS & MORPHOLOGY (e.g., RBC Morphology, Parasites):
#    - Leave the "unit" as "N/A".
#    - Set "reference_range" to "Normal" or "Negative".
#    - Set "status" to "Normal" if no abnormalities are explicitly noted.

# --- START FEW-SHOT EXAMPLES ---

# EXAMPLE 1 (Messy Lipid Layout):
# Raw Input: "Cholesterol mg/dL Desirable : <200 Borderline High : 200 - 239 High : >240 Method 189.0"
# Output Style:
# - test_name: "Cholesterol", value: "189.0", unit: "mg/dL", reference_range: "< 200", status: "Normal"

# EXAMPLE 2 (Qualitative Comments):
# Raw Input: "RBC Morphology Normochromic Normocytic Parasites Malarial parasite is not detected."
# Output Style:
# - test_name: "RBC Morphology", value: "Normochromic Normocytic", unit: "N/A", reference_range: "Normal", status: "Normal"
# - test_name: "Parasites", value: "Not Detected", unit: "N/A", reference_range: "Negative", status: "Normal"

# --- END FEW-SHOT EXAMPLES ---

# Using this logic, evaluate the following raw data dump. Clean up units (e.g., convert bare "/cmm" to standardized strings if context dictates), and strip away diagnostic doctor signatures or metadata footnotes.

# RAW TEXT DATA:
# {text}
# """
#     # ... call your processor execution steps downstream as normal ...

#     try:
#         # Route the layered few-shot construction down to the structural client
#         result = gemini_processor.parse_tests(few_shot_prompt)

#         if not result or "tests" not in result:
#             return {"tests": []}

#         return result

#     except Exception as e:
#         logger.error(f"Gemini few-shot structuring step failed: {e}")
#         return {"tests": []}


# import logging
# import json
# import re
# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)
# gemini_processor = HFLLMProcessor()

# def structure_report(text: str) -> dict:
#     if not text:
#         return {"tests": []}

#     few_shot_prompt = f"""
# You are a precision medical-data parser engine. Your task is to extract unstructured clinical laboratory OCR strings into strict JSON structures. 

# CRITICAL PARSING STRATEGIES:
# 1. QUANTITATIVE METRICS (e.g., Hemoglobin, WBC Count, Cholesterol): Extract only numeric values into the "value" field.
# 2. Return a valid JSON object string containing a single root key called "tests".

# RAW TEXT DATA:
# {text}
# """

#     try:
#         # 1. Fetch raw payload response from processing target
#         raw_response = gemini_processor.parse_tests(few_shot_prompt)

#         # 2. Safety Fallback: If it returns an object directly, use it
#         if isinstance(raw_response, dict):
#             return raw_response if "tests" in raw_response else {"tests": []}

#         # 3. Defensive Cleanup: If it returns a string with markdown blocks, clean it up out of text wraps safely
#         if isinstance(raw_response, str):
#             cleaned_response = raw_response.strip()
#             if cleaned_response.startswith("```json"):
#                 cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
#             elif cleaned_response.startswith("```"):
#                 cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
#             parsed_json = json.loads(cleaned_response)
#             return parsed_json if "tests" in parsed_json else {"tests": []}

#         return {"tests": []}

#     except Exception as e:
#         logger.error(f"❌ Gemini few-shot structuring step failed: {e}")
#         return {"tests": []}


# """
# LLM Parser Module
# Routes text structuring requests to the cloud-hosted Gemini engine
# utilizing production-hardened Few-Shot prompting patterns.
# """

# import logging
# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)

# # Reuses the updated Gemini-backed processor instance
# gemini_processor = HFLLMProcessor()



# # def structure_report(text: str) -> dict:
# #     if not text:
# #         return {"tests": []}

# #     few_shot_prompt = f"""
# # You are an expert clinical laboratory data extraction system. Your goal is to convert messy OCR outputs from a CBC (Complete Blood Count) and Lipid Profile report into a structured list of test elements.

# # CRITICAL PARSING STRATEGIES:
# # 1. QUANTITATIVE METRICS (e.g., Hemoglobin, RBC Count, Cholesterol, Triglycerides):
# #    - Capture ONLY the numeric value in the 'value' field (e.g., '14.5', '4.79', '189.0', '10570').
# #    - For reference limits, capture clean thresholds (e.g. '13.0 - 16.5', '<200', '150 - 199').
# #    - Evaluate 'status' based on reference bounds: 'High' (if elevated), 'Low' (if below interval), 'Borderline' (if right at boundary or flagged borderline), or 'Normal'.

# # 2. QUALITATIVE BIOMARKERS & OBSERVATIONS (e.g., RBC Morphology, Parasites):
# #    - Keep the original textual observation in the 'value' field (e.g., 'Normochromic Normocytic', 'Malarial parasite is not detected').
# #    - Set 'unit' to 'N/A'.
# #    - Set 'reference_range' to 'Normal' or 'Negative'.
# #    - Set 'status' to 'Normal' unless an explicit clinical abnormality is described.

# # 3. CLEANUP RULE:
# #    - Ignore doctor signatures (e.g., Dr. Sanjeev Shah), patient metadata (Lyubochka Svetka), client identifiers, page numbering, and header/footer junk.

# # --- START OF FEW-SHOT EXAMPLES ---

# # EXAMPLE 1 (WBC & Differential lines):
# # Input OCR: "WBC Count H /cmm 4000 - 10000 SF Cube cell analysis 10570"
# # Output tests entry:
# # - test_name: "WBC Count", value: "10570", unit: "/cmm", reference_range: "4000 - 10000", status: "High"

# # EXAMPLE 2 (Lipids & Qualitative findings):
# # Input OCR: "Triglyceride H mg/dL Normal : <150 168.0 Parasites Malarial parasite is not detected."
# # Output tests entries:
# # - test_name: "Triglyceride", value: "168.0", unit: "mg/dL", reference_range: "<150", status: "High"
# # - test_name: "Parasites", value: "Malarial parasite is not detected", unit: "N/A", reference_range: "Negative", status: "Normal"

# # --- END OF FEW-SHOT EXAMPLES ---

# # Please extract every valid laboratory biomarker from the raw report text provided below. Maintain strict data typing.

# # RAW REPORT TEXT:
# # {text}
# # """

# #     try:
# #         # Route the layered few-shot construction down to the structured client
# #         result = gemini_processor.parse_tests(few_shot_prompt)

# #         if not result or "tests" not in result:
# #             logger.warning("Empty dictionary structure received. Retrying with default payload structure.")
# #             return {"tests": []}

# #         return result

# #     except Exception as e:
# #         logger.error(f"Gemini few-shot structuring step failed: {e}")
# #         return {"tests": []}

# def structure_report(text: str) -> dict:
#     if not text:
#         logger.warning("Structure request received empty text.")
#         return {"tests": []}

#     try:
#         # The tenacity decorator inside ensemble_processor will handle 503s automatically
#         result = gemini_processor.parse_tests(few_shot_prompt)
        
#         # Validate that the LLM actually returned data
#         if result and "tests" in result and result["tests"]:
#             return result
            
#         logger.error("EXTRACTION_FAILURE: LLM returned valid JSON but no tests were found.")
#         return {"tests": [], "error": "No clinical metrics extracted"}

#     except Exception as e:
#         logger.critical(f"Pipeline failure after retries: {e}")
#         # Return a structure that the UI can detect as an error
#         return {"tests": [], "error": "System unavailable, please try again."}

"""
LLM Parser Module
Routes text structuring requests to the cloud-hosted Gemini engine
utilizing production-hardened Few-Shot prompting patterns.
"""

import logging
from OCRHandling.ensemble_processor import HFLLMProcessor

logger = logging.getLogger(__name__)

# Reuses the updated Gemini-backed processor instance
gemini_processor = HFLLMProcessor()

def structure_report(text: str) -> dict:
    if not text:
        logger.warning("Structure request received empty text.")
        return {"tests": []}

    # Define the prompt within the function scope so it can use the 'text' argument
    few_shot_prompt = f"""
You are an expert clinical laboratory data extraction system. Your goal is to convert messy OCR outputs from a CBC (Complete Blood Count) and Lipid Profile report into a structured list of test elements.

CRITICAL PARSING STRATEGIES:
1. QUANTITATIVE METRICS: Capture numeric values, units, and reference ranges. Evaluate 'status' based on reference bounds (High, Low, Normal).
2. QUALITATIVE BIOMARKERS: Keep the original text in the 'value' field. Set 'unit' to 'N/A' and status to 'Normal'.
3. CLEANUP RULE: Ignore signatures, patient metadata, and header/footer noise.

--- START OF FEW-SHOT EXAMPLES ---
Input OCR: "WBC Count H /cmm 4000 - 10000 SF Cube cell analysis 10570"
Output: {{"tests": [{{"test_name": "WBC Count", "value": "10570", "unit": "/cmm", "reference_range": "4000 - 10000", "status": "High"}}]}}

Input OCR: "Triglyceride H mg/dL Normal : <150 168.0 Parasites Malarial parasite is not detected."
Output: {{"tests": [{{"test_name": "Triglyceride", "value": "168.0", "unit": "mg/dL", "reference_range": "<150", "status": "High"}}, {{"test_name": "Parasites", "value": "Malarial parasite is not detected", "unit": "N/A", "reference_range": "Negative", "status": "Normal"}}]}}
--- END OF FEW-SHOT EXAMPLES ---

Please extract every valid laboratory biomarker from the raw report text provided below. Return ONLY valid JSON.

RAW REPORT TEXT:
{text}
"""

    try:
        # gemini_processor.parse_tests now has retry logic in ensemble_processor.py
        result = gemini_processor.parse_tests(few_shot_prompt)
        
        # Validate that the LLM returned a non-empty list of tests
        if result and isinstance(result, dict) and "tests" in result and len(result["tests"]) > 0:
            return result
            
        logger.error("EXTRACTION_FAILURE: LLM returned structure but no tests were found.")
        return {"tests": [], "error": "No clinical metrics extracted from report."}

    except Exception as e:
        logger.critical(f"Pipeline failure after retries: {e}")
        return {"tests": [], "error": "System unavailable, please try again."}