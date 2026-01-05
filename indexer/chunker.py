import re
from pathlib import Path
from typing import List, Dict


def chunk_csharp(code: str, file_path: str) -> List[Dict]:
    """
    C# dosyasını class / method seviyesinde parçalara ayırır
    """
    chunks = []

    class_pattern = re.compile(
        r"(class\s+\w+[\s\S]*?\{[\s\S]*?\})",
        re.MULTILINE
    )

    method_pattern = re.compile(
        r"(?:public|private|protected)?\s*(?:static\s+)?\w+\s+\w+\s*\([^)]*\)\s*\{[\s\S]*?\}",
        re.MULTILINE
    )

    classes = class_pattern.findall(code)

    for class_block in classes:
        # Class-level chunk
        chunks.append({
            "text": class_block,
            "meta": {
                "file": file_path,
                "type": "class"
            }
        })

        # Method-level chunks
        methods = method_pattern.findall(class_block)
        for method in methods:
            chunks.append({
                "text": method,
                "meta": {
                    "file": file_path,
                    "type": "method"
                }
            })

    return chunks


def chunk_markdown(text: str, file_path: str) -> List[Dict]:
    chunks = []
    current = []

    for line in text.splitlines():
        if line.startswith("#"):
            if current:
                chunks.append({
                    "text": "\n".join(current),
                    "meta": {
                        "file": file_path,
                        "type": "section"
                    }
                })
                current = []
        current.append(line)

    if current:
        chunks.append({
            "text": "\n".join(current),
            "meta": {
                "file": file_path,
                "type": "section"
            }
        })

    return chunks
