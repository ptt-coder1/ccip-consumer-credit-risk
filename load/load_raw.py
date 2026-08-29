"""
load_raw.py — Giai đoạn 1 [L] Load
Nạp toàn bộ file CSV từ data/raw/ vào schema `raw` trong PostgreSQL.

Nguyên tắc quan trọng:
  - KHÔNG sửa gì dữ liệu ở bước này — giữ nguyên 100% như nguồn gốc.
  - Nếu bảng đã tồn tại: thay thế hoàn toàn (replace) để idempotent
    (chạy lại script nhiều lần cũng cho kết quả như nhau).
  - Ghi log số dòng để kiểm tra sau.

Cách chạy:
  python load/load_raw.py
"""

import os
import sys
import time
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# -----------------------------------------------------------
# Cấu hình kết nối
# -----------------------------------------------------------
DB_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}"
    f":{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}"
    f":{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB', 'ccip_dw')}"
)

# -----------------------------------------------------------
# Danh sách file cần nạp: (đường dẫn CSV, tên bảng trong raw)
# -----------------------------------------------------------
LOAD_MAP = [
    # Home Credit
    ("data/raw/home_credit/application_train.csv",    "raw.hc_application_train"),
    ("data/raw/home_credit/application_test.csv",     "raw.hc_application_test"),
    ("data/raw/home_credit/bureau.csv",               "raw.hc_bureau"),
    ("data/raw/home_credit/bureau_balance.csv",       "raw.hc_bureau_balance"),
    ("data/raw/home_credit/previous_application.csv", "raw.hc_previous_application"),
    ("data/raw/home_credit/installments_payments.csv","raw.hc_installments_payments"),
    ("data/raw/home_credit/credit_card_balance.csv",  "raw.hc_credit_card_balance"),
    ("data/raw/home_credit/POS_CASH_balance.csv",     "raw.hc_pos_cash_balance"),
    # Macro
    ("data/raw/macro/worldbank_macro.csv",            "raw.macro_worldbank"),
    ("data/raw/macro/fred_macro.csv",                 "raw.macro_fred"),
]

# Số dòng tối đa đọc trong mỗi lần (chunking để tránh OutOfMemory với file lớn)
CHUNK_SIZE = 100_000


def load_csv_to_raw(engine: sa.Engine, csv_rel_path: str, table_full: str):
    """
    Nạp một file CSV vào bảng PostgreSQL theo từng chunk.

    csv_rel_path : đường dẫn tương đối từ thư mục gốc dự án
    table_full   : 'schema.table_name' (ví dụ 'raw.hc_application_train')
    """
    csv_path = ROOT_DIR / csv_rel_path
    schema, table_name = table_full.split(".", 1)

    if not csv_path.exists():
        print(f"  ⏭️   {table_full} — file không tồn tại, bỏ qua: {csv_path.name}")
        return 0

    file_mb = csv_path.stat().st_size / 1_048_576
    print(f"\n  ⬇️   Nạp {csv_path.name} ({file_mb:.1f} MB) → {table_full}")
    start = time.time()

    total_rows = 0
    is_first_chunk = True

    for chunk in pd.read_csv(csv_path, chunksize=CHUNK_SIZE, low_memory=False):
        # Chuẩn hóa tên cột: lowercase, thay khoảng trắng bằng gạch dưới
        chunk.columns = [c.strip().lower().replace(" ", "_") for c in chunk.columns]

        chunk.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists="replace" if is_first_chunk else "append",
            index=False,
            # method='multi' giúp insert nhiều dòng cùng lúc — nhanh hơn
            method="multi",
        )
        total_rows += len(chunk)
        is_first_chunk = False

    elapsed = time.time() - start
    print(f"       ✅  {total_rows:,} dòng — {elapsed:.1f}s")
    return total_rows


def main():
    print(f"\n{'='*55}")
    print("  CCIP — Load: CSV → schema raw (PostgreSQL)")
    print(f"{'='*55}")

    try:
        engine = sa.create_engine(DB_URL, echo=False)
        with engine.connect() as conn:
            conn.execute(sa.text("SELECT 1"))
        print("  ✅  Kết nối PostgreSQL OK\n")
    except Exception as e:
        print(f"  ❌  Không kết nối được PostgreSQL: {e}")
        print("      → Chạy: docker compose up -d  rồi thử lại")
        sys.exit(1)

    summary = []
    for csv_path, table in LOAD_MAP:
        rows = load_csv_to_raw(engine, csv_path, table)
        summary.append((table, rows))

    # In tổng kết
    print(f"\n{'='*55}")
    print("  Tổng kết Load:")
    print(f"{'='*55}")
    for table, rows in summary:
        status = "✅" if rows > 0 else "⏭️ "
        print(f"  {status}  {table:<45} {rows:>10,} dòng")

    total = sum(r for _, r in summary)
    print(f"\n  Tổng cộng: {total:,} dòng đã nạp vào schema raw")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
