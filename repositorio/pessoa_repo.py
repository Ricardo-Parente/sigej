from db.conexao import get_conn, get_dict_cursor

def criar_pessoa(nome, cpf=None, email=None, telefone=None):
    conn = get_conn()
    cur = conn.cursor()

    # Se CPF já existe, retorna o ID existente
    if cpf:
        cur.execute("SELECT id FROM pessoa WHERE cpf=%s", (cpf,))
        row = cur.fetchone()
        if row:
            cur.close()
            conn.close()
            return row[0]

    cur.execute("""
        INSERT INTO pessoa (nome, cpf, email, telefone)
        VALUES (%s,%s,%s,%s) RETURNING id
    """, (nome, cpf, email, telefone))
    pessoa_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()
    return pessoa_id


def listar_pessoas(limit=100):
    conn, cur, _ = get_dict_cursor(None)
    cur.execute("SELECT id, nome, cpf, email, telefone, ativo FROM pessoa ORDER BY id LIMIT %s", (limit,))
    res = cur.fetchall(); cur.close(); conn.close(); return res
