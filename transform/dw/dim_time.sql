-- =========================================================
-- dim_time.sql — Star Schema: Dimension thời gian
--
-- Grain: 1 dòng = 1 tháng (YYYY-MM)
-- Lý do chọn tháng thay vì ngày: bộ dữ liệu Home Credit
-- không có ngày vay cụ thể — chỉ có DAYS_* tính từ mốc
-- nộp hồ sơ, nên độ chi tiết phù hợp nhất là theo tháng.
--
-- Chiến lược: generate toàn bộ các tháng trong khoảng
-- 2007–2019 (bao phủ toàn bộ lịch sử dữ liệu).
-- =========================================================

DROP TABLE IF EXISTS dw.dim_time CASCADE;

CREATE TABLE dw.dim_time (
    date_id         SERIAL      PRIMARY KEY,
    year            SMALLINT    NOT NULL,
    month           SMALLINT    NOT NULL,  -- 1–12
    quarter         SMALLINT    NOT NULL,  -- 1–4
    year_month      CHAR(7)     NOT NULL,  -- '2015-03' — tiện dùng trong Power BI
    month_name      VARCHAR(12) NOT NULL,  -- 'March'
    month_name_short VARCHAR(3) NOT NULL,  -- 'Mar'
    is_quarter_end  BOOLEAN     NOT NULL,  -- Tháng cuối quý (3,6,9,12)
    is_year_end     BOOLEAN     NOT NULL,  -- Tháng 12
    UNIQUE (year, month)
);

-- ---------------------------------------------------
-- Generate tất cả tháng từ 2007-01 đến 2019-12
-- dùng generate_series cho gọn
-- ---------------------------------------------------
INSERT INTO dw.dim_time (year, month, quarter, year_month, month_name, month_name_short, is_quarter_end, is_year_end)
SELECT
    EXTRACT(YEAR  FROM d)::SMALLINT                 AS year,
    EXTRACT(MONTH FROM d)::SMALLINT                 AS month,
    EXTRACT(QUARTER FROM d)::SMALLINT               AS quarter,
    TO_CHAR(d, 'YYYY-MM')                           AS year_month,
    TO_CHAR(d, 'Month')                             AS month_name,
    TO_CHAR(d, 'Mon')                               AS month_name_short,
    EXTRACT(MONTH FROM d) IN (3, 6, 9, 12)         AS is_quarter_end,
    EXTRACT(MONTH FROM d) = 12                      AS is_year_end
FROM generate_series(
    '2007-01-01'::DATE,
    '2019-12-01'::DATE,
    INTERVAL '1 month'
) AS d;

DO $$
DECLARE n INT;
BEGIN
    SELECT COUNT(*) INTO n FROM dw.dim_time;
    RAISE NOTICE 'dw.dim_time: % tháng (2007–2019)', n;
END
$$;
