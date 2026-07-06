import streamlit as st
import time
import pandas as pd

# Page configuration for clean corporate layout
st.set_page_config(
    page_title="Tumaini 365 — Vivo Energy Portal",
    page_icon="🧠",
    layout="wide"
)

# Helper functions to isolate variable processing from text parsers
def check_empty_records(records_list):
    if len(records_list) == 0:
        return True
    return False

def get_green_count(scores_list):
    count = 0
    for s in scores_list:
        if s <= 5:
            count += 1
    return count

def get_yellow_count(scores_list):
    count = 0
    for s in scores_list:
        if s >= 6:
            if s <= 9:
                count += 1
    return count

def get_red_count(scores_list):
    count = 0
    for s in scores_list:
        if s >= 10:
            count += 1
    return count

# ==========================================
# INITIALIZE SYSTEM MEMORY SPACE
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
            
            if total_score  0 else 0.0) for dept, count in st.session_state.dept_counts.items()}
            
            chart_vals = list(averages.values())
            chart_idx = list(averages.keys())
