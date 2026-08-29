import psycopg2, sys
sys.stdout.reconfigure(encoding='utf-8')
conn = psycopg2.connect(dbname='ccip_dw', user='openpg', password='openpgpwd', host='localhost', port='5432')
cur = conn.cursor()
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='dw' AND table_name='fact_loan' ORDER BY ordinal_position")
print('=== fact_loan columns ===')
for r in cur.fetchall():
    print(f'  {r[0]:30} {r[1]}')
print()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='dw' AND table_name='dim_customer' ORDER BY ordinal_position")
print('=== dim_customer columns ===')
for r in cur.fetchall():
    print(f'  {r[0]}')
conn.close()
