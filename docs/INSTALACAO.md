# 🚀 Guia de Instalação - Dashboard Impulso Stone

Guia completo para configurar o ambiente e executar a API de Webhook.

---

## 📋 Pré-requisitos

### 1. Python
- **Versão**: Python 3.10 ou superior
- **Download**: https://www.python.org/downloads/

Verificar instalação:
```bash
python --version
# ou
python3 --version
```

### 2. ODBC Driver para SQL Server

#### Windows
1. Baixar: [ODBC Driver 18 for SQL Server](https://go.microsoft.com/fwlink/?linkid=2223304)
2. Executar o instalador
3. Seguir o assistente de instalação

#### Linux (Ubuntu/Debian)
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
```

#### macOS
```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql18
```

Verificar instalação:
```bash
odbcinst -q -d
# Deve mostrar: [ODBC Driver 18 for SQL Server]
```

### 3. Git (opcional)
- **Download**: https://git-scm.com/downloads

---

## 🔧 Instalação Passo a Passo

### Passo 1: Clonar ou Baixar o Projeto

```bash
# Se usar Git
git clone <url-do-repositorio>
cd stone-webhook-data

# Ou descompacte o arquivo ZIP e entre na pasta
```

### Passo 2: Criar Ambiente Virtual

**Windows:**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Confirmar ativação (prompt deve mostrar (venv))
```

**Linux/macOS:**
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Confirmar ativação (prompt deve mostrar (venv))
```

### Passo 3: Instalar Dependências

```bash
# Com ambiente virtual ativado
pip install --upgrade pip
pip install -r requirements.txt
```

Aguarde a instalação (pode levar alguns minutos).

### Passo 4: Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar o arquivo .env com suas credenciais
```

**No Windows:**
```bash
notepad .env
```

**No Linux/macOS:**
```bash
nano .env
# ou
vim .env
```

Preencha as credenciais do Azure SQL Server:
```env
SQL_SERVER=seu-servidor.database.windows.net
SQL_DATABASE=dashboardImpulso
SQL_USERNAME=seu_usuario
SQL_PASSWORD=sua_senha
```

### Passo 5: Testar Conexão com Banco

```bash
python scripts/test_connection.py
```

**Saída esperada:**
```
✅ Conexão estabelecida com sucesso!
Versão do SQL Server: ...
Database atual: dashboardImpulso
```

**Se houver erro:**
- Verifique as credenciais no `.env`
- Verifique se seu IP está liberado no firewall do Azure
- Verifique se o driver ODBC está instalado

### Passo 6: Inicializar Banco de Dados

```bash
python scripts/init_database.py
```

**Saída esperada:**
```
✓ Tabelas criadas/verificadas com sucesso!
✓ Conexão com banco verificada!
  Total de empreendedores: 0

Tabelas criadas:
  - empreendedores
  - mentores
  - status_mentoria
  - creditos
  - nps_scores
  - ludos_atividades

✅ Banco de dados inicializado com sucesso!
```

### Passo 7: Executar a API

```bash
# Modo desenvolvimento (com reload automático)
python -m uvicorn app.main:app --reload --port 8000
```

**Saída esperada:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
🚀 Iniciando Dashboard Impulso Stone API...
✅ Conectado ao banco - 0 empreendedores cadastrados
✅ API iniciada com sucesso!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Passo 8: Verificar Funcionamento

Abra o navegador em:
- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🧪 Testar a API

### Teste Rápido (Browser)

1. Abra: http://localhost:8000/health
2. Deve mostrar:
```json
{
  "status": "healthy",
  "api": "Dashboard Impulso Stone",
  "database": "connected",
  "total_empreendedores": 0
}
```

### Teste Completo (Script)

```bash
# Em outro terminal (com venv ativado)
python test_webhook.py
```

### Teste com Payload de Exemplo

```bash
curl -X POST http://localhost:8000/api/v1/webhook/jotform \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

---

## 📂 Estrutura de Diretórios

```
stone-webhook-data/
├── venv/                    # Ambiente virtual (não commitado)
├── app/                     # Código da aplicação
│   ├── api/                # Endpoints
│   ├── core/               # Configurações
│   ├── data/               # Repositories
│   ├── dto/                # Data Transfer Objects
│   ├── models/             # Modelos do banco
│   ├── utils/              # Utilitários
│   └── main.py            # Aplicação principal
├── scripts/                # Scripts auxiliares
├── .env                    # Configurações (NÃO commitado)
├── .env.example            # Exemplo de configurações
├── requirements.txt        # Dependências
└── README.md              # Documentação
```

---

## ⚙️ Comandos Úteis

### Ativar/Desativar Ambiente Virtual

**Ativar:**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

**Desativar:**
```bash
deactivate
```

### Executar API

**Desenvolvimento:**
```bash
python -m uvicorn app.main:app --reload --port 8000
```

**Produção:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Ver Logs

```bash
# Logs aparecem no terminal onde a API está rodando
# Para salvar em arquivo, use:
python -m uvicorn app.main:app --reload --log-config logging.conf
```

---

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError"
**Causa:** Ambiente virtual não está ativado ou dependências não instaladas

**Solução:**
```bash
# Ativar ambiente virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "ODBC Driver not found"
**Causa:** Driver ODBC não está instalado

**Solução:**
- Baixe e instale o driver (ver Pré-requisitos)
- Reinicie o terminal após instalação

### Erro: "Connection failed"
**Causa:** Credenciais incorretas ou firewall bloqueando

**Solução:**
1. Verifique credenciais no `.env`
2. No Azure Portal:
   - Vá em SQL Server → Firewalls and virtual networks
   - Adicione seu IP público
3. Teste novamente: `python scripts/test_connection.py`

### Erro: "Port 8000 already in use"
**Causa:** Porta 8000 já está sendo usada

**Solução:**
```bash
# Use outra porta
python -m uvicorn app.main:app --reload --port 8001

# Ou mate o processo na porta 8000
# Windows: netstat -ano | findstr :8000
# Linux/macOS: lsof -ti:8000 | xargs kill
```

### API não está acessível de outros computadores
**Causa:** API está escutando apenas em localhost

**Solução:**
```bash
# Iniciar com host 0.0.0.0
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🎓 Próximos Passos

Após instalar e testar:

1. ✅ Leia a [documentação da API](WEBHOOK_API.md)
2. ✅ Configure o webhook no Jotform
3. ✅ Teste enviando um formulário
4. ✅ Explore os [exemplos de uso](exemplos_uso.py)
5. ✅ Configure para produção

---

## 📞 Suporte

Se encontrar problemas:

1. ✅ Verifique os logs da aplicação
2. ✅ Execute `python scripts/test_connection.py`
3. ✅ Consulte a seção Solução de Problemas
4. ✅ Veja a documentação completa

---

**Última atualização:** 10/10/2025

