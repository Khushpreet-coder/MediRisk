# import os
# import chromadb
# from sentence_transformers import SentenceTransformer

# from chunking import chunk_knowledge_base
# from text_normalizer import normalize_medical_text

# print("🧠 Loading embedding model...")
# model = SentenceTransformer("all-MiniLM-L6-v2")

# client = chromadb.PersistentClient(
#     path="rag/chroma_db"
# )

# # ✅ Fresh collection with metadata support
# collection = client.get_or_create_collection(
#     name="medical_knowledge",
#     metadata={"hnsw:space": "cosine"}
# )

# # =====================================
# # Knowledge Base Directory
# # =====================================
# BASE_DIR = os.path.dirname(__file__)
# KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge_base")

# if not os.path.exists(KNOWLEDGE_DIR):
#     raise FileNotFoundError(f"❌ Knowledge folder not found: {KNOWLEDGE_DIR}")

# # =====================================
# # Read and Embed Knowledge Files with Granular Chunks
# # =====================================
# total_chunks = 0
# chunk_counter = 0

# for filename in sorted(os.listdir(KNOWLEDGE_DIR)):
#     filepath = os.path.join(KNOWLEDGE_DIR, filename)

#     # Skip non-text files
#     if not filename.endswith(".txt"):
#         continue

#     print(f"\n📄 Processing: {filename}")

#     try:
#         with open(filepath, "r", encoding="utf-8", errors="replace") as f:
#             content = f.read()
            
#             # Create granular chunks with metadata
#             chunks = chunk_knowledge_base(content, filename)
#             print(f"   ✓ Created {len(chunks)} granular chunks")
            
#             for chunk in chunks:
#                 chunk_counter += 1
                
#                 # Embed chunk content
#                 try:
#                     embedding = model.encode(chunk["content"]).tolist()
                    
#                     # Create unique ID
#                     chunk_id = f"{filename}_{chunk_counter}"
                    
#                     # Prepare metadata
#                     metadata = {
#                         "filename": filename,
#                         "test_name": chunk.get("test_name", ""),
#                         "category": chunk.get("category", ""),
#                         "content_type": chunk.get("content_type", "")
#                     }
                    
#                     # Store in ChromaDB
#                     collection.add(
#                         documents=[chunk["content"]],
#                         metadatas=[metadata],
#                         ids=[chunk_id],
#                         embeddings=[embedding]
#                     )
                    
#                     total_chunks += 1
                    
#                 except Exception as e:
#                     print(f"   ⚠️ Error embedding chunk {chunk_counter}: {e}")
                    
#     except Exception as e:
#         print(f"⚠️ Error reading {filename}: {e}")

# print(f"\n✅ Embedding Complete!")
# print(f"   Total granular chunks stored: {total_chunks}")
# print(f"   Collection name: medical_knowledge")

# ============================================
# embed_knowledgebase.py
# ============================================

# import os
# import chromadb

# from sentence_transformers import SentenceTransformer

# from chunking import chunk_knowledge_base

# # =====================================
# # Paths
# # =====================================

# BASE_DIR = os.path.dirname(__file__)

# KNOWLEDGE_DIR = os.path.join(
#     BASE_DIR,
#     "knowledge_base"
# )

# CHROMA_PATH = os.path.join(
#     BASE_DIR,
#     "chroma_db"
# )

# # =====================================
# # Load Embedding Model
# # =====================================

# print("Loading embedding model...")

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )

# # =====================================
# # ChromaDB Client
# # =====================================

# client = chromadb.PersistentClient(
#     path=CHROMA_PATH
# )

# collection = client.get_or_create_collection(
#     name="medical_knowledge",
#     metadata={"hnsw:space": "cosine"}
# )

# # =====================================
# # Process Knowledge Files
# # =====================================

# total_chunks = 0

# for filename in os.listdir(KNOWLEDGE_DIR):

#     if not filename.endswith(".txt"):
#         continue

#     filepath = os.path.join(
#         KNOWLEDGE_DIR,
#         filename
#     )

#     print(f"\nProcessing {filename}")

#     try:

#         with open(
#             filepath,
#             "r",
#             encoding="utf-8",
#             errors="replace"
#         ) as f:

#             text = f.read()

#     except Exception as e:

#         print("File read error:", e)
#         continue

#     # =====================================
#     # Chunking
#     # =====================================

#     chunks = chunk_knowledge_base(
#         text,
#         filename
#     )

#     print(f"Chunks created: {len(chunks)}")

#     # =====================================
#     # Store Embeddings
#     # =====================================

#     for idx, chunk in enumerate(chunks):

#         try:

#             content = chunk.get(
#                 "content",
#                 ""
#             ).strip()

#             if not content:
#                 continue

#             embedding = model.encode(
#                 content
#             ).tolist()

#             collection.add(

#                 documents=[content],

#                 embeddings=[embedding],

#                 metadatas=[{
#                     "category": chunk.get(
#                         "category",
#                         "general"
#                     ),

