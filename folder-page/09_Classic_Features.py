"""Feature Analysis — Importance, correlation, distribution."""

import streamlit as st
from src.utils.css import get_css
from src.utils.viz import VizEngine

st.set_page_config(page_title="Feature Analysis", page_icon="🔍", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 Classic Features</div>', unsafe_allow_html=True)

if "data_engine" not in st.session_state:
    st.info("Generate data first via **ML Engine**.")
    st.stop()

engine = st.session_state.data_engine
vz = VizEngine()

tab1, tab2, tab3 = st.tabs(["Importance", "Correlation", "Distribution"])

with tab1:
    if "pipeline" in st.session_state:
        imp = st.session_state.pipeline.get_feature_importance(engine.feature_names, "rf")
        if len(imp) > 0:
            top_n = st.slider("Top N Features", 5, 24, 20)
            st.plotly_chart(vz.feature_importance(imp, top_n), use_container_width=True)
            st.dataframe(imp.head(top_n), use_container_width=True, hide_index=True)

with tab2:
    df = engine.get_feature_dataframe()
    if len(df) > 0:
        st.plotly_chart(vz.correlation_heatmap(df), use_container_width=True)

with tab3:
    if len(engine.df) > 0:
        dist = engine.get_class_distribution()
        st.plotly_chart(vz.class_distribution(dist), use_container_width=True)
        import pandas as pd
        dist_df = pd.DataFrame(list(dist.items()), columns=["Class", "Count"])
        st.dataframe(dist_df, use_container_width=True, hide_index=True)
