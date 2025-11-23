# repositorio/produto_repo.py
from db.conexao import get_conn, get_dict_cursor

def criar_produto(descricao, categoria_id=None, unidade_medida_id=None, marca_id=None):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
    INSERT INTO produto (descricao, categoria_id, unidade_medida_id, marca_id)
    VALUES (%s, %s, %s, %s) RETURNING id;
    """
    cur.execute(sql, (descricao, categoria_id, unidade_medida_id, marca_id))
    pid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return pid

def criar_variacao(produto_id, codigo_interno=None, codigo_barras=None, cor_id=None, tamanho_id=None):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
    INSERT INTO produto_variacao (produto_id, cor_id, tamanho_id, codigo_barras, codigo_interno)
    VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    cur.execute(sql, (produto_id, cor_id, tamanho_id, codigo_barras, codigo_interno))
    vid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return vid
