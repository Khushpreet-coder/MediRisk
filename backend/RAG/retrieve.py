# import chromadb
# from sentence_transformers import SentenceTransformer
# from typing import List, Dict, Optional

# # =====================================
# # Initialize Embedding Model & ChromaDB
# # =====================================
# model = SentenceTransformer("all-MiniLM-L6-v2")

# client = chromadb.PersistentClient(
#     path="./rag/chroma_db"
# )

# collection = client.get_collection(
#     name="medical_knowledge"
# )


# # =====================================
# # NOISE REMOVAL PATTERNS
# # =====================================
# NOISE_PATTERNS = [
#     "page",
#     "signature",
#     "end of report",
#     "www",
#     "http",
#     "email",
#     "phone",
#     "fax",
#     "address",
#     "hospital",
#     "diagnostic",
#     "center",
#     "clinic",
#     "download",
#     "scan to validate",
#     "ref no",
#     "doctor",
#     "physician",
#     "timestamp",
#     "date:",
#     "time:",
#     "report id"
# ]

# MIN_CHUNK_LENGTH = 50
# MIN_WORD_COUNT = 5


# def is_noise(text: str) -> bool:
#     """Check if text is noisy OCR artifacts or unrelated content."""
#     if not text:
#         return True
    
#     text_lower = text.lower().strip()
    
#     # Too short to be meaningful
#     if len(text_lower) < MIN_CHUNK_LENGTH:
#         return True
    
#     # Too few words
#     if text_lower.count(" ") < MIN_WORD_COUNT:
#         return True
    
#     # Contains noise patterns
#     if any(pattern in text_lower for pattern in NOISE_PATTERNS):
#         return True
    
#     # Mostly numbers (page numbers, timestamps)
#     digit_count = sum(1 for c in text_lower if c.isdigit())
#     if digit_count > len(text_lower) * 0.5:
#         return True
    
#     return False


# def filter_by_category(results: Dict, category: str) -> List[str]:
#     """
#     Filter retrieval results to only include chunks from specific category.
    
#     Args:
#         results: ChromaDB query results with metadata
#         category: Medical test category (e.g., "cbc", "lft", "kidney_test")
    
#     Returns:
#         Filtered list of documents
#     """
    
#     documents = results.get("documents", [[]])[0]
#     metadatas = results.get("metadatas", [[]])[0]
    
#     filtered = []
    
#     for i, doc in enumerate(documents):
#         if i < len(metadatas):
#             meta = metadatas[i]
#             doc_category = meta.get("category", "").lower()
            
#             # Match category
#             if doc_category == category.lower():
#                 if not is_noise(doc):
#                     filtered.append(doc)
    
#     return filtered


# def retrieve_context_filtered(
#     query: str,
#     category: str = None,
#     n_results: int = 3
# ) -> List[str]:
#     """
#     Retrieve relevant RAG context with metadata filtering.
    
#     Features:
#     - Query embedding search
#     - Category filtering (if provided)
#     - Noise removal
#     - Limited result size (default 3)
    
#     Args:
#         query: Search query (from abnormal findings)
#         category: Medical test category (e.g., "cbc")
#         n_results: Number of results to return (default 3)
    
#     Returns:
#         List of relevant, clean RAG chunks
#     """
    
#     if not query or not query.strip():
#         return []
    
#     try:
#         # Encode query
#         query_embedding = model.encode(query).tolist()
        
#         # Query ChromaDB with metadata filter if category provided
#         where_clause = None
#         if category:
#             where_clause = {"category": category.lower()}
        
#         results = collection.query(
#             query_embeddings=[query_embedding],
#             n_results=n_results,
#             where=where_clause
#         )
        
#         # Extract documents
#         documents = results.get("documents", [[]])[0]
        
#         # Remove noise
#         cleaned = []
#         for doc in documents:
#             if not is_noise(doc):
#                 cleaned.append(doc)
        
#         return cleaned
    
#     except Exception as e:
#         print(f"⚠️ Retrieval error: {e}")
#         return []


# def retrieve_context(query: str, top_k: int = 3, category: str = None) -> List[str]:
#     """
#     Legacy compatibility wrapper. Use retrieve_context_filtered() instead.
    
