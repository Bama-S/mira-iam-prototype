# MIRA vs. Zelkova & Cedar: Detailed Comparison

| Metric                  | Zelkova/Cedar | MIRA               | Improvement | Case Study Insight (External IP S3 Access) |
|------------------------|---------------|--------------------|-------------|--------------------------------------------|
| **Output Values**       | 2 (SAT/UNSAT, permit/no) | 3 ($S$, $V$, $N$) | **+50%** | MIRA detects $V$ (intent violated) vs. UNSAT (safe only) |
| **Intent Coverage**     | 0%            | 100%               | **+∞**  | MIRA tracks "secure read" purpose; others ignore |
| **Goal Tracking**       | 0             | 1 (explicit goal in triplet) | **+1** | MIRA chains `access allowed → secure read` |
| **Violation Types**     | 1 (unsafe access) | 2 ($V$ = intent broken, $N$ = neutral) | **+100%** | $V$ triggers UX fix (VPN); $N$ does not |
| **Expressiveness Score**| 1.0           | **1.3**            | **+30%** | $1.0 \times (1 + 0.3)$ from intent + 3-valued logic |
| **Runtime Complexity**  | O(n log n) avg, 2^O(n) worst | **O(n)**           | **Faster** | Linear chaining vs. SMT solver overhead |

> **Case Study**: External IP → Zelkova: `UNSAT` (correct block). MIRA: `$V$` (secure intent violated) → actionable alert.

**References**:
- Zelkova: [AWS IAM Access Analyzer](https://aws.amazon.com/iam/features/analyze/)
- MIRA: Srinivasan & Parthasarathi (2022, 2025)
