# import json
# from OCRHandling.ocr_service import extract_text
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.llm_parsing import structure_report
# from services.llm_service import generate_summary

# def process_report(file_path: str, output_path="output.json"):
#     # 1. Extract text
#     raw_text = extract_text(file_path)

#     print("✅ Extracted text length:", len(raw_text))

#     # 2. Clean text
#     cleaned_text = clean_text(raw_text)

#     print("🧹 Cleaned text preview:", cleaned_text[:500])

#     # 3. LLM structuring
#     structured_data = structure_report(cleaned_text)

#     # 4. Save JSON
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(structured_data, f, indent=2)

#     print("💾 Saved to:", output_path)

#     return structured_data

# import json

# from OCRHandling.ocr_service import extract_text
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.llm_parsing import structure_report

# from services.llm_service import generate_summary




# # =========================================
# # Full Medical Report Pipeline
# # OCR → Clean → Structure → Summary
# # =========================================
# def process_report(file_path: str, output_path="output.json"):

#     # =====================================
#     # 1. Extract Text
#     # =====================================
#     raw_text = extract_text(file_path)

#     print("✅ Extracted text length:", len(raw_text))

#     # =====================================
#     # 2. Clean Text
#     # =====================================
#     cleaned_text = clean_text(raw_text)

#     print("🧹 Cleaned text preview:", cleaned_text[:500])

#     # =====================================
#     # 3. Structure Report using LLM
#     # =====================================
#     structured_data = structure_report(cleaned_text)

#     # =====================================
#     # 4. Generate Summary
#     # =====================================
#     summary = generate_summary(structured_data)

#     # add summary into final response
#     structured_data["summary"] = summary

#     # =====================================
#     # 5. Save JSON
#     # =====================================
#     with open(output_path, "w", encoding="utf-8") as f:

#         json.dump(
#             structured_data,
#             f,
#             indent=2,
#             ensure_ascii=False
#         )

#     print("💾 Saved to:", output_path)

#     # =====================================
#     # 6. Return Final Data
#     # =====================================
#     return structured_data


# from OCRHandling.ocr_service import extract_text
# from OCRHandling.text_cleaner import clean_text


# def process_report(file_path: str):

#     # =========================
#     # 1. OCR Extraction
#     # =========================

#     raw_text = extract_text(file_path)

#     print("✅ RAW TEXT:")
#     print(raw_text[:1000])

#     # =========================
#     # 2. Clean Text
#     # =========================

#     cleaned_text = clean_text(raw_text)

#     print("🧹 CLEANED TEXT:")
#     print(cleaned_text[:1000])

#     return {
#         "raw_text": raw_text,
#         "cleaned_text": cleaned_text
#     }

# import json

# from OCRHandling.ocr_service import extract_text
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.llm_parsing import structure_report
# from RAG.query_builder import build_queries
# from RAG.retrieve import retrieve_context

# def process_report(file_path: str):

#     # =====================================
#     # 1. OCR Extraction
#     # =====================================

#     raw_text = extract_text(file_path)

#     # =====================================
#     # 2. Clean Text
#     # =====================================

#     cleaned_text = clean_text(raw_text)

#     # =====================================
#     # 3. Structured JSON
#     # =====================================

#     structured_data = structure_report(cleaned_text)

#     # # =====================================
#     # # 4. Final Output
#     # # =====================================

#     # =====================================
# # 4. Build Queries
# # =====================================

# queries = build_queries(structured_data)

# print("🔎 Queries:")

# for q in queries:
#     print(q)


# # =====================================
# # 5. Retrieve Context
# # =====================================

# all_context = []

# for query in queries:

#     context = retrieve_context(query)

#     print(f"\n📚 Context for: {query}")

#     print(context)

#     if context:
#         all_context.extend(context)


# # =====================================
# # 6. Remove Duplicates
# # =====================================

# all_context = list(set(all_context))


# # =====================================
# # 7. Final Output
# # =====================================

# final_output = {
#     "cleaned_text": cleaned_text,
#     "structured_data": structured_data,
#     "rag_context": all_context
# }

# return final_output
    

# import json

# from OCRHandling.ocr_service import extract_text
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.llm_parsing import structure_report

# from RAG.query_builder import build_queries
# from RAG.retrieve import retrieve_context

# from RAG.google_fallback import google_fallback



# def process_report(file_path: str):

#     # =====================================
#     # 1. OCR Extraction
#     # =====================================

#     raw_text = extract_text(file_path)

#     # =====================================
#     # 2. Clean Text
#     # =====================================

#     cleaned_text = clean_text(raw_text)

#     # =====================================
#     # 3. Structured JSON
#     # =====================================

#     structured_data = structure_report(cleaned_text)

#     # =====================================
#     # 4. Build Queries
#     # =====================================

#     queries = build_queries(structured_data)

#     print("🔎 Queries:")

#     for q in queries:
#         print(q)

#     # =====================================
#     # 5. Retrieve Context
#     # =====================================

#     all_context = []

#     for query in queries:

#         context = retrieve_context(query)

#         print(f"\n📚 Context for: {query}")

#         print(context)

#         if context:
#             all_context.extend(context)

#     # =====================================
#     # 6. Remove Duplicates
#     # =====================================

#     all_context = list(set(all_context))

#     # =====================================
#     # 7. Final Output
#     # =====================================

#     final_output = {
#         "cleaned_text": cleaned_text,
#         "structured_data": structured_data,
#         "rag_context": all_context
#     }

#     return final_output

import json

from OCRHandling.ocr_service import extract_text
from OCRHandling.text_cleaner import clean_text
from OCRHandling.llm_parsing import structure_report

from RAG.query_builder import build_queries
from RAG.retrieve import retrieve_context

from RAG.google_fallback import google_fallback

from RAG.llm_summary import generate_summary


def process_report(file_path: str):

    # =====================================
    # 1. OCR Extraction
    # =====================================

    raw_text = extract_text(file_path)

    # =====================================
    # 2. Clean Text
    # =====================================

    cleaned_text = clean_text(raw_text)

    # =====================================
    # 3. Structured JSON
    # =====================================

    structured_data = structure_report(cleaned_text)

    # =====================================
    # 4. Build Queries
    # =====================================

    queries = build_queries(structured_data)

    print("🔎 Queries:")

    for q in queries:
        print(q)

    # =====================================
    # 5. Retrieve Context
    # =====================================

    all_context = []

    for query in queries:

        context = retrieve_context(query)

        print(f"\n📚 Context for: {query}")

        print(context)

        # =====================================
        # Google Fallback
        # =====================================

        if not context:

            print("🌐 Using Google fallback...")

            context = google_fallback(query)

        # =====================================
        # Store Context
        # =====================================

        if context:

            if isinstance(context, list):

                all_context.extend(context)

            else:

                all_context.append(context)

    # =====================================
    # 6. Remove Duplicates
    # =====================================

    all_context = list(set(all_context))

    # =====================================
    # 7. Generate Summary
    # =====================================

    summary = generate_summary(
        structured_data
    )

    # =====================================
    # 8. Final Output
    # =====================================

    final_output = {

        "cleaned_text": cleaned_text,

        "structured_data": structured_data,

        "rag_context": all_context,

        "summary": summary
    }

    return final_output