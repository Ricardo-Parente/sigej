from db.conexao import get_conn, get_dict_cursor
def adicionar_membro(equipe_id, funcionario_id, funcao=None, data_inicio=None, data_fim=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO equipe_membro (equipe_id,funcionario_id,funcao,data_inicio,data_fim) VALUES (%s,%s,%s,%s,%s) RETURNING id",(equipe_id,funcionario_id,funcao,data_inicio,data_fim))
    mid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return mid
def listar_membros(equipe_id):
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT em.id,em.funcionario_id,p.nome AS nome_funcao,em.funcao,em.data_inicio FROM equipe_membro em JOIN funcionario f ON em.funcionario_id=f.id JOIN pessoa p ON f.pessoa_id=p.id WHERE em.equipe_id=%s",(equipe_id,)); res=cur.fetchall(); cur.close(); conn.close(); return res
