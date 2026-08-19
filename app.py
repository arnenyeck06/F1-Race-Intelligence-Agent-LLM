"""
Streamlit UI for F1 Race Intelligence Agent — F1 video game aesthetic.
"""

import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="F1 Race Intelligence Agent",
    page_icon="🏎️",
    layout="wide"
)

# F1 video game dark theme
st.markdown("""
<style>
    /* Global dark theme */
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #222; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d0d0d; border-bottom: 1px solid #222; gap: 0; }
    .stTabs [data-baseweb="tab"] { background-color: transparent; color: #666; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; border-bottom: 2px solid transparent; padding: 12px 20px; }
    .stTabs [aria-selected="true"] { color: #e10600 !important; border-bottom: 2px solid #e10600 !important; background: transparent !important; }
    .stTabs [data-baseweb="tab-panel"] { background-color: #0d0d0d; padding: 20px; }
    .stSelectbox > div > div { background-color: #1a1a1a !important; border: 1px solid #333 !important; color: #fff !important; }
    .stTextInput > div > div > input { background-color: #1a1a1a !important; border: 1px solid #333 !important; color: #fff !important; }
    .stTextInput > div > div > input:focus { border-color: #e10600 !important; }
    .stButton > button { background-color: #e10600 !important; color: #fff !important; border: none !important; font-weight: 700 !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
    .stButton > button:hover { background-color: #c20000 !important; }
    div[data-testid="stMetric"] { background-color: #1a1a1a; border: 1px solid #222; border-radius: 8px; padding: 12px; }
    div[data-testid="stMetric"] label { color: #666 !important; font-size: 11px !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
    div[data-testid="stMetric"] div { color: #ffffff !important; }
    .stDataFrame { background-color: #1a1a1a !important; }
    thead tr th { background-color: #111 !important; color: #666 !important; font-size: 10px !important; letter-spacing: 2px !important; text-transform: uppercase !important; }
    .f1-title { color: #e10600; font-size: 28px; font-weight: 900; letter-spacing: 4px; }
    .f1-sub { color: #666; font-size: 10px; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 20px; }
    .podium-card { background: #1a0000; border: 1px solid #e10600; border-radius: 8px; padding: 16px; text-align: center; }
    .podium-card-2 { background: #1a1a1a; border: 1px solid #444; border-radius: 8px; padding: 16px; text-align: center; }
    .team-ferrari { color: #dc143c; font-weight: 700; }
    .team-mclaren { color: #ff8000; font-weight: 700; }
    .team-redbull { color: #3671c6; font-weight: 700; }
    .team-mercedes { color: #00d2be; font-weight: 700; }
    hr { border-color: #222 !important; }
</style>
""", unsafe_allow_html=True)

# --- Load data ---
from agent.tools import get_race_sessions, get_race_result, get_fastest_laps, get_pit_stops

@st.cache_data
def load_sessions():
    sessions = get_race_sessions(year=2024)
    return [s for s in sessions if s.get("meeting_name")]

sessions = load_sessions()
session_map = {f"{s['meeting_name']} — {s['country']}": s for s in sessions}

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="f1-title">F1</div>', unsafe_allow_html=True)
    st.markdown('<div class="f1-sub">Race Intelligence Agent</div>', unsafe_allow_html=True)
    st.markdown("---")
    selected_label = st.selectbox("SELECT RACE", list(session_map.keys()), label_visibility="visible")
    selected_session = session_map[selected_label]
    session_key = selected_session["session_key"]
    st.markdown("---")
    st.markdown(f"**CIRCUIT** &nbsp; {selected_session.get('circuit_name','N/A')}")
    st.markdown(f"**COUNTRY** &nbsp; {selected_session.get('country','N/A')}")
    st.markdown(f"**DATE** &nbsp; {str(selected_session.get('date_start',''))[:10]}")
    st.markdown("---")
    st.markdown('<span style="background:#e10600;color:#fff;font-size:10px;font-weight:700;padding:3px 10px;border-radius:3px;letter-spacing:2px">RACE</span>', unsafe_allow_html=True)

