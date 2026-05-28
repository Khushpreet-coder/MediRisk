# # from RAG.retrieve import retrieve_context, rank_rag_chunks, is_context_weak
# # from RAG.query_builder import build_queries


# # def generate_summary(structured_data, cleaned_text):

# #     abnormal_tests = structured_data.get("tests", [])

# #     # 🔥 STEP 1: Build smart medical queries
# #     queries = build_queries(structured_data)

# #     all_chunks = []

# #     # 🔥 STEP 2: Query-based retrieval (IMPORTANT FIX)
# #     for q in queries:
# #         chunks = retrieve_context(
# #             q["query"],
# #             q["category"]
# #         )
# #         all_chunks.extend(chunks)

# #     # 🔥 STEP 3: Ranking based on abnormal tests
# #     ranked = rank_rag_chunks(all_chunks, abnormal_tests, top_k=5)

# #     # 🔥 STEP 4: Weak context handling
# #     if is_context_weak(ranked):
# #         ranked = []

# #     return {
# #         "rag_context": ranked
# #     }

# # from RAG.retrieve import (
# #     retrieve_context,
# #     rank_rag_chunks,
# #     is_context_weak
# # )
# # from RAG.query_builder import build_rag_queries, extract_abnormal_tests


# # def generate_summary(structured_data, cleaned_text):
# #     """
# #     Retrieves highly relevant medical reference context for abnormal laboratory findings.
    
# #     1. Extracts abnormal laboratory results.
# #     2. Dynamically builds targeted medical query/category pairs for each out-of-range test.
# #     3. Runs vector database searches filtered by category metadata (to prevent dilution).
# #     4. Performs broader fallback search if the filtered query returns no results.
# #     5. Deduplicates and scores/ranks chunks against the specific abnormal findings.
# #     """
# #     abnormal_tests = extract_abnormal_tests(structured_data)
    
# #     # If no abnormal findings, we don't need semantic RAG context
# #     if not abnormal_tests:
# #         return {
# #             "rag_context": []
# #         }

# #     # Smart medical queries for each abnormal test
# #     queries = build_rag_queries(structured_data)
# #     all_chunks = []

# #     for q in queries:
# #         # Category-specific retrieval to avoid query dilution
# #         chunks = retrieve_context(
# #             query=q["query"],
# #             category=q["category"],
# #             top_k=3
# #         )
        
# #         # Fallback to general/unfiltered search if no matching chunks found under this category
# #         if not chunks and q["category"] != "general":
# #             chunks = retrieve_context(
# #                 query=q["query"],
# #                 category=None,
# #                 top_k=3
# #             )
            
# #         all_chunks.extend(chunks)

# #     # Deduplicate retrieved chunks to save token space
# #     unique_chunks = []
# #     seen = set()
# #     for chunk in all_chunks:
# #         chunk_clean = chunk.strip()
# #         if chunk_clean not in seen:
# #             seen.add(chunk_clean)
# #             unique_chunks.append(chunk)

# #     # Rank chunks according to abnormal findings (keywords match)
# #     ranked = rank_rag_chunks(unique_chunks, abnormal_tests, top_k=5)

# #     # Fallback: if context is weak or empty, run a combined search on all abnormal tests
# #     if is_context_weak(ranked):
# #         combined_query = " ".join([
# #             f"{t.get('test_name', '')} {t.get('status', '')}" 
# #             for t in abnormal_tests
# #         ])
# #         fallback_chunks = retrieve_context(combined_query, category=None, top_k=5)
# #         ranked = rank_rag_chunks(fallback_chunks, abnormal_tests, top_k=5)

# #     if is_context_weak(ranked):
# #         ranked = []

# #     return {
# #     "rag_context": [
# #         {"text": c} for c in ranked
# #     ]
# # }

# #     return {
# #         "rag_context": ranked
# #     }

# from RAG.retrieve import (
#     retrieve_context,
#     rank_rag_chunks,
#     is_context_weak
# )
# from RAG.query_builder import build_rag_queries, extract_abnormal_tests


# # def generate_summary(structured_data):

# #     abnormal_tests = extract_abnormal_tests(structured_data)

# #     if not abnormal_tests:
# #         return {"rag_context": []}

# #     queries = build_rag_queries(structured_data)
# #     all_chunks = []

# #     for q in queries:

# #         chunks = retrieve_context(
# #             query=q["query"],
# #             category=q["category"],
# #             top_k=3
# #         )

# #         if not chunks and q["category"] != "general":
# #             chunks = retrieve_context(
# #                 query=q["query"],
# #                 category=None,
# #                 top_k=3
# #             )

# #         all_chunks.extend(chunks)

# #     # Deduplicate
# #     unique_chunks = []
# #     seen = set()

# #     for chunk in all_chunks:
# #         chunk_clean = chunk.strip()
# #         if chunk_clean not in seen:
# #             seen.add(chunk_clean)
# #             unique_chunks.append(chunk)

