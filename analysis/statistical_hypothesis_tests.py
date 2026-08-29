"""
statistical_fixes.py — Sửa theo feedback leader DA/BI:
1. Chi-square test + 95% CI cho CH2.1 (nhóm quá hạn n nhỏ)
2. Fix CH5: P90 total_overdue_amt chỉ trên nhóm > 0
3. Trace 22 dòng LTV > 2
4. CI cho tất cả nhóm n < 2000
"""
import sys, os, psycopg2, psycopg2.extras
from pathlib import Path
from dotenv import load_dotenv
from scipy import stats
import numpy as np

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

def sep(title):
    print(f"\n{'='*65}")
    print(f"  {title}")
    print(f"{'='*65}")

# ─────────────────────────────────────────────────────────────
# FIX 1: CH2.1 — Chi-square + 95% Wilson CI cho từng nhóm
# ─────────────────────────────────────────────────────────────
sep("FIX 1 — CH2.1: Kiểm định thống kê nhóm quá hạn")

cur.execute("""
SELECT
    CASE
        WHEN dc.max_overdue_days = 0 OR dc.max_overdue_days IS NULL THEN 'Chua tung qua han'
        WHEN dc.max_overdue_days <= 30  THEN 'Qua han <= 30 ngay'
        WHEN dc.max_overdue_days <= 90  THEN 'Qua han 31-90 ngay'
        ELSE 'Qua han > 90 ngay'
    END AS nhom,
    SUM(fl.is_default)::int      AS defaults,
    COUNT(*)::int                AS total
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY nhom
ORDER BY nhom
""")
rows = cur.fetchall()

groups = {r['nhom']: (r['defaults'], r['total']) for r in rows}

print(f"\n  {'Nhóm':<25} {'n':>8} {'vỡ nợ':>7} {'rate%':>7} {'95% CI':>20} {'Ghi chú'}")
print(f"  {'-'*85}")

# Wilson score interval (chính xác hơn normal approx với n nhỏ)
def wilson_ci(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2*n)) / denom
    margin = (z * np.sqrt(p*(1-p)/n + z**2/(4*n**2))) / denom
    return (max(0, center - margin)*100, min(1, center + margin)*100)

for name, (k, n) in sorted(groups.items(), key=lambda x: x[1][1]):
    lo, hi = wilson_ci(k, n)
    rate = k/n*100
    note = "⚠️ n nhỏ — CI rộng" if n < 5000 else "✅ n đủ lớn"
    print(f"  {name:<25} {n:>8,} {k:>7,} {rate:>7.2f}% [{lo:5.2f}%–{hi:5.2f}%] {note}")

# Chi-square test: 3 nhóm có quá hạn vs nhau
print(f"\n  → Chi-square test (3 nhóm có quá hạn vs nhau):")
g1 = groups.get('Qua han <= 30 ngay', (0,1))
g2 = groups.get('Qua han 31-90 ngay', (0,1))
g3 = groups.get('Qua han > 90 ngay', (0,1))

observed = np.array([
    [g1[0], g1[1]-g1[0]],
    [g2[0], g2[1]-g2[0]],
    [g3[0], g3[1]-g3[0]],
])
chi2, p_val, dof, expected = stats.chi2_contingency(observed)
print(f"     χ² = {chi2:.4f}, df = {dof}, p-value = {p_val:.4f}")
if p_val < 0.05:
    print(f"     → p < 0.05: Có sự khác biệt có ý nghĩa thống kê GIỮA 3 nhóm")
    print(f"       (nhưng CI rộng — cần xem xét power và cỡ mẫu)")
else:
    print(f"     → p ≥ 0.05: KHÔNG đủ bằng chứng để kết luận khác biệt có ý nghĩa")

# Pairwise: <= 30 vs > 90
obs_pair = np.array([
    [g1[0], g1[1]-g1[0]],
    [g3[0], g3[1]-g3[0]],
])
chi2_pair, p_pair, _, _ = stats.chi2_contingency(obs_pair)
print(f"\n  → Pairwise: 'Quá hạn ≤30' vs 'Quá hạn >90':")
print(f"     χ² = {chi2_pair:.4f}, p-value = {p_pair:.4f}")
if p_pair < 0.05:
    print(f"     → Sự khác biệt 18.38% vs 11.35% CÓ ý nghĩa thống kê (p<0.05)")
    print(f"       Nhưng CI vẫn rộng ({wilson_ci(*g1)[0]:.1f}–{wilson_ci(*g1)[1]:.1f}% vs {wilson_ci(*g3)[0]:.1f}–{wilson_ci(*g3)[1]:.1f}%)")
    print(f"       → Insight nên viết lại: bỏ diễn giải nhân quả, chỉ mô tả pattern")
else:
    print(f"     → KHÔNG có ý nghĩa thống kê — insight cần viết lại thận trọng hơn")

# ─────────────────────────────────────────────────────────────
# FIX 2: CH5 — P90 total_overdue_amt CHỈ trên nhóm > 0
# ─────────────────────────────────────────────────────────────
sep("FIX 2 — CH5: Ngưỡng cảnh báo sớm (sửa lỗi logic degenerate)")

