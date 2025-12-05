from db.conexao import get_conn, get_dict_cursor
def criar_area(tipo_area_id, descricao, bloco=None):
    conn=get_conn(); cur=conn.cursor()
    cur.execute("INSERT INTO area_campus (tipo_area_id,descricao,bloco) VALUES (%s,%s,%s) RETURNING id",(tipo_area_id,descricao,bloco))
    aid=cur.fetchone()[0]; conn.commit(); cur.close(); conn.close(); return aid
def listar_areas():
    conn,cur,_=get_dict_cursor(None); cur.execute("SELECT a.id,a.descricao,a.bloco,t.descricao AS tipo FROM area_campus a JOIN tipo_area_campus t ON a.tipo_area_id=t.id ORDER BY a.id"); res=cur.fetchall(); cur.close(); conn.close(); return res
