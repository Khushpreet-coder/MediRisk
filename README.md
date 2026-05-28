# 🏥 AI-Powered Medical Report Summarizer

An advanced, production-grade end-to-end medical report digitization, structuring, validation, and AI-guided summarization system. 

This platform transforms unstructured medical reports (PDFs, scans, camera captures) into structured, highly accurate clinical insights using a **Multi-Engine OCR Ensemble**, an **Adaptive LLM Consensus Engine**, and a **Medical Retrieval-Augmented Generation (RAG)** pipeline powered by ChromaDB.

---

## 🚀 Key Features

* **Multi-Engine Ensemble OCR**: Integrates both `Tesseract OCR` and `EasyOCR` to process images and PDFs. Scores character-level and word-level confidence dynamically to extract the highest-quality text.
* **Confidence-Based Adaptive Pipeline**:
  - **High Confidence (>85%)**: Processes fast via standard LLM parser.
  - **Medium Confidence (70% - 85%)**: Validates and consensus-votes across multiple LLM models.
  - **Low Confidence (<70%)**: Triggers the full ensemble validator and automatically flags for human review.
* **Consensus LLM Voting**: Uses Groq-hosted `llama-3.3-70b` and `llama-3.1-70b` models to vote on parsed medical entities (test name, value, unit, reference range, status) to eliminate LLM hallucinations.
* **Medical Retrieval-Augmented Generation (RAG)**:
  - Embeds scientific literature, dictionaries, and lab-manual references into a persistent `ChromaDB` vector store using `sentence-transformers/all-MiniLM-L6-v2`.
  - Performs real-time semantic lookup for out-of-range parameters.
  - **Google Fallback** searches public medical libraries when vector database context is missing or low-confidence.
* **FastAPI Secure Backend**: Featuring SQLAlchemy ORM, robust JWT token-based auth (`/auth/register`, `/auth/login`), uploads management, and custom request validations.
* **Modern React + Vite Frontend**: Premium dashboard web application with reactive upload, responsive landing pages, patient dashboard, authentication modal, and intuitive layout.

---

## 📐 Architecture Overview

```mermaid
graph TD
    A[Upload PDF/Image] --> B[Multi-Engine OCR Ensemble]
    B -->|Tesseract / EasyOCR| C[Normalized Raw Text]
    C --> D[Regex & Text Cleaning]
    D --> E[Adaptive Processing Engine]
    
    E -->|Confidence > 85%| F[Standard LLM Parsing]
    E -->|Confidence 70-85%| G[LLM Ensemble Voting]
    E -->|Confidence < 70%| H[Ensemble + Human Review Flag]
    
    F & G & H --> I[Structured JSON Laboratory Data]
    I --> J[ChromaDB Medical RAG Lookup]
    J -->|Context Retrieval| K[AI Medical Summary Generator]
    K --> L[Structured JSON + Clinical Narrative Result]
```

---

## 📂 Project Structure

```
Medical_Report_Summarizer/
│
├── backend/                        # FastAPI Backend Service
│   ├── OCRHandling/                # OCR Parsing & Adaptive Logic
│   │   ├── enhanced_pipeline.py    # Main confidence-based orchestration
│   │   ├── ensemble_processor.py   # OCR & LLM Ensemble voting modules
│   │   ├── ocr_service.py          # PyTesseract & EasyOCR integrations
│   │   ├── llm_parser.py           # LLM structure formatting
│   │   ├── text_cleaner.py         # Advanced regex cleansers
│   │   └── validator.py            # Pydantic schemas and schema validation
│   │
│   ├── RAG/                        # RAG & ChromaDB Pipeline
│   │   ├── chroma_db/              # Persistent Chroma Vector DB store
│   │   ├── knowledge_base/         # Scientific reference documents & texts
│   │   ├── embed_knowledge.py      # Script to chunk and populate Chroma DB
│   │   ├── retrieve.py             # Vector store query & retrieval utilities
│   │   └── llm_summary.py          # Summary orchestration using RAG context
│   │
│   ├── routes/                     # FastAPI Routing
│   │   ├── auth.py                 # User Auth (/auth/register, /auth/login)
│   │   └── reports.py              # Report Uploads (/upload, /reports)
│   │
│   ├── models/                     # SQLAlchemy Models
│   ├── database.py                 # SQLite/MySQL Session & Engine Setup
│   └── main.py                     # Entry point for FastAPI Application
│
├── frontend/                       # React Web Application
│   ├── src/
│   │   ├── components/             # Reusable UI Elements (UploadSection, AuthModal, etc.)
│   │   ├── pages/                  # Main Router Views (LandingPage, Dashboard)
│   │   ├── App.jsx                 # Routing Setup
│   │   └── main.jsx                # Web Application Entry Point
│   ├── package.json                # NPM configuration & dependencies
│   └── vite.config.js              # Vite bundler parameters
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have the following installed on your machine:
* Python 3.9+
* Node.js 18+ and npm
* Tesseract OCR Engine (installed on system path)

---

### 2. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy mysql-connector-python easyocr pytesseract sentence-transformers chromadb pydantic python-dotenv python-multipart groq pillow PyMuPDF
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the `backend/` directory:
   ```env
   DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/medical_users
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=your_super_secret_jwt_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Initialize ChromaDB Vector Store**:
   Place your medical books or reference texts inside `backend/RAG/knowledge_base/` as `.txt` files. Then run the chunking and embedding pipeline:
   ```bash
   python RAG/embed_knowledge.py
   ```

6. **Run the Backend Server**:
   ```bash
   uvicorn main:app --reload
   ```
   *The backend will be running at `http://localhost:8000`.*
   *Interactive API documentation will be available at `http://localhost:8000/docs`.*

---

### 3. Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

2. **Install frontend packages**:
   ```bash
   npm install
   ```

3. **Launch the development server**:
   ```bash
   npm run dev
   ```
   *The client web application will be live at `http://localhost:5173`.*

---

## 📌 API Reference

### Authentication
* **POST** `/auth/register` - Registers a new user.
* **POST** `/auth/login` - Authenticates user and issues JWT.

### Reports
* **POST** `/upload` - Uploads a medical report (`.pdf`, `.png`, `.jpg`, `.jpeg`), processes it through the entire OCR-RAG-LLM pipeline, and returns structured data and clinical summary.

---

## 🔬 Core Technologies

* **FastAPI**: Modern, high-performance web framework for Python.
* **SQLAlchemy**: Powerful Python SQL Toolkit & ORM mapping.
* **ChromaDB**: AI-native vector database for semantic RAG lookups.
* **PyTesseract & EasyOCR**: Multi-layered character recognition engines.
* **React + Vite**: Blazing fast modern frontend development tooling.
* **Groq SDK**: Ultra-low latency Llama inference API integration.

---

## ⚖️ License
This project is open-source and available under the MIT License.
