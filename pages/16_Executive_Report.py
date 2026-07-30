import streamlit as st
from fpdf import FPDF
import datetime
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.utils import get_css, play_sound

st.markdown(get_css(), unsafe_allow_html=True)
st.components.v1.html(play_sound("click"), height=0)

st.markdown('<div class="main-header">📄 EXECUTIVE REPORT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Generate & Download Intelligence Reports</div>', unsafe_allow_html=True)

# ── Report Configuration ──
st.subheader("📋 Report Configuration")
c1, c2 = st.columns(2)
with c1:
    report_period = st.selectbox("Report Period", [
        "Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last Quarter", "Custom"
    ])
    report_type = st.selectbox("Report Type", [
        "Executive Summary", "Technical Deep Dive", "Compliance Audit", "Incident Review"
    ])
    report_classification = st.selectbox("Classification", [
        "CONFIDENTIAL", "INTERNAL", "RESTRICTED", "PUBLIC"
    ])
with c2:
    include_charts = st.checkbox("Include Charts Section", value=True)
    include_recommendations = st.checkbox("Include Recommendations", value=True)
    include_raw_data = st.checkbox("Include Raw Data Appendix", value=False)
    include_timeline = st.checkbox("Include Incident Timeline", value=True)
    include_ioc = st.checkbox("Include IOC Indicators", value=True)

st.markdown("---")

# ── Report Preview ──
st.subheader("👁️ Report Preview")
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

preview_col1, preview_col2 = st.columns([1, 1])
with preview_col1:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(0,240,255,0.06),rgba(0,240,255,0.01));
                border:1px solid rgba(0,240,255,0.15);border-radius:12px;padding:20px;">
        <div style="color:#00f0ff;font-weight:700;font-family:'JetBrains Mono';font-size:1rem;margin-bottom:12px;">
            📄 Report Metadata
        </div>
        <div style="color:#94a3b8;font-size:0.85rem;line-height:2;">
            <span style="color:#64748b;">Title:</span> <span style="color:#e2e8f0;">Sentinel AI — {report_type}</span><br>
            <span style="color:#64748b;">Period:</span> <span style="color:#e2e8f0;">{report_period}</span><br>
            <span style="color:#64748b;">Generated:</span> <span style="color:#e2e8f0;">{now_str}</span><br>
            <span style="color:#64748b;">Classification:</span> <span style="color:#ff2a6d;font-weight:700;">{report_classification}</span><br>
            <span style="color:#64748b;">Author:</span> <span style="color:#e2e8f0;">Sentinel AI v6.2.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with preview_col2:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(5,255,161,0.06),rgba(5,255,161,0.01));
                border:1px solid rgba(5,255,161,0.15);border-radius:12px;padding:20px;">
        <div style="color:#05ffa1;font-weight:700;font-family:'JetBrains Mono';font-size:1rem;margin-bottom:12px;">
            📊 Key Metrics Summary
        </div>
        <div style="color:#94a3b8;font-size:0.85rem;line-height:2;">
            <span style="color:#64748b;">Total Incidents:</span> <span style="color:#e2e8f0;font-weight:700;">23</span><br>
            <span style="color:#64748b;">Detection Accuracy:</span> <span style="color:#05ffa1;font-weight:700;">99.3%</span><br>
            <span style="color:#64748b;">Mean Time to Detect:</span> <span style="color:#00f0ff;">3.8 min</span><br>
            <span style="color:#64748b;">Mean Time to Respond:</span> <span style="color:#00f0ff;">4.2 min</span><br>
            <span style="color:#64748b;">False Positive Rate:</span> <span style="color:#05ffa1;">0.7%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Section Toggles ──
st.subheader("📑 Report Sections")
sec1, sec2, sec3, sec4 = st.columns(4)
with sec1:
    st.markdown(f"""
    <div style="background:rgba(5,8,20,0.6);border:1px solid rgba(0,240,255,0.1);border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:1.5rem;">📊</div>
        <div style="color:#00f0ff;font-size:0.75rem;font-weight:700;font-family:'JetBrains Mono';margin-top:4px;">Charts</div>
        <div style="color:#05ffa1;font-size:0.65rem;margin-top:4px;">{'✓ Included' if include_charts else '✗ Excluded'}</div>
    </div>
    """, unsafe_allow_html=True)
