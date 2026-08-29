-- =========================================================
-- init.sql — Chạy TỰ ĐỘNG khi PostgreSQL container khởi động
-- lần đầu (nhờ volume mount trong docker-compose.yml)
-- =========================================================

-- =========================================================
-- 1. Tạo user riêng cho dự án
--    (POSTGRES_USER trong .env đã tạo user+database rồi,
--     nhưng nếu muốn user tách biệt với superuser thì thêm vào đây)
-- =========================================================

-- Ghi chú: biến ${POSTGRES_USER} ở docker-compose tự tạo user=ccip_user
-- với database=ccip_dw. Script này chạy với quyền user đó nên không cần
-- CREATE USER nữa — chỉ cần tạo schemas bên dưới.

-- =========================================================
-- 2. Tạo 3 schemas chính của pipeline ELT
-- =========================================================

-- raw: lưu dữ liệu GỐC y nguyên từ nguồn, KHÔNG sửa gì
CREATE SCHEMA IF NOT EXISTS raw;

-- staging: dữ liệu đã làm sạch (xử lý missing, outlier, chuẩn hóa kiểu)
CREATE SCHEMA IF NOT EXISTS staging;

-- dw (data warehouse): star schema — fact + dimension tables
CREATE SCHEMA IF NOT EXISTS dw;

-- =========================================================
-- 3. Gán quyền trên từng schema cho user hiện tại
-- =========================================================
GRANT ALL PRIVILEGES ON SCHEMA raw     TO CURRENT_USER;
GRANT ALL PRIVILEGES ON SCHEMA staging TO CURRENT_USER;
GRANT ALL PRIVILEGES ON SCHEMA dw      TO CURRENT_USER;

-- Đảm bảo các bảng tạo sau này cũng được quyền truy cập đầy đủ
ALTER DEFAULT PRIVILEGES IN SCHEMA raw     GRANT ALL ON TABLES TO CURRENT_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT ALL ON TABLES TO CURRENT_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA dw      GRANT ALL ON TABLES TO CURRENT_USER;

-- =========================================================
-- 4. Log xác nhận (xuất hiện trong docker logs ccip_postgres)
-- =========================================================
DO $$
BEGIN
  RAISE NOTICE '==============================================';
  RAISE NOTICE 'CCIP — Database initialized successfully';
  RAISE NOTICE 'Schemas created: raw, staging, dw';
  RAISE NOTICE '==============================================';
END
$$;
