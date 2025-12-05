from db.conexao import get_conn
from decimal import Decimal
def registrar_movimento(produto_variacao_id, local_estoque_id, tipo_movimento_id, quantidade, funcionario_id=None, ordem_servico_id=None, observacao=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO movimento_estoque (produto_variacao_id, local_estoque_id, tipo_movimento_id, quantidade, funcionario_id, ordem_servico_id, observacao) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                (produto_variacao_id, local_estoque_id, tipo_movimento_id, int(quantidade), funcionario_id, ordem_servico_id, observacao))
    mid=cur.fetchone()[0]
    cur.execute("SELECT sinal FROM tipo_movimento_estoque WHERE id=%s",(tipo_movimento_id,))
    sinal=cur.fetchone()[0]
    if sinal == '+':
        cur.execute("INSERT INTO estoque (produto_variacao_id, local_estoque_id, quantidade) SELECT %s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM estoque WHERE produto_variacao_id=%s AND local_estoque_id=%s)",
                    (produto_variacao_id, local_estoque_id, int(quantidade), produto_variacao_id, local_estoque_id))
        cur.execute("UPDATE estoque SET quantidade = quantidade + %s WHERE produto_variacao_id=%s AND local_estoque_id=%s",(int(quantidade), produto_variacao_id, local_estoque_id))
    else:
        cur.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE produto_variacao_id=%s AND local_estoque_id=%s",(int(quantidade), produto_variacao_id, local_estoque_id))
    conn.commit(); cur.close(); conn.close(); return mid
