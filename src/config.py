"""
Sentinel AI v6 — Centralized Configuration
Single source of truth for all application constants, colors, and ML defaults.
"""

# ── Application Metadata ──
APP_NAME: str = "Sentinel AI"
APP_VERSION: str = "6.0.0"
APP_TAGLINE: str = "Neural Cyber Threat Intelligence"
APP_COPYRIGHT: str = "© 2024 Cyber Defense Systems"

# ── Design Tokens ──
COLORS = {
    "cyan": "#00f0ff",
    "green": "#05ffa1",
    "red": "#ff2a6d",
    "yellow": "#ffae00",
    "purple": "#b829dd",
    "blue": "#3b82f6",
    "pink": "#f472b6",
    "orange": "#fb923c",
    "bg_primary": "#030712",
    "bg_secondary": "#0a101f",
    "bg_card": "#0f172a",
    "bg_card_hover": "#1e293b",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "border_subtle": "rgba(0, 240, 255, 0.06)",
    "border_glow": "rgba(0, 240, 255, 0.25)",
}

# ── Severity Mapping ──
SEVERITY_COLORS = {
    "CRITICAL": "#ff2a6d",
    "HIGH": "#ffae00",
    "MEDIUM": "#00f0ff",
    "LOW": "#05ffa1",
    "INFO": "#64748b",
}

# ── ML Configuration ──
DEFAULT_N_SAMPLES: int = 5000
DEFAULT_TEST_SIZE: float = 0.2
DEFAULT_CONTAMINATION: float = 0.05
DEFAULT_RANDOM_STATE: int = 42
DEFAULT_N_ESTIMATORS: int = 200
DEFAULT_MAX_DEPTH: int = 12
DEFAULT_LEARNING_RATE: float = 0.1
CROSS_VALIDATION_FOLDS: int = 5

# ── Feature Names ──
NETWORK_FEATURES = [
    "packet_length", "src_port", "dst_port", "protocol_num",
    "duration", "bytes_sent", "bytes_received", "packets_sent",
    "packets_received", "flow_rate", "inter_arrival_time",
    "header_length", "payload_entropy", "tcp_flags", "window_size",
]

ENGINEERED_FEATURES = [
    "bytes_per_packet", "packet_ratio", "flow_efficiency",
    "payload_ratio", "burst_index", "entropy_per_byte",
    "port_similarity", "direction_imbalance",
]

ALL_FEATURES = NETWORK_FEATURES + ENGINEERED_FEATURES

# ── Attack Types ──
ATTACK_TYPES = [
    "Normal", "DDoS", "Port Scan", "Brute Force",
    "SQL Injection", "XSS", "Man-in-the-Middle",
    "DNS Tunneling", "Data Exfiltration",
]

ATTACK_COLORS = {
    "Normal": "#05ffa1",
    "DDoS": "#ff2a6d",
    "Port Scan": "#ffae00",
    "Brute Force": "#b829dd",
    "SQL Injection": "#00f0ff",
    "XSS": "#fb923c",
    "Man-in-the-Middle": "#f472b6",
    "DNS Tunneling": "#3b82f6",
    "Data Exfiltration": "#ef4444",
}

# ── Model Registry ──
MODEL_REGISTRY = {
    "rf": {"name": "Random Forest", "color": "#05ffa1"},
    "xgb": {"name": "XGBoost", "color": "#ffae00"},
    "svm": {"name": "SVM (RBF)", "color": "#00f0ff"},
    "mlp": {"name": "Neural Network", "color": "#b829dd"},
    "lgbm": {"name": "LightGBM", "color": "#3b82f6"},
    "ensemble": {"name": "Soft Voting Ensemble", "color": "#ff2a6d"},
}
