import os
import re
import subprocess

os.makedirs('pages', exist_ok=True)

pages_info = [
    {
        "name": "tabular_query_perturbation.md",
        "title": "The Tabular Query Perturbation Era",
        "diagram": "flowchart TD\n    A[Database] --> B{Query}\n    B --> C[Compute Result]\n    C --> D[Add Noise]\n    D --> E[Output Result]",
        "match": "**The Tabular Query Perturbation Era (Statistical Databases, 2006–2013)**",
        "replace": "[**The Tabular Query Perturbation Era (Statistical Databases, 2006–2013)**](pages/tabular_query_perturbation.md)"
    },
    {
        "name": "local_dp_era.md",
        "title": "The Local Differential Privacy Era",
        "diagram": "flowchart TD\n    A[User Device] --> B[Randomize Data]\n    B --> C[Send to Server]\n    C --> D[Aggregate Data]",
        "match": "**The Local Differential Privacy Era (Client-Side Randomization, ~2014–2015)**",
        "replace": "[**The Local Differential Privacy Era (Client-Side Randomization, ~2014–2015)**](pages/local_dp_era.md)"
    },
    {
        "name": "dp_sgd_era.md",
        "title": "The Private Optimization Gradient Era",
        "diagram": "flowchart TD\n    A[Data] --> B[Compute Gradient]\n    B --> C[Clip Gradient]\n    C --> D[Add Noise]\n    D --> E[Update Weights]",
        "match": "**The Private Optimization Gradient Era (DP-SGD, 2016–2023)**",
        "replace": "[**The Private Optimization Gradient Era (DP-SGD, 2016–2023)**](pages/dp_sgd_era.md)"
    },
    {
        "name": "foundation_model_era.md",
        "title": "The Foundation Model Fine-Tuning Era",
        "diagram": "flowchart TD\n    A[Public Pre-training] --> B[Frozen Backbone]\n    B --> C[Private Fine-tuning]\n    C --> D[LoRA/Adapters]",
        "match": "**The Foundation Model Fine-Tuning & Distillation Era (~2024–Present)**",
        "replace": "[**The Foundation Model Fine-Tuning & Distillation Era (~2024–Present)**](pages/foundation_model_era.md)"
    },
    {
        "name": "central_dp.md",
        "title": "Central Differential Privacy",
        "diagram": "flowchart TD\n    A[Raw Data] --> B[Central Server]\n    B --> C[Compute]\n    C --> D[Add Noise]\n    D --> E[Output]",
        "match": "**A. Central Differential Privacy (Global DP)**",
        "replace": "[**A. Central Differential Privacy (Global DP)**](pages/central_dp.md)"
    },
    {
        "name": "local_dp.md",
        "title": "Local Differential Privacy",
        "diagram": "flowchart TD\n    A[User Data] --> B[Local Noise]\n    B --> C[Central Server]",
        "match": "**B. Local Differential Privacy (LDP)**",
        "replace": "[**B. Local Differential Privacy (LDP)**](pages/local_dp.md)"
    },
    {
        "name": "dp_sgd.md",
        "title": "Differentially Private SGD",
        "diagram": "flowchart TD\n    A[Gradient] --> B[Clip]\n    B --> C[Noise]\n    C --> D[Update]",
        "match": "**C. Differentially Private SGD (DP-SGD)**",
        "replace": "[**C. Differentially Private SGD (DP-SGD)**](pages/dp_sgd.md)"
    },
    {
        "name": "epsilon_budget.md",
        "title": "Epsilon Privacy Budget",
        "diagram": "flowchart TD\n    A[Dataset 1] --> B[Algorithm]\n    C[Dataset 2] --> B\n    B --> D[Similar Output Distributions]",
        "match": "**The $\\epsilon$-Privacy Budget Dial (Pure DP)**",
        "replace": "[**The $\\epsilon$-Privacy Budget Dial (Pure DP)**](pages/epsilon_budget.md)"
    },
    {
        "name": "delta_probability.md",
        "title": "Delta Failure Probability",
        "diagram": "flowchart TD\n    A[Privacy Bound] --> B[Success Probability 1-Delta]\n    A --> C[Failure Probability Delta]",
        "match": "**The $\\delta$-Failure Probability Cap (Approximate DP)**",
        "replace": "[**The $\\delta$-Failure Probability Cap (Approximate DP)**](pages/delta_probability.md)"
    },
    {
        "name": "renyi_dp.md",
        "title": "Renyi Differential Privacy",
        "diagram": "flowchart TD\n    A[Moments of Privacy Loss] --> B[RDP Accountant]\n    B --> C[Tight Bounds Epsilon, Delta]",
        "match": "**Rényi Differential Privacy (RDP Accounting)**",
        "replace": "[**Rényi Differential Privacy (RDP Accounting)**](pages/renyi_dp.md)"
    },
    {
        "name": "memory_wall.md",
        "title": "Per-Sample Gradient Tracking Memory Wall",
        "diagram": "flowchart TD\n    A[Standard Backprop] --> B[Aggregate Gradients]\n    C[DP-SGD Backprop] --> D[Per-sample Tracking]\n    D --> E[JIT Compilation / Opacus]",
        "match": "**The Per-Sample Gradient Tracking Memory Wall**",
        "replace": "[**The Per-Sample Gradient Tracking Memory Wall**](pages/memory_wall.md)"
    },
    {
        "name": "capability_collapse.md",
        "title": "Noise-Induced Capability Collapse",
        "diagram": "flowchart TD\n    A[Model] --> B[Excessive Clipping & Noise]\n    B --> C[Capability Collapse]\n    C --> D[Mitigation: Pre-training]",
        "match": "**The Noise-Induced Gradient Clipping Capability Collapse**",
        "replace": "[**The Noise-Induced Gradient Clipping Capability Collapse**](pages/capability_collapse.md)"
    },
    {
        "name": "financial_aml.md",
        "title": "Financial Risk & AML",
        "diagram": "flowchart TD\n    A[Bank A] --> B[Federated DP-SGD]\n    C[Bank B] --> B\n    B --> D[Global AML Model]",
        "match": "**Privacy-Sovereign Financial Risk and Anti-Money Laundering Training**",
        "replace": "[**Privacy-Sovereign Financial Risk and Anti-Money Laundering Training**](pages/financial_aml.md)"
    },
    {
        "name": "clinical_genomic.md",
        "title": "Clinical Pathology & Genomic Research",
        "diagram": "flowchart TD\n    A[Patient Scans] --> B[DP Training Layers]\n    B --> C[Diagnostic Assistance Model]",
        "match": "**HIPAA-Compliant Clinical Pathology & Genomic Diagnostic Research**",
        "replace": "[**HIPAA-Compliant Clinical Pathology & Genomic Diagnostic Research**](pages/clinical_genomic.md)"
    },
    {
        "name": "decentralized_telemetry.md",
        "title": "Decentralized Consumer Telemetry",
        "diagram": "flowchart TD\n    A[Smartphones] --> B[LDP Algorithms]\n    B --> C[Aggregated Analytics]",
        "match": "**Decentralized Consumer Telemetry and Local Text Autocomplete Scaling**",
        "replace": "[**Decentralized Consumer Telemetry and Local Text Autocomplete Scaling**](pages/decentralized_telemetry.md)"
    }
]

for p in pages_info:
    content = f"# {p['title']}\n\nDetailed information about {p['title']} and its relevance to differential privacy.\n\n```mermaid\n{p['diagram']}\n```\n"
    with open(f"pages/{p['name']}", "w", encoding="utf-8") as f:
        f.write(content)

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

for p in pages_info:
    readme = readme.replace(p["match"], p["replace"])

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("Created pages and updated README.")
