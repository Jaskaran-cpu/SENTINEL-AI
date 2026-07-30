import streamlit as st
import plotly.graph_objects as go
import networkx as nx
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, play_sound

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("scan"), height=0)

st.markdown('<div class="main-header">🌍 LIVE THREAT MAP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Network Topology, Attack Vectors & Geospatial Intelligence</div>', unsafe_allow_html=True)

G = nx.DiGraph()
nodes = {"Internet": (0,0), "Firewall": (2,0), "Web Server": (4,1.2), "DB Server": (4,-1.2),
         "App Server": (5,0), "Workstation A": (6.5,2), "Workstation B": (6.5,-2),
         "Attacker 1": (-2,2), "Attacker 2": (-2,-2), "Botnet C&C": (-3.5,0),
         "CDN": (3,2.5), "IDS": (3,-2.5), "DNS Server": (6,1), "Mail Server": (6,-1)}
for node, pos in nodes.items():
    G.add_node(node, pos=pos)

normal_edges = [("Internet","Firewall"),("Firewall","Web Server"),("Firewall","App Server"),
                ("App Server","DB Server"),("App Server","Workstation A"),("App Server","Workstation B"),
                ("CDN","Web Server"),("Firewall","IDS"),("App Server","DNS Server"),("App Server","Mail Server")]
attack_edges = [("Attacker 1","Internet"),("Attacker 2","Internet"),
                ("Botnet C&C","Attacker 1"),("Botnet C&C","Attacker 2")]

for edge in normal_edges: G.add_edge(*edge, type="normal")
for edge in attack_edges: G.add_edge(*edge, type="attack")

pos = nx.get_node_attributes(G, "pos")
fig = go.Figure()

for edge in normal_edges:
    x0,y0 = pos[edge[0]]; x1,y1 = pos[edge[1]]
    fig.add_trace(go.Scatter(x=[x0,x1], y=[y0,y1], mode="lines",
                             line=dict(color="rgba(5,255,161,0.25)", width=1.5), hoverinfo="none", showlegend=False))

for edge in attack_edges:
    x0,y0 = pos[edge[0]]; x1,y1 = pos[edge[1]]
    fig.add_trace(go.Scatter(x=[x0,x1], y=[y0,y1], mode="lines",
                             line=dict(color="rgba(255,42,109,0.7)", width=3.5), hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter(x=[x0,x1], y=[y0,y1], mode="lines",
                             line=dict(color="rgba(255,42,109,0.12)", width=14), hoverinfo="none", showlegend=False))

node_x, node_y, node_colors, node_sizes, node_labels, node_symbols = [], [], [], [], [], []
for node in G.nodes():
    x,y = pos[node]
    node_x.append(x); node_y.append(y); node_labels.append(node)
    if "Attacker" in node or "Botnet" in node:
        node_colors.append("#ff2a6d"); node_sizes.append(50); node_symbols.append("x")
    elif "Firewall" in node or "IDS" in node:
        node_colors.append("#ffae00"); node_sizes.append(38); node_symbols.append("diamond")
    elif "CDN" in node or "DNS" in node or "Mail" in node:
        node_colors.append("#b829dd"); node_sizes.append(32); node_symbols.append("square")
    else:
        node_colors.append("#00f0ff"); node_sizes.append(30); node_symbols.append("circle")

fig.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers+text",
                         marker=dict(size=node_sizes, color=node_colors, line=dict(width=2, color="white"), symbol=node_symbols),
                         text=node_labels, textposition="top center",
                         textfont=dict(size=10, color="#e2e8f0", family="JetBrains Mono")))

fig.update_layout(template="plotly_dark", showlegend=False, height=550,
                  title=dict(text="Network Topology — Active DDoS Attack in Progress",
                             font=dict(color="#e2e8f0", size=14, family="JetBrains Mono")),
                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  plot_bgcolor="rgba(5,8,20,0.4)", paper_bgcolor="rgba(0,0,0,0)",
                  margin=dict(l=20, r=20, t=60, b=20), font=dict(family="JetBrains Mono", size=10))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🚨 Active Attack Details")
