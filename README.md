# Consumer Credit Intelligence Platform (CCIP)
## End-to-End Enterprise Credit Risk Intelligence: ELT Data Warehouse, Executive BI & Interpretable Machine Learning

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Report-F2C811.svg?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![LightGBM](https://img.shields.io/badge/LightGBM-GBDT-brightgreen.svg)](https://lightgbm.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-ff69b4.svg)](https://shap.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Summary

**Consumer Credit Intelligence Platform (CCIP)** is an enterprise-grade credit risk analytics and intelligence platform built on **307,511 loan applications** (~184.2 Billion Currency Units total exposure). 

CCIP bridges the critical gap between raw transactional systems, executive decision-making, and predictive data science by implementing a strict **Single Source of Truth (SSOT)**:
$$\text{Raw Multi-Table Ingestion} \longrightarrow \text{Star Schema DWH} \longrightarrow \text{Executive Power BI Storyboard} \longrightarrow \text{ML Risk Ranking (LightGBM + SHAP)} \longrightarrow \text{Actionable Governance}$$

```
┌─────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│     DATA ENGINEERING    │      │      DESCRIPTIVE BI     │      │      PREDICTIVE ML      │
│  PostgreSQL Star Schema │ ───► │  Power BI 4-Page Story  │ ───► │  LightGBM + SHAP (Colab)│
│  307,511 Rows (SSOT)    │      │  Executive UX (T9 Pass) │      │  AUC: 0.7636 | AP:0.2535│
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
| **Portfolio Baseline** | **8.07%** Default Rate (`24,825` defaults / `307,511` loans) | **184.2B CU** total portfolio exposure; **~13.8B CU** total amount at risk. |
| **Monotonic Risk Gradient** | **Q1 (2.71%) $\longrightarrow$ Q4 (17.28%)** | Q4 default rate is **6.38× higher** than Q1; Q4 accounts for **43.5%** of all portfolio defaults. Pearson $r = -0.2229$. |
| **Critical Risk Hotspot** | **Q4 × T1 Hotspot = 19.91% Default Rate** | **16,158 applications** ($5.25\%$ of portfolio) with **2.10B CU exposure at risk**. Default rate is **2.47×** the portfolio baseline. |
| **ML Predictive Lift** | **ROC-AUC = 0.7636 \| Average Precision (AP) = 0.2535** | $+1.10\text{ pp}$ AUC and $+1.62\text{ pp}$ AP over Logistic Regression baseline. AP is **3.14×** random baseline prevalence. |
| **SQL $\leftrightarrow$ ML Consistency** | **Holdout Test Set Hotspot = 19.90%** (Gap: **0.01 pp**) | Confirms structural model robustness and aligns predictive scores (Mean: **67.48**) with DWH descriptive metrics. |

---

## 🏗️ System Architecture & Pipeline Design

### 1. Data Warehouse Layer (PostgreSQL 16)
- **Dimensional Modeling:** Kimball-standard Star Schema with strict grain rule: **1 Row = 1 Application = 1 Customer = 1 Target (307,511 rows)**.
- **Tables:**
  - `dw.fact_loan`: 307,511 loan records with exposure, annuity, goods price, LTV, affordability ratios.
  - `dw.dim_customer`: Demographics, income, education, employment, and aggregated Bureau history.
  - `dw.dim_region`: 3-tier geographic economic risk classifications.
  - `dw.dim_time` & `dw.fact_economy`: Macroeconomic context tracking (GDP, Inflation, Unemployment).

### 2. Executive BI Layer (Power BI Desktop)
- **4-Page Executive Storyboard:**
  - **P1 - Portfolio Overview:** Macro exposure cards (184.2B CU, 8.07% baseline, 13.8B CU at risk) and product mix.
  - **P2 - Risk Segments:** Monotonic risk quartile distribution (Q1 2.71% $\rightarrow$ Q4 17.28%).
  - **P3 - Risk Hotspots Drill-down:** Interactive $4 \times 4$ Matrix Heatmap (EXT Quartiles $\times$ Affordability Tiers) highlighting the **Q4 × T1 (19.91%)** cluster.
  - **P4 - Borrower Risk Profile:** Deep dive into demographics (<25 age: 12.31%) and education/employment cross-tabulation.
- **Centralized DAX Architecture:** Dynamic hex interpolation (`Heatmap Cell Color`), dynamic tooltips, and strict decoupling from presentation layers. Passed executive UX validation (T9 Protocol).

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

### 1. Clone the Repository & Setup Environment
```bash
git clone https://github.com/your-username/ccip-consumer-credit-risk.git
cd ccip-consumer-credit-risk

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Start PostgreSQL Warehouse
```bash
cp .env.example .env
docker compose up -d
```

### 3. Run the End-to-End Pipeline
```bash
# Execute DWH transformations and export the ML dataset
python run_pipeline.py
python analysis/export_ml_dataset.py
```

### 4. Run Machine Learning & Explainability
Open and run `analysis/02_python_analysis.ipynb` locally or via Google Colab to train the models and generate SHAP values.

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
