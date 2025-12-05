from db.conexao import get_conn, get_dict_cursor
def criar_marca(nome):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO marca (nome) VALUES (%s) RETURNING id",(nome,)); mid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return mid
def listar_marcas():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,nome FROM marca ORDER BY nome"); res=cur.fetchall(); cur.close(); conn.close(); return res
