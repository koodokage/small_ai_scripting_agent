from pathlib import Path
import chromadb
from rag.embedder import embed_text

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma"

# ✅ AYNI PersistentClient
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="project_index"
)

print("CHROMA DIR:", CHROMA_DIR)
print("COLLECTION COUNT:", collection.count())


def retrieve(query: str, tags=None, k=5):
    query_embedding = embed_text(query)

    where = {"tag": tags[0]} if tags else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where=where
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    return [
        {
            "content": d,
            "file": m.get("file"),
            "tag": m.get("tag"),
            "chunk_index": m.get("chunk_index"),
            "distance": dist
        }
        for d, m, dist in zip(docs, metas, dists)
    ]
