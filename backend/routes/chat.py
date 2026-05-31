import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models.report_model import Report
from models.users import User
from auth.dependencies import get_current_user
from llm_clients import call_groq

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    report_id: int | None = None


SYSTEM_PROMPT = """You are a helpful medical analysis assistant. Answer questions clearly and concisely.
Use the provided context (report data and medical knowledge) to give accurate answers.
If you're unsure, say so. Do not make up information.
Always remind users to consult a real doctor for medical decisions."""


@router.post("/chat")
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    context_parts = []

    if req.report_id:
        report = db.query(Report).filter(
            Report.id == req.report_id,
            Report.user_id == current_user.id
        ).first()
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        extracted = {}
        if report.extracted_text:
            try:
                extracted = json.loads(report.extracted_text)
            except Exception:
                extracted = {}

        tests = extracted.get("tests", [])
        summary = report.summary or extracted.get("summary", "")

        if tests:
            tests_str = "\n".join(
                f"- {t.get('test_name', '?')}: {t.get('value', '?')} {t.get('unit', '')} ({t.get('status', '?')})"
                for t in tests
            )
            context_parts.append(f"## Lab Results\n{tests_str}")

        if summary:
            context_parts.append(f"## Summary\n{summary}")

    context = "\n\n".join(context_parts) if context_parts else ""

    prompt = f"{SYSTEM_PROMPT}\n\n"
    if context:
        prompt += f"Here is the patient's report data:\n{context}\n\n"
    prompt += f"User question: {req.message}"

    response = call_groq(prompt, model="llama-3.1-8b-instant")

    if not response:
        return {"response": "Sorry, I couldn't process that request. Please try again."}

    return {"response": response}
