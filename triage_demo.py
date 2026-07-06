import sys
import time

def run_triage_demo():
    print("=" * 65)
    print(" TUMAINI THREE SIXTY FIVE LIMITED — DIGITAL COGNITIVE TRIAGE DEMO")
    print(" Customized Frontend Risk Stratification Filter for Vivo Energy")
    print("=" * 65)
    print("\n[INFO] Initializing Secure Screening Interface (OLBI/GAD-7 Protocol)...")
    time.sleep(1)
    
    print("\nWelcome! Please complete this brief 3-question operational pulse check.")
    print("Rate each statement from 1 to 4:")
    print("  1 = Never | 2 = Rarely | 3 = Frequently | 4 = Always\n")
    
    try:
        # Question 1: Operational Exhaustion (OLBI metric)
        q1 = int(input("[Q1] After a shift/workday, I feel emotionally drained and spent: "))
        if q1 not in [1, 2, 3, 4]: raise ValueError
        
        # Question 2: Cognitive Fatigue (Fit2Drive risk metric)
        q2 = int(input("[Q2] I find it difficult to concentrate or maintain safety focus: "))
        if q2 not in [1, 2, 3, 4]: raise ValueError
        
        # Question 3: Macro-economic/Sales Pressure (Anxiety proxy)
        q3 = int(input("[Q3] Stress about quotas, targets, or economic factors keeps me up: "))
        if q3 not in [1, 2, 3, 4]: raise ValueError
        
    except ValueError:
        print("\n[ERROR] Invalid input. Please enter numbers between 1 and 4 only.")
        sys.exit()

    # Calculate aggregate screening metrics
    total_score = q1 + q2 + q3
    
    print("\n" + "-" * 50)
    print("[PROCESSING] Analyzing psychometric indicators...")
    time.sleep(1.5)
    print("[PROCESSING] Cross-referencing against HSSEQ safety baselines...")
    time.sleep(1.0)
    print("-" * 50 + "\n")
    
    print("=" * 55)
    print(f"TRIAGE RESULT: TOTAL OPERATIONAL RISK SCORE = {total_score} / 12")
    print("=" * 55)
    
    # Automated Risk Stratification Logic
    if total_score <= 5:
        print("STATUS LEVEL: [ GREEN ] — LOW COGNITIVE RISK")
        print("RECOMMENDED PATHWAY:")
        print(" -> Employee is operating well within optimal psychological thresholds.")
        print(" -> Action: Push standard digital self-care toolkits & wellness app tips.")
        
    elif 6 <= total_score <= 9:
        print("STATUS LEVEL: [ YELLOW ] — FUNCTIONAL BURNOUT RISK")
        print("RECOMMENDED PATHWAY (Tumaini Early Intervention):")
        print(" -> Warning: Sub-clinical fatigue detected. Risk of presenteeism or safety slip.")
        print(" -> Action: Trigger the 14-Day Micro-Learning Push via automated loops.")
        print(" -> Action: Flag for a voluntary Monthly 'Wellness Booster' Pod session.")
        
    else:
        print("STATUS LEVEL: [ RED ] — ACUTE CRISIS / HIGH SAFETY RISK")
        print("RECOMMENDED PATHWAY (Immediate De-escalation):")
        print(" -> Critical: Immediate risk to cognitive tracking, drive safety, or personal health.")
        print(" -> Action: Instant hot-link routing to certified Peer Wellness Champions.")
        print(" -> Action: Expedited priority referral to Vivo Energy's Curative EAP partner.")

    print("\n" + "=" * 65)
    print("Demo finalized. Tumaini 365 protects 'Goal Zero' before claims happen.")
    print("=" * 65)

if __name__ == "__main__":
    run_triage_demo()
