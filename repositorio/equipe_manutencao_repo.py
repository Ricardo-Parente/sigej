from db.conexao import get_conn, get_dict_cursor
def criar_equipe(nome, turno=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO equipe_manutencao (nome,turno) VALUES (%s,%s) RETURNING id",(nome,turno))
    eid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return eid
def listar_equipes():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,nome,turno FROM equipe_manutencao ORDER BY nome"); res=cur.fetchall(); cur.close(); conn.close(); return res
