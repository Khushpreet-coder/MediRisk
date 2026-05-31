from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from database import engine, Base
from routes.auth import router as auth_router
from routes.reports import router as reports_router
from routes.chat import router as chat_router
from RAG.retrieve import retrieve_context

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medical Report Summarizer API",
    version="1.0.0",
    description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
app.include_router(chat_router, tags=["Chat"])

@app.get("/")
def root():
    return {"status": "success", "message": "API running 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/query")
def query_medical(data: dict):
    return {
        "status": "success",
        "results": retrieve_context(
            query=data.get("query"),
            category=data.get("category"),
            top_k=5
        )
    }
