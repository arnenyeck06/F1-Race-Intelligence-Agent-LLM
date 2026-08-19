import requests
import time

WIKI_SEARCH = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "f1-intelligence-rag/1.0 (contact@example.com)"}

RACES_2024 = [
    "2024 Bahrain Grand Prix",
    "2024 Saudi Arabian Grand Prix",
    "2024 Australian Grand Prix",
    "2024 Japanese Grand Prix",
    "2024 Chinese Grand Prix",
    "2024 Miami Grand Prix",
    "2024 Emilia Romagna Grand Prix",
    "2024 Monaco Grand Prix",
    "2024 Canadian Grand Prix",
    "2024 Spanish Grand Prix",
    "2024 Austrian Grand Prix",
    "2024 British Grand Prix",
    "2024 Hungarian Grand Prix",
    "2024 Belgian Grand Prix",
    "2024 Dutch Grand Prix",
    "2024 Italian Grand Prix",
    "2024 Azerbaijan Grand Prix",
    "2024 Singapore Grand Prix",
    "2024 United States Grand Prix",
    "2024 Mexico City Grand Prix",
    "2024 São Paulo Grand Prix",
    "2024 Las Vegas Grand Prix",
    "2024 Qatar Grand Prix",
    "2024 Abu Dhabi Grand Prix",
]

REGULATIONS = [
    "Formula One regulations",
    "Formula One car",
    "Pit stop (motorsport)",
    "Formula One tyres",
    "DRS (Formula One)",
    "Safety car",
    "Formula One points system",
]


def fetch_page_text(title):
    resp = requests.get(WIKI_SEARCH, headers=HEADERS, params={
        "action": "query", "titles": title,
        "prop": "extracts", "explaintext": True, "format": "json",
    }, timeout=15)
    resp.raise_for_status()
    pages = resp.json()["query"]["pages"]
    page = next(iter(pages.values()))
    return page.get("extract", "")


def fetch_all(titles, delay=5.0):
    results = []
    for i, title in enumerate(titles):
        try:
            text = fetch_page_text(title)
            if text:
                results.append({"title": title, "text": text})
                print(f"  [wiki] {title}: {len(text):,} chars")
            else:
                print(f"  [wiki] {title}: empty")
        except Exception as e:
            print(f"  [wiki] ERROR {title}: {e}")
            if "429" in str(e):
                print("  [wiki] Rate limited — waiting 30s...")
                time.sleep(30)
        time.sleep(delay)
    return results
