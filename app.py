"""Sentinel AI — Home dashboard for the complete 11-screen workspace."""
import streamlit as st

st.set_page_config(page_title="Sentinel AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top left, #10213b, #070b14 50%); }
[data-testid="stSidebar"] { background:#0b1220; }
.hero { padding: 3rem 0 2rem; text-align:center; }
.hero h1 { font-size:4rem; margin:0; background:linear-gradient(90deg,#22d3ee,#a78bfa,#34d399); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.hero p { color:#aebdd2; font-size:1.1rem; }
.module { min-height:124px; padding:1.1rem; border-radius:14px; border:1px solid rgba(148,163,184,.16); background:rgba(15,23,42,.82); }
.module h3 { color:#67e8f9; margin:0 0 .55rem; }.module p { color:#aebdd2; margin:0; }
</style>
<div class="hero"><h1>🛡️ Sentinel AI</h1><p>Neural Cyber Threat Intelligence Platform · Full Security Operations Workspace</p></div>
""", unsafe_allow_html=True)

for col, (name, value, note) in zip(st.columns(4), [
    ("Active flows", "12,209", "Real-time monitoring"),
    ("Detection accuracy", "99.3%", "AI model confidence"),
    ("Active threats", "5", "Prioritized alerts"),
    ("Blocked IPs", "1,232", "Last 24 hours"),
]):
    col.metric(name, value, note)

st.markdown("### Security workspaces")
modules = [
    ("🏠", "Command Center", "Live security monitoring and KPI overview."),
    ("🌍", "Threat Map", "Geographic threat intelligence and activity mapping."),
    ("🚨", "Incident Response", "Alert triage, containment, and remediation."),
    ("🤖", "AI Model Lab", "Model comparison, training, and evaluation."),
    ("🔍", "Packet Inspector", "Deep packet-level investigation."),
    ("📈", "Predictive Analytics", "Forecasting and anomaly prediction."),
    ("⚙️", "MLOps Settings", "Model operations and configuration."),
    ("📡", "Network Analyzer", "Vulnerability and network posture analysis."),
    ("📋", "Compliance", "Framework gap analysis and reporting."),
    ("📄", "Executive Report", "Leadership-ready security report."),
]
for start in range(0, len(modules), 2):
    columns = st.columns(2)
    for col, (icon, name, text) in zip(columns, modules[start:start+2]):
        col.markdown(f"<div class='module'><h3>{icon} {name}</h3><p>{text}</p></div>", unsafe_allow_html=True)

st.success("All 18 original modules are available from the sidebar, including the Classic ML Suite. Together with this home dashboard, the project contains 19 visible screens.")
