import os
import sys
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

print("=" * 60)
print(f"  {'SCHEMA / BẢNG':<35} | {'SỐ DÒNG':<15}")
print("=" * 60)

for schema in ["raw", "staging", "dw"]:
    print(f"\n📁 [{schema.upper()}]")
    cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' ORDER BY table_name")
    tables = cur.fetchall()
    for (t,) in tables:
        cur.execute(f'SELECT count(*) FROM {schema}."{t}"')
        cnt = cur.fetchone()[0]
        print(f"  • {schema}.{t:<30} : {cnt:>12,} dòng")

print("\n" + "=" * 60)
cur.close()
conn.close()
