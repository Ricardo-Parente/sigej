from db.conexao import get_conn, get_dict_cursor
def criar_cor(nome):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO cor (nome) VALUES (%s) RETURNING id",(nome,)); cid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return cid
def listar_cores():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,nome FROM cor ORDER BY nome"); res=cur.fetchall(); cur.close(); conn.close(); return res
