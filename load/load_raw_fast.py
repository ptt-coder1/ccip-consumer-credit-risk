"""
load_raw_fast.py — Nạp dữ liệu siêu tốc bằng COPY command của PostgreSQL
Tốc độ: nhanh gấp 20-50 lần so với pandas to_sql
"""

import os
import sys
import time
import io
import psycopg2
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

LOAD_MAP = [
    # Macro
    ("data/raw/macro/worldbank_macro.csv",            "raw.macro_worldbank"),
    ("data/raw/macro/fred_macro.csv",                 "raw.macro_fred"),
    # Home Credit
    ("data/raw/home_credit/application_train.csv",    "raw.hc_application_train"),
    ("data/raw/home_credit/application_test.csv",     "raw.hc_application_test"),
    ("data/raw/home_credit/bureau.csv",               "raw.hc_bureau"),
    ("data/raw/home_credit/bureau_balance.csv",       "raw.hc_bureau_balance"),
    ("data/raw/home_credit/previous_application.csv", "raw.hc_previous_application"),
    ("data/raw/home_credit/installments_payments.csv","raw.hc_installments_payments"),
    ("data/raw/home_credit/credit_card_balance.csv",  "raw.hc_credit_card_balance"),
    ("data/raw/home_credit/POS_CASH_balance.csv",     "raw.hc_pos_cash_balance"),
]

def get_pg_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "ccip_dw"),
        user=os.getenv("POSTGRES_USER", "openpg"),
        password=os.getenv("POSTGRES_PASSWORD", "openpgpwd"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

def load_table_fast(conn, csv_rel_path: str, table_full: str):
    csv_path = ROOT_DIR / csv_rel_path
    if not csv_path.exists():
        print(f"  ⏭️   {table_full} — Không tìm thấy file: {csv_path.name}")
        return 0

    file_mb = csv_path.stat().st_size / 1_048_576
    schema, table_name = table_full.split(".", 1)
    print(f"\n  ⬇️   Đang nạp {csv_path.name} ({file_mb:.1f} MB) → {table_full}...")
    start = time.time()

    # Đọc header và mẫu dữ liệu để tạo schema bảng
    sample_df = pd.read_csv(csv_path, nrows=500, low_memory=False)
    sample_df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in sample_df.columns]
    
    col_defs = []
    for col, dtype in zip(sample_df.columns, sample_df.dtypes):
        if "int" in str(dtype):
            pg_type = "BIGINT"
        elif "float" in str(dtype):
            pg_type = "DOUBLE PRECISION"
        else:
            pg_type = "TEXT"
        col_defs.append(f'"{col}" {pg_type}')

    create_table_sql = f'DROP TABLE IF EXISTS {schema}.{table_name}; CREATE TABLE {schema}.{table_name} ({", ".join(col_defs)});'

    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.commit()

    # Dùng COPY streaming chunk để nạp dữ liệu cực nhanh
    total_rows = 0
    CHUNK_SIZE = 250_000
    for chunk in pd.read_csv(csv_path, chunksize=CHUNK_SIZE, low_memory=False):
        chunk.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in chunk.columns]
        
        # Buffer in memory
        buffer = io.StringIO()
        chunk.to_csv(buffer, index=False, header=False, sep="\t", na_rep="\\N")
        buffer.seek(0)
        
        cols_str = ", ".join([f'"{c}"' for c in chunk.columns])
        cur.copy_expert(f"COPY {schema}.{table_name} ({cols_str}) FROM STDIN WITH (FORMAT csv, DELIMITER '\t', NULL '\\N')", buffer)
        total_rows += len(chunk)
        print(f"       ... đã nạp {total_rows:,} dòng", end="\r")

    conn.commit()
    cur.close()

    elapsed = time.time() - start
    print(f"       ✅  Hoàn thành: {total_rows:,} dòng trong {elapsed:.1f}s")
    return total_rows

def main():
    print("=" * 60)
    print("  CCIP — Fast Load: CSV ➔ schema raw (PostgreSQL COPY)")
    print("=" * 60)

    conn = get_pg_connection()
    summary = []
    total_start = time.time()

    for csv_rel_path, table_full in LOAD_MAP:
        rows = load_table_fast(conn, csv_rel_path, table_full)
        summary.append((table_full, rows))

    conn.close()
    total_elapsed = time.time() - total_start

    print("\n" + "=" * 60)
    print("  TỔNG KẾT NẠP DỮ LIỆU THÔ VÀO SCHEMA RAW:")
    print("=" * 60)
    for tbl, rows in summary:
        print(f"  ✅  {tbl:<35} : {rows:>12,} dòng")
    print("-" * 60)
    print(f"  🎉 Tổng cộng: {sum(r for _, r in summary):,} dòng ({total_elapsed:.1f}s)")
    print("=" * 60)

if __name__ == "__main__":
    main()
