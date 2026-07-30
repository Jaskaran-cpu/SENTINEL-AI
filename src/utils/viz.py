"""
Sentinel AI v6 — Visualization Engine
All Plotly/Streamlit charts in one place for consistency.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any
from sklearn.metrics import roc_curve, auc, precision_recall_curve

from src.config import COLORS, ATTACK_COLORS, MODEL_REGISTRY, ATTACK_TYPES, SEVERITY_COLORS


class VizEngine:
    """Centralized chart factory for all Sentinel AI visualizations."""

    # ── Template ──
    @staticmethod
    def _theme() -> dict:
        return dict(
            layout=dict(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif", color="#e2e8f0", size=13),
                margin=dict(l=60, r=30, t=40, b=50),
            )
        )

    # ── Model Comparison Bar Chart ──
    def model_comparison(self, results: Dict[str, Dict[str, float]],
                         metric: str = "f1") -> go.Figure:
        """Horizontal bar chart comparing models on a single metric."""
        df = pd.DataFrame(results).T.sort_values(metric, ascending=True)
        colors = [MODEL_REGISTRY.get(k, {}).get("color", "#64748b") for k in df.index]
        fig = go.Figure(go.Bar(
            orientation="h", y=df.index.map(lambda k: MODEL_REGISTRY.get(k, {}).get("name", k)),
            x=df[metric] * 100, marker_color=colors,
            text=[f"{v*100:.2f}%" for v in df[metric]], textposition="outside",
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
        ))
        fig.update_layout(**self._theme()["layout"],
            xaxis_title=f"{metric.replace('_',' ').title()} (%)", height=max(300, len(df) * 55),
            showlegend=False, xaxis_range=[0, 105],
            title=dict(text=f"Model Comparison — {metric.replace('_',' ').title()}",
                      font=dict(size=16, color="#f1f5f9")))
        return fig

    # ── Multi-metric Radar ──
    def radar(self, results: Dict[str, Dict[str, float]]) -> go.Figure:
        """Spider/radar chart for top models across all metrics."""
        metrics = ["accuracy", "precision", "recall", "f1", "auc_roc"]
        labels = [m.replace("_", " ").title() for m in metrics]
        top = sorted(results.items(), key=lambda x: x[1]["f1"], reverse=True)[:4]
        fig = go.Figure()
        for key, res in top:
            vals = [res.get(m, 0) * 100 for m in metrics]
            vals += vals[:1]
            fig.add_trace(go.Scatterpolar(
                r=vals, theta=labels + [labels[0]], fill="toself",
                name=MODEL_REGISTRY.get(key, {}).get("name", key),
                line_color=MODEL_REGISTRY.get(key, {}).get("color", "#64748b"),
                opacity=0.2, marker=dict(size=6)))
        fig.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)", angularaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                      radialaxis=dict(gridcolor="rgba(255,255,255,0.06)", range=[70, 105])),
            **self._theme()["layout"],
            title=dict(text="Multi-Metric Radar", font=dict(size=16, color="#f1f5f9")),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15), height=500)
        return fig

    # ── Confusion Matrix Heatmap ──
    def confusion_matrix(self, cm: np.ndarray, class_names: List[str]) -> go.Figure:
        fig = go.Figure(go.Heatmap(
            z=cm, x=class_names, y=class_names,
            colorscale=[[0, "#030712"], [0.3, "#0f172a"], [0.6, "#00f0ff"], [1, "#ff2a6d"]],
            text=cm, texttemplate="%{text}", textfont=dict(size=11, color="white"),
            hovertemplate="%{x} → %{y}: %{z}<extra></extra>"))
        fig.update_layout(**self._theme()["layout"],
            xaxis_title="Predicted", yaxis_title="Actual",
            title=dict(text="Confusion Matrix", font=dict(size=16, color="#f1f5f9")),
            height=max(400, len(class_names) * 50 + 100))
        return fig

    # ── ROC Curves (multi-class) ──
    def roc_curves(self, y_test: np.ndarray, y_prob: np.ndarray,
                   class_names: List[str], top_n: int = 5) -> go.Figure:
        fig = go.Figure()
        n_classes = y_prob.shape[1]
        for i in range(min(top_n, n_classes)):
            y_bin = (y_test == i).astype(int)
            fpr, tpr, _ = roc_curve(y_bin, y_prob[:, i])
            fig.add_trace(go.Scatter(
                x=fpr, y=tpr, mode="lines",
                name=f"{class_names[i]} (AUC={auc(fpr,tpr):.3f})",
                line=dict(color=ATTACK_COLORS.get(class_names[i], "#64748b"), width=2),
                hovertemplate="FPR=%{x:.3f} TPR=%{y:.3f}<extra></extra>"))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines",
            line=dict(dash="dash", color="rgba(255,255,255,0.15)"), showlegend=False))
        fig.update_layout(**self._theme()["layout"],
            xaxis_title="False Positive Rate", yaxis_title="True Positive Rate",
            title=dict(text="ROC Curves (One-vs-Rest)", font=dict(size=16, color="#f1f5f9")),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2), height=500)
        return fig

    # ── Feature Importance ──
    def feature_importance(self, imp_df: pd.DataFrame, top_n: int = 20) -> go.Figure:
        df = imp_df.head(top_n).sort_values("importance", ascending=True)
        colors = [f"rgba(0, 240, 255, {0.3 + 0.7 * v / df['importance'].max()})" for v in df["importance"]]
        fig = go.Figure(go.Bar(
            orientation="h", y=df["feature"], x=df["importance"],
            marker_color=colors,
            text=[f"{v:.4f}" for v in df["importance"]], textposition="outside",
            hovertemplate="%{y}: %{x:.4f}<extra></extra>"))
        fig.update_layout(**self._theme()["layout"],
            xaxis_title="Importance (Gini)", height=max(300, len(df) * 35),
            showlegend=False,
            title=dict(text="Feature Importance (Random Forest)", font=dict(size=16, color="#f1f5f9")))
        return fig

    # ── Class Distribution ──
    def class_distribution(self, dist: Dict[str, int]) -> go.Figure:
        labels = list(dist.keys())
        values = list(dist.values())
        colors = [ATTACK_COLORS.get(l, "#64748b") for l in labels]
        fig = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.65,
            marker=dict(colors=colors, line=dict(color="#0f172a", width=2)),
            textinfo="percent", textfont=dict(size=12, color="white"),
            hovertemplate="%{label}: %{value} samples (%{percent})<extra></extra>"))
        fig.update_layout(**self._theme()["layout"],
            title=dict(text="Class Distribution", font=dict(size=16, color="#f1f5f9")),
            showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.1), height=420)
        return fig

    # ── Cross-Validation Scores ──
    def cv_scores(self, cv_history: Dict[str, List[float]]) -> go.Figure:
        fig = go.Figure()
        for key, scores in cv_history.items():
            if not scores: continue
            fig.add_trace(go.Box(
                y=scores, name=MODEL_REGISTRY.get(key, {}).get("name", key),
                marker_color=MODEL_REGISTRY.get(key, {}).get("color", "#64748b"),
                boxmean="sd"))
        fig.update_layout(**self._theme()["layout"],
            yaxis_title="Accuracy", yaxis_range=[0.7, 1.02],
            title=dict(text="Cross-Validation Distribution (5-Fold)",
                      font=dict(size=16, color="#f1f5f9")),
            showlegend=False, height=max(350, len(cv_history) * 60))
        return fig

    # ── Training Time Comparison ──
    def training_time(self, results: Dict[str, Dict[str, float]]) -> go.Figure:
        df = pd.DataFrame(results).T.sort_values("train_time", ascending=True)
        colors = [MODEL_REGISTRY.get(k, {}).get("color", "#64748b") for k in df.index]
        fig = go.Figure(go.Bar(
            orientation="h", y=df.index.map(lambda k: MODEL_REGISTRY.get(k, {}).get("name", k)),
            x=df["train_time"], marker_color=colors,
            text=[f"{v:.1f}s" for v in df["train_time"]], textposition="outside",
            hovertemplate="%{y}: %{x:.2f}s<extra></extra>"))
        fig.update_layout(**self._theme()["layout"],
            xaxis_title="Training Time (seconds)",
            title=dict(text="Training Time Comparison", font=dict(size=16, color="#f1f5f9")),
            showlegend=False, height=max(250, len(df) * 50))
        return fig

    # ── Correlation Heatmap ──
    def correlation_heatmap(self, df: pd.DataFrame, top_n: int = 15) -> go.Figure:
        cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != "label"][:top_n]
        corr = df[cols].corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=cols, y=cols,
            colorscale=[[0,"#030712"],[0.5,"#0f172a"],[0.75,"#00f0ff"],[1,"#ff2a6d"]],
            zmin=-1, zmax=1, hovertemplate="%{x} vs %{y}: %{z:.3f}<extra></extra>"))
        fig.update_layout(**self._theme()["layout"],
            title=dict(text="Feature Correlation Matrix", font=dict(size=16, color="#f1f5f9")),
            height=600, xaxis_showgrid=False, yaxis_showgrid=False)
        return fig

    # ── Metric Gauges ──
    def metric_gauge(self, value: float, title: str, color: str = "#00f0ff") -> go.Figure:
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=value * 100,
            number={"suffix": "%", "font": {"size": 36, "color": color, "family": "Inter"}},
            title={"text": title, "font": {"size": 14, "color": "#94a3b8"}},
            gauge={"axis": {"range": [0, 100], "tickcolor": "rgba(255,255,255,0.1)",
                     "tickfont": {"color": "#64748b", "size": 10}},
                    "bar": {"color": color, "thickness": 0.15},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [{"range": [0,60], "color": "rgba(255,42,109,0.08)"},
                              {"range": [60,85], "color": "rgba(255,174,0,0.08)"},
                              {"range": [85,100], "color": "rgba(5,255,161,0.08)"}],
                    "threshold": {"line": {"color": color, "width": 2},
                                 "thickness": 0.8, "value": value * 100}}))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=200, margin=dict(l=20, r=20, t=30, b=10))
        return fig
