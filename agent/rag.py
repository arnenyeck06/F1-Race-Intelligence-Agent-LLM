import json
import os
import anthropic
from agent.tools import (
    get_race_sessions, get_fastest_laps, get_pit_stops,
    get_race_result, get_driver_laps, find_session
)

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are an F1 Race Intelligence Agent with access to race data tools.

You have access to the following tools:
- get_race_sessions(year): list all races for a year
- find_session(country, meeting_name, year): find a specific race session
- get_fastest_laps(session_key, top_n): get fastest laps in a race
- get_pit_stops(session_key): get all pit stops in a race
- get_race_result(session_key): get final race positions
- get_driver_laps(session_key, driver_name): get all laps for a driver

Always:
1. First find the session_key using find_session or get_race_sessions
2. Then use the session_key to get specific data
3. Answer with specific numbers and facts from the data
4. If data is missing, say so clearly

Be concise and precise like an F1 analyst."""

TOOLS = [
    {
        "name": "get_race_sessions",
        "description": "List all race sessions for a given year",
        "input_schema": {
            "type": "object",
            "properties": {"year": {"type": "integer"}},
            "required": ["year"]
        }
    },
    {
        "name": "find_session",
        "description": "Find a race session by country or meeting name",
        "input_schema": {
            "type": "object",
            "properties": {
                "country": {"type": "string"},
                "meeting_name": {"type": "string"},
                "year": {"type": "integer"}
            }
        }
    },
    {
        "name": "get_fastest_laps",
        "description": "Get the fastest laps for a race session",
        "input_schema": {
            "type": "object",
            "properties": {
                "session_key": {"type": "integer"},
                "top_n": {"type": "integer"}
            },
            "required": ["session_key"]
        }
    },
    {
        "name": "get_pit_stops",
        "description": "Get all pit stops for a race session",
        "input_schema": {
            "type": "object",
            "properties": {"session_key": {"type": "integer"}},
            "required": ["session_key"]
        }
    },
    {
        "name": "get_race_result",
        "description": "Get final race positions for a session",
        "input_schema": {
            "type": "object",
            "properties": {"session_key": {"type": "integer"}},
            "required": ["session_key"]
        }
    },
    {
        "name": "get_driver_laps",
        "description": "Get all laps for a specific driver in a session",
        "input_schema": {
            "type": "object",
            "properties": {
                "session_key": {"type": "integer"},
                "driver_name": {"type": "string"}
            },
            "required": ["session_key", "driver_name"]
        }
    }
]

TOOL_MAP = {
    "get_race_sessions": get_race_sessions,
    "find_session": find_session,
    "get_fastest_laps": get_fastest_laps,
    "get_pit_stops": get_pit_stops,
    "get_race_result": get_race_result,
    "get_driver_laps": get_driver_laps,
}


def run_agent(query: str, verbose: bool = False) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    messages = [{"role": "user", "content": query}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if verbose:
            print(f"[agent] stop_reason={response.stop_reason}")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            answer = " ".join(
                block.text for block in response.content
                if hasattr(block, "text")
            )
            return {
                "answer": answer,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            tool_fn = TOOL_MAP.get(block.name)
            if not tool_fn:
                result = {"error": f"Unknown tool: {block.name}"}
            else:
                try:
                    result = tool_fn(**block.input)
                    if verbose:
                        print(f"[tool] {block.name}({block.input})")
                except Exception as e:
                    result = {"error": str(e)}

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result, default=str),
            })

        messages.append({"role": "user", "content": tool_results})
