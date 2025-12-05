from db.conexao import get_conn, get_dict_cursor
def criar_local(descricao, responsavel_id=None):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO local_estoque (descricao,responsavel_id) VALUES (%s,%s) RETURNING id",(descricao,responsavel_id)); lid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return lid
def listar_locais():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT l.id,l.descricao,l.responsavel_id,p.nome as responsavel FROM local_estoque l LEFT JOIN funcionario f ON l.responsavel_id=f.id LEFT JOIN pessoa p ON f.pessoa_id=p.id ORDER BY l.id"); res=cur.fetchall(); cur.close(); conn.close(); return res
