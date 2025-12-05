from db.conexao import get_conn, get_dict_cursor

def criar_tipo(descricao):
    conn, cur = get_conn(), get_conn().cursor()
    cur.execute("INSERT INTO tipo_funcionario (descricao) VALUES (%s) RETURNING id", (descricao,))
    tid = cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return tid

def listar_tipos():
    conn, cur, _ = get_dict_cursor(None)
    cur.execute("SELECT id, descricao FROM tipo_funcionario ORDER BY id"); res = cur.fetchall(); cur.close(); conn.close(); return res
