# db/init_db.py
import os
import sys
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
    print("Schema executado com sucesso.")


def seed_initial_data():
    conn = get_conn()
    cur = conn.cursor()
    print("Inserindo seeds...")

    # UNIDADES
    cur.execute("INSERT INTO unidade_medida (sigla, descricao) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("un","Unidade"))
    cur.execute("INSERT INTO unidade_medida (sigla, descricao) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("kg","Quilograma"))
    cur.execute("INSERT INTO unidade_medida (sigla, descricao) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("lt","Litro"))

    # TIPO MOVIMENTO ESTOQUE
    cur.execute("INSERT INTO tipo_movimento_estoque (descricao, sinal) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("Entrada","+"))
    cur.execute("INSERT INTO tipo_movimento_estoque (descricao, sinal) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("Saída","-"))

    # TIPO ORDEM E STATUS
    cur.execute("INSERT INTO tipo_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Manutenção Corretiva",))
    cur.execute("INSERT INTO tipo_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Manutenção Preventiva",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("aberta",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("em_atendimento",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("aguardando_material",))
    cur.execute("INSERT INTO status_ordem_servico (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("concluída",))

    # TIPOS FUNCIONARIO / SETORES
    cur.execute("INSERT INTO tipo_funcionario (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Técnico",))
    cur.execute("INSERT INTO tipo_funcionario (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Auxiliar",))
    cur.execute("INSERT INTO setor (nome, sigla) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("Infraestrutura","INF"))
    cur.execute("INSERT INTO setor (nome, sigla) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("Jardinagem","JAR"))

    # TIPOS AREA / AREA CAMPUS
    cur.execute("INSERT INTO tipo_area_campus (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Área Verde",))
    cur.execute("""
        INSERT INTO area_campus (tipo_area_id, descricao, bloco)
        VALUES ((SELECT id FROM tipo_area_campus WHERE descricao='Área Verde'), %s, %s)
        ON CONFLICT DO NOTHING
    """, ("Jardim Principal","A"))

    # EQUIPES
    cur.execute("INSERT INTO equipe_manutencao (nome, turno) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("Equipe A","Manhã"))
    cur.execute("INSERT INTO equipe_manutencao (nome, turno) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("Equipe B","Tarde"))

    # CATEGORIAS / MARCAS / CORES / TAMANHOS / FORNECEDOR
    cur.execute("INSERT INTO categoria_material (nome) VALUES (%s) ON CONFLICT DO NOTHING", ("Fertilizantes",))
    cur.execute("INSERT INTO categoria_material (nome) VALUES (%s) ON CONFLICT DO NOTHING", ("Ferramentas",))
    cur.execute("INSERT INTO marca (nome) VALUES (%s) ON CONFLICT DO NOTHING", ("MarcaEx",))
    cur.execute("INSERT INTO cor (nome) VALUES (%s) ON CONFLICT DO NOTHING", ("Verde",))
    cur.execute("INSERT INTO tamanho (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("P",))
    cur.execute("INSERT INTO fornecedor (nome, cnpj) VALUES (%s,%s) ON CONFLICT DO NOTHING", ("ForneceX","12345678000199"))

    # LOCAL ESTOQUE
    cur.execute("INSERT INTO local_estoque (descricao) VALUES (%s) ON CONFLICT DO NOTHING", ("Depósito Principal",))

    conn.commit()
    cur.close()
    conn.close()
    print("Seeds inseridos com sucesso.")


if __name__ == "__main__":
    args = sys.argv[1:]

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    if "--seed-only" in args:
        print("Executando apenas seeds...")
        seed_initial_data()
    else:
        run_script(schema_path)
        seed_initial_data()
