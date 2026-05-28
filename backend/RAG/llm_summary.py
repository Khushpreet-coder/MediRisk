# import os
# import json
# import requests
# from dotenv import load_dotenv

# # =====================================
# # Load .env
# # =====================================

# load_dotenv()

# HF_TOKEN = os.getenv("HF_TOKEN")

# API_URL = (
#     "https://api-inference.huggingface.co/models/"
#     "BioMistral/BioMistral-7B"
# )

# headers = {
#     "Authorization": f"Bearer {HF_TOKEN}"
# }



# # =====================================
# # Generate Medical Summary
# # =====================================

# def generate_medical_summary(report_data):

#     """
#     Generates elaborated medical summary using:
#     - structured lab report data
#     - abnormal findings
#     - rag medical context
#     - cleaned report content
#     """

#     structured_tests = report_data.get(
#         "structured_data",
#         {}
#     ).get("tests", [])

#     rag_context = report_data.get(
#         "rag_context",
#         []
#     )

#     cleaned_text = report_data.get(
#         "cleaned_text",
#         ""
#     )

#     # =====================================
#     # Abnormal Findings
#     # =====================================

#     abnormal_findings = [

#         {
#             "test_name": test.get("test_name"),
#             "value": test.get("value"),
#             "unit": test.get("unit"),
#             "reference_range": test.get("reference_range"),
#             "status": test.get("status")
#         }

#         for test in structured_tests

#         if test.get("status", "Normal") != "Normal"
#     ]

#     structured_payload = {

#         "all_tests": structured_tests,

#         "abnormal_findings": abnormal_findings,

#         "rag_context": rag_context
#     }

#     # =====================================
#     # Prompt
#     # =====================================

#     prompt = f"""
# You are a medical report explanation assistant.

# You will be given:
# 1. Structured lab test results
# 2. Retrieved medical knowledge (RAG context)

# Your task:
# Convert medical lab data into simple patient-friendly explanations.

# RULES:
# - DO NOT diagnose diseases
# - DO NOT give treatment
# - Use ONLY provided RAG context for explanations
# - If RAG context is missing, say "No medical explanation available"
# - Keep language simple for patients

# OUTPUT FORMAT (STRICT):

# For EACH abnormal test:

# Test Name:
# Value:
# Reference Range:
# Status:

# Meaning: (simple explanation from RAG context)
# Interpretation: (what it means for patient)

# ----------------------------------

# If no abnormal tests:
# Say: "All parameters are within normal range"

# ----------------------------------

# STRUCTURED DATA:
# {json.dumps(structured_payload, indent=2)}

# RAG CONTEXT:
# {json.dumps(rag_context, indent=2)}

# RAW TEXT:
# {cleaned_text}
# """


# Focus mainly on:
# - abnormal findings
# - CBC interpretation
# - overall clinical picture
# """

#     # =====================================
#     # Request Payload
#     # =====================================

#     payload = {

#         "inputs": prompt,

#         "parameters": {
#             "max_new_tokens": 400,
#             "temperature": 0.3,
#             "return_full_text": False
#         }
#     }

#     # =====================================
#     # Generate Response
#     # =====================================

#     try:

#         response = requests.post(
#             API_URL,
#             headers=headers,
#             json=payload,
#             timeout=120
#         )

#         result = response.json()

#         # =====================================
#         # Extract Generated Text
#         # =====================================

#         if isinstance(result, list):

#             summary = result[0].get(
#                 "generated_text",
#                 ""
#             )

#         elif isinstance(result, dict):

#             summary = result.get(
#                 "generated_text",
#                 ""
#             )

#         else:

#             summary = ""

#         if not summary:

#             return (
#                 "Unable to generate medical summary."
#             )

#         return summary.strip()

#     except Exception as e:

#         print("HuggingFace Error:", e)

#         return (
#             "Unable to generate medical summary."
#         )

# import os
# import json
# import requests
# from dotenv import load_dotenv

# # =====================================
# # Load .env
# # =====================================

# load_dotenv()

# HF_TOKEN = os.getenv("HF_TOKEN")

# API_URL = "https://api-inference.huggingface.co/models/BioMistral/BioMistral-7B"

# headers = {
#     "Authorization": f"Bearer {HF_TOKEN}"
# }


# # =====================================
# # Generate Medical Summary
# # =====================================

# def generate_medical_summary(report_data):

#     structured_tests = report_data.get("structured_data", {}).get("tests", [])
#     rag_context = report_data.get("rag_context", [])
#     cleaned_text = report_data.get("cleaned_text", "")

#     # =====================================
#     # Abnormal Findings
#     # =====================================

#     abnormal_findings = [
#         {
#             "test_name": test.get("test_name"),
#             "value": test.get("value"),
#             "unit": test.get("unit"),
#             "reference_range": test.get("reference_range"),
#             "status": test.get("status")
#         }
#         for test in structured_tests
#         if test.get("status", "").lower() not in ["normal", "optimal", "negative", "within limits", ""]
#     ]

#     structured_payload = {
#         "all_tests": structured_tests,
#         "abnormal_findings": abnormal_findings,
#         "rag_context": rag_context
#     }

#     # =====================================
#     # Prompt (FIXED)
#     # =====================================

#     prompt = f"""
# You are a medical report explanation assistant.

# TASK:
# Convert lab test results into simple patient-friendly explanations.

# RULES:
# - Do NOT diagnose diseases
# - Do NOT suggest treatment
# - Use ONLY RAG CONTEXT for explanations
# - If RAG context is missing, say "No medical explanation available"
# - Keep language simple and clear

# OUTPUT FORMAT (STRICT):

# For EACH abnormal test:

# Test Name:
# Value:
# Reference Range:
# Status:

# Meaning:
# Interpretation:

# ----------------------------------

# If all tests are normal:
# Say: "All parameters are within normal range"

# ----------------------------------

# STRUCTURED DATA:
# {json.dumps(structured_payload, indent=2)}

# RAG CONTEXT:
# {json.dumps(rag_context, indent=2)}

# RAW TEXT:
# {cleaned_text}
# """

#     # =====================================
#     # Request Payload
#     # =====================================

#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 400,
#             "temperature": 0.3,
#             "return_full_text": False
#         }
#     }

#     # =====================================
#     # API CALL
#     # =====================================

#     try:
#         response = requests.post(
#             API_URL,
#             headers=headers,
#             json=payload,
#             timeout=120
#         )

#         result = response.json()

#         # =====================================
#         # SAFE RESPONSE PARSING (FIXED)
#         # =====================================

#         if isinstance(result, list) and "generated_text" in result[0]:
#             summary = result[0]["generated_text"]

#         elif isinstance(result, dict):
#             summary = result.get("generated_text", "")

#         else:
#             summary = ""

#         if not summary:
#             return "Unable to generate medical summary."

#         return summary.strip()

#     except Exception as e:
#         print("HuggingFace Error:", e)
#         return "Unable to generate medical summary."


# import os
# import json
# import requests
# from dotenv import load_dotenv

# # =====================================
# # Load ENV
# # =====================================

# load_dotenv()

# HF_TOKEN = os.getenv("HF_TOKEN")

# API_URL = "https://api-inference.huggingface.co/models/BioMistral/BioMistral-7B"

# headers = {
#     "Authorization": f"Bearer {HF_TOKEN}"
# }


# # =====================================
# # LLM SUMMARY GENERATOR
# # =====================================

# def generate_medical_summary(report_data):

#     structured_tests = report_data.get("structured_data", {}).get("tests", [])
#     rag_context = report_data.get("rag_context", [])
#     cleaned_text = report_data.get("cleaned_text", "")

#     # =====================================
#     # Extract abnormal findings
#     # =====================================

#     abnormal_findings = [
#         {
#             "test_name": test.get("test_name"),
#             "value": test.get("value"),
#             "unit": test.get("unit"),
#             "reference_range": test.get("reference_range"),
#             "status": test.get("status")
#         }
#         for test in structured_tests
#         if test.get("status", "").lower() not in
#         ["normal", "optimal", "negative", "within limits", ""]
#     ]

#     structured_payload = {
#         "all_tests": structured_tests,
#         "abnormal_findings": abnormal_findings
#     }

#     # =====================================
#     # SAFE TEXT RAG FORMAT (IMPORTANT FIX)
#     # =====================================

#     rag_text = "\n".join(rag_context) if rag_context else "No medical context available."

#     # =====================================
#     # PROMPT (CLEAN + GROUNDED)
#     # =====================================

#     prompt = f"""
# You are a medical report explanation assistant.

# TASK:
# Convert lab test results into simple patient-friendly explanations.

# RULES:
# - Do NOT diagnose diseases
# - Do NOT suggest treatment
# - Use ONLY the provided RAG CONTEXT
# - If RAG CONTEXT is missing, say "No medical explanation available"
# - Keep explanations simple and clear

# OUTPUT FORMAT:

# For EACH abnormal test:

# Test Name:
# Value:
# Reference Range:
# Status:

# Meaning:
# Interpretation:

# ----------------------------------

# If all tests are normal:
# Say: "All parameters are within normal range"

# ----------------------------------

# STRUCTURED DATA:
# {json.dumps(structured_payload, indent=2)}

# RAG CONTEXT:
# {rag_text}

# RAW TEXT:
# {cleaned_text}
# """

#     # =====================================
#     # REQUEST
#     # =====================================

#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 400,
#             "temperature": 0.3,
#             "return_full_text": False
#         }
#     }

#     # =====================================
#     # CALL HF MODEL
#     # =====================================

#     try:
#         response = requests.post(
#             API_URL,
#             headers=headers,
#             json=payload,
#             timeout=120
#         )

#         result = response.json()

#         # =====================================
#         # SAFE PARSING
#         # =====================================

#         if isinstance(result, list) and len(result) > 0:
#             summary = result[0].get("generated_text", "")

#         elif isinstance(result, dict):
#             summary = result.get("generated_text", "")

#         else:
#             summary = ""

#         if not summary:
#             return "Unable to generate medical summary."

#         return summary.strip()

#     except Exception as e:
#         print("HuggingFace Error:", e)
#         return "Unable to generate medical summary."


# import os
# import json
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()

# genai.configure(
#     api_key=os.getenv("GEMINI_API_KEY")
# )


# def generate_medical_summary(report_data):

#     # =====================================
#     # FIXED JSON EXTRACTION
#     # =====================================

#     data = report_data.get("data", report_data)

#     tests = data.get("tests", [])
#     rag_context = data.get("rag_context", [])
#     cleaned_text = data.get("cleaned_text", "")

#     # =====================================
#     # FIND ABNORMAL TESTS
#     # =====================================

#     abnormal_tests = []

#     ignore_status = [
#         "normal",
#         "optimal",
#         "negative",
#         "within limits",
#         ""
#     ]

#     for test in tests:

#         status = str(
#             test.get("status", "")
#         ).strip().lower()

#         if status not in ignore_status:

#             abnormal_tests.append({
#                 "test_name": test.get("test_name"),
#                 "value": test.get("value"),
#                 "unit": test.get("unit"),
#                 "reference_range": test.get("reference_range"),
#                 "status": test.get("status")
#             })

#     # =====================================
#     # IF ALL NORMAL
#     # =====================================

#     if not abnormal_tests:

#         return """
# # Medical Report Summary

# All major laboratory parameters are within normal reference ranges.

# No significant abnormal findings were identified in this report.

# Overall blood counts, lipid markers, and general hematology parameters appear stable based on the provided data.

# Please correlate clinically with symptoms and consult your healthcare provider for final interpretation.
# """

#     # =====================================
#     # RAG CONTEXT
#     # =====================================

#     rag_text = "\n\n".join(rag_context[:5])

#     # =====================================
#     # PROMPT
#     # =====================================

#     prompt = f"""
# You are an AI medical report explanation assistant.

# Your role:
# - Explain abnormal lab findings
# - Use simple human-readable language
# - Keep response detailed but understandable
# - Do NOT diagnose diseases
# - Do NOT prescribe medications
# - Do NOT create panic

# Use ONLY the provided report findings and medical context.

# ABNORMAL TESTS:
# {json.dumps(abnormal_tests, indent=2)}

