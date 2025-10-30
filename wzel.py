# zelkova_simulation.py (with z3-solver)
from z3 import *

def zelkova_s3_ip_analysis():
    # Model IAM policy as SMT
    # Variables: principal_ip, action = GetObject, resource = S3 bucket
    principal_ip = String('principal_ip')
    trusted_range = String('trusted_range')  # "192.168.0.0/16"
    s = Solver()

    # Policy: Allow if IP in range (condition)
    s.add(And(
        principal_ip == "203.0.113.5",  # External IP
        principal_ip != trusted_range   # Condition false
    ))

    # Check for unintended access: Is GetObject possible for external?
    access_possible = Bool('access_possible')
    s.add(Implies(principal_ip != trusted_range, Not(access_possible)))  # Deny if not trusted

    # Query: External access sat?
    result = s.check()
    if result == sat:
        print("Zelkova: sat - External access possible (policy flaw)")
    else:
        print("Zelkova: unsat - External access blocked (policy safe)")
        m = s.model()
        print(f"Model: {m}")  # E.g., access_possible = False

zelkova_s3_ip_analysis()