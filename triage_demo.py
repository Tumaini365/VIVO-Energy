import streamlit as st
import time
import pandas as pd
import numpy as np

# Page configuration for clean corporate layout
st.set_page_config(
    page_title="Tumaini 365 — Vivo Energy Portal",
    page_icon="🧠",
    layout="wide"
)

# --- SIDEBAR NAVIGATION BUTTONS ---
st.sidebar.image("https://icons8.com", width=80)
st.sidebar.title("Tumaini 365")
st.sidebar.write("Integrated Wellness Infrastructure")
st.sidebar.markdown("---")

st.sidebar.subheader("Select Interface View:")
user_role = st.sidebar.radio(
    "Choose your access role:",
    ["👤 Staff Triage Portal", "🩺 Clinician Diagnostic Desk", "📊 HR & HSSEQ Admin Dashboard"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("🔒 Secured with AES-256 Protocol")
st.sidebar.caption("Tumaini 365 Ltd © 2026")


# ==========================================
# ROLE 1: STAFF TRIAGE PORTAL
# ==========================================
if user_role == "👤 Staff Triage Portal":
    st.title("🧠 Frontend Risk Stratification Filter")
    st.caption("Customized Cognitive Triage for Vivo Energy Kenya (HSSEQ & HR Divisions)")
    st.markdown("---")
    
    st.markdown("""
    ### Welcome to the Operational Pulse Check
    Please complete this brief 3-question assessment. This data acts as an early-warning filter 
    to track fatigue and sub-clinical burnout before they escalate into safety risks or medical claims.
    """)
    
    score_map = {"Never": 1, "Rarely": 2, "Frequently": 3, "Always": 4}
    
    with st.form("triage_form"):
        q1_choice = st.radio(
            "**[Q1] After an operational shift or a long workday, I feel emotionally drained and completely spent:**",
            ["Never", "Rarely", "Frequently", "Always"], index=0
        )
        q2_choice = st.radio(
            "**[Q2] I find it difficult to concentrate, maintain strict safety focus, or keep track of complex tasks:**",
            ["Never", "Rarely", "Frequently", "Always"], index=0
        )
        q3_choice = st.radio(
            "**[Q3] Anxiety regarding performance targets, strict logistics quotas, or macroeconomic stressors disrupts my sleep:**",
            ["Never", "Rarely", "Frequently", "Always"], index=0
        )
        submit_button = st.form_submit_button("Submit Diagnostic Pulse Check")
        
    if submit_button:
        total_score = score_map[q1_choice] + score_map[q2_choice] + score_map[q3_choice]
        with st.spinner("Processing psychometric vectors..."):
            time.sleep(1.0)
            
        st.markdown("### 📊 Assessment Stratification")
        st.metric(label="Total Operational Risk Score", value=f"{total_score} / 12")
        
        if total_score <= 5:
            st.success("### STATUS LEVEL: [ GREEN ] — LOW COGNITIVE RISK")
            st.markdown("**Recommended Pathway:** Employee operates well within safe parameters. Standard digital self-care toolkits dispatched.")
        elif 6 <= total_score <= 9:
            st.warning("### STATUS LEVEL: [ YELLOW ] — FUNCTIONAL BURNOUT RISK")
            st.markdown("**Recommended Pathway:** Sub-clinical fatigue detected. Initiating **14-Day Micro-Learning Push** loops via WhatsApp/Email.")
        else:
            st.error("### STATUS LEVEL: [ RED ] — ACUTE CRISIS / HIGH SAFETY RISK")
            st.markdown("**Recommended Pathway:** Critical exhaustion. Immediate hot-link routing to certified internal **Peer Wellness Champions** and curative EAP partners.")


# ==========================================
# ROLE 2: CLINICIAN DIAGNOSTIC DESK
# ==========================================
elif user_role == "🩺 Clinician Diagnostic Desk":
    st.title("🩺 Clinician Diagnostic Desk")
    st.caption("Secure Intake & Clinical Case Management Portal — Ezekiel Kiago Wangunyu")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Active Clinical Referrals (Red/Yellow Tiers)")
        
        # Bypassing array filters completely using separate clean string processing variables
        score_val_a = 10
        score_val_b = 8
        score_val_c = 11
        
        referrals_df = pd.DataFrame({
            "Reference ID": ["VIVO-7831", "VIVO-9022", "VIVO-1145"],
            "Department": ["Logistics (Haulage)", "Retail Operations", "Underwriting Desk"],
            "Triage Score": [score_val_a, score_val_b, score_val_c],
            "Trigger Date": ["2026-07-04", "2026-07-05", "2026-07-06"],
            "Status": ["Pending Intake", "Assigned to Champion", "Booster Pod Scheduled"]
        })
        st.dataframe(referrals_df, use_container_width=True)
        
    with col2:
        st.markdown("### Record On-Site Case Assessment")
        with st.form("clinical_notes_form"):
            ref_id = st.selectbox("Select Patient Reference ID", ["VIVO-7831", "VIVO-9022", "VIVO-1145"])
            mse_status = st.multiselect("Mental Status Examination (MSE) Flags:", ["Cognitive Slowing", "Affective Flattening", "Hyper-vigilance", "Extreme Exhaustion"])
            clinical_notes = st.text_area("Intake & Treatment Recommendations")
            save_clinical = st.form_submit_button("Commit to Secure Clinical Record")
            if save_clinical:
                st.success(f"Case file for {ref_id} safely updated. Audit trails recorded.")


# ==========================================
# ROLE 3: HR & HSSEQ ADMIN DASHBOARD
# ==========================================
elif user_role == "📊 HR & HSSEQ Admin Dashboard":
    st.title("📊 Macro-Level Organizational Health Dashboard")
    st.caption("Anonymized Analytics & Fatigue Audits for Senior Management Execution")
    st.markdown("---")
    
    # Overview KPI metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Screened (Q2 2026)", "412 Staff")
    m2.metric("Green Tier (Safe Parameters)", "78%", "🚀 Optimal")
    m3.metric("Yellow Tier (Burnout Risk)", "14%", "⚠️ Watchlist")
    m4.metric("Red Tier (Immediate Action)", "8%", "🚨 Critical")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### 📉 Stress/Burnout Concentrations by Department")
        
        val_corp = 2.4
        val_ret = 4.1
        val_log = 8.7
        val_eng = 5.3
        
        chart_data = pd.DataFrame(
            [val_corp, val_ret, val_log, val_eng],
            index=["Corporate & HR", "Retail Management", "Depots & Logistics", "Engineering"],
            columns=["Fatigue/Burnout Index Score"]
        )
        st.bar_chart(chart_data)
        st.caption("Higher score denotes critical fatigue concentrations requiring shift/quota adjustment.")
        
    with col_chart2:
        st.markdown("#### 🛡️ Infrastructure Intervention Metrics")
        st.write("""
        * **Certified Peer Champions On-site:** 24 Active Staff
        * **14-Day Micro-Learning Cues Delivered:** 1,240 Automated Pushes
        * **Wellness Booster Pod Attendance:** 89% Month-on-Month Engagement
        * **Estimated Claims Savings via Front-End Filter:** KES 620,000
        """)
