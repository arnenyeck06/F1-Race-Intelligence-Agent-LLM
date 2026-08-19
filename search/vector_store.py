import os
import psycopg2
import psycopg2.extras


def get_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5433"),
        dbname=os.getenv("POSTGRES_DB", "f1_rag"),
        user=os.getenv("POSTGRES_USER", "f1"),
        password=os.getenv("POSTGRES_PASSWORD", "f1pass"),
    )


def upsert_chunks(chunks, embeddings):
    conn = get_conn()
    cur = conn.cursor()
    for chunk, embedding in zip(chunks, embeddings):
        cur.execute("""
            INSERT INTO chunks (id, source, category, year, text, embedding)
            VALUES (%s, %s, %s, %s, %s, %s::vector)
            ON CONFLICT (id) DO UPDATE SET text = EXCLUDED.text, embedding = EXCLUDED.embedding
        """, (chunk["id"], chunk["source"], chunk["category"], chunk["year"], chunk["text"], str(embedding)))
    conn.commit()
    cur.close()
    conn.close()


def vector_search(query_embedding, category=None, num_results=10):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    where = "WHERE category = %s" if category else ""
    params = [str(query_embedding)]
    if category:
        params.append(category)
    params.extend([str(query_embedding), num_results])
    cur.execute(f"""
        SELECT id, source, category, year, text,
               1 - (embedding <=> %s::vector) AS _score
        FROM chunks {where}
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, params)
    results = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results
