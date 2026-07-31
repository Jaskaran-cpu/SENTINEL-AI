"""ML Engine — Train all models with one click."""

import streamlit as st
from src.config import DEFAULT_N_SAMPLES, DEFAULT_TEST_SIZE, APP_VERSION
from src.data.engine import DataEngine
from src.models.pipeline import MLPipeline
from src.utils.css import get_css
from src.utils.viz import VizEngine

st.set_page_config(page_title="ML Engine", page_icon="🧠", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown('<div class="section-title">🧠 Classic ML Training Engine</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Training Configuration**")
    st.caption("Fast mode is tuned to finish on a normal laptop.")
    n_samples = st.slider("Samples", 500, 5000, 1500, step=250)
    test_size = st.slider("Test Split", 0.15, 0.35, 0.2, step=0.05)
    cv_folds = st.slider("Validation Folds", 2, 3, 2)

if st.button("🚀  Train All Models", type="primary", use_container_width=True):
    with st.status("Training pipeline running...", expanded=True) as status:
        st.write("⏳ Generating synthetic network data...")
        engine = DataEngine(n_samples=n_samples)
        engine.generate()
        st.write(f"✅ Generated {len(engine.df)} samples")

        st.write("⏳ Engineering features & preprocessing...")
        X_tr, X_te, y_tr, y_te = engine.preprocess(test_size=test_size)
        st.write(f"✅ Train: {X_tr.shape[0]}, Test: {X_te.shape[0]}")

        st.write("⏳ Training optimized models (Random Forest, Boosting, SVM, MLP, Ensemble)...")
        pipe = MLPipeline()
        pipe.train_all(X_tr, y_tr, X_te, y_te, cv=cv_folds, on_progress=st.write)
        st.write("✅ All models trained!")

        st.session_state["data_engine"] = engine
        st.session_state["pipeline"] = pipe
        st.session_state["class_names"] = list(engine.label_encoder.classes_)
        status.update(label="Training complete!", state="complete")

    st.balloons()

if "pipeline" in st.session_state and st.session_state.pipeline.is_trained:
    st.success(f"✅ {len(st.session_state.pipeline.results)} models ready")
    import pandas as pd
    df = pd.DataFrame(st.session_state.pipeline.results).T
    st.dataframe(df.style.format("{:.4f}"), use_container_width=True)