# MEDICAL CONTEXT:
# {rag_text}

# Generate a professional report summary with:

# 1. Overall Health Summary
# 2. Important Abnormal Findings
# 3. Explanation of Each Abnormal Parameter
# 4. Possible Clinical Meaning
# 5. General Lifestyle Recommendations
# 6. Final Note

# Use markdown formatting.
# """

#     # =====================================
#     # GEMINI CALL
#     # =====================================

#     try:

#         model = genai.GenerativeModel(
#             "gemini-2.0-flash"
#         )

#         response = model.generate_content(prompt)

#         return response.text

#     except Exception as e:


#         return f"Gemini Error: {str(e)}"

# import os
# import json
# import re
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()

# genai.configure(
#     api_key=os.getenv("GEMINI_API_KEY")
# )


# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test):

#     status = str(
#         test.get("status", "")
#     ).strip().lower()

#     abnormal_keywords = [
#         "high",
#         "low",
#         "positive",
#         "abnormal",
#         "borderline",
#         "critical",
#         "reactive"
#     ]

#     for word in abnormal_keywords:
#         if word in status:
#             return True

#     return False


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(report_data):

#     data = report_data.get("data", report_data)

#     tests = data.get("tests", [])
#     rag_context = data.get("rag_context", [])
#     cleaned_text = data.get("cleaned_text", "")

#     # ==========================================
#     # FIND ABNORMAL TESTS
#     # ==========================================

#     abnormal_tests = []

#     for test in tests:

#         if is_abnormal(test):

#             abnormal_tests.append({
#                 "test_name": test.get("test_name"),
#                 "value": test.get("value"),
#                 "unit": test.get("unit"),
#                 "reference_range": test.get("reference_range"),
#                 "status": test.get("status")
#             })

#     # ==========================================
#     # RAG CONTEXT
#     # ==========================================

#     rag_text = "\n\n".join(rag_context[:5])

#     # ==========================================
#     # IF NO ABNORMALITIES
#     # ==========================================

#     if len(abnormal_tests) == 0:

#         prompt = f"""
# You are a medical report summarization assistant.

# The report appears mostly normal.

# Generate a SHORT professional summary.

# Mention:
# - Overall report is stable
# - No major abnormalities detected
# - General health appears normal
# - Advise clinical correlation

# REPORT TEXT:
# {cleaned_text[:3000]}
# """

#     else:

#         # ==========================================
#         # DETAILED ABNORMAL SUMMARY PROMPT
#         # ==========================================

#         prompt = f"""
# You are an AI medical report explanation assistant.

# Your job is to explain abnormal medical findings
# in simple patient-friendly language.

# IMPORTANT RULES:
# - Do NOT diagnose diseases
# - Do NOT prescribe medicines
# - Do NOT create panic
# - Explain findings calmly
# - Focus MOSTLY on abnormal tests
# - Mention possible meaning briefly

# ABNORMAL TESTS:
# {json.dumps(abnormal_tests, indent=2)}

# MEDICAL CONTEXT:
# {rag_text}

# OCR REPORT TEXT:
# {cleaned_text[:5000]}

# Generate a detailed markdown summary with:

# # Overall Health Summary

# # Key Abnormal Findings

# For EACH abnormal parameter explain:
# - what is abnormal
# - possible meaning
# - whether mildly/moderately abnormal

# # General Recommendations

# # Final Note

# Keep explanation medically accurate but easy to understand.
# """

#     # ==========================================
#     # GEMINI API
#     # ==========================================

#     try:

#         model = genai.GenerativeModel(
#             "gemini-2.0-flash"
#         )

#         response = model.generate_content(prompt)

#         return response.text

#     except Exception as e:

#         return f"Gemini Error: {str(e)}"

# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test):

#     status = str(
#         test.get("status", "")
#     ).strip().lower()

#     abnormal_keywords = [
#         "high",
#         "low",
#         "positive",
#         "abnormal",
#         "borderline",
#         "critical",
#         "reactive"
#     ]

#     for word in abnormal_keywords:
#         if word in status:
#             return True

#     return False


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(report_data):

#     data = report_data.get("data", report_data)

#     tests = data.get("tests", [])
#     rag_context = data.get("rag_context", [])
#     cleaned_text = data.get("cleaned_text", "")

#     # ==========================================
#     # FIND ABNORMAL TESTS
#     # ==========================================

#     abnormal_tests = []

#     for test in tests:

#         if is_abnormal(test):

#             abnormal_tests.append({
#                 "test_name": test.get("test_name"),
#                 "value": test.get("value"),
#                 "unit": test.get("unit"),
#                 "reference_range": test.get("reference_range"),
#                 "status": test.get("status")
#             })

#     # ==========================================
#     # RAG CONTEXT
#     # ==========================================

#     rag_text = "\n\n".join(rag_context[:5])

#     # ==========================================
#     # NORMAL REPORT PROMPT
#     # ==========================================

#     if len(abnormal_tests) == 0:

#         prompt = f"""
# You are a medical report summarization assistant.

# The report appears mostly normal.

# Generate a SHORT professional summary.

# Mention:
# - Overall report is stable
# - No major abnormalities detected
# - General health appears normal
# - Advise clinical correlation

# REPORT TEXT:
# {cleaned_text[:3000]}
# """

#     else:

#         # ==========================================
#         # ABNORMAL REPORT PROMPT
#         # ==========================================

#         prompt = f"""
# You are an AI medical report explanation assistant.

# Your job is to explain abnormal medical findings
# in simple patient-friendly language.

# IMPORTANT RULES:
# - Do NOT diagnose diseases
# - Do NOT prescribe medicines
# - Do NOT create panic
# - Explain findings calmly
# - Focus MOSTLY on abnormal tests
# - Mention possible meaning briefly

# ABNORMAL TESTS:
# {json.dumps(abnormal_tests, indent=2)}

# MEDICAL CONTEXT:
# {rag_text}

# OCR REPORT TEXT:
# {cleaned_text[:5000]}

# Generate a detailed markdown summary with:

# # Overall Health Summary

# # Key Abnormal Findings

# For EACH abnormal parameter explain:
# - what is abnormal
# - possible meaning
# - whether mildly/moderately abnormal

# # General Recommendations

# # Final Note

# Keep explanation medically accurate but easy to understand.
# """

#     # ==========================================
#     # GROQ API CALL
#     # ==========================================

#     try:

#         completion = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a professional medical report "
#                         "summarization assistant."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.3,
#             max_tokens=1200
#         )

#         summary = completion.choices[0].message.content

#         return summary

#     except Exception as e:

#         return f"Groq Error: {str(e)}"

# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test):

#     status = str(
#         test.get("status", "")
#     ).strip().lower()

#     abnormal_keywords = [
#         "high",
#         "low",
#         "positive",
#         "abnormal",
#         "borderline",
#         "critical",
#         "reactive"
#     ]

#     return any(
#         word in status
#         for word in abnormal_keywords
#     )


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(report_data):

#     try:

#         # ==========================================
#         # EXTRACT DATA
#         # ==========================================

#         data = report_data.get("data", report_data)

#         tests = data.get("tests", [])
#         rag_context = data.get("rag_context", [])
#         cleaned_text = data.get("cleaned_text", "")

#         # ==========================================
#         # FIND ABNORMAL TESTS
#         # ==========================================

#         abnormal_tests = []

#         for test in tests:

#             if is_abnormal(test):

#                 abnormal_tests.append({
#                     "test_name": test.get("test_name", ""),
#                     "value": test.get("value", ""),
#                     "unit": test.get("unit", ""),
#                     "reference_range": test.get("reference_range", ""),
#                     "status": test.get("status", "")
#                 })

#         # ==========================================
#         # PREPARE RAG CONTEXT
#         # ==========================================

#         rag_text = "\n\n".join(
#             rag_context[:5]
#         )

#         # ==========================================
#         # PROMPT FOR NORMAL REPORT
#         # ==========================================

#         if len(abnormal_tests) == 0:

#             prompt = f"""
# You are a professional medical report summarizer.

# The medical report appears mostly normal.

# Generate a concise patient-friendly summary.

# Include:
# - Overall health impression
# - Mention that no major abnormalities were found
# - Mention general stability of blood tests
# - Advise consultation with doctor if symptoms exist

# REPORT TEXT:
# {cleaned_text[:3000]}
# """

#         # ==========================================
#         # PROMPT FOR ABNORMAL REPORT
#         # ==========================================

#         else:

#             prompt = f"""
# You are an AI medical report explanation assistant.

# Your task is to explain abnormal medical findings
# in simple and calm patient-friendly language.

# IMPORTANT RULES:
# - Do NOT diagnose diseases
# - Do NOT prescribe medicines
# - Do NOT create fear or panic
# - Explain abnormalities clearly
# - Focus mainly on abnormal parameters
# - Mention whether findings are mild/moderate/significant

# ABNORMAL TESTS:
# {json.dumps(abnormal_tests, indent=2)}

# MEDICAL CONTEXT:
# {rag_text}

# OCR REPORT TEXT:
# {cleaned_text[:5000]}

# Generate a markdown summary with:

# # Overall Health Summary

# # Key Abnormal Findings

# For EACH abnormal parameter explain:
# - what is abnormal
# - possible clinical meaning
# - whether it is mild/moderate/significant

# # General Recommendations

# # Final Note

# Keep explanation medically accurate,
# easy to understand,
# and professional.
# """

#         # ==========================================
#         # GROQ API CALL
#         # ==========================================

#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an expert AI medical report "
#                         "summarization assistant."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.3,
#             max_tokens=1200
#         )

#         summary = completion.choices[0].message.content

#         # ==========================================
#         # FALLBACK IF EMPTY
#         # ==========================================

#         if not summary:
#             return "Unable to generate medical summary."

#         return summary

#     except Exception as e:

#         print("SUMMARY ERROR:", str(e))

#         return f"Groq Error: {str(e)}"

# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )

# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test):

#     status = str(
#         test.get("status", "")
#     ).strip().lower()

#     abnormal_keywords = [
#         "high",
#         "low",
#         "positive",
#         "abnormal",
#         "borderline",
#         "critical",
#         "reactive"
#     ]

#     return any(
#         word in status
#         for word in abnormal_keywords
#     )


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(report_data):

#     try:

#         # ==========================================
#         # EXTRACT DATA
#         # ==========================================

#         data = report_data.get("data", report_data)

#         tests = data.get("tests", [])
#         rag_context = data.get("rag_context", [])

#         # ==========================================
#         # SEPARATE NORMAL + ABNORMAL TESTS
#         # ==========================================

#         abnormal_tests = []
#         normal_tests = []

#         for test in tests:

#             formatted_test = {
#                 "test_name": test.get("test_name", ""),
#                 "value": test.get("value", ""),
#                 "unit": test.get("unit", ""),
#                 "reference_range": test.get("reference_range", ""),
#                 "status": test.get("status", "")
#             }

#             if is_abnormal(test):
#                 abnormal_tests.append(formatted_test)
#             else:
#                 normal_tests.append(formatted_test)

#         # ==========================================
#         # RAG CONTEXT
#         # ==========================================

#         rag_text = "\n\n".join(
#             rag_context[:5]
#         )

#         # ==========================================
#         # NORMAL REPORT PROMPT
#         # ==========================================

#         if len(abnormal_tests) == 0:

#             prompt = f"""
# You are a professional AI medical report summarizer.

# The report appears mostly normal.

# STRUCTURED LAB REPORT:
# {json.dumps(normal_tests[:20], indent=2)}

# Generate a professional patient-friendly summary.

# INSTRUCTIONS:
# - Mention overall health impression
# - Mention that most parameters are within normal limits
# - Mention important normal findings
# - Keep tone reassuring and professional
# - Do NOT diagnose diseases
# - Do NOT prescribe medicines
# - Keep summary around 250-400 words

# FORMAT:

# # Overall Health Summary

# # Important Normal Findings

# # General Advice

# # Final Note
# """

#         # ==========================================
#         # ABNORMAL REPORT PROMPT
#         # ==========================================

#         else:

#             prompt = f"""
# You are an expert AI medical report explanation assistant.

