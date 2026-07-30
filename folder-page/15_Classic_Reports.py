"""Reports — Classification report and data export."""

import streamlit as st
import pandas as pd
from src.utils.css import get_css
from src.config import MODEL_REGISTRY

st.set_page_config(page_title="Reports", page_icon="📋", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Classic Reports</div>', unsafe_allow_html=True)

if "pipeline" not in st.session_state or not st.session_state.pipeline.is_trained:
    st.info("Train models first.")
    st.stop()

pipe = st.session_state.pipeline
class_names = st.session_state.get("class_names", [])

model_key = st.selectbox("Model", list(pipe.results.keys()),
    format_func=lambda k: MODEL_REGISTRY.get(k, {}).get("name", k))

tab1, tab2, tab3 = st.tabs(["Classification Report", "Results Table", "Raw Data"])

with tab1:
    report = pipe.get_report(model_key, class_names)
    if report:
        st.code(report, language="text")
        st.download_button("Download Report", report, file_name=f"report_{model_key}.txt")

with tab2:
    df = pd.DataFrame(pipe.results).T
    df.index = df.index.map(lambda k: MODEL_REGISTRY.get(k, {}).get("name", k))
    st.dataframe(df.style.format(precision=4), use_container_width=True)
    csv = df.to_csv()
    st.download_button("Download CSV", csv, file_name="model_results.csv", mime="text/csv")

with tab3:
    if "data_engine" in st.session_state:
        df_raw = st.session_state.data_engine.get_feature_dataframe()
        st.dataframe(df_raw.head(100), use_container_width=True)
        csv_raw = df_raw.to_csv()
        st.download_button("Download Dataset", csv_raw, file_name="sentinel_dataset.csv", mime="text/csv")
