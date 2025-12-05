from db.conexao import get_conn, get_dict_cursor
def criar_produto(descricao, categoria_id=None, unidade_medida_id=None, marca_id=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO produto (descricao,categoria_id,unidade_medida_id,marca_id) VALUES (%s,%s,%s,%s) RETURNING id",(descricao,categoria_id,unidade_medida_id,marca_id))
    pid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return pid

def criar_variacao(produto_id, cor_id=None, tamanho_id=None, codigo_barras=None, codigo_interno=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO produto_variacao (produto_id,cor_id,tamanho_id,codigo_barras,codigo_interno) VALUES (%s,%s,%s,%s,%s) RETURNING id",(produto_id,cor_id,tamanho_id,codigo_barras,codigo_interno))
    vid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return vid

def listar_produtos(limit=100):
    conn,cur,_=get_dict_cursor(None)
    cur.execute("SELECT p.id,p.descricao,c.nome AS categoria,u.sigla AS unidade,m.nome AS marca FROM produto p LEFT JOIN categoria_material c ON p.categoria_id=c.id LEFT JOIN unidade_medida u ON p.unidade_medida_id=u.id LEFT JOIN marca m ON p.marca_id=m.id ORDER BY p.id LIMIT %s",(limit,))
    res=cur.fetchall(); cur.close(); conn.close(); return res