# Your task is to explain medical abnormalities
# in clear and patient-friendly language.

# IMPORTANT RULES:
# - Do NOT diagnose diseases
# - Do NOT prescribe medicines
# - Do NOT create panic
# - Explain findings calmly and professionally
# - Focus mainly on abnormal findings
# - Mention if abnormalities appear mild/moderate/significant

# ABNORMAL TESTS:
# {json.dumps(abnormal_tests, indent=2)}

# NORMAL TESTS:
# {json.dumps(normal_tests[:10], indent=2)}

# MEDICAL KNOWLEDGE CONTEXT:
# {rag_text}

# Generate a DETAILED markdown summary.

# The response should be at least 500-800 words.

# FORMAT:

# # Overall Health Summary

# Provide overall interpretation of the report.

# # Important Abnormal Findings

# For EACH abnormal parameter explain:
# - what is abnormal
# - actual value vs normal range
# - possible clinical meaning
# - whether it appears mild/moderate/significant

# # Important Normal Findings

# Briefly mention important parameters that are normal.

# # General Recommendations

# Mention:
# - healthy lifestyle
# - hydration
# - diet
# - exercise
# - follow-up testing if needed

# # Final Note

# Mention that results should always be correlated
# with symptoms and doctor's clinical evaluation.

# IMPORTANT:
# Use simple understandable language.
# Avoid overly technical wording.
# """

#         # ==========================================
#         # GROQ API CALL
#         # ==========================================

#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an expert medical AI assistant "
#                         "specialized in laboratory report summarization."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.3,
#             max_tokens=1800
#         )

#         summary = completion.choices[0].message.content

#         # ==========================================
#         # FALLBACK
#         # ==========================================

#         if not summary:
#             return "Unable to generate medical summary."

#         return summary

#     except Exception as e:

#         print("SUMMARY ERROR:", str(e))

#         return f"Groq Error: {str(e)}"

# import os
# import json
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )


# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test: dict) -> bool:
#     """Return True if the test result is outside the normal range."""

#     status = str(test.get("status", "")).strip().lower()

#     abnormal_keywords = [
#         "high",
#         "low",
#         "positive",
#         "abnormal",
#         "borderline",
#         "critical",
#         "reactive"
#     ]

#     return any(word in status for word in abnormal_keywords)


# # ==========================================
# # FORMAT TEST LIST FOR PROMPT
# # ==========================================

# def format_tests_for_prompt(tests: list) -> str:
#     """
#     Convert test list to a clean readable table string for the LLM.
#     Much easier for the LLM to parse than raw JSON.
#     """

#     lines = []

#     for t in tests:
#         name   = t.get("test_name", "Unknown")
#         value  = t.get("value", "")
#         unit   = t.get("unit", "")
#         ref    = t.get("reference_range", "")
#         status = t.get("status", "")

#         line = f"- {name}: {value} {unit}".strip()

#         if ref:
#             line += f"  |  Reference: {ref}"
#         if status:
#             line += f"  |  Status: {status}"

#         lines.append(line)

#     return "\n".join(lines)


# # ==========================================
# # FORMAT RAG CONTEXT FOR PROMPT
# # ==========================================

# def format_rag_context(rag_context: list, abnormal_tests: list) -> str:
#     """
#     Prioritize RAG chunks that are relevant to the abnormal parameters.
#     Returns the top relevant chunks as a formatted string.
#     """

#     if not rag_context:
#         return "No additional medical knowledge available."

#     # Build a set of abnormal parameter name keywords for relevance scoring
#     abnormal_keywords = set()
#     for t in abnormal_tests:
#         name = t.get("test_name", "").lower()
#         # Add individual words from the test name for fuzzy matching
#         for word in name.split():
#             if len(word) > 2:
#                 abnormal_keywords.add(word)

#     # Score each RAG chunk by how many abnormal keywords it contains
#     scored_chunks = []
#     for chunk in rag_context:
#         chunk_lower = chunk.lower()
#         score = sum(1 for kw in abnormal_keywords if kw in chunk_lower)
#         scored_chunks.append((score, chunk))

#     # Sort by relevance descending, take top 6 chunks
#     scored_chunks.sort(key=lambda x: x[0], reverse=True)
#     top_chunks = [chunk for _, chunk in scored_chunks[:6]]

#     return "\n\n---\n\n".join(top_chunks)


# # ==========================================
# # BUILD SYSTEM PROMPT
# # ==========================================

# SYSTEM_PROMPT = """You are a senior clinical AI assistant specialized in 
# laboratory report interpretation. You generate detailed, professional, 
# and patient-friendly medical report summaries.

# Your summaries:
# - Use clear, simple English that any patient can understand
# - Are thorough, structured, and cover every finding in the report
# - Ground all explanations in the provided medical knowledge context
# - Never diagnose diseases or prescribe medications
# - Never create unnecessary panic — use calm, informative language
# - Clearly distinguish between mild, moderate, and significant findings
# - Always recommend consulting a doctor for any abnormal result"""


# # ==========================================
# # BUILD PROMPT — FULLY NORMAL REPORT
# # ==========================================

# def build_normal_prompt(normal_tests: list) -> str:

#     tests_text = format_tests_for_prompt(normal_tests)

#     return f"""
# The patient's lab report has been analyzed. All parameters are within normal limits.

# LAB RESULTS:
# {tests_text}

# Generate a detailed, professional, and reassuring medical summary for this patient.

# INSTRUCTIONS:
# - Open with a positive overall health impression
# - Go through the important parameters by category (e.g., blood count, 
#   metabolic, lipid, etc.) and explain what each one means in simple language
# - Reassure the patient that values are within healthy ranges
# - Provide practical general health maintenance advice
# - Close with a recommendation for regular health monitoring
# - Write at least 400–500 words
# - Do NOT diagnose diseases
# - Do NOT prescribe medications

# USE THIS EXACT MARKDOWN FORMAT:

# # 🩺 Overall Health Summary

# [Provide a 2–3 sentence overall impression of the report.]

# # ✅ Key Normal Findings — Explained

# [For each major parameter or group of parameters:]

# ### [Parameter / Category Name]
# **Value:** [value with unit]  
# **Reference Range:** [range]  
# **What This Means:** [plain-language explanation of what this parameter 
# measures and why it being normal is a good sign]

# # 💡 General Health Recommendations

# [Provide specific, practical lifestyle advice in bullet points covering 
# diet, hydration, exercise, sleep, and preventive care.]

# # 📋 Final Note

# [Remind the patient that lab results should always be reviewed with their 
# doctor alongside symptoms and clinical history. Encourage regular check-ups.]
# """


# # ==========================================
# # BUILD PROMPT — REPORT WITH ABNORMAL VALUES
# # ==========================================

# def build_abnormal_prompt(
#     abnormal_tests: list,
#     normal_tests: list,
#     rag_text: str
# ) -> str:

#     abnormal_text = format_tests_for_prompt(abnormal_tests)
#     normal_text   = format_tests_for_prompt(normal_tests[:15])

#     return f"""
# A patient's lab report has been analyzed. Several parameters are outside 
# the normal reference range and require explanation.

# === ABNORMAL FINDINGS ===
# {abnormal_text}

# === NORMAL FINDINGS ===
# {normal_text}

# === MEDICAL KNOWLEDGE BASE (Use this to explain findings accurately) ===
# {rag_text}

# Generate a DETAILED, PROFESSIONAL, and PATIENT-FRIENDLY medical summary.

# CRITICAL INSTRUCTIONS:
# - Use the Medical Knowledge Base to explain each abnormal finding accurately
# - For every abnormal parameter: explain what the test measures, what the 
#   abnormal value means, possible reasons, and the severity level
# - Severity levels: Mild (slightly outside range), Moderate (noticeably 
#   outside range), Significant (far outside range or clinically critical)
# - Cover all normal findings briefly to give the patient a complete picture
# - Do NOT diagnose diseases
# - Do NOT prescribe medications
# - Write minimum 600–900 words
# - Use calm, informative, non-alarming language

# USE THIS EXACT MARKDOWN FORMAT:

# # 🩺 Overall Health Summary

# [2–4 sentences summarizing the overall picture of the report — how many 
# parameters are abnormal vs normal, and the general impression.]

# # ⚠️ Abnormal Findings — Detailed Explanation

# [For EVERY single abnormal parameter, create a dedicated section:]

# ### [Test Name]
# **Your Value:** [value] [unit]  
# **Normal Range:** [reference range]  
# **Status:** [High / Low / Positive / etc.]  
# **Severity:** [Mild / Moderate / Significant]

# **What this test measures:**  
# [Explain in 1–2 plain-language sentences what this parameter is and why 
# it is measured. Use the medical knowledge base.]

# **What your result means:**  
# [Explain what it means when this value is high or low. What could cause 
# this? Use the knowledge base context. Keep it informative but calm.]

# **What you should know:**  
# [Any practical point the patient should be aware of — e.g., "This finding 
# alone is not diagnostic. Your doctor will correlate this with your symptoms."]

# ---

# # ✅ Normal Findings — Brief Overview

# [Briefly list and acknowledge the key parameters that are within normal 
# range, grouped by category where possible. 2–4 sentences or a short 
# bullet list. Reassure the patient about these findings.]

# # 💡 General Health Recommendations

# [Based on the abnormal findings, provide specific and relevant 
# recommendations. Include:]
# - Dietary advice relevant to the abnormal findings
# - Lifestyle modifications (exercise, sleep, stress)
# - Hydration and general wellness
# - Specific follow-up tests that may be advised (without prescribing)
# - Importance of follow-up with the treating doctor

# # 📋 Final Note

# [Remind the patient that this summary is AI-generated for informational 
# purposes only. Lab results must always be interpreted by a qualified 
# healthcare professional in the context of symptoms and clinical history. 
# Encourage them not to self-medicate or self-diagnose based on this report.]
# """


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(report_data: dict) -> str:
#     """
#     Generate a detailed, professional medical report summary using
#     Groq LLM grounded on RAG context and structured test data.

#     Args:
#         report_data: Dict containing:
#             - tests: list of structured test dicts (from llm_parser)
#             - rag_context: list of relevant knowledge base chunk strings

#     Returns:
#         Markdown-formatted summary string
#     """

#     try:

#         # ==========================================
#         # EXTRACT REPORT DATA
#         # ==========================================

#         data = report_data.get("data", report_data)

#         tests       = data.get("tests", [])
#         rag_context = data.get("rag_context", [])

#         if not tests:
#             return (
#                 "⚠️ No test data found in the report. "
#                 "Please check the uploaded file and try again."
#             )

#         # ==========================================
#         # SPLIT TESTS INTO NORMAL + ABNORMAL
#         # ==========================================

#         abnormal_tests = []
#         normal_tests   = []

#         for test in tests:

#             formatted = {
#                 "test_name":       test.get("test_name", ""),
#                 "value":           test.get("value", ""),
#                 "unit":            test.get("unit", ""),
#                 "reference_range": test.get("reference_range", ""),
#                 "status":          test.get("status", "")
#             }

#             if is_abnormal(test):
#                 abnormal_tests.append(formatted)
#             else:
#                 normal_tests.append(formatted)

#         # ==========================================
#         # PREPARE RAG CONTEXT
#         # ==========================================

#         # For abnormal reports: prioritize chunks relevant to abnormal params
#         # For normal reports: use all available context
#         if abnormal_tests:
#             rag_text = format_rag_context(rag_context, abnormal_tests)
#         else:
#             rag_text = "\n\n---\n\n".join(rag_context[:5])

#         # ==========================================
#         # SELECT PROMPT
#         # ==========================================

#         if not abnormal_tests:
#             prompt = build_normal_prompt(normal_tests)
#         else:
#             prompt = build_abnormal_prompt(
#                 abnormal_tests,
#                 normal_tests,
#                 rag_text
#             )

#         # ==========================================
#         # GROQ API CALL
#         # ==========================================

#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": SYSTEM_PROMPT
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2,    # Low temp for factual, consistent output
#             max_tokens=2500     # Enough for a thorough 700–900 word summary
#         )

#         summary = completion.choices[0].message.content

#         # ==========================================
#         # FALLBACK
#         # ==========================================

