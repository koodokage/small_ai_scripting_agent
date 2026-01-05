# Small AI Scripting Agent

Local-first, open-source AI scripting agent with RAG-based code indexing.
Designed for game development workflows (Unity, Unreal, custom engines).

---

## Prerequisites

### Operating System
- Windows 10 / 11 (64-bit)

---

## Python

This project **requires Python 3.10.x**.

Tested and verified with:

> ⚠️ Python 3.12+ / 3.13+ are **not supported** due to incompatibilities with
> chromadb, onnxruntime, and NumPy 2.x.


During installation:
- Enable **Add Python to PATH**
- Recommended: **Install for all users**

## Ollama
https://ollama.com
ollama pull deepseek-coder:6.7b

pip install pydantic==1.10.13
pip install numpy==1.26.4
pip install chromadb==0.4.24
pip install tqdm