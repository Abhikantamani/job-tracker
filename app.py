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
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

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

    .metric-icon {
        font-size: 1.4rem;
        margin-bottom: 10px;
    }

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

    .section-title i {
        color: #555;
        font-size: 0.85rem;
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

    .chart-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    }

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

    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
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
</style>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="header-title">◆ JobTrack</div>
    <div class="header-sub">Your personal job search command center</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-logo">◆ JobTrack</div>', unsafe_allow_html=True)
    st.markdown("### Add Application")
    company = st.text_input("🏢 Company")
    role = st.text_input("💼 Role")
    status = st.selectbox("📌 Status", ["Applied", "Interview", "Offer", "Rejected"])
    date_applied = st.date_input("📅 Date Applied")
    notes = st.text_area("📝 Notes")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("＋ Add Job"):
        if company and role:
            add_job(company, role, status, str(date_applied), notes)
            st.success("✅ Added successfully!")
        else:
            st.error("⚠️ Fill in Company and Role.")

# Load data
jobs = get_all_jobs()

if jobs:
    df = pd.DataFrame(jobs, columns=["ID", "Company", "Role", "Status", "Date Applied", "Notes"])

    # Metrics
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

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Status Breakdown</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="section-title">📈 Applications Over Time</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-title">📁 All Applications</div>', unsafe_allow_html=True)
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🤖 AI Insights</div>', unsafe_allow_html=True)

    if st.button("✨ Generate Insights"):
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