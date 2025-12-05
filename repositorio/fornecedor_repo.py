from db.conexao import get_conn, get_dict_cursor
def criar_fornecedor(nome, cnpj=None):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO fornecedor (nome,cnpj) VALUES (%s,%s) RETURNING id",(nome,cnpj)); fid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return fid
def listar_fornecedores():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,nome,cnpj FROM fornecedor ORDER BY nome"); res=cur.fetchall(); cur.close(); conn.close(); return res