#         if not summary or not summary.strip():
#             return "⚠️ Unable to generate medical summary. Please try again."

#         return summary.strip()

#     except Exception as e:

#         print("SUMMARY ERROR:", str(e))
#         return f"⚠️ Error generating summary: {str(e)}"


# import os
# import logging
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# logger = logging.getLogger(__name__)

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )


# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test: dict) -> bool:
#     """Return True if the test result is outside the normal range."""

#     status = str(test.get("status", "")).strip().lower()

#     abnormal_keywords = [
#         "high",
#         "low",
#         "positive",
#         "abnormal",
#         "borderline",
#         "critical",
#         "reactive"
#     ]

#     return any(word in status for word in abnormal_keywords)


# # ==========================================
# # FORMAT TEST LIST FOR PROMPT
# # ==========================================

# def format_tests_for_prompt(tests: list) -> str:
#     """
#     Convert test list into a clean, readable text table for the LLM.
#     Structured text is far easier for LLMs to parse than raw JSON.
#     """

#     if not tests:
#         return "  (none)"

#     lines = []

#     for t in tests:
#         name   = t.get("test_name", "Unknown")
#         value  = t.get("value", "")
#         unit   = t.get("unit", "")
#         ref    = t.get("reference_range", "")
#         status = t.get("status", "")

#         line = f"  - {name}: {value} {unit}".strip()

#         if ref:
#             line += f"  |  Ref: {ref}"
#         if status:
#             line += f"  |  Status: {status}"

#         lines.append(line)

#     return "\n".join(lines)


# # ==========================================
# # SMART RAG CONTEXT SELECTOR
# # ==========================================

# def select_rag_context(rag_context: list, abnormal_tests: list) -> str:
#     """
#     Score and rank RAG chunks by relevance to the abnormal parameters.

#     - For abnormal reports: picks the top 6 most relevant chunks
#     - Falls back to first 5 chunks if no abnormal tests

#     The RAG chunks follow the format produced by the knowledge base files:
#       PARAMETER: X
#       TEST: Y
#       Meaning: ...
#       Normal Range: ...
#       Low Interpretation: ...
#       High Interpretation: ...
#     """

#     if not rag_context:
#         return "No additional medical knowledge available."

#     if not abnormal_tests:
#         # Normal report — just use the first few chunks for context
#         return "\n\n---\n\n".join(rag_context[:5])

#     # Build keyword set from abnormal test names for relevance scoring
#     keywords = set()
#     for t in abnormal_tests:
#         name = t.get("test_name", "").lower()
#         for word in name.split():
#             if len(word) > 2:   # skip tiny words like "of", "in"
#                 keywords.add(word)

#     # Score each chunk by keyword hits
#     scored = []
#     for chunk in rag_context:
#         chunk_lower = chunk.lower()
#         score = sum(1 for kw in keywords if kw in chunk_lower)
#         scored.append((score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)

#     # Take top 6 most relevant chunks
#     top_chunks = [chunk for _, chunk in scored[:6]]

#     return "\n\n---\n\n".join(top_chunks)


# # ==========================================
# # SYSTEM PROMPT
# # ==========================================

# SYSTEM_PROMPT = (
#     "You are a senior clinical AI assistant specialized in laboratory "
#     "report interpretation. You generate detailed, professional, and "
#     "patient-friendly medical report summaries.\n\n"
#     "Rules you always follow:\n"
#     "- Use clear, simple English that any patient can understand\n"
#     "- Cover every single finding — do not skip any parameter\n"
#     "- Ground all explanations in the provided Medical Knowledge Base\n"
#     "- Never diagnose diseases or prescribe medications\n"
#     "- Never create unnecessary panic — use calm, informative language\n"
#     "- Clearly classify severity: Mild / Moderate / Significant\n"
#     "- Always recommend consulting a qualified doctor for abnormal results"
# )


# # ==========================================
# # PROMPT — FULLY NORMAL REPORT
# # ==========================================

# def build_normal_prompt(normal_tests: list, rag_text: str) -> str:

#     tests_text = format_tests_for_prompt(normal_tests)

#     return f"""
# A patient's lab report has been fully analyzed.
# All {len(normal_tests)} parameters are within their normal reference ranges.

# LAB RESULTS:
# {tests_text}

# MEDICAL KNOWLEDGE BASE:
# {rag_text}

# Generate a detailed, professional, and reassuring medical summary.

# INSTRUCTIONS:
# - Use the Medical Knowledge Base to explain what each parameter measures
# - Group parameters by category where possible (Blood Count, Metabolic, 
#   Lipid Panel, Kidney, Liver, Thyroid, Vitamins, etc.)
# - For each parameter or group: explain what it measures and why being 
#   normal is a positive sign
# - Provide practical, specific health maintenance advice
# - Write at least 450-550 words
# - Do NOT diagnose diseases or prescribe medications

# REQUIRED FORMAT:

# # 🩺 Overall Health Summary

# [3–4 sentence overall impression. How many tests were run, 
# all within normal limits, general health picture.]

# # ✅ Normal Findings — Parameter by Parameter

# [Group by test category. For each parameter:]

# ### [Category / Parameter Name]
# **Value:** [value unit]
# **Reference Range:** [range]
# **What This Means:** [1–2 sentences explaining this parameter using the 
# knowledge base, and why a normal result is reassuring.]

# # 💡 Health Maintenance Recommendations

# [Specific, practical bullet-point advice covering:]
# - Diet and nutrition
# - Hydration
# - Physical activity
# - Sleep and stress management
# - Schedule for next routine check-up

# # 📋 Final Note

# [Remind the patient that even normal results should be reviewed with 
# their doctor alongside their symptoms. Encourage regular health check-ups.]
# """


# # ==========================================
# # PROMPT — REPORT WITH ABNORMAL VALUES
# # ==========================================

# def build_abnormal_prompt(
#     abnormal_tests: list,
#     normal_tests: list,
#     rag_text: str,
#     requires_review: bool
# ) -> str:

#     abnormal_text  = format_tests_for_prompt(abnormal_tests)
#     normal_text    = format_tests_for_prompt(normal_tests[:15])
#     review_warning = (
#         "\n⚠️ NOTE: This report was flagged for human review due to "
#         "low OCR confidence. Mention this in the Final Note.\n"
#         if requires_review else ""
#     )

#     return f"""
# A patient's lab report has been analyzed.
# {len(abnormal_tests)} parameter(s) are OUTSIDE the normal range.
# {len(normal_tests)} parameter(s) are within normal limits.
# {review_warning}
# === ABNORMAL FINDINGS ===
# {abnormal_text}

# === NORMAL FINDINGS ===
# {normal_text}

# === MEDICAL KNOWLEDGE BASE ===
# (Use this to accurately explain what each parameter measures, 
# what the abnormal value means, and possible causes.)

# {rag_text}

# Generate a DETAILED, PROFESSIONAL, PATIENT-FRIENDLY medical summary.

# CRITICAL INSTRUCTIONS:
# - Cover EVERY abnormal parameter — do not skip any
# - For each abnormal finding use ONLY the Medical Knowledge Base to explain 
#   the meaning, causes, and clinical significance
# - Classify severity for each: 
#     Mild   = value slightly outside range
#     Moderate = value noticeably outside range
#     Significant = value far outside range or clinically critical
# - Cover normal findings briefly to give a complete picture
# - Do NOT diagnose diseases or prescribe medications
# - Write minimum 650–900 words
# - Use calm, informative, non-alarming language throughout

# REQUIRED FORMAT:

# # 🩺 Overall Health Summary

# [3–5 sentences. How many parameters total, how many abnormal vs normal,
# and the general clinical picture. Keep it informative, not alarming.]

# # ⚠️ Abnormal Findings — Detailed Explanation

# [Create one section per abnormal parameter in this exact layout:]

# ### [Test Name]
# **Your Value:** [value] [unit]
# **Normal Range:** [reference_range]
# **Status:** [High / Low / Positive / Reactive / etc.]
# **Severity:** [Mild / Moderate / Significant]

# **What this test measures:**
# [1–2 sentences from the Knowledge Base explaining the biological role 
# of this parameter and why it is measured.]

# **What your result means:**
# [2–3 sentences explaining what a high/low value indicates. 
# List 2–3 common causes. Use the Knowledge Base. Stay calm and factual.]

# **What you should know:**
# [1–2 practical sentences — e.g. whether this finding alone is diagnostic,
# whether it needs follow-up testing, or what symptoms to watch for.]

# ---

# # ✅ Normal Findings — Brief Overview

# [Short paragraph or grouped bullet list of normal parameters. 
# Group by category (CBC, Kidney, Liver, etc.) where possible.
# Reassure the patient about these findings.]

# # 💡 Recommendations

# [Targeted, specific advice based directly on the abnormal findings found 
# in this report. Include:]
# - Diet changes relevant to these specific findings
# - Lifestyle modifications (exercise, sleep, alcohol, smoking if relevant)
# - Hydration advice
# - Follow-up tests that are commonly advised for these findings
#   (present as suggestions, not prescriptions)
# - Urgency of seeing a doctor (routine follow-up vs prompt consultation)

# # 📋 Final Note

# [State clearly: this is an AI-generated summary for informational purposes 
# only. It is not a medical diagnosis. All results must be interpreted by a 
# qualified healthcare professional alongside symptoms and clinical history. 
# The patient should not self-medicate or self-diagnose based on this report.
# {"Mention that the report was flagged for human review due to OCR confidence." if requires_review else ""}]
# """


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(pipeline_result: dict) -> str:
#     """
#     Generate a detailed, professional medical report summary.

#     Receives the direct output of process_report_enhanced() from pipeline.py:

#         pipeline_result = {
#             "tests":          [ {test_name, value, unit, reference_range, status}, ... ],
#             "rag_context":    [ "PARAMETER: ...\nMeaning: ...", ... ],
#             "metrics":        { "confidence": 0.91, "method": "...", ... },
#             "requires_review": False,
#             "cleaned_text":   "..."
#         }

#     Returns:
#         Markdown-formatted summary string ready to display to the patient.
#     """

#     try:

#         # ==========================================
#         # UNPACK PIPELINE OUTPUT
#         # ==========================================

#         # pipeline.py returns a flat dict — no nested "data" wrapper
#         tests           = pipeline_result.get("tests", [])
#         rag_context     = pipeline_result.get("rag_context", [])
#         requires_review = pipeline_result.get("requires_review", False)
#         metrics         = pipeline_result.get("metrics", {})

#         logger.info(
#             f"Generating summary | tests={len(tests)} "
#             f"| rag_chunks={len(rag_context)} "
#             f"| method={metrics.get('method', 'unknown')} "
#             f"| requires_review={requires_review}"
#         )

#         if not tests:
#             return (
#                 "⚠️ No test data found in the report. "
#                 "Please check the uploaded file and try again."
#             )

#         # ==========================================
#         # SPLIT INTO NORMAL / ABNORMAL
#         # ==========================================

#         abnormal_tests = []
#         normal_tests   = []

#         for test in tests:

#             clean = {
#                 "test_name":       test.get("test_name", ""),
#                 "value":           test.get("value", ""),
#                 "unit":            test.get("unit", ""),
#                 "reference_range": test.get("reference_range", ""),
#                 "status":          test.get("status", "")
#             }

#             if is_abnormal(test):
#                 abnormal_tests.append(clean)
#             else:
#                 normal_tests.append(clean)

#         logger.info(
#             f"Split complete | abnormal={len(abnormal_tests)} "
#             f"| normal={len(normal_tests)}"
#         )

#         # ==========================================
#         # SELECT RELEVANT RAG CONTEXT
#         # ==========================================

#         rag_text = select_rag_context(rag_context, abnormal_tests)

#         # ==========================================
#         # BUILD PROMPT
#         # ==========================================

#         if not abnormal_tests:
#             prompt = build_normal_prompt(normal_tests, rag_text)
#         else:
#             prompt = build_abnormal_prompt(
#                 abnormal_tests,
#                 normal_tests,
#                 rag_text,
#                 requires_review
#             )

#         # ==========================================
#         # GROQ API CALL
#         # ==========================================

