# Hybrid Zelkova–MIRA Policy Evaluation Report
**Sample output of hybrid.py**

This report combines **Zelkova logical verification** (SAT/UNSAT) with **MIRA intent-aware evaluation** (S/V/N).

| IP Address | Zelkova (SAT/UNSAT) | Goal Intended | Access Possible | MIRA State | Meaning |
|-------------|---------------------|----------------|-----------------|-------------|----------|
| `192.168.1.10` | UNSAT (safe ✅) | True | True | S | Satisfied (goal achieved) |
| `203.0.113.5` | UNSAT (safe ✅) | True | False | V | Violated (goal blocked) |
| `192.168.255.200` | UNSAT (safe ✅) | False | True | N | Neutral (no intention) |

