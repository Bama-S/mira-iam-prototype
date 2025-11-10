# mira_zelkova_s3_analysis_report.py
from z3 import *
import ipaddress
from prettytable import PrettyTable  # for neat tabular output (pip install prettytable)

def ip_in_cidr(ip_str, cidr_str):
    """Return True if IP belongs to CIDR range."""
    ip = ipaddress.ip_address(ip_str)
    network = ipaddress.ip_network(cidr_str, strict=False)
    return ip in network


def mira_zelkova_s3_ip_analysis():
    # ------------------------------------------
    # 1. Setup symbolic variables for reasoning
    # ------------------------------------------
    principal_ip = String('principal_ip')
    access_possible = Bool('access_possible')
    goal_intended = Bool('goal_intended')
    action_executed = Bool('action_executed')
    mira_state = String('mira_state')

    s = Solver()
    trusted_range = "192.168.0.0/16"

    # ------------------------------------------
    # 2. Model IAM-like policy
    # ------------------------------------------
    def policy_allows(ip_value):
        """Return True if policy allows access for IP."""
        return ip_in_cidr(ip_value, trusted_range)

    # ------------------------------------------
    # 3. Test different IP cases
    # ------------------------------------------
    test_cases = [
        ("192.168.1.10", True),    # trusted + goal
        ("203.0.113.5", True),     # untrusted + goal
        ("192.168.255.200", False) # trusted + no goal
    ]

    # Create output table
    table = PrettyTable()
    table.field_names = [
        "IP Address",
        "Zelkova (SAT/UNSAT)",
        "Goal Intended",
        "Access Possible",
        "MIRA State",
        "Meaning"
    ]

    # ------------------------------------------
    # 4. Evaluate each case
    # ------------------------------------------
    for ip_value, has_goal in test_cases:
        s.push()  # save solver state

        s.add(principal_ip == ip_value)
        s.add(goal_intended == has_goal)

        # Policy logic
        in_trusted = policy_allows(ip_value)
        if in_trusted:
            s.add(Implies(principal_ip == ip_value, access_possible))
        else:
            s.add(Implies(principal_ip == ip_value, Not(access_possible)))

        s.add(action_executed == access_possible)

        # MIRA logic
        S = And(goal_intended, action_executed)
        V = And(goal_intended, Not(action_executed))
        N = Not(goal_intended)

        s.add(If(S, mira_state == StringVal("S"),
              If(V, mira_state == StringVal("V"),
                 If(N, mira_state == StringVal("N"),
                    mira_state == StringVal("U")))))

        # Query Zelkova: any policy flaw?
        s.push()
        s.add(Not(in_trusted))        # untrusted access
        s.add(access_possible == True)  # but still allowed?
        zelkova_result = s.check()
        s.pop()

        # Solve MIRA semantics
        mira_result = s.check()
        if mira_result == sat:
            model = s.model()
            g = model[goal_intended]
            a = model[access_possible]
            m = model[mira_state]
        else:
            g, a, m = "-", "-", "-"

        # Interpret Zelkova result
        if zelkova_result == sat:
            zelkova_str = "SAT (flaw ❌)"
        else:
            zelkova_str = "UNSAT (safe ✅)"

        # Interpret MIRA state
        meaning_map = {
            "S": "Satisfied (goal achieved)",
            "V": "Violated (goal blocked)",
            "N": "Neutral (no intention)",
            "U": "Undefined"
        }
        meaning = meaning_map.get(str(m), "-")

        # Add to table
        table.add_row([ip_value, zelkova_str, g, a, m, meaning])

        s.pop()  # restore state

    # ------------------------------------------
    # 5. Print Final Hybrid Report
    # ------------------------------------------
    print("\n========== HYBRID ZELKOVA–MIRA POLICY EVALUATION ==========")
    print(table)
    print("============================================================")

if __name__ == "__main__":
    mira_zelkova_s3_ip_analysis()

