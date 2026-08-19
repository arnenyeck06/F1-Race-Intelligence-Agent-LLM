"""
db_loader.py
Load OpenF1 data into Postgres.
"""

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


def upsert_session(session):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sessions (session_key, meeting_name, circuit_name, country, year, session_type, date_start)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (session_key) DO UPDATE SET
            meeting_name = EXCLUDED.meeting_name,
            circuit_name = EXCLUDED.circuit_name
    """, (
        session["session_key"],
        session.get("meeting_name"),
        session.get("circuit_short_name"),
        session.get("country_name"),
        session.get("year"),
        session.get("session_type"),
        session.get("date_start"),
    ))
    conn.commit()
    cur.close()
    conn.close()


def insert_laps(session_key, laps, drivers):
    if not laps:
        return
    driver_map = {d["driver_number"]: d for d in drivers}
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM laps WHERE session_key = %s", (session_key,))
    for lap in laps:
        driver = driver_map.get(lap.get("driver_number"), {})
        cur.execute("""
            INSERT INTO laps (session_key, driver_number, driver_name, team_name,
                              lap_number, lap_duration, is_pit_out_lap, compound, tyre_age_at_start)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            session_key,
            lap.get("driver_number"),
            driver.get("full_name"),
            driver.get("team_name"),
            lap.get("lap_number"),
            lap.get("lap_duration"),
            lap.get("is_pit_out_lap", False),
            lap.get("compound"),
            lap.get("tyre_age_at_start"),
        ))
    conn.commit()
    cur.close()
    conn.close()


def insert_pit_stops(session_key, pit_stops, stints, drivers):
    if not pit_stops:
        return
    driver_map = {d["driver_number"]: d for d in drivers}
    # Build stint map for compound info
    stint_map = {}
    for s in stints:
        key = (s["driver_number"], s.get("lap_start"))
        stint_map[key] = s.get("compound")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM pit_stops WHERE session_key = %s", (session_key,))
    for pit in pit_stops:
        driver = driver_map.get(pit.get("driver_number"), {})
        cur.execute("""
            INSERT INTO pit_stops (session_key, driver_number, driver_name, team_name,
                                   lap_number, pit_duration, compound_in, compound_out)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            session_key,
            pit.get("driver_number"),
            driver.get("full_name"),
            driver.get("team_name"),
            pit.get("lap_number"),
            pit.get("pit_duration"),
            None,
            None,
        ))
    conn.commit()
    cur.close()
    conn.close()


def insert_positions(session_key, positions, drivers):
    if not positions:
        return
    driver_map = {d["driver_number"]: d for d in drivers}
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM positions WHERE session_key = %s", (session_key,))
    seen = set()
    for pos in positions:
        key = (pos.get("driver_number"), pos.get("position"))
        if key in seen:
            continue
        seen.add(key)
        driver = driver_map.get(pos.get("driver_number"), {})
        cur.execute("""
            INSERT INTO positions (session_key, driver_number, driver_name, team_name, lap_number, position)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            session_key,
            pos.get("driver_number"),
            driver.get("full_name"),
            driver.get("team_name"),
            pos.get("lap"),
            pos.get("position"),
        ))
    conn.commit()
    cur.close()
    conn.close()
