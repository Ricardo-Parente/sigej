from db.conexao import get_conn, get_dict_cursor
from decimal import Decimal

def create_local_estoque(descricao):
    """
    Cria um local de estoque e retorna o ID gerado.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO local_estoque (descricao) VALUES (%s) RETURNING id",
        (descricao,)
    )
    local_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return local_id


def set_estoque(produto_variacao_id, local_estoque_id, quantidade, ponto_reposicao=0):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO estoque (produto_variacao_id, local_estoque_id, quantidade, ponto_reposicao)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (produto_variacao_id, local_estoque_id)
           DO UPDATE SET
                quantidade = EXCLUDED.quantidade,
                ponto_reposicao = EXCLUDED.ponto_reposicao""",
        (produto_variacao_id, local_estoque_id, int(quantidade), int(ponto_reposicao))
    )
    conn.commit()
    cur.close()
    conn.close()


def get_estoque_below_reorder():
    conn, cur, _ = get_dict_cursor(None)
    cur.execute(
        """SELECT 
                p.descricao,
                pv.codigo_interno,
                le.descricao AS local,
                e.quantidade,
                e.ponto_reposicao
           FROM estoque e
           JOIN produto_variacao pv ON e.produto_variacao_id = pv.id
           JOIN produto p ON pv.produto_id = p.id
           JOIN local_estoque le ON e.local_estoque_id = le.id
           WHERE e.quantidade < e.ponto_reposicao"""
    )
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res
