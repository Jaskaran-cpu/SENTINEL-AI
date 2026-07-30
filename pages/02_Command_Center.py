import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, get_attack_data, generate_live_metrics, play_sound

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("boot"), height=0)

st.markdown('<div class="main-header typewriter-cursor">🏠 COMMAND CENTER</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-Time Network Security Monitoring & AI Threat Intelligence</div>', unsafe_allow_html=True)

m=generate_live_metrics()
c1,c2,c3,c4=st.columns(4)
for col,val,lab,clr,dt in [(c1,f"{m['active_flows']:,}","Active Flows","#00f0ff","+2.4% vs last hour"),
    (c2,f"{m['accuracy']:.1f}%","Detection Accuracy","#05ffa1","+0.3% today"),
    (c3,f"{m['active_threats']}","Active Threats","#ff2a6d","+3 since last check"),
    (c4,f"{m['auc']:.3f}","AUC-ROC Score","#ffae00","Ensemble model")]:
    with col: st.markdown(f'<div class="metric-card scan-line"><div class="metric-value" style="color:{clr};">{val}</div><div class="metric-label">{lab}</div><div class="metric-delta" style="color:{clr};">{dt}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
c5,c6,c7,c8=st.columns(4)
tl="CRITICAL" if m["threat_score"]>80 else "HIGH" if m["threat_score"]>60 else "MEDIUM"
tc="#ff2a6d" if tl=="CRITICAL" else "#ffae00" if tl=="HIGH" else "#05ffa1"
pl="threat-pulse" if tl=="CRITICAL" else ""
for col,val,lab,clr,dt in [(c5,f"{m['blocked_ips']}","Blocked IPs","#b829dd","Last 24h"),
    (c6,f"{m['mitigated']}","Threats Mitigated","#05ffa1","Today"),
    (c7,f"{m['pending']}","Pending Review","#ffae00","Requires action")]:
    with col: st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{clr};">{val}</div><div class="metric-label">{lab}</div><div class="metric-delta" style="color:{clr};">{dt}</div></div>', unsafe_allow_html=True)
with c8: st.markdown(f'<div class="metric-card alert-critical"><div class="metric-value {pl}" style="color:{tc};">{tl}</div><div class="metric-label">Threat Level</div><div class="metric-delta" style="color:{tc};">Score: {m["threat_score"]}/100</div></div>', unsafe_allow_html=True)

st.markdown("---")
left,right=st.columns([2,1])
with left:
    st.subheader("📊 Real-Time Traffic Monitor")
    tp=list(range(60)); np.random.seed(42)
    nm=[450+np.random.normal(0,25) for _ in tp]
    an=[0]*42+[np.random.normal(200,50) for _ in range(6)]+[1200+np.random.normal(0,200) for _ in range(12)]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=tp,y=nm,mode="lines",name="Normal",line=dict(color="#05ffa1",width=2),fill="tozeroy",fillcolor="rgba(5,255,161,.06)"))
    fig.add_trace(go.Scatter(x=tp,y=an,mode="lines",name="Anomalous",line=dict(color="#ff2a6d",width=2.5),fill="tozeroy",fillcolor="rgba(255,42,109,.12)"))
    fig.add_hline(y=800,line_dash="dash",line_color="#ffae00",annotation_text="Alert Threshold")
    fig.add_vrect(x0=42,x1=60,fillcolor="rgba(255,42,109,.08)",layer="below",line_width=0)
    fig.add_annotation(x=51,y=1300,text="⚠️ ATTACK DETECTED",showarrow=False,font=dict(color="#ff2a6d",size=14,family="JetBrains Mono"),bgcolor="rgba(5,8,20,.85)")
    fig.update_layout(template="plotly_dark",height=420,xaxis_title="Time (seconds)",yaxis_title="Requests/Second",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,x=.5,xanchor="center"),margin=dict(l=40,r=40,t=60,b=40),
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(5,8,20,.3)",font=dict(family="JetBrains Mono",size=10))
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("🎯 Threat Level Gauge")
    fig=go.Figure(go.Indicator(mode="gauge+number+delta",value=m["threat_score"],
        domain={"x":[0,1],"y":[0,1]},title={"text":"Threat Score","font":{"size":16,"color":"#64748b"}},
        number={"font":{"size":40,"color":"#ff2a6d","family":"JetBrains Mono"},"suffix":"/100"},
        delta={"reference":50,"increasing":{"color":"#ff2a6d"}},
        gauge={"axis":{"range":[0,100],"tickcolor":"#334155"},"bar":{"color":"#ff2a6d","thickness":.75},
            "bgcolor":"rgba(5,8,20,.5)","borderwidth":2,"bordercolor":"rgba(0,240,255,.2)",
            "steps":[{"range":[0,40],"color":"rgba(5,255,161,.1)"},{"range":[40,70],"color":"rgba(255,174,0,.1)"},
                     {"range":[70,100],"color":"rgba(255,42,109,.15)"}],
            "threshold":{"line":{"color":"white","width":3},"thickness":.8,"value":m["threat_score"]}}))
    fig.update_layout(template="plotly_dark",height=350,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",margin=dict(l=30,r=30,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""<div style="background:rgba(255,42,109,.06);border:1px solid rgba(255,42,109,.2);border-radius:8px;padding:10px;margin-top:8px;">
        <div style="color:#ff2a6d;font-family:'JetBrains Mono',monospace;font-size:.75rem;font-weight:700;">🔴 CRITICAL ALERT</div>
        <div style="color:#94a3b8;font-family:'JetBrains Mono',monospace;font-size:.65rem;margin-top:4px;">DDoS from 45.23.112.8 — 12,400 req/s</div></div>""", unsafe_allow_html=True)

st.markdown("---")
left2,right2=st.columns([1.2,1])
with left2:
    st.subheader("⚡ Live Attack Timeline")
    sc={"CRITICAL":"#ff2a6d","HIGH":"#ffae00","MEDIUM":"#00f0ff","LOW":"#05ffa1"}
    ti={"DDoS":"🌊","Port Scan":"🔭","Brute Force":"🔑","Botnet":"🤖","Infiltration":"🕳️","SQL Injection":"💉","XSS":"💻","Ransomware":"🔒"}
    for a in get_attack_data()[:7]:
        c=sc.get(a["severity"],"#fff"); ic=ti.get(a["type"],"⚠️")
        st.markdown(f"""<div style="background:linear-gradient(90deg,rgba(5,8,20,.7),rgba(15,20,45,.5));padding:12px 16px;border-radius:10px;margin:5px 0;border-left:3px solid {c};">
            <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:#475569;font-size:.7rem;font-weight:500;font-family:'JetBrains Mono';">{a['time']}</span><span style="background:{c};color:#000;padding:2px 10px;border-radius:4px;font-size:.65rem;font-weight:700;">{a['severity']}</span></div>
            <div style="margin-top:5px;"><span style="color:white;font-weight:600;font-size:.9rem;">{ic} {a['type']}</span><span style="color:#475569;font-size:.75rem;"> from {a['source']} [{a['country']}]</span></div>
            <div style="margin-top:3px;color:#334155;font-size:.7rem;">Target: {a['target']} | Confidence: {a['confidence']}</div></div>""", unsafe_allow_html=True)

with right2:
    st.subheader("🤖 Model Performance Radar")
    cats=["Accuracy","Precision","Recall","F1","AUC","Speed"]
    fig=go.Figure()
    for nm,vs,cl,w in [("RF",[.962,.958,.961,.959,.987,.95],"#3b82f6",1.5),("XGB",[.981,.979,.982,.980,.994,.92],"#ffae00",1.5),
                        ("BiLSTM",[.987,.985,.988,.986,.996,.78],"#b829dd",1.5),("Ensemble",[.993,.992,.993,.992,.998,.70],"#00f0ff",2.5)]:
        r,g,b=int(cl[1:3],16),int(cl[3:5],16),int(cl[5:7],16)
        fig.add_trace(go.Scatterpolar(r=vs+[vs[0]],theta=cats+[cats[0]],fill="toself",name=nm,line_color=cl,line_width=w,fillcolor=f"rgba({r},{g},{b},.06)"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,1],gridcolor="rgba(255,255,255,.04)")),
        template="plotly_dark",height=420,font=dict(family="JetBrains Mono",size=10),
        legend=dict(orientation="h",yanchor="bottom",y=-.25,x=.5,xanchor="center"),margin=dict(l=40,r=40,t=40,b=40),paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
bw1,bw2=st.columns(2)
with bw1:
    st.subheader("📈 Bandwidth (24h)")
    hrs=list(range(24)); np.random.seed(42)
    fig=go.Figure()
    fig.add_trace(go.Bar(x=hrs,y=[np.random.normal(4.2,.8) for _ in hrs],name="Inbound",marker_color="rgba(0,240,255,.6)"))
    fig.add_trace(go.Bar(x=hrs,y=[np.random.normal(2.1,.5) for _ in hrs],name="Outbound",marker_color="rgba(184,41,221,.6)"))
    fig.update_layout(template="plotly_dark",barmode="stack",height=300,xaxis_title="Hour",yaxis_title="Gbps",
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(5,8,20,.3)",margin=dict(l=40,r=40,t=30,b=40),font=dict(family="JetBrains Mono",size=10))
    st.plotly_chart(fig, use_container_width=True)
with bw2:
    st.subheader("🔌 Protocol Distribution")
    fig=go.Figure(go.Pie(labels=["TCP","UDP","ICMP","HTTP","HTTPS","DNS","SSH"],values=[35,20,5,15,18,5,2],hole=.55,
        marker=dict(colors=["#00f0ff","#b829dd","#ff2a6d","#05ffa1","#ffae00","#3b82f6","#f472b6"],line=dict(color="#04060e",width=2))))
    fig.update_traces(textinfo="percent+label",textfont_size=11,textfont_color="#e2e8f0")
    fig.update_layout(template="plotly_dark",height=300,showlegend=False,paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=20,r=20,t=20,b=20),font=dict(family="JetBrains Mono",size=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("🛡️ Sentinel AI v3.0.0 — Command Center | Neural Engine Active")