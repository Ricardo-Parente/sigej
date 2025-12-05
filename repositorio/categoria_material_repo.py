from db.conexao import get_conn, get_dict_cursor
def criar_categoria(nome):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO categoria_material (nome) VALUES (%s) RETURNING id",(nome,)); cid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return cid
def listar_categorias():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,nome FROM categoria_material ORDER BY nome"); res=cur.fetchall(); cur.close(); conn.close(); return res
