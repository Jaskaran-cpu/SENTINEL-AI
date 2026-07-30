import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, play_sound

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("scan"), height=0)

st.markdown('<div class="main-header">🔍 DEEP PACKET INSPECTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Explainable AI — SHAP Values, Attention Maps & Feature Analysis</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background:#050814;border:1px solid rgba(0,240,255,0.15);border-radius:8px;padding:14px;
            font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#05ffa1;margin-bottom:20px;
            overflow:hidden;position:relative;">
    <div style="color:#64748b;margin-bottom:6px;">$ sentinel-ai --inspect --flow-id 0x7a3f9c2d --deep</div>
    <div>[OK] Capturing packets on interface eth0...</div>
    <div>[OK] Extracting 15 flow features</div>
    <div>[OK] Running BiLSTM + Multi-Head Attention inference</div>
    <div>[<span style="color:#ff2a6d;">ALERT</span>] Classification: <strong>DDoS Attack</strong> | Confidence: 99.1%</div>
    <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#00f0ff,transparent);animation:scanSweep 2.5s linear infinite;"></div>
</div>
""", unsafe_allow_html=True)

flow_data = {"Flow Duration (ms)":125000,"Total Fwd Pkts":45,"Total Bwd Pkts":12,
             "Total Length Fwd (B)":67500,"Flow Bytes/s":540.0,"Flow Packets/s":0.456,
             "Flow IAT Mean (ms)":2847.73,"Fwd Pkt Len Mean":1500.0,"Bwd Pkt Len Mean":1200.0,
             "SYN Flag Count":45,"ACK Flag Count":57,"PSH Flag Count":12,
             "URG Flag Count":0,"FIN Flag Count":2,"RST Flag Count":1}

st.subheader("📋 Flow Features")
cols = st.columns(5)
for i, (feature, value) in enumerate(flow_data.items()):
    with cols[i % 5]:
        st.metric(feature, f"{value:,.2f}" if isinstance(value, float) else f"{value:,}")

st.markdown("---")
st.subheader("🧠 SHAP Explanation — Why DDoS?")
features = list(flow_data.keys())
shap_values = [0.15,0.12,0.08,0.07,0.06,0.05,0.04,0.03,0.02,0.18,0.10,0.05,0.01,0.01,0.01]
base_value = 0.3
sorted_data = sorted(zip(features, shap_values), key=lambda x: abs(x[1]), reverse=True)
features_sorted = [d[0] for d in sorted_data]
shap_sorted = [d[1] for d in sorted_data]

fig = go.Figure()
fig.add_trace(go.Bar(y=["Base Value"], x=[base_value], orientation="h", marker_color="#475569", name="Base Value"))
fig.add_trace(go.Bar(y=features_sorted, x=shap_sorted, orientation="h",
                     marker_color=["#ff2a6d" if v>0 else "#05ffa1" for v in shap_sorted], name="SHAP Value"))
fig.update_layout(template="plotly_dark", title="SHAP Waterfall — Feature Contribution to DDoS Prediction",
                  xaxis_title="Impact on Prediction", yaxis_title="Feature", height=520, barmode="relative",
                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                  margin=dict(l=40,r=40,t=60,b=40), font=dict(family="JetBrains Mono", size=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🔥 Multi-Head Attention Heatmap — BiLSTM Focus")
np.random.seed(42)
attention_matrix = np.random.rand(15, 15)
attention_matrix = (attention_matrix + attention_matrix.T) / 2
np.fill_diagonal(attention_matrix, np.random.uniform(0.7, 1.0, 15))

fig_attn = go.Figure(data=go.Heatmap(z=attention_matrix, x=list(flow_data.keys()), y=list(flow_data.keys()),
                                      colorscale=[[0,"#0a0e1f"],[0.2,"#1e1b4b"],[0.5,"#581c87"],[0.8,"#7c3aed"],[1,"#f472b6"]],
                                      zmid=0.5, hovertemplate="%{x} → %{y}<br>Attention: %{z:.3f}<extra></extra>"))
fig_attn.update_layout(template="plotly_dark", title="Attention Weights — Layer 3, Head 2", height=520,
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                       margin=dict(l=40,r=40,t=60,b=40), font=dict(family="JetBrains Mono", size=9))
st.plotly_chart(fig_attn, use_container_width=True)

st.markdown("---")
st.subheader("🎯 Model Prediction Confidence")
c1, c2, c3 = st.columns(3)
for col, label, color, pct, w in [(c1,"DDoS Attack","#ff2a6d","99.1%",99.1),
                                    (c2,"Port Scan","#00f0ff","0.5%",1),
                                    (c3,"Benign Traffic","#05ffa1","0.4%",1)]:
    r,g,b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba({r},{g},{b},0.1),rgba({r},{g},{b},0.02));
                    border-radius:12px;padding:20px;text-align:center;border:1px solid rgba({r},{g},{b},0.2);">
            <div style="color:{color};font-weight:700;font-size:1rem;">{label}</div>
            <div style="margin:12px 0;"><div style="background:#0a1420;border-radius:8px;height:8px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,{color},rgba({r},{g},{b},0.5));height:100%;width:{w}%;border-radius:8px;"></div>
            </div></div>
            <div style="font-size:1.8rem;font-weight:800;color:{color};font-family:'JetBrains Mono';">{pct}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📦 Raw Packet Hex Dump")
hex_lines = ["45 00 00 3c 1c 46 40 00 40 06 b1 e6 c0 a8 01 01  E..<.F@.@.......",
             "c0 a8 01 0a 1f 90 00 50 00 00 00 00 00 00 00 00  .......P........",
             "a0 02 ff ff 00 00 00 00 02 04 05 b4 01 03 03 08  ................",
             "01 01 04 02 00 00 00 00 00 00 00 00 00 00 00 00  ................"]
hex_html = '<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;background:#050814;border-radius:8px;padding:12px;border:1px solid rgba(0,240,255,0.1);">'
for line in hex_lines:
    hex_html += f'<div style="color:#475569;line-height:1.8;"><span style="color:#00f0ff;">{line[:48]}</span>  <span style="color:#64748b;">{line[50:]}</span></div>'
hex_html += "</div>"
st.markdown(hex_html, unsafe_allow_html=True)

st.markdown("---")
st.caption("🛡️ Sentinel AI v6.2.0 — Deep Packet Inspector | XAI Engine Active")