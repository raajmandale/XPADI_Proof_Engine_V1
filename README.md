<p align="center">
  <img src="./assets/banner.svg" width="1000" alt="XPADI Banner">
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
  <a href="./docs/index.html">
    <img src="https://img.shields.io/badge/View-Command_UI-0A84FF?style=for-the-badge&logo=googlechrome&logoColor=white" alt="View Command UI">
  </a>
  <a href="https://zenodo.org/records/19500143">
    <img src="https://img.shields.io/badge/Read-Research_Paper-7A1CAC?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Research Paper">
  </a>
</p>

<p align="center">
  <b>ATTACK / DELETION / CORRUPTION ≠ PERMANENT DATA LOSS</b>
</p>

---

## ⚡ 2040 Command UI Preview

<p align="center">
  <img src="./assets/xpadi-ui-preview.gif" width="1000" alt="XPADI 2040 Command UI Preview">
</p>

<p align="center">
  <b>SELECT → PROTECT → ATTACK → RECOVER → VERIFY</b><br>
  Real-time survivability proof, not simulation theater
</p>

---

## 🧠 What is XPADI

XPADI is a **Survivability-Governed Data System (SGDS)**.

It does not focus on storage first.  
It focuses on **outcome continuity**.

Traditional systems ask:

> Can we store and recover data?

XPADI asks:

> Can data survive disruption itself?

---

## 🚨 Why This Matters

Modern data systems still break at the wrong moment:

- Backup depends on restore points
- RAID covers only limited hardware failure
- Recovery tools are often uncertain
- Corruption can still lead to irreversible loss

XPADI introduces a different model:

- ✅ survivability-first design
- ✅ deterministic reconstruction
- ✅ integrity-verified output
- ✅ failure-resilient data state

---

## 📊 System Snapshot

| Signal | State |
|--------|-------|
| Protected Files | 12,480 |
| Fragments Generated | 96,112 |
| Recovery Confidence | 99.94% |
| Integrity Drift | 0.00% |

---

## 🌐 System Positioning

XPADI sits above ordinary storage behavior and focuses on the one thing most systems do not prove clearly:

> whether data can survive disruption itself.

It is not centered on copy count.  
It is centered on **survivability outcome**.

---

## 🚀 60-Second Quickstart

Get XPADI running in less than a minute.

---

### 1. Clone the repository

git clone https://github.com/raajmandale/XPADI_Proof_Engine_V1.git  
cd XPADI_Proof_Engine_V1  

---

### 2. Install dependencies

pip install -r requirements.txt  

---

### 3. Run the proof engine

python run.py  

---

### 4. Open the interface

http://127.0.0.1:8000  

---

### Example Output

[SAFE MODE] Original file protected  

Creating internal proof state...  
Fragmenting...  
Encrypting...  
Simulating attack...  

Reconstructing file...  
Verifying integrity...  

SUCCESS: DATA MATCHED  
FINAL RESULT: ATTACK ≠ DATA LOSS  

---

## 🧬 Architecture

<p align="center">
  <img src="./assets/architecture.svg" width="900">
</p>

XPADI operates as a controlled survivability pipeline:

- Source remains untouched  
- Protection layer creates internal state  
- Attack is applied to derived state  
- Reconstruction rebuilds deterministically  
- Verification confirms integrity  

---

## 🔄 Survivability Flow

<p align="center">
  <img src="./assets/flow.svg" width="900">
</p>

Source → Protected State → Attack → Reconstruction → Verification  

---

## 🔬 What This Repo Proves

XPADI demonstrates:

- Data is never directly exposed  
- Disruption affects only internal state  
- Reconstruction is deterministic  
- Integrity validation is exact  
- Final outcome survives disruption  

---

## ⚙️ Execution Model

XPADI runs in a controlled proof environment:

- Source is sealed  
- Internal state is generated  
- Attack is simulated internally  
- Reconstruction resolves structure  
- Output is verified  

---

## 📊 Output Guarantee

hash(original) == hash(reconstructed)  

If true:

ATTACK ≠ DATA LOSS  

---

## 📂 Project Structure

XPADI_Proof_Engine_V1/

- app → UI + orchestration  
- core → processing engine  
- assets → visuals  
- docs → demo UI  
- templates → HTML layer  
- logs → runtime logs  
- data → workspace  

run.py  
requirements.txt  
README.md  

---

## ⚖️ System Comparison

Backup → needs restore  
RAID → limited scope  
Recovery tools → uncertain  

XPADI → deterministic survivability  

---

## 🔮 Strategic Direction

Past  
- deletion  
- disk failure  
- corruption  

Present  
- survivability proof  
- deterministic reconstruction  
- integrity validation  

Future  
- AI-native memory  
- advanced storage  
- survivability-first systems  

---

## 📄 Research Paper

https://zenodo.org/records/19500143  

---

## 👤 Author

Raaj Mandale  
Founder — ERANEST Technoware Pvt Ltd  

https://raajmandale.in  

---

## 📄 License

MIT License  

---

## Final Statement

XPADI is not a backup system.  
It is not a recovery tool.  
It is a proof that data can survive disruption itself.