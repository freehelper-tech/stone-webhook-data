"""
Serviço para encaminhar dados do formulário Jotform ao webhook Sheets Stone.
Toda vez que entrarem dados do Jotform, faz POST em https://webhook.amcbots.com.br/webhook/sheetsstone
"""
import logging
from typing import Dict, Any, List, Union

import httpx

from core.config import settings

logger = logging.getLogger(__name__)

# Timeout para o POST externo (não bloquear a resposta do webhook)
DEFAULT_TIMEOUT = 15.0


async def forward_to_sheets_webhook(payload: Union[Dict[str, Any], List[Dict[str, Any]]]) -> bool:
    """
    Envia um POST ao webhook Sheets Stone com o payload do formulário Jotform.

    Args:
        payload: Dados do formulário (um objeto ou lista de objetos).
                 Será enviado como JSON no body.

    Returns:
        True se o POST foi enviado com sucesso (2xx), False caso contrário ou se URL não configurada.
    """
    url = (settings.SHEETS_STONE_WEBHOOK_URL or "").strip()
    if not url:
        logger.debug("SHEETS_STONE_WEBHOOK_URL não configurada; encaminhamento desativado.")
        return False

    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.post(url, json=payload)
            if response.is_success:
                logger.info("Encaminhamento para Sheets Stone webhook OK: %s", url)
                return True
            # 404 = webhook ainda não registrado/ativo no destino
            if response.status_code == 404:
                logger.info(
                    "Sheets Stone webhook não registrado/ativo (404). Registre e ative o workflow em produção."
                )
            else:
                logger.warning(
                    "Sheets Stone webhook retornou %s: %s",
                    response.status_code,
                    response.text[:200] if response.text else "",
                )
            return False
    except httpx.TimeoutException as e:
        logger.warning("Timeout ao enviar para Sheets Stone webhook: %s", e)
        return False
    except Exception as e:
        logger.exception("Erro ao encaminhar para Sheets Stone webhook: %s", e)
        return False
