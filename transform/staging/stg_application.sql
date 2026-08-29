-- =========================================================
-- stg_application.sql — [T] Transform lần 1
-- raw.hc_application_train → staging.stg_application
--
-- Mục tiêu:
--   1. Loại bỏ / điền giá trị cho missing values
--   2. Xử lý outlier đã biết (DAYS_EMPLOYED = 365243)
--   3. Chuyển đổi DAYS_* → tuổi / số năm thực
--   4. Chuẩn hóa các cột categorical
--   5. Tạo cột phái sinh hữu ích cho phân tích
-- =========================================================

DROP TABLE IF EXISTS staging.stg_application;

CREATE TABLE staging.stg_application AS
SELECT
    -- -------------------------------------------------------
    -- Khóa chính
    -- -------------------------------------------------------
    sk_id_curr                                AS customer_id,

    -- -------------------------------------------------------
    -- Biến mục tiêu (nhãn phân loại)
    -- -------------------------------------------------------
    target                                    AS is_default,   -- 1=vỡ nợ, 0=không

    -- -------------------------------------------------------
    -- Thông tin cơ bản khoản vay
    -- -------------------------------------------------------
    name_contract_type                        AS contract_type,
    amt_credit                                AS loan_amount,
    amt_annuity                               AS annuity_amount,
    amt_goods_price                           AS goods_price,
    -- Tỷ lệ giữa số tiền vay / giá hàng (> 1 → vay nhiều hơn giá hàng)
    CASE
        WHEN amt_goods_price > 0
        THEN ROUND((amt_credit / amt_goods_price)::numeric, 4)
        ELSE NULL
    END                                       AS loan_to_value_ratio,

    -- -------------------------------------------------------
    -- Thông tin nhân khẩu học
    -- -------------------------------------------------------
    -- DAYS_BIRTH là số âm (đếm ngược từ ngày nộp hồ sơ)
    ABS(days_birth) / 365                     AS age_years,
    CASE
        WHEN ABS(days_birth) / 365 < 25 THEN '< 25'
        WHEN ABS(days_birth) / 365 < 35 THEN '25–34'
        WHEN ABS(days_birth) / 365 < 45 THEN '35–44'
        WHEN ABS(days_birth) / 365 < 55 THEN '45–54'
        ELSE '55+'
    END                                       AS age_group,

    code_gender                               AS gender,
    cnt_children                              AS num_children,
    cnt_fam_members                           AS family_size,
    name_family_status                        AS family_status,

    -- -------------------------------------------------------
    -- Thông tin kinh tế / tài chính cá nhân
    -- -------------------------------------------------------
    name_income_type                          AS income_type,
    amt_income_total                          AS annual_income,
    -- Thu nhập / số lần trả góp hàng năm → xem khách hàng có đủ khả năng không
    CASE
        WHEN amt_annuity > 0
        THEN ROUND((amt_income_total / amt_annuity)::numeric, 4)
        ELSE NULL
    END                                       AS income_to_annuity_ratio,

    -- -------------------------------------------------------
    -- Thông tin nghề nghiệp / việc làm
    -- -------------------------------------------------------
    name_education_type                       AS education_level,
    occupation_type                           AS occupation,

    -- DAYS_EMPLOYED = 365243 là mã lỗi đặc biệt (không làm việc / hưu trí)
    CASE
        WHEN days_employed = 365243 THEN NULL
        ELSE ABS(days_employed) / 365
    END                                       AS years_employed,

    -- Cờ: có kinh nghiệm làm việc hợp lệ không
    CASE
        WHEN days_employed = 365243 THEN 0
        WHEN days_employed IS NULL   THEN 0
        ELSE 1
    END                                       AS has_employment,

    -- -------------------------------------------------------
    -- Thông tin tài sản
    -- -------------------------------------------------------
    flag_own_car                              AS owns_car,       -- Y/N
    flag_own_realty                           AS owns_realty,    -- Y/N
    name_housing_type                         AS housing_type,

    -- -------------------------------------------------------
    -- Thông tin khu vực / địa lý
    -- -------------------------------------------------------
    region_population_relative                AS region_population_rel,
    region_rating_client                      AS region_rating,
    region_rating_client_w_city               AS region_rating_w_city,
    organization_type                         AS org_type,

    -- -------------------------------------------------------
    -- Chỉ số tài liệu / liên lạc
    -- -------------------------------------------------------
    flag_mobil                                AS has_mobile,
    flag_email                                AS has_email,
    flag_phone                                AS has_phone,
    -- Số loại tài liệu đã cung cấp (tổng 20 cột FLAG_DOCUMENT_*)
    (
        COALESCE(flag_document_2,  0) + COALESCE(flag_document_3,  0) +
        COALESCE(flag_document_4,  0) + COALESCE(flag_document_5,  0) +
        COALESCE(flag_document_6,  0) + COALESCE(flag_document_7,  0) +
        COALESCE(flag_document_8,  0) + COALESCE(flag_document_9,  0) +
        COALESCE(flag_document_10, 0) + COALESCE(flag_document_11, 0) +
        COALESCE(flag_document_12, 0) + COALESCE(flag_document_13, 0) +
        COALESCE(flag_document_14, 0) + COALESCE(flag_document_15, 0) +
        COALESCE(flag_document_16, 0) + COALESCE(flag_document_17, 0) +
        COALESCE(flag_document_18, 0) + COALESCE(flag_document_19, 0) +
        COALESCE(flag_document_20, 0) + COALESCE(flag_document_21, 0)
    )                                         AS num_documents_provided,

    -- -------------------------------------------------------
    -- Điểm đánh giá rủi ro từ bên ngoài (External Source)
    -- EXT_SOURCE_1/2/3: điểm tín dụng từ bureau bên ngoài, 0–1
    -- -------------------------------------------------------
    ext_source_1                              AS ext_score_1,
    ext_source_2                              AS ext_score_2,
    ext_source_3                              AS ext_score_3,
    -- Trung bình 3 điểm (dùng COALESCE để bỏ qua NULL khi tính)
    ROUND(
        ((COALESCE(ext_source_1, 0) + COALESCE(ext_source_2, 0) + COALESCE(ext_source_3, 0))
        / NULLIF(
            (CASE WHEN ext_source_1 IS NOT NULL THEN 1 ELSE 0 END +
             CASE WHEN ext_source_2 IS NOT NULL THEN 1 ELSE 0 END +
             CASE WHEN ext_source_3 IS NOT NULL THEN 1 ELSE 0 END),
            0
        ))::numeric, 4)                       AS ext_score_avg,

    -- -------------------------------------------------------
    -- Siêu dữ liệu (dùng để truy vết nếu cần)
    -- -------------------------------------------------------
    weekday_appr_process_start                AS apply_weekday,
    hour_appr_process_start                   AS apply_hour,
    CURRENT_TIMESTAMP                         AS _loaded_at

FROM raw.hc_application_train
-- Lọc bỏ dòng không có customer_id (dữ liệu lỗi căn bản)
WHERE sk_id_curr IS NOT NULL;

-- -----------------------------------------------------------
-- Tạo index để JOIN nhanh hơn ở bước dw
-- -----------------------------------------------------------
CREATE INDEX idx_stg_app_customer ON staging.stg_application (customer_id);

-- -----------------------------------------------------------
-- Kiểm tra nhanh kết quả
-- -----------------------------------------------------------
DO $$
DECLARE
    total_rows INT;
    default_rate NUMERIC;
BEGIN
    SELECT COUNT(*), ROUND(AVG(is_default)::numeric * 100, 2)
    INTO total_rows, default_rate
    FROM staging.stg_application;

    RAISE NOTICE '-------------------------------------------';
    RAISE NOTICE 'staging.stg_application đã tạo xong';
    RAISE NOTICE '  Tổng dòng      : %', total_rows;
    RAISE NOTICE '  Tỷ lệ vỡ nợ   : %s%%', default_rate;
    RAISE NOTICE '-------------------------------------------';
END
$$;
