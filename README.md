# 🚀 Dashboard Impulso Stone - API de Webhook

API completa para receber e processar dados de empreendedores do formulário Jotform e integrá-los ao Dashboard Impulso Stone.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Características](#características)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Testes](#testes)
- [Documentação Completa](#documentação-completa)

---

## 🎯 Visão Geral

Esta API fornece endpoints para:

- ✅ Receber webhooks do Jotform com dados de empreendedores
- ✅ Validar e processar dados automaticamente
- ✅ Armazenar no Azure SQL Server
- ✅ Buscar, atualizar e deletar empreendedores
- ✅ Gerar estatísticas e relatórios

## ✨ Características

- **FastAPI**: Framework moderno e rápido
- **SQLAlchemy**: ORM robusto para manipulação de dados
- **Pydantic**: Validação automática de dados
- **Azure SQL Server**: Banco de dados escalável
- **Documentação Automática**: Swagger UI e ReDoc
- **Logs Detalhados**: Rastreamento completo de operações
- **Tratamento de Duplicatas**: Gerenciamento inteligente de telefones duplicados

## 🛠 Tecnologias

- Python 3.10+
- FastAPI 0.104+
- SQLAlchemy 2.0+
- Pydantic 2.5+
- Azure SQL Server
- pyodbc 5.0+

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone <repository-url>
cd stone-webhook-data
```

### 2. Criar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar ODBC Driver (se necessário)

**Windows:**
- Baixe e instale: [ODBC Driver 18 for SQL Server](https://docs.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)

**Linux:**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

## ⚙️ Configuração

### 1. Criar arquivo .env

Copie o `.env.example` e configure suas credenciais:

```bash
cp .env.example .env
```

### 2. Configurar variáveis de ambiente

Edite o arquivo `.env`:

```env
# SQL Server (Azure)
SQL_SERVER=seu-servidor.database.windows.net
SQL_DATABASE=dashboardImpulso
SQL_USERNAME=seu_usuario
SQL_PASSWORD=sua_senha
SQL_DRIVER=ODBC Driver 18 for SQL Server

# Aplicação
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 3. Testar conexão com banco

```bash
python scripts/test_connection.py
```

### 4. Inicializar banco de dados

```bash
python scripts/init_database.py
```

## 🚀 Uso

### Iniciar o servidor

```bash
# Desenvolvimento (com reload automático)
python -m uvicorn app.main:app --reload --port 8000

# Produção
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Acessar a API

- **API Base**: http://localhost:8000
- **Documentação Interativa (Swagger)**: http://localhost:8000/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/webhook/health

## 📡 API Endpoints

### Webhook

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/webhook/jotform` | Receber webhook do Jotform (único) |
| POST | `/api/v1/webhook/jotform/bulk` | Receber múltiplos webhooks |
| POST | `/api/v1/webhook/jotform/raw` | Receber webhook raw (qualquer estrutura) |

### Empreendedores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/webhook/empreendedores/{id}` | Buscar por ID |
| POST | `/api/v1/webhook/empreendedores/search` | Buscar com filtros |
| PUT | `/api/v1/webhook/empreendedores/{id}` | Atualizar |
| DELETE | `/api/v1/webhook/empreendedores/{id}` | Deletar |
| GET | `/api/v1/webhook/empreendedores/stats` | Obter estatísticas |

### Sistema

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/webhook/health` | Health check do webhook |
| GET | `/health` | Health check geral da aplicação |

## 🧪 Testes

### Executar testes automatizados

```bash
python test_webhook.py
```

### Testar com cURL

```bash
# Health check
curl http://localhost:8000/api/v1/webhook/health

# Enviar webhook
curl -X POST http://localhost:8000/api/v1/webhook/jotform \
  -H "Content-Type: application/json" \
  -d @test_payload.json

# Obter estatísticas
curl http://localhost:8000/api/v1/webhook/empreendedores/stats
```

### Testar com Postman/Insomnia

1. Importe a coleção de endpoints disponível em `/docs`
2. Configure a base URL: `http://localhost:8000`
3. Execute os requests de exemplo

## 📚 Documentação Completa

Para documentação detalhada, consulte:

- **[WEBHOOK_API.md](WEBHOOK_API.md)**: Documentação completa da API
- **[modelsdata.md](modelsdata.md)**: Estrutura do banco de dados
- **Swagger UI**: http://localhost:8000/docs (quando servidor estiver rodando)

## 🗂 Estrutura do Projeto

```
stone-webhook-data/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   └── webhook.py          # Endpoints do webhook
│   ├── core/
│   │   ├── config.py           # Configurações
│   │   └── dependencies.py
│   ├── data/
│   │   ├── empreendedor_repository.py  # Repository
│   │   ├── mongo_repository.py
│   │   └── sql_repository.py
│   ├── dto/
│   │   ├── requests.py
│   │   ├── responses.py
│   │   └── webhook_dtos.py     # DTOs do webhook
│   ├── models/
│   │   ├── domain.py
│   │   └── impulso_models.py   # Modelos SQLAlchemy
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── analysis_service.py
│   │   └── user_service.py
│   ├── utils/
│   │   └── jotform_processor.py  # Processador do Jotform
│   └── main.py                 # Aplicação principal
├── scripts/
│   ├── init_database.py        # Inicializar banco
│   └── test_connection.py      # Testar conexão
├── tests/
├── .env.example                # Exemplo de configuração
├── requirements.txt            # Dependências
├── test_webhook.py             # Script de testes
├── test_payload.json           # Payload de exemplo
├── README.md                   # Este arquivo
├── WEBHOOK_API.md              # Documentação da API
└── modelsdata.md               # Estrutura do banco
```

## 🔧 Configuração do Jotform

Para configurar o webhook no Jotform:

1. Acesse seu formulário no Jotform
2. Vá em **Settings** → **Integrations**
3. Procure por **Webhooks**
4. Configure a URL: `https://seu-dominio.com/api/v1/webhook/jotform`
5. Teste enviando um formulário

## 📊 Monitoramento

### Logs

A aplicação gera logs detalhados:

```log
2025-10-10 12:30:00 - INFO - Webhook Jotform recebido
2025-10-10 12:30:00 - INFO - Empreendedor criado: ID=123
2025-10-10 12:30:00 - INFO - Tempo de processamento: 45.23ms
```

### Métricas

Acesse as estatísticas em:
```bash
GET /api/v1/webhook/empreendedores/stats
```

## 🛡 Segurança

- ✅ Validação de dados com Pydantic
- ✅ Proteção contra SQL Injection (SQLAlchemy ORM)
- ✅ Conexão segura com banco (TLS/SSL)
- ✅ Logs sem dados sensíveis
- ✅ Rate limiting (configurável)
- ✅ CORS configurável

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -am 'Adiciona nova feature'`
4. Push: `git push origin feature/nova-feature`
5. Abra um Pull Request

## 📝 Licença

© 2025 Dashboard Impulso Stone. Todos os direitos reservados.

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique a [documentação completa](WEBHOOK_API.md)
2. Consulte os logs da aplicação
3. Execute o health check
4. Teste a conexão com o banco

---

**Última atualização**: 10/10/2025

**Versão**: 1.0.0
