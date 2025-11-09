# zelkova_s3_ip_analysis_cidr.py
# This is a sample code that checks whether the policy is correct
from z3 import *
import ipaddress

def ip_in_cidr(ip_str, cidr_str):
    """Return True if IP belongs to CIDR range."""
    ip = ipaddress.ip_address(ip_str)
    network = ipaddress.ip_network(cidr_str, strict=False)
    return ip in network

def zelkova_s3_ip_analysis():
    # ------------------------------------------
    # 1. Setup symbolic variables for reasoning
    # ------------------------------------------
    principal_ip = String('principal_ip')
    access_possible = Bool('access_possible')
    s = Solver()

    # Trusted network (CIDR range)
    trusted_range = "192.168.0.0/16"

    # ------------------------------------------
    # 2. Model IAM-like policy as logic
    # ------------------------------------------
    # The real policy: "Allow only if IP ∈ trusted_range"
    # We'll represent that with a helper predicate
    def policy_allows(ip_value):
        if ip_in_cidr(ip_value, trusted_range):
            return True
        else:
            return False

    # ------------------------------------------
    # 3. Ask Zelkova-style query
    # ------------------------------------------
    # We’ll iterate over a few possible IPs (for illustration)
    test_ips = [
        "192.168.1.10",   # internal trusted
        "203.0.113.5",    # external untrusted
        "192.168.255.200" # edge case within /16
    ]

    for ip_value in test_ips:
        s.push()  # save solver state

        # Case: principal_ip = specific IP
        s.add(principal_ip == ip_value)

        # Policy logic: if IP not in trusted → deny
        in_trusted = policy_allows(ip_value)
        if not in_trusted:
            s.add(Implies(principal_ip == ip_value, Not(access_possible)))
        else:
            s.add(Implies(principal_ip == ip_value, access_possible))

        # Now ask if a violation exists: untrusted IP but access allowed
        s.add(Not(in_trusted))      # external IP
        s.add(access_possible == True)  # and still allowed?

        result = s.check()
        print(f"\n--- Checking IP: {ip_value} ---")
        if result == sat:
            print("Zelkova: sat → Policy flaw detected ❌")
            print(f"Example model: {s.model()}")
        else:
            print("Zelkova: unsat → Policy safe ✅ (no unintended access)")

        s.pop()  # restore state

if __name__ == "__main__":
    zelkova_s3_ip_analysis()
