import html
import os
import re

import streamlit as st

from pipeline import run_research_pipeline


st.set_page_config(
    page_title="ORCA — Research Studio",
    page_icon="🌊",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --orca-ink: #eaf3f4;
        --orca-muted: #93a8ad;
        --orca-teal: #65e0ca;
        --orca-blue: #82baff;
        --orca-line: rgba(160, 194, 198, .15);
        --orca-panel: rgba(15, 31, 39, .82);
    }
    .stApp {
        background:
            radial-gradient(ellipse at 90% 4%, rgba(39, 102, 130, .22), transparent 34%),
            radial-gradient(ellipse at 8% 16%, rgba(33, 124, 112, .17), transparent 32%),
            #081116;
        color: var(--orca-ink);
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 1180px;
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102129 0%, #0b171d 100%);
        border-right: 1px solid var(--orca-line);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--orca-muted);
    }
    .brand-lockup {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin: .35rem 0 1.4rem;
    }
    .brand-mark {
        display: grid;
        width: 46px;
        height: 46px;
        place-items: center;
        border: 1px solid rgba(101, 224, 202, .48);
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(101, 224, 202, .2), rgba(130, 186, 255, .09));
        box-shadow: 0 0 30px rgba(70, 210, 190, .12);
        color: var(--orca-teal);
        font-size: 1.45rem;
    }
    .brand-name {
        color: var(--orca-ink);
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: .17em;
    }
    .brand-subtitle {
        color: var(--orca-muted);
        font-size: .72rem;
        letter-spacing: .04em;
    }
    .side-heading {
        margin: 1.2rem 0 .6rem;
        color: var(--orca-ink);
        font-size: .77rem;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
    }
    .workflow-step {
        display: flex;
        align-items: center;
        gap: .7rem;
        margin: .55rem 0;
        color: #c1d0d1;
        font-size: .88rem;
    }
    .step-number {
        display: grid;
        width: 25px;
        height: 25px;
        flex: 0 0 25px;
        place-items: center;
        border: 1px solid var(--orca-line);
        border-radius: 50%;
        color: var(--orca-teal);
        font-size: .72rem;
        font-weight: 700;
    }
    .hero {
        position: relative;
        overflow: hidden;
        padding: 1.65rem 1.8rem 1.8rem;
        border: 1px solid var(--orca-line);
        border-radius: 24px;
        background:
            radial-gradient(ellipse at 92% 0%, rgba(101, 224, 202, .12), transparent 35%),
            linear-gradient(125deg, rgba(17, 37, 45, .96), rgba(11, 25, 33, .88));
        box-shadow: 0 24px 80px rgba(0, 0, 0, .18);
    }
    .hero-topline {
        display: flex;
        align-items: center;
        gap: .5rem;
        margin-bottom: 1.3rem;
    }
    .eyebrow {
        color: var(--orca-teal);
        font-size: .7rem;
        font-weight: 700;
        letter-spacing: .18em;
        text-transform: uppercase;
    }
    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--orca-teal);
        box-shadow: 0 0 12px rgba(101, 224, 202, .8);
    }
    .hero h1 {
        max-width: 760px;
        margin: 0;
        color: var(--orca-ink);
        font-size: clamp(2.1rem, 5vw, 3.55rem);
        letter-spacing: -.055em;
        line-height: 1.05;
    }
    .hero h1 span {
        color: var(--orca-teal);
    }
    .hero-copy {
        max-width: 620px;
        margin: .9rem 0 0;
        color: #a8bbbe;
        font-size: .98rem;
        line-height: 1.7;
    }
    .hero-foot {
        display: flex;
        flex-wrap: wrap;
        gap: .5rem;
        margin-top: 1.35rem;
    }
    .hero-tag {
        padding: .35rem .65rem;
        border: 1px solid var(--orca-line);
        border-radius: 999px;
        color: #c1d4d4;
        font-size: .72rem;
    }
    .section-label {
        margin: 1.7rem 0 .3rem;
        color: var(--orca-teal);
        font-size: .7rem;
        font-weight: 700;
        letter-spacing: .17em;
        text-transform: uppercase;
    }
    .section-title {
        margin: 0 0 .25rem;
        color: var(--orca-ink);
        font-size: 1.22rem;
        font-weight: 700;
    }
    .section-copy {
        margin: 0 0 1rem;
        color: var(--orca-muted);
        font-size: .86rem;
    }
    div[data-testid="stForm"] {
        padding: 1.15rem 1.25rem 1.25rem;
        border: 1px solid var(--orca-line);
        border-radius: 18px;
        background: var(--orca-panel);
        box-shadow: 0 18px 54px rgba(0, 0, 0, .14);
    }
    div[data-testid="stTextArea"] label {
        color: #d7e5e4;
        font-weight: 600;
    }
    div[data-testid="stTextArea"] textarea {
        border: 1px solid rgba(155, 192, 195, .2);
        border-radius: 12px;
        background: rgba(6, 18, 23, .7);
        color: var(--orca-ink);
    }
    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button {
        min-height: 2.9rem;
        border: 0;
        border-radius: 11px;
        background: linear-gradient(100deg, #65e0ca, #83d6d2);
        color: #06201e;
        font-weight: 700;
        transition: transform .18s ease, box-shadow .18s ease;
    }
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(101, 224, 202, .2);
    }
    div[data-testid="stTabs"] button {
        color: #a8bbbe;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--orca-teal);
    }
    .result-heading {
        margin: 1.7rem 0 .2rem;
        color: var(--orca-ink);
        font-size: 1.5rem;
        font-weight: 750;
        letter-spacing: -.025em;
    }
    .result-topic {
        margin-bottom: .9rem;
        color: var(--orca-muted);
        font-size: .9rem;
    }
    div[data-testid="stMetric"] {
        padding: .8rem 1rem;
        border: 1px solid var(--orca-line);
        border-radius: 14px;
        background: rgba(15, 31, 39, .72);
    }
    div[data-testid="stMetricLabel"] {
        color: var(--orca-muted);
    }
    div[data-testid="stMetricValue"] {
        color: var(--orca-teal);
    }
    .source-card {
        margin: .55rem 0;
        padding: .9rem 1rem;
        border: 1px solid var(--orca-line);
        border-radius: 13px;
        background: rgba(15, 31, 39, .65);
    }
    .source-title {
        margin-bottom: .35rem;
        color: var(--orca-ink);
        font-weight: 650;
    }
    .source-url {
        overflow-wrap: anywhere;
        color: var(--orca-blue);
        font-size: .78rem;
    }
    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 1rem 2rem;
        }
        .hero {
            padding: 1.25rem;
            border-radius: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
          <div class="brand-mark">◉</div>
          <div>
            <div class="brand-name">ORCA</div>
            <div class="brand-subtitle">Research Studio</div>
          </div>
        </div>
        <div class="muted">Orchestrated Research and Cognition Agent</div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown('<div class="side-heading">The research loop</div>', unsafe_allow_html=True)
    for number, label in enumerate(
        ("Discover sources", "Read the signal", "Synthesize findings", "Challenge the draft"),
        start=1,
    ):
        st.markdown(
            f'<div class="workflow-step"><span class="step-number">{number:02}</span>'
            f'<span>{label}</span></div>',
            unsafe_allow_html=True,
        )
    st.divider()
    st.markdown('<div class="side-heading">Under the surface</div>', unsafe_allow_html=True)
    st.caption("Tavily finds the signal. Gemini turns it into a report and a second-pass critique.")
    st.caption(
        "Configure `TAVILY_API_KEY` and `GOOGLE_API_KEY` in your `.env` file."
    )

st.markdown(
    """
    <div class="hero">
      <div class="hero-topline"><span class="live-dot"></span>
        <span class="eyebrow">Orchestrated Research and Cognition Agent</span>
      </div>
      <h1>Follow the current.<br><span>Find the signal.</span></h1>
      <p class="hero-copy">Give ORCA a question. It will search, read, synthesize, then challenge its own findings—so you get more than a pile of links.</p>
      <div class="hero-foot">
        <span class="hero-tag">01 · Discover</span>
        <span class="hero-tag">02 · Read</span>
        <span class="hero-tag">03 · Synthesize</span>
        <span class="hero-tag">04 · Critique</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-label">Start an expedition</div>
    <div class="section-title">What are you curious about?</div>
    <div class="section-copy">Ask a focused question for a sharper, more useful report.</div>
    """,
    unsafe_allow_html=True,
)

if "topic_input" not in st.session_state:
    st.session_state["topic_input"] = ""

suggestion_columns = st.columns(3)
suggestions = (
    "How is AI changing drug discovery?",
    "What is the future of clean energy storage?",
    "Can small language models run on-device?",
)
for column, suggestion in zip(suggestion_columns, suggestions):
    column.button(
        suggestion,
        key=f"suggestion_{suggestion}",
        on_click=lambda value=suggestion: st.session_state.update(
            topic_input=value
        ),
        use_container_width=True,
    )

with st.form("research_form"):
    topic = st.text_area(
        "Your research question",
        key="topic_input",
        placeholder="For example: Will event-based vision replace large language models in the next five years?",
        height=110,
        max_chars=500,
    )
    submitted = st.form_submit_button(
        "Dive into the research  →",
        type="primary",
        use_container_width=True,
    )

if submitted:
    topic = topic.strip()
    if not topic:
        st.warning("Enter a research topic to get started.")
    elif not os.getenv("TAVILY_API_KEY") or not os.getenv("GOOGLE_API_KEY"):
        st.error(
            "API keys are missing. Set both `TAVILY_API_KEY` and `GOOGLE_API_KEY` "
            "in your `.env` file, then restart the app."
        )
    else:
        try:
            with st.status("Starting your research...", expanded=True) as status:
                result = run_research_pipeline(
                    topic,
                    progress_callback=status.write,
                )
                status.update(
                    label="Research complete",
                    state="complete",
                    expanded=False,
                )
            st.session_state["research_result"] = result
            st.session_state["research_topic"] = topic
        except Exception as exc:
            st.error(f"Research failed: {exc}")

result = st.session_state.get("research_result")
if result:
    st.markdown(
        f'<div class="section-label">Expedition complete</div>'
        f'<div class="result-heading">Your research brief</div>'
        f'<div class="result-topic">{html.escape(st.session_state["research_topic"])}</div>',
        unsafe_allow_html=True,
    )
    source_matches = list(
        re.finditer(
            r"Title:\s*(.*?)\s*\nURL:\s*(https?://\S+)",
            result["search_result"],
        )
    )
    metric_columns = st.columns(3)
    metric_columns[0].metric("Sources discovered", len(source_matches))
    metric_columns[1].metric("Deep reads", 1 if result["reader_result"] else 0)
    metric_columns[2].metric("Cognition passes", 2)

    report_tab, review_tab, sources_tab, research_tab = st.tabs(
        ["✦  Research brief", "◎  Critical review", "↗  Sources", "≋  Field notes"]
    )

    with report_tab:
        st.markdown(result["report"])
        report_download = (
            f"# Research report: {st.session_state['research_topic']}\n\n"
            f"{result['report']}\n"
        )
        st.download_button(
            "Download report",
            data=report_download,
            file_name="orca-research-report.md",
            mime="text/markdown",
        )

    with review_tab:
        st.markdown(result["feedback"])

    with sources_tab:
        if source_matches:
            for index, source in enumerate(source_matches, start=1):
                title = html.escape(source.group(1).strip() or source.group(2))
                url = html.escape(source.group(2), quote=True)
                st.markdown(
                    f'<div class="source-card"><div class="source-title">'
                    f'{index:02} &nbsp; {title}</div>'
                    f'<a class="source-url" href="{url}" target="_blank" '
                    f'rel="noopener noreferrer">{url}</a></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No source links were returned by the search.")

    with research_tab:
        with st.expander("Search results", expanded=True):
            st.text(result["search_result"])
        with st.expander("Scraped source notes"):
            st.text(result["reader_result"])