#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": SYSTEM_PROMPT
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2,   # Low for factual, consistent clinical output
#             max_tokens=2500    # Covers 700–900 word summary comfortably
#         )

#         summary = completion.choices[0].message.content

#         # ==========================================
#         # FALLBACK
#         # ==========================================

#         if not summary or not summary.strip():
#             logger.warning("Groq returned empty response")
#             return "⚠️ Unable to generate medical summary. Please try again."

#         logger.info("Summary generated successfully")
#         return summary.strip()

#     except Exception as e:

#         logger.error(f"generate_medical_summary failed: {e}")
#         return f"⚠️ Error generating summary: {str(e)}"
# import os
# import logging
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# logger = logging.getLogger(__name__)

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )


# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test: dict) -> bool:
#     """Return True if the test result is outside the normal range."""

#     status = str(test.get("status", "")).strip().lower()

#     abnormal_keywords = [
#         "high",
#         "low",
#         "positive",
#         "abnormal",
#         "borderline",
#         "critical",
#         "reactive"
#     ]

#     return any(word in status for word in abnormal_keywords)


# # ==========================================
# # FORMAT TEST LIST FOR PROMPT
# # ==========================================

# def format_tests_for_prompt(tests: list) -> str:
#     """
#     Convert test list into a clean, readable text table for the LLM.
#     Structured text is far easier for LLMs to parse than raw JSON.
#     """

#     if not tests:
#         return "  (none)"

#     lines = []

#     for t in tests:
#         name   = t.get("test_name", "Unknown")
#         value  = t.get("value", "")
#         unit   = t.get("unit", "")
#         ref    = t.get("reference_range", "")
#         status = t.get("status", "")

#         line = f"  - {name}: {value} {unit}".strip()

#         if ref:
#             line += f"  |  Ref: {ref}"
#         if status:
#             line += f"  |  Status: {status}"

#         lines.append(line)

#     return "\n".join(lines)


# # ==========================================
# # SMART RAG CONTEXT SELECTOR
# # ==========================================

# def select_rag_context(rag_context: list, abnormal_tests: list) -> str:
#     """
#     Score and rank RAG chunks by relevance to the abnormal parameters.
#     """

#     if not rag_context:
#         return "No additional medical knowledge available."

#     if not abnormal_tests:
#         return "\n\n---\n\n".join(rag_context[:5])

#     keywords = set()
#     for t in abnormal_tests:
#         name = t.get("test_name", "").lower()
#         for word in name.split():
#             if len(word) > 2:
#                 keywords.add(word)

#     scored = []
#     for chunk in rag_context:
#         chunk_lower = chunk.lower()
#         score = sum(1 for kw in keywords if kw in chunk_lower)
#         scored.append((score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)
#     top_chunks = [chunk for _, chunk in scored[:6]]

#     return "\n\n---\n\n".join(top_chunks)


# # ==========================================
# # SYSTEM PROMPT
# # ==========================================

# SYSTEM_PROMPT = """You are a warm, caring doctor writing a personal letter
# to your patient after reviewing their lab report. Your tone is like a
# trusted family doctor — calm, reassuring, clear, and genuinely helpful.

# You explain things the way a good doctor would to a patient sitting
# across from them: no jargon, no robotic templates, no unnecessary alarm.

# You always:
# - Write in flowing, natural paragraphs — not stiff bullet-point templates
# - Use "your" and "you" to speak directly to the patient
# - Explain what each test actually IS before saying what the result means
# - Acknowledge concern where needed but always end with reassurance and a path forward
# - Never diagnose, never prescribe — always guide toward seeing their doctor
# - Keep caretakers in mind too — write so a family member reading alongside
#   the patient also understands everything clearly"""


# # ==========================================
# # PROMPT — FULLY NORMAL REPORT
# # ==========================================

# def build_normal_prompt(normal_tests: list, rag_text: str) -> str:

#     tests_text = format_tests_for_prompt(normal_tests)

#     return f"""
# You are writing a warm, reassuring letter to a patient whose lab report
# has come back completely normal. All {len(normal_tests)} parameters
# are within their healthy reference ranges.

# LAB RESULTS:
# {tests_text}

# MEDICAL KNOWLEDGE BASE (use this to explain what each test measures):
# {rag_text}

# Write this summary as a caring doctor would — warm, personal, clear.
# Imagine you are sitting across from the patient and their family member,
# and you are walking them through the good news together.

# TONE RULES:
# - Speak directly to the patient using "you" and "your"
# - Use simple everyday language — avoid medical jargon
# - Be genuinely warm and encouraging, not clinically cold
# - Write in natural paragraphs, not stiff template blocks
# - Do NOT diagnose or prescribe anything

# WRITE THIS EXACT STRUCTURE:

# # 🩺 Your Health Report Summary

# [Open warmly — congratulate them on the good results. Give a 2-3 sentence
# human overview of what the report shows. Example: "I am happy to share that
# your lab results look very reassuring..."]

# # 📊 What Your Results Show

# [Walk through the results grouped by category — Blood Count, Lipid Panel,
# etc. For each group write 2-4 warm sentences explaining:
#   - What these tests measure in plain English
#   - What it means that their values are in the healthy range
#   - Why this is a positive sign for their health
# Do NOT use bold label fields like "Value:" "Range:" — weave the numbers
# naturally into the sentences instead.
# Example: "Your hemoglobin came in at 14.5 g/dL, which sits comfortably
# within the healthy range of 13 to 16.5. This tells us your blood is
# carrying oxygen efficiently — a sign your red blood cells are doing
# their job well."]

# # 💛 Keeping Your Health on Track

# [Write 1 warm paragraph of lifestyle advice relevant to the tests run.
# Then follow with 4-5 short, friendly bullet points — diet, movement,
# hydration, sleep, and when to come back for the next check-up.
# Make the advice feel encouraging, not like a prescription.]

# # 📋 A Note Before You Go

# [Close warmly. Remind them in a human way that even great results are
# best reviewed with their doctor alongside their symptoms. Encourage
# regular check-ups. End on a positive, caring note.]
# """


# # ==========================================
# # PROMPT — REPORT WITH ABNORMAL VALUES
# # ==========================================

# def build_abnormal_prompt(
#     abnormal_tests: list,
#     normal_tests: list,
#     rag_text: str,
#     requires_review: bool
# ) -> str:

#     abnormal_text = format_tests_for_prompt(abnormal_tests)
#     normal_text   = format_tests_for_prompt(normal_tests[:15])

#     review_note = (
#         "\nNOTE FOR FINAL SECTION: This report was flagged for manual "
#         "review due to OCR processing confidence. Mention this gently "
#         "in the closing note.\n"
#         if requires_review else ""
#     )

#     closing_review = (
#         "- Gently mention the report was flagged for additional manual review."
#         if requires_review else ""
#     )

#     return f"""
# You are writing a warm, clear, caring letter to a patient after reviewing
# their lab report. {len(abnormal_tests)} of their results need attention,
# while {len(normal_tests)} results are within healthy ranges.
# {review_note}
# RESULTS NEEDING ATTENTION:
# {abnormal_text}

# RESULTS WITHIN NORMAL RANGE:
# {normal_text}

# MEDICAL KNOWLEDGE BASE:
# (Use this to accurately explain what each test measures and what the
# abnormal value means. Do not use knowledge outside of this context.)
# {rag_text}

# Write this as a trusted family doctor would speak to their patient and
# the patient's family — warm, honest, calm, and genuinely helpful.
# The patient may be anxious. Your job is to inform without alarming,
# and to always end with a clear, reassuring path forward.

# TONE RULES:
# - Speak directly: use "you", "your", "we"
# - No medical jargon — if a term is needed, immediately explain it in
#   plain English in the same sentence
# - Write in natural flowing paragraphs — avoid robotic bold label fields
# - Weave values naturally into sentences rather than listing them as
#   "Your Value: X | Normal Range: Y"
# - Every abnormal finding must end with reassurance and next steps
# - Do NOT diagnose or prescribe
# - Minimum 700 words — be thorough, the patient deserves a full explanation
# - Caretakers should be able to read this alongside the patient and
#   understand everything without a medical background

# WRITE THIS EXACT STRUCTURE:

# # 🩺 Your Health Report — A Personal Summary

# [Open warmly in 3-4 sentences. Acknowledge that some results need
# attention but frame it positively — "This is exactly why we run these
# tests." Give a gentle overall picture without leading with alarm.
# Example: "Thank you for getting your blood work done — it takes courage
# and care to stay on top of your health. After reviewing your results,
# most of your parameters look healthy and reassuring. There are a few
# values that are slightly outside the normal range, and I want to walk
# you through each one clearly so you know exactly what they mean and
# what steps to consider next."]

# # 🔍 Results That Need Your Attention

# [For EVERY single abnormal result write one dedicated section.
# Each section must feel like a doctor personally explaining it — NOT a
# template form. Use this natural flow for each:]

# ## [Test Name] — [High / Low / Borderline]

# [Open with 1-2 sentences explaining what this test actually measures
# in plain everyday language. Use the Medical Knowledge Base.]

# [Next, 2-3 sentences explaining what the patient's specific value means.
# Mention the actual number and the normal range naturally in the sentence.
# Example: "Your WBC count came back at 10,570 — just slightly above the
# upper limit of 10,000. This tells us your immune system is a little more
# active than usual right now, which can happen for many common reasons."]

# [Then 1-2 sentences on common reasons this happens — list 2-3 causes
# calmly. Frame them as possibilities, not diagnoses.]

# [Close each section with 1 reassuring sentence and a practical next step.
# Example: "This is a mild elevation and on its own is not a cause for
# alarm — your doctor will look at this alongside your other results and
# any symptoms you may have been experiencing."]

# [Add severity as a single line at the end: Severity: Mild / Moderate / Significant]

# ---

# # ✅ What Is Looking Good

# [Write 2-3 warm sentences acknowledging the normal results. Group them
# by category. Make the patient feel genuinely reassured about what IS
# working well. Do not just list parameters — explain what each group of
# normal results means for their health in plain language.]

# # 💛 Steps You Can Take

# [Write this section as personal, caring advice — like a doctor giving
# practical guidance at the end of an appointment.

# Open with 1 warm paragraph connecting the advice specifically to what
# was found in THIS report. Then give 5-6 specific, friendly bullet points:
# - What to eat or avoid based on these specific findings
# - Movement and exercise advice relevant to these results
# - Sleep and stress guidance if relevant
# - Hydration
# - Which follow-up tests are typically recommended for these findings
#   (framed as "your doctor may suggest..." not as prescriptions)
# - How soon to follow up with their doctor (routine vs prompt)]

# # 📋 Before You Go

# [Close the letter warmly and humanly. In 3-4 sentences:
# - Remind them this is an AI-assisted summary to help them understand
#   their report, not a medical diagnosis
# - Encourage them not to worry alone — to bring this summary to their
#   doctor and ask questions
# - End with a genuinely warm closing line
# {closing_review}]
# """


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(pipeline_result: dict) -> str:
#     """
#     Generate a warm, patient-friendly medical report summary.

#     Receives the direct output of process_report_enhanced() from pipeline.py:

#         pipeline_result = {
#             "tests":           [ {test_name, value, unit, reference_range, status}, ... ],
#             "rag_context":     [ "PARAMETER: ...\nMeaning: ...", ... ],
#             "metrics":         { "confidence": 0.91, "method": "...", ... },
#             "requires_review": False,
#             "cleaned_text":    "..."
#         }

#     Returns:
#         Markdown-formatted summary string ready to display to the patient.
#     """

#     try:

#         # ==========================================
#         # UNPACK PIPELINE OUTPUT
#         # ==========================================

#         tests           = pipeline_result.get("tests", [])
#         rag_context     = pipeline_result.get("rag_context", [])
#         requires_review = pipeline_result.get("requires_review", False)
#         metrics         = pipeline_result.get("metrics", {})

#         logger.info(
#             f"Generating summary | tests={len(tests)} "
#             f"| rag_chunks={len(rag_context)} "
#             f"| method={metrics.get('method', 'unknown')} "
#             f"| requires_review={requires_review}"
#         )

