# Curso "Raio X do Endividamento" → Nova aba na planilha

Script que busca na Ludos todos os usuários que **terminaram** o curso "Raio X do Endividamento" e envia os dados para um webhook, para serem gravados numa **nova aba** da planilha (via fluxo AMC Bots).

## O que a Ludos puxa

| API | Campos úteis |
|-----|--------------|
| **GET /report/courses** | `courseId`, `courseName` – para identificar o curso pelo nome |
| **GET /report/performance?courseId=X** | `playerId`, `progression`, `startDate`, `endDate`, `performanceFirst`, `performanceBest`, `activitiesPlayed`, `workload` |
| **GET /report/players** | `playerId`, `login`, `email`, `playerName`, `nickName`, `status`, `createdAt` |

## Critério “terminou o curso”

- `progression` ≥ 100 **ou**
- `endDate` preenchido (data de conclusão).

## Campos enviados no webhook (uma linha por concluinte)

| Campo | Origem | Uso na planilha |
|-------|--------|------------------|
| **playerId** | Ludos | ID do jogador na plataforma |
| **Nome** | players.playerName | Nome do usuário |
| **Email** | players.email / login | Email (identificação) |
| **Apelido** | players.nickName | Apelido na Ludos |
| **Curso** | courses.courseName | Nome do curso (ex.: "Raio X do Endividamento") |
| **courseId** | courses | ID do curso |
| **Início Curso** | performance.startDate | Data de início no curso |
| **Conclusão Curso** | performance.endDate | Data em que terminou |
| **Progressão (%)** | performance.progression | Percentual concluído |
| **Performance Primeira** | performance.performanceFirst | Nota/performance na primeira tentativa |
| **Performance Melhor** | performance.performanceBest | Melhor nota/performance |
| **Atividades Realizadas** | performance.activitiesPlayed | Quantidade de atividades feitas |
| **Carga (min)** | performance.workload | Carga em minutos |
| **Status Ludos** | players.status | Ex.: ACTIVE |
| **Data Cadastro Ludos** | players.createdAt | Quando se cadastrou na Ludos |

## Como usar

1. **Configurar o webhook da nova aba**  
   No AMC Bots, crie um workflow que:
   - Recebe POST com um **array de objetos** (lista de concluintes).
   - Escreve/atualiza uma **nova aba** na planilha com essas colunas (ou as que fizerem sentido para você).

2. **Definir a URL do webhook**  
   No script, troque `WEBHOOK_RAIO_X_PLANILHA_URL` pelo URL real do workflow, ou defina a variável de ambiente:
   ```bash
   export WEBHOOK_RAIO_X_PLANILHA_URL="https://webhook.amcbots.com.br/webhook/SEU_ID_AQUI"
   ```

3. **Rodar o script** (manual ou agendado):
   ```bash
   python scripts/ludos_raio_x_planilha.py
   ```

4. **Automatizar**  
   Para “jogar automaticamente” na planilha, agende o script (cron, Azure Function, etc.) com a frequência desejada (ex.: 1x por dia).

## Saída local

- `concluintes_raio_x_endividamento.json` na raiz do projeto com a mesma lista enviada ao webhook (útil para conferência ou backup).
