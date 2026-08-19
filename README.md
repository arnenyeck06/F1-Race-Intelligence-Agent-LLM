# 🏎️ F1 Race Intelligence Agent

> Ask natural-language questions about the 2024 Formula 1 season — powered by real race data, hybrid RAG search.

---

## What it does

This agent answers questions about the 2024 F1 season by combining:
- **Structured race data** (lap times, pit stops, positions) from the OpenF1 API
- **Text search** over Wikipedia race summaries and F1 regulations
- **Claude AI** with tool-calling to reason across both data sources

### Example questions
- *"Who won the Monaco Grand Prix 2024?"*
- *"What were Hamilton's fastest laps at Silverstone?"*
- *"How many pit stops did Ferrari make in Bahrain?"*
- *"What is DRS and when can drivers use it?"*
- *"Compare Red Bull and McLaren lap times at the British GP"*

---

## Run it locally (5 steps)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — for Postgres
- Python 3.12+
- An [Anthropic API key](https://console.anthropic.com/settings/keys)

### Step 1 — Clone and configure
```bash
git clone https://github.com/arnenyeck06/F1-Race-Intelligence-Agent-LLM.git
cd F1-Race-Intelligence-Agent-LLM
cp .env.example .env
```
Open `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your-key-here
```

### Step 2 — Start the database
```bash
docker compose up -d
```
This starts Postgres + pgvector on port 5433.

### Step 3 — Install dependencies and download model
```bash
pip install -r requirements.txt
python ingestion/download_model.py
```
The ONNX embedding model is ~90MB — downloads once.

### Step 4 — Ingest 2024 season data
```bash
python ingest.py --year 2024
python ingestion/fix_meeting_names.py --year 2024
python ingest_text.py
```
This fetches race data from OpenF1 and Wikipedia. Takes ~10 minutes due to API rate limits.

### Step 5 — Launch the app
```bash
export TOKENIZERS_PARALLELISM=false
export $(cat .env | xargs)
streamlit run app.py
```
Open **http://localhost:8501** in your browser.

---

## How to use the app

| Tab | What you get |
|-----|-------------|
| 🏆 Race Result | Full classification + podium for any 2024 race |
| ⚡ Fastest Laps | Top lap times per race |
| 🔧 Pit Stops | All pit stop durations and timing |
| 💬 Ask Agent | Type any F1 question — Claude answers from real data |

Use the **race selector** in the left sidebar to switch between any of the 30 sessions from the 2024 season.

To ask a question: click the **💬 Ask Agent** tab → type your question or pick an example → click **ASK AGENT**.

---

## Architecture

```
OpenF1 API ──────────────────→ Postgres (laps, pit stops, positions)
Wikipedia API ────────────────→ pgvector (race summaries, regulations)
                                        ↓
                        Hybrid RRF Search (BM25 + cosine similarity)
                                        ↓
                        Claude Agent (tool-calling loop)
                                        ↓
                              Streamlit UI
```

## Stack

| Layer | Technology |
|-------|-----------|
| Race data | OpenF1 API (free, no auth) |
| Text data | Wikipedia API |
| Database | Postgres + pgvector |
| Keyword search | minsearch (TF-IDF) |
| Vector search | ONNX (Xenova/all-MiniLM-L6-v2, 384-dim) |
| Hybrid search | Reciprocal Rank Fusion (RRF) |
| LLM | Claude Sonnet |
| Interface | Streamlit |

## Data sources

All data is free and publicly available — no special access needed:
- [OpenF1 API](https://openf1.org) — live and historical F1 race data
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) — race summaries and regulations

## Knowledge base

| Source | Records |
|--------|---------|
| Race sessions (2024) | 30 sessions |
| Lap times | ~30,000 laps |
| Pit stops | ~500 pit stops |
| Text chunks | 214 chunks (21 Wikipedia articles) |