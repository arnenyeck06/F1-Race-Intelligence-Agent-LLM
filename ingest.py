"""
ingest.py — Fetch F1 data from OpenF1 and load into Postgres.

Usage:
  python ingest.py --year 2024
  python ingest.py --year 2023 --year 2024
"""

import argparse
import time
from ingestion.openf1_client import get_sessions, get_laps, get_pit_stops, get_positions, get_drivers, get_stints
from ingestion.db_loader import upsert_session, insert_laps, insert_pit_stops, insert_positions

DELAY = 3  # seconds between API calls


def ingest_session(session):
    session_key = session["session_key"]
    meeting = session.get("meeting_name", "Unknown")
    print(f"  [{session_key}] {meeting}")

    upsert_session(session)

    drivers = get_drivers(session_key); time.sleep(DELAY)
    laps = get_laps(session_key); time.sleep(DELAY)
    pit_stops = get_pit_stops(session_key); time.sleep(DELAY)
    stints = get_stints(session_key); time.sleep(DELAY)
    positions = get_positions(session_key); time.sleep(DELAY)

    insert_laps(session_key, laps, drivers)
    insert_pit_stops(session_key, pit_stops, stints, drivers)
    insert_positions(session_key, positions, drivers)

    print(f"    laps={len(laps)} pits={len(pit_stops)} positions={len(positions)}")
    time.sleep(DELAY)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", action="append", type=int, required=True)
    args = parser.parse_args()

    for year in args.year:
        print(f"\n[ingest] Year {year}")
        sessions = get_sessions(year=year, session_type="Race")
        print(f"[ingest] Found {len(sessions)} race sessions.")
        for session in sessions:
            try:
                ingest_session(session)
            except Exception as e:
                print(f"  ERROR: {e}")
                time.sleep(10)  # longer wait on error


if __name__ == "__main__":
    main()
