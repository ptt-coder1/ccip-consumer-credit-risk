-- =========================================================
-- stg_macro.sql — [T] Transform
-- raw.macro_worldbank + raw.macro_fred
--  → staging.stg_macro
--
-- Mục tiêu: gộp dữ liệu vĩ mô từ 2 nguồn thành 1 bảng
-- sạch, sẵn sàng cho fact_economy.
-- =========================================================

DROP TABLE IF EXISTS staging.stg_macro;

CREATE TABLE staging.stg_macro AS

-- World Bank: dữ liệu theo năm + quốc gia
SELECT
    'worldbank'                 AS source,
    country_code,
    country_name,
    year::INT                   AS year,
    NULL::INT                   AS month,
    gdp_growth_pct::NUMERIC     AS gdp_growth_pct,
    inflation_cpi_pct::NUMERIC  AS inflation_cpi_pct,
    NULL::NUMERIC               AS unemployment_rate_pct,
    domestic_credit_gdp_pct::NUMERIC AS domestic_credit_gdp_pct,
    NULL::NUMERIC               AS gni_per_capita_usd,
    -- FRED fields (không có ở World Bank)
    NULL::NUMERIC               AS fed_funds_rate,
    NULL::NUMERIC               AS m2_money_supply_bn,
    NULL::NUMERIC               AS cpi_us,
    NULL::NUMERIC               AS unemployment_us_pct,
    CURRENT_TIMESTAMP           AS _loaded_at

FROM raw.macro_worldbank
WHERE country_code IS NOT NULL

UNION ALL

-- FRED: dữ liệu Mỹ theo tháng
SELECT
    'fred'                      AS source,
    'US'                        AS country_code,
    'United States'             AS country_name,
    EXTRACT(YEAR  FROM date::DATE)::INT AS year,
    EXTRACT(MONTH FROM date::DATE)::INT AS month,
    -- World Bank fields (không có ở FRED)
    NULL::NUMERIC               AS gdp_growth_pct,
    cpi_us::NUMERIC             AS inflation_cpi_pct,  -- dùng CPI Mỹ làm proxy
    unemployment_us_pct::NUMERIC AS unemployment_rate_pct,
    NULL::NUMERIC               AS domestic_credit_gdp_pct,
    NULL::NUMERIC               AS gni_per_capita_usd,
    fed_funds_rate::NUMERIC,
    m2_money_supply_bn::NUMERIC,
    cpi_us::NUMERIC,
    unemployment_us_pct::NUMERIC,
    CURRENT_TIMESTAMP           AS _loaded_at

FROM raw.macro_fred
WHERE date IS NOT NULL;

-- Indexes cho JOIN theo năm / quốc gia
CREATE INDEX idx_stg_macro_year    ON staging.stg_macro (year);
CREATE INDEX idx_stg_macro_country ON staging.stg_macro (country_code, year);

DO $$
DECLARE n INT;
BEGIN
    SELECT COUNT(*) INTO n FROM staging.stg_macro;
    RAISE NOTICE 'staging.stg_macro: % dòng', n;
END
$$;
