from db.conexao import get_conn, get_dict_cursor
def criar_ordem_servico(numero_sequencial, solicitante_id, area_campus_id, tipo_os_id, equipe_id=None, lider_id=None, prioridade=3, data_prevista=None, descricao_problema=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO ordem_servico (numero_sequencial,solicitante_id,area_campus_id,tipo_os_id,equipe_id,lider_id,prioridade,data_prevista,descricao_problema) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                (numero_sequencial,solicitante_id,area_campus_id,tipo_os_id,equipe_id,lider_id,prioridade,data_prevista,descricao_problema))
    oid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return oid

def adicionar_item_os(os_id, produto_variacao_id, quantidade_prevista):
    conn=get_conn(); cur=conn.cursor(); cur.execute("INSERT INTO item_ordem_servico (os_id,produto_variacao_id,quantidade_prevista) VALUES (%s,%s,%s) RETURNING id",(os_id,produto_variacao_id,quantidade_prevista)); iid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return iid

def listar_os_abertas():
    conn,cur,_=get_dict_cursor(None)
    cur.execute("""SELECT os.id, os.numero_sequencial, os.prioridade, ac.descricao AS area, tos.descricao AS tipo_servico, p.nome AS solicitante, os.data_abertura
                   FROM ordem_servico os
                   LEFT JOIN area_campus ac ON os.area_campus_id = ac.id
                   LEFT JOIN tipo_ordem_servico tos ON os.tipo_os_id = tos.id
                   LEFT JOIN status_ordem_servico sts ON os.status_id = sts.id
                   LEFT JOIN pessoa p ON os.solicitante_id = p.id
                   WHERE COALESCE(sts.descricao,'aberta') IN ('aberta','em_atendimento','aguardando_material')
                   ORDER BY os.prioridade ASC, os.data_abertura ASC;""")
    res=cur.fetchall(); cur.close(); conn.close(); return res

def timeline_os(os_id):
    conn,cur,_=get_dict_cursor(None)
    cur.execute("""SELECT a.data_hora, pes.nome AS funcionario, sts_novo.descricao AS status_atual, a.descricao FROM andamento_ordem_servico a
                   LEFT JOIN funcionario f ON a.funcionario_id=f.id LEFT JOIN pessoa pes ON f.pessoa_id=pes.id LEFT JOIN status_ordem_servico sts_novo ON a.status_novo_id=sts_novo.id WHERE a.os_id=%s ORDER BY a.data_hora""",(os_id,))
    res=cur.fetchall(); cur.close(); conn.close(); return res

def registrar_andamento(os_id, funcionario_id, status_anterior_id, status_novo_id, descricao=None, inicio_atendimento=None, fim_atendimento=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO andamento_ordem_servico (os_id,status_anterior_id,status_novo_id,funcionario_id,descricao,inicio_atendimento,fim_atendimento) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",(os_id,status_anterior_id,status_novo_id,funcionario_id,descricao,inicio_atendimento,fim_atendimento))
    aid=cur.fetchone()[0]; cur.execute("UPDATE ordem_servico SET status_id=%s WHERE id=%s",(status_novo_id,os_id)); conn.commit(); cur.close(); conn.close(); return aid
