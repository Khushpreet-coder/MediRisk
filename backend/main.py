# from fastapi import FastAPI
# from database import engine, Base
# from routes.reports import router as report_router



# # 👇 VERY IMPORTANT (register models)
# from models import *

# # 👇 Import routers
# from routes.auth import router as auth_router

# # 🚀 Create app
# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0"
# )

# # 🧱 Create tables
# Base.metadata.create_all(bind=engine)

# # 🔐 Include auth routes
# app.include_router(auth_router)

# app.include_router(report_router)


# # 🏠 Root route
# @app.get("/")
# def root():
#     return {"message": "API is running 🚀"}


# from fastapi import FastAPI

# from database import engine, Base
# from models import *  # IMPORTANT: register models

# # Routers
# from routes.auth import router as auth_router
# from routes.reports import router as report_router

# # 🚀 Create FastAPI app
# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0"
# )

# # 🧱 Create database tables
# Base.metadata.create_all(bind=engine)

# # 🔐 Include routers with prefixes (clean API structure)
# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(report_router, prefix="/reports", tags=["Reports"])


# # 🏠 Health check / root route
# @app.get("/")
# def root():
#     return {
#         "message": "Medical Report Summarizer API is running 🚀"
#     }

# from fastapi import FastAPI

# from database import engine, Base

# # Import ONLY users model
# from models.users import User

# # Routers
# from routes.auth import router as auth_router
# from routes.reports import router as report_router


# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0"
# )

# # Create ONLY users table
# Base.metadata.create_all(bind=engine)

# # Routes
# app.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Auth"]
# )

# app.include_router(
#     report_router,
#     prefix="/reports",
#     tags=["Reports"]
# )


# @app.get("/")
# def root():

#     return {
#         "message": "Medical Report Summarizer API running 🚀"
#     }


# from fastapi import FastAPI
# from pydantic import BaseModel

# from database import engine, Base
# from models.users import User
# from rag.rag_pipeline import generate_summary  # you will create this

# from routes.auth import router as auth_router
# from routes.reports import router as report_router

# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0"
# )

# Base.metadata.create_all(bind=engine)

# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(report_router, prefix="/reports", tags=["Reports"])


# @app.get("/")
# def root():
#     return {
#         "message": "Medical Report Summarizer API running 🚀"
#     }


# class SummaryRequest(BaseModel):
#     text: str


# # =========================
# # Summary Route
# # =========================
# @app.post("/summary")
# def get_summary(request: SummaryRequest):
#     text = request.text

#     summary = generate_summary(text)

#     return {
#         "original_text": text,
#         "summary": summary
#     }

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from database import engine, Base

# # Import routers
# from routes.auth import router as auth_router
# from routes.reports import router as report_router


# # =========================================
# # Create Database Tables
# # =========================================
# Base.metadata.create_all(bind=engine)


# # =========================================
# # Initialize FastAPI App
# # =========================================
# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0",
#     description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
# )


# # =========================================
# # Enable CORS
# # =========================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # change later in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # =========================================
# # Include Routers
# # =========================================
# app.include_router(
#     auth_router,
#     prefix="/auth",
#     tags=["Authentication"]
# )

# app.include_router(
#     report_router,
#     prefix="/reports",
#     tags=["Reports"]
# )


# # =========================================
# # Root Endpoint
# # =========================================
# @app.get("/")
# def root():
#     return {
#         "status": "success",
#         "message": "Medical Report Summarizer API running 🚀"
#     }


# # =========================================
# # Health Check Endpoint
# # =========================================
# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy"
#     }


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from database import engine, Base

# # Import Routers
# from routes.auth import router as auth_router
# from routes.reports import router as reports



# # =========================================
# # Create Database Tables
# # =========================================
# Base.metadata.create_all(bind=engine)


# # =========================================
# # Initialize FastAPI App
# # =========================================
# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0",
#     description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
# )


# # =========================================
# # Enable CORS
# # =========================================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # change in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # =========================================
# # Include Routers
# # =========================================
# app.include_router(auth_router)



# # =========================================
# # Root Endpoint
# # =========================================
# @app.get("/")
# def root():
#     return {
#         "status": "success",
#         "message": "Medical Report Summarizer API running 🚀"
#     }


# # =========================================
# # Health Check Endpoint
# # =========================================
# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy"
#     }

# from RAG import retrieve
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from database import engine, Base
# from fastapi import APIRouter
# from RAG.llm_summary import generate_medical_summary

# router = APIRouter()
# # Import Routers
# from routes.auth import router as auth_router
# from routes.reports import router as reports


# # Create DB tables
# Base.metadata.create_all(bind=engine)


# # FastAPI app
# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0",
#     description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
# )


# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ROUTES
# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(reports, tags=["Reports"])


# # Root
# @app.get("/")
# def root():
#     return {
#         "status": "success",
#         "message": "Medical Report Summarizer API running 🚀"
#     }


# # Health
# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy"
#     }

# @app.post("/query")
# def query_medical(data: dict):
#     query = data["query"]
#     category = data.get("category")

#     results = retrieve(query, category)

#     context = "\n\n".join(results["documents"][0])

#     return {
#         "query": query,
#         "context": context
#     }

# @router.post("/generate-summary")
# def generate_summary_api(report_data: dict):
#     summary = generate_medical_summary(report_data)
#     return {
#         "status": "success",
#         "summary": summary
#     }


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from RAG.llm_summary import generate_medical_summary
# from fastapi import APIRouter

# router = APIRouter()

# from database import engine, Base

# # Routers
# from routes.auth import router as auth_router
# from routes.reports import router as reports_router

# # RAG + Summary
# from RAG.retrieve import retrieve_context



# # =====================================
# # CREATE DATABASE TABLES
# # =====================================

# Base.metadata.create_all(bind=engine)


# # =====================================
# # FASTAPI APP
# # =====================================

# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0",
#     description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
# )


# # =====================================
# # CORS
# # =====================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # =====================================
# # INCLUDE ROUTERS
# # =====================================

# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(reports_router, prefix="/reports", tags=["Reports"])


# # =====================================
# # ROOT
# # =====================================

# @app.get("/")
# def root():
#     return {
#         "status": "success",
#         "message": "Medical Report Summarizer API running 🚀"
#     }


# # =====================================
# # HEALTH CHECK
# # =====================================

# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy"
#     }


# # =====================================
# # RAG QUERY TEST API
# # =====================================

# @app.post("/query")
# def query_medical(data: dict):

#     query = data.get("query")
#     category = data.get("category")

#     results = retrieve_context(
#         query=query,
#         category=category,
#         top_k=5
#     )

#     return {
#         "status": "success",
#         "query": query,
#         "results": results
#     }


# # =====================================
# # GENERATE MEDICAL SUMMARY
# # =====================================

# @router.post("/generate-summary")
# def generate_summary_api(report_data: dict):

#     summary = generate_medical_summary(report_data)

#     return {
#         "status": "success",
#         "summary": summary
#     }


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from database import engine, Base

# # Routers
# from routes.auth import router as auth_router
# from routes.reports import router as reports_router


# # RAG
# from RAG.retrieve import retrieve_context

# # LLM Summary
# from RAG.llm_summary import generate_medical_summary


# # =====================================
# # CREATE DATABASE TABLES
# # =====================================

# Base.metadata.create_all(bind=engine)


# # =====================================
# # FASTAPI APP
# # =====================================

# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0",
#     description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
# )


# # =====================================
# # CORS
# # =====================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # =====================================
# # INCLUDE ROUTERS
# # =====================================

# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(reports_router, prefix="/reports", tags=["Reports"])


# # =====================================
# # ROOT
# # =====================================

# @app.get("/")
# def root():
#     return {
#         "status": "success",
#         "message": "Medical Report Summarizer API running 🚀"
#     }


# # =====================================
# # HEALTH CHECK
# # =====================================

# @app.get("/health")
# def health_check():
#     return {
#         "status": "healthy"
#     }


# # =====================================
# # RAG QUERY TEST API
# # =====================================

# @app.post("/query")
# def query_medical(data: dict):

#     query = data.get("query")
#     category = data.get("category")

#     results = retrieve_context(
#         query=query,
#         category=category,
#         top_k=5
#     )

#     return {
#         "status": "success",
#         "query": query,
#         "results": results
#     }


# # =====================================
# # GENERATE MEDICAL SUMMARY
# # =====================================

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from database import engine, Base

# from routes.auth import router as auth_router
# from routes.reports import router as reports_router


# from RAG.retrieve import retrieve_context

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="Medical Report Summarizer API",
#     version="1.0.0",
#     description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Routers
# app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(reports_router, prefix="/reports", tags=["Reports"])

# @app.get("/")
# def root():
#     return {"status": "success", "message": "API running 🚀"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# @app.post("/query")
# def query_medical(data: dict):
#     return {
#         "status": "success",
#         "results": retrieve_context(
#             query=data.get("query"),
#             category=data.get("category"),
#             top_k=5
#         )
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks  # optional, but good practice

from database import engine, Base
from routes.auth import router as auth_router # can ignore this import error for now, I'll create this later
from routes.reports import router as reports_router
from RAG.retrieve import retrieve_context

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medical Report Summarizer API",
    version="1.0.0",
    description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
)

# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])

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