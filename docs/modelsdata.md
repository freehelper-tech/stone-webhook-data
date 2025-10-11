# 📊 Documentação dos Modelos de Banco de Dados

Este documento descreve a estrutura completa do banco de dados do Dashboard Impulso Stone, incluindo todas as tabelas, campos, tipos de dados e relacionamentos.

---

## 📚 Índice

1. [Visão Geral](#visão-geral)
2. [Tabela: empreendedores](#tabela-empreendedores)
3. [Tabela: mentores](#tabela-mentores)
4. [Tabela: status_mentoria](#tabela-status_mentoria)
5. [Tabela: creditos](#tabela-creditos)
6. [Tabela: nps_scores](#tabela-nps_scores)
7. [Tabela: ludos_atividades](#tabela-ludos_atividades)
8. [Relacionamentos](#relacionamentos)
9. [Exemplos de Inserção](#exemplos-de-inserção)

---

## 🎯 Visão Geral

### Banco de Dados Suportados

# Para produção (Azure SQL Server)
AZURE_SQL_CONNECTION_STRING="mssql+pyodbc://usr_free_helper:23%403ryR2@dev-free-helper.database.windows.net:1433/dashboardImpulso?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&ConnectionTimeout=30"


- **Azure SQL Server** (produção): Via connection string ODBC

### Tecnologias
- **ORM**: SQLAlchemy 2.0.43
- **Driver SQL Server**: pyodbc 5.2.0

### Estrutura de Tabelas

```
empreendedores (principal)
├── status_mentoria (1:N)
├── creditos (1:N)
├── nps_scores (1:N)
└── ludos_atividades (1:N)

mentores
└── status_mentoria (1:N)
```

---

## 📋 Tabela: `empreendedores`

Tabela principal que armazena todos os dados dos empreendedores.

### Estrutura SQL

```sql
CREATE TABLE empreendedores (
    -- Campos Principais (OBRIGATÓRIOS)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telefone VARCHAR(20) NOT NULL,  -- ⚠️ SEM UNIQUE para permitir duplicatas
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    comunidade_originadora VARCHAR(50),
    data_inscricao DATETIME,
    
    -- Campos do Formulário Jotform
    apelido VARCHAR(100),
    cpf VARCHAR(14),
    cidade VARCHAR(100),
    estado VARCHAR(50),
    idade VARCHAR(20),
    genero VARCHAR(50),
    raca_cor VARCHAR(50),
    escolaridade VARCHAR(100),
    faixa_renda VARCHAR(100),
    fonte_renda TEXT,
    tempo_funcionamento VARCHAR(50),
    segmento_atuacao VARCHAR(100),
    segmento_outros VARCHAR(100),
    organizacao_stone VARCHAR(100),
    formulario_tipo VARCHAR(50),
    
    -- Campos da Plataforma Ludos
    ludos_id INTEGER,
    ludos_login VARCHAR(100),
    ludos_status VARCHAR(20),
    ludos_pontos INTEGER DEFAULT 0,
    ludos_moedas INTEGER DEFAULT 0,
    ludos_nivel INTEGER DEFAULT 1,
    ludos_primeiro_login DATETIME,
    ludos_ultimo_login DATETIME,
    
    -- Campos do MGM (WhatsApp)
    mgm_user_name VARCHAR(100),
    mgm_whatsapp VARCHAR(20),
    mgm_total_mensagens INTEGER DEFAULT 0,
    mgm_total_reacoes INTEGER DEFAULT 0,
    mgm_total_interacoes INTEGER DEFAULT 0,
    mgm_ultima_mensagem DATETIME,
    mgm_ultima_reacao DATETIME,
    mgm_engajamento_percent FLOAT DEFAULT 0.0,
    
    -- Status Flags (Booleanos)
    esta_na_comunidade BOOLEAN DEFAULT 0,
    esta_no_grupo_mentoria BOOLEAN DEFAULT 0,
    esta_no_papo_impulso BOOLEAN DEFAULT 0,
    interacao_nos_grupos INTEGER DEFAULT 0,
    ativo_na_ludos BOOLEAN DEFAULT 0,
    fazendo_mentoria BOOLEAN DEFAULT 0,
    solicitou_credito BOOLEAN DEFAULT 0,
    
    -- NPS Scores
    nps_geral INTEGER,      -- 0-10
    nps_mentoria INTEGER,   -- 0-10
    nps_ludos INTEGER       -- 0-10
);
```

### 📝 Descrição dos Campos

#### Campos Obrigatórios

| Campo | Tipo | Tamanho | Descrição | Exemplo |
|-------|------|---------|-----------|---------|
| `id` | INTEGER | - | ID único (auto incremento) | 1 |
| `telefone` | VARCHAR | 20 | Telefone do empreendedor | `(11) 987654321` |
| `nome` | VARCHAR | 100 | Nome completo | `João Silva` |

#### Campos Principais

| Campo | Tipo | Tamanho | Descrição | Exemplo |
|-------|------|---------|-----------|---------|
| `email` | VARCHAR | 100 | Email | `joao@gmail.com` |
| `comunidade_originadora` | VARCHAR | 50 | Comunidade de origem | `Impulso Stone` |
| `data_inscricao` | DATETIME | - | Data/hora da inscrição | `2025-10-10 12:30:00` |

#### Campos Demográficos

| Campo | Tipo | Tamanho | Descrição | Valores Possíveis |
|-------|------|---------|-----------|-------------------|
| `cpf` | VARCHAR | 14 | CPF (sem formatação) | `12345678900` |
| `cidade` | VARCHAR | 100 | Cidade | `São Paulo` |
| `estado` | VARCHAR | 50 | Estado (UF ou nome) | `SP` ou `São Paulo` |
| `idade` | VARCHAR | 20 | Faixa etária | `25 a 34 anos` |
| `genero` | VARCHAR | 50 | Gênero | `Masculino`, `Feminino`, etc. |
| `raca_cor` | VARCHAR | 50 | Raça/cor | `Branca`, `Parda`, `Preta`, etc. |

#### Campos Socioeconômicos

| Campo | Tipo | Tamanho | Descrição | Valores Possíveis |
|-------|------|---------|-----------|-------------------|
| `escolaridade` | VARCHAR | 100 | Nível de escolaridade | `Ensino Superior completo` |
| `faixa_renda` | VARCHAR | 100 | Faixa de renda mensal | `Entre 1 e 2 salários mínimos` |
| `fonte_renda` | TEXT | - | Fontes de renda (separadas por `;`) | `MEI; CLT` |

#### Campos do Negócio

| Campo | Tipo | Tamanho | Descrição | Valores Possíveis |
|-------|------|---------|-----------|-------------------|
| `tempo_funcionamento` | VARCHAR | 50 | Tempo de negócio | `1 a 3 anos`, `Menos de 6 meses` |
| `segmento_atuacao` | VARCHAR | 100 | Segmento principal | `Tecnologia`, `Alimentação` |
| `segmento_outros` | VARCHAR | 100 | Outro segmento (se aplicável) | `Desenvolvimento web` |
| `organizacao_stone` | VARCHAR | 100 | Organização da Rede Stone | `Banco Pérola` |
| `formulario_tipo` | VARCHAR | 50 | Origem do cadastro | `Comunidade Impulso` |

#### Campos Ludos (Plataforma de Cursos)

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `ludos_id` | INTEGER | NULL | ID do usuário no Ludos |
| `ludos_login` | VARCHAR(100) | NULL | Login/email no Ludos |
| `ludos_status` | VARCHAR(20) | NULL | Status (`Ativo`/`Inativo`) |
| `ludos_pontos` | INTEGER | 0 | Total de pontos acumulados |
| `ludos_moedas` | INTEGER | 0 | Total de moedas |
| `ludos_nivel` | INTEGER | 1 | Nível atual (1-N) |
| `ludos_primeiro_login` | DATETIME | NULL | Data do primeiro acesso |
| `ludos_ultimo_login` | DATETIME | NULL | Data do último acesso |

#### Campos MGM (WhatsApp)

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `mgm_user_name` | VARCHAR(100) | NULL | Nome no WhatsApp |
| `mgm_whatsapp` | VARCHAR(20) | NULL | Número do WhatsApp |
| `mgm_total_mensagens` | INTEGER | 0 | Total de mensagens enviadas |
| `mgm_total_reacoes` | INTEGER | 0 | Total de reações |
| `mgm_total_interacoes` | INTEGER | 0 | Total de interações |
| `mgm_ultima_mensagem` | DATETIME | NULL | Data da última mensagem |
| `mgm_ultima_reacao` | DATETIME | NULL | Data da última reação |
| `mgm_engajamento_percent` | FLOAT | 0.0 | Percentual de engajamento (0-100) |

#### Status Flags (Booleanos)

| Campo | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| `esta_na_comunidade` | BOOLEAN | 0 | Está na comunidade? |
| `esta_no_grupo_mentoria` | BOOLEAN | 0 | Está no grupo de mentoria? |
| `esta_no_papo_impulso` | BOOLEAN | 0 | Está no grupo Papo Impulso? |
| `interacao_nos_grupos` | INTEGER | 0 | Número total de interações |
| `ativo_na_ludos` | BOOLEAN | 0 | Ativo na plataforma Ludos? |
| `fazendo_mentoria` | BOOLEAN | 0 | Está em mentoria ativa? |
| `solicitou_credito` | BOOLEAN | 0 | Solicitou crédito? |

#### NPS (Net Promoter Score)

| Campo | Tipo | Range | Descrição |
|-------|------|-------|-----------|
| `nps_geral` | INTEGER | 0-10 | NPS geral do programa |
| `nps_mentoria` | INTEGER | 0-10 | NPS da mentoria |
| `nps_ludos` | INTEGER | 0-10 | NPS da plataforma Ludos |

---

## 👨‍🏫 Tabela: `mentores`

Armazena dados dos mentores do programa.

### Estrutura SQL

```sql
CREATE TABLE mentores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);
```

### Campos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `id` | INTEGER | Sim | ID único |
| `nome` | VARCHAR(100) | Sim | Nome completo do mentor |
| `telefone` | VARCHAR(20) | Sim | Telefone de contato |
| `email` | VARCHAR(100) | Sim | Email do mentor |

---

## 🤝 Tabela: `status_mentoria`

Relaciona empreendedores com mentores e armazena o status da mentoria.

### Estrutura SQL

```sql
CREATE TABLE status_mentoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendedor_id INTEGER NOT NULL,
    mentor_id INTEGER,
    status VARCHAR(50) NOT NULL,
    data_inicio DATETIME,
    data_fim DATETIME,
    horas_realizadas FLOAT DEFAULT 0.0,
    observacoes TEXT,
    data_atualizacao DATETIME,
    FOREIGN KEY (empreendedor_id) REFERENCES empreendedores(id),
    FOREIGN KEY (mentor_id) REFERENCES mentores(id)
);
```

### Campos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `id` | INTEGER | Sim | ID único |
| `empreendedor_id` | INTEGER | Sim | FK para empreendedores |
| `mentor_id` | INTEGER | Não | FK para mentores |
| `status` | VARCHAR(50) | Sim | Status da mentoria |
| `data_inicio` | DATETIME | Não | Data de início |
| `data_fim` | DATETIME | Não | Data de término |
| `horas_realizadas` | FLOAT | Não | Total de horas realizadas |
| `observacoes` | TEXT | Não | Observações sobre a mentoria |
| `data_atualizacao` | DATETIME | Não | Data da última atualização |

### Valores de Status

- `Inscrito` - Empreendedor inscrito, aguardando match
- `Em andamento` - Mentoria ativa
- `Pausada` - Mentoria temporariamente pausada
- `Finalizada` - Mentoria concluída
- `Cancelada` - Mentoria cancelada

---

## 💰 Tabela: `creditos`

Armazena solicitações de crédito dos empreendedores.

### Estrutura SQL

```sql
CREATE TABLE creditos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendedor_id INTEGER NOT NULL,
    valor_solicitado FLOAT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pendente',
    data_solicitacao DATETIME,
    data_aprovacao DATETIME,
    observacoes TEXT,
    FOREIGN KEY (empreendedor_id) REFERENCES empreendedores(id)
);
```

### Campos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `id` | INTEGER | Sim | ID único |
| `empreendedor_id` | INTEGER | Sim | FK para empreendedores |
| `valor_solicitado` | FLOAT | Sim | Valor solicitado em R$ |
| `status` | VARCHAR(50) | Não | Status da solicitação |
| `data_solicitacao` | DATETIME | Não | Data da solicitação |
| `data_aprovacao` | DATETIME | Não | Data da aprovação |
| `observacoes` | TEXT | Não | Observações |

### Valores de Status

- `Pendente` - Aguardando análise
- `Aprovado` - Crédito aprovado
- `Negado` - Crédito negado

---

## ⭐ Tabela: `nps_scores`

Armazena avaliações NPS detalhadas dos empreendedores.

### Estrutura SQL

```sql
CREATE TABLE nps_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendedor_id INTEGER NOT NULL,
    tipo_nps VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL,
    comentario TEXT,
    data_avaliacao DATETIME,
    FOREIGN KEY (empreendedor_id) REFERENCES empreendedores(id)
);
```

### Campos

| Campo | Tipo | Range | Descrição |
|-------|------|-------|-----------|
| `id` | INTEGER | - | ID único |
| `empreendedor_id` | INTEGER | - | FK para empreendedores |
| `tipo_nps` | VARCHAR(50) | - | Tipo de avaliação |
| `score` | INTEGER | 0-10 | Nota (0 a 10) |
| `comentario` | TEXT | - | Comentário opcional |
| `data_avaliacao` | DATETIME | - | Data da avaliação |

### Tipos de NPS

- `geral` - Avaliação geral do programa
- `mentoria` - Avaliação da mentoria
- `ludos` - Avaliação da plataforma Ludos
- `comunidade` - Avaliação da comunidade

### Classificação NPS

- **Detratores**: 0-6
- **Neutros**: 7-8
- **Promotores**: 9-10

---

## 🎓 Tabela: `ludos_atividades`

Armazena atividades dos empreendedores na plataforma de cursos Ludos.

### Estrutura SQL

```sql
CREATE TABLE ludos_atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empreendedor_id INTEGER NOT NULL,
    player_id INTEGER,
    course_id INTEGER,
    course_name VARCHAR(200),
    module_id INTEGER,
    module_name VARCHAR(200),
    activity_id INTEGER,
    activity_name VARCHAR(200),
    performance_first INTEGER,
    performance_best INTEGER,
    total_plays INTEGER DEFAULT 0,
    completed_plays INTEGER DEFAULT 0,
    coins INTEGER DEFAULT 0,
    points_first INTEGER DEFAULT 0,
    points_best INTEGER DEFAULT 0,
    start_date DATETIME,
    end_date DATETIME,
    conclusion_time INTEGER,
    course_published BOOLEAN DEFAULT 0,
    last_visit DATETIME,
    data_atualizacao DATETIME,
    FOREIGN KEY (empreendedor_id) REFERENCES empreendedores(id)
);
```

### Campos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único |
| `empreendedor_id` | INTEGER | FK para empreendedores |
| `player_id` | INTEGER | ID do player no Ludos |
| `course_id` | INTEGER | ID do curso |
| `course_name` | VARCHAR(200) | Nome do curso |
| `module_id` | INTEGER | ID do módulo |
| `module_name` | VARCHAR(200) | Nome do módulo |
| `activity_id` | INTEGER | ID da atividade |
| `activity_name` | VARCHAR(200) | Nome da atividade |
| `performance_first` | INTEGER | Performance na primeira tentativa |
| `performance_best` | INTEGER | Melhor performance |
| `total_plays` | INTEGER | Total de tentativas |
| `completed_plays` | INTEGER | Tentativas completas |
| `coins` | INTEGER | Moedas ganhas |
| `points_first` | INTEGER | Pontos da primeira tentativa |
| `points_best` | INTEGER | Pontos da melhor tentativa |
| `start_date` | DATETIME | Data de início |
| `end_date` | DATETIME | Data de conclusão |
| `conclusion_time` | INTEGER | Tempo de conclusão (segundos) |
| `course_published` | BOOLEAN | Curso está publicado? |
| `last_visit` | DATETIME | Última visita |
| `data_atualizacao` | DATETIME | Data de atualização |

---

## 🔗 Relacionamentos

### Diagrama de Relacionamentos

```
empreendedores (1) ──┬── (N) status_mentoria
                     ├── (N) creditos
                     ├── (N) nps_scores
                     └── (N) ludos_atividades

mentores (1) ────────── (N) status_mentoria
```

### Foreign Keys

- `status_mentoria.empreendedor_id` → `empreendedores.id`
- `status_mentoria.mentor_id` → `mentores.id`
- `creditos.empreendedor_id` → `empreendedores.id`
- `nps_scores.empreendedor_id` → `empreendedores.id`
- `ludos_atividades.empreendedor_id` → `empreendedores.id`

---

## 💻 Exemplos de Inserção

### 1. Inserir Novo Empreendedor (Mínimo)

```sql
INSERT INTO empreendedores (telefone, nome, email, data_inscricao, formulario_tipo)
VALUES (
    '(11) 987654321',
    'João Silva',
    'joao.silva@gmail.com',
    '2025-10-10 12:00:00',
    'Webhook Jotform'
);
```

### 2. Inserir Empreendedor Completo

```sql
INSERT INTO empreendedores (
    telefone, nome, email, cpf, cidade, estado, idade, genero,
    raca_cor, escolaridade, faixa_renda, fonte_renda,
    tempo_funcionamento, segmento_atuacao, organizacao_stone,
    formulario_tipo, data_inscricao
) VALUES (
    '(11) 987654321',
    'Maria Santos',
    'maria@gmail.com',
    '12345678900',
    'São Paulo',
    'SP',
    '25 a 34 anos',
    'Feminino',
    'Parda',
    'Ensino Superior completo',
    'Entre 2 e 3 salários mínimos',
    'Meu próprio negócio formalizado (MEI, ME, etc.)',
    '1 a 3 anos',
    'Tecnologia',
    'Banco Pérola',
    'Webhook Jotform',
    '2025-10-10 14:30:00'
);
```

### 3. Inserir com Python/SQLAlchemy

```python
from data.models import DatabaseManager, Empreendedor
from datetime import datetime

# Criar gerenciador do banco
db_manager = DatabaseManager()

# Criar novo empreendedor
with db_manager.get_session() as session:
    empreendedor = Empreendedor(
        nome="João Silva",
        email="joao@gmail.com",
        telefone="(11) 987654321",
        cpf="12345678900",
        cidade="São Paulo",
        estado="SP",
        idade="25 a 34 anos",
        genero="Masculino",
        raca_cor="Parda",
        escolaridade="Ensino Superior completo",
        faixa_renda="Entre 2 e 3 salários mínimos",
        segmento_atuacao="Tecnologia",
        organizacao_stone="Banco Pérola",
        formulario_tipo="Webhook Jotform",
        data_inscricao=datetime.now()
    )
    
    session.add(empreendedor)
    session.commit()
    
    print(f"Empreendedor criado! ID: {empreendedor.id}")
```

### 4. Inserir via REST API (JSON)

```json
POST /webhook/empreendedor
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@gmail.com",
  "telefone": "(11) 987654321",
  "cpf": "12345678900",
  "cidade": "São Paulo",
  "estado": "SP",
  "idade": "25 a 34 anos",
  "genero": "Masculino",
  "raca_cor": "Parda",
  "escolaridade": "Ensino Superior completo",
  "faixa_renda": "Entre 2 e 3 salários mínimos",
  "fonte_renda": "Meu próprio negócio formalizado (MEI, ME, etc.)",
  "tempo_funcionamento": "1 a 3 anos",
  "segmento_atuacao": "Tecnologia",
  "organizacao_stone": "Banco Pérola",
  "formulario_tipo": "Webhook Jotform"
}
```

---

## 📝 Mapeamento Jotform → Banco

### Campos do Formulário Jotform

Quando receber dados do Jotform neste formato:

```json
{
  "Nome": {
    "first": "SOFIA",
    "last": "RODRIGUES"
  },
  "E-mail": "sofia@gmail.com",
  "Telefone": {
    "area": "54",
    "phone": "996953242"
  },
  "CPF": "12345678900",
  "Cidade": "Florianópolis",
  "Estado": "SC",
  "Idade": "25 a 34 anos",
  "Gênero": "Feminino",
  "Raça/cor": "Branca",
  "Escolaridade": "Ensino Superior completo",
  "Faixa de renda familiar mensal": "Entre 1 e 2 salários mínimos",
  "Quais são as suas fontes de renda atualmente?": [
    "Meu próprio negócio formalizado (MEI, ME, etc.)"
  ],
  "Tempo de funcionamento do negócio": "Menos de 6 meses",
  "Segmento de atuação": "Serviços",
  "Se outros, qual o segmento de atuação do seu négocio?": "",
  "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Banco Pérola"
}
```

### Processamento Necessário

```python
# 1. Processar Nome
nome_completo = f"{data['Nome']['first']} {data['Nome']['last']}"

# 2. Processar Telefone
telefone = f"({data['Telefone']['area']}) {data['Telefone']['phone']}"

# 3. Processar Fontes de Renda (lista → string)
if isinstance(data['Quais são as suas fontes de renda atualmente?'], list):
    fonte_renda = '; '.join(data['Quais são as suas fontes de renda atualmente?'])
else:
    fonte_renda = data['Quais são as suas fontes de renda atualmente?']

# 4. Data de inscrição
data_inscricao = datetime.now()

# 5. Tipo de formulário
formulario_tipo = "Webhook Jotform"
```

---

## ⚠️ Regras Importantes

### 1. Telefones Duplicados

**PROBLEMA**: A tabela tem restrição UNIQUE no campo `telefone`

**SOLUÇÃO**: Adicionar sufixo único para telefones duplicados

```python
# Se telefone já existe no banco
if telefone_existe:
    telefone_unico = telefone[:17] + "_1"  # ou _2, _3...
```

### 2. Campos Obrigatórios

Sempre preencher:
- `telefone` (VARCHAR 20)
- `nome` (VARCHAR 100)

Se não tiver telefone, criar um placeholder:
```python
telefone = f"email_{email[:12]}" if email else f"sem_tel_{timestamp}"
```

### 3. Limites de Tamanho

Sempre truncar strings para o tamanho máximo:

```python
def safe_str(value, max_length):
    if value is None:
        return None
    str_value = str(value).strip()
    if len(str_value) > max_length:
        return str_value[:max_length]
    return str_value if str_value else None
```

### 4. Tipos de Dados

- **DATETIME**: Usar formato ISO `YYYY-MM-DD HH:MM:SS`
- **BOOLEAN**: 0 (False) ou 1 (True)
- **INTEGER**: Números inteiros
- **FLOAT**: Números decimais
- **TEXT**: Sem limite de tamanho

---

## 🔧 Funções Auxiliares Recomendadas

### Python

```python
from datetime import datetime
import pandas as pd

def safe_str(value, max_length):
    """Trunca string no tamanho máximo"""
    if pd.isna(value) or value is None:
        return None
    str_value = str(value).strip()
    return str_value[:max_length] if len(str_value) > max_length else str_value

def parse_jotform_date(date_str):
    """Converte data do Jotform"""
    try:
        return datetime.strptime(date_str, '%b. %d, %Y')
    except:
        return datetime.now()

def processar_telefone_jotform(tel_obj):
    """Processa objeto telefone do Jotform"""
    if isinstance(tel_obj, dict):
        area = tel_obj.get('area', '')
        phone = tel_obj.get('phone', '')
        return f"({area}) {phone}"
    return str(tel_obj)

def processar_nome_jotform(nome_obj):
    """Processa objeto nome do Jotform"""
    if isinstance(nome_obj, dict):
        first = nome_obj.get('first', '')
        last = nome_obj.get('last', '')
        return f"{first} {last}".strip()
    return str(nome_obj)
```

### Node.js

```javascript
function safeStr(value, maxLength) {
  if (!value) return null;
  const str = String(value).trim();
  return str.length > maxLength ? str.substring(0, maxLength) : str;
}

function processarTelefone(telObj) {
  if (typeof telObj === 'object') {
    return `(${telObj.area}) ${telObj.phone}`;
  }
  return String(telObj);
}

function processarNome(nomeObj) {
  if (typeof nomeObj === 'object') {
    return `${nomeObj.first} ${nomeObj.last}`.trim();
  }
  return String(nomeObj);
}
```

---

## 📊 Connection String

### SQLite (Desenvolvimento)

```
sqlite:///data/database.db
```

### Azure SQL Server (Produção)

```
mssql+pyodbc://usuario:senha@servidor.database.windows.net:1433/database?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30
```

Ou via PyODBC puro:

```
DRIVER={ODBC Driver 18 for SQL Server};
SERVER=servidor.database.windows.net;
DATABASE=database;
UID=usuario;
PWD=senha;
Encrypt=yes;
TrustServerCertificate=no;
Connection Timeout=30;
```

---

## 🧪 Exemplo Completo de Inserção via Webhook

```python
# webhook_handler.py
from data.models import DatabaseManager, Empreendedor
from datetime import datetime

def processar_webhook_jotform(payload):
    """
    Processa dados do webhook Jotform e insere no banco
    
    Args:
        payload: Lista ou dict com dados do formulário
    
    Returns:
        dict: Resultado da operação
    """
    
    # Converter para lista se necessário
    registros = payload if isinstance(payload, list) else [payload]
    
    db_manager = DatabaseManager()
    importados = 0
    erros = []
    
    for registro in registros:
        try:
            # Processar campos
            nome = f"{registro['Nome']['first']} {registro['Nome']['last']}"
            email = registro.get('E-mail')
            telefone = f"({registro['Telefone']['area']}) {registro['Telefone']['phone']}"
            
            # Verificar se telefone já existe
            with db_manager.get_session() as session:
                existe = session.query(Empreendedor).filter(
                    Empreendedor.telefone == telefone
                ).first()
                
                # Se existe, adicionar sufixo
                if existe:
                    contador = 1
                    telefone_original = telefone
                    while existe:
                        telefone = f"{telefone_original[:17]}_{contador}"
                        existe = session.query(Empreendedor).filter(
                            Empreendedor.telefone == telefone
                        ).first()
                        contador += 1
                
                # Criar empreendedor
                empreendedor = Empreendedor(
                    nome=nome[:100],
                    email=email[:100] if email else None,
                    telefone=telefone[:20],
                    cpf=registro.get('CPF', '')[:14],
                    cidade=registro.get('Cidade', '')[:100],
                    estado=registro.get('Estado', '')[:50],
                    idade=registro.get('Idade', '')[:20],
                    genero=registro.get('Gênero', '')[:50],
                    raca_cor=registro.get('Raça/cor', '')[:50],
                    escolaridade=registro.get('Escolaridade', '')[:100],
                    faixa_renda=registro.get('Faixa de renda familiar mensal', '')[:100],
                    fonte_renda='; '.join(registro.get('Quais são as suas fontes de renda atualmente?', [])),
                    tempo_funcionamento=registro.get('Tempo de funcionamento do negócio', '')[:50],
                    segmento_atuacao=registro.get('Segmento de atuação', '')[:100],
                    organizacao_stone=registro.get('Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?', '')[:100],
                    formulario_tipo='Webhook Jotform',
                    data_inscricao=datetime.now()
                )
                
                session.add(empreendedor)
                session.commit()
                
                importados += 1
        
        except Exception as e:
            erros.append(str(e))
    
    return {
        'importados': importados,
        'erros': len(erros),
        'detalhes_erros': erros
    }
```

---

## 📞 Consultas Úteis

### Buscar empreendedor por telefone

```sql
SELECT * FROM empreendedores WHERE telefone = '(11) 987654321';
```

### Buscar empreendedor por email

```sql
SELECT * FROM empreendedores WHERE email = 'joao@gmail.com';
```

### Listar empreendedores por fonte

```sql
SELECT formulario_tipo, COUNT(*) as total
FROM empreendedores
GROUP BY formulario_tipo;
```

### Empreendedores com mentoria ativa

```sql
SELECT e.*, m.nome as mentor_nome
FROM empreendedores e
JOIN status_mentoria sm ON e.id = sm.empreendedor_id
JOIN mentores m ON sm.mentor_id = m.id
WHERE sm.status = 'Em andamento';
```

### Total por segmento

```sql
SELECT segmento_atuacao, COUNT(*) as total
FROM empreendedores
WHERE segmento_atuacao IS NOT NULL
GROUP BY segmento_atuacao
ORDER BY total DESC;
```

---

## ✅ Checklist para Backend de Webhook

- [ ] Validar campos obrigatórios (telefone, nome)
- [ ] Processar objeto Nome (first + last)
- [ ] Processar objeto Telefone (area + phone)
- [ ] Processar listas (fontes de renda)
- [ ] Truncar strings para tamanho máximo
- [ ] Tratar telefones duplicados (adicionar sufixo)
- [ ] Usar `formulario_tipo = 'Webhook Jotform'`
- [ ] Definir `data_inscricao = datetime.now()`
- [ ] Fazer commit após inserção
- [ ] Retornar resposta JSON com status
- [ ] Logar todas as operações
- [ ] Tratar erros e fazer rollback se necessário

---

## 🔒 Segurança

### Validações Recomendadas

1. **Validar formato de email**
2. **Validar formato de CPF**
3. **Sanitizar entradas** (prevenir SQL injection)
4. **Limitar tamanho** do payload
5. **Autenticar** requisições (token/API key)
6. **Rate limiting** para prevenir abuso

---

## 📚 Referências

- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **PyODBC**: https://github.com/mkleehammer/pyodbc
- **Jotform API**: https://api.jotform.com/docs/

---

**Última atualização**: 10/10/2025

