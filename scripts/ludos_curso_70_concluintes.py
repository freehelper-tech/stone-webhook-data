#!/usr/bin/env python3
"""
Script de automação: verificar quais empreendedores do CSV
"Controle de Cadastros Impulso - Negativados - Empreendedores Interessados.csv"
concluíram o curso ID 70 na Ludos e salvar o resultado.

Uso:
  python scripts/ludos_curso_70_concluintes.py

Requer: requests (pip install requests)
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Instale requests: pip install requests")
    sys.exit(1)

# Configuração Ludos (mesmo do n8n)
LUDOS_API_BASE = "https://api.ludos.pro/api3"
LUDOS_API_KEY = "44dd6115bd97476497a28668847b4a54"
COURSE_ID = 70

# Webhook: enviar lista de empreendedores encontrados (match)
WEBHOOK_CONCLUINTES_URL = "https://webhook.amcbots.com.br/webhook/039ef1ef-12c6-45d7-85e9-dcc8b9466288"

# Arquivos
REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_ENTRADA = REPO_ROOT / "Controle de Cadastros Impulso - Negativados - Empreendedores Interessados.csv"
CSV_SAIDA = REPO_ROOT / "empreendedores_concluintes_curso_70.csv"
JSON_SAIDA = REPO_ROOT / "empreendedores_concluintes_curso_70.json"

HEADERS = {
    "Ocp-Apim-Subscription-Key": LUDOS_API_KEY,
    "Content-Type": "application/json",
}


def normalizar_telefone(t: str) -> str:
    """Deixa só dígitos do telefone."""
    if not t:
        return ""
    return re.sub(r"\D", "", str(t)).strip()


def normalizar_email(e: str) -> str:
    """Email em minúsculas e sem espaços."""
    if not e:
        return ""
    return str(e).strip().lower()


def carregar_csv(caminho: Path) -> list[dict]:
    """Carrega o CSV de empreendedores. Retorna lista de dicts com chaves do cabeçalho."""
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho}")
    rows = []
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def api_get(url: str, params: dict | None = None) -> dict:
    """GET na API Ludos. Retorna JSON ou levanta em caso de erro HTTP."""
    r = requests.get(url, headers=HEADERS, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


def buscar_performance_curso(course_id: int) -> list:
    """
    GET /api3/report/performance?courseId=70
    Retorna lista de registros: courseId, playerId, progression, endDate, ...
    """
    url = f"{LUDOS_API_BASE}/report/performance"
    data = api_get(url, params={"courseId": str(course_id)})
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "performances"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def buscar_players() -> list:
    """
    GET /api3/report/players
    Retorna lista de players com playerId, login, email (como /player/get).
    """
    url = f"{LUDOS_API_BASE}/report/players"
    data = api_get(url)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "players"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def buscar_courses() -> list:
    """
    GET /api3/report/courses
    Retorna lista de cursos: courseId, courseName, isPublished, modules (activities), groups.
    """
    url = f"{LUDOS_API_BASE}/report/courses"
    data = api_get(url)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "results", "courses"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def buscar_trails_performance(trail_id: int | None = None) -> list:
    """
    GET /api3/report/trails-performance
    Retorna performance por trilha: trailId, playerId, progression, coursesCompleted, endDate, ...
    Se trail_id for passado, filtra por trailId (ex.: 70).
    """
    url = f"{LUDOS_API_BASE}/report/trails-performance"
    params = {}
    if trail_id is not None:
        params["trailId"] = str(trail_id)
    data = api_get(url, params=params if params else None)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "trailId" in data and "playerId" in data:
            return [data]  # resposta única vira lista de 1
        for key in ("data", "items", "results", "performances"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def enviar_webhook_concluintes(concluintes: list[dict]) -> bool:
    """Envia POST ao webhook AMC Bots com a lista de empreendedores encontrados (match)."""
    if not WEBHOOK_CONCLUINTES_URL.strip():
        return False
    try:
        r = requests.post(
            WEBHOOK_CONCLUINTES_URL,
            json=concluintes,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        if r.ok:
            print(f"Webhook enviado com sucesso: {len(concluintes)} empreendedor(es) -> {WEBHOOK_CONCLUINTES_URL}")
            return True
        print(f"Webhook retornou {r.status_code}: {r.text[:200]}")
        return False
    except Exception as e:
        print(f"Erro ao enviar webhook: {e}")
        return False


def extrair_identificadores_ludos(performance: list, players: list, debug: bool = False) -> tuple[set[tuple[str, str]], dict[tuple[str, str], dict]]:
    """
    Extrai (email_normalizado, telefone_normalizado) de quem concluiu o curso
    e um mapa (email, tel) -> { startDate, endDate, progression } para o webhook.

    Retorna: (set de (email, phone), dict (email, phone) -> { startDate, endDate, progression })
    """
    concluintes = set()
    perf_por_chave: dict[tuple[str, str], dict] = {}

    # Mapear playerId -> player (player tem login, email como na doc /player/get)
    players_por_id = {}
    for p in players:
        pid = p.get("id") or p.get("playerId") or p.get("player_id")
        if pid is not None:
            players_por_id[str(pid)] = p

    if debug and performance:
        print("  [DEBUG] Primeiro item de performance:", json.dumps(performance[0], indent=2, ensure_ascii=False)[:600])
    if debug and players:
        print("  [DEBUG] Primeiro item de players:", json.dumps(players[0], indent=2, ensure_ascii=False)[:600])

    for item in performance:
        # Critério Ludos: conclusão por progression >= 100 ou endDate preenchido
        progression = item.get("progression")
        end_date = item.get("endDate")
        completed = False
        if progression is not None:
            try:
                completed = float(progression) >= 100
            except (TypeError, ValueError):
                pass
        if not completed and end_date:
            completed = True
        # Fallbacks para outros formatos de API
        if not completed:
            completed = item.get("completed") is True
        if not completed and item.get("completion") is not None:
            try:
                completed = float(item.get("completion")) >= 100
            except (TypeError, ValueError):
                pass

        if not completed:
            continue

        pid = item.get("playerId") or item.get("player_id") or item.get("id")
        pl = players_por_id.get(str(pid)) if pid is not None else None
        # login e email conforme /player/get
        email = (item.get("email") or (pl or {}).get("email") or (pl or {}).get("login") or (pl or {}).get("mail"))
        phone = item.get("phone") or item.get("telefone") or (pl or {}).get("phone") or (pl or {}).get("telefone") or (pl or {}).get("mobile")

        key = (normalizar_email(email or ""), normalizar_telefone(phone or ""))
        if not key[0] and not key[1]:
            continue
        concluintes.add(key)

        # Guardar dados de performance (preferir registro com endDate ou maior progressão)
        prog_val = None
        if progression is not None:
            try:
                prog_val = float(progression)
            except (TypeError, ValueError):
                pass
        perf_info = {
            "startDate": item.get("startDate"),
            "endDate": end_date,
            "progression": prog_val,
        }
        if key not in perf_por_chave:
            perf_por_chave[key] = perf_info
        else:
            # Manter o que tiver endDate ou maior progression
            atual = perf_por_chave[key]
            if perf_info.get("endDate") and not atual.get("endDate"):
                perf_por_chave[key] = perf_info
            elif (prog_val or 0) > (atual.get("progression") or 0):
                perf_por_chave[key] = perf_info

    if debug:
        print(f"  [DEBUG] Concluintes com email/telefone identificado: {len(concluintes)}")
    return concluintes, perf_por_chave


def main():
    debug = "--debug" in sys.argv or "-d" in sys.argv
    print("Carregando CSV de empreendedores...")
    try:
        rows = carregar_csv(CSV_ENTRADA)
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        sys.exit(1)
    print(f"  Total de linhas no CSV: {len(rows)}")

    # Cursos: listar e mostrar info do curso 70 (nome usado no payload do webhook)
    curso_70_name = ""
    print("Buscando cursos (GET /report/courses)...")
    try:
        courses = buscar_courses()
        print(f"  Total de cursos: {len(courses)}")
        curso_70 = next((c for c in courses if c.get("courseId") == COURSE_ID), None)
        if curso_70:
            curso_70_name = curso_70.get("courseName") or f"Curso {COURSE_ID}"
            print(f"  Curso 70: {curso_70_name} (publicado={curso_70.get('isPublished')})")
            mods = curso_70.get("modules") or []
            for m in mods[:3]:
                print(f"    - Módulo: {m.get('moduleName')} (atividades: {len(m.get('activities') or [])})")
            if len(mods) > 3:
                print(f"    ... e mais {len(mods) - 3} módulos")
        else:
            curso_70_name = f"Curso {COURSE_ID}"
            print(f"  Curso {COURSE_ID} não encontrado na lista.")
    except Exception as e:
        curso_70_name = f"Curso {COURSE_ID}"
        print(f"  Aviso ao buscar cursos: {e}")

    # Performance do curso 70
    print("Buscando performance do curso 70 (GET /report/performance)...")
    try:
        performance = buscar_performance_curso(COURSE_ID)
    except Exception as e:
        print(f"Erro ao buscar performance: {e}")
        sys.exit(1)
    print(f"  Registros de performance (curso): {len(performance)}")

    # Performance da trilha 70 (se existir), mescla com performance do curso
    print("Buscando performance da trilha 70 (GET /report/trails-performance)...")
    try:
        trails_perf = buscar_trails_performance(trail_id=COURSE_ID)
        if trails_perf:
            print(f"  Registros de performance (trilha): {len(trails_perf)}")
            # Mesclar: mesma estrutura (playerId, progression, endDate)
            performance = list(performance) + list(trails_perf)
            print(f"  Total combinado (curso + trilha): {len(performance)}")
    except Exception as e:
        print(f"  Aviso ao buscar trails-performance: {e}")

    print("Buscando players na API Ludos...")
    try:
        players = buscar_players()
    except Exception as e:
        print(f"Erro ao buscar players: {e}")
        sys.exit(1)
    print(f"  Total de players: {len(players)}")

    concluintes_ludos, perf_por_chave = extrair_identificadores_ludos(performance, players, debug=debug)
    print(f"  Concluintes identificados (email/telefone): {len(concluintes_ludos)}")

    # Montar set de emails e telefones para matching
    emails_ok = {e for e, _ in concluintes_ludos if e}
    telefones_ok = {t for _, t in concluintes_ludos if t}

    # Filtrar linhas do CSV que batem com concluintes
    concluintes_csv = []
    for row in rows:
        email = normalizar_email(row.get("Email", ""))
        tel = normalizar_telefone(row.get("Telefone", ""))
        if email in emails_ok or tel in telefones_ok:
            concluintes_csv.append(row)

    print(f"Empreendedores do CSV que concluíram o curso 70: {len(concluintes_csv)}")

    # Montar payload do webhook com os campos esperados (Fase, Nome, CPF, Telefone, Email, Status Impulso, Status Pérola, Curso, Início Curso, Conclusão Curso, Progressão (%))
    def linha_webhook(row: dict) -> dict:
        email_n = normalizar_email(row.get("Email", ""))
        tel_n = normalizar_telefone(row.get("Telefone", ""))
        key = (email_n, tel_n)
        perf = perf_por_chave.get(key) or {}
        prog = perf.get("progression")
        return {
            "Fase": row.get("Fase", ""),
            "Nome": row.get("Nome", ""),
            "CPF": row.get("CPF", ""),
            "Telefone": row.get("Telefone", ""),
            "Email": row.get("Email", ""),
            "Status Impulso": row.get("Status Impulso", ""),
            "Status Pérola": row.get("Status Pérola", ""),
            "Curso": curso_70_name,
            "Início Curso": perf.get("startDate") or "",
            "Conclusão Curso": perf.get("endDate") or "",
            "Progressão (%)": round(prog, 2) if prog is not None else "",
        }

    webhook_payload = [linha_webhook(row) for row in concluintes_csv]

    # Salvar CSV
    if concluintes_csv:
        fieldnames = list(concluintes_csv[0].keys())
        with open(CSV_SAIDA, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(concluintes_csv)
        print(f"Salvo: {CSV_SAIDA}")

        with open(JSON_SAIDA, "w", encoding="utf-8") as f:
            json.dump(concluintes_csv, f, ensure_ascii=False, indent=2)
        print(f"Salvo: {JSON_SAIDA}")

        # POST no webhook com payload enriquecido (campos do CSV + Curso, Início Curso, Conclusão Curso, Progressão %)
        enviar_webhook_concluintes(webhook_payload)
    else:
        print("Nenhum empreendedor do CSV foi encontrado como concluinte do curso 70.")
        # Criar arquivos vazios ou com cabeçalho
        if rows:
            with open(CSV_SAIDA, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
            print(f"Criado CSV vazio: {CSV_SAIDA}")
        open(JSON_SAIDA, "w", encoding="utf-8").write("[]\n")
        print(f"Criado JSON vazio: {JSON_SAIDA}")
        # Envia lista vazia no webhook (mesmo formato: Fase, Nome, CPF, ...)
        enviar_webhook_concluintes([])

    return 0


if __name__ == "__main__":
    sys.exit(main())
