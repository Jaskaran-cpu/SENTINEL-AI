# 🛡️ SENTINAL AI

**Neural Cyber Threat Intelligence Platform**

Pure ML pipeline for multi-class network intrusion detection with 6 model architectures, 24 engineered features, and interactive visualizations.

## Architecture

```
┌──────────────────────────────────────────┐
│           Streamlit Multi-Page UI         │
├──────────────────────────────────────────┤
│  Dashboard │ ML Engine │ Model Lab │ ...  │
├──────────────────────────────────────────┤
│           VizEngine (Plotly)             │
├──────────────────────────────────────────┤
│           MLPipeline                      │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐      │
│  │ RF │ │XGB │ │SVM │ │MLP │ │LGBM│      │
│  └──┬─┘ └──┬─┘ └──┬─┘ └──┬─┘ └──┬─┘      │
│     └───────┴───────┼───────┴─────┘      │
│              Soft Voting Ensemble          │
├──────────────────────────────────────────┤
│           DataEngine                       │
│  Generate → Engineer → Scale → Split      │
└──────────────────────────────────────────┘
```
```
sentinel-ai-v3/
├── app.py                          ← Main entry with sound toggle + animations
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   └── utils.py                    ← Real ML training, data generators, sound FX
└── pages/
    ├── command_center.py           ← 🏠 10 animated metrics, threat gauge, radar
    ├── threat_map.py               ← 🌍 Network topology with attack pulses
    ├── packet_inspector.py         ← 🔍 SHAP + attention + hex dump + terminal FX
    ├── model_lab.py                ← 🤖 REAL sklearn model training + feature importance
    ├── predictive.py               ← 📈 Time-series forecasting + anomaly predictions
    ├── incident.py                 ← 🚨 5-tab playbooks + MTTR analytics
    ├── report.py                   ← 📄 PDF generation (fixed, working)
    ├── threat_actors.py            ← 👤 NEW! APT profiles + MITRE ATT&CK mapping
    └── mlops.py                    ← ⚙️ Model registry + training + logs
## Quick Start

```bash
cd SENTINEL-AI
pip install -r requirements.txt
streamlit run app.py
```

## Docker

```bash
docker-compose up --build
```

## Features

- **6 Models**: Random Forest, XGBoost, SVM, Neural Network, LightGBM, Soft Voting Ensemble
- **24 Features**: 15 raw network features + 9 engineered features
- **9 Classes**: Normal, DDoS, Port Scan, Brute Force, SQL Injection, XSS, MITM, DNS Tunneling, Data Exfiltration
- **Evaluation**: Confusion matrix, ROC curves, cross-validation, feature importance
- **Real-time Detection**: Classify single traffic samples with probability breakdown

## License

MIT © 2024 Cyber Defense Systems