# #     # Rank
# #     ranked = rank_rag_chunks(unique_chunks, abnormal_tests, top_k=5)

# #     # Fallback
# #     if is_context_weak(ranked):
# #         combined_query = " ".join([
# #             f"{t.get('test_name', '')} {t.get('status', '')}"
# #             for t in abnormal_tests
# #         ])

# #         fallback_chunks = retrieve_context(combined_query, category=None, top_k=5)
# #         ranked = rank_rag_chunks(fallback_chunks, abnormal_tests, top_k=5)

# #     if is_context_weak(ranked):
# #         ranked = []

# #     # ✅ FINAL CONSISTENT FORMAT (IMPORTANT)
# #     return {
# #         "rag_context": ranked
# #     }

# def generate_summary(structured_data):

#     abnormal_tests = extract_abnormal_tests(structured_data)

#     if not abnormal_tests:
#         return {"rag_context": []}

#     queries = build_rag_queries(structured_data)
#     all_chunks = []

#     for q in queries:
#         chunks = retrieve_context(
#             query=q["query"],
#             category=None,
#             top_k=3
#         )

#         if not chunks:
#             chunks = retrieve_context(
#                 query=q["query"],
#                 category=None,
#                 top_k=3
#             )

#         all_chunks.extend(chunks)

#     # Deduplicate
#     unique_chunks = []
#     seen = set()

#     for chunk in all_chunks:
#         chunk_clean = chunk.strip()
#         if chunk_clean not in seen:
#             seen.add(chunk_clean)
#             unique_chunks.append(chunk)

#     ranked = rank_rag_chunks(unique_chunks, abnormal_tests, top_k=5)

#     if is_context_weak(ranked):
#         combined_query = " ".join(
#             f"{t.get('test_name','')} {t.get('status','')}"
#             for t in abnormal_tests
#         )

#         fallback_chunks = retrieve_context(combined_query, category=None, top_k=5)
#         ranked = rank_rag_chunks(fallback_chunks, abnormal_tests, top_k=5)

#     if is_context_weak(ranked):
#         ranked = []

#     return {
#         "rag_context": ranked
#     }

# # RAG/rag_service.py
# import logging

# logger = logging.getLogger(__name__)

# def generate_summary(data: dict) -> dict:
#     """
#     RAG Context Router. Receives an extracted tests object dictionary 
#     and returns matching vector guide knowledge lines.
#     """
#     tests = data.get("tests", [])
#     logger.info(f"RAG Service processing similarity context routing for {len(tests)} entries.")
    
#     # Safe fallback array if your ChromaDB path configurations are not fully initialized yet
#     return {
#         "rag_context": [
#             "Baseline Lab Guideline: Standard physiological levels dictate verifying abnormal anomalies with a primary clinician path."
#         ]
#     }

# """
# Dynamic RAG Context Retrieval Service
# Extracts out-of-range clinical metrics and queries ChromaDB 
# utilizing identical text embedding model mapping dimensions.
# """

# import os
# import logging
# import chromadb
# from typing import Dict, List
# from sentence_transformers import SentenceTransformer

# logger = logging.getLogger(__name__)

# # =========================================================
# # CONFIGURATION & DETERMINISTIC PATHS
# # =========================================================

# # Moves up one level from RAG/ to the backend root directory to locate the chroma storage folder
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

# # 1. Thread-safe initialization of your embedding model
# try:
#     embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
#     embedding_model.max_seq_length = 512
#     logger.info("✅ RAG SentenceTransformer model initialized successfully.")
# except Exception as e:
#     logger.error(f"❌ Failed to load RAG sentence embedding model: {e}")
#     embedding_model = None


# # =========================================================
# # CORE RETRIEVER METHOD
# # =========================================================

# def generate_summary(structured_data: Dict) -> Dict:
#     """
#     Scans structured test lists for out-of-range thresholds, 
#     queries the local ChromaDB instance, and returns relevant clinical snippets.
#     """
#     tests = structured_data.get("tests", [])
    
#     if not tests:
#         return {"rag_context": ["No structured metrics available to query vector storage."]}

#     # 1. Parse anomalies to avoid indexing clean baseline metrics
#     anomalous_findings = []
#     for test in tests:
#         test_name = test.get("test_name", "Unknown Test")
#         status = str(test.get("status", "")).strip().lower()
#         value = test.get("value", "N/A")
#         unit = test.get("unit", "")

#         if status in ["high", "low", "abnormal"]:
#             anomalous_findings.append(f"{test_name} is {status.upper()} (Value: {value} {unit})")

#     # 2. Construct targeted structural string query
#     if not anomalous_findings:
#         search_query = "Standard healthy baseline laboratory diagnostics interpretation parameters."
#     else:
#         # e.g., "Clinical significance of anomalies: WBC Count is HIGH, Triglyceride is HIGH"
#         search_query = f"Clinical significance and patient advice for abnormal indicators: {', '.join(anomalous_findings)}"

