import psycopg2
import os

url = os.getenv('DATABASE_URL', 'postgres://postgres:Kenogoi@127.0.0.1:5432/postgres')
print('Using DATABASE_URL=', url)
import urllib.parse as up

# parse
res = up.urlparse(url)
user = res.username
pw = res.password
host = res.hostname
port = res.port
db = res.path.lstrip('/')
print('params', user, host, port, db)
try:
    conn = psycopg2.connect(dbname=db, user=user, password=pw, host=host, port=port)
    cur = conn.cursor()
    cur.execute('select version()')
    print('server version:', cur.fetchone())
    conn.close()
    print('CONNECTED_OK')
except Exception as e:
    print('CONNECT_ERROR', type(e).__name__, e)
