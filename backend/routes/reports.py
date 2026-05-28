# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
# from sqlalchemy.orm import Session

# from OCRHandling.enhanced_pipeline import process_report_enhanced as process_report

# from database import SessionLocal
# from models.report_model import Report

# import shutil
# import os
# import uuid
# import json


# router = APIRouter()

# # =========================================
# # Upload Directory
# # =========================================
# UPLOAD_DIR = "uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # =========================================
# # Allowed File Types
# # =========================================
# ALLOWED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]


# # =========================================
# # Database Dependency
# # =========================================
# def get_db():
#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()


# # =========================================
# # Upload + OCR + Summary Route
# # =========================================
# @router.post("/upload")
# async def upload_report(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):

#     file_path = ""

#     try:

#         # ==============================
#         # Validate File
#         # ==============================
#         if not file.filename:
#             raise HTTPException(400, "File name missing")

#         file_ext = os.path.splitext(file.filename)[1].lower()

#         if file_ext not in ALLOWED_EXTENSIONS:
#             raise HTTPException(400, "Invalid file type")

#         # ==============================
#         # Save File
#         # ==============================
#         unique_filename = f"{uuid.uuid4()}{file_ext}"

#         file_path = os.path.join(UPLOAD_DIR, unique_filename)

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         print(f"📄 File Saved: {file_path}")

#         # ==============================
#         # Process OCR + LLM
#         # ==============================
#         result = process_report(file_path)

#         print("🔥 EXTRACTED RESULT:", result)

#         # ==============================
#         # Extract Data
#         # ==============================
#         tests = result.get("tests", [])

#         metrics = result.get("metrics", {})

        

#         summary_text = json.dumps(tests)

#         extracted_text = json.dumps(result)

#         # ==============================
#         # Save to Database
#         # ==============================
#         new_report = Report(
#             original_filename=file.filename,
#             stored_filename=unique_filename,
#             file_path=file_path,
#             file_extension=file_ext,

#             extracted_text=extracted_text,
#             summary=summary_text,

            

#             status="completed"
#         )

#         db.add(new_report)

#         db.commit()

#         db.refresh(new_report)

#         # ==============================
#         # Return Response
#         # ==============================
#         return {
#             "status": "success",

#             "report_id": new_report.id,

            

#             "data": result
#         }

#     except HTTPException as e:
#         raise e

#     except Exception as e:
#         print("❌ ERROR:", str(e))

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

#     finally:

#         # Optional:
#         # remove uploaded file after processing

#         if file_path and os.path.exists(file_path):

#             os.remove(file_path)

#             print(f"🗑 Deleted Temp File: {file_path}")

# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
# from sqlalchemy.orm import Session

# from OCRHandling.enhanced_pipeline import process_report_enhanced as process_report
# from RAG.llm_summary import generate_medical_summary


# from database import SessionLocal
# from models.report_model import Report

# import shutil
# import os
# import uuid
# import json


# router = APIRouter()

# # =========================================
# # Upload Directory
# # =========================================
# UPLOAD_DIR = "uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # =========================================
# # Allowed File Types
# # =========================================
# ALLOWED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]


# # =========================================
# # Database Dependency
# # =========================================
# def get_db():
#     db = SessionLocal()

#     try:
#         yield db

#     finally:
#         db.close()


# # =========================================
# # Upload + OCR + RAG + Summary Route
# # =========================================
# @router.post("/upload")
# def upload_report(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     background_tasks: BackgroundTasks = None
# ):

#     file_path = save_file(file)

#     # create DB entry FIRST
#     new_report = Report(
#         original_filename=file.filename,
#         stored_filename=file_path,
#         status="processing"
#     )

#     db.add(new_report)
#     db.commit()
#     db.refresh(new_report)

#     # run heavy work in background
#     background_tasks.add_task(
#         process_in_background,
#         file_path,
#         new_report.id
#     )

#     return {
#         "status": "processing",
#         "report_id": new_report.id
#     }        
# # =========================================
# # Get Report By ID
# # =========================================

# @router.get("/report/{report_id}")
# def get_report(
#     report_id: int,
#     db: Session = Depends(get_db)
# ):

#     report = db.query(Report).filter(
#         Report.id == report_id
#     ).first()

#     if not report:
#         raise HTTPException(
#             status_code=404,
#             detail="Report not found"
#         )

