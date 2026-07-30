import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, play_sound, get_vulnerability_data

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("scan"), height=0)

st.markdown('<div class="main-header">🛡️ VULNERABILITY SCANNER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">CVE Tracking, Patch Management & Risk Assessment</div>', unsafe_allow_html=True)

st.subheader("🔍 Scan Configuration")
c1, c2, c3 = st.columns(3)
with c1:
    scan_target = st.selectbox("Target", ["Full Network","Web Servers","DB Servers","Workstations","DMZ"])
    scan_type = st.selectbox("Scan Type", ["Comprehensive","Quick","Stealth","Compliance"])
with c2:
    scan_ports = st.text_input("Port Range", "1-65535")
    scan_threads = st.slider("Threads", 10, 200, 50)
with c3:
    include_cve = st.checkbox("CVE Database Lookup", value=True)
    include_exploit = st.checkbox("Exploit DB Check", value=True)
    schedule = st.checkbox("Schedule Recurring Scan", value=False)

if st.button("🔍 Start Vulnerability Scan", type="primary", use_container_width=True):
    st.components.v1.html(play_sound("scan"), height=0)
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.03)
        bar.progress(i + 1, text=f"Scanning {scan_target}... {i+1}%")
    bar.empty()
    st.success(f"Scan complete! Found 8 vulnerabilities on {scan_target}.")

st.markdown("---")
st.subheader("📋 Discovered Vulnerabilities")
vulns = get_vulnerability_data()
df_vulns = pd.DataFrame(vulns)

def color_severity(val):
    return {"CRITICAL":"background:linear-gradient(90deg,#450a0a,#7f1d1d);color:#fecaca;font-weight:700;border-left:3px solid #ff2a6d",
            "HIGH":"background:linear-gradient(90deg,#451a03,#713f12);color:#fde68a;font-weight:600;border-left:3px solid #ffae00",
            "MEDIUM":"background:linear-gradient(90deg,#1a2e05,#3f6212);color:#d9f99d;font-weight:500;border-left:3px solid #00f0ff",
            "LOW":"background:linear-gradient(90deg,#022c22,#064e3b);color:#a7f3d0;font-weight:500;border-left:3px solid #05ffa1"}.get(val,"")

def color_status(val):
    return {"Unpatched":"color:#ff2a6d;font-weight:600","Patch Available":"color:#ffae00;font-weight:600","Patched":"color:#05ffa1;font-weight:600"}.get(val,"")

st.dataframe(df_vulns.style.map(color_severity, subset=["severity"]).map(color_status, subset=["status"]),
             use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("📊 Risk Assessment Summary")
r1, r2, r3, r4 = st.columns(4)
for col, label, color in [(r1,"CRITICAL","#ff2a6d"),(r2,"HIGH","#ffae00"),(r3,"MEDIUM","#00f0ff"),(r4,"LOW","#05ffa1")]:
    count = df_vulns[df_vulns["severity"] == label].shape[0]
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color};">{count}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 CVSS Score Distribution")
    fig = go.Figure(go.Bar(x=df_vulns["id"], y=df_vulns["cvss"],
                           marker_color=["#ff2a6d" if s>=9 else "#ffae00" if s>=7 else "#00f0ff" if s>=4 else "#05ffa1" for s in df_vulns["cvss"]],
                           marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1))
    fig.add_hline(y=9, line_dash="dash", line_color="#ff2a6d", annotation_text="Critical")
    fig.add_hline(y=7, line_dash="dash", line_color="#ffae00", annotation_text="High")
    fig.update_layout(template="plotly_dark", height=380, xaxis_title="CVE ID", yaxis_title="CVSS Score",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                      margin=dict(l=40,r=40,t=40,b=40), font=dict(family="JetBrains Mono", size=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("📊 Patch Status")
    status_counts = df_vulns["status"].value_counts()
    fig = go.Figure(go.Pie(labels=status_counts.index, values=status_counts.values, hole=0.55,
                           marker=dict(colors=["#ff2a6d","#ffae00","#05ffa1"], line=dict(color="#050814", width=2))))
    fig.update_traces(textinfo="percent+label", textfont_size=12, textfont_color="#e2e8f0")
    fig.update_layout(template="plotly_dark", height=380, showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=20,b=20),
                      font=dict(family="JetBrains Mono", size=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🔧 Remediation Priority Queue")
for _, vuln in df_vulns.sort_values("cvss", ascending=False).iterrows():
    severity_color = {"CRITICAL":"#ff2a6d","HIGH":"#ffae00","MEDIUM":"#00f0ff","LOW":"#05ffa1"}.get(vuln["severity"],"#fff")
    status_color = {"Unpatched":"#ff2a6d","Patch Available":"#ffae00","Patched":"#05ffa1"}.get(vuln["status"],"#fff")
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,rgba(5,8,20,0.7),rgba(15,20,45,0.5));
                padding:12px 16px;border-radius:10px;margin:4px 0;border-left:3px solid {severity_color};">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div><span style="color:{severity_color};font-weight:700;font-family:'JetBrains Mono';">{vuln['id']}</span>
            <span style="color:#e2e8f0;margin-left:8px;">{vuln['service']}</span>
            <span style="color:#475569;font-size:0.8rem;margin-left:8px;">— {vuln['description']}</span></div>
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="color:{severity_color};font-weight:700;font-family:'JetBrains Mono';">CVSS: {vuln['cvss']}</span>
                <span style="color:{status_color};font-size:0.75rem;font-weight:600;">● {vuln['status']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("🛡️ Sentinel AI v6.2.0 — Vulnerability Scanner | CVE Database Updated")