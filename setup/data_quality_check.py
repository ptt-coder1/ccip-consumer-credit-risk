"""
data_quality_check.py — Kiểm tra chất lượng dữ liệu sau quá trình ELT
"""
import os, sys, psycopg2, psycopg2.extras
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB","ccip_dw"), user=os.getenv("POSTGRES_USER","openpg"),
    password=os.getenv("POSTGRES_PASSWORD","openpgpwd"), host=os.getenv("POSTGRES_HOST","localhost"),
    port=os.getenv("POSTGRES_PORT","5432")
)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def q(sql):
    cur.execute(sql)
    return cur.fetchall()

results = {}

# ─── RAW SCHEMA ───────────────────────────────────────────────
results["raw_row_counts"] = q("""
SELECT table_name, (xpath('/row/cnt/text()',
    query_to_xml(format('SELECT count(*) AS cnt FROM raw.%I', table_name), false, true, '')))[1]::text::int AS rows
FROM information_schema.tables WHERE table_schema='raw' ORDER BY table_name
""")

results["raw_application_null_rate"] = q("""
SELECT
    COUNT(*) AS total,
    ROUND(100.0 * SUM(CASE WHEN target IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS target_null_pct,
    ROUND(100.0 * SUM(CASE WHEN amt_credit IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS credit_null_pct,
    ROUND(100.0 * SUM(CASE WHEN ext_source_1 IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS ext1_null_pct,
    ROUND(100.0 * SUM(CASE WHEN ext_source_2 IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS ext2_null_pct,
    ROUND(100.0 * SUM(CASE WHEN ext_source_3 IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS ext3_null_pct
FROM raw.hc_application_train
""")

results["raw_outlier_days_employed"] = q("""
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN days_employed = 365243 THEN 1 ELSE 0 END) AS outlier_count,
    ROUND(100.0 * SUM(CASE WHEN days_employed = 365243 THEN 1 ELSE 0 END) / COUNT(*), 2) AS outlier_pct
FROM raw.hc_application_train
""")

results["raw_class_imbalance"] = q("""
SELECT
    target, COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM raw.hc_application_train GROUP BY target ORDER BY target
""")

# ─── STAGING SCHEMA ────────────────────────────────────────────
results["stg_application_summary"] = q("""
SELECT
    COUNT(*) AS total_rows,
    ROUND(AVG(age_years)::numeric, 1) AS avg_age,
    ROUND(MIN(age_years)::numeric, 1) AS min_age,
    ROUND(MAX(age_years)::numeric, 1) AS max_age,
    ROUND(AVG(loan_amount)::numeric, 0) AS avg_loan,
    ROUND(AVG(income_to_annuity_ratio)::numeric, 2) AS avg_income_to_annuity,
    SUM(CASE WHEN years_employed IS NULL THEN 1 ELSE 0 END) AS employed_null_after_clean,
    ROUND(100.0 * SUM(CASE WHEN ext_score_avg IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS ext_score_avg_null_pct
FROM staging.stg_application
""")

results["stg_age_group_dist"] = q("""
SELECT age_group, COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM staging.stg_application GROUP BY age_group ORDER BY age_group
""")

results["stg_bureau_summary_quality"] = q("""
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN num_external_credits = 0 THEN 1 ELSE 0 END) AS no_credit_history,
    ROUND(AVG(num_external_credits)::numeric, 1) AS avg_credits,
    ROUND(AVG(max_overdue_days)::numeric, 1) AS avg_max_overdue,
    SUM(CASE WHEN pct_late_months > 0.5 THEN 1 ELSE 0 END) AS high_late_count,
    ROUND(100.0 * SUM(CASE WHEN pct_late_months > 0.5 THEN 1 ELSE 0 END) / COUNT(*), 2) AS high_late_pct
FROM staging.stg_bureau_summary
""")