#     extracted_data = json.loads(
#         report.extracted_text
#     )

#     return {
#         "status": "success",
#         "report_id": report.id,
#         "data": {
#             "tests": extracted_data.get("tests", []),
#             "summary": report.summary,
#             "metrics": extracted_data.get("metrics", {}),
#             "requires_review":
#                 extracted_data.get(
#                     "requires_review",
#                     False
#                 )
#         }
#     }

# def process_in_background(file_path, report_id):

#     try:
#         result = process_report(file_path)

#         summary = generate_medical_summary(result)

#         # ❌ REMOVE update_report (it is causing crash)

#         print("Processing done for report:", report_id)

#     except Exception as e:
#         print("Background error:", e)

#     finally:
#         if os.path.exists(file_path):
#             os.remove(file_path)


# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
# from sqlalchemy.orm import Session

# from OCRHandling.enhanced_pipeline import process_report_enhanced as process_report
# from RAG.llm_summary import generate_medical_summary
# from starlette.concurrency import run_in_threadpool

# from database import SessionLocal
# from models.report_model import Report

# import shutil
# import os
# import uuid
# import json

# router = APIRouter()

# # =========================================
# # Upload Directory
# # =========================================
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # =========================================
# # Allowed File Types
# # =========================================
# ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

# # =========================================
# # Database Dependency
# # =========================================
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Helper: update DB safely
# def update_report(db: Session, report_id: int, status: str, extracted_text: str = None, summary: str = None):
#     db_report = db.query(Report).filter(Report.id == report_id).first()
#     if not db_report:
#         return
#     db_report.status = status
#     if extracted_text is not None:
#         db_report.extracted_text = extracted_text
#     if summary is not None:
#         db_report.summary = summary
#     try:
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         print("DB update failed:", e)

# # =========================================
# # Upload + OCR + RAG + Summary Route
# # =========================================
# @router.post("/upload")
# def upload_report(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     background_tasks: BackgroundTasks = None
# ):
#     # Validate extension
#     ext = os.path.splitext(file.filename)[1].lower()
#     if ext not in ALLOWED_EXTENSIONS:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
#         )

#     # Save file
#     stored_filename = f"{uuid.uuid4()}{ext}"
#     file_path = os.path.join(UPLOAD_DIR, stored_filename)

#     with open(file_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Create DB entry
#     new_report = Report(
#         original_filename=file.filename,
#         stored_filename=file_path,
#         file_path=file_path,
#         file_extension=ext,
#         status="uploaded"
#     )
#     db.add(new_report)
#     db.commit()
#     db.refresh(new_report)

#     # Mark as processing
#     update_report(db, new_report.id, "processing")

#     # Run heavy work in background
#     background_tasks.add_task(
#         process_in_background,
#         file_path,
#         new_report.id
#     )

#     return {
#         "status": "processing",
#         "report_id": new_report.id
#     }

# # =========================================
# # Get Report By ID
# # =========================================
# @router.get("/report/{report_id}")
# def get_report(
#     report_id: int,
#     db: Session = Depends(get_db)
# ):
#     report = db.query(Report).filter(Report.id == report_id).first()
#     if not report:
#         raise HTTPException(status_code=404, detail="Report not found")

#     # Safely parse extracted_text
#     extracted_data = {}
#     if report.extracted_text:
#         try:
#             extracted_data = json.loads(report.extracted_text)
#         except (json.JSONDecodeError, TypeError):
#             extracted_data = {}

#     return {
#         "status": "success",
#         "report_id": report.id,
#         "status_label": report.status,
#         "data": {
#             "tests": extracted_data.get("tests", []),
#             "summary": report.summary or "",
#             "metrics": extracted_data.get("metrics", {}),
#             "requires_review": extracted_data.get("requires_review", False)
#         }
#     }

# # =========================================
# # Background processing (runs in threadpool by FastAPI)
# # =========================================
# def process_in_background(file_path: str, report_id: int):
#     db = SessionLocal()
#     try:
#         # 1. OCR / pipeline
#         result = process_report(file_path)   # your existing OCR + parsing

#         # 2. RAG + LLM summary
#         summary = generate_medical_summary(result)  # your existing LLM call

#         # 3. Convert to JSON
#         # Example format; adjust to match your OCR output
#         extracted_data = {
#             "tests": result.get("tests", []),
#             "metrics": result.get("metrics", {}),
#             "requires_review": result.get("requires_review", False),
#         }
#         extracted_text_json = json.dumps(extracted_data)

