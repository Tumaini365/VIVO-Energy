import streamlit as st
import time
import pandas as pd

# Page configuration for clean corporate layout
st.set_page_config(
    page_title="Tumaini 365 — Vivo Energy Portal",
    page_icon="🧠",
    layout="wide"
)

# Global string variables declared completely outside form blocks to prevent structural truncation
act_green = "Deploy Proactive Digital Self-Care Toolkit (Green Tier)"
act_yellow = "Trigger 14-Day Micro-Learning Push Loops & Notify Peer Champion (Yellow Tier)"
act_red_standdown = "Issue Immediate Short-Term Safety Stand-down & De-escalation Session (Red Tier)"
act_red_referral = "Execute Expedited Priority Referral to Vivo Curative EAP Partner (Red Tier)"
action_options_pool = [act_green, act_yellow, act_red_standdown, act_red_referral]

# Helper functions to isolate variable processing from text parsers
def check_empty_records(records_list):
    if len(records_list) == 0:
        return True
    return False

def get_green_count(records_list):
    count = 0
    for r in records_list:
        if r["Normalized Stress Index"] <= 0.35:
            count += 1
    return count

def get_yellow_count(records_list):
    count = 0
    for r in records_list:
        val = r["Normalized Stress Index"]
        if val > 0.35 and val <= 0.65:
            count += 1
    return count

def get_red_count(records_list):
    count = 0
    for r in records_list:
        if r["Normalized Stress Index"] > 0.65:
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
    
    score_map = {
        "Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3,
        "Never": 1, "Rarely": 2, "Frequently": 3, "Always": 4
    }
    
    st.subheader("⚙️ Assessment Infrastructure Configuration")
    test_mode = st.selectbox(
        "Select Psychometric Protocol Layer:",
        ["Standard 3-Question Rapid Safety Triage", "Comprehensive GAD-7 Psychometric Screening Protocol"]
    )
    st.markdown("---")
    
    with st.form("triage_form"):
        st.subheader("Personal Identification")
        staff_name = st.text_input("Full Name:", placeholder="e.g., John Kamau")
        staff_id = st.text_input("Vivo Staff Payroll Number:", placeholder="e.g., VEK-8840")
        target_dept = st.selectbox("Select Your Department:", ["Corporate & HR", "Retail Management", "Depots & Logistics", "Engineering"])
        
        st.markdown("---")
        
        if test_mode == "Standard 3-Question Rapid Safety Triage":
            st.subheader("Rapid Safety Pulse Check")
            q1 = st.radio("**[Q1] After an operational shift, I feel emotionally drained:**", ["Never", "Rarely", "Frequently", "Always"])
            q2 = st.radio("**[Q2] I find it difficult to concentrate or maintain safety focus:**", ["Never", "Rarely", "Frequently", "Always"])
            q3 = st.radio("**[Q3] Anxiety regarding performance targets disrupts my sleep:**", ["Never", "Rarely", "Frequently", "Always"])
            submit_button = st.form_submit_button("Submit Rapid Safety Triage")
            
        else:
            st.subheader("Official GAD-7 Anxiety Diagnostic Module")
            st.markdown("*Over the last 2 weeks, how often have you been bothered by any of the following problems?*")
            g1 = st.radio("1. Feeling nervous, anxious, or on edge:", ["Not at all", "Several days", "More than half the days", "Nearly every day"])
            g2 = st.radio("2. Not being able to stop or control worrying:", ["Not at all", "Several days", "More than half the days", "Nearly every day"])
            g3 = st.radio("3. Worrying too much about different things:", ["Not at all", "Several days", "More than half the days", "Nearly every day"])
            g4 = st.radio("4. Trouble relaxing:", ["Not at all", "Several days", "More than half the days", "Nearly every day"])
            g5 = st.radio("5. Being so restless that it is hard to sit still:", ["Not at all", "Several days", "More than half the days", "Nearly every day"])
            g6 = st.radio("6. Becoming easily annoyed or irritable:", ["Not at all", "Several days", "More than half the days", "Nearly every day"])
            g7 = st.radio("7. Feeling afraid, as if something awful might happen:", ["Not at all", "Several days", "More than half the days", "Nearly every day"])
            submit_button = st.form_submit_button("Submit Complete GAD-7 Psychometric Evaluation")
        
    if submit_button:
        if not staff_name or not staff_id:
            st.error("⚠️ Error: Name and Payroll fields must be completed to securely generate your clinical token identifier.")
        else:
            if test_mode == "Standard 3-Question Rapid Safety Triage":
                raw_score = score_map[q1] + score_map[q2] + score_map[q3]
                max_possible = 12
            else:
                raw_score = score_map[g1] + score_map[g2] + score_map[g3] + score_map[g4] + score_map[g5] + score_map[g6] + score_map[g7]
                max_possible = 21
            
            norm_index = float(raw_score / max_possible)
            generated_token = f"VIVO-{1000 + len(st.session_state.staff_records)}"
            
            st.markdown("### 📊 Assessment Stratification")
            st.metric(label=f"Your Raw Score ({test_mode})", value=f"{raw_score} / {max_possible}")
            
            if norm_index <= 0.35:
                strat_label = "GREEN"
                st.success(f"### STATUS LEVEL: [ GREEN ] — Safe Parameters. Token: {generated_token}")
            elif norm_index <= 0.65:
                strat_label = "YELLOW"
                st.warning(f"### STATUS LEVEL: [ YELLOW ] — WATCHLIST / EARLY INTERVENTION. Token: {generated_token}")
            else:
                strat_label = "RED"
                st.error(f"### STATUS LEVEL: [ RED ] — CRITICAL RISK / CLINICAL INTAKE REQUIRED. Token: {generated_token}")
                
            st.session_state.staff_records.append({
                "Reference Token": generated_token,
                "Protocol": "Rapid Triage" if max_possible == 12 else "Full GAD-7",
                "Department": target_dept,
                "Raw Score": raw_score,
                "Normalized Stress Index": round(norm_index, 2),
                "Trigger Date": time.strftime("%Y-%m-%d"),
                "Status": "Action Required" if strat_label != "GREEN" else "Compliant"
            })
            
            st.session_state.token_registry[generated_token] = {
                "Real Name": staff_name,
                "Payroll ID": staff_id,
                "Department": target_dept,
                "Score": f"{raw_score} / {max_possible} (Index: {round(norm_index, 2)})"
            }
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
        if check_empty_records(st.session_state.staff_records):
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
                st.write(f"📊 **Initial Triage Mapped Metrics:** {identity_data['Score']}")
            else:
                st.error("Token not found or invalid lookup permissions.")
        
    with col2:
        st.markdown("### 🛠️ Record On-Site Case Assessment & Action")
        with st.form("clinical_notes_form"):
            # 🚀 ARCHITECTURE CHANGE: UNLOCKED DROPDOWN GATEWAY
            # If HR list is empty, switches instantly to a manual free-text fallback token entry option
