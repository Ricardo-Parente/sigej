# db/conexao.py
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

DBNAME = os.getenv("PGDATABASE", "sigej")
DBUSER = os.getenv("PGUSER", "Ricardo")
DBPASS = os.getenv("PGPASSWORD", "789423")
DBHOST = os.getenv("PGHOST", "localhost")
DBPORT = os.getenv("PGPORT", "5432")

def get_conn():
    return psycopg2.connect(
        dbname=DBNAME,
        user=DBUSER,
        password=DBPASS,
        host=DBHOST,
        port=DBPORT
    )

def get_dict_cursor(conn=None):
    """Helper: returns a connection and RealDictCursor"""
    close_conn = False
    if conn is None:
        conn = get_conn()
        close_conn = True
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur, close_conn