#         # 4. Update DB
#         update_report(db, report_id, "completed", extracted_text_json, summary)

#     except Exception as e:
#         print("Background error:", e)
#         update_report(db, report_id, "failed", summary="Error during processing")

#     finally:
#         db.close()
#         if os.path.exists(file_path):
#             os.remove(file_path)

# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
# from sqlalchemy.orm import Session

# from OCRHandling.enhanced_pipeline import process_report_enhanced as process_report
# from RAG.llm_summary import generate_medical_summary
# from starlette.concurrency import run_in_threadpool

# from database import SessionLocal
# from models.report_model import Report

# import shutil
# import os
# import uuid
# import json

# router = APIRouter()

# # =========================================
# # Upload Directory
# # =========================================
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # =========================================
# # Allowed File Types
# # =========================================
# ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

# # =========================================
# # Database Dependency
# # =========================================
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Helper: update DB safely
# def update_report(db: Session, report_id: int, status: str, extracted_text: str = None, summary: str = None):
#     db_report = db.query(Report).filter(Report.id == report_id).first()
#     if not db_report:
#         return
#     db_report.status = status
#     if extracted_text is not None:
#         db_report.extracted_text = extracted_text
#     if summary is not None:
#         db_report.summary = summary
#     try:
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         print("DB update failed:", e)

# # =========================================
# # Upload + OCR + RAG + Summary Route
# # =========================================
# @router.post("/upload")
# async def upload_report(
#     background_tasks: BackgroundTasks,
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     # Validate extension
#     ext = os.path.splitext(file.filename)[1].lower()
#     if ext not in ALLOWED_EXTENSIONS:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
#         )

#     # Save file
#     stored_filename = f"{uuid.uuid4()}{ext}"
#     file_path = os.path.join(UPLOAD_DIR, stored_filename)

#     with open(file_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # Create DB entry
#     new_report = Report(
#         original_filename=file.filename,
#         stored_filename=file_path,
#         file_path=file_path,
#         file_extension=ext,
#         status="uploaded"
#     )
#     db.add(new_report)
#     db.commit()
#     db.refresh(new_report)

#     # Mark as processing
#     update_report(db, new_report.id, "processing")

#     # Run heavy work in background (via async wrapper)
#     background_tasks.add_task(
#         process_in_background_async,
#         file_path,
#         new_report.id
#     )

#     return {
#         "status": "processing",
#         "report_id": new_report.id
#     }

# # =========================================
# # Get Report By ID
# # =========================================
# @router.get("/report/{report_id}")
# def get_report(
#     report_id: int,
#     db: Session = Depends(get_db)
# ):
#     report = db.query(Report).filter(Report.id == report_id).first()
#     if not report:
#         raise HTTPException(status_code=404, detail="Report not found")

#     # Safely parse extracted_text
#     extracted_data = {}
#     if report.extracted_text:
#         try:
#             extracted_data = json.loads(report.extracted_text)
#         except (json.JSONDecodeError, TypeError):
#             extracted_data = {}

#     return {
#         "status": "success",
#         "report_id": report.id,
#         "status_label": report.status,
#         "data": {
#             "tests": extracted_data.get("tests", []),
#             "summary": report.summary or "",
#             "metrics": extracted_data.get("metrics", {}),
#             "requires_review": extracted_data.get("requires_review", False)
#         }
#     }

# # =========================================
# # Background processing (sync CPU‑bound code)
# # =========================================
# def process_in_background(file_path: str, report_id: int):
#     db = SessionLocal()
#     try:
#         # 1. OCR / pipeline
#         result = process_report(file_path)   # your existing OCR + parsing

#         # 2. RAG + LLM summary
#         summary = generate_medical_summary(result)  # your existing LLM call

#         # 3. Convert to JSON
#         extracted_data = {
#             "tests": result.get("tests", []),
#             "metrics": result.get("metrics", {}),
#             "requires_review": result.get("requires_review", False),
#         }
#         extracted_text_json = json.dumps(extracted_data)

#         # 4. Update DB
#         update_report(db, report_id, "completed", extracted_text_json, summary)

#     except Exception as e:
#         print("Background error:", e)
#         update_report(db, report_id, "failed", summary="Error during processing")

#     finally:
#         db.close()
#         if os.path.exists(file_path):
#             os.remove(file_path)

