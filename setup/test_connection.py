"""
test_connection.py — Giai đoạn 0
Kiểm tra kết nối PostgreSQL và xác nhận 3 schemas đã được tạo đúng.

Cách chạy:
    python setup/test_connection.py
"""

import sys
from pathlib import Path

# Thêm thư mục gốc dự án vào sys.path để import được .env
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
import os
import sqlalchemy as sa

# -----------------------------------------------------------
# 1. Đọc biến môi trường từ file .env
# -----------------------------------------------------------
load_dotenv(ROOT_DIR / ".env")

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "ccip_dw")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

if not DB_USER or not DB_PASS:
    print("❌  Lỗi: Chưa có POSTGRES_USER hoặc POSTGRES_PASSWORD trong .env")
    print("   → Hãy copy .env.example thành .env và điền thông tin.")
    sys.exit(1)

# -----------------------------------------------------------
# 2. Tạo connection string và engine
# -----------------------------------------------------------
connection_url = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print(f"\n{'='*55}")
print("  CCIP — Kiểm tra kết nối PostgreSQL")
print(f"{'='*55}")
print(f"  Host    : {DB_HOST}:{DB_PORT}")
print(f"  Database: {DB_NAME}")
print(f"  User    : {DB_USER}")
print(f"{'='*55}\n")

try:
    engine = sa.create_engine(connection_url, echo=False)

    with engine.connect() as conn:
        # ---------------------------------------------------
        # 3. Kiểm tra cơ bản
        # ---------------------------------------------------
        version = conn.execute(sa.text("SELECT version();")).scalar()
        print(f"✅  Kết nối thành công!")
        print(f"    PostgreSQL version: {version.split(',')[0]}\n")

        # ---------------------------------------------------
        # 4. Kiểm tra 3 schemas bắt buộc
        # ---------------------------------------------------
        required_schemas = ["raw", "staging", "dw"]
        result = conn.execute(sa.text(
            "SELECT schema_name FROM information_schema.schemata "
            "WHERE schema_name = ANY(:schemas) ORDER BY schema_name;"
        ), {"schemas": required_schemas})
        found_schemas = [row[0] for row in result]

        print("  Kiểm tra schemas:")
        all_ok = True
        for schema in required_schemas:
            if schema in found_schemas:
                print(f"    ✅  Schema '{schema}' — tồn tại")
            else:
                print(f"    ❌  Schema '{schema}' — CHƯA TẠO")
                print(f"        → Thử khởi động lại container: docker compose down -v && docker compose up -d")
                all_ok = False

        print()
        if all_ok:
            print("✅  Tất cả schemas đều sẵn sàng. Giai đoạn 0 HOÀN THÀNH!\n")
        else:
            print("⚠️   Một số schemas chưa tồn tại. Xem gợi ý khắc phục ở trên.\n")
            sys.exit(1)

except sa.exc.OperationalError as e:
    print(f"❌  Không kết nối được PostgreSQL!\n")
    print(f"    Chi tiết lỗi: {e}\n")
    print("  Các nguyên nhân thường gặp:")
    print("    1. Container chưa chạy → thử: docker compose up -d")
    print("    2. Sai password trong .env")
    print("    3. Port 5432 bị chiếm bởi PostgreSQL khác trên máy")
    sys.exit(1)
