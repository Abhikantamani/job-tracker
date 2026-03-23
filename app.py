import streamlit as st
import pandas as pd
import plotly.express as px
from database import create_table, add_job, get_all_jobs
from groq import Groq

create_table()

st.set_page_config(page_title="JobTrack", page_icon="◆", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #f8f9fa; }

    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: none;
    }

    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    section[data-testid="stSidebar"] .stTextInput input,
    section[data-testid="stSidebar"] .stSelectbox select,
    section[data-testid="stSidebar"] .stTextArea textarea {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        color: #fff !important;
        border-radius: 6px !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 12px !important;
        transition: all 0.2s ease !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #e0e0e0 !important;
        transform: translateY(-1px);
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e8e8e8;
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
        animation: fadeInUp 0.5s ease forwards;
        opacity: 0;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        transform: translateY(-3px);
    }

    .metric-icon { font-size: 1.4rem; margin-bottom: 10px; }

    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0a0a0a;
        line-height: 1;
    }

    .metric-label {
        font-size: 0.72rem;
        font-weight: 500;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 6px;
    }

    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .main-header {
        padding: 32px 0 28px 0;
        border-bottom: 1px solid #e8e8e8;
        margin-bottom: 36px;
        animation: slideInLeft 0.5s ease forwards;
    }

    .header-title {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0a0a0a;
        letter-spacing: -0.04em;
    }

    .header-sub {
        font-size: 0.85rem;
        color: #999;
        margin-top: 5px;
    }

    .section-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #0a0a0a;
        letter-spacing: -0.01em;
        margin-bottom: 14px;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .chart-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 16px;
        padding: 24px;
        animation: fadeInUp 0.6s ease forwards;
        opacity: 0;
        transition: box-shadow 0.2s ease;
    }

    .chart-card:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.06); }

    .ai-box {
        background: #0a0a0a;
        border-radius: 16px;
        padding: 32px;
        color: #e8e8e8;
        line-height: 1.9;
        font-size: 0.92rem;
        animation: fadeIn 0.6s ease forwards;
    }

    .ai-box strong { color: #ffffff; }

    .stButton button {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
    }

    .stButton button:hover {
        background-color: #333 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15) !important;
    }

    .sidebar-logo {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #fff;
        padding: 8px 0 24px 0;
        border-bottom: 1px solid #222;
        margin-bottom: 28px;
    }

    .empty-state {
        text-align: center;
        padding: 100px 0;
        color: #bbb;
        animation: fadeIn 0.5s ease;
    }

    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        animation: fadeInUp 0.6s ease forwards;
    }

    hr { border-color: #ececec !important; }

    /* ── AGENT STYLES ── */

    .agent-header-box {
        background: linear-gradient(135deg, #0a0a0a 0%, #1e3a5f 100%);
        border-radius: 20px;
        padding: 32px 36px;
        margin-bottom: 28px;
        color: white;
    }

    .agent-header-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .agent-header-sub {
        font-size: 0.88rem;
        color: rgba(255,255,255,0.65);
    }

    .agent-tag {
        display: inline-block;
        background: #22c55e;
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        margin-left: 12px;
        vertical-align: middle;
        letter-spacing: 0.08em;
    }

    .step-indicator {
        display: flex;
        gap: 10px;
        margin-bottom: 24px;
    }

    .step-dot {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .step-dot-active {
        background: #2563eb;
        color: white;
    }

    .step-dot-done {
        background: #22c55e;
        color: white;
    }

    .step-dot-pending {
        background: #e5e7eb;
        color: #9ca3af;
    }

    .step-label {
        font-size: 0.78rem;
        color: #6b7280;
        margin-top: 4px;
    }

    .agent-step {
        background: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }

    .agent-step-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 6px;
    }

    .agent-step-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0a0a0a;
        margin-bottom: 16px;
    }

    .question-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
        border-left: 4px solid #2563eb;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin-bottom: 8px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #1e3a5f;
        line-height: 1.5;
    }

    .question-number {
        display: inline-block;
        background: #2563eb;
        color: white;
        font-size: 0.72rem;
        font-weight: 700;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        text-align: center;
        line-height: 24px;
        margin-right: 10px;
    }

    .eval-card {
        background: #ffffff;
        border: 1.5px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .eval-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }

    .eval-value {
        font-size: 0.9rem;
        color: #1f2937;
        line-height: 1.7;
    }

    .strength-card {
        background: #f0fdf4;
        border: 1.5px solid #86efac;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 14px;
    }

    .strength-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #16a34a;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }

    .improve-card {
        background: #fffbeb;
        border: 1.5px solid #fcd34d;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 14px;
    }

    .improve-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #d97706;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }

    .tip-card {
        background: #eff6ff;
        border: 1.5px solid #bfdbfe;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 14px;
    }

    .tip-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }

    .score-pill {
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 5px 16px;
        border-radius: 20px;
        margin-top: 10px;
        color: white;
    }

    .score-high { background: #16a34a; }
    .score-mid  { background: #d97706; }
    .score-low  { background: #dc2626; }

    .overall-score-box {
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        color: #fff;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }

    .overall-score-number {
        font-size: 5rem;
        font-weight: 800;
        line-height: 1;
    }

    .next-steps-box {
        background: #0f172a;
        border-radius: 16px;
        padding: 24px 28px;
        color: #e2e8f0;
        margin-top: 4px;
        line-height: 1.8;
        font-size: 0.9rem;
    }

    .next-steps-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="header-title">JobTrack</div>
    <div class="header-sub">Your personal job search command center</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-logo">JobTrack</div>', unsafe_allow_html=True)
    st.markdown("### Add Application")
    company = st.text_input("Company")
    role = st.text_input("Role")
    status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
    date_applied = st.date_input("Date Applied")
    notes = st.text_area("Notes")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Add Job"):
        if company and role:
            add_job(company, role, status, str(date_applied), notes)
            st.success("Added successfully!")
        else:
            st.error("Fill in Company and Role.")

# TABS
tab1, tab2 = st.tabs(["Dashboard", "Interview Prep Agent"])

# ==============================================================================
# TAB 1 - DASHBOARD
# ==============================================================================
with tab1:
    jobs = get_all_jobs()

    if jobs:
        df = pd.DataFrame(jobs, columns=["ID", "Company", "Role", "Status", "Date Applied", "Notes"])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-icon">📋</div>
                <div class="metric-number">{len(df)}</div>
                <div class="metric-label">Total Applied</div>
            </div>''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-icon">🤝</div>
                <div class="metric-number">{len(df[df["Status"] == "Interview"])}</div>
                <div class="metric-label">Interviews</div>
            </div>''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-number">{len(df[df["Status"] == "Offer"])}</div>
                <div class="metric-label">Offers</div>
            </div>''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-icon">❌</div>
                <div class="metric-number">{len(df[df["Status"] == "Rejected"])}</div>
                <div class="metric-label">Rejected</div>
            </div>''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Status Breakdown</div>', unsafe_allow_html=True)
            status_counts = df["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            fig = px.pie(status_counts, names="Status", values="Count", hole=0.6,
                         color_discrete_sequence=["#0a0a0a", "#404040", "#808080", "#c0c0c0"])
            fig.update_layout(
                paper_bgcolor="white", plot_bgcolor="white",
                font_family="Inter", margin=dict(t=10, b=10, l=10, r=10),
                showlegend=True, legend=dict(orientation="h", y=-0.1)
            )
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Applications Over Time</div>', unsafe_allow_html=True)
            df["Date Applied"] = pd.to_datetime(df["Date Applied"])
            timeline = df.groupby("Date Applied").size().reset_index(name="Count")
            fig2 = px.bar(timeline, x="Date Applied", y="Count",
                          color_discrete_sequence=["#0a0a0a"])
            fig2.update_layout(
                paper_bgcolor="white", plot_bgcolor="white",
                font_family="Inter", margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#f0f0f0")
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">All Applications</div>', unsafe_allow_html=True)
        st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI Insights</div>', unsafe_allow_html=True)

        if st.button("Generate Insights"):
            with st.spinner("Analysing your job search..."):
                summary = df[["Company", "Role", "Status", "Date Applied"]].to_string(index=False)
                client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
                message = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "user",
                        "content": f"""You are a helpful career coach. Analyse this job application data and give friendly, specific advice:

{summary}

Please provide:
1. A brief summary of the job search so far
2. What's going well
3. What could be improved
4. 2-3 specific actionable tips

Keep it encouraging and concise."""
                    }]
                )
                result = message.choices[0].message.content
                st.markdown(f'<div class="ai-box">{result}</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size: 2.5rem; margin-bottom: 16px;">◆</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #555;">No applications yet</div>
            <div style="font-size: 0.85rem; margin-top: 8px; color: #aaa;">Add your first job from the sidebar to get started</div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2 - INTERVIEW PREP AGENT
# ==============================================================================
with tab2:

    # Hero header
    st.markdown("""
    <div class="agent-header-box">
        <div class="agent-header-title">
            Interview Prep Agent
            <span class="agent-tag">AGENTIC AI</span>
        </div>
        <div class="agent-header-sub">
            Paste a job description &rarr; Agent generates 5 targeted questions &rarr; You answer &rarr; Agent scores and coaches you
        </div>
    </div>
    """, unsafe_allow_html=True)

    # State init
    if "agent_stage" not in st.session_state:
        st.session_state.agent_stage = "input"
    if "agent_questions" not in st.session_state:
        st.session_state.agent_questions = []
    if "agent_answers" not in st.session_state:
        st.session_state.agent_answers = {}
    if "agent_evaluations" not in st.session_state:
        st.session_state.agent_evaluations = []
    if "agent_overall" not in st.session_state:
        st.session_state.agent_overall = ""
    if "agent_jd" not in st.session_state:
        st.session_state.agent_jd = ""
    if "agent_role" not in st.session_state:
        st.session_state.agent_role = ""

    client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))

    # Step indicator
    stage_map = {"input": 1, "answering": 2, "results": 3}
    current = stage_map.get(st.session_state.agent_stage, 1)

    def dot(n, label):
        cls = "step-dot-active" if n == current else "step-dot-done" if n < current else "step-dot-pending"
        return f'<div style="text-align:center"><div class="step-dot {cls}">{n}</div><div class="step-label">{label}</div></div>'

    st.markdown(f"""
    <div style="display:flex; gap:20px; align-items:flex-start; margin-bottom:28px;">
        {dot(1, "Job Details")}
        <div style="flex:1; height:2px; background:#e5e7eb; margin-top:16px;"></div>
        {dot(2, "Your Answers")}
        <div style="flex:1; height:2px; background:#e5e7eb; margin-top:16px;"></div>
        {dot(3, "Results")}
    </div>
    """, unsafe_allow_html=True)

    # ── STAGE 1: Input ────────────────────────────────────────────────────────
    if st.session_state.agent_stage == "input":

        st.markdown('<div class="agent-step">', unsafe_allow_html=True)
        st.markdown('<div class="agent-step-header">Step 1 of 3 - Paste the Job Description</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-step-title">What role are you interviewing for?</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        role_input = st.text_input("Role / Position Title", placeholder="e.g. AI Innovation Associate Intern")
        jd_input = st.text_area("Job Description", placeholder="Paste the full job description here...", height=240)

        col_btn, col_hint = st.columns([1, 3])
        with col_btn:
            generate_btn = st.button("Analyse and Generate Questions")
        with col_hint:
            st.markdown(
                "<div style='padding-top:10px; font-size:0.82rem; color:#6b7280;'>"
                "The agent will read the JD and craft 5 role-specific questions.</div>",
                unsafe_allow_html=True
            )

        if generate_btn:
            if not jd_input.strip():
                st.error("Please paste a job description first.")
            else:
                with st.spinner("Agent is reading the JD and crafting questions..."):
                    resp = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{
                            "role": "user",
                            "content": f"""You are an expert technical interviewer.
Read this job description carefully and generate exactly 5 interview questions specific to this role.

Mix:
- 2 technical/skills questions from the JD requirements
- 1 behavioural question
- 1 situational/problem-solving question
- 1 motivation/fit question

Job Title: {role_input}
Job Description:
{jd_input}

Return ONLY a numbered list of 5 questions. No preamble.
Format:
1. [question]
2. [question]
3. [question]
4. [question]
5. [question]"""
                        }]
                    )
                    raw = resp.choices[0].message.content.strip()
                    questions = []
                    for line in raw.split("\n"):
                        line = line.strip()
                        if line and line[0].isdigit() and "." in line:
                            q = line.split(".", 1)[1].strip()
                            if q:
                                questions.append(q)
                    if len(questions) < 3:
                        questions = [l.strip() for l in raw.split("\n") if len(l.strip()) > 20][:5]

                    st.session_state.agent_questions = questions
                    st.session_state.agent_jd = jd_input
                    st.session_state.agent_role = role_input
                    st.session_state.agent_stage = "answering"
                    st.rerun()

    # ── STAGE 2: Answer Questions ─────────────────────────────────────────────
    elif st.session_state.agent_stage == "answering":

        st.markdown('<div class="agent-step">', unsafe_allow_html=True)
        st.markdown('<div class="agent-step-header">Step 2 of 3 - Answer Each Question</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="agent-step-title">5 Questions for: {st.session_state.agent_role or "the role"}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='font-size:0.85rem; color:#6b7280; margin-bottom:20px;'>"
            "Answer as you would in a real interview. The agent evaluates each answer individually.</div>",
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        answers = {}
        for i, question in enumerate(st.session_state.agent_questions, 1):
            st.markdown(
                f'<div class="question-card"><span class="question-number">{i}</span>{question}</div>',
                unsafe_allow_html=True
            )
            ans = st.text_area(
                f"Answer {i}",
                key=f"ans_{i}",
                placeholder="Type your answer here...",
                height=110,
                label_visibility="collapsed"
            )
            answers[i] = ans
            st.markdown("<br>", unsafe_allow_html=True)

        col_back, col_submit = st.columns([1, 2])
        with col_back:
            if st.button("Start Over"):
                for key in ["agent_stage", "agent_questions", "agent_answers",
                            "agent_evaluations", "agent_overall", "agent_jd", "agent_role"]:
                    del st.session_state[key]
                st.rerun()
        with col_submit:
            submit_btn = st.button("Submit Answers for Evaluation")

        if submit_btn:
            unanswered = [i for i, a in answers.items() if not a.strip()]
            if unanswered:
                st.warning(f"Please answer all questions. Missing: Q{', Q'.join(map(str, unanswered))}")
            else:
                st.session_state.agent_answers = answers
                evaluations = []
                progress = st.progress(0, text="Agent evaluating your answers...")

                for i, question in enumerate(st.session_state.agent_questions, 1):
                    progress.progress(
                        i / len(st.session_state.agent_questions),
                        text=f"Evaluating answer {i} of {len(st.session_state.agent_questions)}..."
                    )
                    eval_resp = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{
                            "role": "user",
                            "content": f"""You are a senior interviewer evaluating a candidate's answer.

Job Role: {st.session_state.agent_role}
Interview Question: {question}
Candidate's Answer: {answers[i]}

Respond in this exact format:
SCORE: [number from 1-10]
STRENGTH: [one sentence on what was good]
IMPROVEMENT: [one specific actionable suggestion]
TIP: [one quick tip to make this answer stronger]"""
                        }]
                    )
                    evaluations.append({
                        "question": question,
                        "answer": answers[i],
                        "evaluation": eval_resp.choices[0].message.content.strip()
                    })

                progress.progress(1.0, text="Generating overall assessment...")

                all_qa = "\n\n".join([
                    f"Q: {e['question']}\nA: {e['answer']}\nEval: {e['evaluation']}"
                    for e in evaluations
                ])
                overall_resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{
                        "role": "user",
                        "content": f"""You are a senior hiring manager. Review this candidate's complete interview performance.

Role: {st.session_state.agent_role}

Full Q&A with evaluations:
{all_qa}

Provide final assessment in this exact format:
OVERALL_SCORE: [number from 1-100]
VERDICT: [one sentence summary]
TOP_STRENGTH: [candidate's biggest strength]
CRITICAL_GAP: [most important thing to work on]
NEXT_STEPS: [2-3 specific action items before the real interview]"""
                    }]
                )

                st.session_state.agent_evaluations = evaluations
                st.session_state.agent_overall = overall_resp.choices[0].message.content.strip()
                st.session_state.agent_stage = "results"
                progress.empty()
                st.rerun()

    # ── STAGE 3: Results ──────────────────────────────────────────────────────
    elif st.session_state.agent_stage == "results":

        overall_text = st.session_state.agent_overall
        overall_score = 0
        for line in overall_text.split("\n"):
            if line.startswith("OVERALL_SCORE:"):
                try:
                    overall_score = int(line.split(":")[1].strip().split()[0])
                except:
                    overall_score = 0

        score_color = (
            "linear-gradient(135deg, #166534 0%, #15803d 100%)" if overall_score >= 70
            else "linear-gradient(135deg, #92400e 0%, #b45309 100%)" if overall_score >= 45
            else "linear-gradient(135deg, #991b1b 0%, #b91c1c 100%)"
        )
        score_label = (
            "Interview Ready" if overall_score >= 70
            else "Getting There" if overall_score >= 45
            else "Needs Practice"
        )

        st.markdown(f"""
        <div class="overall-score-box" style="background: {score_color};">
            <div style="font-size:0.82rem; color:rgba(255,255,255,0.65); text-transform:uppercase;
                        letter-spacing:0.12em; margin-bottom:12px;">Overall Readiness Score</div>
            <div class="overall-score-number">{overall_score}<span style="font-size:2.2rem; font-weight:400;">/100</span></div>
            <div style="font-size:1.1rem; font-weight:600; margin-top:14px; color:rgba(255,255,255,0.9);">
                {score_label}
            </div>
        </div>
        """, unsafe_allow_html=True)

        overall_lines = {}
        for line in overall_text.split("\n"):
            if ":" in line and not line.startswith("OVERALL_SCORE"):
                k, v = line.split(":", 1)
                overall_lines[k.strip()] = v.strip()

        if overall_lines:
            cols = st.columns(3)
            card_configs = [
                ("TOP_STRENGTH", "Top Strength",  "strength-card", "strength-label", cols[0]),
                ("CRITICAL_GAP", "Critical Gap",  "improve-card",  "improve-label",  cols[1]),
                ("VERDICT",      "Verdict",        "tip-card",      "tip-label",      cols[2]),
            ]
            for key, label, card_cls, lbl_cls, col in card_configs:
                val = overall_lines.get(key, "")
                if val:
                    with col:
                        st.markdown(f"""
                        <div class="{card_cls}">
                            <div class="{lbl_cls}">{label}</div>
                            <div class="eval-value">{val}</div>
                        </div>""", unsafe_allow_html=True)

            next_steps = overall_lines.get("NEXT_STEPS", "")
            if next_steps:
                st.markdown(f"""
                <div class="next-steps-box">
                    <div class="next-steps-label">Next Steps Before the Interview</div>
                    {next_steps}
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Question-by-Question Breakdown</div>', unsafe_allow_html=True)

        for i, item in enumerate(st.session_state.agent_evaluations, 1):
            eval_text = item["evaluation"]
            eval_lines = {}
            for line in eval_text.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    eval_lines[k.strip()] = v.strip()

            q_score = 0
            try:
                q_score = int(eval_lines.get("SCORE", "0").split("/")[0].split()[0])
            except:
                q_score = 0

            badge_class = "score-high" if q_score >= 7 else "score-mid" if q_score >= 4 else "score-low"

            with st.expander(f"Q{i}  —  {item['question'][:75]}{'...' if len(item['question']) > 75 else ''}"):
                st.markdown(f"""
                <div class="eval-card">
                    <div class="eval-label">Your Answer</div>
                    <div class="eval-value" style="font-style:italic;">"{item['answer']}"</div>
                    <span class="score-pill {badge_class}">{q_score} / 10</span>
                </div>
                """, unsafe_allow_html=True)

                row1, row2, row3 = st.columns(3)
                for col, key, card_cls, lbl_cls, label in [
                    (row1, "STRENGTH",    "strength-card", "strength-label", "Strength"),
                    (row2, "IMPROVEMENT", "improve-card",  "improve-label",  "Improvement"),
                    (row3, "TIP",         "tip-card",      "tip-label",      "Quick Tip"),
                ]:
                    val = eval_lines.get(key, "")
                    if val:
                        with col:
                            st.markdown(f"""
                            <div class="{card_cls}">
                                <div class="{lbl_cls}">{label}</div>
                                <div class="eval-value">{val}</div>
                            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Try a Different Job Description"):
                for key in ["agent_stage", "agent_questions", "agent_answers",
                            "agent_evaluations", "agent_overall", "agent_jd", "agent_role"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        with col2:
            if st.button("Re-attempt Same Questions"):
                st.session_state.agent_stage = "answering"
                st.session_state.agent_answers = {}
                st.session_state.agent_evaluations = []
                st.session_state.agent_overall = ""
                st.rerun()