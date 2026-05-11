# import os
# import chromadb

# from sentence_transformers import SentenceTransformer
# from RAG.text_normalizer import normalize_medical_text

# # =====================================
# # Load Embedding Model
# # =====================================

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )


# # =====================================
# # Create ChromaDB Client
# # =====================================

# client = chromadb.PersistentClient(
#     path="./RAG/chroma_db"
# )


# # =====================================
# # Create Collection
# # =====================================

# collection = client.get_or_create_collection(
#     name="medical_knowledge"
# )


# # =====================================
# # Clear Old Embeddings
# # =====================================

# try:

#     existing = collection.get()["ids"]

#     if existing:
#         collection.delete(ids=existing)

# except Exception as e:

#     print("⚠️ Could not clear old embeddings:", e)


# # =====================================
# # Knowledge Folder
# # =====================================

# BASE_DIR = os.path.dirname(__file__)

# KNOWLEDGE_DIR = os.path.join(
#     BASE_DIR,
#     "knowledge_base"
# )


# # =====================================
# # Check Folder Exists
# # =====================================

# if not os.path.exists(KNOWLEDGE_DIR):

#     raise FileNotFoundError(
#         f"❌ Knowledge folder not found: {KNOWLEDGE_DIR}"
#     )


# # =====================================
# # Read Knowledge Files
# # =====================================

# documents = []

# for filename in os.listdir(KNOWLEDGE_DIR):

#     filepath = os.path.join(
#         KNOWLEDGE_DIR,
#         filename
#     )

#     # skip non-text files
#     if not filename.endswith(".txt"):
#         continue

#     print(f"📄 Reading: {filename}")

#     try:

#         with open(
#             filepath,
#             "r",
#             encoding="utf-8",
#             errors="replace"
#         ) as f:

#             text = f.read()

#             # split into small chunks
#             chunks = text.split("\n\n")

#             for chunk in chunks:

#                 chunk = chunk.strip()

#                 if chunk:
#                     documents.append(chunk)

#     except Exception as e:

#         print(f"❌ Failed reading {filename}: {e}")


# # =====================================
# # Check Documents
# # =====================================

# if not documents:

#     raise ValueError(
#         "❌ No documents found in knowledge base"
#     )


# print(f"\n📚 Total Chunks: {len(documents)}")


# # =====================================
# # Generate Embeddings
# # =====================================

# print("\n🧠 Generating embeddings...")

# embeddings = model.encode(
#     documents
# ).tolist()


# # =====================================
# # Store In ChromaDB
# # =====================================

# print("\n💾 Storing embeddings in ChromaDB...")

# for i, doc in enumerate(documents):

#     collection.add(
#         ids=[str(i)],
#         documents=[doc],
#         embeddings=[embeddings[i]]
#     )


# # =====================================
# # Final Success
# # =====================================

# print("\n✅ Knowledge Base Embedded Successfully")

# print(
#     "📦 Total Stored Documents:",
#     collection.count()
# )

# import os
# import chromadb

# from sentence_transformers import SentenceTransformer

# from text_normalizer import normalize_medical_text


# # =====================================
# # Load Embedding Model
# # =====================================

# print("🧠 Loading embedding model...")

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )


# # =====================================
# # Create ChromaDB Client
# # =====================================

# client = chromadb.PersistentClient(
#     path="./RAG/chroma_db"
# )


# # =====================================
# # Create Collection
# # =====================================

# collection = client.get_or_create_collection(
#     name="medical_knowledge"
# )


# # =====================================
# # Clear Old Embeddings
# # =====================================

# try:

#     existing = collection.get()["ids"]

#     if existing:

#         collection.delete(ids=existing)

#         print(f"🗑 Deleted {len(existing)} old embeddings")

# except Exception as e:

#     print("⚠️ Could not clear old embeddings:", e)


# # =====================================
# # Knowledge Folder
# # =====================================

# BASE_DIR = os.path.dirname(__file__)

# KNOWLEDGE_DIR = os.path.join(
#     BASE_DIR,
#     "knowledge_base"
# )


# # =====================================
# # Check Folder Exists
# # =====================================

# if not os.path.exists(KNOWLEDGE_DIR):

#     raise FileNotFoundError(
#         f"❌ Knowledge folder not found: {KNOWLEDGE_DIR}"
#     )


# # =====================================
# # Read Knowledge Files
# # =====================================

# documents = []
# metadatas = []
# ids = []

