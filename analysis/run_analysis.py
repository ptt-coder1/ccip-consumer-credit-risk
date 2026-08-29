"""
run_analysis.py — Giai đoạn 4: Chạy phân tích SQL & xuất kết quả
Trả lời 6 câu hỏi nghiên cứu RQ1–RQ6 và in kết quả ra terminal.
"""
import os
import sys
import psycopg2
import psycopg2.extras
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "ccip_dw"),
    user=os.getenv("POSTGRES_USER", "openpg"),
    password=os.getenv("POSTGRES_PASSWORD", "openpgpwd"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432")
)

def run_query(label, sql):
    print(f"\n{'='*65}")
    print(f"  {label}")
    print(f"{'='*65}")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [d.name for d in cur.description]
    # Header
    header = " | ".join(f"{c:<25}" for c in cols)
    print(f"  {header}")
    print(f"  {'-'*len(header)}")
    for row in rows:
        line = " | ".join(f"{str(v):<25}" for v in row)
        print(f"  {line}")
    cur.close()
    print(f"  → {len(rows)} dòng kết quả")
    return rows

# =====================================================
# Tổng quan danh mục (Dashboard metric)
# =====================================================
run_query("TỔNG QUAN DANH MỤC VAY (Dashboard KPIs)", """
SELECT
    COUNT(*)                                        AS tong_so_khoan_vay,
    ROUND(SUM(loan_amount) / 1e6, 2)               AS tong_gia_tri_tr_usd,
    ROUND(AVG(loan_amount), 0)                      AS so_tien_trung_binh,
    ROUND(AVG(is_default::numeric) * 100, 2)       AS ty_le_vo_no_pct,
    SUM(is_default)                                 AS tong_so_vo_no
FROM dw.fact_loan
""")

# =====================================================
# RQ1: Phân khúc khách hàng rủi ro cao (Association)
# =====================================================
run_query("RQ1.1 — Tỷ lệ vỡ nợ theo NHÓM TUỔI", """
SELECT
    dc.age_group,
    COUNT(*)                                        AS so_khoan_vay,
    SUM(fl.is_default)                              AS so_vo_no,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct,
    ROUND(AVG(fl.loan_amount), 0)                   AS so_tien_trung_binh
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY dc.age_group
ORDER BY ty_le_vo_no_pct DESC
""")

run_query("RQ1.2 — Top 10 NGHỀ NGHIỆP có tỷ lệ vỡ nợ cao nhất", """
SELECT
    COALESCE(dc.occupation, 'Không xác định')       AS nghe_nghiep,
    COUNT(*)                                        AS so_khoan_vay,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY dc.occupation
HAVING COUNT(*) >= 100
ORDER BY ty_le_vo_no_pct DESC
LIMIT 10
""")

run_query("RQ1.3 — Ma trận rủi ro: THU NHẬP × HỌC VẤN", """
SELECT
    dc.education_level,
    CASE
        WHEN dc.annual_income < 100000  THEN '< 100K'
        WHEN dc.annual_income < 200000  THEN '100K–200K'
        WHEN dc.annual_income < 400000  THEN '200K–400K'
        ELSE '> 400K'
    END                                             AS income_group,
    COUNT(*)                                        AS so_khoan_vay,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY dc.education_level, income_group
ORDER BY ty_le_vo_no_pct DESC
LIMIT 15
""")

# =====================================================
# RQ2: Ảnh hưởng lịch sử tín dụng (Predictive evidence)
# =====================================================
run_query("RQ2.1 — Tỷ lệ vỡ nợ theo LỊCH SỬ QUÁ HẠN", """
SELECT
    CASE
        WHEN dc.max_overdue_days = 0 OR dc.max_overdue_days IS NULL
        THEN 'Chưa từng quá hạn'
        WHEN dc.max_overdue_days <= 30  THEN 'Quá hạn ≤ 30 ngày'
        WHEN dc.max_overdue_days <= 90  THEN 'Quá hạn 31–90 ngày'
        ELSE 'Quá hạn > 90 ngày'
    END                                             AS nhom_qua_han,
    COUNT(*)                                        AS so_khach_hang,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY nhom_qua_han
ORDER BY ty_le_vo_no_pct DESC
""")

run_query("RQ2.2 — Tương quan ĐIỂM TÍN DỤNG (EXT_SOURCE) với vỡ nợ", """
SELECT
    ROUND(CORR(dc.ext_score_avg, fl.is_default)::numeric, 4)
                                                    AS corr_ext_score_default,
    ROUND(CORR(dc.pct_late_months, fl.is_default)::numeric, 4)
                                                    AS corr_late_months_default,
    ROUND(CORR(dc.num_external_credits, fl.is_default)::numeric, 4)
                                                    AS corr_num_credits_default
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
WHERE dc.ext_score_avg IS NOT NULL
""")

