import chromadb
from chunking import chunk_medical_report

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="medical_reports")


def ingest_file(text: str, filename: str):

    chunks = chunk_medical_report(text, filename)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        doc_id = f"{filename}_{i}"

        ids.append(doc_id)
        documents.append(chunk["content"])
        metadatas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"✅ Ingested {len(chunks)} chunks from {filename}")