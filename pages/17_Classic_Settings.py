"""Settings — Configuration and about."""

import streamlit as st
from src.config import APP_NAME, APP_VERSION, APP_TAGLINE, APP_COPYRIGHT, COLORS, ATTACK_TYPES
from src.utils.css import get_css

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown('<div class="section-title">⚙️ Classic Settings</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Configuration", "ML Defaults", "About"])

with tab1:
    st.markdown("### Streamlit Configuration")
    st.code("""
[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
base = "dark"
primaryColor = "#00f0ff"
backgroundColor = "#030712"
secondaryBackgroundColor = "#0a101f"
textColor = "#e2e8f0"

[client]
showErrorDetails = false
toolbarMode = "minimal"
    """, language="toml")

with tab2:
    st.markdown("### ML Hyperparameters")
    import pandas as pd
    defaults = pd.DataFrame({
        "Parameter": ["N Samples", "Test Size", "N Estimators", "Max Depth",
                       "Learning Rate", "CV Folds", "Contamination", "Random State"],
        "Default": [5000, 0.2, 200, 12, 0.1, 5, 0.05, 42],
        "Type": ["int", "float", "int", "int", "float", "int", "float", "int"],
    })
    st.dataframe(defaults, use_container_width=True, hide_index=True)

    st.markdown("### Model Architectures")
    models = pd.DataFrame({
        "Model": ["Random Forest", "XGBoost", "SVM (RBF)", "Neural Network", "LightGBM", "Ensemble"],
        "Key": ["rf", "xgb", "svm", "mlp", "lgbm", "ensemble"],
        "Type": ["Ensemble", "Boosting", "Kernel", "Deep Learning", "Boosting", "Voting"],
        "Key Param": ["n_estimators=200", "n_estimators=200", "C=10, rbf", "3x (256,128,64)", "n_estimators=150", "Top-3 Soft Vote"],
    })
    st.dataframe(models, use_container_width=True, hide_index=True)

with tab3:
    st.markdown(f"""
    <div style="text-align:center; padding:40px 0">
        <h2 style="font-size:32px; font-weight:800; background: linear-gradient(135deg, #00f0ff, #b829dd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0 0 8px">
            {APP_NAME} v{APP_VERSION}
        </h2>
        <p style="color:#94a3b8; font-size:16px">{APP_TAGLINE}</p>
        <p style="color:#475569; font-size:13px; margin-top:16px">{APP_COPYRIGHT}</p>
        <p style="color:#475569; font-size:12px; margin-top:8px">
            Pure ML pipeline • 6 models • 24 features • 9-class classification<br>
            Built with scikit-learn, Plotly, Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Supported Attack Types")
    for attack in ATTACK_TYPES:
        st.markdown(f"• {attack}")