# ─── DW SCHEMA ─────────────────────────────────────────────────
results["dw_dim_customer_coverage"] = q("""
SELECT
    COUNT(*) AS dim_rows,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(CASE WHEN ext_score_avg IS NULL THEN 1 ELSE 0 END) AS ext_null,
    SUM(CASE WHEN max_overdue_days IS NULL THEN 1 ELSE 0 END) AS overdue_null,
    SUM(CASE WHEN annual_income IS NULL THEN 1 ELSE 0 END) AS income_null,
    ROUND(AVG(age_years)::numeric, 1) AS avg_age
FROM dw.dim_customer
""")

results["dw_fact_loan_integrity"] = q("""
SELECT
    COUNT(*) AS total_facts,
    SUM(CASE WHEN customer_sk IS NULL THEN 1 ELSE 0 END) AS null_customer_sk,
    SUM(CASE WHEN region_sk IS NULL THEN 1 ELSE 0 END) AS null_region_sk,
    SUM(CASE WHEN date_id IS NULL THEN 1 ELSE 0 END) AS null_date_id,
    SUM(is_default) AS total_defaults,
    ROUND(100.0 * AVG(is_default::numeric), 2) AS default_rate_pct,
    ROUND(AVG(loan_amount)::numeric, 0) AS avg_loan_amt,
    ROUND(MIN(loan_amount)::numeric, 0) AS min_loan,
    ROUND(MAX(loan_amount)::numeric, 0) AS max_loan
FROM dw.fact_loan
""")

results["dw_dim_time"] = q("""
SELECT MIN(year) AS min_year, MAX(year) AS max_year, COUNT(*) AS total_months FROM dw.dim_time
""")

results["dw_dim_region"] = q("""
SELECT region_label, risk_level, region_rating FROM dw.dim_region ORDER BY region_rating
""")

results["dw_loan_amount_distribution"] = q("""
SELECT
    CASE
        WHEN loan_amount < 200000 THEN '< 200K'
        WHEN loan_amount < 500000 THEN '200K–500K'
        WHEN loan_amount < 1000000 THEN '500K–1M'
        ELSE '> 1M'
    END AS loan_range,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM dw.fact_loan
GROUP BY loan_range ORDER BY loan_range
""")

results["dw_loan_by_gender"] = q("""
SELECT dc.gender, COUNT(*) AS count,
    ROUND(AVG(fl.is_default::numeric)*100, 2) AS default_rate_pct
FROM dw.fact_loan fl JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY dc.gender ORDER BY default_rate_pct DESC
""")

results["dw_loan_by_contract_type"] = q("""
SELECT fl.contract_type, COUNT(*) AS count,
    ROUND(AVG(fl.is_default::numeric)*100, 2) AS default_rate_pct,
    ROUND(AVG(fl.loan_amount)::numeric, 0) AS avg_loan
FROM dw.fact_loan fl JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY fl.contract_type
""")

results["stg_loan_to_value_outliers"] = q("""
SELECT
    COUNT(*) AS total,
    SUM(CASE WHEN loan_to_value_ratio > 2 THEN 1 ELSE 0 END) AS ltv_over_2,
    SUM(CASE WHEN loan_to_value_ratio IS NULL THEN 1 ELSE 0 END) AS ltv_null,
    ROUND(MIN(loan_to_value_ratio)::numeric, 4) AS min_ltv,
    ROUND(MAX(loan_to_value_ratio)::numeric, 4) AS max_ltv,
    ROUND(AVG(loan_to_value_ratio)::numeric, 4) AS avg_ltv
FROM staging.stg_application
""")

cur.close()
conn.close()

# Output as structured dict for report
import json
output = {}
for key, rows in results.items():
    if rows:
        cols = [d for d in rows[0].keys()]
        output[key] = {
            "columns": cols,
            "rows": [[str(row[c]) for c in cols] for row in rows]
        }
    else:
        output[key] = {"columns": [], "rows": []}

print(json.dumps(output, ensure_ascii=False, indent=2))
