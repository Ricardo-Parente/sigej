# repositorio/pessoa_repo.py
from db.conexao import get_conn, get_dict_cursor

def criar_pessoa(nome, cpf=None, matricula_siape=None, email=None, telefone=None):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
    INSERT INTO pessoa (nome, cpf, matricula_siape, email, telefone)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    cur.execute(sql, (nome, cpf, matricula_siape, email, telefone))
    pid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return pid

def listar_pessoas(limit=100):
    conn, cur, _ = get_dict_cursor(None)
    cur.execute("SELECT id, nome, cpf, email, ativo FROM pessoa ORDER BY id LIMIT %s", (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def atualizar_pessoa(pessoa_id, **fields):
    if not fields:
        return
    sets = []
    vals = []
    for k, v in fields.items():
        sets.append(f"{k} = %s")
        vals.append(v)
    vals.append(pessoa_id)
    sql = f"UPDATE pessoa SET {', '.join(sets)} WHERE id = %s"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, vals)
    conn.commit()
    cur.close()
    conn.close()
