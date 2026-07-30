"""Predictive Analytics — Live prediction and probability breakdown."""

import streamlit as st
import numpy as np
from src.utils.css import get_css
from src.utils.viz import VizEngine
from src.config import ATTACK_COLORS, MODEL_REGISTRY

st.set_page_config(page_title="Predictive Analytics", page_icon="📈", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Classic Analytics</div>', unsafe_allow_html=True)

if "pipeline" not in st.session_state or not st.session_state.pipeline.is_trained:
    st.info("Train models first.")
    st.stop()

pipe = st.session_state.pipeline
engine = st.session_state.data_engine
class_names = st.session_state.get("class_names", [])

model_key = st.selectbox("Model", list(pipe.results.keys()),
    format_func=lambda k: MODEL_REGISTRY.get(k, {}).get("name", k))

n_pred = st.slider("Number of random predictions", 1, 50, 10)
if st.button("🎯 Generate Predictions"):
    idx = np.random.choice(len(engine.df), n_pred, replace=False)
    X_raw = engine.df.iloc[idx][engine.feature_names].values
    X_scaled = engine.scaler.transform(X_raw)
    preds, probs = pipe.predict(X_scaled, model_key)
    pred_names = [class_names[p] for p in preds]

    cols = st.columns(min(5, n_pred))
    for i, (name, prob_row) in enumerate(zip(pred_names, probs)):
        with cols[i % len(cols)]:
            top_class = np.argmax(prob_row)
            conf = prob_row[top_class]
            color = ATTACK_COLORS.get(name, "#64748b")
            st.markdown(f"""<div class="metric-card" style="--accent:{color}">
                <p style="color:#64748b; font-size:11px; text-transform:uppercase; margin:0 0 4px">Sample {i+1}</p>
                <p style="color:{color}; font-size:14px; font-weight:700; margin:0">{name}</p>
                <p style="color:#94a3b8; font-size:12px; margin:4px 0 0">Conf: {conf*100:.1f}%</p>
            </div>""", unsafe_allow_html=True)