# doc_id = 0

# for filename in os.listdir(KNOWLEDGE_DIR):

#     filepath = os.path.join(
#         KNOWLEDGE_DIR,
#         filename
#     )

#     # Skip non-text files
#     if not filename.endswith(".txt"):
#         continue

#     print(f"\n📄 Reading: {filename}")

#     try:

#         with open(
#             filepath,
#             "r",
#             encoding="utf-8",
#             errors="replace"
#         ) as f:

#             text = f.read()

#             # =====================================
#             # Split into chunks
#             # =====================================

#             chunks = text.split("\n\n")

#             for chunk in chunks:

#                 chunk = chunk.strip()

#                 if not chunk:
#                     continue

#                 # =====================================
#                 # Normalize text for embeddings
#                 # =====================================

#                 normalized_chunk = normalize_medical_text(
#                     chunk
#                 )

#                 documents.append(normalized_chunk)

#                 metadatas.append({
#                     "source_file": filename,
#                     "original_text": chunk
#                 })

#                 ids.append(str(doc_id))

#                 doc_id += 1

#     except Exception as e:

#         print(f"❌ Failed reading {filename}: {e}")


# # =====================================
# # Check Documents
# # =====================================

# if not documents:

#     raise ValueError(
#         "❌ No documents found in knowledge base"
#     )


# print(f"\n📚 Total Chunks: {len(documents)}")


# # =====================================
# # Generate Embeddings
# # =====================================

# print("\n🧠 Generating embeddings...")

# embeddings = model.encode(
#     documents,
#     show_progress_bar=True
# ).tolist()


# # =====================================
# # Store In ChromaDB
# # =====================================

# print("\n💾 Storing embeddings in ChromaDB...")


# collection.add(
#     ids=ids,
#     documents=documents,
#     embeddings=embeddings,
#     metadatas=metadatas
# )


# # =====================================
# # Final Success
# # =====================================

# print("\n✅ Knowledge Base Embedded Successfully")

# print(
#     "📦 Total Stored Documents:",
#     collection.count()
# )

# import os
# import chromadb

# from sentence_transformers import SentenceTransformer

# from text_normalizer import normalize_medical_text


# # =====================================
# # Load Embedding Model
# # =====================================

# print("🧠 Loading embedding model...")

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )


# # =====================================
# # Create ChromaDB Client
# # =====================================

# client = chromadb.PersistentClient(
#     path="./RAG/chroma_db"
# )


# # =====================================
# # Create Collection
# # =====================================

# collection = client.get_or_create_collection(
#     name="medical_knowledge"
# )


# # =====================================
# # Clear Old Embeddings
# # =====================================

# try:

#     existing = collection.get()["ids"]

#     if existing:

#         collection.delete(ids=existing)

#         print(f"🗑 Deleted {len(existing)} old embeddings")

# except Exception as e:

#     print("⚠️ Could not clear old embeddings:", e)


# # =====================================
# # Knowledge Folder
# # =====================================

# BASE_DIR = os.path.dirname(__file__)

# KNOWLEDGE_DIR = os.path.join(
#     BASE_DIR,
#     "knowledge_base"
# )


# # =====================================
# # Check Folder Exists
# # =====================================

# if not os.path.exists(KNOWLEDGE_DIR):

#     raise FileNotFoundError(
#         f"❌ Knowledge folder not found: {KNOWLEDGE_DIR}"
#     )


# # =====================================
# # Chunking Function
# # =====================================

# def chunk_text(text, max_len=800):

#     paragraphs = text.split("\n")

#     chunks = []
#     current = ""

#     for p in paragraphs:

#         if len(current) + len(p) < max_len:
#             current += " " + p
#         else:
#             chunks.append(current.strip())
#             current = p

#     if current:
#         chunks.append(current.strip())

#     return chunks


# # =====================================
# # Read Knowledge Files
# # =====================================

# documents = []
# metadatas = []
# ids = []

# doc_id = 0

# for filename in os.listdir(KNOWLEDGE_DIR):

#     filepath = os.path.join(
#         KNOWLEDGE_DIR,
#         filename
#     )

#     # Skip non-text files
#     if not filename.endswith(".txt"):
#         continue

#     print(f"\n📄 Reading: {filename}")

#     try:

#         with open(
#             filepath,
#             "r",
#             encoding="utf-8",
#             errors="replace"
#         ) as f:

#             text = f.read()

#             # =====================================
#             # Split into chunks
#             # =====================================

