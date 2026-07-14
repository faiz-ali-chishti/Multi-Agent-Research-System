"""
Streamlit UI for the multi-agent research pipeline defined in pipeline.py

Run with:
    streamlit run app.py

Place this file in the same folder as pipeline.py, agents.py, and tools.py
(i.e. your existing project folder structure) so the import below works.
"""

import io
import re
import contextlib
import traceback

import streamlit as st

from pipeline import run_research_pipeline


st.set_page_config(
    page_title="Research Pipeline",
    page_icon="🧪",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Design tokens
# Each pipeline stage gets its own identity color, used consistently across
# the rail, tabs, and section labels so a color always means the same agent.
#   01 Search    -> teal    #2DD4BF
#   02 Scrape    -> amber   #F5B942
#   03 Write     -> violet  #A78BFA
#   04 Critique  -> rose    #FB7185
# ---------------------------------------------------------------------------
STAGES = [
    {"n": "01", "label": "Search", "color": "#2DD4BF", "glow": "rgba(45,212,191,0.35)"},
    {"n": "02", "label": "Scrape", "color": "#F5B942", "glow": "rgba(245,185,66,0.35)"},
    {"n": "03", "label": "Write", "color": "#A78BFA", "glow": "rgba(167,139,250,0.35)"},
    {"n": "04", "label": "Critique", "color": "#FB7185", "glow": "rgba(251,113,133,0.35)"},
]

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root {
    --bg: #10121b;
    --bg-alt: #171a28;
    --surface: #1b1f31;
    --surface-2: #232840;
    --border: #2c3150;
    --text: #f1eee7;
    --text-muted: #9096b4;
    --teal: #2dd4bf;
    --amber: #f5b942;
    --violet: #a78bfa;
    --rose: #fb7185;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 0%, rgba(167,139,250,0.10), transparent 40%),
        radial-gradient(circle at 80% 10%, rgba(45,212,191,0.10), transparent 40%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 780px;
    padding-top: 2.2rem;
}

/* ---------- Hero ---------- */
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.3rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, var(--teal), var(--amber), var(--violet), var(--rose));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0.15rem;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 0.98rem;
    margin-bottom: 1.4rem;
}

/* ---------- Pipeline rail (signature element) ---------- */
.rail {
    display: flex;
    align-items: center;
    margin: 0.2rem 0 1.8rem 0;
    flex-wrap: wrap;
    gap: 0.4rem 0;
}
.rail-node {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0.9rem;
    border-radius: 999px;
    background: var(--surface);
    border: 1px solid var(--border);
    white-space: nowrap;
}
.rail-node.active {
    border-color: var(--dot-color);
    box-shadow: 0 0 0 1px var(--dot-color), 0 0 18px var(--glow-color);
}
.rail-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--dot-color);
    opacity: 0.35;
}
.rail-node.active .rail-dot {
    opacity: 1;
}
.rail-n {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
}
.rail-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text);
}
.rail-line {
    flex: 1;
    min-width: 16px;
    height: 1px;
    background: var(--border);
    margin: 0 0.4rem;
}

/* ---------- Input card ---------- */
.stTextArea textarea {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 10px;
}
.stTextArea textarea:focus {
    border-color: var(--violet);
    box-shadow: 0 0 0 1px var(--violet);
}

/* Primary run button: teal -> violet gradient, the app's one loud gesture */
button[kind="primary"] {
    background: linear-gradient(120deg, var(--teal), var(--violet));
    color: #0c0e16;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(167,139,250,0.35);
}
.stButton button, .stDownloadButton button {
    border-radius: 10px;
}

/* ---------- Section badges ---------- */
.section-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    padding-bottom: 0.3rem;
    margin-bottom: 0.6rem;
    border-bottom: 2px solid var(--badge-color);
    color: var(--text);
}
.section-badge .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--badge-color);
    box-shadow: 0 0 10px var(--badge-color);
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-bottom: none;
    border-radius: 10px 10px 0 0;
    padding: 0.5rem 1rem;
    color: var(--text-muted);
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    color: var(--text) !important;
    background: var(--surface-2) !important;
}

/* ---------- Expander (history) ---------- */
div[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
}

/* ---------- Alerts / status ---------- */
div[data-testid="stAlert"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
}
div[data-testid="stStatusWidget"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
}

