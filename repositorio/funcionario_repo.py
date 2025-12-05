from db.conexao import get_conn, get_dict_cursor
from datetime import date
def criar_funcionario(pessoa_id, tipo_funcionario_id=None, setor_id=None, data_admissao=None):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO funcionario (pessoa_id,tipo_funcionario_id,setor_id,data_admissao) VALUES (%s,%s,%s,%s) RETURNING id",
                (pessoa_id,tipo_funcionario_id,setor_id,data_admissao))
    fid = cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return fid
def listar_funcionarios(limit=100):
    conn, cur, _ = get_dict_cursor(None)
    cur.execute("""SELECT f.id, p.nome AS nome, tf.descricao AS tipo, s.nome AS setor, f.data_admissao FROM funcionario f
                   LEFT JOIN pessoa p ON f.pessoa_id=p.id LEFT JOIN tipo_funcionario tf ON f.tipo_funcionario_id=tf.id LEFT JOIN setor s ON f.setor_id=s.id
                   ORDER BY f.id LIMIT %s""",(limit,))
    res=cur.fetchall(); cur.close(); conn.close(); return res