#             chunks = chunk_text(text)

#             for chunk in chunks:

#                 chunk = chunk.strip()

#                 if not chunk:
#                     continue

#                 # =====================================
#                 # Normalize text for embeddings
#                 # =====================================

#                 normalized_chunk = normalize_medical_text(
#                     chunk
#                 )

#                 documents.append(normalized_chunk)

#                 metadatas.append({
#                     "source_file": filename,
#                     "original_text": chunk
#                 })

#                 ids.append(str(doc_id))

#                 doc_id += 1

#     except Exception as e:

#         print(f"❌ Failed reading {filename}: {e}")


# # =====================================
# # Check Documents
# # =====================================

# if not documents:

#     raise ValueError(
#         "❌ No documents found in knowledge base"
#     )


# print(f"\n📚 Total Chunks: {len(documents)}")


# # =====================================
# # Generate Embeddings
# # =====================================

# print("\n🧠 Generating embeddings...")

# embeddings = model.encode(
#     documents,
#     show_progress_bar=True
# ).tolist()


# # =====================================
# # Store In ChromaDB
# # =====================================

# print("\n💾 Storing embeddings in ChromaDB...")


# collection.add(
#     ids=ids,
#     documents=documents,
#     embeddings=embeddings,
#     metadatas=metadatas
# )


# # =====================================
# # Final Success
# # =====================================

# print("\n✅ Knowledge Base Embedded Successfully")

# print(
#     "📦 Total Stored Documents:",
#     collection.count()
# )


# import os
# import re
# import chromadb

# from sentence_transformers import SentenceTransformer

# from text_normalizer import normalize_medical_text


# # =====================================
# # Load Embedding Model
# # =====================================

# print("🧠 Loading embedding model...")

# model = SentenceTransformer(
#     "all-MiniLM-L6-v2"
# )


# # =====================================
# # Create ChromaDB Client
# # =====================================

# client = chromadb.PersistentClient(
#     path="./RAG/chroma_db"
# )


# # =====================================
# # Create Collection
# # =====================================

# collection = client.get_or_create_collection(
#     name="medical_knowledge"
# )


# # =====================================
# # Clear Old Embeddings
# # =====================================

# try:

#     existing = collection.get()["ids"]

#     if existing:

#         collection.delete(ids=existing)

#         print(f"🗑 Deleted {len(existing)} old embeddings")

# except Exception as e:

#     print("⚠️ Could not clear old embeddings:", e)


# # =====================================
# # Knowledge Folder
# # =====================================

# BASE_DIR = os.path.dirname(__file__)

# KNOWLEDGE_DIR = os.path.join(
#     BASE_DIR,
#     "knowledge_base"
# )


# # =====================================
# # Check Folder Exists
# # =====================================

# if not os.path.exists(KNOWLEDGE_DIR):

#     raise FileNotFoundError(
#         f"❌ Knowledge folder not found: {KNOWLEDGE_DIR}"
#     )


# # =====================================
# # Semantic Chunking Function
# # =====================================

# def chunk_text(text):

#     # Normalize line breaks
#     text = text.replace("\r", "\n")

#     # Split using section headings
#     pattern = r'\n(?=[A-Z][A-Za-z0-9\s\(\)/%-]+:)'

#     sections = re.split(pattern, text)

#     chunks = []

#     for sec in sections:

#         sec = sec.strip()

#         # Skip noisy chunks
#         if len(sec) < 50:
#             continue

#         # Large sections → split further
#         if len(sec) > 1200:

#             paragraphs = sec.split("\n\n")

#             current = ""

#             for para in paragraphs:

#                 para = para.strip()

#                 if not para:
#                     continue

#                 if len(current) + len(para) < 800:

#                     current += "\n" + para

#                 else:

#                     chunks.append(current.strip())

#                     current = para

#             if current:
#                 chunks.append(current.strip())

#         else:

#             chunks.append(sec)

#     return chunks


# # =====================================
# # Read Knowledge Files
# # =====================================

# documents = []

# metadatas = []

# ids = []

# doc_id = 0


# for filename in os.listdir(KNOWLEDGE_DIR):

#     filepath = os.path.join(
#         KNOWLEDGE_DIR,
#         filename
#     )

#     # Skip non-text files
#     if not filename.endswith(".txt"):
#         continue

#     print(f"\n📄 Reading: {filename}")

#     try:

#         with open(
#             filepath,
#             "r",
#             encoding="utf-8",
#             errors="replace"
#         ) as f:

#             text = f.read()

#             # =====================================
#             # Create semantic chunks
#             # =====================================

#             chunks = chunk_text(text)

#             print(f"🔹 Chunks Created: {len(chunks)}")

#             for chunk in chunks:

#                 chunk = chunk.strip()

#                 if not chunk:
#                     continue

#                 # =====================================
#                 # Normalize medical text
#                 # =====================================

#                 normalized_chunk = normalize_medical_text(
#                     chunk
#                 )

#                 documents.append(
#                     normalized_chunk
#                 )

#                 metadatas.append({

#                     "source_file": filename,

#                     "original_text": chunk

#                 })

#                 ids.append(
#                     str(doc_id)
#                 )

#                 doc_id += 1

#     except Exception as e:

#         print(
#             f"❌ Failed reading {filename}: {e}"
#         )


# # =====================================
# # Check Documents
# # =====================================

# if not documents:

#     raise ValueError(
#         "❌ No documents found in knowledge base"
#     )


# print(f"\n📚 Total Chunks: {len(documents)}")


# # =====================================
# # Generate Embeddings
# # =====================================

# print("\n🧠 Generating embeddings...")

# embeddings = model.encode(

#     documents,

#     show_progress_bar=True

# ).tolist()


# # =====================================
# # Store In ChromaDB
# # =====================================

# print("\n💾 Storing embeddings in ChromaDB...")


# collection.add(

#     ids=ids,

#     documents=documents,

#     embeddings=embeddings,

#     metadatas=metadatas

# )


# # =====================================
# # Final Success
# # =====================================

# print("\n✅ Knowledge Base Embedded Successfully")

# print(
#     "📦 Total Stored Documents:",
#     collection.count()
# )


import os
import chromadb

from sentence_transformers import SentenceTransformer

from chunking import semantic_chunk
from text_normalizer import normalize_medical_text


# =====================================
# Load Model
# =====================================

print("🧠 Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =====================================
# ChromaDB Client
# =====================================

client = chromadb.PersistentClient(
    path="rag/chroma_db"
)


# =====================================
# Collection
# =====================================

collection = client.get_or_create_collection(
    name="medical_kb"
)


# =====================================
# Clear Old Data
# =====================================

try:

    existing = collection.get()["ids"]

    if existing:

        collection.delete(ids=existing)

        print(f"🗑 Deleted {len(existing)} old embeddings")

except Exception as e:

    print("⚠️ Cleanup issue:", e)


# =====================================
# Knowledge Base Path
# =====================================

KB_PATH = "rag/knowledge_base"


# =====================================
# Store Data
# =====================================

documents = []
embeddings = []
metadatas = []
ids = []

doc_id = 0


# =====================================
# Read Files
# =====================================

for file in os.listdir(KB_PATH):

    filepath = os.path.join(
        KB_PATH,
        file
    )

    # Skip non-txt files
    if not file.endswith(".txt"):
        continue

    print(f"\n📄 Reading: {file}")

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as f:

            text = f.read()

        # =====================================
        # Semantic Chunking
        # =====================================

        chunks = semantic_chunk(text)

        print(f"🔹 Chunks Created: {len(chunks)}")

        for chunk in chunks:

            chunk = chunk.strip()

            if not chunk:
                continue

            # =====================================
            # Normalize Text
            # =====================================

            normalized_chunk = normalize_medical_text(
                chunk
            )

            documents.append(
                normalized_chunk
            )

            metadatas.append({

                "source_file": file,

                "original_text": chunk

            })

            ids.append(
                str(doc_id)
            )

            doc_id += 1

    except Exception as e:

        print(f"❌ Failed reading {file}: {e}")


# =====================================
# Check Empty
# =====================================

if not documents:

    raise ValueError(
        "❌ No documents found"
    )


print(f"\n📚 Total Chunks: {len(documents)}")


# =====================================
# Generate Embeddings
# =====================================

print("\n🧠 Generating embeddings...")

embeddings = model.encode(

    documents,

    show_progress_bar=True

).tolist()


# =====================================
# Store In ChromaDB
# =====================================

print("\n💾 Storing embeddings...")


collection.add(

    ids=ids,

    documents=documents,

    embeddings=embeddings,

    metadatas=metadatas

)


# =====================================
# Done
# =====================================

print("\n✅ Embedding completed")

print(
    "📦 Total Stored Documents:",
    collection.count()
)