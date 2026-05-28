import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("medical_reports")

results = collection.get(include=["documents", "metadatas"])

print("\n================ CHROMA STORED CHUNK ================\n")

for i, (doc, meta) in enumerate(zip(results["documents"], results["metadatas"])):
    print(f"CHUNK {i}")
    print("-" * 50)
    print("TEXT:")
    print(doc[:1000])  # limit for readability
    print("\nMETADATA:")
    print(meta)
    print("\n" + "=" * 60 + "\n")