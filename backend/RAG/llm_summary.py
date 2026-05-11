# import requests
# import json

# from RAG.retrieve import retrieve_context
# from RAG.query_builder import build_queries


# # =========================================
# # Generate Medical Summary
# # =========================================

# def generate_summary(structured_data):

#     tests = structured_data.get("tests", [])

#     abnormal_tests = []

#     # =====================================
#     # Detect abnormal tests
#     # =====================================

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

#     # =====================================
#     # All Normal
#     # =====================================

#     if not abnormal_tests:

#         return (
#             "All major laboratory parameters "
#             "are within normal limits."
#         )

#     # =====================================
#     # Build RAG Queries
#     # =====================================

#     queries = build_queries(
#         structured_data
#     )

#     # =====================================
#     # Retrieve RAG Context
#     # =====================================

#     rag_context = []

#     for item in queries:

#         query = item["query"]

#         category = item["category"]

#         try:

#             results = retrieve_context(

#     query=query,

#     category=category

# )

# if isinstance(results, list):

#     rag_context.extend(results)

# elif isinstance(results, str):

#     rag_context.append(results)

#         except Exception as e:

#             print(
#                 f"Retrieval error: {e}"
#             )

#     # Remove duplicates
#     rag_context = list(
#         set(rag_context)
#     )

#     # =====================================
#     # Build Abnormal Findings
#     # =====================================

#     findings = []

#     for test in abnormal_tests:

#         findings.append({

#             "test_name": test.get(
#                 "test_name"
#             ),

#             "value": test.get(
#                 "value"
#             ),

#             "unit": test.get(
#                 "unit"
#             ),

#             "status": test.get(
#                 "status"
#             ),

#             "reference_range": test.get(
#                 "reference_range"
#             )

#         })

#     # =====================================
#     # Final Prompt
#     # =====================================

#     prompt = f"""
# You are an expert medical report summarizer.

# PATIENT ABNORMAL FINDINGS:
# {json.dumps(findings, indent=2)}

# MEDICAL KNOWLEDGE:
# {chr(10).join(rag_context)}

# TASK:
# Generate a short patient-friendly summary.

# RULES:
# - Mention only important abnormalities
# - Explain possible meaning simply
# - Keep response under 150 words
# - Avoid medical jargon
# - Mention lifestyle advice if relevant
# - Mention if doctor consultation may help
# """

#     # =====================================
#     # Call Ollama
#     # =====================================

#     response = requests.post(

#         "http://localhost:11434/api/generate",

#         json={

#             "model": "phi3",

#             "prompt": prompt,

#             "stream": False

#         }

#     )

#     result = response.json()

#     summary = result.get(
#         "response",
#         ""
#     )

#     return summary.strip()


# import requests
# import json

# from RAG.retrieve import retrieve_context
# from RAG.query_builder import build_queries


# # =========================================
# # Generate Medical Summary
# # =========================================

# def generate_summary(structured_data):

#     tests = structured_data.get("tests", [])

#     abnormal_tests = []

#     # =====================================
#     # Detect abnormal tests
#     # =====================================

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

#     # =====================================
#     # All Normal
#     # =====================================

#     if not abnormal_tests:

#         return (
#             "All major laboratory parameters "
#             "are within normal limits."
#         )

#     # =====================================
#     # Build RAG Queries
#     # =====================================

#     queries = build_queries(
#         structured_data
#     )

#     # =====================================
#     # Retrieve RAG Context
#     # =====================================

#     rag_context = []

#     for query in queries:
#         try:

#         results = retrieve_context(query)
#         if isinstance(results, list):

#             rag_context.extend(results)

#         elif isinstance(results, str):

#             rag_context.append(results)

#     except Exception as e:

#         print(
#             f"Retrieval error: {e}"
#         )

#     # =====================================
#     # Remove duplicate context
#     # =====================================

#     rag_context = list(
#         set(rag_context)
#     )

#     # =====================================
#     # Build Abnormal Findings
#     # =====================================

#     findings = []

#     for test in abnormal_tests:

#         findings.append({

