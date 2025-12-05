from db.conexao import get_conn, get_dict_cursor
def criar_setor(nome, sigla=None):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO setor (nome, sigla) VALUES (%s,%s) RETURNING id", (nome, sigla))
    sid = cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return sid
def listar_setores():
    conn, cur, _ = get_dict_cursor(None); cur.execute("SELECT id,nome,sigla FROM setor ORDER BY nome"); res=cur.fetchall(); cur.close(); conn.close(); return res
