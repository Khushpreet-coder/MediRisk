# import json

# from OCRHandling.ocr_service import extract_text
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.llm_parsing import structure_report


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
#     # 4. Final Output
#     # =====================================

#     final_output = {
#         "cleaned_text": cleaned_text,
#         "structured_data": structured_data
#     }

#     return final_output

# def validate_data(data):

#     if not data or "tests" not in data:
#         return False

#     for test in data["tests"]:

#         if not isinstance(test, dict):
#             return False

#         if not test.get("test_name"):
#             return False

#         value = test.get("value")

#         if value is None:
#             return False

#         try:
#             float(value)
#         except:
#             return False

#     return True


# =====================================
# VALIDATE JSON STRUCTURE
# =====================================


def validate_data(data):

    if not data:
        return False

    if "tests" not in data:
        return False

    if not isinstance(data["tests"], list):
        return False

    for test in data["tests"]:

        if not isinstance(test, dict):
            return False

        if not test.get("test_name"):
            return False

    return True