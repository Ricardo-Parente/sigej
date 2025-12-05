from db.conexao import get_conn, get_dict_cursor
def criar_tipo(descricao):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO tipo_ordem_servico (descricao) VALUES (%s) RETURNING id",(descricao,)); tid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return tid
def listar_tipos():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,descricao FROM tipo_ordem_servico ORDER BY id"); res=cur.fetchall(); cur.close(); conn.close(); return res
