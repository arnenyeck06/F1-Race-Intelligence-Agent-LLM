"""
reranker.py
Re-rank retrieved chunks by relevance to the query.
Uses cosine similarity between query embedding and chunk embeddings
as a lightweight cross-encoder approximation.
No extra model needed — reuses the ONNX embedder.
"""

import numpy as np


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


def rerank(query: str, chunks: list[dict], embedder, top_n: int = 5) -> list[dict]:
    """
    Re-rank chunks by cosine similarity between query and chunk embeddings.
    Returns top_n chunks sorted by relevance score descending.
    """
    if not chunks:
        return chunks

    query_vec = embedder.encode(query)
    scored = []

    for chunk in chunks:
        chunk_vec = embedder.encode(chunk["text"][:500])
        score = cosine_similarity(query_vec, chunk_vec)
        scored.append({**chunk, "_rerank_score": round(score, 4)})

    scored.sort(key=lambda x: x["_rerank_score"], reverse=True)
    return scored[:top_n]
