-- =========================================================
-- fact_economy.sql — Star Schema: Fact chỉ số kinh tế vĩ mô
-- staging.stg_macro → dw.fact_economy
--
-- Grain: 1 dòng = 1 quốc gia × 1 tháng
-- (hoặc 1 quốc gia × 1 năm với World Bank — month = NULL)
-- =========================================================

DROP TABLE IF EXISTS dw.fact_economy CASCADE;

CREATE TABLE dw.fact_economy (
    economy_sk              BIGSERIAL       PRIMARY KEY,

    -- Foreign key → dim_time
    date_id                 INTEGER         NOT NULL
        REFERENCES dw.dim_time(date_id),

    -- Thông tin địa lý
    country_code            CHAR(2),
    country_name            VARCHAR(100),
    source                  VARCHAR(20),    -- 'worldbank' / 'fred'

    -- Measures: Kinh tế vĩ mô
    gdp_growth_pct          NUMERIC(8,4),
    inflation_cpi_pct       NUMERIC(8,4),
    unemployment_rate_pct   NUMERIC(8,4),
    domestic_credit_gdp_pct NUMERIC(8,4),
    gni_per_capita_usd      NUMERIC(12,2),
    fed_funds_rate          NUMERIC(8,4),
    m2_money_supply_bn      NUMERIC(15,2),
    cpi_us                  NUMERIC(10,4),
    unemployment_us_pct     NUMERIC(8,4),

    _created_at             TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dw.fact_economy (
    date_id, country_code, country_name, source,
    gdp_growth_pct, inflation_cpi_pct, unemployment_rate_pct,
    domestic_credit_gdp_pct, gni_per_capita_usd,
    fed_funds_rate, m2_money_supply_bn, cpi_us, unemployment_us_pct
)
SELECT
    dt.date_id,
    m.country_code,
    m.country_name,
    m.source,
    m.gdp_growth_pct,
    m.inflation_cpi_pct,
    m.unemployment_rate_pct,
    m.domestic_credit_gdp_pct,
    m.gni_per_capita_usd,
    m.fed_funds_rate,
    m.m2_money_supply_bn,
    m.cpi_us,
    m.unemployment_us_pct
FROM staging.stg_macro m
JOIN dw.dim_time dt ON (
    dt.year  = m.year
    AND dt.month = COALESCE(m.month, 1)  -- World Bank year-only → dùng tháng 1
);

CREATE INDEX idx_fact_economy_date    ON dw.fact_economy (date_id);
CREATE INDEX idx_fact_economy_country ON dw.fact_economy (country_code);

DO $$
DECLARE n INT;
BEGIN
    SELECT COUNT(*) INTO n FROM dw.fact_economy;
    RAISE NOTICE 'dw.fact_economy: % dòng', n;
END
$$;
