# ⚡ Início Rápido - Dashboard Impulso Stone

Guia rápido para rodar a API em 5 minutos!

---

## 🚀 Instalação Rápida

### 1️⃣ Criar e Ativar Ambiente Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar Banco de Dados

Edite o arquivo `.env` com suas credenciais do Azure SQL:

```env
SQL_SERVER=dev-free-helper.database.windows.net
SQL_DATABASE=dashboardImpulso
SQL_USERNAME=usr_free_helper
SQL_PASSWORD=23@3ryR2
```

### 4️⃣ Testar Conexão

```bash
python scripts/test_connection.py
```

### 5️⃣ Inicializar Tabelas

```bash
python scripts/init_database.py
```

### 6️⃣ Executar API

```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 7️⃣ Acessar

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

---

## 🧪 Testar

```bash
# Em outro terminal (com venv ativado)
python test_webhook.py
```

---

## 📡 Enviar Webhook

```bash
curl -X POST http://localhost:8000/api/v1/webhook/jotform \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

Ou use o Swagger em http://localhost:8000/docs

---

## 📊 Obter Estatísticas

```bash
curl http://localhost:8000/api/v1/webhook/empreendedores/stats
```

---

## ❓ Problemas?

Consulte o [Guia Completo de Instalação](INSTALACAO.md)

---

✅ **Pronto! Sua API está rodando!** 🎉

