<p align="center">
  <img src="assets/xpadi-banner.svg" width="1000" alt="XPADI Banner">
</p>

<h1 align="center">XPADI</h1>

<p align="center">
  <b>Survivability Proof Engine</b><br>
  Outcome-preserving data systems across attack, failure, and unknown states
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-proof--engine-blue?style=for-the-badge" alt="status">
  <img src="https://img.shields.io/badge/system-SGDS-green?style=for-the-badge" alt="system">
  <img src="https://img.shields.io/badge/mode-safe--simulation-purple?style=for-the-badge" alt="mode">
  <img src="https://img.shields.io/badge/version-v1-orange?style=for-the-badge" alt="version">
</p>

<p align="center">
  <a href="#-60-second-quickstart">
    <img src="https://img.shields.io/badge/Run-Locally-black?style=for-the-badge&logo=terminal" alt="Run Locally">
  </a>
  <a href="docs/index.html">
    <img src="https://img.shields.io/badge/View-Command_UI-blue?style=for-the-badge&logo=googlechrome" alt="View Command UI">
  </a>
  <a href="https://zenodo.org/records/19500143">
    <img src="https://img.shields.io/badge/Read-Research_Paper-purple?style=for-the-badge&logo=readthedocs" alt="Research Paper">
  </a>
</p>

---

## ⚡ 2040 Command UI Preview

<p align="center">
  <img src="assets/xpadi-ui-preview.gif" width="1000" alt="XPADI 2040 Command UI Preview">
</p>

<p align="center">
  <b>SELECT → PROTECT → ATTACK → RECOVER → VERIFY</b><br>
  Real-time survivability proof, not simulation theater
</p>

---

## 🧠 Core Statement

<p align="center">
  <b>ATTACK / DELETION / CORRUPTION ≠ PERMANENT DATA LOSS</b>
</p>

<p align="center">
  XPADI proves that disruption changes state — not outcome.
</p>

---

## 📊 System Snapshot

| Signal | State |
|--------|-------|
| Protected Files | 12,480 |
| Fragments Generated | 96,112 |
| Recovery Confidence | 99.94% |
| Integrity Drift | 0.00% |

---

## What is XPADI

XPADI is a **Survivability-Governed Data System (SGDS)**.

It does not focus on storage alone.

It focuses on **outcome continuity**.

Traditional systems ask:

> Can we store and recover data?

XPADI asks:

> Can data survive disruption itself?

---

## Why This Matters

Modern data systems still fail in critical ways:

- Backup depends on restore points
- RAID handles only limited hardware failure
- Recovery tools are often uncertain
- Corruption can still lead to irreversible loss

XPADI introduces a different model:

- survivability-first design
- deterministic reconstruction
- integrity-verified output
- failure-resilient data state

---

## System Positioning

<p align="center">
  <img src="assets/xpadi-positioning-map.svg" width="900" alt="XPADI Positioning Map">
</p>

XPADI operates **above traditional storage logic** and focuses on **data survivability across disruption layers and time states**.

---

## 🚀 60-Second Quickstart

### 1. Clone

```bash
git clone https://github.com/raajmandale/XPADI_Proof_Engine_V1.git
cd XPADI_Proof_Engine_V1
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
python -m app.main
```

---

## Example Output

```text
[SAFE MODE] Original file protected

Creating internal proof state...
Fragmenting...
Encrypting...
Simulating attack...

Reconstructing file...
Verifying integrity...

SUCCESS: DATA MATCHED
FINAL RESULT: ATTACK ≠ DATA LOSS
```

---

## Proof Architecture

<p align="center">
  <img src="assets/xpadi-architecture.svg" width="900" alt="XPADI Architecture">
</p>

| Stage | Responsibility |
|------|----------------|
| Source | Original file remains untouched |
| Protection | Internal survivability state is created |
| Attack | Controlled disruption is applied |
| Reconstruction | File is rebuilt deterministically |
| Verification | Hash integrity is validated |

---

## Survivability Flow

<p align="center">
  <img src="assets/xpadi-flow.svg" width="900" alt="XPADI Survivability Flow">
</p>

```text
Source
↓
Protected State
↓
Attack Simulation
↓
Reconstruction
↓
Integrity Verification
```

---

## What This Repo Proves

This repo proves that:

- the original file remains untouched
- attack is executed only on protected state
- reconstruction is deterministic
- integrity is validated through hashing
- outcome survives disruption

---

## Execution Model

XPADI currently operates in **Safe Mode Simulation**:

- Source file is sealed
- Internal working state is created
- Disruption is applied to internal state only
- Reconstruction pipeline executes
- Output is verified against original integrity

---

## Output Guarantee

```text
hash(original) == hash(reconstructed)
```

If true:

<p align="center">
  <b>ATTACK ≠ DATA LOSS</b>
</p>

---

## Project Structure

```text
XPADI_Proof_Engine_V1/
│
├── app/              # UI + orchestration
├── core/             # fragment / encrypt / reconstruct / verify
├── data/             # runtime workspace
├── docs/             # flagship demo + explanation layer
├── assets/           # diagrams + banners
├── tests/            # validation notes
│
├── README.md
├── requirements.txt
└── repo_manifest.json
```

---

## System Comparison

| System | Focus | Limitation |
|--------|-------|------------|
| Backup | Copy | Needs restore |
| RAID | Hardware resilience | Limited failure scope |
| Recovery Tools | Reconstruction | Often uncertain |
| XPADI | Survivability logic | Outcome-driven proof |

---

## Strategic Position

### Past
Protects against:

- deletion
- disk failure
- corruption

### Present
Demonstrates:

- survivability proof
- deterministic reconstruction
- integrity validation

### Future
Aligns with:

- DNA storage
- 5D glass storage
- AI memory systems
- survivability-native architectures

---

## Research Paper

[Zenodo Record](https://zenodo.org/records/19500143)

---

## Author

**Raaj Mandale**  
Founder & Architect  
ERANEST Technoware Pvt Ltd

[raajmandale.in](https://raajmandale.in/)

---

## License

MIT License

---

## Final Statement

XPADI is not a backup system.

It is not a recovery tool.

It is a proof that data can survive disruption itself.
