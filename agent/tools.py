"""
tools.py
SQL-backed tools the LLM agent can call to answer F1 questions.
"""

import os
import psycopg2
import psycopg2.extras
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ingestion.db_loader import get_conn


def get_race_sessions(year: int = 2024) -> list[dict]:
    """List all race sessions for a given year."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT session_key, meeting_name, circuit_name, country, year, date_start
        FROM sessions WHERE year = %s ORDER BY session_key
    """, (year,))
    results = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results


def get_fastest_laps(session_key: int, top_n: int = 5) -> list[dict]:
    """Get the fastest laps for a session."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT driver_name, team_name, lap_number, lap_duration, compound
        FROM laps
        WHERE session_key = %s AND lap_duration IS NOT NULL AND is_pit_out_lap = false
        ORDER BY lap_duration ASC
        LIMIT %s
    """, (session_key, top_n))
    results = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results


def get_pit_stops(session_key: int) -> list[dict]:
    """Get all pit stops for a session."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT driver_name, team_name, lap_number, pit_duration
        FROM pit_stops
        WHERE session_key = %s
        ORDER BY lap_number, pit_duration
    """, (session_key,))
    results = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results


def get_race_result(session_key: int) -> list[dict]:
    """Get final race positions."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT DISTINCT ON (driver_number)
            driver_name, team_name, position
        FROM positions
        WHERE session_key = %s
        ORDER BY driver_number, lap_number DESC
    """, (session_key,))
    results = sorted([dict(r) for r in cur.fetchall()], key=lambda x: x["position"] or 99)
    cur.close()
    conn.close()
    return results


def get_driver_laps(session_key: int, driver_name: str) -> list[dict]:
    """Get all laps for a specific driver in a session."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT lap_number, lap_duration, compound, tyre_age_at_start
        FROM laps
        WHERE session_key = %s AND driver_name ILIKE %s
        ORDER BY lap_number
    """, (session_key, f"%{driver_name}%"))
    results = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results


def find_session(country: str = None, meeting_name: str = None, year: int = 2024) -> dict | None:
    """Find a session by country or meeting name."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if country:
        cur.execute("""
            SELECT * FROM sessions
            WHERE year = %s AND country ILIKE %s
            ORDER BY session_key DESC LIMIT 1
        """, (year, f"%{country}%"))
    elif meeting_name:
        cur.execute("""
            SELECT * FROM sessions
            WHERE year = %s AND meeting_name ILIKE %s
            ORDER BY session_key DESC LIMIT 1
        """, (year, f"%{meeting_name}%"))
    else:
        return None
    result = cur.fetchone()
    cur.close()
    conn.close()
    return dict(result) if result else None