cur.execute("""
SELECT COUNT(*) AS tong_co_no_qua_han,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM staging.stg_bureau_summary), 2) AS pct_of_total
FROM staging.stg_bureau_summary
WHERE total_overdue_amt > 0
""")
r = cur.fetchone()
print(f"\n  Số KH có nợ quá hạn (total_overdue_amt > 0): {r['tong_co_no_qua_han']:,} ({r['pct_of_total']}%)")

cur.execute("""
SELECT
    ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY total_overdue_amt)::numeric, 0)
                                                AS p50_overdue_khi_co_no,
    ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_overdue_amt)::numeric, 0)
                                                AS p75_overdue_khi_co_no,
    ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY total_overdue_amt)::numeric, 0)
                                                AS p90_overdue_khi_co_no,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY total_overdue_amt)::numeric, 0)
                                                AS p95_overdue_khi_co_no
FROM staging.stg_bureau_summary
WHERE total_overdue_amt > 0
""")
r2 = cur.fetchone()
print(f"\n  Trong nhóm có nợ quá hạn:")
print(f"  P50 = {r2['p50_overdue_khi_co_no']:>12,}  (median — mức điển hình)")
print(f"  P75 = {r2['p75_overdue_khi_co_no']:>12,}")
print(f"  P90 = {r2['p90_overdue_khi_co_no']:>12,}  ← Ngưỡng cảnh báo đỏ đề xuất")
print(f"  P95 = {r2['p95_overdue_khi_co_no']:>12,}")

# So sánh tỷ lệ vỡ nợ: có nợ quá hạn vs không
cur.execute("""
SELECT
    CASE WHEN sb.total_overdue_amt > 0 THEN 'Co no qua han' ELSE 'Khong co' END AS nhom,
    COUNT(*) AS n,
    ROUND(AVG(fl.is_default::numeric)*100, 2) AS default_rate
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
LEFT JOIN staging.stg_bureau_summary sb ON sb.customer_id = dc.customer_id
GROUP BY nhom
""")
print(f"\n  Tỷ lệ vỡ nợ phân tách theo có/không có nợ quá hạn:")
for r in cur.fetchall():
    print(f"  {r['nhom']:<20} n={r['n']:>7,}  vỡ nợ={r['default_rate']}%")

# ─────────────────────────────────────────────────────────────
# FIX 3: Trace 22 dòng LTV > 2
# ─────────────────────────────────────────────────────────────
sep("FIX 3 — Trace 22 dòng LTV > 2 (kiểm tra lỗi nhập liệu vs thực tế)")

cur.execute("""
SELECT
    fl.contract_type,
    fl.loan_amount,
    ROUND(fl.loan_to_value_ratio::numeric, 4) AS ltv,
    fl.is_default,
    dc.occupation,
    dc.income_type
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
WHERE fl.loan_to_value_ratio > 2
ORDER BY fl.loan_to_value_ratio DESC
""")
rows_ltv = cur.fetchall()
if rows_ltv:
    print(f"\n  {'contract_type':<20} {'LTV':>6} {'loan_amount':>12} {'default':>8} {'occupation':<25}")
    print(f"  {'-'*80}")
    contract_types = {}
    for r in rows_ltv:
        print(f"  {str(r['contract_type']):<20} {float(r['ltv']):>6.2f} {float(r['loan_amount']):>12,.0f} {r['is_default']:>8} {str(r['occupation']):<25}")
        ct = r['contract_type']
        contract_types[ct] = contract_types.get(ct, 0) + 1
    print(f"\n  Phân tích contract_type của {len(rows_ltv)} dòng LTV>2: {contract_types}")
    default_count = sum(1 for r in rows_ltv if r['is_default'] == 1)
    print(f"  Số dòng bị vỡ nợ: {default_count}/{len(rows_ltv)} ({default_count/len(rows_ltv)*100:.1f}%)")
else:
    print("  Không có dòng LTV > 2 trong fact_loan")

# ─────────────────────────────────────────────────────────────
# FIX 4: CI cho các nhóm n < 2000 trong CH1
# ─────────────────────────────────────────────────────────────
sep("FIX 4 — 95% CI cho các nhóm n < 5,000 trong CH1")

cur.execute("""
SELECT
    COALESCE(dc.occupation, 'Không xác định') AS nghe_nghiep,
    COUNT(*)::int AS n,
    SUM(fl.is_default)::int AS defaults
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY dc.occupation
HAVING COUNT(*) BETWEEN 100 AND 5000
ORDER BY SUM(fl.is_default)::float/COUNT(*) DESC
LIMIT 10
""")
print(f"\n  Các nghề nghiệp n<5,000 với 95% Wilson CI:")
print(f"  {'Nghề nghiệp':<25} {'n':>6} {'rate%':>7} {'95% CI':>22}")
print(f"  {'-'*65}")
for r in cur.fetchall():
    lo, hi = wilson_ci(r['defaults'], r['n'])
    print(f"  {r['nghe_nghiep']:<25} {r['n']:>6,} {r['defaults']/r['n']*100:>7.2f}% [{lo:5.2f}% – {hi:5.2f}%]")

cur.close()
conn.close()

print("\n" + "="*65)
print("  ✅ Hoàn thành kiểm định thống kê — sẵn sàng cập nhật báo cáo")
print("="*65)