# # =========================================
# # Async wrapper using run_in_threadpool (for FastAPI BackgroundTasks)
# # =========================================
# async def process_in_background_async(file_path: str, report_id: int):
#     await run_in_threadpool(process_in_background, file_path, report_id)


# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
# from sqlalchemy.orm import Session

# from OCRHandling.enhanced_pipeline import process_report_enhanced as process_report
# from RAG.llm_summary import generate_medical_summary

# from database import SessionLocal
# from models.report_model import Report

# import shutil
# import os
# import uuid
# import json

# router = APIRouter()

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

# # =========================
# # DB SESSION
# # =========================
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # =========================
# # SAFE DB UPDATE
# # =========================
# def update_report(db: Session, report_id: int, status: str, extracted_text=None, summary=None):
#     try:
#         report = db.query(Report).filter(Report.id == report_id).first()
#         if not report:
#             return

#         report.status = status

#         if extracted_text is not None:
#             report.extracted_text = extracted_text

#         if summary is not None:
#             report.summary = summary

#         db.commit()

#     except Exception as e:
#         db.rollback()
#         print("❌ DB update failed:", e)


# # =========================
# # UPLOAD ROUTE
# # =========================
# @router.post("/upload")
# async def upload_report(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):

#     ext = os.path.splitext(file.filename)[1].lower()

#     if ext not in ALLOWED_EXTENSIONS:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid file type"
#         )

#     file_path = os.path.join(
#         UPLOAD_DIR,
#         f"{uuid.uuid4()}{ext}"
#     )

#     with open(file_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     # =====================================
#     # CREATE DB ENTRY
#     # =====================================

#     report = Report(
#         original_filename=file.filename,
#         stored_filename=file_path,
#         file_path=file_path,
#         file_extension=ext,
#         status="processing"
#     )

#     db.add(report)
#     db.commit()
#     db.refresh(report)

#     try:

#         print("🔥 Processing started")

#         # =====================================
#         # FULL PIPELINE
#         # =====================================

#         result = process_report(file_path)

#         print("✅ OCR + RAG + Summary done")

#         extracted_data = {
#             "tests": result.get("tests", []),

#             "cleaned_text": result.get(
#                 "cleaned_text",
#                 ""
#             ),

#             "rag_context": result.get(
#                 "rag_context",
#                 []
#             ),

#             "summary": result.get(
#                 "summary",
#                 ""
#             ),

#             "metrics": result.get(
#                 "metrics",
#                 {}
#             ),

#             "requires_review": result.get(
#                 "requires_review",
#                 False
#             )
#         }

#         # =====================================
#         # SAVE RESULT
#         # =====================================

#         update_report(
#             db,
#             report.id,
#             "completed",
#             json.dumps(extracted_data),
#             extracted_data["summary"]
#         )

#         print("🎉 Report completed")

#         return {
#             "status": "success",

#             "report_id": report.id,

#             "data": extracted_data
#         }

#     except Exception as e:

#         print("❌ Processing error:", e)

#         update_report(
#             db,
#             report.id,
#             "failed",
#             summary=str(e)
#         )

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

#     finally:

#         if os.path.exists(file_path):
#             os.remove(file_path)
# # =========================
# # BACKGROUND TASK (FIXED)
# # =========================
# def process_background_task(file_path: str, report_id: int):

#     db = SessionLocal()

#     try:
#         print("🔥 Background started")

#         # =====================================
#         # FULL PIPELINE
#         # =====================================

#         result = process_report(file_path)

#         print("✅ OCR + RAG + Summary done")

#         # =====================================
#         # SAVE EVERYTHING
#         # =====================================

#         extracted_data = {
#             "tests": result.get("tests", []),

#             "cleaned_text": result.get(
#                 "cleaned_text",
#                 ""
#             ),

#             "rag_context": result.get(
#                 "rag_context",
#                 []
#             ),

#             "summary": result.get(
#                 "summary",
#                 ""
#             ),

#             "metrics": result.get(
#                 "metrics",
#                 {}
#             ),

#             "requires_review": result.get(
#                 "requires_review",
#                 False
#             )
#         }

#         update_report(
#             db,
#             report_id,
#             "completed",
#             json.dumps(extracted_data),
#             extracted_data["summary"]
#         )

#         print("🎉 DB updated successfully")

#     except Exception as e:

