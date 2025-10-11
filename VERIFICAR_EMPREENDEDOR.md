# 🔍 Guia: Verificar Empreendedor no Banco

Script interativo para consultar empreendedores cadastrados no banco de dados.

---

## 🚀 Como Usar

### 1. Executar o Script

```bash
# Com ambiente virtual ativado
python scripts/verificar_empreendedor.py
```

### 2. Menu Interativo

```
================================================================================
            🔍 VERIFICAR EMPREENDEDOR NO BANCO DE DADOS
================================================================================

Conectando ao banco de dados...
✅ Conectado com sucesso!

────────────────────────────────────────────────────────────────────────────────
Escolha uma opção:

  1 - Buscar por ID
  2 - Buscar por Telefone
  3 - Buscar por Email
  4 - Buscar por CPF
  5 - Buscar por Nome
  6 - Listar Últimos Cadastrados
  0 - Sair
────────────────────────────────────────────────────────────────────────────────

Digite a opção:
```

---

## 📋 Opções Disponíveis

### 1️⃣ Buscar por ID
Busca exata por ID do empreendedor.

**Exemplo:**
```
Digite o ID do empreendedor: 1754
```

### 2️⃣ Buscar por Telefone
Busca exata por telefone.

**Exemplo:**
```
Digite o telefone: (45) 3353535353
```

### 3️⃣ Buscar por Email
Busca exata por email.

**Exemplo:**
```
Digite o email: louiteste@gmail.com
```

### 4️⃣ Buscar por CPF
Busca exata por CPF.

**Exemplo:**
```
Digite o CPF: 535353453453
```

### 5️⃣ Buscar por Nome
Busca parcial por nome (retorna todos que contenham o texto).

**Exemplo:**
```
Digite o nome: louigi
```
Retorna: "louigi teste", "Maria Louigi", etc.

### 6️⃣ Listar Últimos Cadastrados
Lista os N empreendedores mais recentes.

**Exemplo:**
```
Quantos deseja ver? (padrão 5): 10
```

---

## 📊 Informações Exibidas

Quando um empreendedor é encontrado, o script mostra:

```
────────────────────────────────────────────────────────────────────────────────
EMPREENDEDOR ENCONTRADO
────────────────────────────────────────────────────────────────────────────────

📋 DADOS PRINCIPAIS
ID                            : 1754
Nome                          : louigi teste
Telefone                      : (45) 3353535353
Email                         : louiteste@gmail.com
CPF                           : 535353453453

📍 LOCALIZAÇÃO
Cidade                        : floripa
Estado                        : sc

👤 DADOS DEMOGRÁFICOS
Idade                         : Ensino Superior comp
Gênero                        : Masculino
Raça/Cor                      : Amarela
Escolaridade                  : Não informado

💰 DADOS SOCIOECONÔMICOS
Faixa de Renda               : Não informado
Fonte de Renda               : Aposentadoria ou pensão

🏢 NEGÓCIO
Tempo de Funcionamento       : Menos de 6 meses
Segmento de Atuação          : Tecnologia
Segmento (Outros)            : tech
Organização Stone            : Freehelper

📊 STATUS
Na Comunidade                : ❌ Não
Ativo na Ludos               : ❌ Não
Fazendo Mentoria             : ❌ Não
Solicitou Crédito            : ❌ Não

📅 METADADOS
Comunidade Originadora       : Impulso Stone
Tipo de Formulário           : Webhook Jotform
Data de Inscrição            : 10/10/2025 20:12:09

────────────────────────────────────────────────────────────────────────────────
```

---

## 💡 Exemplos de Uso

### Verificar se o webhook funcionou
```bash
python scripts/verificar_empreendedor.py
# Opção 6 - Listar Últimos Cadastrados
# Ver se o último cadastro é do webhook que acabou de enviar
```

### Buscar por telefone específico
```bash
python scripts/verificar_empreendedor.py
# Opção 2 - Buscar por Telefone
# Digite: (45) 3353535353
```

### Ver todos com nome "teste"
```bash
python scripts/verificar_empreendedor.py
# Opção 5 - Buscar por Nome
# Digite: teste
# Mostra: louigi teste, mario teste, jack teste, etc.
```

---

## ⚠️ Troubleshooting

### Erro de conexão
```
❌ Erro ao conectar ao banco: ...
```
**Solução:** Verifique o `.env` e conexão com Azure SQL

### Nenhum resultado
```
❌ Empreendedor não encontrado
```
**Possíveis causas:**
- ID/telefone/email incorreto
- Empreendedor não foi cadastrado
- Busca é case-sensitive (tente variações)

---

## 🎨 Recursos do Script

- ✅ Interface colorida e amigável
- ✅ Menu interativo
- ✅ Múltiplos tipos de busca
- ✅ Exibição completa de todos os dados
- ✅ Suporte a buscas parciais (nome)
- ✅ Lista múltiplos resultados
- ✅ Mostra status e flags booleanas
- ✅ Formatação de datas
- ✅ Tratamento de erros

---

## 🔧 Integração com Outros Scripts

Pode ser usado junto com:
- `test_webhook.py` - Para verificar se webhooks estão salvando
- `test_connection.py` - Para testar conexão antes
- `init_database.py` - Para criar tabelas

---

**Última atualização:** 10/10/2025

