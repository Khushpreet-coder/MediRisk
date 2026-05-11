# import chromadb

# from sentence_transformers import SentenceTransformer


# # =====================================
# # Load Model
# # =====================================

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )


# # =====================================
# # Connect ChromaDB
# # =====================================

# client = chromadb.PersistentClient(
#     path="./rag/chroma_db"
# )

# collection = client.get_collection(
#     "medical_knowledge"
# )


# # =====================================
# # Retrieve Context
# # =====================================

# def retrieve_context(query, top_k=2):

#     query_embedding = model.encode(
#         query
#     ).tolist()

#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=top_k
#     )

#     return results["documents"][0]


# def is_context_weak(context):

#     if not context:
#         return True

#     if len(context) < 2:
#         return True

#     return False

import chromadb
from sentence_transformers import SentenceTransformer

# =====================================
# Load Embedding Model
# =====================================
model = SentenceTransformer("all-MiniLM-L6-v2")


# =====================================
# Connect ChromaDB
# =====================================
client = chromadb.PersistentClient(
    path="./rag/chroma_db"
)

collection = client.get_collection(
    name="medical_knowledge"
)


# =====================================
# CLEAN FUNCTION (IMPORTANT)
# =====================================
def clean_context(results):

    cleaned = []

    for doc in results:

        if not doc:
            continue

        text = doc.strip()

        # remove very small noisy chunks
        if len(text) < 40:
            continue

        # remove page artifacts
        if "Page" in text:
            continue

        # remove repeated garbage separators
        if "----" in text:
            continue

        cleaned.append(text)

    return cleaned


# =====================================
# RETRIEVAL FUNCTION (FIXED)
# =====================================
def retrieve_context(query, top_k=3):

    # 1. Convert query → embedding
    query_embedding = model.encode(query).tolist()

    # 2. Search in vector DB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # 3. Raw documents from Chroma
    raw_docs = results.get("documents", [[]])[0]

    # 4. Clean noisy OCR chunks
    cleaned_docs = clean_context(raw_docs)

    return cleaned_docs


# =====================================
# CONTEXT QUALITY CHECK
# =====================================
def is_context_weak(context):

    if not context:
        return True

    if len(context) < 2:
        return True

    # check if meaningful content exists
    total_length = sum(len(c) for c in context)

    if total_length < 100:
        return True

    return False