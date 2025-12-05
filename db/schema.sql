-- ============================================================
-- SIGEJ - Sistema de Gestão de Jardinagem e Manutenção
-- Banco completo com 25 tabelas
-- ============================================================

-- ============================================================
-- 1. PESSOAS E FUNCIONÁRIOS
-- ============================================================

CREATE TABLE pessoa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(11) UNIQUE,
    email VARCHAR(120),
    telefone VARCHAR(20),
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE tipo_funcionario (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE setor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    sigla VARCHAR(10)
);

CREATE TABLE funcionario (
    id SERIAL PRIMARY KEY,
    pessoa_id INTEGER REFERENCES pessoa(id),
    tipo_funcionario_id INTEGER REFERENCES tipo_funcionario(id),
    setor_id INTEGER REFERENCES setor(id),
    data_admissao DATE NOT NULL DEFAULT CURRENT_DATE,
    data_demissao DATE
);

-- ============================================================
-- 2. CAMPUS E ÁREAS
-- ============================================================

CREATE TABLE tipo_area_campus (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE area_campus (
    id SERIAL PRIMARY KEY,
    tipo_area_id INTEGER REFERENCES tipo_area_campus(id),
    descricao VARCHAR(150) NOT NULL,
    bloco VARCHAR(20)
);

-- ============================================================
-- 3. EQUIPES DE MANUTENÇÃO
-- ============================================================

CREATE TABLE equipe_manutencao (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    turno VARCHAR(40)
);

CREATE TABLE equipe_membro (
    id SERIAL PRIMARY KEY,
    equipe_id INTEGER REFERENCES equipe_manutencao(id),
    funcionario_id INTEGER REFERENCES funcionario(id),
    funcao VARCHAR(80),
    data_inicio DATE DEFAULT CURRENT_DATE,
    data_fim DATE
);

-- ============================================================
-- 4. MATERIAIS / PRODUTOS
-- ============================================================

CREATE TABLE categoria_material (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL
);

CREATE TABLE unidade_medida (
    id SERIAL PRIMARY KEY,
    sigla VARCHAR(10) NOT NULL,
    descricao VARCHAR(60) NOT NULL
);

CREATE TABLE fornecedor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cnpj VARCHAR(14)
);

CREATE TABLE marca (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL
);

CREATE TABLE cor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL
);

CREATE TABLE tamanho (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(40) NOT NULL
);

CREATE TABLE produto (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(150) NOT NULL,
    categoria_id INTEGER REFERENCES categoria_material(id),
    unidade_medida_id INTEGER REFERENCES unidade_medida(id),
    marca_id INTEGER REFERENCES marca(id)
);

CREATE TABLE produto_variacao (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER REFERENCES produto(id),
    cor_id INTEGER REFERENCES cor(id),
    tamanho_id INTEGER REFERENCES tamanho(id),
    codigo_barras VARCHAR(40),
    codigo_interno VARCHAR(40)
);

-- ============================================================
-- 5. ESTOQUE E MOVIMENTAÇÃO
-- ============================================================

CREATE TABLE local_estoque (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(120) NOT NULL,
    responsavel_id INTEGER REFERENCES funcionario(id)
);

CREATE TABLE estoque (
    produto_variacao_id INTEGER REFERENCES produto_variacao(id),
    local_estoque_id INTEGER REFERENCES local_estoque(id),
    quantidade INTEGER NOT NULL DEFAULT 0,
    ponto_reposicao INTEGER DEFAULT 0,
    PRIMARY KEY (produto_variacao_id, local_estoque_id)
);

CREATE TABLE tipo_movimento_estoque (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(60) NOT NULL UNIQUE,
    sinal CHAR(1) NOT NULL CHECK (sinal IN ('+', '-'))
);

CREATE TABLE movimento_estoque (
    id SERIAL PRIMARY KEY,
    produto_variacao_id INTEGER REFERENCES produto_variacao(id),
    local_estoque_id INTEGER REFERENCES local_estoque(id),
    tipo_movimento_id INTEGER REFERENCES tipo_movimento_estoque(id),
    funcionario_id INTEGER REFERENCES funcionario(id),
    ordem_servico_id INTEGER,
    quantidade INTEGER NOT NULL,
    data_hora TIMESTAMP DEFAULT NOW(),
    observacao TEXT
);

-- ============================================================
-- 6. ORDEM DE SERVIÇO
-- ============================================================

CREATE TABLE tipo_ordem_servico (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE status_ordem_servico (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE ordem_servico (
    id SERIAL PRIMARY KEY,
    numero_sequencial VARCHAR(20) UNIQUE,
    solicitante_id INTEGER REFERENCES pessoa(id),
    area_campus_id INTEGER REFERENCES area_campus(id),
    tipo_os_id INTEGER REFERENCES tipo_ordem_servico(id),
    equipe_id INTEGER REFERENCES equipe_manutencao(id),
    lider_id INTEGER REFERENCES funcionario(id),
    status_id INTEGER REFERENCES status_ordem_servico(id),
    prioridade INTEGER DEFAULT 1,
    descricao_problema TEXT,
    data_abertura TIMESTAMP DEFAULT NOW(),
    data_prevista DATE
);

CREATE TABLE item_ordem_servico (
    id SERIAL PRIMARY KEY,
    os_id INTEGER REFERENCES ordem_servico(id),
    produto_variacao_id INTEGER REFERENCES produto_variacao(id),
    quantidade_prevista INTEGER,
    quantidade_usada INTEGER
);

CREATE TABLE andamento_ordem_servico (
    id SERIAL PRIMARY KEY,
    os_id INTEGER REFERENCES ordem_servico(id),
    status_anterior_id INTEGER REFERENCES status_ordem_servico(id),
    status_novo_id INTEGER REFERENCES status_ordem_servico(id),
    funcionario_id INTEGER REFERENCES funcionario(id),
    data_hora TIMESTAMP DEFAULT NOW(),
    descricao TEXT,
    inicio_atendimento TIMESTAMP,
    fim_atendimento TIMESTAMP
);
