"""Threat Detection — Classify a single traffic sample."""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.utils.css import get_css
from src.config import ATTACK_COLORS, MODEL_REGISTRY, NETWORK_FEATURES, ENGINEERED_FEATURES, ALL_FEATURES

st.set_page_config(page_title="Threat Detection", page_icon="🛡️", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown('<div class="section-title">🛡️ Classic Detection</div>', unsafe_allow_html=True)

if "pipeline" not in st.session_state or not st.session_state.pipeline.is_trained:
    st.info("Train models first.")
    st.stop()

pipe = st.session_state.pipeline
engine = st.session_state.data_engine
class_names = st.session_state.get("class_names", [])

st.markdown("Enter network traffic features or use a random sample:")
c1, c2 = st.columns([3, 1])
with c2:
    if st.button("🎲 Random Sample", use_container_width=True):
        idx = np.random.randint(len(engine.df))
        row = engine.df.iloc[idx]
        for f in NETWORK_FEATURES:
            st.session_state[f"inp_{f}"] = float(row[f])
        st.rerun()

with c1:
    cols = st.columns(4)
    defaults = {"packet_length": 256, "src_port": 45000, "dst_port": 443, "protocol_num": 6,
        "duration": 0.5, "bytes_sent": 512, "bytes_received": 256, "packets_sent": 10,
        "packets_received": 8, "flow_rate": 50, "inter_arrival_time": 0.01,
        "header_length": 20, "payload_entropy": 4.5, "tcp_flags": 2, "window_size": 8192}
    for i, f in enumerate(NETWORK_FEATURES):
        with cols[i % 4]:
            st.number_input(f.replace("_", " ").title(), min_value=0.0,
                key=f"inp_{f}", value=float(st.session_state.get(f"inp_{f}", defaults.get(f, 0.0))))

if st.button("🔍 Classify", type="primary", use_container_width=True):
    features = np.array([[st.session_state.get(f"inp_{f}", 0) for f in ALL_FEATURES]])
    # Simple imputation for engineered features if they are 0
    for i, f in enumerate(ALL_FEATURES):
        if features[0][i] == 0 and i >= len(NETWORK_FEATURES):
            features[0][i] = 0.5
    features_scaled = engine.scaler.transform(features)
    pred, prob = pipe.predict(features_scaled, "ensemble")
    name = class_names[pred[0]]
    conf = prob[0][pred[0]]
    color = ATTACK_COLORS.get(name, "#64748b")

    st.markdown(f"""<div style="text-align:center; padding:30px; margin:20px 0">
        <p style="font-size:14px; color:#64748b; margin:0">Detected Threat Type</p>
        <p style="font-size:36px; font-weight:800; color:{color}; margin:8px 0; text-shadow: 0 0 30px {color}40">{name}</p>
        <p style="font-size:18px; color:#94a3b8; margin:0">Confidence: {conf*100:.2f}%</p>
    </div>""", unsafe_allow_html=True)

    prob_data = {class_names[i]: prob[0][i] for i in range(len(class_names))}
    sorted_probs = dict(sorted(prob_data.items(), key=lambda x: x[1], reverse=True))
    fig = go.Figure(go.Bar(
        x=list(sorted_probs.keys()), y=[v*100 for v in sorted_probs.values()],
        marker_color=[ATTACK_COLORS.get(k, "#64748b") for k in sorted_probs.keys()],
        text=[f"{v*100:.1f}%" for v in sorted_probs.values()], textposition="outside"))
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"),
        yaxis_title="Probability (%)", height=400,
        xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)
