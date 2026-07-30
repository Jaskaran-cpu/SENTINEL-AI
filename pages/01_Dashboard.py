"""Dashboard — System Overview & Key Metrics."""

import streamlit as st
import numpy as np
from src.config import APP_NAME, APP_VERSION, COLORS, ATTACK_TYPES, ATTACK_COLORS
from src.utils.css import get_css

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

st.markdown('<div class="section-title">🏠 Classic Dashboard</div>', unsafe_allow_html=True)

if "pipeline" not in st.session_state or not st.session_state.pipeline.is_trained:
    st.info("Train models first via **ML Engine** page.")
    st.stop()

pipe = st.session_state.pipeline
res = pipe.results
best = max(res.items(), key=lambda x: x[1]["f1"])
best_name = res[best[0]]

# Top gauges
st.markdown("### Ensemble Performance")
g1, g2, g3, g4, g5 = st.columns(5)
from src.utils.viz import VizEngine
vz = VizEngine()

with g1:
    st.plotly_chart(vz.metric_gauge(best_name["accuracy"], "Accuracy", "#00f0ff"), use_container_width=True)
with g2:
    st.plotly_chart(vz.metric_gauge(best_name["precision"], "Precision", "#05ffa1"), use_container_width=True)
with g3:
    st.plotly_chart(vz.metric_gauge(best_name["recall"], "Recall", "#ffae00"), use_container_width=True)
with g4:
    st.plotly_chart(vz.metric_gauge(best_name["f1"], "F1 Score", "#b829dd"), use_container_width=True)
with g5:
    st.plotly_chart(vz.metric_gauge(best_name["auc_roc"], "AUC-ROC", "#ff2a6d"), use_container_width=True)

st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

# Comparison charts
left, right = st.columns(2)
with left:
    st.plotly_chart(vz.model_comparison(res, "f1"), use_container_width=True)
with right:
    st.plotly_chart(vz.training_time(res), use_container_width=True)

# Model leaderboard
st.markdown('<div class="section-title" style="margin-top:24px">Model Leaderboard</div>', unsafe_allow_html=True)
import pandas as pd
df = pd.DataFrame(res).T
if "ensemble" in df.index:
    df = df.reindex(["ensemble"] + [i for i in df.index if i != "ensemble"])
df["model"] = df.index.map(lambda k: "✅ " + {"rf":"Random Forest","xgb":"XGBoost","svm":"SVM","mlp":"Neural Network","lgbm":"LightGBM","ensemble":"Soft Voting Ensemble"}.get(k, k))
df_display = df[["model", "accuracy", "precision", "recall", "f1", "auc_roc", "cv_mean", "train_time"]].copy()
df_display.columns = ["Model", "Accuracy", "Precision", "Recall", "F1", "AUC-ROC", "CV Mean", "Time(s)"]
for c in ["Accuracy", "Precision", "Recall", "F1", "AUC-ROC", "CV Mean"]:
    df_display[c] = df_display[c].apply(lambda x: f"{x*100:.2f}%")
df_display["Time(s)"] = df_display["Time(s)"].apply(lambda x: f"{x:.1f}s")
st.dataframe(df_display.reset_index(drop=True), use_container_width=True, hide_index=True)