#         if not tests:
#             return (
#                 "No test data found in the report. "
#                 "Please check the uploaded file and try again."
#             )

#         # ==========================================
#         # SPLIT INTO NORMAL / ABNORMAL
#         # ==========================================

#         abnormal_tests = []
#         normal_tests   = []

#         for test in tests:

#             clean = {
#                 "test_name":       test.get("test_name", ""),
#                 "value":           test.get("value", ""),
#                 "unit":            test.get("unit", ""),
#                 "reference_range": test.get("reference_range", ""),
#                 "status":          test.get("status", "")
#             }

#             if is_abnormal(test):
#                 abnormal_tests.append(clean)
#             else:
#                 normal_tests.append(clean)

#         logger.info(
#             f"Split complete | abnormal={len(abnormal_tests)} "
#             f"| normal={len(normal_tests)}"
#         )

#         # ==========================================
#         # SELECT RELEVANT RAG CONTEXT
#         # ==========================================

#         rag_text = select_rag_context(rag_context, abnormal_tests)

#         # ==========================================
#         # BUILD PROMPT
#         # ==========================================

#         if not abnormal_tests:
#             prompt = build_normal_prompt(normal_tests, rag_text)
#         else:
#             prompt = build_abnormal_prompt(
#                 abnormal_tests,
#                 normal_tests,
#                 rag_text,
#                 requires_review
#             )

#         # ==========================================
#         # GROQ API CALL
#         # ==========================================

#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": SYSTEM_PROMPT
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.4,   # Slightly higher for warmer, more natural writing
#             max_tokens=2800    # Extra room for flowing prose
#         )

#         summary = completion.choices[0].message.content

#         # ==========================================
#         # FALLBACK
#         # ==========================================

#         if not summary or not summary.strip():
#             logger.warning("Groq returned empty response")
#             return "Unable to generate medical summary. Please try again."

#         logger.info("Summary generated successfully")
#         return summary.strip()

#     except Exception as e:

#         logger.error(f"generate_medical_summary failed: {e}")
#         return f"Error generating summary: {str(e)}"


# import os
# import logging
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# logger = logging.getLogger(__name__)

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )


# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test: dict) -> bool:

#     status = str(test.get("status", "")).strip().lower()

#     abnormal_keywords = [
#         "high", "low", "positive", "abnormal",
#         "borderline", "critical", "reactive"
#     ]

#     return any(word in status for word in abnormal_keywords)


# # ==========================================
# # FORMAT TEST LIST FOR PROMPT
# # ==========================================

# def format_tests_for_prompt(tests: list) -> str:

#     if not tests:
#         return "  (none)"

#     lines = []

#     for t in tests:
#         name   = t.get("test_name", "Unknown")
#         value  = t.get("value", "")
#         unit   = t.get("unit", "")
#         ref    = t.get("reference_range", "")
#         status = t.get("status", "")

#         line = f"  - {name}: {value} {unit}".strip()

#         if ref:
#             line += f"  |  Ref: {ref}"
#         if status:
#             line += f"  |  Status: {status}"

#         lines.append(line)

#     return "\n".join(lines)


# # ==========================================
# # SMART RAG CONTEXT SELECTOR
# # ==========================================

# def select_rag_context(rag_context: list, abnormal_tests: list) -> str:

#     if not rag_context:
#         return "No additional medical knowledge available."

#     if not abnormal_tests:
#         return "\n\n---\n\n".join(rag_context[:5])

#     keywords = set()
#     for t in abnormal_tests:
#         name = t.get("test_name", "").lower()
#         for word in name.split():
#             if len(word) > 2:
#                 keywords.add(word)

#     scored = []
#     for chunk in rag_context:
#         chunk_lower = chunk.lower()
#         score = sum(1 for kw in keywords if kw in chunk_lower)
#         scored.append((score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)
#     top_chunks = [chunk for _, chunk in scored[:6]]

#     return "\n\n---\n\n".join(top_chunks)


# # ==========================================
# # SYSTEM PROMPT
# # ==========================================

# SYSTEM_PROMPT = """You are a clinical report writer producing structured 
# medical summaries for patients and their caregivers.

# Style rules — follow strictly:
# - Professional and concise. No filler sentences, no over-explanation.
# - Patient-readable: plain English, but not dumbed down. 
#   If using a medical term, define it once in parentheses.
# - Direct and factual. State what the value is, what it means, why it matters.
# - Never alarming, never dismissive.
# - No greetings, no sign-offs, no "I hope you..." language.
# - No bullet walls. Use short focused paragraphs under each finding.
# - Never diagnose. Never prescribe. Always recommend doctor follow-up for abnormal results."""


# # ==========================================
# # PROMPT — FULLY NORMAL REPORT
# # ==========================================

# def build_normal_prompt(normal_tests: list, rag_text: str) -> str:

#     tests_text = format_tests_for_prompt(normal_tests)

#     return f"""
# All {len(normal_tests)} parameters in this lab report are within normal limits.

# LAB RESULTS:
# {tests_text}

# MEDICAL KNOWLEDGE BASE:
# {rag_text}

# Write a concise, professional lab report summary. 
# Group findings by category (CBC, Lipid Panel, etc.).
# For each group: one short paragraph — what was tested, what the values 
# show, and what that means for this person's health. 
# No fluff. No greetings. No sign-offs.
# End with a brief general health advice section and a one-line disclaimer.

# FORMAT:

# ## Overall Impression
# [2 sentences. All clear, concise statement of overall result.]

# ## Test Results by Category

# ### [Category Name]
# [1 short paragraph: what these tests measure + what normal values mean here.
# Mention actual values. Keep it under 4 sentences per category.]

# ## Health Recommendations
# [4-5 tight bullet points. Specific, actionable, relevant to the tests run.]

# ## Note
# [One line: results should be reviewed with a qualified doctor.]
# """


# # ==========================================
# # PROMPT — REPORT WITH ABNORMAL VALUES
# # ==========================================

# def build_abnormal_prompt(
#     abnormal_tests: list,
#     normal_tests: list,
#     rag_text: str,
#     requires_review: bool
# ) -> str:

#     abnormal_text = format_tests_for_prompt(abnormal_tests)
#     normal_text   = format_tests_for_prompt(normal_tests[:15])

#     review_line = (
#         "\nFlag at end: This report was processed with low OCR confidence "
#         "and should be verified against the original document.\n"
#         if requires_review else ""
#     )

#     return f"""
# Lab report analysis: {len(abnormal_tests)} abnormal, {len(normal_tests)} normal.
# {review_line}
# ABNORMAL:
# {abnormal_text}

# NORMAL:
# {normal_text}

# MEDICAL KNOWLEDGE BASE:
# {rag_text}

# Write a structured, professional clinical summary.
# Tone: clear, direct, calm. Like a doctor's written report — not a letter, 
# not a conversation. Patient and caregiver should both understand it easily.

# STRICT RULES:
# - No greetings, no sign-offs, no "I" statements
# - No filler like "It's important to note that..." or "Please remember..."
# - State facts directly: what the test measures, what the value is, 
#   what it means, how significant it is
# - Use the Medical Knowledge Base for accuracy
# - Cover every abnormal result — no skipping
# - Keep each finding tight: 3-4 sentences max
# - Total length: 500-700 words

# FORMAT:

# ## Summary
# [3 sentences max. Total tests, how many flagged, general clinical picture.]

# ## Findings Requiring Attention

# ### [Test Name]
# **Result:** [value unit] — [High/Low] (Normal: [range])
# **Severity:** Mild / Moderate / Significant

# [2-3 sentences: what this test measures, what this specific value 
# indicates, and the most likely clinical significance. Use the knowledge 
# base. No vague language — be specific about what elevated/low means.]

# [1 sentence: recommended next step or what the doctor will assess.]

# ---

# [Repeat for every abnormal result]

# ## Normal Findings
# [1-2 sentences per category. State what was tested and confirm it's within 
# range. No need to explain every parameter — group them.]

# ## Recommendations
# [5-6 bullet points. Specific to THIS report's findings. 
# Diet, lifestyle, follow-up tests, urgency of doctor visit.
# Framed as clinical guidance, not life coaching.]

# ## Disclaimer
# [One sentence. AI-generated summary, not a diagnosis, consult your doctor.{" Report flagged for OCR review." if requires_review else ""}]
# """


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(pipeline_result: dict) -> str:
#     """
#     Generate a professional, concise medical report summary.

#     Receives direct output of process_report_enhanced():
#         {
#             "tests":           [...],
#             "rag_context":     [...],
#             "metrics":         {...},
#             "requires_review": bool,
#             "cleaned_text":    "..."
#         }
#     """

#     try:

#         tests           = pipeline_result.get("tests", [])
#         rag_context     = pipeline_result.get("rag_context", [])
#         requires_review = pipeline_result.get("requires_review", False)
#         metrics         = pipeline_result.get("metrics", {})

#         logger.info(
#             f"Generating summary | tests={len(tests)} "
#             f"| rag_chunks={len(rag_context)} "
#             f"| method={metrics.get('method', 'unknown')} "
#             f"| requires_review={requires_review}"
#         )

#         if not tests:
#             return (
#                 "No test data found in the report. "
#                 "Please check the uploaded file and try again."
#             )

#         # ==========================================
#         # SPLIT INTO NORMAL / ABNORMAL
#         # ==========================================

#         abnormal_tests = []
#         normal_tests   = []

#         for test in tests:

#             clean = {
#                 "test_name":       test.get("test_name", ""),
#                 "value":           test.get("value", ""),
#                 "unit":            test.get("unit", ""),
#                 "reference_range": test.get("reference_range", ""),
#                 "status":          test.get("status", "")
#             }

#             if is_abnormal(test):
#                 abnormal_tests.append(clean)
#             else:
#                 normal_tests.append(clean)

#         logger.info(
#             f"Split | abnormal={len(abnormal_tests)} | normal={len(normal_tests)}"
#         )

#         # ==========================================
#         # SELECT RELEVANT RAG CONTEXT
#         # ==========================================

#         rag_text = select_rag_context(rag_context, abnormal_tests)

#         # ==========================================
#         # BUILD PROMPT
#         # ==========================================

#         if not abnormal_tests:
#             prompt = build_normal_prompt(normal_tests, rag_text)
#         else:
#             prompt = build_abnormal_prompt(
#                 abnormal_tests,
#                 normal_tests,
#                 rag_text,
#                 requires_review
#             )

#         # ==========================================
#         # GROQ API CALL
#         # ==========================================

#         completion = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": SYSTEM_PROMPT
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2,
#             max_tokens=2500
#         )

#         summary = completion.choices[0].message.content

#         if not summary or not summary.strip():
#             logger.warning("Groq returned empty response")
#             return "Unable to generate medical summary. Please try again."

#         logger.info("Summary generated successfully")
#         return summary.strip()

#     except Exception as e:

