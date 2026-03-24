<div align="center">

#  RERA: Rare Event Risk Amplification and Assessment

**An End-to-End Pipeline for Mathematical Boundary Discovery, Causal Root-Cause Extraction, and Automated SOTIF Compliance.**

[![CUDA](https://img.shields.io/badge/CUDA-12.1-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![NVIDIA Omniverse](https://img.shields.io/badge/Omniverse_Ready-000000?style=for-the-badge&logo=nvidia&logoColor=76B900)](https://developer.nvidia.com/nvidia-omniverse-platform)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

<br/>

> **The Problem:** Standard simulation platforms tell you *if* an Autonomous Vehicle (AV) crashed. 
>
> **The Solution:** RERA tells you *why* it crashed, exactly what operating conditions are mathematically guaranteed to be safe, and automatically generates the regulatory compliance dossier to prove it.

RERA is a GPU-accelerated validation infrastructure tool designed to orchestrate photorealistic digital twins, mathematically map the safe operating envelopes of autonomous systems, and synthesize auto-repair policy patches.

---

##  See it in Action

<div align="center">
  <img src="docs/assets/pipeline_demo.gif" alt="RERA Execution Demo" width="800"/>
</div>

---

##  Core Architecture 

The engine executes entirely within an isolated, zero-dependency Docker container, dynamically scaling to consume up to 90% of available VRAM for maximum parallelization.

1. **Deep Bayesian Ensemble Search:** Utilizes 5 parallel neural networks to evaluate ~1.4 million scenarios simultaneously in VRAM, filtering "easy" scenarios to hunt the exact mathematical edge of failure.
2. **Procedural Scene Generation:** Translates mathematical edge cases into photorealistic 3D USD scenes using **NVIDIA Omniverse Replicator**.
3. **Ray-Traced Physics Execution:** Evaluates the USD scenes using the high-fidelity sensor models of **NVIDIA DRIVE Sim**.
4. **Boundary Geometry Extraction:** Calculates the Hessian Spectral Norm and Variance Explosions to map the exact "sharpness" (cliff vs. plateau) of the AV's safety boundaries.
5. **Operational Envelope Certification:** Dynamically clusters failures into Instability Regimes and calculates the Weighted Robustness Margin (RM) with 95% Confidence Intervals.
6. **Structural Causal Inference:** Extracts Directed Acyclic Graphs (DAGs) from vehicle telemetry to transition from correlation to causation (e.g., proving a crash was a *Perception Fault* vs. a *Control Fault*).
7. **Automated ISO 21448 (SOTIF) Compliance:** Maps the system's operational limits and causal hazards directly into a formalized JSON dossier for regulatory review.

---

##  Enterprise Output Artifacts

Upon completion, RERA generates a comprehensive suite of audit-grade artifacts saved to the `/results` directory:

*  **`certification_report.html`**: An interactive dashboard detailing the mathematically proven Operational Design Domain (ODD), Regime Clusters, and 7D Curvature Metrics.
*  **`sotif_compliance_dossier.json`**: An automated ISO 21448 compliance export tracking verified safe scenarios and extracted causal hazards.
*  **`RERA_execution_[TIMESTAMP].log`**: Persistent, timestamped enterprise execution logs ready for CI/CD ingestion (Datadog, CloudWatch).
*  **`Auto-Repair Patch`**: Mathematical suggestions for controller covariance and PID tuning generated via differentiable backpropagation.

---

##  Quick Start

RERA is built for zero-friction deployment. The entire environment (CUDA, PyTorch, Causal engines) is containerized.

### 1. Clone & Build
```bash
git clone [https://github.com/YOUR_USERNAME/RERA_Engine.git](https://github.com/YOUR_USERNAME/RERA_Engine.git)
cd RERA_Engine

# Build the GPU-accelerated container
docker build -t RERA-engine -f docker/Dockerfile .
