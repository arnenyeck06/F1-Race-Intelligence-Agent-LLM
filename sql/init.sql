CREATE EXTENSION IF NOT EXISTS vector;

-- Race sessions
CREATE TABLE IF NOT EXISTS sessions (
    session_key     INTEGER PRIMARY KEY,
    meeting_name    TEXT,
    circuit_name    TEXT,
    country         TEXT,
    year            INTEGER,
    session_type    TEXT,
    date_start      TIMESTAMP
);

-- Lap times
CREATE TABLE IF NOT EXISTS laps (
    id              SERIAL PRIMARY KEY,
    session_key     INTEGER REFERENCES sessions(session_key),
    driver_number   INTEGER,
    driver_name     TEXT,
    team_name       TEXT,
    lap_number      INTEGER,
    lap_duration    FLOAT,
    is_pit_out_lap  BOOLEAN,
    compound        TEXT,
    tyre_age_at_start INTEGER
);

-- Pit stops
CREATE TABLE IF NOT EXISTS pit_stops (
    id              SERIAL PRIMARY KEY,
    session_key     INTEGER REFERENCES sessions(session_key),
    driver_number   INTEGER,
    driver_name     TEXT,
    team_name       TEXT,
    lap_number      INTEGER,
    pit_duration    FLOAT,
    compound_in     TEXT,
    compound_out    TEXT
);

-- Driver positions over race
CREATE TABLE IF NOT EXISTS positions (
    id              SERIAL PRIMARY KEY,
    session_key     INTEGER REFERENCES sessions(session_key),
    driver_number   INTEGER,
    driver_name     TEXT,
    team_name       TEXT,
    lap_number      INTEGER,
    position        INTEGER
);

-- RAG chunks (for regulation/report text)
CREATE TABLE IF NOT EXISTS chunks (
    id          TEXT PRIMARY KEY,
    source      TEXT,
    category    TEXT,
    year        INTEGER,
    text        TEXT NOT NULL,
    embedding   vector(384)
);

CREATE INDEX IF NOT EXISTS chunks_embedding_idx
    ON chunks USING hnsw (embedding vector_cosine_ops);

-- Feedback
CREATE TABLE IF NOT EXISTS query_feedback (
    id          SERIAL PRIMARY KEY,
    query       TEXT,
    answer      TEXT,
    feedback    INTEGER,
    created_at  TIMESTAMP DEFAULT NOW()
);