#                     "test_name": chunk.get(
#                         "test_name",
#                         ""
#                     ),

#                     "content_type": chunk.get(
#                         "content_type",
#                         "general"
#                     ),

#                     "source_file": filename
#                 }],

#                 ids=[f"{filename}_{idx}"]
#             )

#             total_chunks += 1

#         except Exception as e:

#             print("Embedding error:", e)

# # =====================================
# # Done
# # =====================================

# print("\nEmbedding completed")
# print("Total chunks:", total_chunks)


# import os
# import chromadb
# import uuid
# from sentence_transformers import SentenceTransformer
# from chunking import chunk_medical_report

# # =========================================================
# # PATHS (FIXED)
# # =========================================================

# BASE_DIR = os.path.dirname(__file__)

# KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge_base")
# CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

# # 👉 IMPORTANT: auto-create folder if missing
# os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
# os.makedirs(CHROMA_PATH, exist_ok=True)


# # =========================================================
# # LOAD MODEL
# # =========================================================

# print("Loading embedding model...")

# model = SentenceTransformer("all-MiniLM-L6-v2")
# model.max_seq_length = 512


# # =========================================================
# # CHROMA CLIENT
# # =========================================================

# client = chromadb.PersistentClient(path=CHROMA_PATH)

# collection = client.get_or_create_collection(
#     name="medical_knowledge",
#     metadata={"hnsw:space": "cosine"}
# )


# # =========================================================
# # PROCESS FILES
# # =========================================================

# total_chunks = 0

# for filename in os.listdir(KNOWLEDGE_DIR):

#     if not filename.endswith(".txt"):
#         continue

#     filepath = os.path.join(KNOWLEDGE_DIR, filename)

#     print(f"\n📄 Processing file: {filename}")

#     try:
#         with open(filepath, "r", encoding="utf-8", errors="replace") as f:
#             text = f.read()

#     except Exception as e:
#         print("❌ File read error:", e)
#         continue


#     # =====================================================
#     # CHUNKING
#     # =====================================================

#     chunks = chunk_medical_report(text, filename)

#     print(f"🔹 Chunks created: {len(chunks)}")


#     # =====================================================
#     # BATCH STORAGE (IMPORTANT OPTIMIZATION)
#     # =====================================================

#     docs = []
#     embs = []
#     metas = []
#     ids = []

#     for idx, chunk in enumerate(chunks):

#         try:
#             content = chunk.get("content", "").strip()

#             if not content:
#                 continue

#             # skip extremely short noise chunks
#             if len(content) < 20:
#                 continue

#             # embedding (NORMALIZED → IMPORTANT)
#             embedding = model.encode(
#                 content,
#                 normalize_embeddings=True
#             ).tolist()

#             docs.append(content)
#             embs.append(embedding)

#             metas.append({
#                 "category": chunk.get("category", "general"),
#                 "test_name": chunk.get("test_name", ""),
#                 "content_type": chunk.get("content_type", "general"),
#                 "source_file": filename
#             })

#             # SAFE UNIQUE ID (prevents overwrite)
#             ids.append(f"{filename}_{idx}_{uuid.uuid4().hex[:8]}")

#         except Exception as e:
#             print("⚠️ Embedding error:", e)


#     # =====================================================
#     # STORE IN CHROMA
#     # =====================================================

#     if docs:

#         collection.add(
#             documents=docs,
#             embeddings=embs,
#             metadatas=metas,
#             ids=ids
#         )

#         total_chunks += len(docs)

#         print(f"✅ Stored {len(docs)} chunks")


# # =========================================================
# # DONE
# # =========================================================

# print("\n🎉 Embedding completed successfully!")
# print("📊 Total chunks stored:", total_chunks)



# import os
# import chromadb
# import uuid
# from sentence_transformers import SentenceTransformer
# from chunking import chunk_medical_report

# # =========================================================
# # PATHS
# # =========================================================

# BASE_DIR = os.path.dirname(__file__)

# KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge_base")
# CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

# # Auto-create folders if missing
# os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
# os.makedirs(CHROMA_PATH, exist_ok=True)

# # =========================================================
# # LOAD MODEL
# # =========================================================

# print("Loading embedding model...")

# model = SentenceTransformer("all-MiniLM-L6-v2")
# model.max_seq_length = 512

# # =========================================================
# # CHROMA CLIENT
# # =========================================================

# client = chromadb.PersistentClient(path=CHROMA_PATH)

# collection = client.get_or_create_collection(
#     name="medical_knowledge",
#     metadata={"hnsw:space": "cosine"}
# )

# # =========================================================
# # CHECK INPUT DATA
# # =========================================================

# files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith(".txt")]

# if not files:
#     print("⚠️ No .txt files found in knowledge_base folder.")
#     print("👉 Add files and run again.")
#     exit()

# # =========================================================
# # PROCESS FILES
# # =========================================================

# total_chunks = 0

# for filename in files:

#     filepath = os.path.join(KNOWLEDGE_DIR, filename)