#     logger.info(f"🎯 Constructed RAG Query Vector String: '{search_query}'")

#     # 3. Handle embedding model safety check
#     if embedding_model is None:
#         logger.error("RAG tracking skipped: Embedding model not instantiated.")
#         return {"rag_context": ["Reference guideline retrieval offline due to model initialization failure."]}

#     try:
#         # 4. Connect to persistent storage cluster client instance
#         client = chromadb.PersistentClient(path=CHROMA_PATH)
        
#         # Pull your collection matching your upload script name exactly
#         collection = client.get_collection(name="medical_knowledge")

#         # 5. Convert query text string into normalized vector floats list
#         query_vector = embedding_model.encode(
#             search_query,
#             normalize_embeddings=True
#         ).tolist()

#         # 6. Search vector neighborhood for top 3 matches using cosine metrics
#         results = collection.query(
#             query_embeddings=[query_vector],
#             n_results=3
#         )

#         # 7. Unpack database document fragments arrays safely
#         retrieved_knowledge_chunks = []
#         if results and "documents" in results and results["documents"]:
#             # Chroma outputs structurally wrapped array nested layers: [[doc1, doc2, doc3]]
#             nested_documents = results["documents"][0]
#             retrieved_knowledge_chunks = [str(doc).strip() for doc in nested_documents if doc.strip()]

#         # 8. Fallback baseline if collection is empty or query drops out
    #     if not retrieved_knowledge_chunks:
    #         logger.warning("⚠️ ChromaDB query executed but returned zero context matches.")
    #         retrieved_knowledge_chunks = [
    #             "Standard clinical reference validation protocol applies. Review anomalies with a primary physician."
    #         ]

    #     return {"rag_context": retrieved_knowledge_chunks}

    # except Exception as e:
    #     logger.error(f"❌ Critical system failure during ChromaDB RAG processing step: {e}")
    #     return {"rag_context": ["Internal knowledge base retrieval unavailable due to structural database error."]}

"""
Dynamic RAG Context Gateway Service
Connects the production pipeline directly to the advanced retrieval, 
filtering, and keyword-reranking logic inside retrieve.py.
"""

import logging
from typing import Dict, List
# Import the heavy-lifting functions from your retrieve.py file
from RAG.retrieve import retrieve_context, rank_rag_chunks

logger = logging.getLogger(__name__)

def generate_summary(structured_data: Dict) -> Dict:
    """
    Parses out-of-range clinical anomalies, queries ChromaDB via retrieve.py,
    applies medical keyword boosting/reranking, and returns pristine context.
    """
    tests = structured_data.get("tests", [])
    
    if not tests:
        return {"rag_context": ["No structured metrics available to query vector storage."]}

    # 1. Isolate the abnormal findings to construct a clean search query
    abnormal_tests_list = []
    anomalous_strings = []
    
    for test in tests:
        status = str(test.get("status", "")).strip().lower()
        if status in ["high", "low", "abnormal"]:
            abnormal_tests_list.append(test) # Keep the dictionary for the reranker
            anomalous_strings.append(f"{test.get('test_name')} is {status.upper()}")

    # 2. Build target search string query
    if not anomalous_strings:
        search_query = "Standard healthy baseline laboratory diagnostics interpretation parameters."
    else:
        search_query = f"Clinical significance and patient advice for abnormal indicators: {', '.join(anomalous_strings)}"

    logger.info(f"🎯 Directing Targeted Query to retrieve.py: '{search_query}'")

    try:
        # 3. Step A: Retrieve raw text blocks using retrieve.py's native embedding & noise filters
        # We request 15 chunks initially to give our noise filter and reranker plenty of material
        raw_retrieved_chunks = retrieve_context(query=search_query, category="general", top_k=15)

        # 4. Step B: Apply your custom medical entity heuristic boosts and keyword reranking
        if abnormal_tests_list and raw_retrieved_chunks:
            logger.info(f"⚖️ Applying medical heuristic reranking across {len(raw_retrieved_chunks)} raw chunks...")
            final_ranked_context = rank_rag_chunks(
                chunks=raw_retrieved_chunks, 
                abnormal_tests=abnormal_tests_list, 
                top_k=3 # Return the top 3 absolute best chunks to Groq
            )
        else:
            final_ranked_context = raw_retrieved_chunks[:3]

        # 5. Fallback safeguard if filters wiped out all context
        if not final_ranked_context:
            logger.warning("⚠️ RAG filters returned empty. Applying baseline fallback snippet.")
            final_ranked_context = ["Standard clinical reference validation protocol applies. Review anomalies with a primary physician."]

        return {"rag_context": final_ranked_context}

    except Exception as e:
        logger.error(f"❌ Critical breakdown routing through retrieve.py gateway: {e}")
        return {"rag_context": ["Internal knowledge base retrieval temporarily dropped due to processing error."]}