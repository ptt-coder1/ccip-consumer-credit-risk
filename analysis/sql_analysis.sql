-- =========================================================
-- sql_analysis.sql — Giai đoạn 4: Phân tích SQL
-- Trả lời các câu hỏi nghiên cứu RQ1–RQ6
-- Chạy từng block trong DBeaver hoặc pgAdmin
-- =========================================================

-- =========================================================
-- RQ1: Phân khúc khách hàng rủi ro cao
-- Problem Question: Tại sao một số nhóm khách hàng có khả năng
--                   vỡ nợ cao hơn các nhóm khác?
-- Research Question: Các đặc điểm nhân khẩu học và thu nhập có
--                    mối quan hệ như thế nào với khả năng vỡ nợ,
--                    nhóm nào cần được giám sát đặc biệt?
-- Evidence Level: Association
-- =========================================================

-- RQ1.1: Tỷ lệ vỡ nợ theo nhóm tuổi
SELECT
    dc.age_group,
    COUNT(*)                                        AS so_khoan_vay,
    SUM(fl.is_default)                              AS so_vo_no,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct,
    ROUND(AVG(fl.loan_amount), 0)                   AS so_tien_trung_binh
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY dc.age_group
ORDER BY ty_le_vo_no_pct DESC;


-- RQ1.2: Top 10 nghề nghiệp có tỷ lệ vỡ nợ cao nhất
SELECT
    COALESCE(dc.occupation, 'Không xác định')       AS nghe_nghiep,
    COUNT(*)                                        AS so_khoan_vay,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
GROUP BY dc.occupation
HAVING COUNT(*) >= 100  -- Lọc nhóm ít mẫu
ORDER BY ty_le_vo_no_pct DESC
LIMIT 10;


-- RQ1.3: Ma trận rủi ro theo thu nhập × học vấn
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
ORDER BY ty_le_vo_no_pct DESC;


-- =========================================================
-- RQ2: Ảnh hưởng của lịch sử tín dụng đến vỡ nợ
-- Problem Question: Quá khứ tín dụng có thể cảnh báo nguy cơ
--                   vỡ nợ trong tương lai đến mức nào?
-- Research Question: Lịch sử tín dụng và hành vi quá hạn trong
--                    quá khứ có giá trị dự báo mạnh đến mức nào,
--                    và khi kết hợp với các yếu tố khác thì đánh
--                    giá rủi ro thay đổi ra sao?
-- Evidence Level: Predictive evidence
-- =========================================================

-- RQ2.1: So sánh tỷ lệ vỡ nợ: có / không có lịch sử quá hạn
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
ORDER BY ty_le_vo_no_pct DESC;


-- RQ2.2: Tương quan giữa điểm tín dụng bên ngoài và vỡ nợ
-- CORR() trả về hệ số tương quan Pearson / Point-biserial (-1 đến 1)
SELECT
    ROUND(CORR(dc.ext_score_avg, fl.is_default)::numeric, 4)
                                                     AS corr_ext_score_default,
    ROUND(CORR(dc.pct_late_months, fl.is_default)::numeric, 4)
                                                     AS corr_late_months_default,
    ROUND(CORR(dc.num_external_credits, fl.is_default)::numeric, 4)
                                                     AS corr_num_credits_default
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
WHERE dc.ext_score_avg IS NOT NULL;


-- =========================================================
-- RQ3: Khu vực địa lý và rủi ro
-- Problem Question: Rủi ro có thay đổi theo cách sản phẩm /
--                   khu vực tín dụng được thiết kế hay không?
-- Research Question: Khu vực địa lý có phản ánh khác biệt về
--                    rủi ro và quy mô khoản vay không, và khác biệt
--                    đó có còn tồn tại sau khi kiểm soát các đặc điểm
--                    khách hàng khác không?
-- Evidence Level: Adjusted association (raw association, chưa kiểm soát biến khác)
-- =========================================================

SELECT
    dr.region_label,
    dr.risk_level,
    COUNT(*)                                        AS so_khoan_vay,
    ROUND(AVG(fl.is_default::numeric) * 100, 2)    AS ty_le_vo_no_pct,
    ROUND(AVG(fl.loan_amount), 0)                   AS so_tien_trung_binh
FROM dw.fact_loan fl
JOIN dw.dim_region dr USING (region_sk)
GROUP BY dr.region_label, dr.risk_level
ORDER BY ty_le_vo_no_pct DESC;


-- =========================================================
-- RQ4: Xếp hạng khách hàng theo mức độ rủi ro
-- Problem Question: Làm thế nào chuyển nhiều tín hiệu rủi ro
--                   riêng lẻ thành một đánh giá rủi ro tổng thể?
-- Research Question: Làm thế nào xếp hạng và phân nhóm khách hàng
--                    theo mức độ rủi ro tín dụng tổng hợp (risk_quartile/NTILE)?
-- Evidence Level: Model performance (proxy tuyến tính, chưa phải model PD chuẩn)
-- =========================================================

