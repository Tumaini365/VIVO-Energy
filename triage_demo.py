import streamlit as st
import time

# Page Configuration for Corporate Styling
st.set_page_config(
    page_title="Tumaini 365 — Digital Triage Demo",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Frontend Risk Stratification Filter")
st.caption("Customized Cognitive Triage for Vivo Energy Kenya (HSSEQ & HR Divisions)")
st.markdown("---")

st.markdown("""
### Welcome to the Operational Pulse Check
Please complete this brief 3-question assessment. This data acts as an early-warning filter 
to track fatigue and sub-clinical burnout before they escalate into safety risks or medical claims.
""")

# Scoring mapping dictionary
score_map = {
    "Never": 1,
    "Rarely": 2,
    "Frequently": 3,
    "Always": 4
}

# Interactive Questionnaire Form
with st.form("triage_form"):
    q1_choice = st.radio(
        "**[Q1] After an operational shift or a long workday, I feel emotionally drained and completely spent:**",
        ["Never", "Rarely", "Frequently", "Always"],
        index=0
    )
    
    q2_choice = st.radio(
        "**[Q2] I find it difficult to concentrate, maintain strict safety focus, or keep track of complex tasks:**",
        ["Never", "Rarely", "Frequently", "Always"],
        index=0
    )
    
    q3_choice = st.radio(
        "**[Q3] Anxiety regarding performance targets, strict logistics quotas, or macroeconomic stressors disrupts my sleep:**",
        ["Never", "Rarely", "Frequently", "Always"],
        index=0
    )
    
    submit_button = st.form_submit_button("Submit Diagnostic Pulse Check")

# Processing Logic upon Form Submission
if submit_button:
    # Compute total psychometric score
    total_score = score_map[q1_choice] + score_map[q2_choice] + score_map[q3_choice]
    
    with st.spinner("Processing psychometric vectors against safety baselines..."):
        time.sleep(1.2)
        
    st.markdown("### 📊 Assessment Stratification")
    st.metric(label="Total Operational Risk Score", value=f"{total_score} / 12")
    
    # Risk Matrix Evaluation
    if total_score <= 5:
        st.success("### STATUS LEVEL: [ GREEN ] — LOW COGNITIVE RISK")
        st.markdown("""
        **Recommended Pathway:**
        * **Optimal Performance:** Employee is operating well within safe psychological and fatigue thresholds.
        * **Action Triggered:** Automated delivery of standard digital self-care toolkits and micro-learning mental fitness modules to maintain resilience.
        """)
        
    elif 6 <= total_score <= 9:
        st.warning("### STATUS LEVEL: [ YELLOW ] — FUNCTIONAL BURNOUT RISK")
        st.markdown("""
        **Recommended Pathway (Tumaini Early Intervention):**
        * **Early-Warning Indicator:** Sub-clinical fatigue detected. Increased risk of operational errors, presenteeism, or safety slip-ups.
        * **Action Triggered:** Initiating the **14-Day Micro-Learning Push** via automated, bite-sized WhatsApp/email cues.
        * **Next Steps:** Prioritizing the employee for a voluntary slot in the upcoming **Monthly Wellness Booster Pod**.
        """)
        
    else:
        st.error("### STATUS LEVEL: [ RED ] — ACUTE CRISIS / HIGH SAFETY RISK")
        st.markdown("""
        **Recommended Pathway (Immediate Operational De-escalation):**
        * **Critical Threshold:** Severe exhaustion affecting cognitive tracking and safety compliance. Immediate risk to transport safety or personal health.
        * **Action Triggered:** Instant, automated priority hot-link routing to certified internal **Peer Wellness Champions**.
        * **Next Steps:** Expedited referral mechanism directly to Vivo Energy's Curative EAP partner or medical concierge.
        """)
        
    st.info("**Data Safety Note:** This screening is aggregated anonymously at the departmental level to protect employee confidentiality while ensuring macro-level HSSEQ risk reporting.")
