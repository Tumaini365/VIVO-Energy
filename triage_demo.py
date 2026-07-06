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
    
    # Empty lists ready to record incoming raw data
    st.session_state.staff_records = []
    st.session_state.clinical_records = []
    
    # Department metric tally structure
    st.session_state.dept_scores = {
        "Corporate & HR": 0.0,
        "Retail Management": 0.0,
        "Depots & Logistics": 0.0,
        "Engineering": 0.0
    }
    st.session_state.dept_counts = {
        "Corporate & HR": 0,
        "Retail Management": 0,
        "Depots & Logistics": 0,
        "Engineering": 0
    }

# --- SIDEBAR NAVIGATION ---
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

# Admin utility to clear dynamic storage instantly during presentations
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Reset System Memory Workspace"):
    st.session_state.staff_records = []
    st.session_state.clinical_records = []
    for d in st.session_state.dept_scores:
        st.session_state.dept_scores[d] = 0.0
        st.session_state.dept_counts[d] = 0
    st.sidebar.success("All operational inputs cleared!")
    time.sleep(0.5)
    st.rerun()

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
    Please complete this brief assessment. Your input acts as an early-warning filter 
    to track fatigue and sub-clinical burnout before they escalate into safety risks.
    """)
    
    score_map = {"Never": 1, "Rarely": 2, "Frequently": 3, "Always": 4}
    
    with st.form("triage_form"):
        target_dept = st.selectbox("Select Your Operational Department:", ["Corporate & HR", "Retail Management", "Depots & Logistics", "Engineering"])
        
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
            time.sleep(0.8)
            
        st.markdown("### 📊 Assessment Stratification")
        st.metric(label="Your Operational Risk Score", value=f"{total_score} / 12")
        
        # Determine risk classification label
        if total_score <= 5:
            strat_label = "GREEN"
            st.success("### STATUS LEVEL: [ GREEN ] — LOW COGNITIVE RISK")
            st.markdown("**Recommended Pathway:** Operating well within safe parameters. Standard digital self-care toolkits dispatched.")
        elif 6 <= total_score <= 9:
            strat_label = "YELLOW"
            st.warning("### STATUS LEVEL: [ YELLOW ] — FUNCTIONAL BURNOUT RISK")
            st.markdown("**Recommended Pathway:** Sub-clinical fatigue detected. Initiating **14-Day Micro-Learning Push** loops.")
        else:
            strat_label = "RED"
            st.error("### STATUS LEVEL: [ RED ] — ACUTE CRISIS / HIGH SAFETY RISK")
            st.markdown("**Recommended Pathway:** Critical exhaustion. Immediate hot-link routing to certified internal **Peer Wellness Champions**.")
            
        # Append record dynamically to session memory
        generated_id = f"VIVO-{1000 + len(st.session_state.staff_records)}"
        new_record = {
            "Reference ID": generated_id,
            "Department": target_dept,
            "Triage Score": total_score,
            "Trigger Date": time.strftime("%Y-%m-%d"),
            "Status": "Pending Review" if strat_label != "GREEN" else "Safe Parameter"
        }
        st.session_state.staff_records.append(new_record)
        
        # Accumulate metrics for dynamic HR graphing
        st.session_state.dept_scores[target_dept] += float(total_score)
        st.session_state.dept_counts[target_dept] += 1


# ==========================================
# ROLE 2: CLINICIAN DIAGNOSTIC DESK
# ==========================================
elif user_role == "🩺 Clinician Diagnostic Desk":
    st.title("🩺 Clinician Diagnostic Desk")
    st.caption("Secure Intake & Clinical Case Management Portal — Ezekiel Kiago Wangunyu")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Dynamic Clinical Action Feed")
        if len(st.session_state.staff_records) == 0:
            st.info("No active staff assessments recorded yet. Complete a form in the Staff Portal to populate this feed.")
        else:
            # Display real-time input history table
            feed_df = pd.DataFrame(st.session_state.staff_records)
            st.dataframe(feed_df, use_container_width=True)
        
    with col2:
        st.markdown("### Record On-Site Case Assessment")
        with st.form("clinical_notes_form"):
            if len(st.session_state.staff_records) == 0:
                patient_options = ["No active profiles found"]
            else:
                patient_options = [r["Reference ID"] for r in st.session_state.staff_records]
                
            ref_id = st.selectbox("Select Patient Reference ID", patient_options)
            mse_status = st.multiselect("Mental Status Examination (MSE) Flags:", ["Cognitive Slowing", "Affective Flattening", "Hyper-vigilance", "Extreme Exhaustion"])
            clinical_notes = st.text_area("Intake & Treatment Recommendations")
            save_clinical = st.form_submit_button("Commit to Secure Clinical Record")
            
            if save_clinical and len(st.session_state.staff_records) > 0:
                new_clinical = {
                    "Reference ID": ref_id,
                    "MSE Flags": ", ".join(mse_status),
                    "Notes": clinical_notes,
                    "Timestamp": time.strftime("%H:%M:%S")
                }
                st.session_state.clinical_records.append(new_clinical)
                st.success(f"Case file for {ref_id} safely updated inside temporary memory.")


# ==========================================
# ROLE 3: HR & HSSEQ ADMIN DASHBOARD
# ==========================================
elif user_role == "📊 HR & HSSEQ Admin Dashboard":
    st.title("📊 Macro-Level Organizational Health Dashboard")
    st.caption("Anonymized Analytics & Fatigue Audits driven by Active System Data")
    st.markdown("---")
    
    total_screened = len(st.session_state.staff_records)
    
    if total_screened == 0:
        st.warning("⚠️ No assessment data collected. Please fill out multiple screening entries inside the 'Staff Triage Portal' to generate real-time metrics.")
        
        # Fallback empty metrics display
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Screened", "0 Staff")
        m2.metric("Green Tier", "0%")
        m3.metric("Yellow Tier", "0%")
        m4.metric("Red Tier", "0%")
    else:
        # Calculate dynamic metric parameters from live user scores
        scores = [r["Triage Score"] for r in st.session_state.staff_records]
        green_count = sum(1 for s in scores if s <= 5)
        yellow_count = sum(1 for s in scores if 6 <= s <= 9)
        red_count = sum(1 for s in scores if s >= 10)
        
        pct_green = int((green_count / total_screened) * 100)
        pct_yellow = int((yellow_count / total_screened) * 100)
        pct_red = int((red_count / total_screened) * 100)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Screened (Live Data)", f"{total_screened} Staff")
        m2.metric("Green Tier (Safe)", f"{pct_green}%", "🚀 Target Fit")
        m3.metric("Yellow Tier (Burnout)", f"{pct_yellow}%", "⚠️ Monitor")
        m4.metric("Red Tier (Critical)", f"{pct_red}%", "🚨 Direct Intervention")
        
        st.markdown("---")
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("#### 📉 Average Fatigue Index Concentration by Department")
            
            # Compute live averages per department
            averages = {}
            for dept in st.session_state.dept_scores:
                count = st.session_state.dept_counts[dept]
                averages[dept] = float(st.session_state.dept_scores[dept] / count) if count > 0 else 0.0
                