#         print("❌ Background error:", e)

#         update_report(
#             db,
#             report_id,
#             "failed",
#             summary=str(e)
#         )

#     finally:

#         db.close()

#         if os.path.exists(file_path):
#             os.remove(file_path)


# # =========================
# # GET REPORT
# # =========================
# @router.get("/report/{report_id}")
# def process_background_task(file_path: str, report_id: int):

#     db = SessionLocal()

#     try:
#         print("🔥 Background started")

#         # =====================================
#         # FULL PIPELINE
#         # =====================================

#         result = process_report(file_path)

#         print("✅ OCR + RAG + Summary done")

#         # =====================================
#         # SAVE EVERYTHING
#         # =====================================

#         extracted_data = {
#             "tests": result.get("tests", []),

#             "cleaned_text": result.get(
#                 "cleaned_text",
#                 ""
#             ),

#             "rag_context": result.get(
#                 "rag_context",
#                 []
#             ),

#             "summary": result.get(
#                 "summary",
#                 ""
#             ),

#             "metrics": result.get(
#                 "metrics",
#                 {}
#             ),

#             "requires_review": result.get(
#                 "requires_review",
#                 False
#             )
#         }

#         update_report(
#             db,
#             report_id,
#             "completed",
#             json.dumps(extracted_data),
#             extracted_data["summary"]
#         )

#         print("🎉 DB updated successfully")

#     except Exception as e:

#         print("❌ Background error:", e)

#         update_report(
#             db,
#             report_id,
#             "failed",
#             summary=str(e)
#         )

#     finally:

#         db.close()

#         if os.path.exists(file_path):
#             os.remove(file_path)

import os
import json
import uuid
import shutil
import logging
from typing import Dict
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

# Import your unified, optimized linear parsing pipeline execution target
from OCRHandling.enhanced_pipeline import process_report_enhanced as process_report

from database import SessionLocal
from models.report_model import Report

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


# =====================================
# DATABASE SESSION MANAGEMENT DEPENDENCY
# =====================================
def get_db():
    """Provides a transactional database session per network request flow."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================
# THREAD-SAFE DATABASE TRANSACTION WORKER
# =====================================
def update_report(db: Session, report_id: int, status: str, extracted_text: str = None, summary: str = None):
    """Safely updates report row entry statuses and fields with automated database rollbacks."""
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            logger.warning(f"Report execution lookup failed for ID: {report_id}")
            return

        report.status = status

        if extracted_text is not None:
            report.extracted_text = extracted_text

        if summary is not None:
            report.summary = summary

        db.commit()
        logger.info(f"Report ID {report_id} successfully updated to status: {status}")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Database update failure encountered on Report {report_id}: {e}")


# =====================================
# ROUTE 1: INGESTION & PIPELINE TRIGGER
# =====================================
# @router.post("/upload")
# async def upload_report(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     """
#     Receives incoming file payloads, initializes processing states, 
#     and executes the linear processing pipeline sequence.
#     """
#     if not file.filename:
#         raise HTTPException(status_code=400, detail="Missing valid upload file name metadata.")

#     ext = os.path.splitext(file.filename)[1].lower()
#     if ext not in ALLOWED_EXTENSIONS:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Unsupported file format extension. Permitted formats include: {ALLOWED_EXTENSIONS}"
#         )

#     # Generate an un-clashable unique local identifier tracking path
#     file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")

#     try:
#         # Buffer save incoming file streaming chunks over to disk space
#         with open(file_path, "wb") as f:
#             shutil.copyfileobj(file.file, f)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to write file stream data to temporary workspace: {e}")

#     # Initialize processing ticket footprint inside your MySQL schema logs right away
#     report = Report(
#         original_filename=file.filename,
#         stored_filename=file_path,
#         file_path=file_path,
#         file_extension=ext,
#         status="processing"
#     )
    
#     try:
#         db.add(report)
#         db.commit()
#         db.refresh(report)
#     except Exception as e:
#         if os.path.exists(file_path):
#             os.remove(file_path)
#         raise HTTPException(status_code=500, detail=f"Failed initialization logs insertion tracking block: {e}")

#     try:
#         print("🔥 Ingestion Complete. Starting Core Extraction Pipeline...")

#         # Hand off control to the linear pipeline: OCR -> Gemini Client Parsing -> RAG -> Summary
#         result = process_report(file_path)

