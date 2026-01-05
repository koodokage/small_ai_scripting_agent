import ollama

EMBED_MODEL = "nomic-embed-text"

def embed_text(text: str) -> list[float]:
    result = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )
    return result["embedding"]