/* ---------- Text blocks / code ---------- */
.stMarkdown, .stText, p, li {
    color: var(--text);
}
pre, code {
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-testid="stTextArea"] textarea,
.stCodeBlock, pre {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ---------- Divider ---------- */
hr {
    border-color: var(--border) !important;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


def render_rail(reached_stage: int = -1):
    """Render the 4-stage pipeline rail.

    reached_stage: index of the furthest stage completed/attempted (-1 =
    light up all, -2 = no run yet so dim all, 0..3 = light up through that
    index).
    """
    nodes_html = []
    for i, stage in enumerate(STAGES):
        if reached_stage == -2:
            active = ""
        elif reached_stage == -1 or i <= reached_stage:
            active = "active"
        else:
            active = ""
        nodes_html.append(
            f'<div class="rail-node {active}" style="--dot-color:{stage["color"]}; '
            f'--glow-color:{stage["glow"]}">'
            f'<span class="rail-dot"></span>'
            f'<span class="rail-n">{stage["n"]}</span>'
            f'<span class="rail-label">{stage["label"]}</span>'
            f'</div>'
        )
        if i != len(STAGES) - 1:
            nodes_html.append('<div class="rail-line"></div>')
    st.markdown(f'<div class="rail">{"".join(nodes_html)}</div>', unsafe_allow_html=True)


def section_badge(label: str, color: str):
    st.markdown(
        f'<div class="section-badge" style="--badge-color:{color}">'
        f'<span class="dot"></span>{label}</div>',
        unsafe_allow_html=True,
    )


def detect_reached_step(logs: str) -> int:
    """Look at captured console output and figure out the furthest
    'step N' marker printed, so the rail can reflect real progress."""
    found = -1
    for i in range(4):
        if re.search(rf"step\s*{i + 1}\b", logs, re.IGNORECASE):
            found = i
    return found


# ---------------------------------------------------------------------------
# Session state setup
# ---------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "logs" not in st.session_state:
    st.session_state.logs = ""
if "error" not in st.session_state:
    st.session_state.error = None
if "history" not in st.session_state:
    st.session_state.history = []  # list of (topic, result, logs) tuples


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown('<div class="hero-eyebrow">🧪 Multi-agent system</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Research Pipeline</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Four agents, one report — a Streamlit front end for '
    '<code>pipeline.run_research_pipeline</code></div>',
    unsafe_allow_html=True,
)

_reached = detect_reached_step(st.session_state.logs) if st.session_state.logs else -2
render_rail(_reached)


# ---------------------------------------------------------------------------
# Input + controls — everything lives in this single column, top to bottom
# ---------------------------------------------------------------------------
topic = st.text_area(
    "Research topic",
    placeholder="e.g. Impact of quantum computing on cryptography",
    height=90,
)

col_run, col_clear = st.columns([3, 1])
with col_run:
    run_clicked = st.button("Run pipeline", type="primary", use_container_width=True)
with col_clear:
    clear_clicked = st.button("Clear", use_container_width=True)

if clear_clicked:
    st.session_state.result = None
    st.session_state.logs = ""
    st.session_state.error = None
    st.rerun()

if st.session_state.history:
    with st.expander(f"Past runs ({len(st.session_state.history)})"):
        for i, (past_topic, _, _) in enumerate(reversed(st.session_state.history)):
            if st.button(f"↺ {past_topic[:60]}", key=f"hist_{i}", use_container_width=True):
                idx = len(st.session_state.history) - 1 - i
                st.session_state.result = st.session_state.history[idx][1]
                st.session_state.logs = st.session_state.history[idx][2]
                st.session_state.error = None
                st.rerun()


# ---------------------------------------------------------------------------
# Run the pipeline
# ---------------------------------------------------------------------------
if run_clicked:
    if not topic or not topic.strip():
        st.warning("Please enter a research topic before running the pipeline.")
    else:
        st.session_state.error = None
        status_box = st.status("Starting pipeline...", expanded=True)
        log_buffer = io.StringIO()

        try:
            status_box.write("Step 1 · Searching the web...")
            # Capture everything the pipeline prints to stdout so we can show
            # it to the user as a log, since run_research_pipeline() itself
            # only returns a value at the very end.
            with contextlib.redirect_stdout(log_buffer):
                result = run_research_pipeline(topic.strip())

            status_box.update(label="Pipeline finished", state="complete", expanded=False)

            st.session_state.result = result
            st.session_state.logs = log_buffer.getvalue()
            st.session_state.history.append((topic.strip(), result, log_buffer.getvalue()))
            st.rerun()

        except Exception as e:
            status_box.update(label="Pipeline failed", state="error", expanded=True)
            st.session_state.error = f"{e}\n\n{traceback.format_exc()}"
            st.session_state.logs = log_buffer.getvalue()
            st.session_state.result = None


# ---------------------------------------------------------------------------
# Error display
# ---------------------------------------------------------------------------
if st.session_state.error:
    st.error("The pipeline raised an error:")
    st.code(st.session_state.error, language="text")


# ---------------------------------------------------------------------------
# Results display
# ---------------------------------------------------------------------------
if st.session_state.result:
    result = st.session_state.result

    tab_report, tab_feedback, tab_search, tab_scraped, tab_logs = st.tabs(
        ["📄 Report", "🧐 Critique", "🔍 Search", "📑 Scraped", "🖥️ Logs"]
    )

    with tab_report:
        section_badge("Final Report", "#A78BFA")
        st.markdown(result.get("report", "_No report generated._"))
        st.download_button(
            "Download report (.md)",
            data=result.get("report", ""),
            file_name="report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        section_badge("Critic Feedback", "#FB7185")
        st.markdown(result.get("feedback", "_No feedback generated._"))

    with tab_search:
        section_badge("Raw Search Results", "#2DD4BF")
        st.text(result.get("search_results", "_No search results._"))

    with tab_scraped:
        section_badge("Scraped Content", "#F5B942")
        st.text(result.get("scraped_content", "_No scraped content._"))

    with tab_logs:
        section_badge("Console Output", "#9096B4")
        st.text(st.session_state.logs or "_No logs captured._")

elif not st.session_state.error:
    st.info("Enter a topic above and click **Run pipeline** to get started.")