# # from fastapi import APIRouter, UploadFile, File, Depends
# # from sqlalchemy.orm import Session
# # from database import get_db
# # import shutil
# # import os

# # from services.ocr_services import extract_text
# # from services.text_cleaner import clean_text_regex
# # from services.llm_service import clean_with_llm
# # from services.parser import convert_to_json

# # router = APIRouter(prefix="/report", tags=["Report"])

# # UPLOAD_DIR = "uploads"
# # os.makedirs(UPLOAD_DIR, exist_ok=True)


# # @router.post("/upload")
# # def upload_report(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
# #     # 1. Save file
# #     file_path = f"{UPLOAD_DIR}/{file.filename}"
# #     with open(file_path, "wb") as buffer:
# #         shutil.copyfileobj(file.file, buffer)

# #     # 2. OCR
# #     raw_text = extract_text(file_path)

# #     # 3. Regex cleaning
# #     cleaned_text = clean_text_regex(raw_text)

# #     # 4. LLM cleaning
# #     llm_cleaned = clean_with_llm(cleaned_text)

# #     # 5. Convert to JSON
# #     structured_data = convert_to_json(llm_cleaned)

# #     return {
# #         "message": "Report processed",
# #         "data": structured_data
# #     }


# from OCRHandling.ocr_service import extract_text_from_pdf
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.llm_parsing import parse_medical_report


# def process_report(file_path):
#     raw_text = extract_text_from_pdf(file_path)

#     cleaned = clean_text(raw_text)

#     result = parse_medical_report(cleaned)

#     return result


# from fastapi import APIRouter, UploadFile, File, HTTPException
# import shutil
# import os

# from OCRHandling.pipeline import process_report

# router = APIRouter()

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.post("/upload")
# async def upload_report(file: UploadFile = File(...)):
#     try:
#         file_path = os.path.join(UPLOAD_DIR, file.filename)

#         # Save file
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Run full pipeline
#         result = process_report(file_path)

#         return {
#             "message": "Report processed successfully",
#             "data": result
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
#     finally:
#         if os.path.exists(file_path):
#             os.remove(file_path)

# from fastapi import APIRouter, UploadFile, File, HTTPException
# import shutil
# import os

# from OCRHandling.pipeline import process_report
# from crud.report_crud import save_full_report

# router = APIRouter()

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.post("/upload")
# async def upload_report(file: UploadFile = File(...)):

#     file_path = ""

#     try:
#         file_path = os.path.join(UPLOAD_DIR, file.filename)

#         # Save uploaded file
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # OCR + JSON extraction
#         result = process_report(file_path)

#         print("🔥 EXTRACTED RESULT:", result)

#         # ---------------- SAVE TO MYSQL ----------------
#         report_id = save_full_report(
#             user_id=1,  # test user
#             file_name=file.filename,
#             tests=result.get("tests", []),
#             summary="Summary not generated yet"
#         )

#         print("✅ SAVED REPORT ID:", report_id)

#         return {
#             "message": "Report processed successfully",
#             "report_id": report_id,
#             "data": result
#         }

#     except Exception as e:
#         print("❌ ERROR:", e)
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         if file_path and os.path.exists(file_path):
#             os.remove(file_path)

# from fastapi import APIRouter, UploadFile, File, HTTPException

# import shutil
# import os

# from OCRHandling.pipeline import process_report




# router = APIRouter()

# UPLOAD_DIR = "uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.post("/upload")
# async def upload_report(file: UploadFile = File(...)):

#     file_path = ""

#     try:

#         file_path = os.path.join(
#             UPLOAD_DIR,
#             file.filename
#         )

#         # =========================
#         # Save Uploaded File
#         # =========================
#         with open(file_path, "wb") as buffer:

#             shutil.copyfileobj(file.file, buffer)

#         # =========================
#         # OCR + Extraction
#         # =========================
#         result = process_report(file_path)

#         print("🔥 EXTRACTED RESULT:", result)

#         # =========================
#         # Save to MySQL
#         # =========================
        

#         print("✅ SAVED REPORT ID:", report_id)

#         return {
#             "message": "Report processed successfully",
#             "report_id": report_id,
#             "data": result
#         }

#     except Exception as e:

#         print("❌ ERROR:", e)

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

#     finally:

#         if file_path and os.path.exists(file_path):

#             os.remove(file_path)

# from fastapi import APIRouter, UploadFile, File, HTTPException

# import shutil
# import os

# from OCRHandling.pipeline import process_report

# from rag.store_report import store_report


# router = APIRouter()

# UPLOAD_DIR = "uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.post("/upload")
# async def upload_report(file: UploadFile = File(...)):

#     file_path = ""

#     try:

#         file_path = os.path.join(
#             UPLOAD_DIR,
#             file.filename
#         )

#         # Save uploaded file
#         with open(file_path, "wb") as buffer:

#             shutil.copyfileobj(file.file, buffer)

#         # OCR + extraction
#         result = process_report(file_path)

#         print("🔥 EXTRACTED RESULT:", result)

#         # Store in ChromaDB
#         chroma_id = store_report(result)

#         print("✅ CHROMA REPORT ID:", chroma_id)

#         return {
#             "message": "Report processed successfully",
#             "chroma_id": chroma_id,
#             "data": result
#         }

#     except Exception as e:

#         print("❌ ERROR:", e)

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

#     finally:

#         if file_path and os.path.exists(file_path):

#             os.remove(file_path)


from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

from OCRHandling.pipeline import process_report
# from rag.store_report import store_report

router = APIRouter()

# =========================================
# Upload Directory
# =========================================
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================================
# Allowed File Types
# =========================================
ALLOWED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]


# =========================================
# Upload + OCR + Summary Route
# =========================================
@router.post("/upload")
async def upload_report(file: UploadFile = File(...)):

    file_path = ""

    try:

        if not file.filename:
            raise HTTPException(400, "File name missing")

        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(400, "Invalid file type")

        unique_filename = f"{uuid.uuid4()}{file_ext}"

        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"📄 File Saved: {file_path}")

        # OCR + RAG pipeline
        result = process_report(file_path)

        print("🔥 EXTRACTED RESULT:", result)

        return {
            "status": "success",
            "data": result
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("❌ ERROR:", str(e))
        raise HTTPException(500, str(e))

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑 Deleted Temp File: {file_path}")