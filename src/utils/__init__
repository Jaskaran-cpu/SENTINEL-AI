"""Shared demo data and presentation helpers used by all Sentinel pages."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from .css import get_css
from .viz import VizEngine


def play_sound(_: str) -> str:
    """Return a harmless silent HTML fragment; audio is optional for the UI."""
    return "<span aria-hidden='true'></span>"


def generate_live_metrics() -> dict[str, float | int]:
    return {"active_flows": 12209, "accuracy": 99.3, "active_threats": 5, "auc": 0.999,
            "blocked_ips": 1232, "mitigated": 351, "pending": 10, "threat_score": 66}


def get_attack_data() -> list[dict[str, str]]:
    return [
        {"time":"14:32:19", "severity":"CRITICAL", "type":"DDoS", "source":"45.23.112.8", "country":"US", "target":"API Gateway", "confidence":"99.8%"},
        {"time":"14:28:04", "severity":"HIGH", "type":"Port Scan", "source":"185.220.101.4", "country":"DE", "target":"DMZ", "confidence":"96.2%"},
        {"time":"14:19:37", "severity":"HIGH", "type":"Brute Force", "source":"103.86.98.1", "country":"SG", "target":"VPN", "confidence":"94.6%"},
        {"time":"14:11:22", "severity":"MEDIUM", "type":"SQL Injection", "source":"89.248.165.7", "country":"NL", "target":"Web Portal", "confidence":"88.1%"},
        {"time":"14:04:51", "severity":"MEDIUM", "type":"XSS", "source":"91.240.118.5", "country":"RU", "target":"Customer App", "confidence":"86.4%"},
        {"time":"13:58:16", "severity":"LOW", "type":"Botnet", "source":"198.98.52.9", "country":"US", "target":"DNS", "confidence":"77.2%"},
        {"time":"13:42:03", "severity":"LOW", "type":"Infiltration", "source":"62.210.38.2", "country":"FR", "target":"Endpoint", "confidence":"73.9%"},
    ]


def generate_synthetic_network_data(n_samples: int = 5000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    attack = rng.binomial(1, 0.38, n_samples)
    data = pd.DataFrame({
        "packet_length": rng.normal(700 + attack * 650, 180, n_samples).clip(40),
        "flow_duration": rng.lognormal(-1.4 - attack, .7, n_samples),
        "bytes_sent": rng.lognormal(7.5 + attack * .8, .7, n_samples),
        "packets": rng.poisson(12 + attack * 35, n_samples) + 1,
        "entropy": rng.normal(3.2 + attack * 2.6, .8, n_samples).clip(0, 8),
        "port_risk": rng.uniform(0, 1, n_samples) * (.4 + .6 * attack),
        "request_rate": rng.lognormal(3 + attack * 2.3, .6, n_samples),
        "label": attack,
    })
    return data


def train_models(data: pd.DataFrame):
    features = data.drop(columns="label")
    x_train, x_test, y_train, y_test = train_test_split(features, data.label, test_size=.2, stratify=data.label, random_state=42)
    models = {"Random Forest": RandomForestClassifier(n_estimators=120, max_depth=12, random_state=42, n_jobs=-1),
              "Gradient Boosting": GradientBoostingClassifier(n_estimators=120, random_state=42)}
    results = {}
    for name, model in models.items():
        model.fit(x_train, y_train)
        pred, prob = model.predict(x_test), model.predict_proba(x_test)[:, 1]
        results[name] = {"accuracy": accuracy_score(y_test, pred), "precision": precision_score(y_test, pred, zero_division=0),
                         "recall": recall_score(y_test, pred, zero_division=0), "f1": f1_score(y_test, pred, zero_division=0),
                         "auc": round(roc_auc_score(y_test, prob), 3), "cm": confusion_matrix(y_test, pred),
                         "feature_importance": dict(zip(features.columns, getattr(model, "feature_importances_", np.zeros(features.shape[1]))))}
    return results, x_test, y_test


def get_vulnerability_data() -> list[dict[str, object]]:
    return [
        {"id":"CVE-2024-3094", "service":"OpenSSH", "description":"Supply-chain backdoor exposure", "cvss":10.0, "severity":"CRITICAL", "status":"Unpatched"},
        {"id":"CVE-2024-3400", "service":"Firewall VPN", "description":"Command injection", "cvss":9.8, "severity":"CRITICAL", "status":"Patch Available"},
        {"id":"CVE-2023-48788", "service":"Web Server", "description":"Authentication bypass", "cvss":8.1, "severity":"HIGH", "status":"Patch Available"},
        {"id":"CVE-2023-4966", "service":"Gateway", "description":"Session disclosure", "cvss":7.5, "severity":"HIGH", "status":"Patched"},
        {"id":"CVE-2024-21733", "service":"DNS", "description":"Resource exhaustion", "cvss":6.5, "severity":"MEDIUM", "status":"Unpatched"},
        {"id":"CVE-2023-44487", "service":"HTTP/2", "description":"Rapid reset denial of service", "cvss":5.3, "severity":"MEDIUM", "status":"Patch Available"},
    ]


def get_compliance_data() -> dict[str, dict[str, dict[str, object]]]:
    return {
        "NIST CSF": {"Identify":{"score":92,"status":"Compliant"}, "Protect":{"score":84,"status":"Partial"}, "Detect":{"score":89,"status":"Partial"}, "Respond":{"score":71,"status":"Partial"}, "Recover":{"score":63,"status":"Non-Compliant"}},
        "ISO 27001": {"Access Control":{"score":93,"status":"Compliant"}, "Operations":{"score":88,"status":"Partial"}, "Communications":{"score":76,"status":"Partial"}, "Incident Management":{"score":82,"status":"Partial"}},
        "PCI DSS": {"Network Security":{"score":91,"status":"Compliant"}, "Data Protection":{"score":86,"status":"Partial"}, "Vulnerability Management":{"score":72,"status":"Partial"}, "Monitoring":{"score":64,"status":"Non-Compliant"}},
    }


__all__ = ["VizEngine", "get_css", "play_sound", "generate_live_metrics", "get_attack_data", "generate_synthetic_network_data", "train_models", "get_vulnerability_data", "get_compliance_data"]
