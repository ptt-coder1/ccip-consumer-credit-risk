import os
import sys
import time
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "ccip_dw"),
    user=os.getenv("POSTGRES_USER", "openpg"),
    password=os.getenv("POSTGRES_PASSWORD", "openpgpwd"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432")
)
cur = conn.cursor()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'raw'")
tables = cur.fetchall()

print(f"{'Bảng trong raw':<35} | {'Số dòng':<15}")
print("-" * 55)
total = 0
for (t,) in tables:
    cur.execute(f"SELECT count(*) FROM raw.{t}")
    cnt = cur.fetchone()[0]
    total += cnt
    print(f"{t:<35} | {cnt:>12,}")

print("-" * 55)
print(f"{'TỔNG CỘNG':<35} | {total:>12,}")

cur.close()
conn.close()