#         logger.error(f"generate_medical_summary failed: {e}")
#         return f"Error generating summary: {str(e)}"
# import os
# import logging
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# logger = logging.getLogger(__name__)

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(
#     api_key=os.getenv("GROQ_API_KEY")
# )


# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test: dict) -> bool:

#     status = str(test.get("status", "")).strip().lower()

#     abnormal_keywords = [
#         "high", "low", "positive", "abnormal",
#         "borderline", "critical", "reactive"
#     ]

#     return any(word in status for word in abnormal_keywords)


# # ==========================================
# # FORMAT TEST LIST FOR PROMPT
# # ==========================================

# def format_tests_for_prompt(tests: list) -> str:

#     if not tests:
#         return "  (none)"

#     lines = []

#     for t in tests:
#         name   = t.get("test_name", "Unknown")
#         value  = t.get("value", "")
#         unit   = t.get("unit", "")
#         ref    = t.get("reference_range", "")
#         status = t.get("status", "")

#         line = f"  - {name}: {value} {unit}".strip()

#         if ref:
#             line += f"  |  Ref: {ref}"
#         if status:
#             line += f"  |  Status: {status}"

#         lines.append(line)

#     return "\n".join(lines)


# # ==========================================
# # SMART RAG CONTEXT SELECTOR
# # ==========================================

# def select_rag_context(rag_context: list, abnormal_tests: list) -> str:

#     if not rag_context:
#         return "No additional medical knowledge available."

#     if not abnormal_tests:
#         return "\n\n---\n\n".join(rag_context[:5])

#     keywords = set()
#     for t in abnormal_tests:
#         name = t.get("test_name", "").lower()
#         for word in name.split():
#             if len(word) > 2:
#                 keywords.add(word)

#     scored = []
#     for chunk in rag_context:
#         chunk_lower = chunk.lower()
#         score = sum(1 for kw in keywords if kw in chunk_lower)
#         scored.append((score, chunk))

#     scored.sort(key=lambda x: x[0], reverse=True)
#     top_chunks = [chunk for _, chunk in scored[:6]]

#     return "\n\n---\n\n".join(top_chunks)


# # ==========================================
# # SYSTEM PROMPT
# # ==========================================

# SYSTEM_PROMPT = """You are a clinical report writer producing structured
# medical summaries for patients and their caregivers.

# Style rules — follow strictly:
# - Professional and concise. No filler sentences, no over-explanation.
# - Plain language first. Avoid medical jargon wherever possible.
#   When a medical term is unavoidable, immediately follow it with a simple
#   plain-English explanation in parentheses.
#   Example: "neutrophils (the white blood cells your body sends to fight infection)"
#   Never use a medical term alone and move on without explaining it.
# - Assume the reader has zero medical background. Every sentence should be
#   understandable by someone with no medical training.
# - Replace jargon with everyday equivalents wherever possible:
#     "elevated" → "higher than normal"
#     "lipid" → "fat"
#     "myocardial" → "heart muscle"
#     "hematocrit" → "the percentage of your blood made up of red blood cells"
# - Direct and factual. State what the value is, what it means, why it matters.
# - Never alarming, never dismissive.
# - No greetings, no sign-offs, no "I hope you..." language.
# - No bullet walls. Use short focused paragraphs under each finding.
# - Never diagnose. Never prescribe. Always recommend doctor follow-up for abnormal results."""


# # ==========================================
# # PROMPT — FULLY NORMAL REPORT
# # ==========================================

# def build_normal_prompt(normal_tests: list, rag_text: str) -> str:

#     tests_text = format_tests_for_prompt(normal_tests)

#     return f"""
# All {len(normal_tests)} parameters in this lab report are within normal limits.

# LAB RESULTS:
# {tests_text}

# MEDICAL KNOWLEDGE BASE:
# {rag_text}

# Write a concise, professional lab report summary.
# Group findings by category (CBC, Lipid Panel, etc.).
# For each group: one short paragraph — what was tested, what the values
# show, and what that means for this person's health.
# No fluff. No greetings. No sign-offs.
# End with a brief general health advice section and a one-line disclaimer.

# PLAIN LANGUAGE RULE: Avoid all medical jargon. Use everyday words.
# When a test name or term must appear, explain what it means in simple 
# words immediately after. Example: "Your MCV (the average size of your 
# red blood cells) is 90.3 fL — comfortably within the normal range."
# Write so someone with no medical background understands every sentence.

# FORMAT:

# ## Overall Impression
# [2 sentences. All clear, concise statement of overall result.]

# ## Test Results by Category

# ### [Category Name]
# [1 short paragraph: what these tests measure + what normal values mean here.
# Mention actual values. Keep it under 4 sentences per category.]

# ## Health Recommendations
# [4-5 tight bullet points. Specific, actionable, relevant to the tests run.]

# ## Note
# [One line: results should be reviewed with a qualified doctor.]
# """


# # ==========================================
# # PROMPT — REPORT WITH ABNORMAL VALUES
# # ==========================================

# def build_abnormal_prompt(
#     abnormal_tests: list,
#     normal_tests: list,
#     rag_text: str,
#     requires_review: bool
# ) -> str:

#     abnormal_text = format_tests_for_prompt(abnormal_tests)
#     normal_text   = format_tests_for_prompt(normal_tests[:15])

#     review_line = (
#         "\nFlag at end: This report was processed with low OCR confidence "
#         "and should be verified against the original document.\n"
#         if requires_review else ""
#     )

#     return f"""
# Lab report analysis: {len(abnormal_tests)} abnormal, {len(normal_tests)} normal.
# {review_line}
# ABNORMAL:
# {abnormal_text}

# NORMAL:
# {normal_text}

# MEDICAL KNOWLEDGE BASE:
# {rag_text}

# Write a structured, professional clinical summary.
# Tone: clear, direct, calm. Like a doctor's written report — not a letter, 
# not a conversation. Patient and caregiver should both understand it easily.

# STRICT RULES:
# - No greetings, no sign-offs, no "I" statements
# - No filler like "It's important to note that..." or "Please remember..."
# - State facts directly: what the test measures, what the value is,
#   what it means, how significant it is
# - Use the Medical Knowledge Base for accuracy
# - Cover every abnormal result — no skipping
# - Keep each finding tight: 3-4 sentences max
# - Total length: 500-700 words
# - PLAIN LANGUAGE: avoid medical jargon. When a technical term must appear,
#   explain it immediately in plain words. Replace wherever possible:
#   "leukocytes" → "white blood cells", "triglycerides" → "fats in your blood",
#   "hematocrit" → "red blood cell percentage", "myocardial" → "heart muscle"
#   Write as if explaining to someone who has never had a blood test before.

# FORMAT:

# ## Summary
# [3 sentences max. Total tests, how many flagged, general clinical picture.]

# ## Findings Requiring Attention

# ### [Test Name]
# **Result:** [value unit] — [High/Low] (Normal: [range])
# **Severity:** Mild / Moderate / Significant

# [2-3 sentences: what this test measures, what this specific value 
# indicates, and the most likely clinical significance. Use the knowledge 
# base. No vague language — be specific about what elevated/low means.]

# [1 sentence: recommended next step or what the doctor will assess.]

# ---

# [Repeat for every abnormal result]

# ## Normal Findings
# [1-2 sentences per category. State what was tested and confirm it's within 
# range. No need to explain every parameter — group them.]

# ## Recommendations
# [5-6 bullet points. Specific to THIS report's findings. 
# Diet, lifestyle, follow-up tests, urgency of doctor visit.
# Framed as clinical guidance, not life coaching.]

# ## Disclaimer
# [One sentence. AI-generated summary, not a diagnosis, consult your doctor.{" Report flagged for OCR review." if requires_review else ""}]
# """


# # ==========================================
# # MAIN SUMMARY FUNCTION
# # ==========================================

# def generate_medical_summary(pipeline_result: dict) -> str:
#     """
#     Generate a professional, concise medical report summary.

#     Receives direct output of process_report_enhanced():
#         {
#             "tests":           [...],
#             "rag_context":     [...],
#             "metrics":         {...},
#             "requires_review": bool,
#             "cleaned_text":    "..."
#         }
#     """

#     try:

#         tests           = pipeline_result.get("tests", [])
#         rag_context     = pipeline_result.get("rag_context", [])
#         requires_review = pipeline_result.get("requires_review", False)
#         metrics         = pipeline_result.get("metrics", {})

#         logger.info(
#             f"Generating summary | tests={len(tests)} "
#             f"| rag_chunks={len(rag_context)} "
#             f"| method={metrics.get('method', 'unknown')} "
#             f"| requires_review={requires_review}"
#         )

#         if not tests:
#             return (
#                 "No test data found in the report. "
#                 "Please check the uploaded file and try again."
#             )

#         # ==========================================
#         # SPLIT INTO NORMAL / ABNORMAL
#         # ==========================================

#         abnormal_tests = []
#         normal_tests   = []

#         for test in tests:

#             clean = {
#                 "test_name":       test.get("test_name", ""),
#                 "value":           test.get("value", ""),
#                 "unit":            test.get("unit", ""),
#                 "reference_range": test.get("reference_range", ""),
#                 "status":          test.get("status", "")
#             }

#             if is_abnormal(test):
#                 abnormal_tests.append(clean)
#             else:
#                 normal_tests.append(clean)

#         logger.info(
#             f"Split | abnormal={len(abnormal_tests)} | normal={len(normal_tests)}"
#         )

#         # ==========================================
#         # SELECT RELEVANT RAG CONTEXT
#         # ==========================================

#         rag_text = select_rag_context(rag_context, abnormal_tests)

#         # ==========================================
#         # BUILD PROMPT
#         # ==========================================

#         if not abnormal_tests:
#             prompt = build_normal_prompt(normal_tests, rag_text)
#         else:
#             prompt = build_abnormal_prompt(
#                 abnormal_tests,
#                 normal_tests,
#                 rag_text,
#                 requires_review
#             )

#         # ==========================================
#         # GROQ API CALL
#         # ==========================================

#         completion = client.chat.completions.create(
#             model="llama-3.1-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": SYSTEM_PROMPT
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2,
#             max_tokens=2500
#         )

#         summary = completion.choices[0].message.content

#         if not summary or not summary.strip():
#             logger.warning("Groq returned empty response")
#             return "Unable to generate medical summary. Please try again."

#         logger.info("Summary generated successfully")
#         return summary.strip()

#     except Exception as e:

#         logger.error(f"generate_medical_summary failed: {e}")
#         return f"Error generating summary: {str(e)}"

# import os
# import logging

# from transformers import pipeline
# from dotenv import load_dotenv

# load_dotenv()

# logger = logging.getLogger(__name__)

# # ==========================================
# # HUGGING FACE MODEL (LOCAL)
# # ==========================================

# # You can switch model here:
# # GOOD OPTION (recommended): mistralai/Mistral-7B-Instruct-v0.2
# # LIGHT OPTION: google/flan-t5-base

# llm = pipeline(
#     "text-generation",
#     model="mistralai/Mistral-7B-Instruct-v0.2",
#     device_map="auto"
# )


# # ==========================================
# # DETECT ABNORMAL STATUS
# # ==========================================

# def is_abnormal(test: dict) -> bool:
#     status = str(test.get("status", "")).strip().lower()

#     abnormal_keywords = [
#         "high", "low", "positive", "abnormal",
#         "borderline", "critical", "reactive"
#     ]

#     return any(word in status for word in abnormal_keywords)


# # ==========================================
# # FORMAT TEST LIST FOR PROMPT
# # ==========================================

# def format_tests_for_prompt(tests: list) -> str:
#     if not tests:
#         return "  (none)"

#     lines = []

#     for t in tests:
#         name = t.get("test_name", "Unknown")
#         value = t.get("value", "")
#         unit = t.get("unit", "")
#         ref = t.get("reference_range", "")
#         status = t.get("status", "")

#         line = f"  - {name}: {value} {unit}".strip()

#         if ref:
#             line += f"  |  Ref: {ref}"
#         if status:
#             line += f"  |  Status: {status}"

#         lines.append(line)

#     return "\n".join(lines)


# # ==========================================
# # SYSTEM PROMPT
# # ==========================================

# SYSTEM_PROMPT = """You are a clinical report writer producing structured medical summaries.

# Rules:
# - Simple language only
# - No jargon without explanation
# - No diagnosis
# - No hallucination
# - Be concise and structured
# """


# # ==========================================
# # PROMPT BUILDERS
# # ==========================================

# def build_normal_prompt(normal_tests: list, rag_text: str) -> str:
#     tests_text = format_tests_for_prompt(normal_tests)

#     return f"""
# All {len(normal_tests)} parameters are normal.

# LAB RESULTS:
# {tests_text}

# KNOWLEDGE:
# {rag_text}

# Write a simple medical summary with categories and clear explanation.
# """


# def build_abnormal_prompt(abnormal_tests, normal_tests, rag_text, requires_review):
#     abnormal_text = format_tests_for_prompt(abnormal_tests)
#     normal_text = format_tests_for_prompt(normal_tests[:10])

#     return f"""
# ABNORMAL TESTS:
# {abnormal_text}

# NORMAL TESTS:
# {normal_text}

# KNOWLEDGE:
# {rag_text}

# Write a structured medical summary:
# - Explain abnormalities clearly
# - Mention risk level
# - Give recommendations
# - Keep simple language
# """


# # ==========================================
# # MAIN FUNCTION (HUGGING FACE VERSION)
# # ==========================================

# def generate_medical_summary(pipeline_result: dict) -> str:

#     try:
#         tests = pipeline_result.get("tests", [])
#         rag_context = pipeline_result.get("rag_context", [])
#         requires_review = pipeline_result.get("requires_review", False)

#         logger.info(f"Generating summary | tests={len(tests)}")

#         if not tests:
#             return "No test data found in the report."

#         # ==========================================
#         # SPLIT NORMAL / ABNORMAL
#         # ==========================================

#         abnormal_tests = []
#         normal_tests = []

#         for test in tests:
#             clean = {
#                 "test_name": test.get("test_name", ""),
#                 "value": test.get("value", ""),
#                 "unit": test.get("unit", ""),
#                 "reference_range": test.get("reference_range", ""),
#                 "status": test.get("status", "")
#             }

#             if is_abnormal(test):
#                 abnormal_tests.append(clean)
#             else:
#                 normal_tests.append(clean)

#         # ==========================================
#         # BUILD PROMPT
#         # ==========================================

#         rag_text = "\n".join(rag_context[:5]) if rag_context else "No context"

#         if abnormal_tests:
#             prompt = build_abnormal_prompt(
#                 abnormal_tests,
#                 normal_tests,
#                 rag_text,
#                 requires_review
#             )
#         else:
#             prompt = build_normal_prompt(normal_tests, rag_text)

#         # ==========================================
#         # HUGGING FACE INFERENCE
#         # ==========================================

#         input_text = f"{SYSTEM_PROMPT}\n\n{prompt}"

#         result = llm(
#             input_text,
#             max_new_tokens=700,
#             do_sample=False
#         )

#         summary = result[0]["generated_text"]

#         if not summary:
#             return "Unable to generate summary."

#         return summary.strip()

#     except Exception as e:
#         logger.error(f"HF summary failed: {e}")
#         return f"Error: {str(e)}"

# import logging
# from llm_clients import call_groq, call_gemini

# logger = logging.getLogger(__name__)


# # ==========================================
# # UTIL
# # ==========================================

# def is_abnormal(test: dict) -> bool:
#     status = str(test.get("status", "")).lower()
#     return any(x in status for x in ["high", "low", "positive", "abnormal", "critical"])


# def format_tests(tests):
#     lines = []
#     for t in tests:
#         lines.append(
#             f"- {t.get('test_name','')} : {t.get('value','')} "
#             f"{t.get('unit','')} | Status: {t.get('status','')}"
#         )
#     return "\n".join(lines)


# # ==========================================
# # PROMPTS
# # ==========================================

# SYSTEM = """
# You are a medical assistant.
# Rules:
# - Simple language
# - No diagnosis
# - No hallucination
# - Be concise
# """


# def build_prompt(abnormal, normal, rag):
#     return f"""
# ABNORMAL:
# {format_tests(abnormal)}

# NORMAL:
# {format_tests(normal)}

# KNOWLEDGE:
# {rag}

# Write a patient-friendly medical summary.
# Include:
# - Explanation
# - Risk level
# - Advice
# """


# # ==========================================
# # MAIN
# # ==========================================

# def generate_medical_summary(result: dict) -> str:
#     try:
#         tests = result.get("tests", [])
#         rag = "\n".join(result.get("rag_context", [])[:5])

#         abnormal = [t for t in tests if is_abnormal(t)]
#         normal = [t for t in tests if not is_abnormal(t)]

#         prompt = build_prompt(abnormal, normal, rag)
#         full_prompt = SYSTEM + "\n\n" + prompt

#         # Try GROQ first
#         summary = call_groq(full_prompt)

#         if summary:
#             return summary.strip()

#         # fallback GEMINI
#         summary = call_gemini(full_prompt)
#         return summary.strip() if summary else "Summary not available"

#     except Exception as e:
#         logger.error(f"Summary error: {e}")
#         return str(e)

# import logging

# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)

# # Load HF model once
# hf_processor = HFLLMProcessor()


# # ==========================================
# # UTIL
# # ==========================================

# def is_abnormal(test: dict) -> bool:
#     status = str(test.get("status", "")).lower()

#     return any(
#         x in status
#         for x in [
#             "high",
#             "low",
#             "positive",
#             "abnormal",
#             "critical"
#         ]
#     )


# def format_tests(tests):

#     lines = []

#     for t in tests:
#         lines.append(
#             f"- {t.get('test_name','')} : "
#             f"{t.get('value','')} "
#             f"{t.get('unit','')} | "
#             f"Status: {t.get('status','')}"
#         )

#     return "\n".join(lines)


# # ==========================================
# # PROMPT
# # ==========================================

# SYSTEM = """
# You are a medical assistant.

# Rules:
# - Use simple patient-friendly language
# - No diagnosis
# - No hallucinations
# - Be concise
# """


# def build_prompt(abnormal, normal, rag):

#     return f"""
# ABNORMAL TESTS:
# {format_tests(abnormal)}

# NORMAL TESTS:
# {format_tests(normal)}

# MEDICAL KNOWLEDGE:
# {rag}

# Write a patient-friendly medical summary.

# Include:
# - What looks abnormal
# - Possible meaning
# - General precautions
# - Whether medical follow-up may help
# """


# # ==========================================
# # MAIN
# # ==========================================

# def generate_medical_summary(result: dict) -> str:

#     try:
#         tests = result.get("tests", [])

#         rag = "\n".join(
#             result.get("rag_context", [])[:5]
#         )

#         abnormal = [
#             t for t in tests
#             if is_abnormal(t)
#         ]

#         normal = [
#             t for t in tests
#             if not is_abnormal(t)
#         ]

#         prompt = build_prompt(
#             abnormal,
#             normal,
#             rag
#         )

#         full_prompt = SYSTEM + "\n\n" + prompt

#         summary = hf_processor.generate_summary(
#             full_prompt
#         )

#         if not summary:
#             return "Summary not available"

#         return summary.strip()

#     except Exception as e:
#         logger.error(f"Summary error: {e}")

#         return "Summary generation failed"


# def generate_medical_summary(self, abnormal, normal, rag):
#     prompt = f"""
# You are a medical assistant.

# Use only the information below.
# Do not diagnose.
# Do not invent missing details.

# ABNORMAL TESTS:
# {abnormal}

# NORMAL TESTS:
# {normal}

# RETRIEVED MEDICAL CONTEXT:
# {rag}

# Write a patient-friendly summary.
# """
#     return self.generate(prompt, max_new_tokens=200)


# import logging
# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)

# hf_processor = HFLLMProcessor()


# def is_abnormal(test: dict) -> bool:
#     status = str(test.get("status", "")).lower()
#     return any(x in status for x in ["high", "low", "positive", "abnormal", "critical"])


# def format_tests(tests):
#     lines = []
#     for t in tests:
#         lines.append(
#             f"- {t.get('test_name', '')} : "
#             f"{t.get('value', '')} "
#             f"{t.get('unit', '')} | "
#             f"Status: {t.get('status', '')}"
#         )
#     return "\n".join(lines)


# SYSTEM = """
# You are a medical assistant.

# Rules:
# - Use simple patient-friendly language.
# - No diagnosis.
# - No hallucinations.
# - Be concise.
# - If something is missing, say it is not mentioned.
# """


# def build_prompt(abnormal, normal, rag):
#     return f"""
# Instruction:
# Summarize the medical report in simple patient-friendly language.

# Report Data:
# ABNORMAL TESTS:
# {format_tests(abnormal)}

# NORMAL TESTS:
# {format_tests(normal)}

# Retrieved Medical Context:
# {rag if rag else "No additional context retrieved."}

# Output Requirements:
# - What looks abnormal
# - Possible general meaning
# - General precautions
# - Whether medical follow-up may help
# """


# def generate_medical_summary(result: dict) -> str:
#     try:
#         tests = result.get("tests", [])
#         rag = "\n".join(result.get("rag_context", [])[:5])

#         abnormal = [t for t in tests if is_abnormal(t)]
#         normal = [t for t in tests if not is_abnormal(t)]

#         user_prompt = build_prompt(abnormal, normal, rag)
#         full_prompt = SYSTEM + "\n\n" + user_prompt

#         summary = hf_processor.generate(full_prompt, max_new_tokens=200)

#         if not summary:
#             return "Summary not available"

#         return summary.strip()

#     except Exception as e:
#         logger.error(f"Summary error: {e}")
#         return "Summary generation failed"


# import logging
# from OCRHandling.ensemble_processor import HFLLMProcessor

# logger = logging.getLogger(__name__)

# # Reuses the updated client architecture safely
# hf_processor = HFLLMProcessor()


# def is_abnormal(test: dict) -> bool:
#     status = str(test.get("status", "")).lower()
#     return any(x in status for x in ["high", "low", "positive", "abnormal", "critical"])


# def format_tests(tests):
#     lines = []
#     for t in tests:
#         lines.append(
#             f"- {t.get('test_name', '')} : "
#             f"{t.get('value', '')} "
#             f"{t.get('unit', '')} | "
#             f"Status: {t.get('status', '')}"
#         )
#     return "\n".join(lines)


# SYSTEM = """
# You are a medical assistant.

# Rules:
# - Use simple patient-friendly language.
# - No diagnosis.
# - No hallucinations.
# - Be concise.
# - If something is missing, say it is not mentioned.
# """


# def build_prompt(abnormal, normal, rag):
#     return f"""
# Instruction:
# Summarize the medical report in simple patient-friendly language.

# Report Data:
# ABNORMAL TESTS:
# {format_tests(abnormal)}

# NORMAL TESTS:
# {format_tests(normal)}

# Retrieved Medical Context:
# {rag if rag else "No additional context retrieved."}

# Output Requirements:
# - What looks abnormal
# - Possible general meaning
# - General precautions
# - Whether medical follow-up may help
# """


# def generate_medical_summary(result: dict) -> str:
#     try:
#         tests = result.get("tests", [])
#         rag = "\n".join(result.get("rag_context", [])[:5])

#         abnormal = [t for t in tests if is_abnormal(t)]
#         normal = [t for t in tests if not is_abnormal(t)]

#         user_prompt = build_prompt(abnormal, normal, rag)

#         # Utilize native system instruction configurations
#         summary = hf_processor.generate(
#             prompt=user_prompt, 
#             max_new_tokens=400, 
#             system_instruction=SYSTEM
#         )

#         if not summary:
#             return "Summary not available"

#         return summary.strip()

#     except Exception as e:
#         logger.error(f"Summary error: {e}")
#         return "Summary generation failed"

# RAG/llm_summary.py
import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

def generate_medical_summary(pipeline_payload: dict) -> str:
    """
    Generates a patient-friendly executive summary using Groq's high-speed 
    Llama-3.3 inference engine backed by RAG context guidelines.
    """
    tests = pipeline_payload.get("tests", [])
    rag_context = pipeline_payload.get("rag_context", [])

    if not tests:
        return "No structured laboratory parameters were discovered to summarize."

    # 1. Initialize Groq Engine Client
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY environment variable is completely missing.")
        return "Summary generation unavailable: API configuration missing."

    client = Groq(api_key=api_key)

    # 2. Frame System Instructions and Context Arrays
    system_instruction = (
        "You are an empathetic clinical communications assistant. Your task is to explain "
        "complex lab diagnostic findings to patients using clear, accessible terms. "
        "Always group abnormal/out-of-range metrics first, offer reassurance, list dietary or "
        "general lifestyle precautions, and conclude with a recommendation to check with their doctor."
    )

    user_prompt = f"""
Review the following structured medical metrics and clinical reference context:

--- RETRIEVED MEDICAL CONTEXT ---
{rag_context}

--- STRUCTURED LABORATORY TEST DATA ---
{tests}

Provide a comprehensive clinical executive summary tailored for the patient. Do not cut off mid-sentence.
"""

    try:
        # 3. Request high-speed streaming generation from Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,          # Slight variability for fluid narrative structure
            max_completion_tokens=1000 # Large ceiling budget to fix previous cutoffs
        )
        
        return completion.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"Groq summary block generation execution failed: {e}")
        return "An internal error occurred while compiling your patient health overview narrative."