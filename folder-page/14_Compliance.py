import streamlit as st
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, play_sound, get_compliance_data

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("click"), height=0)

st.markdown('<div class="main-header">📋 COMPLIANCE DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Framework Audit, Gap Analysis & Regulatory Reporting</div>', unsafe_allow_html=True)

compliance = get_compliance_data()

# Overall compliance score
total_score = sum(v["score"] for framework in compliance.values() for v in framework.values())
total_items = sum(len(framework) for framework in compliance.values())
overall_pct = total_score / total_items

s1, s2, s3, s4 = st.columns(4)
with s1:
    color = "#05ffa1" if overall_pct >= 85 else "#ffae00" if overall_pct >= 70 else "#ff2a6d"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{color};">{overall_pct:.1f}%</div>
        <div class="metric-label">Overall Compliance</div>
        <div class="metric-delta" style="color:{color};">Across all frameworks</div>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#05ffa1;">{sum(1 for f in compliance.values() for v in f.values() if v['status']=='Compliant')}</div>
        <div class="metric-label">Compliant Controls</div>
    </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#ffae00;">{sum(1 for f in compliance.values() for v in f.values() if v['status']=='Partial')}</div>
        <div class="metric-label">Partial Controls</div>
    </div>
    """, unsafe_allow_html=True)
with s4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#ff2a6d;">{sum(1 for f in compliance.values() for v in f.values() if v['status']=='Non-Compliant')}</div>
        <div class="metric-label">Non-Compliant</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Framework tabs
st.subheader("📊 Framework Compliance Details")
framework_tabs = st.tabs(list(compliance.keys()))

for i, (framework, controls) in enumerate(compliance.items()):
    with framework_tabs[i]:
        c1, c2 = st.columns([1.2, 1])

        with c1:
            for control_name, data in controls.items():
                score = data["score"]
                status = data["status"]
                color = "#05ffa1" if status == "Compliant" else "#ffae00" if status == "Partial" else "#ff2a6d"
                r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
                st.markdown(f"""
                <div style="background:linear-gradient(90deg,rgba(5,8,20,0.6),rgba(15,20,45,0.4));
                            padding:12px 16px;border-radius:10px;margin:4px 0;border-left:3px solid {color};
                            display:flex;justify-content:space-between;align-items:center;">
                    <div><span style="color:#e2e8f0;font-weight:600;font-size:0.9rem;">{control_name}</span>
                    <span style="color:{color};font-size:0.7rem;margin-left:8px;font-weight:600;">● {status}</span></div>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div style="background:#0a1420;border-radius:6px;width:80px;height:6px;overflow:hidden;">
                            <div style="background:linear-gradient(90deg,{color},rgba({r},{g},{b},0.5));height:100%;width:{score}%;"></div>
                        </div>
                        <span style="color:{color};font-weight:700;font-family:'JetBrains Mono';font-size:0.85rem;">{score}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            categories = list(controls.keys())
            scores = [v["score"] for v in controls.values()]
            colors_radar = ["#05ffa1" if s >= 90 else "#ffae00" if s >= 75 else "#ff2a6d" for s in scores]
            fig = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]], fill="toself",
                line_color="#00f0ff", line_width=2, fillcolor="rgba(0,240,255,0.1)",
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.04)")),
                              template="plotly_dark", height=380, title=dict(text=f"{framework} Radar", font=dict(size=14, color="#e2e8f0")),
                              paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=40,r=40,t=60,b=40),
                              font=dict(family="JetBrains Mono", size=10))
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📊 Cross-Framework Comparison")
fig = go.Figure()
framework_names = list(compliance.keys())
all_categories = set()
for fw in compliance.values():
    all_categories.update(fw.keys())

for framework, controls in compliance.items():
    avg = sum(v["score"] for v in controls.values()) / len(controls)
    fig.add_trace(go.Bar(x=[framework], y=[avg], name=framework,
                         marker_color=["#00f0ff","#b829dd","#ffae00"][list(compliance.keys()).index(framework)],
                         marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1))

fig.update_layout(template="plotly_dark", height=350, yaxis_title="Average Compliance Score",
                  xaxis_title="Framework", showlegend=False,
                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                  margin=dict(l=40,r=40,t=30,b=40), font=dict(family="JetBrains Mono", size=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📋 Recommended Actions")
actions = [
    ("NIST CSF — Recover", "Develop and test disaster recovery procedures", "HIGH", "#ff2a6d"),
    ("NIST CSF — Respond", "Establish automated incident response playbooks", "HIGH", "#ffae00"),
    ("ISO 27001 — Comms Security", "Implement encrypted communication channels", "MEDIUM", "#00f0ff"),
    ("PCI DSS — Monitoring & Testing", "Deploy continuous security monitoring", "CRITICAL", "#ff2a6d"),
    ("PCI DSS — Vulnerability Mgmt", "Establish quarterly vulnerability scanning", "HIGH", "#ffae00"),
]
for title, desc, priority, color in actions:
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,rgba(5,8,20,0.6),rgba(15,20,45,0.4));
                padding:12px 16px;border-radius:10px;margin:4px 0;border-left:3px solid {color};">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div><span style="color:{color};font-weight:700;font-family:'JetBrains Mono';font-size:0.85rem;">{title}</span>
            <span style="color:#e2e8f0;margin-left:8px;font-size:0.85rem;">{desc}</span></div>
            <span style="background:{color};color:#000;padding:2px 10px;border-radius:4px;font-size:0.65rem;font-weight:700;">{priority}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("🛡️ Sentinel AI v6.2.0 — Compliance Dashboard | Last Audit: 2024-07-15")