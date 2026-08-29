# Consumer Credit Intelligence Platform (CCIP)
### End-to-End Credit Risk Analytics | Data Engineering | Executive BI | Interpretable Machine Learning

> 📊 **Power BI Storyboard** · 🤖 **Interpretable ML Pipeline** · 🐳 **Dockerized Environment** · 📑 **Governance Matrix**

An end-to-end analytics platform transforming **58.5M+ raw records** into a **PostgreSQL Star Schema Data Warehouse**, an interactive **4-Page Executive Power BI Storyboard**, and an interpretable **LightGBM risk-ranking model**.

**Scale:** `307,511` loan applications | `184.2B CU` portfolio exposure | `8.07%` portfolio default rate  
**Stack:** `PostgreSQL 16` · `SQL (ELT)` · `Python 3.11` · `Power BI (DAX / TMDL)` · `LightGBM` · `SHAP` · `Docker`

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Report-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![LightGBM](https://img.shields.io/badge/LightGBM-GBDT-brightgreen.svg)](https://lightgbm.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-ff69b4.svg)](https://shap.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🔎 At a Glance

| Functional Domain | Key Implementation & Deliverable | Technical Stack & Artifacts |
| :--- | :--- | :--- |
| **Data Engineering** | Scalable ELT ingestion pipeline from 58.5M raw records | Python, `psycopg2 COPY`, Streaming Ingestion |
| **Data Warehouse (DWH)** | 3-tier architecture (`RAW` $\rightarrow$ `STAGING` $\rightarrow$ `DW`), Kimball Star Schema (307.5k grain SSOT) | PostgreSQL 16, SQL Views & Tables, Constraints |
| **Executive BI** | 4-Page Storyboard (Overview, Segments, Hotspots, Demographics) | Power BI Desktop, Centralized DAX, TMDL |
| **Statistical Risk Analytics** | Monotonic risk gradient (Q1–Q4) & multivariate $4 \times 4$ Hotspot Matrix | Pearson Correlation, Fixed Operational Cut-offs |
| **Predictive Modeling** | Non-linear risk ranking evaluated on strict holdout test set | LightGBM vs Logistic Regression (ROC-AUC 0.7636, AP 0.2535) |
| **Model Explainability (XAI)** | Global feature importance & risk drivers (Top: `ext_score_avg`, `LTV`) | SHAP (TreeExplainer), 5,000 holdout test samples |
| **Actionable Governance** | 5 core insights mapped to 3 decision tiers (Descriptive, Operational, Policy) | Formal Matrix with designated Decision Owners |
| **Reproducibility** | Containerized ML environment & anonymized sample dataset | Docker (`Dockerfile`, `.dockerignore`), Parquet |

---

## 📌 Executive Summary

**Consumer Credit Intelligence Platform (CCIP)** bridges the critical gap between raw transactional systems, executive decision-making, and predictive data science by implementing a strict **Single Source of Truth (SSOT)**:
$$\text{Raw Multi-Table Ingestion} \longrightarrow \text{Star Schema DWH} \longrightarrow \text{Executive Power BI Storyboard} \longrightarrow \text{ML Risk Ranking (LightGBM + SHAP)} \longrightarrow \text{Actionable Governance}$$

```
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│     DATA ENGINEERING    │      │      DESCRIPTIVE BI     │      │      PREDICTIVE ML      │
│  PostgreSQL Star Schema │ ───► │  Executive BI Storyboard│ ───► │  LightGBM + SHAP (Colab)│
│  307,511 Rows (SSOT)    │      │  Interactive 4-Page App │      │  AUC: 0.7636 | AP:0.2535│
└─────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                              │                                │
                                              └────────────────┬───────────────┘
                                                               ▼
                                              ┌─────────────────────────────────┐
                                              │      ACTIONABLE GOVERNANCE      │
                                              │  5 Insights ──► 3 Decision Lvs  │
                                              └─────────────────────────────────┘
```

---

## 🚀 Key Business & Statistical Findings

| Category | Finding & Metric | Business & Strategic Impact |
| :--- | :--- | :--- |
| **Portfolio Baseline** | **8.07%** Default Rate (`24,825` defaults / `307,511` loans) | **184.2B CU** total portfolio exposure; **~13.8B CU** total amount at risk (`13,846,851,950 CU`). |
| **Operational Risk Segmentation** | **Q1 (2.69%) $\longrightarrow$ Q4 (18.60%)** | Q4 default rate is **6.91× higher (≈6.93x)** than Q1; Q4 accounts for **46.9%** of all portfolio defaults (`11,653 / 24,825`). Pearson $r = -0.2229$. *(Exploratory SQL NTILE baseline: 2.71% $\rightarrow$ 17.28%).* |
| **Critical Risk Hotspot** | **Q4 × T1 Hotspot = 19.90% Default Rate** | **16,158 applications** ($5.25\%$ of portfolio) with **2.10B CU exposure at risk** (`2,096,007,278 CU`). Default rate is **2.47×** the portfolio baseline. |
| **ML Predictive Lift** | **ROC-AUC = 0.7636 \| Average Precision (AP) = 0.2535** | $+1.10\text{ pp}$ ROC-AUC and $+1.62\text{ pp}$ AP over Logistic Regression baseline. AP is **3.14×** random baseline prevalence. |
| **SQL $\leftrightarrow$ ML Consistency** | **Holdout Test Set Hotspot = 19.90%** (Gap: **0.00 pp**) | Confirms structural model robustness and aligns predictive risk ranking scores (Mean: **67.48**) with DWH descriptive metrics. |

---

## 🏗️ System Architecture & Pipeline Design

### 1. Data Warehouse Layer (PostgreSQL 16)
- **Dimensional Modeling:** Kimball-standard Star Schema with strict grain rule: **1 Row = 1 Application = 1 Customer = 1 Target (307,511 rows)**.
- **Tables:**
  - `dw.fact_loan`: 307,511 loan records with exposure, annuity, goods price, LTV, affordability ratios.
  - `dw.dim_customer`: Demographics, income, education, employment, and aggregated Bureau history.
  - `dw.dim_region`: 3-tier geographic economic risk classifications.
  - `dw.dim_time` & `dw.fact_economy`: Macroeconomic context tracking (GDP, Inflation, Unemployment).

### 2. Executive BI Layer (Power BI Desktop Storyboard)

#### 📊 Page 1: Executive Portfolio Overview
*High-level portfolio visibility tracking 307.5k loans, 184.2B CU exposure, 13.85B CU amount at risk, and product risk breakdowns.*
![Executive Portfolio Overview](docs/images/01_portfolio_overview.png)

#### 📊 Page 2: Risk Segmentation (Monotonic Risk Gradient)
*Univariate monotonic risk stratification (Q1 2.69% $\rightarrow$ Q4 18.60%, 6.93× risk ratio) equipped with dynamic metric parameter switcher.*
![Risk Segmentation](docs/images/02_risk_segmentation.png)

#### 📊 Page 3: Risk Drivers & Hotspots ($4 \times 4$ Matrix Heatmap)
*Multivariate risk concentration uncovering the critical **Q4 × T1 Hotspot** (19.90% default rate, 16,158 applications, 2.10B CU exposure at risk).*
![Risk Drivers and Hotspots](docs/images/03_risk_hotspots.png)

#### 📊 Page 4: Borrower Risk Profile (Demographics & Financial Profile)
*Deep demographic analysis across age cohorts (<25: 12.31%), employment status, and education $\times$ income cross-tabulation.*
![Borrower Risk Profile](docs/images/04_borrower_profile.png)

---

### 3. Predictive Machine Learning Layer (LightGBM + SHAP)
- **Leakage-Free Experimental Design:** 60% Train (184,506) / 20% Validation (61,502) / 20% Test Holdout (61,503) stratified split. Early stopping evaluated exclusively on Validation Set.
- **Model Explainability (SHAP):** Global feature importance computed on 5,000 holdout samples identified `ext_score_avg` (Mean $|SHAP| = 0.4320$), `ext_score_3` (0.1532), and `loan_to_value` (0.1308) as top predictive drivers.

---

## 📂 Repository Structure

```
ccip-consumer-credit-risk/
│
├── README.md                               # Executive portfolio presentation & overview
├── LICENSE                                 # MIT Open-Source License
├── .gitignore                              # Strict data, secrets, and cache exclusion
├── requirements.txt                        # Python dependencies
├── docker-compose.yml                      # PostgreSQL 16 container definition
│
├── data/
│   ├── README.md                           # Data governance & sample reproduction guide
│   └── sample_ccip_data.parquet            # 1,000-row anonymized sample dataset
│
├── transform/                              # SQL ELT & Data Warehouse transformation scripts
│   ├── staging/                            # Cleaning, sentinel value handling, type casting
│   │   ├── stg_application.sql
│   │   ├── stg_bureau_summary.sql
│   │   └── stg_previous_application.sql
│   └── dw/                                 # Star Schema tables (Fact & Dimensions)
│       ├── fact_loan.sql
│       ├── dim_customer.sql
│       ├── dim_region.sql
│       ├── dim_time.sql
│       └── fact_economy.sql
│
├── analysis/                               # Analytical & Modeling pipelines
│   ├── export_ml_dataset.py                # Automated DWH-to-Parquet ML dataset extractor
│   ├── sql_analysis.sql                    # SQL analytical queries (RQ1 to RQ6)
│   └── 02_python_analysis.ipynb            # ML training, validation, evaluation & SHAP notebook
│
├── reports/                                # Formal governance & research deliverables
│   ├── findings_and_recommendations_matrix.md  # 5-Insight matrix with 3 decision levels & owners
│   └── ccip_academic_report.md             # Complete 7-chapter academic research report
│
└── docs/                                   # Data dictionaries & analytical documentation
    ├── data_dictionary.md
    └── huong_dan_giai_thich_du_lieu_cho_nguoi_moi.md
```

---

## 🛠️ Tech Stack

- **Core & Storage:** PostgreSQL 16, Docker Compose, Parquet (Snappy Compression).
- **Data Engineering & ETL:** Python 3.10+, SQLAlchemy, psycopg2, pandas, NumPy.
- **Business Intelligence:** Microsoft Power BI, DAX, Tabular Model Definition Language (TMDL).
- **Predictive Analytics:** LightGBM, Scikit-Learn, SHAP, Matplotlib, Seaborn.

---

## 🚦 Quick Start & Reproduction Guide

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.10 or higher

### 1. Clone the Repository
```bash
git clone https://github.com/ptt-coder1/ccip-consumer-credit-risk.git
cd ccip-consumer-credit-risk
```

### 2. Option A: Run via Docker (Recommended for Reproducibility)
Build and run the containerized Python/ML environment with a single command:
```bash
# Build the Docker image
docker build -t ccip-ml-env .

# Run Jupyter Notebook container (accessible at http://localhost:8888)
docker run -it -p 8888:8888 -v ${PWD}:/app ccip-ml-env
```

### 3. Option B: Run Locally (Virtual Environment)
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Start PostgreSQL Warehouse & Run Pipeline
```bash
cp .env.example .env
docker compose up -d

# Execute DWH transformations and export the ML dataset
python run_pipeline.py
python analysis/export_ml_dataset.py
```

### 5. Run Machine Learning & Explainability
Open and run `analysis/02_python_analysis.ipynb` locally, inside the Docker container, or via Google Colab to reproduce models and SHAP explanations on `data/sample_ccip_data.parquet` or the full DWH dataset.

---

## 🗺️ Project Roadmap

- [x] **v1.0 (Current) — End-to-End Analytics & Predictive Intelligence:**
  - PostgreSQL Star Schema DWH (307.5k rows SSOT).
  - Power BI 4-Page Executive Dashboard (P1 $\rightarrow$ P4).
  - LightGBM + SHAP explainability on holdout test set.
  - Actionable Governance Framework with 3-tier Decision Matrix.
- [ ] **v2.0 (Engineering Extension) — Workflow Orchestration:**
  - Apache Airflow DAG orchestration (`validate_source` $\rightarrow$ `run_dwh` $\rightarrow$ `export_ml` $\rightarrow$ `train_model`).
  - Automated data quality assertions (Great Expectations / dbt test).
- [ ] **v3.0 (Cloud Analytical Warehouse):**
  - Cloud migration to Google Cloud BigQuery.
  - Managed Airflow integration.

---

## 📄 License & Attribution

This project is licensed under the [MIT License](LICENSE). Built for enterprise risk intelligence and research demonstration.
