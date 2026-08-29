-- =========================================================
-- dim_customer.sql — Star Schema: Dimension khách hàng
-- staging.stg_application → dw.dim_customer
--
-- Grain: 1 dòng = 1 khách hàng (customer_id duy nhất)
-- =========================================================

DROP TABLE IF EXISTS dw.dim_customer CASCADE;

CREATE TABLE dw.dim_customer (
    -- ---------------------------------------------------
    -- Surrogate key (khóa thay thế — do chúng ta tạo)
    -- Dùng SERIAL thay vì customer_id gốc để dw không phụ
    -- thuộc vào hệ thống nguồn
    -- ---------------------------------------------------
    customer_sk         SERIAL          PRIMARY KEY,

    -- Natural key (khóa tự nhiên từ nguồn)
    customer_id         INTEGER         NOT NULL UNIQUE,

    -- ---------------------------------------------------
    -- Nhân khẩu học
    -- ---------------------------------------------------
    age_years           INTEGER,
    age_group           VARCHAR(10),    -- '< 25', '25–34', ...
    gender              VARCHAR(5),     -- 'M', 'F', 'XNA'
    num_children        INTEGER,
    family_size         NUMERIC(5,1),
    family_status       VARCHAR(50),

    -- ---------------------------------------------------
    -- Kinh tế / tài chính cá nhân
    -- ---------------------------------------------------
    income_type         VARCHAR(50),
    annual_income       NUMERIC(15,2),
    education_level     VARCHAR(50),
    occupation          VARCHAR(50),
    years_employed      NUMERIC(6,2),
    has_employment      SMALLINT,       -- 0/1

    -- ---------------------------------------------------
    -- Tài sản
    -- ---------------------------------------------------
    owns_car            VARCHAR(3),     -- 'Y'/'N'
    owns_realty         VARCHAR(3),
    housing_type        VARCHAR(50),

    -- ---------------------------------------------------
    -- Điểm tín dụng bên ngoài
    -- ---------------------------------------------------
    ext_score_1         NUMERIC(8,6),
    ext_score_2         NUMERIC(8,6),
    ext_score_3         NUMERIC(8,6),
    ext_score_avg       NUMERIC(8,6),

    -- ---------------------------------------------------
    -- Lịch sử tín dụng bên ngoài (từ stg_bureau_summary)
    -- ---------------------------------------------------
    num_external_credits        INTEGER,
    num_active_credits          INTEGER,
    num_closed_credits          INTEGER,
    total_active_credit_amt     NUMERIC(15,2),
    total_overdue_amt           NUMERIC(15,2),
    max_overdue_days            INTEGER,
    pct_credits_overdue         NUMERIC(6,2),
    num_late_payment_months     INTEGER,
    pct_late_months             NUMERIC(6,2),

    -- ---------------------------------------------------
    -- Lịch sử đơn vay cũ tại Home Credit (từ stg_prev_app_summary)
    -- ---------------------------------------------------
    num_prev_applications       INTEGER,
    num_approved                INTEGER,
    num_refused                 INTEGER,
    approval_rate_pct           NUMERIC(6,2),
    avg_prev_credit_amt         NUMERIC(15,2),
    avg_days_since_prev_decision NUMERIC(8,0),

    -- ---------------------------------------------------
    -- Metadata
    -- ---------------------------------------------------
    _created_at         TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------
-- Nạp dữ liệu từ staging (JOIN 3 bảng staging lại)
-- ---------------------------------------------------
INSERT INTO dw.dim_customer (
    customer_id, age_years, age_group, gender, num_children, family_size,
    family_status, income_type, annual_income, education_level, occupation,
    years_employed, has_employment, owns_car, owns_realty, housing_type,
    ext_score_1, ext_score_2, ext_score_3, ext_score_avg,
    num_external_credits, num_active_credits, num_closed_credits,
    total_active_credit_amt, total_overdue_amt, max_overdue_days,
    pct_credits_overdue, num_late_payment_months, pct_late_months,
    num_prev_applications, num_approved, num_refused, approval_rate_pct,
    avg_prev_credit_amt, avg_days_since_prev_decision
)
SELECT
    a.customer_id,
    a.age_years, a.age_group, a.gender, a.num_children, a.family_size,
    a.family_status, a.income_type, a.annual_income, a.education_level,
    a.occupation, a.years_employed, a.has_employment,
    a.owns_car, a.owns_realty, a.housing_type,
    a.ext_score_1, a.ext_score_2, a.ext_score_3, a.ext_score_avg,
    -- Bureau (LEFT JOIN vì không phải khách hàng nào cũng có lịch sử)
    b.num_external_credits, b.num_active_credits, b.num_closed_credits,
    b.total_active_credit_amt, b.total_overdue_amt, b.max_overdue_days,
    b.pct_credits_overdue, b.num_late_payment_months, b.pct_late_months,
    -- Previous application
    p.num_prev_applications, p.num_approved, p.num_refused,
    p.approval_rate_pct, p.avg_prev_credit_amt, p.avg_days_since_prev_decision
FROM staging.stg_application a
LEFT JOIN staging.stg_bureau_summary  b USING (customer_id)
LEFT JOIN staging.stg_prev_app_summary p USING (customer_id);

-- Index hỗ trợ JOIN từ fact_loan
CREATE INDEX idx_dim_customer_id ON dw.dim_customer (customer_id);

DO $$
DECLARE n INT;
BEGIN
    SELECT COUNT(*) INTO n FROM dw.dim_customer;
    RAISE NOTICE 'dw.dim_customer: % khách hàng', n;
END
$$;
