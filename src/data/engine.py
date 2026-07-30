"""
Sentinel AI v6 — Data Engine
Synthetic network traffic generation, feature engineering, and preprocessing.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Optional, Tuple, Dict
import logging

from src.config import (
    DEFAULT_N_SAMPLES, DEFAULT_TEST_SIZE, DEFAULT_RANDOM_STATE,
    NETWORK_FEATURES, ENGINEERED_FEATURES, ALL_FEATURES, ATTACK_TYPES,
)

logger = logging.getLogger(__name__)


class DataEngine:
    """Generates, engineers, and preprocesses network intrusion data."""

    def __init__(self, n_samples: int = DEFAULT_N_SAMPLES, random_state: int = DEFAULT_RANDOM_STATE):
        self.n_samples = n_samples
        self.rng = np.random.default_rng(random_state)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.df: Optional[pd.DataFrame] = None
        self.X_train = self.X_test = self.y_train = self.y_test = None
        self.feature_names: list = ALL_FEATURES

    def generate(self) -> pd.DataFrame:
        """Generate synthetic network traffic with realistic distributions."""
        n = self.n_samples
        records = []

        profiles = {
            "Normal":           {"w": 0.30, "pl": (40, 1500), "dur": (0.01, 30),  "pr": (10, 100),  "ent": (2.0, 7.0)},
            "DDoS":             {"w": 0.15, "pl": (40, 1500), "dur": (0.001, 0.1),"pr": (500,2000), "ent": (0.1, 1.5)},
            "Port Scan":        {"w": 0.12, "pl": (40, 80),   "dur": (0.001,0.05),"pr": (1, 10),    "ent": (0.5, 2.0)},
            "Brute Force":      {"w": 0.10, "pl": (40, 200),  "dur": (0.01, 2),   "pr": (5, 50),    "ent": (1.0, 3.0)},
            "SQL Injection":    {"w": 0.08, "pl": (200,8000), "dur": (0.1, 10),   "pr": (1, 20),    "ent": (4.0, 7.5)},
            "XSS":              {"w": 0.07, "pl": (300,5000), "dur": (0.1, 5),    "pr": (1, 15),    "ent": (4.5, 7.8)},
            "Man-in-the-Middle":{"w": 0.06, "pl": (40, 1500), "dur": (0.01, 60),  "pr": (10, 200),  "ent": (3.0, 7.0)},
            "DNS Tunneling":    {"w": 0.06, "pl": (100, 500), "dur": (0.05, 5),   "pr": (50, 500),  "ent": (5.0, 8.0)},
            "Data Exfiltration":{"w": 0.06, "pl": (500,10000),"dur": (1, 120),    "pr": (100,1000), "ent": (6.0, 8.0)},
        }

        for attack, p in profiles.items():
            count = max(1, int(n * p["w"]))
            for _ in range(count):
                pl = int(self.rng.integers(*p["pl"]))
                dur = float(self.rng.uniform(*p["dur"]))
                pr = float(self.rng.uniform(*p["pr"]))
                ent = float(self.rng.uniform(*p["ent"]))
                src_port = int(self.rng.integers(1024, 65535))
                dst_port = int(self.rng.choice([80,443,22,53,3306,8080,25,110,21,3389],
                    p=[.3,.25,.1,.08,.07,.07,.05,.04,.02,.02]))
                proto = int(self.rng.choice([6, 17, 1], p=[0.7, 0.2, 0.1]))
                bytes_s = int(pl * self.rng.uniform(0.8, 2.5))
                bytes_r = int(pl * self.rng.uniform(0.3, 1.8))
                pkts_s = max(1, int(dur * pr * self.rng.uniform(0.7, 1.3)))
                pkts_r = max(1, int(dur * pr * self.rng.uniform(0.2, 1.0)))
                iat = max(1e-4, dur / max(1, pkts_s + pkts_r) * self.rng.uniform(0.5, 2.0))
                hdr = int(self.rng.choice([20, 24, 32, 40, 60]))
                flags = int(self.rng.integers(0, 64))
                win = int(self.rng.choice([1024, 2048, 4096, 8192, 16384, 32768, 65535]))
                records.append({
                    "packet_length": pl, "src_port": src_port, "dst_port": dst_port,
                    "protocol_num": proto, "duration": round(dur, 6),
                    "bytes_sent": bytes_s, "bytes_received": bytes_r,
                    "packets_sent": pkts_s, "packets_received": pkts_r,
                    "flow_rate": round(pr, 4), "inter_arrival_time": round(iat, 6),
                    "header_length": hdr, "payload_entropy": round(ent, 4),
                    "tcp_flags": flags, "window_size": win, "label": attack,
                })

        self.df = pd.DataFrame(records)
        self._engineer()
        logger.info(f"Generated {len(self.df)} samples across {len(profiles)} classes")
        return self.df

    def _engineer(self) -> None:
        df = self.df
        total_pkts = df["packets_sent"] + df["packets_received"]
        total_bytes = df["bytes_sent"] + df["bytes_received"]
        df["bytes_per_packet"] = np.where(total_pkts > 0, total_bytes / total_pkts, 0).round(2)
        df["packet_ratio"] = np.where(df["packets_received"] > 0, df["packets_sent"] / df["packets_received"], 0).round(4)
        df["flow_efficiency"] = np.where(total_bytes > 0, df["bytes_sent"] / total_bytes, 0.5).round(4)
        df["payload_ratio"] = np.where(df["packet_length"] > 0,
            (df["packet_length"] - df["header_length"]) / df["packet_length"], 0).clip(0, 1).round(4)
        burst = df.groupby((df["inter_arrival_time"].diff().abs() > df["inter_arrival_time"].median()).cumsum()).cumcount()
        df["burst_index"] = burst
        df["entropy_per_byte"] = np.where(df["bytes_sent"] > 0,
            df["payload_entropy"] / (df["bytes_sent"] / 1000 + 1), 0).round(4)
        df["port_similarity"] = (df["src_port"] == df["dst_port"]).astype(int)
        df["direction_imbalance"] = ((df["bytes_sent"] - df["bytes_received"]) / (total_bytes + 1)).round(4)

    def preprocess(self, test_size: float = DEFAULT_TEST_SIZE):
        if self.df is None:
            raise ValueError("No data. Call generate() first.")
        X = self.df[self.feature_names].values
        y = self.label_encoder.fit_transform(self.df["label"].values)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=DEFAULT_RANDOM_STATE, stratify=y)
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        logger.info(f"Train: {self.X_train.shape}, Test: {self.X_test.shape}")
        return self.X_train, self.X_test, self.y_train, self.y_test

    def get_class_distribution(self) -> Dict[str, int]:
        if self.df is None: return {}
        return self.df["label"].value_counts().to_dict()

    def get_feature_dataframe(self) -> pd.DataFrame:
        if self.df is None: return pd.DataFrame()
        return self.df[self.feature_names + ["label"]].copy()
