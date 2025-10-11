"""
Processador de dados do Jotform
Funções auxiliares para converter payload do Jotform em dados estruturados
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

from dto.webhook_dtos import JotformWebhookPayload, EmpreendedorCreateRequest

logger = logging.getLogger(__name__)


class JotformProcessor:
    """Classe para processar dados do Jotform"""
    
    @staticmethod
    def processar_nome(payload: JotformWebhookPayload) -> Optional[str]:
        """
        Processar campo Nome do Jotform
        
        O nome pode vir como:
        - Objeto com first/last
        - String direta
        """
        try:
            # Tentar objeto first/last
            if payload.Nome and hasattr(payload.Nome, 'first'):
                first = payload.Nome.first.strip()
                last = payload.Nome.last.strip()
                return f"{first} {last}".strip()
            
            # Tentar campo nome direto
            if payload.nome:
                return payload.nome.strip()
            
            # Fallback para campos alternativos
            if payload.Nome and isinstance(payload.Nome, str):
                return payload.Nome.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao processar nome: {e}")
            return None
    
    @staticmethod
    def processar_telefone(payload: JotformWebhookPayload) -> Optional[str]:
        """
        Processar campo Telefone do Jotform
        
        O telefone pode vir como:
        - Objeto com area/phone
        - String direta
        """
        try:
            # Tentar objeto area/phone
            if payload.Telefone and hasattr(payload.Telefone, 'area'):
                area = payload.Telefone.area.strip()
                phone = payload.Telefone.phone.strip()
                return f"({area}) {phone}"
            
            # Tentar campo telefone direto
            if payload.telefone:
                return payload.telefone.strip()
            
            # Fallback para campos alternativos
            if payload.Telefone and isinstance(payload.Telefone, str):
                return payload.Telefone.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao processar telefone: {e}")
            return None
    
    @staticmethod
    def processar_email(payload: JotformWebhookPayload) -> Optional[str]:
        """Processar campo Email"""
        try:
            email = payload.email or payload.Email
            return email.strip().lower() if email else None
        except Exception as e:
            logger.error(f"Erro ao processar email: {e}")
            return None
    
    @staticmethod
    def processar_fontes_renda(payload: JotformWebhookPayload) -> Optional[str]:
        """
        Processar fontes de renda
        Pode vir como lista ou string
        """
        try:
            # Se vier lista do Jotform
            if payload.fontes_renda and isinstance(payload.fontes_renda, list):
                return '; '.join([str(item).strip() for item in payload.fontes_renda])
            
            # Se vier string direta
            if payload.fonte_renda:
                return payload.fonte_renda.strip()
            
            # Fallback para fontes_renda como string
            if payload.fontes_renda and isinstance(payload.fontes_renda, str):
                return payload.fontes_renda.strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao processar fontes de renda: {e}")
            return None
    
    @staticmethod
    def limpar_cpf(cpf: Optional[str]) -> Optional[str]:
        """Limpar CPF removendo caracteres especiais"""
        if not cpf:
            return None
        
        try:
            # Remover pontos, hífens e espaços
            cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))
            return cpf_limpo[:14] if cpf_limpo else None
        except Exception as e:
            logger.error(f"Erro ao limpar CPF: {e}")
            return None
    
    @staticmethod
    def processar_data_inscricao(data_str: Optional[str] = None) -> datetime:
        """
        Processar data de inscrição
        Se não fornecida, usar data/hora atual
        """
        if not data_str:
            return datetime.now()
        
        try:
            # Tentar formatos comuns
            formatos = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%d/%m/%Y %H:%M:%S',
                '%b. %d, %Y',  # Formato Jotform: "Oct. 10, 2025"
            ]
            
            for formato in formatos:
                try:
                    return datetime.strptime(data_str, formato)
                except ValueError:
                    continue
            
            # Se nenhum formato funcionou, usar data atual
            logger.warning(f"Não foi possível parsear data: {data_str}. Usando data atual.")
            return datetime.now()
            
        except Exception as e:
            logger.error(f"Erro ao processar data: {e}")
            return datetime.now()
    
    @staticmethod
    def payload_to_empreendedor(payload: JotformWebhookPayload) -> EmpreendedorCreateRequest:
        """
        Converter payload do Jotform em EmpreendedorCreateRequest
        
        Args:
            payload: Payload recebido do webhook Jotform
            
        Returns:
            EmpreendedorCreateRequest: Dados estruturados do empreendedor
        """
        try:
            # Processar nome (obrigatório)
            nome = JotformProcessor.processar_nome(payload)
            if not nome:
                raise ValueError("Nome é obrigatório")
            
            # Processar telefone (obrigatório)
            telefone = JotformProcessor.processar_telefone(payload)
            if not telefone:
                raise ValueError("Telefone é obrigatório")
            
            # Processar email
            email = JotformProcessor.processar_email(payload)
            
            # Processar CPF
            cpf = JotformProcessor.limpar_cpf(payload.CPF or payload.cpf)
            
            # Processar fontes de renda
            fonte_renda = JotformProcessor.processar_fontes_renda(payload)
            
            # Criar request
            return EmpreendedorCreateRequest(
                # Obrigatórios
                nome=nome,
                telefone=telefone,
                
                # Principais
                email=email,
                comunidade_originadora="Impulso Stone",  # Padrão
                data_inscricao=datetime.now(),
                
                # Formulário Jotform
                apelido=payload.apelido,
                cpf=cpf,
                cidade=payload.Cidade or payload.cidade,
                estado=payload.Estado or payload.estado,
                idade=payload.Idade or payload.idade,
                genero=payload.Genero or payload.genero,
                raca_cor=payload.raca_cor,
                escolaridade=payload.Escolaridade or payload.escolaridade,
                faixa_renda=payload.faixa_renda,
                fonte_renda=fonte_renda,
                tempo_funcionamento=payload.tempo_funcionamento,
                segmento_atuacao=payload.segmento_atuacao,
                segmento_outros=payload.segmento_outros,
                organizacao_stone=payload.organizacao_stone,
                formulario_tipo="Webhook Jotform",
                
                # Defaults para campos Ludos
                ludos_pontos=0,
                ludos_moedas=0,
                ludos_nivel=1,
                
                # Defaults para campos MGM
                mgm_total_mensagens=0,
                mgm_total_reacoes=0,
                mgm_total_interacoes=0,
                mgm_engajamento_percent=0.0,
                
                # Defaults para flags
                esta_na_comunidade=False,
                esta_no_grupo_mentoria=False,
                esta_no_papo_impulso=False,
                interacao_nos_grupos=0,
                ativo_na_ludos=False,
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