#     Args:
#         query: Search query
#         top_k: Number of results (default 3, was old default 5)
#         category: Optional category filter
    
#     Returns:
#         List of relevant chunks
#     """
#     return retrieve_context_filtered(query, category=category, n_results=top_k)


# def is_context_weak(context: List[str]) -> bool:
#     """
#     Check if retrieval context is insufficient.
    
#     Args:
#         context: List of retrieved chunks
    
#     Returns:
#         True if context is weak, False if adequate
#     """
    
#     if not context:
#         return True
    
#     if len(context) < 1:
#         return True
    
#     # Check total meaningful length
#     total_length = sum(len(c) for c in context)
#     if total_length < 100:
#         return True
    
#     return False


# def rank_rag_chunks(
#     chunks: List[str],
#     abnormal_tests: List[Dict] = None,
#     top_k: int = 3
# ) -> List[str]:
#     """
#     Rank retrieved chunks by relevance to abnormal findings.
    
#     Scoring factors:
#     - Keyword match with test names (high weight)
#     - Content type (interpretation > normal_range > parameter)
#     - Chunk length (too short = penalized)
    
#     Args:
#         chunks: List of retrieved chunks
#         abnormal_tests: List of abnormal test dicts with test_name
#         top_k: Number of top chunks to return
    
#     Returns:
#         Top-k ranked chunks
#     """
    
#     if not chunks:
#         return []
    
#     abnormal_tests = abnormal_tests or []
    
#     # Build keywords from abnormal test names
#     keywords = set()
#     for test in abnormal_tests:
#         test_name = test.get("test_name", "").lower()
#         if test_name:
#             keywords.add(test_name)
#             # Also add parts of the name
#             for word in test_name.split():
#                 if len(word) > 2:
#                     keywords.add(word)
    
#     def score_chunk(chunk: str) -> float:
#         """Score a chunk based on relevance."""
#         if not chunk:
#             return -999
        
#         score = 0.0
#         chunk_lower = chunk.lower()
        
#         # Keyword matching (high weight)
#         for keyword in keywords:
#             if keyword in chunk_lower:
#                 score += 10
        
#         # Content type scoring
#         if "interpretation" in chunk_lower:
#             score += 5
#         elif "normal range" in chunk_lower:
#             score += 3
#         elif "parameter" in chunk_lower or "type" in chunk_lower:
#             score += 1
        
#         # Length scoring (too short or too long is bad)
#         chunk_length = len(chunk)
#         if chunk_length < 80:
#             score -= 5
#         elif chunk_length > 1000:
#             score -= 2
#         else:
#             score += 2
        
#         # Penalize if mostly numbers
#         digit_ratio = sum(1 for c in chunk if c.isdigit()) / len(chunk)
#         if digit_ratio > 0.5:
#             score -= 3
        
#         return score
    
#     # Score all chunks
#     scored = [(chunk, score_chunk(chunk)) for chunk in chunks]
    
#     # Sort by score (descending)
#     ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    
#     # Return top-k chunks only
#     return [chunk for chunk, score in ranked[:top_k]]


# def clean_rag_context(results: List[str]) -> List[str]:
#     """Clean retrieval results."""
#     return [doc for doc in results if not is_noise(doc)]


# ============================================
# retrieve.py
# ============================================

# import chromadb

# from sentence_transformers import SentenceTransformer

# import os

# BASE_DIR = os.path.dirname(__file__)

# CHROMA_PATH = os.path.join(
#     BASE_DIR,
#     "chroma_db"
# )

# client = chromadb.PersistentClient(
#     path=CHROMA_PATH
# ) 
# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )



# collection = client.get_collection(
#     name="medical_knowledge"
# )


# NOISE_WORDS = [
#     "download",
#     "doctor",
#     "page",
#     "hospital",
#     "signature",
#     "address",
#     "phone",
#     "timing",
#     "registration"
# ]


# def is_noise(text: str):

#     text = text.lower()

#     # too short
#     if len(text) < 25:
#         return True

