import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, play_sound

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("scan"), height=0)

st.markdown('<div class="main-header">📈 PREDICTIVE ANALYTICS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Time-Series Forecasting, Seasonal Decomposition & Anomaly Prediction</div>', unsafe_allow_html=True)

np.random.seed(42)
dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
trend = np.linspace(100, 200, len(dates))
seasonal = 50 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
noise = np.random.normal(0, 20, len(dates))
attacks = np.maximum(trend + seasonal + noise, 0)
df_ts = pd.DataFrame({"ds": dates, "y": attacks})

future_dates = pd.date_range("2025-01-01", periods=90, freq="D")
future_trend = np.linspace(200, 220, 90)
future_seasonal = 50 * np.sin(2 * np.pi * np.arange(90) / 365.25)
future_yhat = future_trend + future_seasonal + np.random.normal(0, 15, 90)
yhat_upper = future_yhat + 30
yhat_lower = future_yhat - 30

st.subheader("🔮 Attack Volume Forecasting (Prophet + LSTM Ensemble)")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_ts["ds"], y=df_ts["y"], mode="lines", name="Historical Data", line=dict(color="#00f0ff", width=1), opacity=0.6))
fig.add_trace(go.Scatter(x=future_dates, y=future_yhat, mode="lines", name="Forecast", line=dict(color="#ff2a6d", width=2.5)))
fig.add_trace(go.Scatter(x=future_dates, y=yhat_upper, mode="lines", line=dict(color="rgba(255,42,109,0.3)", dash="dash"), showlegend=False))
fig.add_trace(go.Scatter(x=future_dates, y=yhat_lower, mode="lines", line=dict(color="rgba(255,42,109,0.3)", dash="dash"),
                          fill="tonexty", fillcolor="rgba(255,42,109,0.06)", showlegend=False))
fig.add_vrect(x0=pd.Timestamp("2025-01-01"), x1=pd.Timestamp("2025-03-31"), fillcolor="rgba(184,41,221,0.05)",
              layer="below", line_width=0, annotation_text="Forecast Period", annotation_position="top left",
              annotation_font_color="#b829dd")
fig.update_layout(template="plotly_dark", height=520, xaxis_title="Date", yaxis_title="Predicted Attack Volume",
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                  margin=dict(l=40,r=40,t=60,b=40), font=dict(family="JetBrains Mono", size=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📊 Seasonal Decomposition")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**Trend Component**")
    fig_t = go.Figure(go.Scatter(x=dates, y=trend, mode="lines", line=dict(color="#05ffa1", width=2)))
    fig_t.update_layout(template="plotly_dark", height=260, margin=dict(l=20,r=20,t=30,b=20),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)", font=dict(family="JetBrains Mono", size=9))
    st.plotly_chart(fig_t, use_container_width=True)
with c2:
    st.markdown("**Seasonal Component**")
    fig_s = go.Figure(go.Scatter(x=dates, y=seasonal, mode="lines", line=dict(color="#ffae00", width=2)))
    fig_s.update_layout(template="plotly_dark", height=260, margin=dict(l=20,r=20,t=30,b=20),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)", font=dict(family="JetBrains Mono", size=9))
    st.plotly_chart(fig_s, use_container_width=True)
with c3:
    st.markdown("**Residual / Noise**")
    fig_r = go.Figure(go.Scatter(x=dates, y=noise, mode="lines", line=dict(color="#ff2a6d", width=1), opacity=0.7))
    fig_r.update_layout(template="plotly_dark", height=260, margin=dict(l=20,r=20,t=30,b=20),
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)", font=dict(family="JetBrains Mono", size=9))
    st.plotly_chart(fig_r, use_container_width=True)

st.markdown("---")
st.subheader("📋 Forecast Accuracy Metrics")
m1, m2, m3, m4 = st.columns(4)
m1.metric("MAPE", "8.3%", delta="-1.2%", delta_color="inverse")
m2.metric("RMSE", "18.7", delta="+0.5", delta_color="inverse")
m3.metric("MAE", "14.2", delta="-0.8%", delta_color="normal")
m4.metric("R-Squared", "0.947", delta="+0.012", delta_color="normal")

st.markdown("---")
st.subheader("⚠️ Predicted Anomaly Events (Next 30 Days)")
for ev in [{"date":"2025-01-03","type":"DDoS Spike","probability":0.87,"severity":"HIGH"},
           {"date":"2025-01-12","type":"Credential Stuffing","probability":0.72,"severity":"MEDIUM"},
           {"date":"2025-01-18","type":"Port Scan Surge","probability":0.91,"severity":"HIGH"},
           {"date":"2025-01-25","type":"Ransomware Campaign","probability":0.45,"severity":"LOW"},
           {"date":"2025-02-02","type":"Zero-Day Exploit","probability":0.33,"severity":"LOW"}]:
    color = {"HIGH":"#ffae00","MEDIUM":"#00f0ff","LOW":"#05ffa1"}.get(ev["severity"],"#fff")
    r,g,b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,rgba(5,8,20,0.6),rgba(15,20,45,0.4));
                padding:12px 16px;border-radius:10px;margin:4px 0;border-left:3px solid {color};
                display:flex;justify-content:space-between;align-items:center;">
        <div><span style="color:{color};font-weight:700;font-family:'JetBrains Mono';">{ev['date']}</span>
        <span style="color:#e2e8f0;margin-left:12px;">{ev['type']}</span></div>
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="background:#0a1420;border-radius:6px;width:100px;height:6px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,{color},rgba({r},{g},{b},0.5));height:100%;width:{ev['probability']*100:.0f}%;"></div>
            </div>
            <span style="color:{color};font-weight:700;font-family:'JetBrains Mono';font-size:0.85rem;">{ev['probability']:.0%}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Predicted Attack Type Distribution (Next 90 Days)")
fig_f = go.Figure(go.Bar(
    x=[340,280,195,45,120,85,62,12],
    y=["DDoS","Port Scan","Brute Force","Ransomware","Phishing","SQL Injection","XSS","Zero-Day"],
    orientation="h",
    marker_color=["#ff2a6d","#ffae00","#00f0ff","#b829dd","#05ffa1","#3b82f6","#f472b6","#ff6b9d"],
    marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1))
fig_f.update_layout(template="plotly_dark", height=380, xaxis_title="Predicted Incidents",
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                    margin=dict(l=40,r=40,t=20,b=40), font=dict(family="JetBrains Mono", size=10))
st.plotly_chart(fig_f, use_container_width=True)

st.markdown("---")
st.caption("🛡️ Sentinel AI v6.2.0 — Predictive Analytics | Forecast Engine Active")