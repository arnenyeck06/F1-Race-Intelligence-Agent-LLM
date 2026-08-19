import uuid
import re

CHUNK_WORDS = 300
OVERLAP_WORDS = 50


def clean_text(text):
    text = re.sub(r"==+[^=]+=+", " ", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text, chunk_words=CHUNK_WORDS, overlap=OVERLAP_WORDS):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += chunk_words - overlap
    return chunks


def build_chunks(articles, category="race_summary", year=2024):
    chunks = []
    for article in articles:
        text = clean_text(article["text"])
        if len(text.split()) < 50:
            continue
        for idx, chunk_text_val in enumerate(chunk_text(text)):
            chunks.append({
                "id": str(uuid.uuid4()),
                "source": article["title"],
                "category": category,
                "year": year,
                "text": chunk_text_val,
            })
    return chunks
