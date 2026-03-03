"""
Tratamento de dados antes de inserir no banco (webhook Jotform e importações).

Funções reutilizáveis para validação, normalização e regras de negócio.
Ref.: documento "Tratamento de dados antes de inserir no banco (dados via webhook)".
"""
import re
from datetime import datetime
from typing import Optional

# Limites das colunas (Empreendedor) para truncar
MAX_NOME = 100
MAX_TELEFONE = 20
MAX_EMAIL = 100
MAX_CPF = 14
MAX_CIDADE = 100
MAX_ESTADO = 50
MAX_IDADE = 20
MAX_GENERO = 50
MAX_RACA_COR = 50
MAX_ESCOLARIDADE = 100
MAX_FAIXA_RENDA = 100
MAX_TEMPO_FUNCIONAMENTO = 50
MAX_SEGMENTO_ATUACAO = 100
MAX_SEGMENTO_OUTROS = 100
MAX_ORGANIZACAO_STONE = 100
MAX_FORMULARIO_TIPO = 50
MAX_APELIDO = 100
MAX_FONTE_RENDA = 500  # Text; truncar para evitar payload gigante


def safe_value(val: Optional[str]) -> Optional[str]:
    """
    Trim e trata vazios/nulos. Valores como None, "", "nan" viram None.
    """
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() in ("nan", "none", "null"):
        return None
    return s


def _safe_str(value: Optional[str], max_length: int) -> Optional[str]:
    """String segura: trim + truncar ao limite."""
    s = safe_value(value)
    if s is None:
        return None
    return s[:max_length] if len(s) > max_length else s


def clean_nome(nome: Optional[str]) -> Optional[str]:
    """
    Remove prefixos numéricos do nome (CPF ou telefone no início).
    Ex.: "030.029.877-35 Mattos" -> "Mattos"; "11919456464 Lopes" -> "Lopes".
    """
    s = safe_value(nome)
    if not s:
        return None
    # CPF formatado no início (xxx.xxx.xxx-xx ou 11 dígitos)
    s = re.sub(r"^\d{3}\.\d{3}\.\d{3}-\d{2}\s*", "", s)
    # Sequência de 10 ou 11 dígitos no início (telefone)
    s = re.sub(r"^\d{10,11}\s*", "", s)
    return s.strip() or None


def padronizar_organizacao(org: Optional[str]) -> Optional[str]:
    """
    Padroniza resposta "não vim de nenhuma organização" para valor canônico.
    Saída desejada: "Nao vim de nenhuma organizacao" (consistência no dashboard).
    """
    s = safe_value(org)
    if not s:
        return None
    low = s.lower()
    if "não" in low or "nao" in low:
        if "nenhuma" in low or "organização" in low or "organizacao" in low:
            return "Nao vim de nenhuma organizacao"
    return _safe_str(s, MAX_ORGANIZACAO_STONE)


def safe_cpf(cpf: Optional[str]) -> Optional[str]:
    """
    CPF: apenas dígitos, 11 caracteres. Rejeita sequências de teste (111..., 000...).
    Retorna None se vazio, inválido ou teste.
    """
    s = safe_value(cpf)
    if not s:
        return None
    digits = re.sub(r"\D", "", s)
    if len(digits) != 11:
        return None
    if digits == "0" * 11 or digits == "1" * 11:
        return None
    return digits[:MAX_CPF]


def validar_email(email: Optional[str]) -> bool:
    """Email válido: após trim, contém @."""
    s = safe_value(email)
    if not s:
        return False
    return "@" in s


def parse_datetime(val: Optional[str], default_now: bool = True) -> Optional[datetime]:
    """
    Interpreta data em formatos comuns ou timestamp (segundos/ms).
    Jotform envia submitDate como timestamp em milissegundos (ex.: "1772558985692").
    Em falha: datetime.now() se default_now, senão None.
    """
    s = safe_value(val)
    if not s:
        return datetime.now() if default_now else None
    # Timestamp numérico (Jotform: milissegundos; Unix: segundos)
    try:
        n = float(s.strip())
        if n > 1e12:  # milissegundos (13 dígitos)
            return datetime.fromtimestamp(n / 1000.0)
        if n > 1e9:  # segundos (10 dígitos)
            return datetime.fromtimestamp(n)
    except (ValueError, TypeError, OSError):
        pass
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%b. %d, %Y",  # Jotform: "Oct. 10, 2025"
    ]
    for fmt in formatos:
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return datetime.now() if default_now else None


def to_bool(val: Optional[str]) -> bool:
    """Converte strings para booleano: true, 1, sim, ativo -> True; demais -> False."""
    if val is None:
        return False
    s = str(val).strip().lower()
    if s in ("true", "1", "sim", "yes", "ativo", "s", "y"):
        return True
    return False


def normalizar_telefone_digitos(telefone: Optional[str]) -> Optional[str]:
    """Apenas dígitos do telefone (para comparação na deduplicação)."""
    s = safe_value(telefone)
    if not s:
        return None
    digits = re.sub(r"\D", "", s)
    return digits if digits else None


def safe_telefone(val: Optional[str]) -> Optional[str]:
    """Telefone: trim, no máximo 20 caracteres."""
    s = safe_value(val)
    if not s:
        return None
    return _safe_str(s, MAX_TELEFONE)
