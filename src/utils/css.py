"""
Sentinel AI v6 — Professional CSS Engine
"""

def get_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    .stApp { background: linear-gradient(160deg, #030712 0%, #0a101f 40%, #0f172a 100%) !important; background-attachment: fixed !important; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0a101f 0%, #030712 100%) !important; border-right: 1px solid rgba(0,240,255,0.08) !important; }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    /* Do not override Streamlit's Material Symbols font: doing so turns icons
       such as keyboard_double_arrow into visible text. */
    .stApp, .stApp p, .stApp div, .stApp label, .stApp button { font-family: 'Inter', -apple-system, sans-serif !important; }
    .material-symbols-rounded, .material-symbols-outlined, .material-icons, [class*="material-symbols"] { font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important; font-style: normal !important; }
    code, pre, .stCodeBlock { font-family: 'JetBrains Mono', monospace !important; }
    .metric-card { background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(10,16,31,0.95)); border: 1px solid rgba(0,240,255,0.1); border-radius: 16px; padding: 20px 24px; margin-bottom: 16px; transition: all 0.3s cubic-bezier(0.4,0,0.2,1); backdrop-filter: blur(20px); position: relative; overflow: hidden; }
    .metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--accent, #00f0ff), transparent); opacity: 0.6; }
    .metric-card:hover { border-color: rgba(0,240,255,0.25); transform: translateY(-2px); box-shadow: 0 8px 32px rgba(0,240,255,0.08); }
    .glow-cyan { color: #00f0ff; text-shadow: 0 0 20px rgba(0,240,255,0.3); }
    .glow-green { color: #05ffa1; text-shadow: 0 0 20px rgba(5,255,161,0.3); }
    .glow-red { color: #ff2a6d; text-shadow: 0 0 20px rgba(255,42,109,0.3); }
    .glow-yellow { color: #ffae00; text-shadow: 0 0 20px rgba(255,174,0,0.3); }
    .glow-purple { color: #b829dd; text-shadow: 0 0 20px rgba(184,41,221,0.3); }
    .badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }
    .badge-success { background: rgba(5,255,161,0.1); color: #05ffa1; border: 1px solid rgba(5,255,161,0.2); }
    .badge-danger { background: rgba(255,42,109,0.1); color: #ff2a6d; border: 1px solid rgba(255,42,109,0.2); }
    .badge-warning { background: rgba(255,174,0,0.1); color: #ffae00; border: 1px solid rgba(255,174,0,0.2); }
    .badge-info { background: rgba(0,240,255,0.1); color: #00f0ff; border: 1px solid rgba(0,240,255,0.2); }
    .section-title { font-size: 20px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }
    .section-title::before { content: ''; width: 4px; height: 24px; background: linear-gradient(180deg, #00f0ff, #b829dd); border-radius: 2px; }
    .dataframe { background: rgba(15,23,42,0.6) !important; border: 1px solid rgba(0,240,255,0.08) !important; border-radius: 12px !important; }
    thead tr th { background: rgba(0,240,255,0.05) !important; color: #00f0ff !important; font-weight: 600 !important; font-size: 13px !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; border-bottom: 1px solid rgba(0,240,255,0.15) !important; }
    tbody tr { border-bottom: 1px solid rgba(255,255,255,0.03) !important; }
    tbody tr:hover { background: rgba(0,240,255,0.03) !important; }
    td, th { color: #e2e8f0 !important; font-size: 13px !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px; background: rgba(15,23,42,0.6); color: #94a3b8; font-weight: 500; padding: 8px 20px; border: 1px solid transparent; }
    .stTabs [aria-selected="true"] { background: rgba(0,240,255,0.08); color: #00f0ff; border-color: rgba(0,240,255,0.25); box-shadow: 0 0 20px rgba(0,240,255,0.1); }
    .stButton > button { background: linear-gradient(135deg, rgba(0,240,255,0.15), rgba(184,41,221,0.15)) !important; border: 1px solid rgba(0,240,255,0.25) !important; color: #00f0ff !important; font-weight: 600 !important; border-radius: 10px !important; transition: all 0.3s !important; }
    .stButton > button:hover { background: linear-gradient(135deg, rgba(0,240,255,0.25), rgba(184,41,221,0.25)) !important; box-shadow: 0 0 30px rgba(0,240,255,0.15) !important; }
    .stSpinner > div { border-top-color: #00f0ff !important; }
    .stMetric { background: rgba(15,23,42,0.5); border-radius: 12px; padding: 12px 16px; border: 1px solid rgba(0,240,255,0.06); }
    .stMetricLabel { color: #94a3b8 !important; font-size: 12px !important; font-weight: 500 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
    .stMetricValue { color: #f1f5f9 !important; font-size: 28px !important; font-weight: 700 !important; }
    .stAlert { border-radius: 12px !important; background: rgba(15,23,42,0.8) !important; }
    .stExpander { border: 1px solid rgba(0,240,255,0.1) !important; border-radius: 12px !important; background: rgba(15,23,42,0.5) !important; }
    @keyframes sentinelFloat { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
    .metric-card { animation: sentinelFloat 5s ease-in-out infinite; }
    @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; } }
    </style>
    """
