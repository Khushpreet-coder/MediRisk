
# # # def clean_with_llm(text: str):
# # #     # Later replace with OpenAI / LLM call
# # #     return text

# # import requests
# # import os

# # HF_TOKEN = os.getenv("HF_TOKEN")

# # API_URL = "https://api-inference.huggingface.co/models/BioMistral/BioMistral-7B"

# # headers = {
# #     "Authorization": f"Bearer {HF_TOKEN}"
# # }


# # def summarize_medical_text(text: str):

# #     prompt = f"""
# # You are a medical assistant.

# # Extract and summarize this medical report in JSON format:

# # Return:
# # {{
# #   "patient_summary": "",
# #   "key_findings": [],
# #   "abnormal_values": [],
# #   "possible_concerns": [],
# #   "doctor_notes": ""
# # }}

# # Report:
# # {text}
# # """

# #     response = requests.post(
# #         API_URL,
# #         headers=headers,
# #         json={"inputs": prompt}
# #     )

# #     return response.json()

# import requests
# import os

# HF_TOKEN = os.getenv("HF_TOKEN")

# API_URL = "https://api-inference.huggingface.co/models/BioMistral/BioMistral-7B"

# headers = {"Authorization": f"Bearer {HF_TOKEN}"}


# def summarize_medical_text(prompt: str):

#     response = requests.post(
#         API_URL,
#         headers=headers,
#         json={
#             "inputs": prompt,
#             "parameters": {
#                 "temperature": 0.3,
#                 "max_new_tokens": 400
#             }
#         }
#     )

#     try:
#         return response.json()[0]["generated_text"]
#     except:
#         return {"error": "LLM failed", "raw": response.text}
    
# from transformers import pipeline

# # Load model once
# summarizer = pipeline(
#     "text-generation",
#     model="google/flan-t5-base"
# )


# def generate_summary(report_data):

#     tests = report_data.get("tests", [])

#     report_text = ""

#     for test in tests:

#         report_text += (
#             f"{test['test_name']} = {test['value']} "
#             f"{test['unit']} "
#             f"Status: {test['status']}. "
#         )

#     prompt = f"""
#     Summarize this medical report in simple language:

#     {report_text}
#     """

#     result = summarizer(
#         prompt,
#         max_length=120,
#         do_sample=False
#     )

#     return result[0]["generated_text"]

# from transformers import (
#     AutoTokenizer,
#     AutoModelForSeq2SeqLM
# )

# import torch


# # =========================================
# # Load Model
# # =========================================
# MODEL_NAME = "google/flan-t5-base"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


# # =========================================
# # Generate Summary
# # =========================================
# def generate_summary(report_data):

#     tests = report_data.get("tests", [])

#     report_text = ""

#     for test in tests:

#         report_text += (
#             f"{test['test_name']} = {test['value']} "
#             f"{test['unit']} "
#             f"Status: {test['status']}. "
#         )

#     prompt = f"""
#     Summarize this medical report in simple and patient-friendly language.

#     Mention only important abnormal findings.

#     Medical Report:
#     {report_text}
#     """

#     # tokenize
#     inputs = tokenizer(
#         prompt,
#         return_tensors="pt",
#         truncation=True,
#         max_length=1024
#     )

#     # generate
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=120,
#         temperature=0.3,
#         do_sample=True
#     )

#     # decode
#     summary = tokenizer.decode(
#         outputs[0],
#         skip_special_tokens=True
#     )

#     return summary

# from transformers import (
#     AutoTokenizer,
#     AutoModelForSeq2SeqLM
# )

# import torch


# # =========================================
# # Load Model
# # =========================================
# MODEL_NAME = "google/flan-t5-base"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


# # =========================================
# # Generate Summary
# # =========================================
# def generate_summary(report_data):

#     tests = report_data.get("tests", [])

#     # -------------------------------------
#     # Keep only abnormal findings
#     # -------------------------------------
#     abnormal_tests = []

