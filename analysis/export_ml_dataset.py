"""
export_ml_dataset.py — CCIP ML Dataset Extractor
Xuất bảng dữ liệu ML-ready từ Data Warehouse (PostgreSQL) sang định dạng Parquet.

Data Grain Contract:
  - 1 dòng = 1 hồ sơ vay (SK_ID_CURR / customer_id / loan_sk)
  - Số lượng dòng: 307,511
  - Target: is_default (0 / 1), tỷ lệ vỡ nợ portfolio: 8.07%
"""

import os
import sys
from pathlib import Path
import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}"
    f":{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}"
    f":{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB', 'ccip_dw')}"
)

EXPORT_QUERY = """
SELECT
    -- Identifiers
    fl.loan_sk,
    fl.customer_sk,
    fl.customer_id,

    -- Target
    fl.is_default                               AS target,

    -- Loan Features (fact_loan)
    fl.contract_type,
    fl.loan_amount                              AS amt_credit,
    fl.annuity_amount                           AS amt_annuity,
    fl.goods_price                              AS amt_goods_price,
    fl.loan_to_value_ratio                      AS loan_to_value,
    fl.income_to_annuity_ratio                  AS income_to_annuity,
    fl.num_documents_provided                   AS num_documents,
    fl.apply_weekday                            AS weekday_appr_process_start,
    fl.apply_hour                               AS hour_appr_process_start,

    -- Customer Demographic & Financial Features (dim_customer)
    dc.age_years,
    dc.age_group,
    dc.gender                                   AS code_gender,
    dc.num_children                             AS cnt_children,
    dc.family_size                              AS cnt_fam_members,
    dc.family_status                            AS name_family_status,
    dc.income_type                              AS name_income_type,
    dc.annual_income                            AS amt_income_total,
    dc.education_level                          AS name_education_type,
    dc.occupation                               AS occupation_type,
    dc.years_employed,
    dc.has_employment,
    dc.owns_car                                 AS flag_own_car,
    dc.owns_realty                              AS flag_own_realty,
    dc.housing_type                             AS name_housing_type,

    -- External Credit Scores
    dc.ext_score_1,
    dc.ext_score_2,
    dc.ext_score_3,
    dc.ext_score_avg,

    -- Bureau Summary Features
    dc.num_external_credits,
    dc.num_active_credits,
    dc.num_closed_credits,
    dc.total_active_credit_amt,
    dc.total_overdue_amt,
    dc.max_overdue_days,
    dc.pct_credits_overdue,
    dc.num_late_payment_months,
    dc.pct_late_months,

    -- Previous Application Summary Features
    dc.num_prev_applications,
    dc.num_approved,
    dc.num_refused,
    dc.approval_rate_pct,
    dc.avg_prev_credit_amt,
    dc.avg_days_since_prev_decision,

    -- Region Features (from staging & dim_region)
    dr.region_rating                            AS region_rating_client,
    stg.region_rating_w_city                    AS region_rating_client_w_city,
    stg.region_population_rel                   AS region_population_relative

FROM dw.fact_loan fl
JOIN dw.dim_customer dc          ON fl.customer_sk = dc.customer_sk
JOIN dw.dim_region dr            ON fl.region_sk = dr.region_sk
JOIN staging.stg_application stg ON fl.customer_id = stg.customer_id
ORDER BY fl.customer_id;
"""

def main():
    print("=" * 65)
    print("🚀 CCIP — EXPORT ML DATASET FROM POSTGRESQL DW")
    print("=" * 65)
    
    print(f"Connecting to database: {os.getenv('POSTGRES_DB', 'ccip_dw')}...")
    engine = sa.create_engine(DB_URL)

    try:
        print("Executing DW analytical feature query...")
        df = pd.read_sql(EXPORT_QUERY, engine)
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        return

    print(f"\n📊 Extracted Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # --- DATA GRAIN & INTEGRITY VALIDATION ---
    print("\n🔍 Validating Data Grain & SSOT Consistency:")
    
    # 1. Total row count check
    expected_rows = 307511
    if len(df) == expected_rows:
        print(f"  ✅ Grain Check: Exactly {expected_rows:,} rows (1 row per loan application)")
    else:
        print(f"  ❌ Grain Check FAILED: Expected {expected_rows:,}, got {len(df):,}")

    # 2. Target distribution check
    target_counts = df['target'].value_counts().to_dict()
    default_rate = df['target'].mean() * 100
    print(f"  ✅ Target Class 0 (Non-default): {target_counts.get(0, 0):,}")
    print(f"  ✅ Target Class 1 (Default):     {target_counts.get(1, 0):,}")
    print(f"  ✅ Portfolio Default Rate:       {default_rate:.2f}% (Expected: 8.07%)")

    # 3. Duplicate check on customer_id
    dup_customers = df['customer_id'].duplicated().sum()
    if dup_customers == 0:
        print("  ✅ Uniqueness Check: 0 duplicate customer IDs")
    else:
        print(f"  ⚠️ Warning: Found {dup_customers} duplicate customer IDs")

    # Output paths
    output_dir = ROOT_DIR / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = output_dir / "ccip_ml_dataset.parquet"
    
    print(f"\n💾 Saving Parquet file to: {parquet_path}")
    df.to_parquet(parquet_path, index=False, compression="snappy")

    file_size_mb = parquet_path.stat().st_size / (1024 * 1024)
    print(f"✅ Export completed successfully! File size: {file_size_mb:.2f} MB")
    print("=" * 65)

if __name__ == "__main__":
    main()