#     # corrupted chunks
#     bad_patterns = [
#         "�",
#         "download",
#         "page",
#         "hospital",
#         "phone",
#         "address",
#         "signature",
#         "registration"
#     ]

#     for word in bad_patterns:

#         if word in text:
#             return True

#     # excessive symbols
#     symbol_count = sum(
#         1 for c in text
#         if not c.isalnum() and c not in " .,-:/%"
#     )

#     if symbol_count > 10:
#         return True

#     return False


# def retrieve_context(
#     query: str,
#     category: str = None,
#     top_k: int = 3
# ):

#     try:

#         embedding = model.encode(query).tolist()

#         where_clause = None

#         if category and category != "general":

#             where_clause = {
#                 "category": category
#             }

#         results = collection.query(

#             query_embeddings=[embedding],

#             n_results=top_k,

#             where=where_clause
#         )

#         documents = results["documents"][0]

#         cleaned = []

#         for doc in documents:

#             if not is_noise(doc):

#                 cleaned.append(doc)

#         return cleaned

#     except Exception as e:

#         print("Retrieval error:", e)

#         return []


# def rank_rag_chunks(chunks, abnormal_tests, top_k=3):

#     if not chunks:
#         return []

#     keywords = []

#     for test in abnormal_tests:

#         name = test.get("test_name", "")

#         keywords.extend(name.lower().split())

#     scored = []

#     for chunk in chunks:

#         score = 0

#         lower = chunk.lower()

#         for keyword in keywords:

#             if keyword in lower:
#                 score += 10

#         if "may indicate" in lower:
#             score += 5

#         if len(chunk) > 50:
#             score += 2

#         scored.append((chunk, score))

#     scored.sort(
#         key=lambda x: x[1],
#         reverse=True
#     )

#     return [x[0] for x in scored[:top_k]]


# def is_context_weak(context):

#     """
#     Detect weak or empty RAG retrieval.
#     """

#     if not context:
#         return True

#     if len(context) == 0:
#         return True

#     total_length = sum(len(c) for c in context)

#     if total_length < 80:
#         return True

#     return False

# import chromadb
# from sentence_transformers import SentenceTransformer
# import os

# BASE_DIR = os.path.dirname(__file__)
# CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

# client = chromadb.PersistentClient(path=CHROMA_PATH)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# collection = client.get_collection(name="medical_knowledge")


# def is_noise(text: str) -> bool:
#     text = text.lower()

#     if len(text) < 25:
#         return True

#     bad_patterns = [
#         "�", "download", "page", "hospital",
#         "phone", "address", "signature", "registration"
#     ]

#     if any(p in text for p in bad_patterns):
#         return True

#     symbol_count = sum(
#         1 for c in text
#         if not c.isalnum() and c not in " .,-:/%"
#     )

#     return symbol_count > 10


# def retrieve_context(query: str, category: str = None, top_k: int = 5):

#     try:
#         embedding = model.encode(query).tolist()

#         where_clause = None
#         if category and category != "general":
#             where_clause = {"category": category}

#         results = collection.query(
#             query_embeddings=[embedding],
#             n_results=top_k,
#             where=where_clause
#         )

#         docs = results.get("documents", [[]])[0]

#         return [d for d in docs if not is_noise(d)]

#     except Exception as e:
#         print("Retrieval error:", e)
#         return []


# def rank_rag_chunks(chunks, abnormal_tests, top_k=3):

#     if not chunks:
#         return []

#     keywords = []
#     for test in abnormal_tests:
#         name = test.get("test_name", "")
#         keywords.extend(name.lower().split())

#     scored = []

#     for chunk in chunks:
#         score = 0
#         lower = chunk.lower()

#         for kw in keywords:
#             if kw in lower:
#                 score += 10

#         if "normal" in lower:
#             score -= 2

#         if len(chunk) > 50:
#             score += 2

#         scored.append((chunk, score))

#     scored.sort(key=lambda x: x[1], reverse=True)

#     return [c[0] for c in scored[:top_k]]


# def is_context_weak(context) -> bool:
#     if not context:
#         return True

#     total_len = sum(len(c) for c in context)

#     return total_len < 80


