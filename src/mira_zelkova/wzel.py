# zelkova_s3_ip_analysis_corrected.py
from z3 import *

def zelkova_s3_ip_analysis():
    # ----------------------------
    # 1. Variables and setup
    # ----------------------------
    principal_ip = String('principal_ip')
    trusted_range = String('trusted_range')
    access_possible = Bool('access_possible')
    s = Solver()

    # ----------------------------
    # 2. Model an IAM-like policy
    # ----------------------------
    # Policy rule (the intended behavior):
    # "Access is allowed only if IP is within trusted range."
    # In other words: if IP is NOT trusted -> access = False
    s.add(Implies(principal_ip != trusted_range, Not(access_possible)))

    # ----------------------------
    # 3. Security query (Zelkova style)
    # ----------------------------
    # We now *ask* the opposite question:
    # "Is there ANY model where an untrusted IP CAN access?"
    s.push()  # Save solver state
    s.add(principal_ip != trusted_range)  # IP outside trusted network
    s.add(access_possible)                # but still allowed access?
    
    # ----------------------------
    # 4. Check if such a bad situation is possible
    # ----------------------------
    result = s.check()

    if result == sat:
        print("Zelkova: sat → Policy flaw detected ❌")
        print(f"Example model: {s.model()}")
    else:
        print("Zelkova: unsat → Policy safe ✅ (no external access possible)")

zelkova_s3_ip_analysis()
