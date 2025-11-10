# 🧠 MIRA–Zelkova Hybrid Reasoning Framework

This repository contains a **goal- and intent-aware reasoning framework** that extends AWS Zelkova-style declarative policy verification with **Mīmāṃsā-Inspired Representation of Actions (MIRA)** semantics.

Zelkova and Cedar perform **binary (SAT/UNSAT)** analysis of IAM policies.  
MIRA introduces a **three-valued logic (S, V, N)** based on intention and goal execution, enabling deeper interpretability of policy outcomes.

---

## 📁 Repository Structure

mira-iam-prototype/  
│  
├── src/  
│ ├── mira_instruction_svn/  
│ │ ├── instruction.py  
│ │ ├── sequence.py  
│ │ └── aws_demo.py  
│ │  
│ └── mira_zelkova/  
│ ├── wzel.py  
│ ├── wzel2.py  
│ └── hybrid.py  
│  
├── reports/  
│ ├── mira_zelkova_report.md  
│ └── zelkova_mira_extension_metrics.md  
│ 
└── README.md 


---

## 🚀 How to Run

### 1 **MIRA Instructional Reasoning (Standalone)**

Implements MIRA’s **pure intention–goal–action semantics**, following the Mīmāṃsā-Inspired Representation of Actions (S / V / N).

```bash
cd src/mira_instruction_svn
python3 aws_demo.py 
```
## Description

- instruction.py – core MIRA instruction class (defines S, V, N evaluation)

- sequence.py – supports sequential and temporal reasoning

- aws_demo.py – demonstration with example MIRA instructions (no Zelkova dependency)

## Output:
- Produces step-by-step MIRA reasoning trace showing Success (S), Violation (V), and Neutral (N) outcomes for each action sequence.

### 2 **Hybrid MIRA–Zelkova Reasoning (Z3-Based)**
Integrates Zelkova’s SMT-based policy verification with MIRA’s intent semantics.
```bash
cd src/mira_zelkova
python3 hybrid.py
```
## Description

- wzel.py and wzel2.py – experimental Zelkova-style verifiers using Z3 solver

- hybrid.py – unified hybrid verifier that outputs both:

- Zelkova results (SAT / UNSAT for logical safety)

- MIRA interpretation (S / V / N for intent analysis)

## Output:

- Prints a hybrid table in the console

| Report                                    | Description                                                      | Link                                                                           |
| :---------------------------------------- | :--------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| **Hybrid Zelkova–MIRA Evaluation Report** | Policy-level verification results with intent semantics          | [mira_zelkova_report.md](reports/mira_zelkova_report.md)                       |
| **Zelkova–MIRA Extension Metrics**        | Quantitative metrics showing how MIRA augments Zelkova and Cedar | [zelkova_mira_extension_metrics.md](reports/zelkova_mira_extension_metrics.md) |

🧰 Requirements

 - Python ≥ 3.8 
 - z3-solver  
 - prettytable
- ipaddress (standard library) 

## Install dependencies:
pip install z3-solver prettytable

🪶 License

Released under the MIT License.

## Citation

1.Bama Srinivasan and Ranjani Parthasarathi. A formalism to specify unambiguous instruc-
tions inspired by Mīmām̃sā in computational settings. Logica Universalis, 16:275–305, 2021. 

2.Bama Srinivasan. A Mīmāmsā inspired framework for instruction sequencing in AI agents, arXiv preprint arXiv:2510.17691, 2025.