#     print(f"\n📄 Processing file: {filename}")

#     try:
#         with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
#             text = f.read()

#     except Exception as e:
#         print("❌ File read error:", e)
#         continue

#     # =====================================================
#     # CHUNKING
#     # =====================================================

#     chunks = chunk_medical_report(text, filename)

#     print(f"🔹 Chunks created: {len(chunks)}")

#     # =====================================================
#     # STORAGE PREP
#     # =====================================================

#     docs = []
#     embs = []
#     metas = []
#     ids = []

#     for idx, chunk in enumerate(chunks):

#         content = chunk.get("content", "").strip()

#         if len(content) < 20:
#             continue

#         try:
#             embedding = model.encode(
#                 content,
#                 normalize_embeddings=True
#             ).tolist()

#             docs.append(content)
#             embs.append(embedding)

#             metas.append({
#                 "category": chunk.get("category", "general"),
#                 "test_name": chunk.get("test_name", ""),
#                 "content_type": chunk.get("content_type", "general"),
#                 "source_file": filename
#             })

#             ids.append(f"{filename}_{idx}_{uuid.uuid4().hex[:8]}")

#         except Exception as e:
#             print("⚠️ Embedding error:", e)

#     # =====================================================
#     # STORE IN CHROMA
#     # =====================================================

#     if docs:
#         collection.add(
#             documents=docs,
#             embeddings=embs,
#             metadatas=metas,
#             ids=ids
#         )

#         total_chunks += len(docs)

#         print(f"✅ Stored {len(docs)} chunks")

# # =========================================================
# # DONE
# # =========================================================

# print("\n🎉 Embedding completed successfully!")
# print(f"📊 Total chunks stored: {total_chunks}")

import os
import chromadb
import uuid
from sentence_transformers import SentenceTransformer
from chunking import chunk_medical_report

# =========================================================
# PATHS (SAFE + ROBUST)
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_DIR = os.path.join(BASE_DIR, "KB")
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

print("\n📂 BASE_DIR:", BASE_DIR)
print("📂 KNOWLEDGE_DIR:", KNOWLEDGE_DIR)
print("📂 CHROMA_PATH:", CHROMA_PATH)

# Auto-create folders if missing
# os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(CHROMA_PATH, exist_ok=True)

# =========================================================
# CHECK FILES
# =========================================================

all_files = os.listdir(KNOWLEDGE_DIR) if os.path.exists(KNOWLEDGE_DIR) else []

print("\n📄 All files found:", all_files)

files = [
    f for f in all_files
    if f.lower().endswith(".txt")
]

print("📄 .txt files filtered:", files)

if not files:
    print("\n⚠️ No .txt files found in knowledge_base folder.")
    print("👉 Add .txt files here:", KNOWLEDGE_DIR)
    exit()

# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("\n🔄 Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")
model.max_seq_length = 512

print("✅ Model loaded successfully")

# =========================================================
# CHROMA DB INIT
# =========================================================

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="medical_knowledge",
    metadata={"hnsw:space": "cosine"}
)

print("✅ Chroma DB initialized")

# =========================================================
# PROCESS FILES
# =========================================================

total_chunks = 0

for filename in files:

    filepath = os.path.join(KNOWLEDGE_DIR, filename)

    print(f"\n📄 Processing file: {filename}")

    # -------------------------
    # READ FILE
    # -------------------------
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        if not text.strip():
            print("⚠️ Empty file skipped:", filename)
            continue

    except Exception as e:
        print("❌ File read error:", e)
        continue

    # -------------------------
    # CHUNKING
    # -------------------------
    chunks = chunk_medical_report(text, filename)

    print(f"🔹 Chunks created: {len(chunks)}")

    docs, embs, metas, ids = [], [], [], []

    # -------------------------
    # EMBEDDING
    # -------------------------
    for idx, chunk in enumerate(chunks):

        content = chunk.get("content", "").strip()

        if len(content) < 20:
            continue

        try:
            embedding = model.encode(
                content,
                normalize_embeddings=True
            ).tolist()

            docs.append(content)
            embs.append(embedding)

            metas.append({
                "category": chunk.get("category", "general"),
                "test_name": chunk.get("test_name", ""),
                "content_type": chunk.get("content_type", "general"),
                "source_file": filename
            })

            ids.append(f"{filename}_{idx}_{uuid.uuid4().hex[:8]}")

        except Exception as e:
            print("⚠️ Embedding error:", e)

    # -------------------------
    # STORE IN CHROMA
    # -------------------------
    if docs:
        collection.add(
            documents=docs,
            embeddings=embs,
            metadatas=metas,
            ids=ids
        )

        total_chunks += len(docs)
        print(f"✅ Stored {len(docs)} chunks")

    else:
        print("⚠️ No valid chunks to store for:", filename)

# =========================================================
# DONE
# =========================================================

print("\n🎉 Embedding pipeline completed successfully!")
print(f"📊 Total chunks stored: {total_chunks}")