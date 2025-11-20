import psycopg2
try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='Kenogoi', host='localhost', port=5432)
    conn.close()
    print('OK')
except Exception as e:
    print('ERROR', type(e).__name__, str(e))
