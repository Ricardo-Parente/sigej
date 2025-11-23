# main.py
import sys, os
sys.path.append(os.path.dirname(__file__))
from db.init_db import run_script, seed_initial_data
from repositorio.pessoa_repo import criar_pessoa, listar_pessoas
from repositorio.produto_repo import criar_produto, criar_variacao
from repositorio.estoque_repo import create_local_estoque, set_estoque, get_estoque_below_reorder
from repositorio.movimento_repo import registrar_movimento
from repositorio.ordem_servico_repo import criar_ordem_servico, adicionar_item_os, listar_os_abertas, timeline_os, registrar_andamento
from db import conexao
import datetime

HERE = os.path.dirname(__file__)

def setup_db():
    path = os.path.join(HERE, "db", "schema.sql")
    run_script(path)
    seed_initial_data()

def demo():
    print("=== DEMO SIGEJ (Python) ===")
    # Criar pessoas
    pid = criar_pessoa("João da Silva", cpf="12345678901", email="joao@ifce.edu.br")
    print("Pessoa criada:", pid)
    # Criar produto e variação
    prod_id = criar_produto("Adubo NPK 4kg")
    var_id = criar_variacao(prod_id, codigo_interno="ADUBO4KG")
    print("Produto e variação criados:", prod_id, var_id)
    # Criar local de estoque e setar estoque
    local_id = create_local_estoque("Depósito Central")
    set_estoque(var_id, local_id, 10, ponto_reposicao=5)
    print("Estoque inicial configurado.")
    # Registrar saída (tipo_movimento_estoque id 2 assumido como Saída)
    # Descobrir ids de tipos via SQL no DB se diferente
    mover = registrar_movimento(var_id, local_id, 2, 2, funcionario_id=None, ordem_servico_id=None, observacao="Uso em jardim")
    print("Movimento registrado:", mover)
    # Criar area e OS (é preciso que area_campus exista; criar manual na DB antes ou ajustar aqui)
    # Para demo simples, vamos inserir area temporariamente
    conn = conexao.get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO area_campus (descricao, bloco) VALUES (%s,%s) RETURNING id", ("Jardim Principal","A"))
    area_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    os_num = "OS-0001"
    os_id = criar_ordem_servico(os_num, pid, area_id, 1, equipe_id=None, lider_id=None, prioridade=2, data_prevista=datetime.date.today(), descricao_problema="Poda de arbustos")
    print("OS criada:", os_id)
    # adicionar item
    adicionar_item_os(os_id, var_id, 1)
    print("Item adicionado na OS.")
    # registrar andamento e atualizar status (status ids: dependerão dos inserts do seed; ajustar se necessário)
    registrar_andamento(os_id, funcionario_id=None, status_anterior_id=1, status_novo_id=2, descricao="Iniciando atendimento")
    print("Andamento registrado.")
    # Relatórios
    print("\n--- OS em aberto ---")
    for r in listar_os_abertas():
        print(r)
    print("\n--- Materiais abaixo do ponto de reposição ---")
    for r in get_estoque_below_reorder():
        print(r)
    print("\n--- Timeline OS ---")
    for r in timeline_os(os_id):
        print(r)

if __name__ == "__main__":
    # Se quiser rodar a criação do schema automaticamente:
    # setup_db()
    demo()
