-- =========================================================
-- fact_loan.sql — Star Schema: Fact Table chính
-- staging.stg_application → dw.fact_loan
--
-- Grain: 1 dòng = 1 đơn vay (SK_ID_CURR)
-- Measures: số tiền, tỷ lệ, điểm rủi ro, cờ vỡ nợ
-- Foreign keys: → dim_customer, dim_time, dim_region
-- =========================================================

DROP TABLE IF EXISTS dw.fact_loan CASCADE;

CREATE TABLE dw.fact_loan (
    -- ---------------------------------------------------
    -- Surrogate key
    -- ---------------------------------------------------
    loan_sk                 BIGSERIAL       PRIMARY KEY,

    -- ---------------------------------------------------
    -- Foreign keys → Dimensions
    -- ---------------------------------------------------
    customer_sk             INTEGER         NOT NULL
        REFERENCES dw.dim_customer(customer_sk),

    date_id                 INTEGER         NOT NULL
        REFERENCES dw.dim_time(date_id),

    region_sk               INTEGER         NOT NULL
        REFERENCES dw.dim_region(region_sk),

    -- ---------------------------------------------------
    -- Natural key (để truy vết về raw nếu cần)
    -- ---------------------------------------------------
    customer_id             INTEGER         NOT NULL,

    -- ---------------------------------------------------
    -- Measures: Khoản vay
    -- ---------------------------------------------------
    contract_type           VARCHAR(30),
    loan_amount             NUMERIC(15,2),
    annuity_amount          NUMERIC(15,2),
    goods_price             NUMERIC(15,2),
    loan_to_value_ratio     NUMERIC(8,4),
    income_to_annuity_ratio NUMERIC(8,4),

    -- ---------------------------------------------------
    -- Measures: Rủi ro
    -- ---------------------------------------------------
    is_default              SMALLINT        NOT NULL,   -- 1=vỡ nợ, 0=không
    ext_score_avg           NUMERIC(8,6),
    num_documents_provided  SMALLINT,

    -- ---------------------------------------------------
    -- Measures: Thời điểm nộp đơn
    -- ---------------------------------------------------
    apply_weekday           VARCHAR(15),
    apply_hour              SMALLINT,

    -- ---------------------------------------------------
    -- Metadata
    -- ---------------------------------------------------
    _created_at             TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------
-- Nạp dữ liệu
-- ---------------------------------------------------
INSERT INTO dw.fact_loan (
    customer_sk, date_id, region_sk, customer_id,
    contract_type, loan_amount, annuity_amount, goods_price,
    loan_to_value_ratio, income_to_annuity_ratio,
    is_default, ext_score_avg, num_documents_provided,
    apply_weekday, apply_hour
)
SELECT
    dc.customer_sk,
    dt.date_id,
    dr.region_sk,
    a.customer_id,
    a.contract_type,
    a.loan_amount,
    a.annuity_amount,
    a.goods_price,
    a.loan_to_value_ratio,
    a.income_to_annuity_ratio,
    a.is_default,
    a.ext_score_avg,
    a.num_documents_provided,
    a.apply_weekday,
    a.apply_hour

FROM staging.stg_application a

-- JOIN → dim_customer (natural key lookup)
JOIN dw.dim_customer dc ON dc.customer_id = a.customer_id

-- JOIN → dim_time
-- Bộ dữ liệu Home Credit không có ngày vay cụ thể.
-- Chiến lược: dùng DAYS_BIRTH + một mốc tham chiếu giả định (2017-09-01
-- là ngày cuối dataset theo Kaggle) để tính ra năm+tháng ứng vay.
-- Đây là giả định rõ ràng — cần ghi chú trong báo cáo.
JOIN dw.dim_time dt ON (
    dt.year  = EXTRACT(YEAR  FROM (DATE '2017-09-01' + (a.apply_hour || ' hours')::INTERVAL))::SMALLINT
    AND dt.month = EXTRACT(MONTH FROM (DATE '2017-09-01'))::SMALLINT
)

-- JOIN → dim_region
JOIN dw.dim_region dr ON dr.region_rating = a.region_rating;

-- ---------------------------------------------------
-- Indexes hỗ trợ Power BI query
-- ---------------------------------------------------
CREATE INDEX idx_fact_loan_customer  ON dw.fact_loan (customer_sk);
CREATE INDEX idx_fact_loan_time      ON dw.fact_loan (date_id);
CREATE INDEX idx_fact_loan_region    ON dw.fact_loan (region_sk);
CREATE INDEX idx_fact_loan_default   ON dw.fact_loan (is_default);

DO $$
DECLARE
    total_rows    INT;
    default_count INT;
    default_rate  NUMERIC;
BEGIN
    SELECT COUNT(*), SUM(is_default),
           ROUND(AVG(is_default::numeric) * 100, 2)
    INTO total_rows, default_count, default_rate
    FROM dw.fact_loan;

    RAISE NOTICE '=========================================';
    RAISE NOTICE 'dw.fact_loan đã tạo xong!';
    RAISE NOTICE '  Tổng khoản vay  : %', total_rows;
    RAISE NOTICE '  Số vỡ nợ        : %', default_count;
    RAISE NOTICE '  Tỷ lệ vỡ nợ    : %s%%', default_rate;
    RAISE NOTICE '=========================================';
END
$$;
