# Data Directory

This directory contains data files for the CCIP (Consumer Credit Intelligence Platform) project.

## ⚠️ Data Privacy & Reproducibility Notice
- **Full Production Dataset (`307,511` records, `18.65 MB`):** Excluded from this Git repository in accordance with data governance, security best practices, and repository size policies.
- **Anonymized Sample (`sample_ccip_data.parquet`):** A small 1,000-record randomized sample is provided for pipeline demonstration, CI/CD testing, and quick schema validation.

## 🔄 How to Generate the Full Dataset
1. Run the local PostgreSQL instance via Docker Compose:
   ```bash
   docker compose up -d
   ```
2. Execute the complete ELT pipeline to build the Star Schema Data Warehouse:
   ```bash
   python run_pipeline.py
   ```
3. Export the ML-ready dataset:
   ```bash
   python analysis/export_ml_dataset.py
   ```
   This will generate `data/processed/ccip_ml_dataset.parquet` (307,511 rows × 50 features).
