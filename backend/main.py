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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

# Import Routers
from routes.auth import router as auth_router
from routes.reports import router as reports


# Create DB tables
Base.metadata.create_all(bind=engine)


# FastAPI app
app = FastAPI(
    title="Medical Report Summarizer API",
    version="1.0.0",
    description="AI-powered Medical Report Summarizer using OCR + RAG + LLM"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ROUTES (IMPORTANT FIX HERE)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.include_router(reports, tags=["Reports"])


# Root
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Medical Report Summarizer API running 🚀"
    }


# Health
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }