from pathlib import Path
import chromadb
import ollama
from tqdm import tqdm
from indexer.chunker import chunk_csharp, chunk_markdown

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma"

# ✅ DOĞRU CLIENT
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="project_index"
)


def embed_text(text: str):
    result = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return result["embedding"]


def index_file(file: Path, tag: str):
    content = file.read_text(encoding="utf-8", errors="ignore")

    if file.suffix == ".cs":
        chunks = chunk_csharp(content, str(file))
    elif file.suffix == ".md":
        chunks = chunk_markdown(content, str(file))
    else:
        return

    print(f"{file} -> {len(chunks)} chunks")

    if not chunks:
        print(f"[WARN] No chunks produced for {file}")
        return

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk["text"])

        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{
                **chunk["meta"],
                "tag": tag,
                "chunk_index": i,
                "extension": file.suffix
            }],
            ids=[f"{file}:{i}"]
        )


def index_folder(root_path: str, tag: str):
    root = Path(root_path)
    for file in tqdm(root.rglob("*"), desc=f"Indexing {tag}"):
        if file.is_file() and file.suffix in [".cs", ".md"]:
            index_file(file, tag)


if __name__ == "__main__":
    index_folder("data/docs", "docs")
    index_folder("data/code/unity", "unity")
    index_folder("data/code/unreal", "unreal")
    index_folder("data/code/custom", "custom")

    print("Indexing finished successfully.")
