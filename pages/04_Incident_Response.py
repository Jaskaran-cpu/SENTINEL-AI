import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, play_sound

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("alarm"), height=0)

st.markdown('<div class="main-header">🚨 INCIDENT RESPONSE CENTER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Alert Triage, Auto-Playbooks & MTTR Analytics</div>', unsafe_allow_html=True)

alerts = pd.DataFrame({
    "ID": [f"ALT-2024-{str(i).zfill(3)}" for i in range(1,9)],
    "Timestamp": ["2024-01-15 14:32:15","2024-01-15 14:28:03","2024-01-15 14:15:44",
                  "2024-01-15 13:52:11","2024-01-15 13:30:00","2024-01-15 12:45:22",
                  "2024-01-15 11:20:10","2024-01-15 10:55:33"],
    "Severity": ["CRITICAL","HIGH","MEDIUM","HIGH","CRITICAL","HIGH","MEDIUM","CRITICAL"],
    "Type": ["DDoS","Port Scan","Brute Force","Botnet","Infiltration","SQL Injection","XSS","Ransomware"],
    "Source IP": ["45.23.112.8","103.45.67.12","78.192.45.3","91.234.56.78",
                  "185.67.89.12","203.112.45.67","198.51.100.42","192.168.77.5"],
    "Target": ["Web Server","Firewall","SSH Server","Workstation A","DB Server","App Server","Web Server","File Server"],
    "Status": ["Active","Mitigated","Investigating","Active","Contained","Mitigated","Investigating","Active"],
    "Confidence": ["99.1%","94.3%","91.7%","96.2%","98.8%","93.5%","89.2%","97.4%"],
})

def color_severity(val):
    return {"CRITICAL":"background:linear-gradient(90deg,#450a0a,#7f1d1d);color:#fecaca;font-weight:700;border-left:3px solid #ff2a6d",
            "HIGH":"background:linear-gradient(90deg,#451a03,#713f12);color:#fde68a;font-weight:600;border-left:3px solid #ffae00",
            "MEDIUM":"background:linear-gradient(90deg,#1a2e05,#3f6212);color:#d9f99d;font-weight:500;border-left:3px solid #00f0ff",
            "LOW":"background:linear-gradient(90deg,#022c22,#064e3b);color:#a7f3d0;font-weight:500;border-left:3px solid #05ffa1"}.get(val,"")

def color_status(val):
    return {"Active":"color:#ff2a6d;font-weight:600","Mitigated":"color:#05ffa1;font-weight:600",
            "Investigating":"color:#ffae00;font-weight:600","Contained":"color:#00f0ff;font-weight:600"}.get(val,"")