#         print("✅ Core Analytics Chain Execution Met Successfully.")

#         # Structure payload package cleanly matching frontend expectation criteria
#         extracted_data = {
#             "tests": result.get("tests", []),
#             "cleaned_text": result.get("cleaned_text", ""),
#             "rag_context": result.get("rag_context", []),
#             "summary": result.get("summary", ""),
#             "metrics": result.get("metrics", {"method": "gemini_native_flash"}),
#             "requires_review": result.get("requires_review", False)
#         }

#         # Dump results array to structural text column inside database row target
#         update_report(
#             db=db,
#             report_id=report.id,
#             status="completed",
#             extracted_text=json.dumps(extracted_data),
#             summary=extracted_data["summary"]
#         )

#         print("🎉 Transaction logged and completed smoothly.")
#         return {
#             "status": "success",
#             "report_id": report.id,
#             "data": extracted_data
#         }

#     except Exception as e:
#         print(f"❌ Critical Processing Interruption Triggered: {e}")
#         update_report(db=db, report_id=report.id, status="failed", summary=str(e))
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         # Failsafe cleanup tracking to protect available disk space metrics
#         if os.path.exists(file_path):
#             os.remove(file_path)

@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Receives incoming file payloads, initializes processing states, 
    and executes the linear processing pipeline sequence.
    Exposes raw ocr text, structured tests, rag context, and clinical summary.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing valid upload file name metadata.")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format extension. Permitted formats include: {ALLOWED_EXTENSIONS}"
        )

    # Generate an un-clashable unique local identifier tracking path
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")

    try:
        # Buffer save incoming file streaming chunks over to disk space
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file stream data to temporary workspace: {e}")

    # Initialize processing ticket footprint inside your MySQL schema logs right away
    report = Report(
        original_filename=file.filename,
        stored_filename=file_path,
        file_path=file_path,
        file_extension=ext,
        status="processing"
    )
    
    try:
        db.add(report)
        db.commit()
        db.refresh(report)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed initialization logs insertion tracking block: {e}")

    try:
        print("🔥 Ingestion Complete. Starting Core Extraction Pipeline...")

        # Hand off control to the linear pipeline: OCR -> Gemini Client Parsing -> RAG -> Summary
        result = process_report(file_path)

        print("✅ Core Analytics Chain Execution Met Successfully.")

        # Structure payload package cleanly matching verified debugging criteria
        extracted_data = {
            "cleaned_text": result.get("cleaned_text", ""), # <-- Captures raw text cleanly now
            "tests": result.get("tests", []),               # <-- Houses your pristine structured JSON array
            "rag_context": result.get("rag_context", []),   # <-- Fetched medical context rules
            "summary": result.get("summary", ""),           # <-- Patient-friendly clinical overview
            "metrics": result.get("metrics", {"method": "gemini_native_flash"}),
            "requires_review": result.get("requires_review", False)
        }

        # Dump complete dictionary array to structural text column inside database row target
        update_report(
            db=db,
            report_id=report.id,
            status="completed",
            extracted_text=json.dumps(extracted_data),
            summary=extracted_data["summary"]
        )

        print("🎉 Transaction logged and completed smoothly.")
        return {
            "status": "success",
            "report_id": report.id,
            "data": extracted_data
        }

    except Exception as e:
        print(f"❌ Critical Processing Interruption Triggered: {e}")
        update_report(db=db, report_id=report.id, status="failed", summary=str(e))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Failsafe cleanup tracking to protect available disk space metrics
        if os.path.exists(file_path):
            os.remove(file_path)
# =====================================
# ROUTE 2: GET REPORT RECORD BY ID (FIXED)
# =====================================
@router.get("/report/{report_id}")
def get_report_results(report_id: int, db: Session = Depends(get_db)):
    """
    Fetches the completed parsing records and clinical summary vectors 
    for a specific report ID from the database.
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"No report record discovered matching ID: {report_id}")

    # De-serialize the raw structural text blob if entries are populated, otherwise handle gracefully
    parsed_json_data = None
    if report.extracted_text:
        try:
            parsed_json_data = json.loads(report.extracted_text)
        except Exception as e:
            logger.error(f"Failed decoding database text mapping array: {e}")

    return {
        "status": "success",
        "report_id": report.id,
        "filename": report.original_filename,
        "processing_status": report.status,
        "summary": report.summary,
        "extracted_data": parsed_json_data
    }