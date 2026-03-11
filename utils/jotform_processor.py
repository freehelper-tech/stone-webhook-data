"""
Processador de dados do Jotform
Validação, normalização e conversão para EmpreendedorCreateRequest.
Ref.: Tratamento de dados antes de inserir no banco (webhook).
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

from dto.webhook_dtos import JotformWebhookPayload, EmpreendedorCreateRequest
from services.data_service import (
    safe_value,
    clean_nome,
    padronizar_organizacao as padronizar_organizacao_ds,
    safe_cpf,
    validar_email,
    parse_datetime,
    to_bool,
    safe_telefone,
    _safe_str,
    MAX_NOME,
    MAX_TELEFONE,
    MAX_EMAIL,
    MAX_CPF,
    MAX_CIDADE,
    MAX_ESTADO,
    MAX_IDADE,
    MAX_GENERO,
    MAX_RACA_COR,
    MAX_ESCOLARIDADE,
    MAX_FAIXA_RENDA,
    MAX_TEMPO_FUNCIONAMENTO,
    MAX_SEGMENTO_ATUACAO,
    MAX_SEGMENTO_OUTROS,
    MAX_ORGANIZACAO_STONE,
    MAX_FORMULARIO_TIPO,
    MAX_APELIDO,
    MAX_FONTE_RENDA,
)

logger = logging.getLogger(__name__)


def _segmento_outros_com_segundo_negocio(payload: JotformWebhookPayload) -> Optional[str]:
    """
    Monta segmento_outros: texto "Se outros qual" do primeiro negócio e, quando
    "Você tem outro negócio?" = Sim, acrescenta "Segundo negócio: [segmento], [tempo]".
    """
    extra = getattr(payload, "model_extra", None) or {}
    primeiro = safe_value(getattr(payload, "segmento_outros", None))
    tem_outro = safe_value(extra.get("Você tem outro negócio que gostaria de cadastrar?"))
    seg2 = safe_value(extra.get("Segmento de atuação (segundo negócio)"))
    tempo2 = safe_value(extra.get("Tempo de funcionamento do segundo negócio"))
    partes = []
    if primeiro:
        partes.append(primeiro)
    if tem_outro and str(tem_outro).lower() in ("sim", "s", "yes") and (seg2 or tempo2):
        segundo = "Segundo negócio: " + ", ".join(x for x in (seg2, tempo2) if x)
        partes.append(segundo)
    return ", ".join(partes) if partes else None


class JotformProcessor:
    """Classe para processar dados do Jotform"""
    
    @staticmethod
    def processar_nome(payload: JotformWebhookPayload) -> Optional[str]:
        """
        Processar campo Nome: objeto first/last ou string, depois clean_nome e truncar.
        """
        try:
            raw = None
            if payload.Nome and hasattr(payload.Nome, "first"):
                first = (payload.Nome.first or "").strip()
                last = (payload.Nome.last or "").strip()
                raw = f"{first} {last}".strip()
            elif payload.nome:
                raw = payload.nome.strip()
            elif payload.Nome and isinstance(payload.Nome, str):
                raw = payload.Nome.strip()
            if not raw:
                return None
            nome_limpo = clean_nome(raw)
            return _safe_str(nome_limpo or raw, MAX_NOME) if (nome_limpo or raw) else None
        except Exception as e:
            logger.error(f"Erro ao processar nome: {e}")
            return None
    
    @staticmethod
    def processar_telefone(payload: JotformWebhookPayload) -> Optional[str]:
        """
        Processar campo Telefone: objeto area/phone ou string; trim e máx 20 caracteres.
        """
        try:
            raw = None
            if payload.Telefone and hasattr(payload.Telefone, "area"):
                area = (getattr(payload.Telefone, "area", "") or "").strip()
                phone = (getattr(payload.Telefone, "phone", "") or "").strip()
                raw = f"({area}) {phone}".strip() if (area or phone) else None
            if raw is None and payload.telefone:
                raw = payload.telefone.strip()
            if raw is None and payload.Telefone and isinstance(payload.Telefone, str):
                raw = payload.Telefone.strip()
            return safe_telefone(raw) if raw else None
        except Exception as e:
            logger.error(f"Erro ao processar telefone: {e}")
            return None
    
    @staticmethod
    def processar_email(payload: JotformWebhookPayload) -> Optional[str]:
        """Email: trim, minúsculas, válido (contém @). Se informado sem @, ignora (None) e registra log."""
        try:
            email = safe_value(getattr(payload, "email", None) or getattr(payload, "Email", None))
            if not email:
                return None
            email = email.strip().lower()
            if "@" not in email:
                logger.info("Campo email descartado (sem @): valor não será gravado no banco")
                return None
            return _safe_str(email, MAX_EMAIL)
        except Exception as e:
            logger.error(f"Erro ao processar email: {e}")
            return None
    
    @staticmethod
    def processar_fontes_renda(payload: JotformWebhookPayload) -> Optional[str]:
        """Fontes de renda: lista juntada com '; ' ou string; truncar ao limite da coluna."""
        try:
            raw = None
            if getattr(payload, "fontes_renda", None) and isinstance(payload.fontes_renda, list):
                items = [str(item).strip() for item in payload.fontes_renda if item]
                raw = "; ".join(items) if items else None
            elif getattr(payload, "fonte_renda", None) and payload.fonte_renda.strip():
                raw = payload.fonte_renda.strip()
            elif getattr(payload, "fontes_renda", None) and isinstance(payload.fontes_renda, str):
                raw = payload.fontes_renda.strip() or None
            return _safe_str(raw, MAX_FONTE_RENDA) if raw else None
        except Exception as e:
            logger.error(f"Erro ao processar fontes de renda: {e}")
            return None
    
    @staticmethod
    def payload_to_empreendedor(payload: JotformWebhookPayload) -> EmpreendedorCreateRequest:
        """
        Converter payload do Jotform em EmpreendedorCreateRequest.
        Aplica validação, normalização e truncamento conforme documento de tratamento de dados.

        Campos que são levados ao banco (não deixamos de levar se vierem no payload):
        nome, telefone, email, cpf, apelido, cidade, estado, idade, genero, raca_cor,
        escolaridade, faixa_renda, fonte_renda, tempo_funcionamento, segmento_atuacao,
        segmento_outros, organizacao_stone, data_inscricao (submitDate), formulario_tipo.
        """
        try:
            nome = JotformProcessor.processar_nome(payload)
            if not nome:
                raise ValueError("Nome é obrigatório (não pode ser vazio após trim/clean)")
            telefone = JotformProcessor.processar_telefone(payload)
            if not telefone:
                raise ValueError("Telefone é obrigatório")
            email = JotformProcessor.processar_email(payload)
            cpf_raw = getattr(payload, "CPF", None) or getattr(payload, "cpf", None)
            cpf = safe_cpf(cpf_raw)
            if cpf_raw and safe_value(cpf_raw) and not cpf:
                logger.info("Campo CPF descartado (inválido ou sequência de teste): valor não será gravado no banco")
            fonte_renda = JotformProcessor.processar_fontes_renda(payload)
            data_str = getattr(payload, "submitDate", None) or getattr(payload, "submissionDate", None) or getattr(payload, "Submission Date", None)
            data_inscricao = parse_datetime(data_str, default_now=True)
            org_raw = getattr(payload, "organizacao_stone", None)
            organizacao_stone = padronizar_organizacao_ds(org_raw)
            # Comunidade originadora: quando escolhe uma organização (ex.: Empreende Aí, Recomeçar), grava nessa coluna; senão "Impulso Stone"
            if organizacao_stone and organizacao_stone != "Nao vim de nenhuma organizacao":
                comunidade_originadora = _safe_str(organizacao_stone, 50)
            else:
                comunidade_originadora = _safe_str("Impulso Stone", 50)
            return EmpreendedorCreateRequest(
                nome=nome,
                telefone=telefone,
                email=email,
                comunidade_originadora=comunidade_originadora,
                data_inscricao=data_inscricao,
                apelido=_safe_str(getattr(payload, "apelido", None), MAX_APELIDO),
                cpf=cpf,
                cidade=_safe_str(getattr(payload, "Cidade", None) or getattr(payload, "cidade", None), MAX_CIDADE),
                estado=_safe_str(getattr(payload, "Estado", None) or getattr(payload, "estado", None), MAX_ESTADO),
                idade=_safe_str(getattr(payload, "Idade", None) or getattr(payload, "idade", None), MAX_IDADE),
                genero=_safe_str(getattr(payload, "Genero", None) or getattr(payload, "genero", None), MAX_GENERO),
                raca_cor=_safe_str(getattr(payload, "raca_cor", None), MAX_RACA_COR),
                escolaridade=_safe_str(getattr(payload, "Escolaridade", None) or getattr(payload, "escolaridade", None), MAX_ESCOLARIDADE),
                faixa_renda=_safe_str(getattr(payload, "faixa_renda", None), MAX_FAIXA_RENDA),
                fonte_renda=fonte_renda,
                tempo_funcionamento=_safe_str(getattr(payload, "tempo_funcionamento", None), MAX_TEMPO_FUNCIONAMENTO),
                segmento_atuacao=_safe_str(getattr(payload, "segmento_atuacao", None), MAX_SEGMENTO_ATUACAO),
                segmento_outros=_safe_str(
                    _segmento_outros_com_segundo_negocio(payload),
                    MAX_SEGMENTO_OUTROS,
                ),
                organizacao_stone=organizacao_stone,
                formulario_tipo=_safe_str("Webhook Jotform", MAX_FORMULARIO_TIPO) or "Webhook Jotform",
                ludos_pontos=0,
                ludos_moedas=0,
                ludos_nivel=1,
                mgm_total_mensagens=0,
                mgm_total_reacoes=0,
                mgm_total_interacoes=0,
                mgm_engajamento_percent=0.0,
                esta_na_comunidade=False,
                esta_no_grupo_mentoria=False,
                esta_no_papo_impulso=False,
                interacao_nos_grupos=0,
                ativo_na_ludos=to_bool(getattr(payload, "ativo_na_ludos", None)),
                fazendo_mentoria=False,
                solicitou_credito=False,
            )
        except ValueError as e:
            logger.error(f"Erro de validação ao processar payload: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao converter payload: {e}")
            raise
    
    @staticmethod
    def payload_list_to_empreendedores(
        payloads: List[JotformWebhookPayload]
    ) -> List[EmpreendedorCreateRequest]:
        """
        Converter lista de payloads em lista de EmpreendedorCreateRequest
        
        Args:
            payloads: Lista de payloads do Jotform
            
        Returns:
            List[EmpreendedorCreateRequest]: Lista de dados estruturados
        """
        empreendedores = []
        
        for idx, payload in enumerate(payloads):
            try:
                empreendedor = JotformProcessor.payload_to_empreendedor(payload)
                empreendedores.append(empreendedor)
            except Exception as e:
                logger.error(f"Erro ao processar payload {idx + 1}: {e}")
                # Continuar processando os outros
                continue
        
        return empreendedores
    
    @staticmethod
    def validar_payload(payload: Dict[str, Any]) -> bool:
        """
        Validar se payload tem campos mínimos necessários
        
        Args:
            payload: Payload bruto do webhook
            
        Returns:
            bool: True se válido, False caso contrário
        """
        try:
            # Verificar se tem pelo menos nome e telefone
            has_nome = (
                'Nome' in payload or 
                'nome' in payload
            )
            
            has_telefone = (
                'Telefone' in payload or 
                'telefone' in payload
            )
            
            return has_nome and has_telefone
            
        except Exception as e:
            logger.error(f"Erro ao validar payload: {e}")
            return False
    
    @staticmethod
    def extrair_metadata(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrair metadata do payload do Jotform
        
        Args:
            payload: Payload bruto do webhook
            
        Returns:
            Dict com metadata extraída
        """
        metadata = {
            'submission_id': payload.get('submissionID'),
            'form_id': payload.get('formID'),
            'ip': payload.get('ip'),
            'created_at': payload.get('created_at'),
            'updated_at': payload.get('updated_at'),
        }
        
        return {k: v for k, v in metadata.items() if v is not None}

