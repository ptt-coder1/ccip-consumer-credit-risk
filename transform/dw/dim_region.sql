-- =========================================================
-- dim_region.sql — Star Schema: Dimension khu vực
--
-- Grain: 1 dòng = 1 khu vực (region_rating duy nhất từ dữ liệu)
-- Lưu ý: Home Credit không tiết lộ tên tỉnh/thành phố cụ thể
-- vì lý do riêng tư — chỉ có mã rating khu vực (1/2/3).
-- =========================================================

DROP TABLE IF EXISTS dw.dim_region CASCADE;

CREATE TABLE dw.dim_region (
    region_sk           SERIAL      PRIMARY KEY,
    region_rating       SMALLINT    NOT NULL UNIQUE,  -- 1/2/3
    region_label        VARCHAR(20) NOT NULL,         -- 'Thấp'/'Trung bình'/'Cao'
    risk_level          VARCHAR(20) NOT NULL,         -- 'Thấp'/'Trung bình'/'Cao'
    description         TEXT
);

INSERT INTO dw.dim_region (region_rating, region_label, risk_level, description) VALUES
(1, 'Loại 1', 'Thấp',
 'Khu vực có rating tín dụng cao nhất — tỷ lệ vỡ nợ thường thấp'),
(2, 'Loại 2', 'Trung bình',
 'Khu vực rating trung bình'),
(3, 'Loại 3', 'Cao',
 'Khu vực có rating thấp nhất — tỷ lệ vỡ nợ thường cao hơn');

DO $$
BEGIN
    RAISE NOTICE 'dw.dim_region: 3 khu vực (rating 1/2/3)';
END
$$;