#     ignore_status = [
#         "normal",
#         "optimal",
#         ""
#     ]

#     for test in tests:

#         status = test.get("status", "").strip().lower()

#         if status not in ignore_status:

#             abnormal_tests.append(test)

#     # -------------------------------------
#     # If everything normal
#     # -------------------------------------
#     if not abnormal_tests:

#         return (
#             "All major laboratory parameters are within normal limits."
#         )

#     # -------------------------------------
#     # Build compact abnormal report
#     # -------------------------------------
#     report_text = ""

#     for test in abnormal_tests:

#         test_name = test.get("test_name", "")
#         value = test.get("value", "")
#         unit = test.get("unit", "")
#         status = test.get("status", "")

#         report_text += (
#             f"{test_name}: {value} {unit}, "
#             f"Status: {status}. "
#         )

#     # -------------------------------------
#     # Better Prompt
#     # -------------------------------------
#     prompt = f"""
# You are a medical report summarization assistant.

# TASK:
# Generate a short, professional, patient-friendly summary.

# RULES:
# - Mention ONLY abnormal or important findings
# - Avoid repetition
# - Keep summary under 80 words
# - Use simple language
# - Do not mention normal tests
# - Do not explain every test

# ABNORMAL FINDINGS:
# {report_text}

# SUMMARY:
# """

#     # -------------------------------------
#     # Tokenize
#     # -------------------------------------
#     inputs = tokenizer(
#         prompt,
#         return_tensors="pt",
#         truncation=True,
#         max_length=512
#     )

#     # -------------------------------------
#     # Generate
#     # -------------------------------------
#     outputs = model.generate(
#         **inputs,

#         max_new_tokens=80,

#         temperature=0.2,

#         do_sample=False,

#         repetition_penalty=1.5,

#         no_repeat_ngram_size=3,

#         early_stopping=True
#     )

#     # -------------------------------------
#     # Decode
#     # -------------------------------------
#     summary = tokenizer.decode(
#         outputs[0],
#         skip_special_tokens=True
#     )

#     return summary.strip()


# from transformers import (
#     AutoTokenizer,
#     AutoModelForSeq2SeqLM
# )

# from rag.retrieve import retrieve_context
# from rag.web_search import search_web_medical_context


# # =========================================
# # Load Model
# # =========================================
# MODEL_NAME = "google/flan-t5-base"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


# # =========================================
# # Generate Summary
# # =========================================
# def generate_summary(report_data):

#     tests = report_data.get("tests", [])

#     abnormal_tests = []

#     # -------------------------------------
#     # Detect abnormal tests
#     # -------------------------------------
#     ignore_status = [
#         "normal",
#         "optimal",
#         ""
#     ]

#     for test in tests:

#         status = test.get(
#             "status",
#             ""
#         ).strip().lower()

#         if status not in ignore_status:

#             abnormal_tests.append(test)

#     # -------------------------------------
#     # All Normal
#     # -------------------------------------
#     if not abnormal_tests:

#         return (
#             "All major laboratory parameters "
#             "are within normal limits."
#         )

#     # -------------------------------------
#     # Build abnormal report text
#     # -------------------------------------
#     report_text = ""

#     for test in abnormal_tests:

#         report_text += (
#             f"{test['test_name']} = "
#             f"{test['value']} "
#             f"{test['unit']} "
#             f"Status: {test['status']}. "
#         )

#     # -------------------------------------
#     # Build RAG Query
#     # -------------------------------------
#     rag_query = " ".join(

#         [
#             f"{test['test_name']} "
#             f"{test['status']}"

#             for test in abnormal_tests
#         ]
#     )

#     # -------------------------------------
#     # Retrieve Context From ChromaDB
#     # -------------------------------------
#     rag_context = retrieve_context(
#         rag_query
#     )

#     # -------------------------------------
#     # Web Fallback
#     # -------------------------------------
#     if (
#         not rag_context
#         or len(rag_context.strip()) < 50
#     ):

#         print(
#             "🌐 Using Google Search Fallback..."
#         )

