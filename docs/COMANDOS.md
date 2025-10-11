# 💻 Comandos Úteis - Dashboard Impulso Stone

Referência rápida de comandos para trabalhar com a API.

---

## 🔧 Ambiente Virtual

### Criar
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### Ativar
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Desativar
```bash
deactivate
```

---

## 📦 Dependências

### Instalar
```bash
pip install -r requirements.txt
```

### Atualizar pip
```bash
pip install --upgrade pip
```

### Ver instaladas
```bash
pip list
```

### Gerar requirements.txt
```bash
pip freeze > requirements.txt
```

---

## 🗄️ Banco de Dados

### Testar Conexão
```bash
python scripts/test_connection.py
```

### Inicializar Tabelas
```bash
python scripts/init_database.py
```

---

## 🚀 Executar API

### Desenvolvimento (com reload)
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Produção
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Porta Customizada
```bash
python -m uvicorn app.main:app --reload --port 8080
```

### Com Logs Detalhados
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

---

## 🧪 Testes

### Script de Testes Automatizado
```bash
python test_webhook.py
```

### Exemplos de Uso
```bash
python exemplos_uso.py
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Enviar Webhook
```bash
curl -X POST http://localhost:8000/api/v1/webhook/jotform \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

### Buscar Empreendedores
```bash
curl -X POST http://localhost:8000/api/v1/webhook/empreendedores/search \
  -H "Content-Type: application/json" \
  -d '{"estado":"SP","page":1,"page_size":10}'
```

### Obter Estatísticas
```bash
curl http://localhost:8000/api/v1/webhook/empreendedores/stats
```

---

## 📊 URLs Importantes

### Locais
- API: http://localhost:8000
- Docs (Swagger): http://localhost:8000/docs
- Docs (ReDoc): http://localhost:8000/redoc
- Health Check: http://localhost:8000/health
- Webhook Health: http://localhost:8000/api/v1/webhook/health

### Endpoints Webhook
- POST /api/v1/webhook/jotform
- POST /api/v1/webhook/jotform/bulk
- POST /api/v1/webhook/jotform/raw
- GET /api/v1/webhook/empreendedores/{id}
- POST /api/v1/webhook/empreendedores/search
- PUT /api/v1/webhook/empreendedores/{id}
- DELETE /api/v1/webhook/empreendedores/{id}
- GET /api/v1/webhook/empreendedores/stats

---

## 🐛 Debug

### Ver Portas em Uso
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### Matar Processo em Porta
```bash
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

### Ver Logs em Tempo Real
```bash
# API já mostra logs no terminal
# Para salvar em arquivo:
python -m uvicorn app.main:app --reload 2>&1 | tee api.log
```

---

## 🔐 Git

### Status
```bash
git status
```

### Adicionar Arquivos
```bash
git add .
```

### Commit
```bash
git commit -m "Mensagem do commit"
```

### Push
```bash
git push origin main
```

### Ver Histórico
```bash
git log --oneline
```

---

## 🔍 Verificações

### Verificar Python
```bash
python --version
# ou
python3 --version
```

### Verificar ODBC Driver
```bash
odbcinst -q -d
# Deve mostrar: ODBC Driver 18 for SQL Server
```

### Verificar Variáveis de Ambiente
```bash
# Windows
type .env

# Linux/Mac
cat .env
```

---

## 📝 Editar Arquivos

### Editar .env
```bash
# Windows
notepad .env

# Linux/Mac
nano .env
# ou
vim .env
```

### Editar código
```bash
code .  # Visual Studio Code
```

---

## 🧹 Limpeza

### Limpar cache Python
```bash
# Windows
rmdir /s /q __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +

# Linux/Mac
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### Remover ambiente virtual
```bash
# Desativar primeiro
deactivate

# Depois remover
# Windows
rmdir /s /q venv

# Linux/Mac
rm -rf venv
```

---

## 📦 Build/Deploy

### Gerar requirements
```bash
pip freeze > requirements.txt
```

### Verificar imports
```bash
python -m py_compile app/main.py
```

### Rodar testes antes de deploy
```bash
python test_webhook.py
python scripts/test_connection.py
```

---

## 🎯 Atalhos Úteis

### Tudo de uma vez (fresh start)
```bash
# Windows
python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python scripts/test_connection.py && python scripts/init_database.py && python -m uvicorn app.main:app --reload

# Linux/Mac
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python scripts/test_connection.py && python scripts/init_database.py && python -m uvicorn app.main:app --reload
```

### Reiniciar API
```bash
# Ctrl+C para parar
# Depois:
python -m uvicorn app.main:app --reload
```

---

**Última atualização:** 10/10/2025

