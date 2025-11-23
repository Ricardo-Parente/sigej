# repositorio/estoque_repo.py
from db.conexao import get_conn, get_dict_cursor
from decimal import Decimal

def create_local_estoque(descricao, responsavel_id=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO local_estoque (descricao, responsavel_id) VALUES (%s, %s) RETURNING id", (descricao, responsavel_id))
    lid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return lid

def set_estoque(produto_variacao_id, local_estoque_id, quantidade, ponto_reposicao=0):
    conn = get_conn()
    cur = conn.cursor()
    # upsert
    sql = """
    INSERT INTO estoque (produto_variacao_id, local_estoque_id, quantidade, ponto_reposicao)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (produto_variacao_id, local_estoque_id)
    DO UPDATE SET quantidade = EXCLUDED.quantidade, ponto_reposicao = EXCLUDED.ponto_reposicao;
    """
    cur.execute(sql, (produto_variacao_id, local_estoque_id, Decimal(quantidade), Decimal(ponto_reposicao)))
    conn.commit()
    cur.close()
    conn.close()

def get_estoque_below_reorder():
    conn, cur, _ = get_dict_cursor(None)
    sql = """
    SELECT p.descricao, pv.codigo_interno, le.descricao AS local, e.quantidade, e.ponto_reposicao
    FROM estoque e
    JOIN produto_variacao pv ON e.produto_variacao_id = pv.id
    JOIN produto p ON pv.produto_id = p.id
    JOIN local_estoque le ON e.local_estoque_id = le.id
    WHERE e.quantidade < e.ponto_reposicao;
    """
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res
