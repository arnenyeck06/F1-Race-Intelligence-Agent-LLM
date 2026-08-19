"""
openf1_client.py
Fetch F1 data from OpenF1 API — free, no auth required.
Docs: https://openf1.org
"""

import requests
import time

BASE_URL = "https://api.openf1.org/v1"


def get(endpoint, params=None, retries=3):
    url = f"{BASE_URL}/{endpoint}"
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2)
    return []


def get_sessions(year=2024, session_type="Race"):
    """Get all race sessions for a given year."""
    return get("sessions", {"year": year, "session_type": session_type})


def get_laps(session_key):
    """Get all lap data for a session."""
    return get("laps", {"session_key": session_key})


def get_pit_stops(session_key):
    """Get all pit stop data for a session."""
    return get("pit", {"session_key": session_key})


def get_positions(session_key):
    """Get position data for a session."""
    return get("position", {"session_key": session_key})


def get_drivers(session_key):
    """Get driver info for a session."""
    return get("drivers", {"session_key": session_key})


def get_stints(session_key):
    """Get stint/tyre data for a session."""
    return get("stints", {"session_key": session_key})
