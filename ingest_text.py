import json
import os
import sys

from ingestion.wiki_client import fetch_all, RACES_2024, REGULATIONS
from ingestion.chunk_builder import build_chunks
from search.vector_store import upsert_chunks

CHUNKS_PATH = "data/text_chunks.json"


def main():
    os.makedirs("data", exist_ok=True)
    print("[ingest_text] Fetching race summaries...")
    race_articles = fetch_all(RACES_2024)
    print("\n[ingest_text] Fetching regulation articles...")
    reg_articles = fetch_all(REGULATIONS)
    print("\n[ingest_text] Building chunks...")
    race_chunks = build_chunks(race_articles, category="race_summary", year=2024)
    reg_chunks = build_chunks(reg_articles, category="regulation", year=2024)
    all_chunks = race_chunks + reg_chunks
    print(f"[ingest_text] {len(all_chunks)} total chunks")
    with open(CHUNKS_PATH, "w") as f:
        json.dump(all_chunks, f, indent=2)
    from ingestion.embedder import Embedder
    embedder = Embedder()
    print(f"[ingest_text] Embedding {len(all_chunks)} chunks...")
    embeddings = embedder.encode_batch([c["text"] for c in all_chunks]).tolist()
    upsert_chunks(all_chunks, embeddings)
    print(f"[ingest_text] Done — {len(all_chunks)} chunks upserted to pgvector.")


if __name__ == "__main__":
    main()
