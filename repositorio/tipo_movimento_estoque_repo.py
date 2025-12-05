from db.conexao import get_conn, get_dict_cursor
def criar_tipo(descricao, sinal):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO tipo_movimento_estoque (descricao,sinal) VALUES (%s,%s) RETURNING id",(descricao,sinal)); tid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return tid
def listar_tipos():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,descricao,sinal FROM tipo_movimento_estoque ORDER BY id"); res=cur.fetchall(); cur.close(); conn.close(); return res