#         rag_context = (
#             search_web_medical_context(
#                 rag_query
#             )
#         )

#     # -------------------------------------
#     # Final Prompt
#     # -------------------------------------
#     prompt = f"""
# You are an expert medical report summarizer.

# PATIENT ABNORMAL RESULTS:
# {report_text}

# MEDICAL KNOWLEDGE:
# {rag_context}

# TASK:
# Generate a short, patient-friendly summary.

# RULES:
# - Mention only important abnormalities
# - Explain possible meaning simply
# - Avoid repetition
# - Keep summary under 100 words
# - Use professional but simple language
# """

#     # -------------------------------------
#     # Tokenize
#     # -------------------------------------
#     inputs = tokenizer(
#         prompt,
#         return_tensors="pt",
#         truncation=True,
#         max_length=512
#     )

#     # -------------------------------------
#     # Generate
#     # -------------------------------------
#     outputs = model.generate(
#         **inputs,

#         max_new_tokens=80,

#         temperature=0.2,

#         do_sample=False,

#         repetition_penalty=1.5,

#         no_repeat_ngram_size=3,

#         early_stopping=True
#     )

#     # -------------------------------------
#     # Decode
#     # -------------------------------------
#     summary = tokenizer.decode(
#         outputs[0],
#         skip_special_tokens=True
#     )

#     return summary.strip()


# from rag.retrieve import retrieve_context
# from rag.web_search import search_web_medical_context


# # =========================================
# # Generate Medical Summary
# # =========================================
# def generate_summary(report_data):

#     tests = report_data.get("tests", [])

#     important_findings = []

#     # =====================================
#     # Detect Important Abnormal Findings
#     # =====================================
#     for test in tests:

#         test_name = test.get(
#             "test_name",
#             ""
#         )

#         value = test.get(
#             "value",
#             ""
#         )

#         unit = test.get(
#             "unit",
#             ""
#         )

#         status = test.get(
#             "status",
#             ""
#         ).strip().lower()

#         # Skip normal findings
#         if status in [
#             "normal",
#             "optimal",
#             ""
#         ]:
#             continue

#         # ---------------------------------
#         # Build clean finding sentence
#         # ---------------------------------
#         finding = (
#             f"{test_name} is "
#             f"{status} "
#             f"({value} {unit})"
#         )

#         important_findings.append(finding)

#     # =====================================
#     # If Everything Normal
#     # =====================================
#     if not important_findings:

#         return (
#             "All major laboratory parameters "
#             "are within normal limits."
#         )

#     # =====================================
#     # Build Query For RAG
#     # =====================================
#     rag_query = " ".join(
#         important_findings
#     )

#     # =====================================
#     # Retrieve Chroma Context
#     # =====================================
#     try:

#         rag_results = retrieve_context(
#             rag_query
#         )

#         if isinstance(rag_results, list):

#             rag_context = " ".join(
#                 [
#                     item["text"]
#                     for item in rag_results
#                 ]
#             )

#         else:
#             rag_context = ""

#     except Exception as e:

#         print("RAG ERROR:", e)

#         rag_context = ""

#     # =====================================
#     # Web Search Fallback
#     # =====================================
#     if len(rag_context.strip()) < 50:

#         try:

#             print(
#                 "🌐 Using Google Search..."
#             )

#             web_context = (
#                 search_web_medical_context(
#                     rag_query
#                 )
#             )

#             rag_context += (
#                 "\n" + web_context
#             )

#         except Exception as e:

#             print(
#                 "WEB SEARCH ERROR:",
#                 e
#             )

#     # =====================================
#     # Build Final Summary
#     # =====================================
#     summary = (
#         "Key findings: "
#         + ", ".join(important_findings)
#         + "."
#     )

#     # =====================================
#     # Add Medical Insight
#     # =====================================
#     if rag_context:

#         summary += (
#             " These findings may require "
#             "clinical correlation and "
#             "medical evaluation."
#         )

#     return summarys