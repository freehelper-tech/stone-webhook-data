#!/usr/bin/env python3
"""
Script: empreendedores do CSV que concluíram o curso 70 (Raio X) na Ludos → webhook

Lógica:
  1. Carrega o CSV "Controle de Cadastros Impulso - Negativados - Empreendedores Interessados.csv"
  2. Consulta a Ludos: quem terminou o curso 70 (Raio X do Endividamento)
  3. Cruza por email ou telefone: fica só quem está NO CSV e concluiu o curso 70
  4. Envia para o webhook apenas esses (dados do CSV + datas/progressão da Ludos)

Uso:
  python scripts/ludos_raio_x_planilha.py
  python scripts/ludos_raio_x_planilha.py --show-api   # mostra amostra da API Ludos

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

# Configuração Ludos
LUDOS_API_BASE = "https://api.ludos.pro/api3"
LUDOS_API_KEY = "44dd6115bd97476497a28668847b4a54"

# Curso 70 = Raio X do Endividamento na Ludos
CURSO_RAIO_X_ID = 70
CURSO_NOME_RAIO_X = "Raio X do Endividamento"

WEBHOOK_RAIO_X_PLANILHA_URL = os.environ.get(
    "WEBHOOK_RAIO_X_PLANILHA_URL",
    "https://webhook.amcbots.com.br/webhook/039ef1ef-12c6-45d7-85e9-dcc8b9466288",
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_CADASTROS = REPO_ROOT / "Controle de Cadastros Impulso - Negativados - Empreendedores Interessados.csv"
JSON_SAIDA_RAIO_X = REPO_ROOT / "concluintes_raio_x_endividamento.json"


def normalizar_email(e: str) -> str:
    if not e:
        return ""
    return str(e).strip().lower()


def normalizar_telefone(t: str) -> str:
    if not t:
        return ""
    return re.sub(r"\D", "", str(t)).strip()


def carregar_csv(caminho: Path) -> list[dict]:
    """Carrega o CSV e retorna lista de linhas (dict por linha)."""
    if not caminho.exists():
        return []
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


HEADERS = {
    "Ocp-Apim-Subscription-Key": LUDOS_API_KEY,
    "Content-Type": "application/json",
}


def api_get(url: str, params: dict | None = None):
    r = requests.get(url, headers=HEADERS, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


def _extrair_lista(data, keys=("data", "items", "results", "courses", "players", "performances")):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in keys:
            if k in data and isinstance(data[k], list):
                return data[k]
    return []


def buscar_courses() -> list:
    url = f"{LUDOS_API_BASE}/report/courses"
    data = api_get(url)
    return _extrair_lista(data)


def buscar_performance_todos() -> list:
    """GET /report/performance sem parâmetros; retorna todos os registros. Filtramos por courseId no script."""
    url = f"{LUDOS_API_BASE}/report/performance"
    data = api_get(url)
    return _extrair_lista(data)


def filtrar_performance_por_curso(performance: list, course_id: int) -> list:
    """Filtra a lista de performance pelo courseId (ex.: 70 = Raio X do Endividamento)."""
    return [p for p in performance if p.get("courseId") == course_id]


def buscar_players() -> list:
    url = f"{LUDOS_API_BASE}/report/players"
    data = api_get(url)
    return _extrair_lista(data)


def encontrar_curso_raio_x(courses: list) -> dict | None:
    """Encontra o curso pelo nome (Raio X, Raio-X, Endividamento) ou por courseId 70."""
    # Busca por nome (aceita "Raio X", "Raio-X", "Endividamento")
    for c in courses:
        name = (c.get("courseName") or "").strip().lower()
        if "endividamento" in name and ("raio" in name or "raio-x" in name):
            return c
        if CURSO_NOME_RAIO_X.lower() in name:
            return c
    # Fallback: curso 70 é o Raio X do Endividamento
    for c in courses:
        if c.get("courseId") == CURSO_RAIO_X_ID:
            return c
    return None


def _concluinte(item: dict) -> bool:
    """Considera concluinte quando endDate preenchido ou progression >= 100."""
    if item.get("endDate"):
        return True
    p = item.get("progression")
    if p is not None:
        try:
            return float(p) >= 100
        except (TypeError, ValueError):
            pass
    return False


def extrair_concluintes_ludos(performance: list, players: list) -> tuple[set[tuple[str, str]], dict[str, dict], dict[str, dict]]:
    """
    De quem concluiu o curso na Ludos: set de (email_norm, tel_norm),
    perf_por_email e perf_por_telefone para montar o payload.
    """
    players_por_id = {}
    for p in players:
        pid = p.get("id") or p.get("playerId") or p.get("player_id")
        if pid is not None:
            players_por_id[str(pid)] = p

    concluintes = set()
    perf_por_chave = {}

    for item in performance:
        if not _concluinte(item):
            continue
        pid = item.get("playerId") or item.get("player_id") or item.get("id")
        pl = players_por_id.get(str(pid)) if pid is not None else {}
        email = pl.get("email") or pl.get("login") or pl.get("mail") or item.get("email") or ""
        phone = pl.get("phone") or pl.get("telefone") or pl.get("mobile") or item.get("phone") or item.get("telefone") or item.get("mobile") or ""
        key = (normalizar_email(email), normalizar_telefone(phone))
        if not key[0] and not key[1]:
            continue
        concluintes.add(key)
        prog = item.get("progression")
        prog_val = float(prog) if prog is not None else None
        if prog_val is not None:
            try:
                prog_val = round(prog_val, 2)
            except (TypeError, ValueError):
                pass
        perf = {"startDate": item.get("startDate") or "", "endDate": item.get("endDate") or "", "progression": prog_val}
        if key not in perf_por_chave or (perf.get("endDate") and not perf_por_chave[key].get("endDate")):
            perf_por_chave[key] = perf

    emails_ok = {k[0] for k in concluintes if k[0]}
    telefones_ok = {k[1] for k in concluintes if k[1]}
    perf_por_email = {}
    perf_por_telefone = {}
    for (e, t), p in perf_por_chave.items():
        if e:
            perf_por_email[e] = p
        if t:
            perf_por_telefone[t] = p
    return concluintes, perf_por_email, perf_por_telefone


def enviar_webhook(payload: list[dict], url: str) -> bool:
    if not (url or "").strip():
        return False
    try:
        r = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        if r.ok:
            print(f"Webhook enviado: {len(payload)} registro(s) -> {url}")
            return True
        print(f"Webhook retornou {r.status_code}: {r.text[:200]}")
        return False
    except Exception as e:
        print(f"Erro ao enviar webhook: {e}")
        return False


def main():
    show_api = "--show-api" in sys.argv or "-s" in sys.argv
    print("Carregando CSV de empreendedores...")
    rows_csv = carregar_csv(CSV_CADASTROS)
    print(f"  Total de linhas no CSV: {len(rows_csv)}")

    print("Buscando cursos (GET /report/courses)...")
    try:
        courses = buscar_courses()
    except Exception as e:
        print(f"Erro ao buscar cursos: {e}")
        return 1
    curso = encontrar_curso_raio_x(courses)
    if not curso:
        print(f'  Curso "{CURSO_NOME_RAIO_X}" (id 70) não encontrado.')
        return 1
    course_id = curso.get("courseId")
    course_name = curso.get("courseName") or CURSO_NOME_RAIO_X
    print(f"  Curso: {course_name} (courseId={course_id})")

    print("Buscando performance do curso na Ludos...")
    try:
        performance_todos = buscar_performance_todos()
    except Exception as e:
        print(f"Erro ao buscar performance: {e}")
        return 1
    performance = filtrar_performance_por_curso(performance_todos, course_id)
    print(f"  Registros do curso na Ludos: {len(performance)}")

    if show_api and performance:
        with_end = [p for p in performance if p.get("endDate")]
        print("\n  [--show-api] Com endDate (concluíram):", len(with_end))
        if with_end:
            print("  Exemplo:", json.dumps(with_end[0], indent=2, ensure_ascii=False)[:500])

    print("Buscando players na Ludos...")
    try:
        players = buscar_players()
    except Exception as e:
        print(f"Erro ao buscar players: {e}")
        return 1

    concluintes, perf_por_email, perf_por_telefone = extrair_concluintes_ludos(performance, players)
    emails_ok = {k[0] for k in concluintes if k[0]}
    telefones_ok = {k[1] for k in concluintes if k[1]}
    print(f"  Concluintes do curso na Ludos (com email ou telefone): {len(concluintes)}")

    # Filtrar: só linhas do CSV que concluíram o curso 70 (match por email ou telefone)
    concluintes_csv = []
    for row in rows_csv:
        email_n = normalizar_email(row.get("Email", ""))
        tel_n = normalizar_telefone(row.get("Telefone", ""))
        if email_n in emails_ok or tel_n in telefones_ok:
            concluintes_csv.append(row)

    print(f"Empreendedores do CSV que concluíram o curso 70: {len(concluintes_csv)}")

    # Montar payload: dados do CSV + datas/progressão da Ludos
    linhas = []
    for row in concluintes_csv:
        email_n = normalizar_email(row.get("Email", ""))
        tel_n = normalizar_telefone(row.get("Telefone", ""))
        perf = perf_por_email.get(email_n) or perf_por_telefone.get(tel_n) or {}
        prog = perf.get("progression")
        linhas.append({
            "Fase": row.get("Fase", ""),
            "Nome": row.get("Nome", ""),
            "CPF": row.get("CPF", ""),
            "Telefone": row.get("Telefone", ""),
            "Email": row.get("Email", ""),
            "Status Impulso": row.get("Status Impulso", ""),
            "Status Pérola": row.get("Status Pérola", ""),
            "Curso": course_name,
            "Início Curso": perf.get("startDate") or "",
            "Conclusão Curso": perf.get("endDate") or "",
            "Progressão (%)": prog,
        })

    print(f"Enviando ao webhook: {len(linhas)} registro(s)")

    # Salvar JSON local
    with open(JSON_SAIDA_RAIO_X, "w", encoding="utf-8") as f:
        json.dump(linhas, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {JSON_SAIDA_RAIO_X}")

    # Enviar para o webhook (nova aba da planilha)
    if "RAIO_X_ABA" in WEBHOOK_RAIO_X_PLANILHA_URL:
        print("Configure WEBHOOK_RAIO_X_PLANILHA_URL no script com o URL do webhook da nova aba.")
    else:
        enviar_webhook(linhas, WEBHOOK_RAIO_X_PLANILHA_URL)

    return 0


if __name__ == "__main__":
    sys.exit(main())