#             "test_name": test.get(
#                 "test_name"
#             ),

#             "value": test.get(
#                 "value"
#             ),

#             "unit": test.get(
#                 "unit"
#             ),

#             "status": test.get(
#                 "status"
#             ),

#             "reference_range": test.get(
#                 "reference_range"
#             )

#         })

#     # =====================================
#     # Final Prompt
#     # =====================================

#     prompt = f"""
# You are an expert medical report summarizer.

# PATIENT ABNORMAL FINDINGS:
# {json.dumps(findings, indent=2)}

# MEDICAL KNOWLEDGE:
# {chr(10).join(rag_context)}

# TASK:
# Generate a short patient-friendly summary.

# RULES:
# - Mention only important abnormalities
# - Explain possible meaning simply
# - Keep response under 150 words
# - Avoid medical jargon
# - Mention lifestyle advice if relevant
# - Mention if doctor consultation may help
# """

#     # =====================================
#     # Call Ollama
#     # =====================================

#     try:

#         response = requests.post(

#             "http://localhost:11434/api/generate",

#             json={

#                 "model": "phi3",

#                 "prompt": prompt,

#                 "stream": False

#             }

#         )

#         result = response.json()

#         summary = result.get(
#             "response",
#             ""
#         )

#         return summary.strip()

#     except Exception as e:

#         print("LLM ERROR:", e)

#         return (
#             "Unable to generate summary "
#             "at the moment."
#         )


import requests
import json

from RAG.retrieve import retrieve_context
from RAG.query_builder import build_queries


# =========================================
# Generate Medical Summary
# =========================================

def generate_summary(structured_data):

    tests = structured_data.get("tests", [])

    abnormal_tests = []

    # =====================================
    # Detect abnormal tests
    # =====================================

    ignore_status = [
        "normal",
        "optimal",
        ""
    ]

    for test in tests:

        status = test.get(
            "status",
            ""
        ).strip().lower()

        if status not in ignore_status:

            abnormal_tests.append(test)

    # =====================================
    # All Normal
    # =====================================

    if not abnormal_tests:

        return (
            "All major laboratory parameters "
            "are within normal limits."
        )

    # =====================================
    # Build RAG Queries
    # =====================================

    queries = build_queries(
        structured_data
    )

    # =====================================
    # Retrieve RAG Context
    # =====================================

    rag_context = []

    for query in queries:

        try:

            results = retrieve_context(query)

            if isinstance(results, list):

                rag_context.extend(results)

            elif isinstance(results, str):

                rag_context.append(results)

        except Exception as e:

            print(
                f"Retrieval error: {e}"
            )

    # =====================================
    # Remove duplicate context
    # =====================================

    rag_context = list(
        set(rag_context)
    )

    # =====================================
    # Build Abnormal Findings
    # =====================================

    findings = []

    for test in abnormal_tests:

        findings.append({

            "test_name": test.get(
                "test_name"
            ),

            "value": test.get(
                "value"
            ),

            "unit": test.get(
                "unit"
            ),

            "status": test.get(
                "status"
            ),

            "reference_range": test.get(
                "reference_range"
            )

        })

    # =====================================
    # Final Prompt
    # =====================================

    prompt = f"""
You are an expert medical report summarizer.

PATIENT ABNORMAL FINDINGS:
{json.dumps(findings, indent=2)}

MEDICAL KNOWLEDGE:
{chr(10).join(rag_context)}

TASK:
Generate a short patient-friendly summary.

RULES:
- Mention only important abnormalities
- Explain possible meaning simply
- Keep response under 150 words
- Avoid medical jargon
- Mention lifestyle advice if relevant
- Mention if doctor consultation may help
"""

    # =====================================
    # Call Ollama
    # =====================================

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model": "phi3",

                "prompt": prompt,

                "stream": False

            }

        )

        result = response.json()

        summary = result.get(
            "response",
            ""
        )

        return summary.strip()

    except Exception as e:

        print("LLM ERROR:", e)

        return (
            "Unable to generate summary "
            "at the moment."
        )