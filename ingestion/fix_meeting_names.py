import requests
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ingestion.db_loader import get_conn

BASE_URL = "https://api.openf1.org/v1"

def fix_names(year):
    meetings = requests.get(f"{BASE_URL}/meetings", params={"year": year}, timeout=15).json()
    sessions = requests.get(f"{BASE_URL}/sessions", params={"year": year, "session_type": "Race"}, timeout=15).json()
    meeting_map = {m["meeting_key"]: m for m in meetings}
    conn = get_conn()
    cur = conn.cursor()
    for session in sessions:
        meeting = meeting_map.get(session.get("meeting_key"), {})
        name = meeting.get("meeting_name") or "Unknown"
        circuit = meeting.get("circuit_short_name")
        country = meeting.get("country_name")
        cur.execute("""
            UPDATE sessions SET meeting_name = %s, circuit_name = %s, country = %s
            WHERE session_key = %s
        """, (name, circuit, country, session["session_key"]))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Fixed meeting names for {year}.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    args = parser.parse_args()
    fix_names(args.year)