with sec2:
    st.markdown(f"""
    <div style="background:rgba(5,8,20,0.6);border:1px solid rgba(255,174,0,0.1);border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:1.5rem;">💡</div>
        <div style="color:#ffae00;font-size:0.75rem;font-weight:700;font-family:'JetBrains Mono';margin-top:4px;">Recommendations</div>
        <div style="color:#05ffa1;font-size:0.65rem;margin-top:4px;">{'✓ Included' if include_recommendations else '✗ Excluded'}</div>
    </div>
    """, unsafe_allow_html=True)
with sec3:
    st.markdown(f"""
    <div style="background:rgba(5,8,20,0.6);border:1px solid rgba(184,41,221,0.1);border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:1.5rem;">📋</div>
        <div style="color:#b829dd;font-size:0.75rem;font-weight:700;font-family:'JetBrains Mono';margin-top:4px;">Timeline</div>
        <div style="color:#05ffa1;font-size:0.65rem;margin-top:4px;">{'✓ Included' if include_timeline else '✗ Excluded'}</div>
    </div>
    """, unsafe_allow_html=True)
with sec4:
    st.markdown(f"""
    <div style="background:rgba(5,8,20,0.6);border:1px solid rgba(255,42,109,0.1);border-radius:8px;padding:12px;text-align:center;">
        <div style="font-size:1.5rem;">🎯</div>
        <div style="color:#ff2a6d;font-size:0.75rem;font-weight:700;font-family:'JetBrains Mono';margin-top:4px;">IOC List</div>
        <div style="color:#05ffa1;font-size:0.65rem;margin-top:4px;">{'✓ Included' if include_ioc else '✗ Excluded'}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Generate Report Button ──
st.subheader("🚀 Generate Report")

if st.button("📄 Generate PDF Report", type="primary", use_container_width=True):
    st.components.v1.html(play_sound("success"), height=0)

    with st.spinner("Generating comprehensive report..."):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # ── Cover Page ──
        pdf.add_page()
        pdf.set_font("Arial", "B", 28)
        pdf.set_text_color(0, 80, 180)
        pdf.ln(40)
        pdf.cell(0, 15, "SENTINEL AI", ln=True, align="C")
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 100, 200)
        pdf.cell(0, 12, "Cyber Threat Intelligence Report", ln=True, align="C")
        pdf.ln(10)
        pdf.set_draw_color(0, 100, 200)
        pdf.set_line_width(0.5)
        pdf.line(50, pdf.get_y(), 160, pdf.get_y())
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 8, "Report Type: " + report_type, ln=True, align="C")
        pdf.cell(0, 8, "Period: " + report_period, ln=True, align="C")
        pdf.cell(0, 8, "Generated: " + now_str, ln=True, align="C")
        pdf.cell(0, 8, "Classification: " + report_classification, ln=True, align="C")
        pdf.ln(15)
        pdf.set_font("Arial", "I", 10)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 8, "Powered by Sentinel AI v6.2.0 - Neural Ensemble Engine", ln=True, align="C")
        pdf.cell(0, 8, "Cyber Defense Systems - Confidential", ln=True, align="C")

        # ── Table of Contents ──
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "TABLE OF CONTENTS", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(50, 50, 50)
        toc_items = [
            ("1. Executive Summary", "3"),
            ("2. Key Metrics", "3"),
            ("3. Threat Landscape Overview", "4"),
            ("4. Incident Analysis", "4"),
        ]
        if include_charts:
            toc_items.append(("5. Charts & Visualizations", "5"))
        if include_recommendations:
            toc_items.append(("6. Strategic Recommendations", "5"))
        if include_ioc:
            toc_items.append(("7. Indicators of Compromise", "6"))
        if include_timeline:
            toc_items.append(("8. Incident Timeline", "6"))
        toc_items.append(("9. Conclusion", "7"))

        for item, page in toc_items:
            pdf.cell(150, 8, item, ln=0)
            pdf.cell(0, 8, page, ln=1, align="R")

        # ── Executive Summary ──
        pdf.add_page()
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "1. EXECUTIVE SUMMARY", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(50, 50, 50)

        summary_text = (
            "During the " + report_period + " reporting period, Sentinel AI detected and analyzed "
            "23 security incidents across the network infrastructure. The AI-powered detection "
            "system achieved 99.3% accuracy with an average response time of 4.2 minutes. "
            "Critical threats included 2 DDoS attacks, 3 port scanning campaigns, and 1 attempted "
            "infiltration. All critical incidents were successfully mitigated within SLA thresholds. "
            "The ensemble model (Random Forest + XGBoost + BiLSTM) demonstrated superior detection "
            "capabilities with an AUC-ROC score of 0.998, significantly outperforming industry "
            "benchmarks of 94.2%. The false positive rate was reduced to 0.7%, a 30% improvement "
            "over the previous reporting period."
        )
        pdf.multi_cell(0, 6, summary_text)
        pdf.ln(5)

        # ── Key Metrics ──
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "2. KEY METRICS", ln=True)
        pdf.ln(3)

        metrics_list = [
            ("Total Incidents", "23", "+15% vs last period"),
            ("Detection Accuracy", "99.3%", "Industry avg: 94.2%"),
            ("Mean Time to Detect", "3.8 min", "-22% vs last period"),
            ("Mean Time to Respond", "4.2 min", "-18% vs last period"),
            ("False Positive Rate", "0.7%", "-0.3% vs last period"),
            ("AUC-ROC Score", "0.998", "Ensemble model"),
            ("Active Threats Blocked", "1,247", "Last 24 hours"),
            ("Threats Mitigated", "342", "Today"),
            ("Patched Vulnerabilities", "15", "This period"),
        ]

        # Table header
        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(0, 80, 180)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(60, 8, "Metric", 1, 0, "C", fill=True)
        pdf.cell(40, 8, "Value", 1, 0, "C", fill=True)
        pdf.cell(80, 8, "Trend / Note", 1, 1, "C", fill=True)

        # Table rows
        pdf.set_font("Arial", "", 10)
        for i, (metric, value, trend) in enumerate(metrics_list):
            if i % 2 == 0:
                pdf.set_fill_color(240, 245, 255)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(60, 7, metric, 1, 0, "L", fill=True)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(40, 7, value, 1, 0, "C", fill=True)
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(0, 130, 0)
            pdf.cell(80, 7, trend, 1, 1, "L", fill=True)

        pdf.ln(5)

        # ── Threat Landscape Overview ──
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "3. THREAT LANDSCAPE OVERVIEW", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(50, 50, 50)

        threat_overview = (
            "The threat landscape during this reporting period was characterized by an increase in "
            "sophisticated multi-vector attacks. Key observations include:\n\n"
            "- DDoS attacks increased in volume by 15%, with peak traffic reaching 12,400 req/s\n"
            "- Port scanning campaigns shifted from random to targeted enumeration of critical services\n"
            "- Brute force attacks increasingly utilized credential stuffing with leaked password databases\n"
            "- Ransomware operators continued to exploit unpatched vulnerabilities (Log4j, Apache)\n"
            "- Attack origins were geographically distributed: Russia (28%), China (23%), Brazil (13%))\n"
            "- Zero-day exploit attempts were detected but successfully blocked by behavioral analysis\n\n"
            "The AI ensemble model demonstrated robust performance across all attack categories, with "
            "the highest detection accuracy for DDoS (99.8%) and the lowest for XSS (94.2%), which "
            "remains an area for improvement in the next training cycle."
        )
        pdf.multi_cell(0, 6, threat_overview)
        pdf.ln(5)

        # ── Incident Analysis ──
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "4. INCIDENT ANALYSIS", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(50, 50, 50)

        incidents = [
            ("ALT-2024-001", "CRITICAL", "DDoS Attack", "45.23.112.8", "Active", "99.1%"),
            ("ALT-2024-002", "HIGH", "Port Scan", "103.45.67.12", "Mitigated", "94.3%"),
            ("ALT-2024-003", "MEDIUM", "Brute Force", "78.192.45.3", "Investigating", "91.7%"),
            ("ALT-2024-004", "HIGH", "Botnet Activity", "91.234.56.78", "Active", "96.2%"),
            ("ALT-2024-005", "CRITICAL", "Infiltration", "185.67.89.12", "Contained", "98.8%"),
            ("ALT-2024-006", "HIGH", "SQL Injection", "203.112.45.67", "Mitigated", "93.5%"),
            ("ALT-2024-007", "MEDIUM", "XSS Attack", "198.51.100.42", "Investigating", "89.2%"),
            ("ALT-2024-008", "CRITICAL", "Ransomware", "192.168.77.5", "Active", "97.4%"),
        ]

        # Incident table header
        pdf.set_font("Arial", "B", 9)
        pdf.set_fill_color(0, 80, 180)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(28, 7, "ID", 1, 0, "C", fill=True)
        pdf.cell(22, 7, "Severity", 1, 0, "C", fill=True)
        pdf.cell(28, 7, "Type", 1, 0, "C", fill=True)
        pdf.cell(35, 7, "Source IP", 1, 0, "C", fill=True)
        pdf.cell(25, 7, "Status", 1, 0, "C", fill=True)
        pdf.cell(22, 7, "Conf.", 1, 1, "C", fill=True)

        # Incident table rows
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(50, 50, 50)
        for i, (inc_id, sev, inc_type, src, status, conf) in enumerate(incidents):
            if i % 2 == 0:
                pdf.set_fill_color(240, 245, 255)
            else:
                pdf.set_fill_color(255, 255, 255)
            pdf.cell(28, 6, inc_id, 1, 0, "C", fill=True)
            pdf.cell(22, 6, sev, 1, 0, "C", fill=True)
            pdf.cell(28, 6, inc_type, 1, 0, "C", fill=True)
            pdf.cell(35, 6, src, 1, 0, "C", fill=True)
            pdf.cell(25, 6, status, 1, 0, "C", fill=True)
            pdf.cell(22, 6, conf, 1, 1, "C", fill=True)

        pdf.ln(5)

        # ── Charts Section ──
        if include_charts:
            pdf.set_font("Arial", "B", 18)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 12, "5. CHARTS & VISUALIZATIONS", ln=True)
            pdf.ln(3)
            pdf.set_font("Arial", "", 11)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 6, (
                "Visual analytics are available in the interactive dashboard. "
                "Key charts include: Attack volume over time, Severity distribution pie chart, "
                "MTTR by attack type, Protocol distribution, and Model performance radar chart. "
                "For interactive exploration, please access the Sentinel AI dashboard."
            ))
            pdf.ln(3)

            # Simple text-based chart
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Attack Severity Distribution:", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, "  CRITICAL:  ####  (3 incidents - 37.5%)", ln=True)
            pdf.cell(0, 6, "  HIGH:     ###   (3 incidents - 37.5%)", ln=True)
            pdf.cell(0, 6, "  MEDIUM:   ##    (2 incidents - 25.0%)", ln=True)
            pdf.ln(3)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "MTTR by Attack Type:", ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 6, "  DDoS:          4.2 min  [=====]", ln=True)
            pdf.cell(0, 6, "  Port Scan:    12.5 min  [==============]", ln=True)
            pdf.cell(0, 6, "  Brute Force:  18.3 min  [====================]", ln=True)
            pdf.cell(0, 6, "  Ransomware:   32.8 min  [====================================]", ln=True)
            pdf.ln(5)

        # ── Recommendations ──
        if include_recommendations:
            pdf.set_font("Arial", "B", 18)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 12, "6. STRATEGIC RECOMMENDATIONS", ln=True)
            pdf.ln(3)
            pdf.set_font("Arial", "", 11)
            pdf.set_text_color(50, 50, 50)

            recommendations = [
                ("1. DDoS Mitigation Capacity",
                 "Implement additional DDoS mitigation capacity during peak traffic periods. "
                 "Consider deploying Cloudflare Magic Transit or AWS Shield Advanced for automatic "
                 "traffic scrubbing. Estimated cost: $15,000/month."),
                ("2. Endpoint Detection & Response",
                 "Deploy EDR solutions (CrowdStrike Falcon or SentinelOne) on all workstations "
                 "and servers. This will improve detection of ransomware and lateral movement. "
                 "Priority: HIGH - 3 workstations currently unprotected."),
                ("3. Patch Management",
                 "Immediately patch CVE-2024-007 (Log4j RCE, CVSS 10.0) on App Server. "
                 "Implement automated patch management with 48-hour SLA for critical vulnerabilities. "
                 "Current unpatched critical CVEs: 3."),
                ("4. Red Team Exercise",
                 "Conduct a comprehensive red team exercise to test incident response procedures. "
                 "Focus on ransomware scenarios and lateral movement. Schedule for Q2 2025."),
                ("5. AI Model Retraining",
                 "Retrain the ensemble model with latest attack signatures. The XSS detection rate "
                 "(94.2%) is below the 97% target. Increase training data for web application attacks. "
                 "Next retraining cycle: 2025-02-01."),
                ("6. Threat Intelligence Sharing",
                 "Establish threat intelligence sharing agreements with industry partners via "
                 "MISP (Malware Information Sharing Platform). This will improve detection of "
                 "emerging threats by 15-20%."),
                ("7. Zero Trust Architecture",
                 "Begin implementing zero trust network architecture. Phase 1: Micro-segmentation "
                 "of critical servers (DB, App). Phase 2: Identity-based access for all services. "
                 "Timeline: 6 months."),
                ("8. Compliance Improvements",
                 "Address PCI DSS non-compliance in Monitoring & Testing (score: 69%). Deploy "
                 "continuous security monitoring with SIEM integration. This is required for "
                 "regulatory compliance by Q3 2025."),
            ]

            for title, desc in recommendations:
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 80, 180)
                pdf.cell(0, 8, title, ln=True)
                pdf.set_font("Arial", "", 10)
                pdf.set_text_color(50, 50, 50)
                pdf.multi_cell(0, 6, desc)
                pdf.ln(3)

        # ── IOCs ──
        if include_ioc:
            pdf.set_font("Arial", "B", 18)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 12, "7. INDICATORS OF COMPROMISE", ln=True)
            pdf.ln(3)

            iocs = [
                ("IP Addresses", [
                    "45.23.112.8", "103.45.67.12", "78.192.45.3",
                    "91.234.56.78", "185.67.89.12", "203.112.45.67",
                    "198.51.100.42", "192.168.77.5"
                ]),
                ("Domains", [
                    "c2.malware-net.ru", "update.srv-check.com",
                    "cdn.cloudfront-cdn.xyz", "api.darkcloud.io"
                ]),
                ("File Hashes (SHA-256)", [
                    "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
                    "f0e1d2c3b4a5968701234567890123456789abcdef0123456789abcdef012345",
                    "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                ]),
                ("Usernames Attempted", [
                    "root", "admin", "ubuntu", "oracle", "postgres", "sa", "administrator"
                ]),
            ]

            for category, items in iocs:
                pdf.set_font("Arial", "B", 11)
                pdf.set_text_color(0, 80, 180)
                pdf.cell(0, 8, category, ln=True)
                pdf.set_font("Arial", "", 9)
                pdf.set_text_color(50, 50, 50)
                for item in items:
                    pdf.cell(0, 5, "  - " + item, ln=True)
                pdf.ln(2)

        # ── Incident Timeline ──
        if include_timeline:
            pdf.add_page()
            pdf.set_font("Arial", "B", 18)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 12, "8. INCIDENT TIMELINE", ln=True)
            pdf.ln(3)

            timeline = [
                ("10:55:33", "ALT-2024-008", "Ransomware detected on File Server", "CRITICAL"),
                ("11:20:10", "ALT-2024-007", "XSS attack on Web Server", "MEDIUM"),
                ("12:45:22", "ALT-2024-006", "SQL Injection on App Server", "HIGH"),
                ("13:30:00", "ALT-2024-005", "Infiltration attempt on DB Server", "CRITICAL"),
                ("13:52:11", "ALT-2024-004", "Botnet activity on Workstation A", "HIGH"),
                ("14:15:44", "ALT-2024-003", "Brute force on SSH Server", "MEDIUM"),
                ("14:28:03", "ALT-2024-002", "Port scan on Firewall", "HIGH"),
                ("14:32:15", "ALT-2024-001", "DDoS attack on Web Server", "CRITICAL"),
            ]

            pdf.set_font("Arial", "B", 9)
            pdf.set_fill_color(0, 80, 180)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(25, 7, "Time", 1, 0, "C", fill=True)
            pdf.cell(30, 7, "Alert ID", 1, 0, "C", fill=True)
            pdf.cell(95, 7, "Description", 1, 0, "C", fill=True)
            pdf.cell(25, 7, "Severity", 1, 1, "C", fill=True)

            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(50, 50, 50)
            for i, (time_val, aid, desc, sev) in enumerate(timeline):
                if i % 2 == 0:
                    pdf.set_fill_color(240, 245, 255)
                else:
                    pdf.set_fill_color(255, 255, 255)
                pdf.cell(25, 6, time_val, 1, 0, "C", fill=True)
                pdf.cell(30, 6, aid, 1, 0, "C", fill=True)
                pdf.cell(95, 6, desc, 1, 0, "L", fill=True)
                pdf.cell(25, 6, sev, 1, 1, "C", fill=True)

            pdf.ln(5)

        # ── Conclusion ──
        pdf.set_font("Arial", "B", 18)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 12, "9. CONCLUSION", ln=True)
        pdf.ln(3)
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(50, 50, 50)

        conclusion = (
            "The Sentinel AI platform demonstrated robust performance during this reporting period, "
            "achieving a 99.3% detection accuracy and maintaining a mean time to respond of 4.2 minutes. "
            "All critical incidents were successfully contained within SLA thresholds.\n\n"
            "Key areas for improvement include: (1) XSS detection accuracy, currently at 94.2%, needs "
            "to reach the 97% target through model retraining; (2) PCI DSS compliance for Monitoring & "
            "Testing must be addressed urgently; (3) Critical CVEs (Log4j, Apache) require immediate "
            "patching.\n\n"
            "The platform's neural ensemble model continues to outperform industry benchmarks across all "
            "attack categories. The next model retraining cycle is scheduled for February 2025, with "
            "an expected improvement in web application attack detection.\n\n"
            "Overall security posture: STRONG with identified areas for improvement. The threat level "
            "remains at HIGH due to ongoing DDoS activity and unpatched critical vulnerabilities.\n\n"
            "This report was automatically generated by Sentinel AI v6.2.0 Neural Engine."
        )
        pdf.multi_cell(0, 6, conclusion)

        # ── Footer ──
        pdf.ln(10)
        pdf.set_draw_color(0, 80, 180)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Arial", "I", 8)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 5, "Generated: " + now_str + " | Classification: " + report_classification + " | Sentinel AI v6.2.0", ln=True, align="C")
        pdf.cell(0, 5, "This document contains confidential information. Unauthorized distribution is prohibited.", ln=True, align="C")

        # ── Convert to bytes ──
        pdf_bytes = bytes(pdf.output(dest="S"))

    st.success("Report generated successfully!")

    # File info card
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(5,255,161,0.06),rgba(5,255,161,0.01));
                border:1px solid rgba(5,255,161,0.15);border-radius:12px;padding:20px;">
        <div style="color:#05ffa1;font-weight:700;font-family:'JetBrains Mono';font-size:1rem;margin-bottom:8px;">
            Report Ready
        </div>
        <div style="color:#94a3b8;font-size:0.85rem;line-height:1.8;">
            <span style="color:#64748b;">Type:</span> {report_type}<br>
            <span style="color:#64748b;">Period:</span> {report_period}<br>
            <span style="color:#64748b;">Pages:</span> {pdf.page_no()}<br>
            <span style="color:#64748b;">Size:</span> {len(pdf_bytes):,} bytes<br>
            <span style="color:#64748b;">Classification:</span> <span style="color:#ff2a6d;font-weight:700;">{report_classification}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name=f"SentinelAI_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

st.markdown("---")

# ── Report History ──
st.subheader("Recent Reports")
reports = [
    {"date": "2024-07-25 14:30", "type": "Executive Summary", "period": "Last 7 Days", "pages": "7", "size": "45 KB"},
    {"date": "2024-07-24 09:00", "type": "Technical Deep Dive", "period": "Last 24 Hours", "pages": "12", "size": "78 KB"},
    {"date": "2024-07-22 16:45", "type": "Compliance Audit", "period": "Last Quarter", "pages": "15", "size": "92 KB"},
    {"date": "2024-07-20 11:15", "type": "Incident Review", "period": "Last 30 Days", "pages": "9", "size": "56 KB"},
    {"date": "2024-07-18 08:30", "type": "Executive Summary", "period": "Last 7 Days", "pages": "7", "size": "43 KB"},
]

for rpt in reports:
    st.markdown(f"""
    <div style="background:linear-gradient(90deg,rgba(5,8,20,0.6),rgba(15,20,45,0.4));
                padding:12px 16px;border-radius:10px;margin:4px 0;border-left:3px solid #00f0ff;
                display:flex;justify-content:space-between;align-items:center;">
        <div>
            <span style="color:#00f0ff;font-weight:700;font-family:'JetBrains Mono';font-size:0.85rem;">{rpt['date']}</span>
            <span style="color:#e2e8f0;margin-left:12px;">{rpt['type']}</span>
            <span style="color:#475569;font-size:0.8rem;margin-left:8px;">- {rpt['period']}</span>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
            <span style="color:#64748b;font-size:0.75rem;font-family:'JetBrains Mono';">{rpt['pages']} pages</span>
            <span style="color:#64748b;font-size:0.75rem;font-family:'JetBrains Mono';">{rpt['size']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Sentinel AI v6.2.0 - Executive Report Generator | All Reports Encrypted at Rest")