WITH risk_score AS (
    SELECT
        fl.loan_sk,
        dc.customer_id,
        dc.age_group,
        dc.income_type,
        fl.is_default,
        -- Điểm rủi ro tổng hợp proxy: ext_score thấp = rủi ro cao
        COALESCE(1 - dc.ext_score_avg, 0.5)        AS risk_score_proxy,
        -- Xếp hạng 1–4 (1=ít rủi ro nhất, 4=rủi ro nhất)
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
ORDER BY risk_quartile;


-- =========================================================
-- RQ5: Ngưỡng cảnh báo sớm (Early Warning Thresholds)
-- Problem Question: Cảnh báo ở mức nào để vừa phát hiện được
--                   khách hàng rủi ro vừa không loại nhầm quá
--                   nhiều khách hàng tốt?
-- Research Question: Xác định các ngưỡng định lượng nào từ pct_late_months,
--                    total_overdue_amt và ext_score_avg để kích hoạt
--                    cảnh báo sớm rủi ro tín dụng?
-- Evidence Level: Decision threshold (statistical threshold, cần validate ở GĐ 6)
-- =========================================================

SELECT
    -- 1. Ngưỡng 90% số tháng trả trễ
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY dc.pct_late_months)
                                                    AS p90_pct_late_months,
    -- 2. Ngưỡng 90% nợ quá hạn CHỈ TRÊN TẬP KHÁCH HÀNG CÓ NỢ QUÁ HẠN > 0 (tránh suy biến P90=0)
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY dc.total_overdue_amt) 
        FILTER (WHERE dc.total_overdue_amt > 0)     AS p90_total_overdue_amt_khi_co_no,
    -- 3. Điểm tín dụng ngưỡng thấp P10
    PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY dc.ext_score_avg)
                                                    AS p10_ext_score_avg
FROM dw.fact_loan fl
JOIN dw.dim_customer dc USING (customer_sk)
WHERE dc.pct_late_months IS NOT NULL;


-- =========================================================
-- BONUS: Dashboard metric — dùng trong Power BI nếu cần
-- =========================================================

-- Tổng quan toàn bộ danh mục vay
SELECT
    COUNT(*)                                        AS tong_so_khoan_vay,
    ROUND(SUM(loan_amount) / 1e6, 2)               AS tong_gia_tri_ty_usd,
    ROUND(AVG(loan_amount), 0)                      AS so_tien_trung_binh,
    ROUND(AVG(is_default::numeric) * 100, 2)       AS ty_le_vo_no_pct,
    SUM(is_default)                                 AS tong_so_vo_no
FROM dw.fact_loan;


-- =========================================================
-- RQ6: Bối cảnh kinh tế vĩ mô (fact_economy)
-- Problem Question: Khi môi trường kinh tế thay đổi, rủi ro tín dụng
--                   của khách hàng có thể thay đổi như thế nào?
-- Research Question: Môi trường kinh tế giai đoạn 2010–2018 tại thị trường
--                    hoạt động của Home Credit ra sao và đặt ra bối cảnh
--                    gì cho các chỉ số tín dụng?
-- Evidence Level: Context only
-- Lưu ý: fact_loan chỉ có 1 mốc (2017-09 = date_id 129).
--   Dữ liệu fact_economy phân tích ĐỘC LẬP theo năm qua dim_time.
-- =========================================================

-- RQ6.1: Xu hướng lạm phát & tăng trưởng GDP của Nga (thị trường Home Credit)
SELECT
    dt.year,
    fe.country_code,
    ROUND(fe.gdp_growth_pct, 2)                     AS gdp_growth_pct,
    ROUND(fe.inflation_cpi_pct, 2)                  AS inflation_cpi_pct
FROM dw.fact_economy fe
JOIN dw.dim_time dt ON fe.date_id = dt.date_id
WHERE fe.country_code = 'RU'
  AND fe.source = 'worldbank'
ORDER BY dt.year;


-- RQ6.2: Lãi suất FED & lạm phát Mỹ — ảnh hưởng chi phí vốn
-- World Bank: dữ liệu theo năm | FRED: dữ liệu theo tháng (dùng avg theo năm)
SELECT
    dt.year,
    ROUND(AVG(fe.fed_funds_rate)::numeric, 4)       AS fed_rate_avg,
    ROUND(AVG(fe.unemployment_us_pct)::numeric, 2)  AS unemployment_us_avg_pct,
    ROUND(AVG(fe.cpi_us)::numeric, 2)               AS cpi_us_avg
FROM dw.fact_economy fe
JOIN dw.dim_time dt ON fe.date_id = dt.date_id
WHERE fe.source = 'fred'
GROUP BY dt.year
ORDER BY dt.year;


-- RQ6.3: Tổng hợp so sánh đa quốc gia năm 2017
-- (năm xảy ra phần lớn khoản vay trong dataset Home Credit)
SELECT
    fe.country_code,
    fe.country_name,
    ROUND(fe.gdp_growth_pct, 2)                     AS gdp_growth_pct,
    ROUND(fe.inflation_cpi_pct, 2)                  AS inflation_cpi_pct
FROM dw.fact_economy fe
JOIN dw.dim_time dt ON fe.date_id = dt.date_id
WHERE fe.source = 'worldbank'
  AND dt.year = 2017
ORDER BY fe.gdp_growth_pct DESC;
