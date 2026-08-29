-- =========================================================
-- stg_bureau.sql — [T] Transform
-- raw.hc_bureau + raw.hc_bureau_balance
--  → staging.stg_bureau_summary
--
-- Mục tiêu: tổng hợp lịch sử tín dụng bên ngoài của mỗi
-- khách hàng (sk_id_curr) thành 1 dòng/khách hàng —
-- sẵn sàng JOIN vào fact_loan sau này.
-- =========================================================

DROP TABLE IF EXISTS staging.stg_bureau_summary;

CREATE TABLE staging.stg_bureau_summary AS
WITH bureau_agg AS (
    -- Tổng hợp từng dòng bureau (mỗi dòng = 1 khoản tín dụng bên ngoài)
    SELECT
        sk_id_curr                              AS customer_id,

        -- Số lượng khoản tín dụng đã có từ trước
        COUNT(*)                                AS num_external_credits,

        -- Số khoản đang ACTIVE
        COUNT(*) FILTER (WHERE credit_active = 'Active')
                                                AS num_active_credits,

        -- Số khoản đã đóng
        COUNT(*) FILTER (WHERE credit_active = 'Closed')
                                                AS num_closed_credits,

        -- Tổng dư nợ hiện tại (Active)
        SUM(amt_credit_sum) FILTER (WHERE credit_active = 'Active')
                                                AS total_active_credit_amt,

        -- Tổng nợ quá hạn
        SUM(COALESCE(amt_credit_sum_overdue, 0))
                                                AS total_overdue_amt,

        -- Số ngày quá hạn tối đa từng ghi nhận
        MAX(COALESCE(credit_day_overdue, 0))    AS max_overdue_days,

        -- Tỷ lệ số khoản có ghi nhận quá hạn
        ROUND(
            COUNT(*) FILTER (WHERE credit_day_overdue > 0)::numeric
            / NULLIF(COUNT(*), 0) * 100,
        2)                                      AS pct_credits_overdue,

        -- Thời hạn tín dụng trung bình (tháng)
        AVG(cnt_credit_prolong)                 AS avg_credit_prolong,

        -- Loại tín dụng phổ biến nhất
        MODE() WITHIN GROUP (ORDER BY credit_type)
                                                AS most_common_credit_type

    FROM raw.hc_bureau
    GROUP BY sk_id_curr
),
bureau_bal_agg AS (
    -- Tổng hợp bureau_balance: tình trạng trả nợ theo tháng
    -- STATUS: 'C'=đóng, 'X'=không có thông tin, '0'=đúng hạn, '1'–'5'=quá hạn
    SELECT
        b.sk_id_curr                            AS customer_id,
        COUNT(bb.status) FILTER (WHERE bb.status NOT IN ('C','X','0'))
                                                AS num_late_months,
        COUNT(bb.status)                        AS total_months_observed
    FROM raw.hc_bureau b
    JOIN raw.hc_bureau_balance bb
        ON b.sk_id_bureau = bb.sk_id_bureau
    GROUP BY b.sk_id_curr
)
SELECT
    ba.*,
    COALESCE(bbal.num_late_months, 0)           AS num_late_payment_months,
    COALESCE(bbal.total_months_observed, 0)     AS total_months_observed,
    -- Tỷ lệ tháng trả trễ
    CASE
        WHEN COALESCE(bbal.total_months_observed, 0) > 0
        THEN ROUND(
            bbal.num_late_months::numeric / bbal.total_months_observed * 100,
        2)
        ELSE 0
    END                                         AS pct_late_months,

    CURRENT_TIMESTAMP                           AS _loaded_at
FROM bureau_agg ba
LEFT JOIN bureau_bal_agg bbal USING (customer_id);

-- Index cho JOIN
CREATE INDEX idx_stg_bureau_customer ON staging.stg_bureau_summary (customer_id);

DO $$
DECLARE n INT;
BEGIN
    SELECT COUNT(*) INTO n FROM staging.stg_bureau_summary;
    RAISE NOTICE 'staging.stg_bureau_summary: % khách hàng', n;
END
$$;
