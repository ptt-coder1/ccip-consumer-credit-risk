"""
run_pipeline.py — Script điều phối toàn bộ pipeline ELT
Chạy tuần tự: Extract → Load → Transform (staging) → Transform (dw)

Cách chạy:
  python run_pipeline.py [--stage STAGE]

  --stage: (tùy chọn) chỉ chạy từ giai đoạn cụ thể
           Giá trị: extract | load | staging | dw | all (mặc định: all)

Ví dụ:
  python run_pipeline.py              # chạy toàn bộ
  python run_pipeline.py --stage dw   # chỉ chạy bước tạo star schema
"""

import os
import sys
import argparse
import subprocess
import time
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import sqlalchemy as sa
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}"
    f":{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}"
    f":{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB', 'ccip_dw')}"
)


def run_python(script_rel: str, label: str):
    """Chạy một script Python và in kết quả."""
    script = ROOT_DIR / script_rel
    print(f"\n{'─'*55}")
    print(f"  ▶  {label}")
    print(f"     {script_rel}")
    print(f"{'─'*55}")
    start = time.time()

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=False,
        text=True,
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        print(f"\n  ❌  THẤT BẠI sau {elapsed:.1f}s")
        sys.exit(result.returncode)
    print(f"\n  ✅  Hoàn thành ({elapsed:.1f}s)")


def run_sql(sql_rel: str, label: str, engine: sa.Engine):
    """Chạy một file SQL trong PostgreSQL."""
    sql_path = ROOT_DIR / sql_rel
    print(f"\n{'─'*55}")
    print(f"  ▶  {label}")
    print(f"     {sql_rel}")
    print(f"{'─'*55}")
    start = time.time()

    sql_text = sql_path.read_text(encoding="utf-8")
    raw_conn = engine.raw_connection()
    try:
        cur = raw_conn.cursor()
        cur.execute(sql_text)
        raw_conn.commit()
        cur.close()
    finally:
        raw_conn.close()
    elapsed = time.time() - start
    print(f"  ✅  Hoàn thành ({elapsed:.1f}s)")


def main():
    parser = argparse.ArgumentParser(description="CCIP ELT Pipeline runner")
    parser.add_argument(
        "--stage",
        choices=["extract", "load", "staging", "dw", "all"],
        default="all",
        help="Chạy từ giai đoạn cụ thể (mặc định: all)"
    )
    args = parser.parse_args()

    print(f"\n{'='*55}")
    print("  CCIP — ELT Pipeline")
    print(f"  Giai đoạn chạy: {args.stage.upper()}")
    print(f"{'='*55}")

    engine = sa.create_engine(DB_URL, echo=False)

    total_start = time.time()

    # -------------------------------------------------------
    # [E] EXTRACT
    # -------------------------------------------------------
    if args.stage in ("all", "extract"):
        run_python("extract/extract_homecredit.py", "[E] Extract: Home Credit (Kaggle)")
        run_python("extract/extract_macro.py",      "[E] Extract: Macro (World Bank + FRED)")

    # -------------------------------------------------------
    # [L] LOAD → raw
    # -------------------------------------------------------
    if args.stage in ("all", "load"):
        run_python("load/load_raw.py", "[L] Load: CSV → schema raw")

    # -------------------------------------------------------
    # [T1] TRANSFORM → staging
    # -------------------------------------------------------
    if args.stage in ("all", "staging"):
        run_sql("transform/staging/stg_application.sql",   "[T] Transform: stg_application",  engine)
        run_sql("transform/staging/stg_bureau.sql",        "[T] Transform: stg_bureau",        engine)
        run_sql("transform/staging/stg_previous_app.sql",  "[T] Transform: stg_previous_app",  engine)
        run_sql("transform/staging/stg_macro.sql",         "[T] Transform: stg_macro",         engine)

    # -------------------------------------------------------
    # [T2] TRANSFORM → dw (star schema)
    # Thứ tự quan trọng: dimensions trước, fact sau
    # -------------------------------------------------------
    if args.stage in ("all", "dw"):
        run_sql("transform/dw/dim_time.sql",     "[T] DW: dim_time",     engine)
        run_sql("transform/dw/dim_region.sql",   "[T] DW: dim_region",   engine)
        run_sql("transform/dw/dim_customer.sql", "[T] DW: dim_customer", engine)
        run_sql("transform/dw/fact_loan.sql",    "[T] DW: fact_loan",    engine)
        run_sql("transform/dw/fact_economy.sql", "[T] DW: fact_economy", engine)

    total_elapsed = time.time() - total_start
    print(f"\n{'='*55}")
    print(f"  ✅  Pipeline hoàn thành! Tổng thời gian: {total_elapsed:.1f}s")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()
