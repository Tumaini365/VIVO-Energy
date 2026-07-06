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
            
            if total_score <= 5:
                strat_label = "GREEN"
                st.success(f"### STATUS LEVEL: [ GREEN ] — Safe Parameters. Token: {generated_token}")
            elif total_score <= 9:
                strat_label = "YELLOW"
                st.warning(f"### STATUS LEVEL: [ YELLOW ] — BURNOUT WATCHLIST. Token: {generated_token}")
            else:
                strat_label = "RED"
                st.error(f"### STATUS LEVEL: [ RED ] — CRITICAL COGNITIVE RISK. Token: {generated_token}")
                
            st.session_state.staff_records.append({
                "Reference Token": generated_token,
                "Department": target_dept,
                "Triage Score": total_score,
                "Trigger Date": time.strftime("%Y-%m-%d"),
                "Status": "Action Required" if strat_label != "GREEN" else "Compliant"
            })
            
            st.session_state.token_registry[generated_token] = {
                "Real Name": staff_name,
                "Payroll ID": staff_id,
                "Department": target_dept,
                "Score": total_score
            }
            
            st.session_state.dept_scores[target_dept] += float(total_score)
            st.session_state.dept_counts[target_dept] += 1
            st.info(f"🔒 Mapped under confidential reference token: **{generated_token}**.")

# ==========================================
# ROLE 2: CLINICIAN DIAGNOSTIC DESK
# ==========================================
elif user_role == "🩺 Clinician Diagnostic Desk":
    st.title("🩺 Clinician Diagnostic Desk")
    st.caption("Secure Intake Portal — Lead Consultant: Ezekiel Kiago Wangunyu")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Anonymized Intake Action Feed")
        is_empty = check_empty_records(st.session_state.staff_records)
        
        if is_empty:
            st.info("No active staff assessments recorded yet.")
        else:
            st.dataframe(pd.DataFrame(st.session_state.staff_records), use_container_width=True)
            
        st.markdown("---")
        st.markdown("### 🔐 Secure Identity Matrix Lookup")
        lookup_token = st.text_input("Enter Patient Reference Token to verify identity (e.g., VIVO-1000):")
        if lookup_token:
            if lookup_token in st.session_state.token_registry:
                identity_data = st.session_state.token_registry[lookup_token]
                st.success(f"**Identity Verified Successfully:**")
                st.write(f"👤 **Staff Name:** {identity_data['Real Name']}")
                st.write(f"🆔 **Payroll Number:** {identity_data['Payroll ID']}")
                st.write(f"🏢 **Operating Unit:** {identity_data['Department']}")
                st.write(f"📊 **Initial Triage Score:** {identity_data['Score']} / 12")
            else:
                st.error("Token not found or invalid lookup permissions.")
        
    with col2:
        st.markdown("### Record On-Site Case Assessment")
        with st.form("clinical_notes_form"):
            is_empty_selection = check_empty_records(st.session_state.staff_records)
            patient_options = ["No active profiles"] if is_empty_selection else [r["Reference Token"] for r in st.session_state.staff_records]
            ref_id = st.selectbox("Select Patient Reference Token", patient_options)
            mse_status = st.multiselect("MSE Indicators Observed:", ["Cognitive Slowing", "Affective Flattening", "Hyper-vigilance", "Extreme Exhaustion"])
            clinical_notes = st.text_area("Treatment/EAP Recommendations")
            save_clinical = st.form_submit_button("Commit to Secure Clinical Record")
            
            if save_clinical and not is_empty_selection:
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
    is_hr_empty = check_empty_records(st.session_state.staff_records)
    
    if is_hr_empty:
        st.warning("⚠️ No data collected. Complete a screening in the Staff Portal first.")
    else:
        scores = [r["Triage Score"] for r in st.session_state.staff_records]
        
        green_count = get_green_count(scores)
        yellow_count = get_yellow_count(scores)
        red_count = get_red_count(scores)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Screened", f"{total_screened} Staff")
        m2.metric("Green Tier", f"{int((green_count/total_screened)*100)}%")
        m3.metric("Yellow Tier", f"{int((yellow_count/total_screened)*100)}%")
        m4.metric("Red Tier", f"{int((red_count/total_screened)*100)}%")
        
        st.markdown("---")
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("#### 📉 Average Fatigue Index Concentration by Department")
            
            # Replaced the complex dictionary comprehension with standard explicit loops
            chart_vals = []
            chart_idx = ["Corporate & HR", "Retail Management", "Depots & Logistics", "Engineering"]
            
            for dept in chart_idx:
