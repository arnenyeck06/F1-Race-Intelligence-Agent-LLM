# F1 Race Intelligence Agent

## Problem

F1 fans and analysts want instant answers during and after races — lap times, 
tire strategies, pit stop analysis, driver standings — but data is scattered 
across timing screens, race reports, and technical documents.

This agent answers natural-language questions grounded in real F1 race data 
and Wikipedia race summaries. It combines structured SQL data (lap times, 
pit stops, positions) with semantic search over race reports and regulations.

**Example questions:**
- "Who won the Monaco Grand Prix 2024?"
- "What were Hamilton's fastest laps at Silverstone?"
- "How many pit stops did Ferrari make in Bahrain?"
- "What is DRS and when can drivers use it?"
- "Compare Red Bull and McLaren pit stop times at Monaco"

## Architecture
OpenF1 API → Postgres (laps, pits, positions)
Wikipedia → pgvector (race summaries, regulations)
↓
Hybrid RRF Search (BM25 + cosine)
↓
Claude Agent (tool-calling loop)
↓
FastAPI + Streamlit UI


## Stack

- **Race data**: OpenF1 API (free, no auth)
- **Text data**: Wikipedia API (race summaries + regulations)
- **Storage**: Postgres + pgvector (384-dim HNSW index)
- **Keyword search**: minsearch (TF-IDF)
- **Vector search**: ONNX embedder (Xenova/all-MiniLM-L6-v2)
- **Hybrid search**: Reciprocal Rank Fusion (RRF)
- **LLM**: Claude Sonnet (Anthropic API)
- **Interface**: FastAPI + Streamlit

## Setup

### Prerequisites
- Docker + Docker Compose
- Python 3.12+
- Anthropic API key

### Run

```bash
# 1. Clone
git clone https://github.com/arnenyeck06/f1-intelligence
cd f1-intelligence

# 2. Set environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Start Postgres + pgvector
docker compose up -d

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download ONNX model
python ingestion/download_model.py

# 6. Ingest F1 race data (2024 season)
python ingest.py --year 2024

# 7. Fix meeting names
python ingestion/fix_meeting_names.py --year 2024

# 8. Ingest Wikipedia text chunks
python ingest_text.py

# 9. Start Streamlit UI
streamlit run app.py
```

### Query via CLI

```bash
export $(cat .env | xargs)
python query.py "who won the Monaco Grand Prix 2024?"
python query.py "what were the fastest laps at Silverstone 2024?"
```

## Knowledge Base

**Structured data (Postgres):**
- 30 race sessions (2024 season)
- Lap times, pit stops, driver positions

**Text chunks (pgvector):**
- 214 chunks across 21 Wikipedia articles
- Race summaries + F1 regulations

## Data Sources

- [OpenF1 API](https://openf1.org) — free, no auth required
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) — free, no auth required
- All data is publicly available and reproducible