c1, c2, c3 = st.columns(3)
attack_details = [
    ("🔴 DDoS Attack", "#ff2a6d", "Source: 45.23.112.8 [RU]<br>Target: Web Server (192.168.1.10)<br>Volume: <b>12,400 req/s</b> | Baseline: 450<br>Confidence: 99.1% | Duration: 18 min"),
    ("🟡 Port Scan Campaign", "#ffae00", "Source: 103.45.67.12 [CN]<br>Target: Firewall (192.168.1.1)<br>Ports: 22, 80, 443, 3306, 8080<br>Type: SYN Stealth | Confidence: 94.3%"),
    ("🔵 Brute Force Attempt", "#00f0ff", "Source: 78.192.45.3 [BR]<br>Target: SSH Server (192.168.1.5:22)<br>Attempts: 1,247 failed logins<br>Usernames: root, admin, ubuntu, oracle"),
]
for col, (title, color, desc) in zip([c1, c2, c3], attack_details):
    r,g,b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba({r},{g},{b},0.08),rgba({r},{g},{b},0.02));
                    border:1px solid rgba({r},{g},{b},0.25); border-radius:12px; padding:16px;">
            <div style="color:{color};font-weight:700;font-family:'JetBrains Mono';font-size:1rem;">{title}</div>
            <div style="color:#94a3b8;font-size:0.8rem;margin-top:8px;line-height:1.7;">{desc}</div>
            <div style="margin-top:10px;height:3px;background:linear-gradient(90deg,{color},transparent);border-radius:2px;"></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("🌐 Attack Origin Geolocation")
countries = ["RU", "CN", "BR", "UA", "KP", "VN", "NG", "IR"]
latencies = [45, 120, 180, 60, 200, 150, 220, 170]
severities = [95, 88, 72, 85, 98, 80, 68, 92]
attack_counts = [342, 287, 156, 203, 89, 134, 78, 198]
colors_geo = [f"rgba(255,42,109,{s/120})" for s in severities]
fig_geo = go.Figure()
fig_geo.add_trace(go.Scatter(x=list(range(len(countries))), y=latencies, mode="markers+text",
                             marker=dict(size=[s/2.5 for s in severities], color=colors_geo, line=dict(color="white", width=1)),
                             text=countries, textposition="top center",
                             textfont=dict(color="#e2e8f0", size=12, family="JetBrains Mono"),
                             customdata=attack_counts,
                             hovertemplate="<b>%{text}</b><br>Latency: %{y}ms<br>Attacks: %{customdata}<extra></extra>",
                             name="Attack Sources"))
fig_geo.update_layout(template="plotly_dark", height=320,
                      xaxis=dict(showgrid=False, showticklabels=False),
                      yaxis=dict(title="Network Latency (ms)", gridcolor="rgba(255,255,255,0.04)"),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                      margin=dict(l=40, r=40, t=20, b=40), font=dict(family="JetBrains Mono", size=10))
st.plotly_chart(fig_geo, use_container_width=True)

st.subheader("📊 Attack Volume by Region")
fig_bar = go.Figure(go.Bar(x=countries, y=attack_counts,
                           marker_color=["#ff2a6d" if c > 200 else "#ffae00" if c > 100 else "#00f0ff" for c in attack_counts],
                           marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1))
fig_bar.update_layout(template="plotly_dark", height=280, xaxis_title="Country", yaxis_title="Attack Count",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(5,8,20,0.3)",
                      margin=dict(l=40, r=40, t=20, b=40), font=dict(family="JetBrains Mono", size=10))
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.caption("🛡️ Sentinel AI v6.2.0 — Live Threat Intelligence | Data refreshes every 30s")