# --- Main ---
st.markdown(f'<h2 style="color:#e10600;font-weight:900;letter-spacing:3px;margin-bottom:4px">{selected_label.split("—")[0].strip().upper()}</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="color:#666;font-size:11px;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px">2024 Formula 1 World Championship</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏆 RACE RESULT", "⚡ FASTEST LAPS", "🔧 PIT STOPS", "💬 ASK AGENT"])

# TAB 1 — Race Result
with tab1:
    result = get_race_result(session_key)
    if result and len(result) >= 3:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="podium-card-2">
                <div style="font-size:32px;color:#aaa;font-weight:900">2</div>
                <div style="font-size:13px;font-weight:700;color:#fff">{result[1]['driver_name']}</div>
                <div style="font-size:11px;color:#666">{result[1]['team_name']}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="podium-card">
                <div style="font-size:40px;color:#e10600;font-weight:900">1</div>
                <div style="font-size:14px;font-weight:700;color:#fff">{result[0]['driver_name']}</div>
                <div style="font-size:11px;color:#999">{result[0]['team_name']}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="podium-card-2">
                <div style="font-size:32px;color:#b87333;font-weight:900">3</div>
                <div style="font-size:13px;font-weight:700;color:#fff">{result[2]['driver_name']}</div>
                <div style="font-size:11px;color:#666">{result[2]['team_name']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if result:
        df = pd.DataFrame(result)
        df.index = range(1, len(df)+1)
        df.columns = ["Driver", "Team", "Position"]
        df = df[["Position", "Driver", "Team"]]
        st.dataframe(df, use_container_width=True, height=350)

# TAB 2 — Fastest Laps
with tab2:
    top_n = st.slider("Top N laps", 5, 20, 10, key="top_n")
    laps = get_fastest_laps(session_key, top_n=top_n)
    if laps:
        df = pd.DataFrame(laps)
        df["lap_duration"] = df["lap_duration"].apply(
            lambda x: f"{int(x//60)}:{x%60:06.3f}" if x else "N/A"
        )
        df.index = range(1, len(df)+1)
        df.columns = ["Driver", "Team", "Lap", "Time", "Compound"]
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.info("No lap data available.")

# TAB 3 — Pit Stops
with tab3:
    pits = get_pit_stops(session_key)
    pits = [p for p in pits if not (p["lap_number"] == 1 and p.get("pit_duration", 0) and p["pit_duration"] > 100)]
    if pits:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Stops", len(pits))
        fastest = min((p for p in pits if p.get("pit_duration")), key=lambda x: x["pit_duration"], default=None)
        if fastest:
            col2.metric("Fastest Stop", f"{fastest['pit_duration']:.1f}s")
            col3.metric("By", fastest["driver_name"].split()[-1])
        df = pd.DataFrame(pits)
        df["pit_duration"] = df["pit_duration"].apply(lambda x: f"{x:.1f}s" if x else "N/A")
        df.index = range(1, len(df)+1)
        df.columns = ["Driver", "Team", "Lap", "Duration"]
        st.dataframe(df, use_container_width=True, height=350)
    else:
        st.info("No pit stop data available.")

# TAB 4 — Ask Agent
with tab4:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.warning("Set ANTHROPIC_API_KEY in .env to enable the agent.")
        st.info("Explore race data using the tabs above while credits load.")
    else:
        st.markdown('<p style="color:#666;font-size:11px;letter-spacing:1px">ASK ANYTHING ABOUT THE 2024 F1 SEASON</p>', unsafe_allow_html=True)

        examples = [
            f"Who won the {selected_label.split('—')[0].strip()}?",
            "What were Hamilton's fastest laps at Silverstone 2024?",
            "How many pit stops did Ferrari make in Monaco?",
            "What is DRS and when can drivers use it?",
            "Compare Red Bull and McLaren lap times at Silverstone",
        ]

        example = st.selectbox("QUICK QUESTIONS", [""] + examples, label_visibility="visible")
        question = st.text_input("OR TYPE YOUR OWN", value=example, placeholder="e.g. Who won Monaco 2024?")

        if st.button("ASK AGENT") and question:
            with st.spinner("Agent searching race data..."):
                from agent.rag import run_agent
                result_agent = run_agent(question)
                st.markdown("---")
                st.markdown(f'<div style="background:#1a0000;border-left:3px solid #e10600;padding:16px;border-radius:0 8px 8px 0;color:#fff;font-size:14px;line-height:1.7">{result_agent["answer"]}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c1.metric("Input tokens", result_agent["input_tokens"])
                c2.metric("Output tokens", result_agent["output_tokens"])

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.markdown('<span style="color:#666;font-size:11px">📡 DATA: OPENF1 API + WIKIPEDIA</span>', unsafe_allow_html=True)
col2.markdown('<span style="color:#666;font-size:11px">🔍 SEARCH: HYBRID RRF (BM25 + PGVECTOR)</span>', unsafe_allow_html=True)
col3.markdown('<span style="color:#666;font-size:11px">🤖 LLM: CLAUDE SONNET</span>', unsafe_allow_html=True)
