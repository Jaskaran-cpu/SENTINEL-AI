"""Model Lab — Interactive model comparison and evaluation."""

import streamlit as st
import numpy as np
from src.utils.css import get_css
from src.utils.viz import VizEngine
from src.config import MODEL_REGISTRY

st.set_page_config(page_title="Model Lab", page_icon="📊", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Classic Model Lab</div>', unsafe_allow_html=True)

if "pipeline" not in st.session_state or not st.session_state.pipeline.is_trained:
    st.info("Train models first via **ML Engine**.")
    st.stop()

pipe = st.session_state.pipeline
class_names = st.session_state.get("class_names", [])
vz = VizEngine()
res = pipe.results

tab1, tab2, tab3, tab4 = st.tabs(["Comparison", "ROC Curves", "Confusion Matrix", "CV Scores"])

with tab1:
    metric = st.selectbox("Metric", ["f1", "accuracy", "precision", "recall", "auc_roc"], index=0)
    st.plotly_chart(vz.model_comparison(res, metric), use_container_width=True)
    st.plotly_chart(vz.radar(res), use_container_width=True)

with tab2:
    model_key = st.selectbox("Model", list(res.keys()), index=0,
        format_func=lambda k: MODEL_REGISTRY.get(k, {}).get("name", k))
    _, y_prob = pipe.predict(pipe._last_test[0], model_key)
    if len(y_prob) > 0:
        st.plotly_chart(vz.roc_curves(pipe._last_test[1], y_prob, class_names), use_container_width=True)

with tab3:
    mk = st.selectbox("Model for CM", list(res.keys()), index=0,
        format_func=lambda k: MODEL_REGISTRY.get(k, {}).get("name", k), key="cm_sel")
    cm = pipe.get_confusion_matrix(mk)
    if len(cm) > 0 and class_names:
        st.plotly_chart(vz.confusion_matrix(cm, class_names), use_container_width=True)

with tab4:
    st.plotly_chart(vz.cv_scores(pipe.cv_history), use_container_width=True)
