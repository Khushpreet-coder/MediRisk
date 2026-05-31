import os
import json
import uuid
import shutil
import logging
from typing import Dict
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from OCRHandling.enhanced_pipeline import process_report_enhanced as process_report

from database import SessionLocal
from models.report_model import Report
from auth.dependencies import get_current_user
from models.users import User

logger = logging.getLogger(__name__)
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def get_db():
    """Provides a transactional database session per network request flow."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
        logger.error(f"Database update failure encountered on Report {report_id}: {e}")


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing valid upload file name metadata.")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format extension. Permitted formats include: {ALLOWED_EXTENSIONS}"
        )

    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file stream data to temporary workspace: {e}")

    report = Report(
        user_id=current_user.id,
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
        print("Ingestion Complete. Starting Core Extraction Pipeline...")

        result = process_report(file_path)

        print("Core Analytics Chain Execution Met Successfully.")

        extracted_data = {
            "cleaned_text": result.get("cleaned_text", ""),
            "tests": result.get("tests", []),
            "rag_context": result.get("rag_context", []),
            "summary": result.get("summary", ""),
            "metrics": result.get("metrics", {"method": "gemini_native_flash"}),
            "requires_review": result.get("requires_review", False)
        }

        update_report(
            db=db,
            report_id=report.id,
            status="completed",
            extracted_text=json.dumps(extracted_data),
            summary=extracted_data["summary"]
        )

        print("Transaction logged and completed smoothly.")
        return {
            "status": "success",
            "report_id": report.id,
            "data": extracted_data
        }

    except Exception as e:
        print(f"Critical Processing Interruption Triggered: {e}")
        update_report(db=db, report_id=report.id, status="failed", summary=str(e))
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/report/{report_id}")
def get_report_results(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail=f"No report record discovered matching ID: {report_id}")

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


@router.get("/my-reports")
def get_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reports = db.query(Report).filter(
        Report.user_id == current_user.id
    ).order_by(Report.created_at.desc()).all()

    return {
        "status": "success",
        "reports": [
            {
                "report_id": r.id,
                "filename": r.original_filename,
                "status": r.status,
                "created_at": str(r.created_at) if r.created_at else None
            }
            for r in reports
        ]
    }


@router.delete("/my-reports")
def clear_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(Report).filter(Report.user_id == current_user.id).delete()
    db.commit()
    return {"status": "success", "message": "All reports deleted"}


@router.delete("/report/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
    return {"status": "success", "message": "Report deleted"}