# =====================================================
# RQ3: Khu vực địa lý và rủi ro (Adjusted association)
# =====================================================
run_query("RQ3 — Tỷ lệ vỡ nợ theo KHU VỰC ĐỊA LÝ", """
SELECT
    dr.region_label,
    dr.risk_level,
    COUNT(*)                                        AS so_khoan_vay,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct,
    ROUND(AVG(fl.loan_amount), 0)                   AS so_tien_trung_binh
FROM dw.fact_loan fl
JOIN dw.dim_region dr USING (region_sk)
GROUP BY dr.region_label, dr.risk_level
ORDER BY ty_le_vo_no_pct DESC
""")

# =====================================================
# RQ4: Phân loại khách hàng theo risk quartile (Model performance)
# =====================================================
run_query("RQ4 — XẾP HẠNG rủi ro khách hàng (Risk Quartile 1–4)", """
WITH risk_score AS (
    SELECT
        fl.loan_sk,
        fl.is_default,
        COALESCE(1 - dc.ext_score_avg, 0.5)        AS risk_score_proxy,
        NTILE(4) OVER (ORDER BY COALESCE(dc.ext_score_avg, 0) DESC)
                                                    AS risk_quartile
    FROM dw.fact_loan fl
    JOIN dw.dim_customer dc USING (customer_sk)
    WHERE dc.ext_score_avg IS NOT NULL
)
SELECT
    risk_quartile,
    COUNT(*)                                        AS so_khach_hang,
    ROUND(AVG(is_default::numeric) * 100, 2)       AS ty_le_vo_no_pct,
    ROUND(AVG(risk_score_proxy)::numeric, 4)        AS diem_rui_ro_tb
FROM risk_score
GROUP BY risk_quartile
ORDER BY risk_quartile
""")

# =====================================================
# RQ5: Ngưỡng cảnh báo sớm (Decision threshold)
# =====================================================
run_query("RQ5 — NGƯỠNG CẢNH BÁO SỚM (Percentile 90% chuẩn hóa)", """
SELECT
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY dc.pct_late_months)::numeric, 4)
                                                    AS p90_pct_late_months,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY dc.total_overdue_amt)
        FILTER (WHERE dc.total_overdue_amt > 0)::numeric, 0)
                                                    AS p90_overdue_amt_khi_co_no,
    ROUND(PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY dc.ext_score_avg)::numeric, 4)
                                                    AS p10_ext_score_avg
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
WHERE dc.pct_late_months IS NOT NULL
""")

# =====================================================
# RQ6: Bối cảnh kinh tế vĩ mô (dw.fact_economy - Context only)
# Lưu ý: fact_loan chỉ có 1 mốc 2017-09. fact_economy
#         phân tích ĐỘC LẬP theo năm qua dim_time.
# =====================================================
run_query("RQ6.1 — GDP & LẠM PHÁT Nga theo năm (thị trường Home Credit)", """
SELECT
    dt.year,
    fe.country_code,
    ROUND(fe.gdp_growth_pct, 2)                     AS gdp_growth_pct,
    ROUND(fe.inflation_cpi_pct, 2)                  AS inflation_cpi_pct
FROM dw.fact_economy fe
JOIN dw.dim_time dt ON fe.date_id = dt.date_id
WHERE fe.country_code = 'RU'
  AND fe.source = 'worldbank'
ORDER BY dt.year
""")

run_query("RQ6.2 — LÃI SUẤT FED & thất nghiệp Mỹ theo năm (avg tháng)", """
SELECT
    dt.year,
    ROUND(AVG(fe.fed_funds_rate)::numeric, 4)       AS fed_rate_avg,
    ROUND(AVG(fe.unemployment_us_pct)::numeric, 2)  AS unemployment_us_avg_pct,
    ROUND(AVG(fe.cpi_us)::numeric, 2)               AS cpi_us_avg
FROM dw.fact_economy fe
JOIN dw.dim_time dt ON fe.date_id = dt.date_id
WHERE fe.source = 'fred'
GROUP BY dt.year
ORDER BY dt.year
""")

run_query("RQ6.3 — SO SÁNH kinh tế đa quốc gia năm 2017 (năm xảy ra khoản vay)", """
SELECT
    fe.country_code,
    fe.country_name,
    ROUND(fe.gdp_growth_pct, 2)                     AS gdp_growth_pct,
    ROUND(fe.inflation_cpi_pct, 2)                  AS inflation_cpi_pct
FROM dw.fact_economy fe
JOIN dw.dim_time dt ON fe.date_id = dt.date_id
WHERE fe.source = 'worldbank'
  AND dt.year = 2017
ORDER BY fe.gdp_growth_pct DESC
""")

conn.close()
print("\n" + "="*65)
print("  ✅ Giai đoạn 4 HOÀN THÀNH — Kết quả phân tích SQL RQ1–RQ6")
print("="*65 + "\n")
