from db.conexao import get_conn, get_dict_cursor
def criar_status(descricao):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) RETURNING id",(descricao,)); sid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return sid
def listar_status():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,descricao FROM status_ordem_servico ORDER BY id"); res=cur.fetchall(); cur.close(); conn.close(); return res
