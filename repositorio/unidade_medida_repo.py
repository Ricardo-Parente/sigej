from db.conexao import get_conn, get_dict_cursor
def criar_unidade(sigla, descricao):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO unidade_medida (sigla,descricao) VALUES (%s,%s) RETURNING id",(sigla,descricao)); uid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return uid
def listar_unidades():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,sigla,descricao FROM unidade_medida ORDER BY sigla"); res=cur.fetchall(); cur.close(); conn.close(); return res
