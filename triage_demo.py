import streamlit as st
import time
import pandas as pd

# Page configuration for clean corporate layout
st.set_page_config(
    page_title="Tumaini 365 — Vivo Energy Portal",
    page_icon="🧠",
    layout="wide"
)

# ==========================================
# INITIALIZE SYSTEM MEMORY SPACE (SESSION STATE)
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.staff_records = []
    st.session_state.clinical_records = []
    st.session_state.token_registry = {}
    
    st.session_state.dept_scores = {"Corporate & HR": 0.0, "Retail Management": 0.0, "Depots & Logistics": 0.0, "Engineering": 0.0}
    st.session_state.dept_counts = {"Corporate & HR": 0, "Retail Management": 0, "Depots & Logistics": 0, "Engineering": 0}

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://icons8.com", width=80)
st.sidebar.title("Tumaini 365")
st.sidebar.write("Wellness Infrastructure")
st.sidebar.markdown("---")

user_role = st.sidebar.radio(
    "Choose your access role:",
    ["👤 Staff Triage Portal", "🩺 Clinician Diagnostic Desk", "📊 HR & HSSEQ Admin Dashboard"],
    index=0
)

st.sidebar.markdown("---")
if st.sidebar.button("🧹 Reset Workspace"):
    st.session_state.staff_records = []
    st.session_state.clinical_records = []
    st.session_state.token_registry = {}
    for d in st.session_state.dept_scores:
        st.session_state.dept_scores[d] = 0.0
        st.session_state.dept_counts[d] = 0
    st.sidebar.success("All dynamic entries cleared!")
    time.sleep(0.5)
    st.rerun()

# ==========================================
# ROLE 1: STAFF TRIAGE PORTAL
# ==========================================
if user_role == "👤 Staff Triage Portal":
    st.title("🧠 Frontend Risk Stratification Filter")
    st.caption("Customized Cognitive Triage for Vivo Energy Kenya")
    st.markdown("---")
    
    score_map = {"Never": 1, "Rarely": 2, "Frequently": 3, "Always": 4}
    
    with st.form("triage_form"):
        st.subheader("Personal Identification")
        staff_name = st.text_input("Full Name:", placeholder="e.g., John Kamau")
        staff_id = st.text_input("Vivo Staff Payroll Number:", placeholder="e.g., VEK-8840")
        target_dept = st.selectbox("Select Your Department:", ["Corporate & HR", "Retail Management", "Depots & Logistics", "Engineering"])
        
        st.markdown("---")
        st.subheader("Psychometric Assessment Questions")
        q1_choice = st.radio("**[Q1] After an operational shift, I feel emotionally drained:**", ["Never", "Rarely", "Frequently", "Always"])
        q2_choice = st.radio("**[Q2] I find it difficult to concentrate or maintain safety focus:**", ["Never", "Rarely", "Frequently", "Always"])
        q3_choice = st.radio("**[Q3] Anxiety regarding performance targets disrupts my sleep:**", ["Never", "Rarely", "Frequently", "Always"])
        
        submit_button = st.form_submit_button("Submit Diagnostic Pulse Check")
        
    if submit_button:
        if not staff_name or not staff_id:
            st.error("⚠️ Error: Name and Payroll fields must be completed to securely generate your clinical token identifier.")
        else:
            total_score = score_map[q1_choice] + score_map[q2_choice] + score_map[q3_choice]
            generated_token = f"VIVO-{1000 + len(st.session_state.staff_records)}"
            
            st.markdown("### 📊 Assessment Stratification")
            st.metric(label="Your Operational Risk Score", value=f"{total_score} / 12")
            
            if total_score  0:
                st.session_state.clinical_records.append({
                    "Reference Token": ref_id,
                    "MSE Flags": ", ".join(mse_status),
                    "Notes": clinical_notes,
                    "Timestamp": time.strftime("%H:%M:%S")
                })
                st.success(f"Case file for {ref_id} safely appended.")

# ==========================================
# ROLE 3: HR & HSSEQ ADMIN DASHBOARD
# ==========================================
elif user_role == "📊 HR & HSSEQ Admin Dashboard":
    st.title("📊 Macro-Level Organizational Health Dashboard")
    st.caption("Anonymized Analytics & Fatigue Audits (Strictly No PII Displayed)")
    st.markdown("---")
    
    total_screened = len(st.session_state.staff_records)
    if total_screened == 0:
        st.warning("⚠️ No data collected. Complete a screening in the Staff Portal first.")
    else:
        scores = [r["Triage Score"] for r in st.session_state.staff_records]
        green_count = sum(1 for s in scores if s <= 5)
        yellow_count = sum(1 for s in scores if 6 <= s <= 9)
        red_count = sum(1 for s in scores if s >= 10)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Screened", f"{total_screened} Staff")
        m2.metric("Green Tier", f"{int((green_count/total_screened)*100)}%")
        m3.metric("Yellow Tier", f"{int((yellow_count/total_screened)*100)}%")
        m4.metric("Red Tier", f"{int((red_count/total_screened)*100)}%")
        
        st.markdown("---")
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("#### 📉 Average Fatigue Index Concentration by Department")
            averages = {dept: (st.session_state.dept_scores[dept] / count if count > 0 else 0.0) for dept, count in st.session_state.dept_counts.items()}
            
            chart_vals = list(averages.values())
            chart_idx = list(averages.keys())
            st.bar_chart(pd.DataFrame(chart_vals, index=chart_idx, columns=["Fatigue/Burnout Index Score"]))
        with col_chart2:
            st.markdown("#### 🛡️ Infrastructure Intervention Metrics")
            st.write(f"* **14-Day Micro-Learning Cues Delivered:** {yellow_count * 14} Pushes")
            st.write(f"* **Active Clinical Cases Pending Intake:** {red_count} Red Alerts")
            if len(st.session_state.clinical_records) > 0:
                st.dataframe(pd.DataFrame(st.session_state.clinical_records), use_container_width=True)