st.subheader("📋 Active Alerts")
st.dataframe(alerts.style.map(color_severity, subset=["Severity"]).map(color_status, subset=["Status"]),
             use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("🔍 Alert Filters")
f1, f2, f3 = st.columns(3)
with f1: severity_filter = st.multiselect("Severity", ["CRITICAL","HIGH","MEDIUM","LOW"], default=["CRITICAL","HIGH"])
with f2: status_filter = st.multiselect("Status", ["Active","Mitigated","Investigating","Contained"], default=["Active"])
with f3: type_filter = st.multiselect("Attack Type", alerts["Type"].unique().tolist(), default=alerts["Type"].unique().tolist())

filtered = alerts[alerts["Severity"].isin(severity_filter) & alerts["Status"].isin(status_filter) & alerts["Type"].isin(type_filter)]
st.info(f"Showing {len(filtered)} of {len(alerts)} alerts matching filters")
st.dataframe(filtered.style.map(color_severity, subset=["Severity"]).map(color_status, subset=["Status"]),
             use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("📖 Auto-Generated Response Playbooks")
playbook_tabs = st.tabs(["DDoS Response","Port Scan","Brute Force","Ransomware","General Guidelines"])

playbooks = [
    (0, "#ff2a6d", "DDoS Attack Response Playbook (ALT-2024-001)", [
        ("IMMEDIATE (0-5 min)", "#ff2a6d", "• Activate DDoS mitigation service (Cloudflare / AWS Shield)<br>• Rate-limit traffic from 45.23.112.0/24<br>• Enable SYN cookies on firewall<br>• Alert on-call security engineer"),
        ("CONTAINMENT (5-15 min)", "#ffae00", "• Blackhole attack traffic at edge router<br>• Scale up CDN / cache layer<br>• Enable CAPTCHA challenge for suspicious IPs"),
        ("INVESTIGATION (15-60 min)", "#00f0ff", "• Analyze attack pattern (volumetric vs application layer)<br>• Check for secondary attacks (distraction technique)<br>• Review logs for initial access vector")]),
    (1, "#ffae00", "Port Scan Response Playbook (ALT-2024-002)", [
        ("IMMEDIATE", "#ffae00", "• Log all scan attempts for forensics<br>• Check if any ports responded unexpectedly<br>• Verify firewall rules are active"),
        ("CONTAINMENT", "#00f0ff", "• Temporarily block source IP if repeated<br>• Enable port scan detection on IDS<br>• Review exposed services")]),
    (2, "#00f0ff", "Brute Force Response Playbook (ALT-2024-003)", [
        ("IMMEDIATE", "#00f0ff", "• Block source IP after 5 failed attempts<br>• Enable account lockout policy<br>• Force password reset for targeted accounts"),
        ("CONTAINMENT", "#05ffa1", "• Review authentication logs<br>• Implement 2FA for all admin accounts<br>• Deploy fail2ban or equivalent")]),
    (3, "#b829dd", "Ransomware Response Playbook (ALT-2024-008)", [
        ("IMMEDIATE (0-10 min)", "#b829dd", "• ISOLATE infected systems from network immediately<br>• Disable remote access and VPN connections<br>• Preserve forensic evidence (do not reboot)<br>• Alert CISO and legal team"),
        ("CONTAINMENT (10-30 min)", "#ff2a6d", "• Identify encryption method and IOCs<br>• Check backup integrity (air-gapped)<br>• Block known C2 domains at DNS level"),
        ("RECOVERY", "#ffae00", "• Restore from clean backups (DO NOT PAY)<br>• Rebuild affected systems from golden image<br>• Deploy EDR with ransomware behavioral detection")]),
    (4, "#05ffa1", "General Incident Response Guidelines", [
        ("NIST Framework", "#00f0ff", "1. <b>Identify</b> — Confirm the threat and assess scope<br>2. <b>Contain</b> — Limit damage and isolate affected systems<br>3. <b>Eradicate</b> — Remove threat actor access and malware<br>4. <b>Recover</b> — Restore systems to normal operation<br>5. <b>Learn</b> — Document lessons and update procedures")]),
]

for tab_idx, color, title, steps in playbooks:
    with playbook_tabs[tab_idx]:
        steps_html = ""
        for step_name, step_color, step_text in steps:
            steps_html += f'<div style="margin-top:12px;"><strong style="color:{step_color};">{step_name}</strong><br><div style="color:#94a3b8;line-height:1.8;margin-top:4px;">{step_text}</div></div>'
        st.markdown(f'<div style="border-left:3px solid {color};padding-left:16px;"><h4 style="color:{color};">{title}</h4>{steps_html}</div>', unsafe_allow_html=True)

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Alert Severity Distribution")
    severity_counts = alerts["Severity"].value_counts()
    fig = px.pie(values=severity_counts.values, names=severity_counts.index, color=severity_counts.index,
                 color_discrete_map={"CRITICAL":"#ff2a6d","HIGH":"#ffae00","MEDIUM":"#00f0ff","LOW":"#05ffa1"},
                 hole=0.55, template="plotly_dark")
    fig.update_traces(textinfo="percent+label", textfont_size=12, textfont_color="#e2e8f0")
    fig.update_layout(height=380, showlegend=False, margin=dict(l=20,r=20,t=40,b=20),
                      paper_bgcolor="rgba(0,0,0,0)", font=dict(family="JetBrains Mono", size=10))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("⏱️ Mean Time to Response (MTTR)")
    mttr_data = {"DDoS":4.2,"Port Scan":12.5,"Brute Force":18.3,"Botnet":8.7,
                 "Infiltration":25.1,"SQL Injection":15.4,"XSS":10.2,"Ransomware":32.8}
    colors_bar = ["#ff2a6d" if v>20 else "#ffae00" if v>10 else "#05ffa1" for v in mttr_data.values()]
    fig = go.Figure(go.Bar(x=list(mttr_data.keys()), y=list(mttr_data.values()),
                           marker_color=colors_bar, marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1))
    fig.update_layout(template="plotly_dark", height=380, xaxis_title="Attack Type", yaxis_title="Minutes",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                      margin=dict(l=20,r=20,t=40,b=20), font=dict(family="JetBrains Mono", size=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("✅ SLA Compliance This Month")
sla1, sla2, sla3, sla4 = st.columns(4)
for col, label, pct, detail, color in [
    (sla1, "MTTD SLA (<5 min)", "94.2%", "6 / 8 critical", "#05ffa1"),
    (sla2, "MTTR SLA (<15 min)", "87.5%", "7 / 8 critical", "#ffae00"),
    (sla3, "Containment SLA (<30 min)", "100%", "8 / 8 critical", "#05ffa1"),
    (sla4, "Escalation SLA (<10 min)", "75.0%", "6 / 8 critical", "#ff2a6d"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:{color};font-size:1.5rem;">{pct}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-delta" style="color:{color};">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("🛡️ Sentinel AI v6.2.0 — Incident Response Center | Auto-Playbook Engine Active")