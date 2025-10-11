# 📡 API de Webhook - Jotform para Dashboard Impulso Stone

Documentação completa da API de webhook para receber e processar dados de empreendedores do formulário Jotform.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Endpoints Disponíveis](#endpoints-disponíveis)
4. [Exemplos de Uso](#exemplos-de-uso)
5. [Estrutura de Dados](#estrutura-de-dados)
6. [Tratamento de Erros](#tratamento-de-erros)
7. [Testes](#testes)

---

## 🎯 Visão Geral

Esta API fornece endpoints para:

- ✅ Receber webhooks do Jotform (formulário de empreendedores)
- ✅ Processar e validar dados recebidos
- ✅ Inserir dados no banco SQL Server (Azure)
- ✅ Buscar, atualizar e deletar empreendedores
- ✅ Obter estatísticas gerais

### Tecnologias Utilizadas

- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **Banco de Dados**: Azure SQL Server
- **Validação**: Pydantic
- **Python**: 3.10+

---

## 🚀 Instalação e Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

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
API_V1_STR=/api/v1
```

### 3. Criar Tabelas no Banco

As tabelas são criadas automaticamente na primeira execução. Mas você também pode executar:

```python
from app.data.empreendedor_repository import EmpreendedorRepository

repo = EmpreendedorRepository()
# As tabelas são criadas automaticamente no __init__
```

### 4. Executar a API

```bash
# Desenvolvimento
python -m uvicorn app.main:app --reload --port 8000

# Produção
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Acessar Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 Endpoints Disponíveis

### 1. Receber Webhook do Jotform (Único)

```http
POST /api/v1/webhook/jotform
Content-Type: application/json
```

**Payload Exemplo:**

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
  "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Banco Pérola"
}
```

**Resposta de Sucesso (201):**

```json
{
  "success": true,
  "message": "Empreendedor cadastrado com sucesso",
  "empreendedor_id": 123,
  "data": {
    "id": 123,
    "nome": "SOFIA RODRIGUES",
    "telefone": "(54) 996953242",
    "email": "sofia@gmail.com",
    "cpf": "12345678900",
    "cidade": "Florianópolis",
    "estado": "SC",
    "data_inscricao": "2025-10-10T12:30:00",
    "formulario_tipo": "Webhook Jotform"
  }
}
```

---

### 2. Receber Webhook em Lote (Bulk)

```http
POST /api/v1/webhook/jotform/bulk
Content-Type: application/json
```

**Payload**: Array de objetos (mesmo formato do endpoint único)

**Resposta:**

```json
{
  "success": true,
  "total_processados": 10,
  "total_sucesso": 9,
  "total_erros": 1,
  "resultados": [
    {
      "success": true,
      "message": "Registro 1: Sucesso",
      "empreendedor_id": 123,
      "data": { ... }
    },
    ...
  ],
  "tempo_processamento_ms": 523.45
}
```

---

### 3. Receber Webhook Raw (Qualquer Estrutura)

```http
POST /api/v1/webhook/jotform/raw
Content-Type: application/json
```

Aceita qualquer estrutura JSON e tenta processar. Útil para debugging.

---

### 4. Buscar Empreendedor por ID

```http
GET /api/v1/webhook/empreendedores/{id}
```

**Resposta:**

```json
{
  "id": 123,
  "nome": "SOFIA RODRIGUES",
  "telefone": "(54) 996953242",
  "email": "sofia@gmail.com",
  "cpf": "12345678900",
  "cidade": "Florianópolis",
  "estado": "SC",
  "data_inscricao": "2025-10-10T12:30:00",
  "formulario_tipo": "Webhook Jotform"
}
```

---

### 5. Buscar Empreendedores com Filtros

```http
POST /api/v1/webhook/empreendedores/search
Content-Type: application/json
```

**Payload:**

```json
{
  "nome": "Sofia",
  "estado": "SC",
  "ativo_na_ludos": true,
  "page": 1,
  "page_size": 20
}
```

**Filtros Disponíveis:**
- `nome`, `telefone`, `email`, `cpf`
- `cidade`, `estado`
- `comunidade_originadora`, `formulario_tipo`
- `data_inscricao_inicio`, `data_inscricao_fim`
- `ativo_na_ludos`, `fazendo_mentoria`
- `page`, `page_size` (paginação)

**Resposta:**

```json
{
  "success": true,
  "total": 45,
  "page": 1,
  "page_size": 20,
  "total_pages": 3,
  "data": [ ... ]
}
```

---

### 6. Atualizar Empreendedor

```http
PUT /api/v1/webhook/empreendedores/{id}
Content-Type: application/json
```

**Payload:**

```json
{
  "nome": "Sofia Rodrigues Silva",
  "telefone": "(54) 999999999",
  "email": "novo.email@gmail.com",
  "ativo_na_ludos": true,
  "nps_geral": 9
}
```

---

### 7. Deletar Empreendedor

```http
DELETE /api/v1/webhook/empreendedores/{id}
```

⚠️ **ATENÇÃO**: Esta operação não pode ser desfeita!

---

### 8. Obter Estatísticas

```http
GET /api/v1/webhook/empreendedores/stats
```

**Resposta:**

```json
{
  "total_empreendedores": 1250,
  "total_por_comunidade": {
    "Impulso Stone": 800,
    "Banco Pérola": 450
  },
  "total_por_estado": {
    "SP": 500,
    "SC": 300,
    "RJ": 250,
    ...
  },
  "total_por_segmento": {
    "Tecnologia": 400,
    "Serviços": 350,
    "Alimentação": 300,
    ...
  },
  "total_ativos_ludos": 450,
  "total_em_mentoria": 320,
  "media_nps_geral": 8.5,
  "media_nps_mentoria": 9.1,
  "media_nps_ludos": 8.2
}
```

---

### 9. Health Check

```http
GET /api/v1/webhook/health
```

**Resposta:**

```json
{
  "status": "healthy",
  "service": "webhook-jotform",
  "timestamp": "2025-10-10T12:30:00.000Z",
  "database": "connected",
  "total_empreendedores": 1250
}
```

---

## 💡 Exemplos de Uso

### Python (requests)

```python
import requests

# 1. Enviar webhook
payload = {
    "Nome": {"first": "João", "last": "Silva"},
    "Telefone": {"area": "11", "phone": "987654321"},
    "E-mail": "joao@gmail.com",
    "CPF": "12345678900",
    "Cidade": "São Paulo",
    "Estado": "SP"
}

response = requests.post(
    "http://localhost:8000/api/v1/webhook/jotform",
    json=payload
)

print(response.json())

# 2. Buscar por CPF
search_payload = {
    "cpf": "12345678900",
    "page": 1,
    "page_size": 10
}

response = requests.post(
    "http://localhost:8000/api/v1/webhook/empreendedores/search",
    json=search_payload
)

empreendedores = response.json()["data"]
print(f"Encontrados: {len(empreendedores)}")
```

### cURL

```bash
# Enviar webhook
curl -X POST http://localhost:8000/api/v1/webhook/jotform \
  -H "Content-Type: application/json" \
  -d '{
    "Nome": {"first": "João", "last": "Silva"},
    "Telefone": {"area": "11", "phone": "987654321"},
    "E-mail": "joao@gmail.com"
  }'

# Obter estatísticas
curl http://localhost:8000/api/v1/webhook/empreendedores/stats

# Health check
curl http://localhost:8000/api/v1/webhook/health
```

### JavaScript (Fetch)

```javascript
// Enviar webhook
const payload = {
  Nome: { first: "João", last: "Silva" },
  Telefone: { area: "11", phone: "987654321" },
  "E-mail": "joao@gmail.com"
};

fetch("http://localhost:8000/api/v1/webhook/jotform", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
})
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

---

## 📊 Estrutura de Dados

### Campos da Tabela `empreendedores`

#### Obrigatórios
- `telefone` (VARCHAR 20) - Telefone do empreendedor
- `nome` (VARCHAR 100) - Nome completo

#### Principais
- `email` (VARCHAR 100)
- `cpf` (VARCHAR 14)
- `cidade` (VARCHAR 100)
- `estado` (VARCHAR 50)
- `data_inscricao` (DATETIME)

#### Demográficos
- `idade`, `genero`, `raca_cor`, `escolaridade`

#### Socioeconômicos
- `faixa_renda`, `fonte_renda`

#### Negócio
- `tempo_funcionamento`, `segmento_atuacao`, `organizacao_stone`

#### Ludos (Plataforma de Cursos)
- `ludos_id`, `ludos_login`, `ludos_status`
- `ludos_pontos`, `ludos_moedas`, `ludos_nivel`
- `ludos_primeiro_login`, `ludos_ultimo_login`

#### MGM (WhatsApp)
- `mgm_user_name`, `mgm_whatsapp`
- `mgm_total_mensagens`, `mgm_total_reacoes`, `mgm_total_interacoes`
- `mgm_engajamento_percent`

#### Status Flags
- `esta_na_comunidade`, `esta_no_grupo_mentoria`, `esta_no_papo_impulso`
- `ativo_na_ludos`, `fazendo_mentoria`, `solicitou_credito`

#### NPS
- `nps_geral`, `nps_mentoria`, `nps_ludos` (0-10)

---

## ⚠️ Tratamento de Erros

### Códigos de Status HTTP

| Código | Descrição | Quando Ocorre |
|--------|-----------|---------------|
| 200 | OK | Operação bem-sucedida (GET, PUT) |
| 201 | Created | Empreendedor criado com sucesso |
| 400 | Bad Request | Payload inválido ou campos obrigatórios ausentes |
| 404 | Not Found | Empreendedor não encontrado |
| 500 | Internal Server Error | Erro no servidor ou banco de dados |
| 503 | Service Unavailable | Serviço indisponível (health check falhou) |

### Estrutura de Resposta de Erro

```json
{
  "success": false,
  "message": "Descrição do erro",
  "errors": [
    "Detalhes específicos do erro"
  ]
}
```

### Tratamento de Telefones Duplicados

O sistema **PERMITE** telefones duplicados automaticamente adicionando sufixo:

```
Telefone original: (11) 987654321
Se existir: (11) 987654321_1
Se ainda existir: (11) 987654321_2
...
```

---

## 🧪 Testes

### Testar Localmente

1. **Iniciar servidor:**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

2. **Acessar Swagger UI:**
```
http://localhost:8000/docs
```

3. **Testar endpoint de health check:**
```bash
curl http://localhost:8000/api/v1/webhook/health
```

4. **Enviar webhook de teste:**
```bash
curl -X POST http://localhost:8000/api/v1/webhook/jotform \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

### Configurar Webhook no Jotform

1. Acesse seu formulário no Jotform
2. Vá em **Settings** → **Integrations** → **Webhooks**
3. Configure a URL do webhook:
   ```
   https://seu-dominio.com/api/v1/webhook/jotform
   ```
4. Teste o webhook enviando um formulário

---

## 📝 Logs

A API gera logs detalhados de todas as operações:

```log
2025-10-10 12:30:00 - app.api.webhook - INFO - Webhook Jotform recebido
2025-10-10 12:30:00 - app.data.empreendedor_repository - INFO - Empreendedor criado: ID=123, Nome=SOFIA RODRIGUES
2025-10-10 12:30:00 - app.api.webhook - INFO - Empreendedor criado com sucesso: ID=123, Tempo=45.23ms
```

---

## 🔒 Segurança

### Recomendações

1. **HTTPS**: Use sempre HTTPS em produção
2. **Autenticação**: Adicione autenticação por token nos endpoints sensíveis
3. **Rate Limiting**: Configure limites de requisições
4. **Validação**: Todos os dados são validados com Pydantic
5. **SQL Injection**: Proteção via SQLAlchemy ORM
6. **Logs**: Não logamos dados sensíveis (senhas, tokens)

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs da aplicação
2. Teste o health check: `/api/v1/webhook/health`
3. Consulte a documentação interativa: `/docs`
4. Veja exemplos em `modelsdata.md`

---

## 📄 Licença

© 2025 Dashboard Impulso Stone. Todos os direitos reservados.

---

**Última atualização**: 10/10/2025

