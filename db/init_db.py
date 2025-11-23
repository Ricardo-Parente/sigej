# db/init_db.py

import sys
import os

# Adiciona a pasta raiz (sigej/) ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.conexao import get_conn

def run_script(path):
    conn = get_conn()
    cur = conn.cursor()
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("Schema executado.")

def seed_initial_data():
    conn = get_conn()
    cur = conn.cursor()
    # Inserir unidades, tipos e status básicos
    cur.execute("INSERT INTO unidade_medida (sigla, descricao) VALUES (%s, %s) ON CONFLICT DO NOTHING", ("un", "Unidade"))
    cur.execute("INSERT INTO tipo_movimento_estoque (descricao, sinal) VALUES (%s, %s) ON CONFLICT DO NOTHING", ("Entrada", "+"))
    cur.execute("INSERT INTO tipo_movimento_estoque (descricao, sinal) VALUES (%s, %s) ON CONFLICT DO NOTHING", ("Saída", "-"))
    cur.execute("INSERT INTO tipo_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Manutenção Corretiva",))
    cur.execute("INSERT INTO tipo_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Manutenção Preventiva",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("aberta",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("em_atendimento",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("aguardando_material",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("concluída",))
    conn.commit()
    cur.close()
    conn.close()
    print("Dados mestres inseridos.")

if __name__ == "__main__":
    run_script(os.path.join(os.path.dirname(__file__), "schema.sql"))
    seed_initial_data()
