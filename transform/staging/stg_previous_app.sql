-- =========================================================
-- stg_previous_app.sql — [T] Transform
-- raw.hc_previous_application → staging.stg_prev_app_summary
--
-- Mục tiêu: tổng hợp lịch sử đơn vay CŨ tại Home Credit
-- của mỗi khách hàng thành 1 dòng/khách hàng.
-- =========================================================

DROP TABLE IF EXISTS staging.stg_prev_app_summary;

CREATE TABLE staging.stg_prev_app_summary AS
SELECT
    sk_id_curr                                      AS customer_id,

    -- Tổng số đơn đã nộp trước đây
    COUNT(*)                                        AS num_prev_applications,

    -- Số đơn được duyệt / từ chối / hủy / chưa sử dụng
    COUNT(*) FILTER (WHERE name_contract_status = 'Approved')
                                                    AS num_approved,
    COUNT(*) FILTER (WHERE name_contract_status = 'Refused')
                                                    AS num_refused,
    COUNT(*) FILTER (WHERE name_contract_status = 'Canceled')
                                                    AS num_canceled,
    COUNT(*) FILTER (WHERE name_contract_status = 'Unused offer')
                                                    AS num_unused,

    -- Tỷ lệ duyệt
    ROUND(
        COUNT(*) FILTER (WHERE name_contract_status = 'Approved')::numeric
        / NULLIF(COUNT(*), 0) * 100,
    2)                                              AS approval_rate_pct,

    -- Số tiền vay trung bình ở đơn cũ
    ROUND(AVG(amt_credit)::numeric, 2)              AS avg_prev_credit_amt,

    -- Số tiền vay đơn cũ lớn nhất
    MAX(amt_credit)                                 AS max_prev_credit_amt,

    -- Số ngày trung bình từ lần vay gần nhất đến hiện tại
    -- (DAYS_DECISION là số âm, ABS → số ngày đã qua)
    ROUND(AVG(ABS(days_decision))::numeric, 0)      AS avg_days_since_prev_decision,

    -- Loại hợp đồng phổ biến nhất
    MODE() WITHIN GROUP (ORDER BY name_contract_type)
                                                    AS most_common_contract_type,

    CURRENT_TIMESTAMP                               AS _loaded_at

FROM raw.hc_previous_application
GROUP BY sk_id_curr;

CREATE INDEX idx_stg_prev_customer ON staging.stg_prev_app_summary (customer_id);

DO $$
DECLARE n INT;
BEGIN
    SELECT COUNT(*) INTO n FROM staging.stg_prev_app_summary;
    RAISE NOTICE 'staging.stg_prev_app_summary: % khách hàng', n;
END
$$;
