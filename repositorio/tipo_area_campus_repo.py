from db.conexao import get_conn, get_dict_cursor
def criar_tipo_area(descricao):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO tipo_area_campus (descricao) VALUES (%s) RETURNING id",(descricao,))
    tid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return tid
def listar_tipos_area():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT id,descricao FROM tipo_area_campus ORDER BY id"); res=cur.fetchall(); cur.close(); conn.close(); return res