import chromadb
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict, Optional


# =========================================================
# INIT
# =========================================================

BASE_DIR = os.path.dirname(__file__)
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)

model = SentenceTransformer("all-MiniLM-L6-v2")

collection = client.get_collection(name="medical_knowledge")

def retrieve(query, category=None):
    where_filter = {}

    if category:
        where_filter["category"] = category

    results = collection.query(
        query_texts=[query],
        n_results=5,
        where=where_filter
    )

    return results


# =========================================================
# NOISE FILTER (OCR CLEANING)
# =========================================================

def is_noise(text: str) -> bool:
    text = text.lower().strip()

    if len(text) < 20:
        return True

    noise_patterns = [
        "download", "page", "hospital", "address",
        "phone", "signature", "registration",
        "www", "email", "fax"
    ]

    if any(p in text for p in noise_patterns):
        return True

    # OCR garbage detection
    symbol_ratio = sum(
        1 for c in text if not c.isalnum() and c not in " .,-:/%"
    ) / max(len(text), 1)

    if symbol_ratio > 0.35:
        return True

    return False


# =========================================================
# MAIN RETRIEVAL FUNCTION
# =========================================================

def retrieve_context(
    query: str,
    category: Optional[str] = None,
    top_k: int = 5
) -> List[str]:

    try:
        # normalize query embedding
        query_embedding = model.encode(
            query,
            normalize_embeddings=True
        ).tolist()

        # metadata filter (optional)
        where_clause = None
        if category and category != "general":
            where_clause = {"category": category}

        # retrieve more for reranking
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 3,
            where=where_clause
        )

        docs = results.get("documents", [[]])[0]

        # filter noise
        cleaned_docs = [d for d in docs if not is_noise(d)]

        return cleaned_docs[:top_k]

    except Exception as e:
        print("❌ Retrieval error:", e)
        return []


# =========================================================
# MEDICAL RERANKING (IMPORTANT)
# =========================================================

def rank_rag_chunks(
    chunks: List[str],
    abnormal_tests: List[Dict],
    top_k: int = 3
) -> List[str]:

    if not chunks:
        return []

    # extract keywords from abnormal tests
    keywords = set()
    for test in abnormal_tests:
        name = test.get("test_name", "")
        keywords.update(name.lower().split())

    # strong medical boost terms
    medical_boost = {
        "hb": 5,
        "hemoglobin": 5,
        "wbc": 5,
        "rbc": 5,
        "platelet": 5,
        "creatinine": 5,
        "urea": 5,
        "glucose": 5,
        "cholesterol": 5,
        "triglyceride": 5,
        "tsh": 5,
        "t3": 5,
        "t4": 5
    }

    scored = []

    for chunk in chunks:
        lower = chunk.lower()
        score = 0

        # keyword match from abnormal tests
        for kw in keywords:
            if kw and kw in lower:
                score += 8

        # medical entity boost
        for term, boost in medical_boost.items():
            if term in lower:
                score += boost

        # section importance boost
        if "interpretation" in lower:
            score += 4

        if "normal range" in lower:
            score += 2

        if "content:" in lower:
            score += 1

        # slight penalty for noise-like chunks
        if "page" in lower or "download" in lower:
            score -= 5

        scored.append((chunk, score))

    scored.sort(key=lambda x: x[1], reverse=True)

    return [c[0] for c in scored[:top_k]]


# =========================================================
# CONTEXT QUALITY CHECK
# =========================================================

def is_context_weak(context: List[str]) -> bool:
    if not context:
        return True

    total_len = sum(len(c) for c in context)
    avg_len = total_len / len(context)

    return avg_len < 40


# =========================================================
# FULL PIPELINE HELPER (OPTIONAL BUT USEFUL)
# =========================================================

def retrieve_and_rank(
    query: str,
    abnormal_tests: Optional[List[Dict]] = None,
    category: str = None,
    top_k: int = 5
) -> List[str]:

    raw_chunks = retrieve_context(query, category, top_k)

    if abnormal_tests:
        return rank_rag_chunks(raw_chunks, abnormal_tests, top_k=top_k)

    return raw_chunks