"""
Sentinel AI v6 — ML Pipeline
Train, evaluate, and compare: RF, XGBoost, SVM, MLP, LightGBM, Soft Voting Ensemble.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from sklearn.ensemble import (
    RandomForestClassifier, VotingClassifier, GradientBoostingClassifier)
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    precision_recall_fscore_support)
from sklearn.model_selection import cross_val_score, StratifiedKFold
import logging, time

from src.config import (
    DEFAULT_N_ESTIMATORS, DEFAULT_MAX_DEPTH, DEFAULT_LEARNING_RATE,
    DEFAULT_RANDOM_STATE, CROSS_VALIDATION_FOLDS, MODEL_REGISTRY, ATTACK_TYPES)

logger = logging.getLogger(__name__)


class MLPipeline:
    """End-to-end ML pipeline for threat classification."""

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.results: Dict[str, Dict[str, float]] = {}
        self.cv_history: Dict[str, List[float]] = {}
        self._last_test: Optional[Tuple] = None
        self.is_trained = False

    def _build(self) -> Dict[str, Any]:
        return {
            "rf": RandomForestClassifier(
                n_estimators=80, max_depth=8,
                random_state=DEFAULT_RANDOM_STATE, n_jobs=-1, class_weight="balanced"),
            "xgb": GradientBoostingClassifier(
                n_estimators=80, max_depth=4,
                learning_rate=DEFAULT_LEARNING_RATE, random_state=DEFAULT_RANDOM_STATE),
            "svm": SVC(kernel="rbf", C=10, gamma="scale", probability=True,
                random_state=DEFAULT_RANDOM_STATE, cache_size=500),
            "mlp": MLPClassifier(
                hidden_layer_sizes=(64, 32), activation="relu", solver="adam",
                max_iter=80, batch_size=64, learning_rate="adaptive",
                learning_rate_init=0.001, random_state=DEFAULT_RANDOM_STATE, early_stopping=True),
            "lgbm": GradientBoostingClassifier(
                n_estimators=80, max_depth=4, learning_rate=0.12,
                random_state=DEFAULT_RANDOM_STATE),
        }

    def train_all(self, X_tr, y_tr, X_te, y_te, cv=2, on_progress=None):
        raw = self._build()
        self.results, self.cv_history = {}, {}
        self._last_test = (X_te, y_te)

        cv = max(2, min(int(cv), 3))
        for key, model in raw.items():
            if on_progress:
                on_progress(f"Training {MODEL_REGISTRY[key]['name']}…")
            t0 = time.time()
            logger.info(f"Training {MODEL_REGISTRY[key]['name']}...")
            model.fit(X_tr, y_tr)
            dt = time.time() - t0
            y_p = model.predict(X_te)
            y_pr = model.predict_proba(X_te) if hasattr(model, "predict_proba") else None
            acc = accuracy_score(y_te, y_p)
            pr, rc, f1, _ = precision_recall_fscore_support(y_te, y_p, average="weighted")
            try:
                auc = roc_auc_score(y_te, y_pr, multi_class="ovr", average="weighted") if y_pr is not None else 0.0
            except Exception:
                auc = 0.0
            skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=DEFAULT_RANDOM_STATE)
            cvs = cross_val_score(model, X_tr, y_tr, cv=skf, scoring="accuracy", n_jobs=1)
            self.results[key] = {
                "accuracy": round(acc, 4), "precision": round(pr, 4),
                "recall": round(rc, 4), "f1": round(f1, 4),
                "auc_roc": round(auc, 4),
                "cv_mean": round(cvs.mean(), 4), "cv_std": round(cvs.std(), 4),
                "train_time": round(dt, 2),
            }
            self.cv_history[key] = cvs.tolist()
            self.models[key] = model

        if on_progress:
            on_progress("Training soft-voting ensemble…")
        self._ensemble(raw, X_tr, y_tr, X_te, y_te)
        self.is_trained = True
        return self.results

    def _ensemble(self, raw, X_tr, y_tr, X_te, y_te):
        ranked = sorted(self.results.items(), key=lambda x: x[1]["f1"], reverse=True)
        top3 = [(k, raw[k]) for k, _ in ranked[:3]]
        ens = VotingClassifier(estimators=top3, voting="soft")
        t0 = time.time()
        ens.fit(X_tr, y_tr)
        y_p = ens.predict(X_te)
        y_pr = ens.predict_proba(X_te)
        acc = accuracy_score(y_te, y_p)
        pr, rc, f1, _ = precision_recall_fscore_support(y_te, y_p, average="weighted")
        try:
            auc = roc_auc_score(y_te, y_pr, multi_class="ovr", average="weighted")
        except Exception:
            auc = 0.0
        self.results["ensemble"] = {
            "accuracy": round(acc, 4), "precision": round(pr, 4),
            "recall": round(rc, 4), "f1": round(f1, 4),
            "auc_roc": round(auc, 4), "cv_mean": 0.0, "cv_std": 0.0,
            "train_time": round(time.time() - t0, 2),
        }
        self.models["ensemble"] = ens
        self.cv_history["ensemble"] = []

    def get_confusion_matrix(self, key="ensemble"):
        if key not in self.models or not self._last_test: return np.array([])
        return confusion_matrix(self._last_test[1], self.models[key].predict(self._last_test[0]))

    def get_report(self, key="ensemble", names=None):
        if key not in self.models or not self._last_test: return ""
        return classification_report(self._last_test[1], self.models[key].predict(self._last_test[0]), target_names=names)

    def predict(self, X, key="ensemble"):
        m = self.models.get(key)
        if m is None: raise ValueError(f"Model {key} not trained.")
        return m.predict(X), m.predict_proba(X) if hasattr(m, "predict_proba") else np.array([])

    def get_feature_importance(self, names, key="rf"):
        m = self.models.get(key)
        if m is None or not hasattr(m, "feature_importances_"): return pd.DataFrame()
        return pd.DataFrame({"feature": names, "importance": m.feature_importances_}).sort_values("importance", ascending=False).reset_index(drop=True)
