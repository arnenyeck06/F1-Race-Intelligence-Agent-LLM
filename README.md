# 🏎️ F1 Race Intelligence Agent

> Ask natural-language questions about the 2024 Formula 1 season — powered by OpenF1 data, hybrid RAG search.

---

## 🚀 Try It Live



### How to ask a question:
1. Open the app
2. Click the **💬 ASK AGENT** tab (4th tab at the top)
3. Pick a quick example from the dropdown **or** type your own question
4. Click **ASK AGENT**
5. The answer appears below with citations

### Example questions to try:
- *"Who won the Monaco Grand Prix 2024?"*
- *"What were Hamilton's fastest laps at Silverstone?"*
- *"How many pit stops did Ferrari make in Bahrain?"*
- *"What is DRS and when can drivers use it?"*
- *"Compare Red Bull and McLaren lap times at the British GP"*

---

## 📊 What's in the app

| Tab | What you see |
|-----|-------------|
| 🏆 Race Result | Full classification + podium for any 2024 race |
| ⚡ Fastest Laps | Top lap times with driver and compound data |
| 🔧 Pit Stops | All pit stop durations per race |
| 💬 Ask Agent | Natural language Q&A powered by Claude + hybrid RAG |

Use the **race selector** in the left sidebar to switch between any of the 30 race sessions from the 2024 season.

---

## 🏗️ Architecture
OpenF1 API ──────────────────→ Postgres (laps, pit stops, positions)
Wikipedia API ────────────────→ pgvector (race summaries, regulations)
↓
Hybrid RRF Search (BM25 + cosine similarity)
↓
Claude Agent (tool-calling loop)
↓
FastAPI + Streamlit UI

## 🛠️ Stack

- **Race data**: [OpenF1 API](https://openf1.org) — free, no auth
- **Text data**: Wikipedia API — race summaries + F1 regulations
- **Storage**: Postgres + pgvector (384-dim HNSW index)
- **Keyword search**: minsearch (TF-IDF)
- **Vector search**: ONNX embedder (Xenova/all-MiniLM-L6-v2)
- **Hybrid search**: Reciprocal Rank Fusion (RRF)
- **LLM**: Claude Sonnet (Anthropic API)
- **Interface**: Streamlit

## 📦 Run Locally

```bash
# 1. Clone
git clone https://github.com/arnenyeck06/F1-Race-Intelligence-Agent-LLM.git
cd F1-Race-Intelligence-Agent-LLM

# 2. Set API key
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# 3. Start Postgres + pgvector
docker compose up -d

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download ONNX model (~90MB)
python ingestion/download_model.py

# 6. Ingest 2024 season data
python ingest.py --year 2024
python ingestion/fix_meeting_names.py --year 2024
python ingest_text.py

# 7. Run the app
streamlit run app.py
```

## 📁 Knowledge Base

**Structured data (Postgres):**
- 30 race sessions — full 2024 F1 season
- Lap times, pit stops, driver positions per race

**Text chunks (pgvector):**
- 214 chunks from 21 Wikipedia articles
- Race summaries + F1 technical regulations

## 🔗 Data Sources

All data is free and publicly available — no API keys required for ingestion:
- [OpenF1 API](https://openf1.org)
- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page)
