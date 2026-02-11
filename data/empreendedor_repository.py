"""
Repositório para Empreendedores
Camada de acesso a dados para tabela empreendedores
"""
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy import create_engine, and_, or_, func, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

from core.config import settings
from models.impulso_models import (
    Base, Empreendedor, Mentor, StatusMentoria, 
    Credito, NPSScore, LudosAtividade
)
from dto.webhook_dtos import (
    EmpreendedorCreateRequest,
    EmpreendedorUpdateRequest,
    EmpreendedorSearchRequest
)

logger = logging.getLogger(__name__)


class EmpreendedorRepository:
    """Repositório para operações com empreendedores"""
    
    def __init__(self):
        """Inicializar repositório e criar engine"""
        self.engine = create_engine(
            settings.sql_connection_string,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=3600,
            echo=settings.DEBUG
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info("Repositório de empreendedores inicializado (usando tabelas existentes)")
    
    def get_session(self) -> Session:
        """Obter sessão do banco"""
        return self.SessionLocal()
    
    def safe_str(self, value: Any, max_length: int) -> Optional[str]:
        """Truncar string no tamanho máximo"""
        if value is None:
            return None
        str_value = str(value).strip()
        if not str_value:
            return None
        return str_value[:max_length] if len(str_value) > max_length else str_value
    
    def create_empreendedor(self, data: EmpreendedorCreateRequest) -> Tuple[bool, Optional[Empreendedor], Optional[str]]:
        """
        Criar novo empreendedor
        
        Returns:
            Tuple[bool, Optional[Empreendedor], Optional[str]]: (sucesso, empreendedor, erro)
        """
        session = self.get_session()
        try:
            # Verificar duplicidade em 2 minutos (mesmo telefone + mesmo CPF ou email)
            dois_minutos_atras = datetime.now() - timedelta(minutes=2)
            
            # Buscar por telefone nos últimos 2 minutos
            duplicado_recente = session.query(Empreendedor).filter(
                and_(
                    Empreendedor.telefone == data.telefone,
                    Empreendedor.data_inscricao >= dois_minutos_atras,
                    or_(
                        (data.cpf and Empreendedor.cpf == data.cpf),
                        (data.email and Empreendedor.email == data.email)
                    )
                )
            ).first()
            
            if duplicado_recente:
                logger.warning(
                    f"Tentativa de cadastro duplicado detectada: "
                    f"telefone={data.telefone}, CPF={data.cpf}, email={data.email}, "
                    f"ID existente={duplicado_recente.id}"
                )
                return False, None, "Cadastro duplicado detectado nos últimos 2 minutos"
            
            # Verificar se telefone já existe (lógica antiga para sufixos)
            telefone_base = data.telefone[:17]  # Limitar para permitir sufixos
            telefone_final = data.telefone
            
            # Se telefone existe, adicionar sufixo
            contador = 1
            while session.query(Empreendedor).filter(
                Empreendedor.telefone == telefone_final
            ).first():
                telefone_final = f"{telefone_base}_{contador}"
                contador += 1
                if len(telefone_final) > 20:  # Limite do campo
                    return False, None, "Não foi possível gerar telefone único"
            
            # Criar empreendedor
            empreendedor = Empreendedor(
                # Campos obrigatórios
                nome=self.safe_str(data.nome, 100),
                telefone=telefone_final[:20],
                
                # Campos principais
                email=self.safe_str(data.email, 100),
                comunidade_originadora=self.safe_str(data.comunidade_originadora, 50),
                data_inscricao=data.data_inscricao or datetime.now(),
                
                # Campos do formulário
                apelido=self.safe_str(data.apelido, 100),
                cpf=self.safe_str(data.cpf, 14),
                cidade=self.safe_str(data.cidade, 100),
                estado=self.safe_str(data.estado, 50),
                idade=self.safe_str(data.idade, 20),
                genero=self.safe_str(data.genero, 50),
                raca_cor=self.safe_str(data.raca_cor, 50),
                escolaridade=self.safe_str(data.escolaridade, 100),
                faixa_renda=self.safe_str(data.faixa_renda, 100),
                fonte_renda=data.fonte_renda,
                tempo_funcionamento=self.safe_str(data.tempo_funcionamento, 50),
                segmento_atuacao=self.safe_str(data.segmento_atuacao, 100),
                segmento_outros=self.safe_str(data.segmento_outros, 100),
                organizacao_stone=self.safe_str(data.organizacao_stone, 100),
                formulario_tipo=self.safe_str(data.formulario_tipo, 50) or "Webhook Jotform",
                
                # Campos Ludos
                ludos_id=data.ludos_id,
                ludos_login=self.safe_str(data.ludos_login, 100),
                ludos_status=self.safe_str(data.ludos_status, 20),
                ludos_pontos=data.ludos_pontos,
                ludos_moedas=data.ludos_moedas,
                ludos_nivel=data.ludos_nivel,
                ludos_primeiro_login=data.ludos_primeiro_login,
                ludos_ultimo_login=data.ludos_ultimo_login,
                
                # Campos MGM
                mgm_user_name=self.safe_str(data.mgm_user_name, 100),
                mgm_whatsapp=self.safe_str(data.mgm_whatsapp, 20),
                mgm_total_mensagens=data.mgm_total_mensagens,
                mgm_total_reacoes=data.mgm_total_reacoes,
                mgm_total_interacoes=data.mgm_total_interacoes,
                mgm_ultima_mensagem=data.mgm_ultima_mensagem,
                mgm_ultima_reacao=data.mgm_ultima_reacao,
                mgm_engajamento_percent=data.mgm_engajamento_percent,
                
                # Status Flags
                esta_na_comunidade=data.esta_na_comunidade,
                esta_no_grupo_mentoria=data.esta_no_grupo_mentoria,
                esta_no_papo_impulso=data.esta_no_papo_impulso,
                interacao_nos_grupos=data.interacao_nos_grupos,
                ativo_na_ludos=data.ativo_na_ludos,
                fazendo_mentoria=data.fazendo_mentoria,
                solicitou_credito=data.solicitou_credito,
                
                # NPS Scores
                nps_geral=data.nps_geral,
                nps_mentoria=data.nps_mentoria,
                nps_ludos=data.nps_ludos
            )
            
            session.add(empreendedor)
            session.commit()
            session.refresh(empreendedor)
            
            logger.info(f"Empreendedor criado: ID={empreendedor.id}, Nome={empreendedor.nome}")
            return True, empreendedor, None
            
        except IntegrityError as e:
            session.rollback()
            logger.error(f"Erro de integridade ao criar empreendedor: {e}")
            return False, None, "Dados duplicados ou inválidos"
        
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro SQL ao criar empreendedor: {e}")
            return False, None, str(e)
        
        except Exception as e:
            session.rollback()
            logger.error(f"Erro inesperado ao criar empreendedor: {e}")
            return False, None, str(e)
        
        finally:
            session.close()
    
    def get_empreendedor_by_id(self, empreendedor_id: int) -> Optional[Empreendedor]:
        """Buscar empreendedor por ID"""
        session = self.get_session()
        try:
            return session.query(Empreendedor).filter(
                Empreendedor.id == empreendedor_id
            ).first()
        finally:
            session.close()
    
    def get_empreendedor_by_telefone(self, telefone: str) -> Optional[Empreendedor]:
        """Buscar empreendedor por telefone"""
        session = self.get_session()
        try:
            return session.query(Empreendedor).filter(
                Empreendedor.telefone == telefone
            ).first()
        finally:
            session.close()
    
    def get_empreendedor_by_email(self, email: str) -> Optional[Empreendedor]:
        """Buscar empreendedor por email"""
        session = self.get_session()
        try:
            return session.query(Empreendedor).filter(
                Empreendedor.email == email
            ).first()
        finally:
            session.close()
    
    def get_empreendedor_by_cpf(self, cpf: str) -> Optional[Empreendedor]:
        """Buscar empreendedor por CPF"""
        session = self.get_session()
        try:
            return session.query(Empreendedor).filter(
                Empreendedor.cpf == cpf
            ).first()
        finally:
            session.close()
    
    def search_empreendedores(
        self, 
        filters: EmpreendedorSearchRequest
    ) -> Tuple[List[Empreendedor], int]:
        """
        Buscar empreendedores com filtros
        
        Returns:
            Tuple[List[Empreendedor], int]: (lista de empreendedores, total)
        """
        session = self.get_session()
        try:
            query = session.query(Empreendedor)
            
            # Aplicar filtros
            if filters.nome:
                query = query.filter(Empreendedor.nome.ilike(f"%{filters.nome}%"))
            
            if filters.telefone:
                query = query.filter(Empreendedor.telefone.like(f"%{filters.telefone}%"))
            
            if filters.email:
                query = query.filter(Empreendedor.email.ilike(f"%{filters.email}%"))
            
            if filters.cpf:
                query = query.filter(Empreendedor.cpf == filters.cpf)
            
            if filters.cidade:
                query = query.filter(Empreendedor.cidade.ilike(f"%{filters.cidade}%"))
            
            if filters.estado:
                query = query.filter(Empreendedor.estado == filters.estado)
            
            if filters.comunidade_originadora:
                query = query.filter(
                    Empreendedor.comunidade_originadora == filters.comunidade_originadora
                )
            
            if filters.formulario_tipo:
                query = query.filter(Empreendedor.formulario_tipo == filters.formulario_tipo)
            
            if filters.data_inscricao_inicio:
                query = query.filter(Empreendedor.data_inscricao >= filters.data_inscricao_inicio)
            
            if filters.data_inscricao_fim:
                query = query.filter(Empreendedor.data_inscricao <= filters.data_inscricao_fim)
            
            if filters.ativo_na_ludos is not None:
                query = query.filter(Empreendedor.ativo_na_ludos == filters.ativo_na_ludos)
            
            if filters.fazendo_mentoria is not None:
                query = query.filter(Empreendedor.fazendo_mentoria == filters.fazendo_mentoria)
            
            # Contar total
            total = query.count()
            
            # Aplicar paginação
            offset = (filters.page - 1) * filters.page_size
            empreendedores = query.offset(offset).limit(filters.page_size).all()
            
            return empreendedores, total
            
        finally:
            session.close()
    
    def update_empreendedor(
        self, 
        empreendedor_id: int, 
        updates: EmpreendedorUpdateRequest
    ) -> Tuple[bool, Optional[str]]:
        """
        Atualizar empreendedor
        
        Returns:
            Tuple[bool, Optional[str]]: (sucesso, erro)
        """
        session = self.get_session()
        try:
            empreendedor = session.query(Empreendedor).filter(
                Empreendedor.id == empreendedor_id
            ).first()
            
            if not empreendedor:
                return False, "Empreendedor não encontrado"
            
            # Atualizar campos
            update_data = updates.dict(exclude_unset=True)
            for key, value in update_data.items():
                if hasattr(empreendedor, key):
                    # Aplicar safe_str em strings
                    if isinstance(value, str) and key in [
                        'nome', 'telefone', 'email', 'apelido', 'cidade', 'estado'
                    ]:
                        max_lengths = {
                            'nome': 100, 'telefone': 20, 'email': 100,
                            'apelido': 100, 'cidade': 100, 'estado': 50
                        }
                        value = self.safe_str(value, max_lengths.get(key, 100))
                    
                    setattr(empreendedor, key, value)
            
            session.commit()
            logger.info(f"Empreendedor atualizado: ID={empreendedor_id}")
            return True, None
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao atualizar empreendedor: {e}")
            return False, str(e)
        
        finally:
            session.close()
    
    def delete_empreendedor(self, empreendedor_id: int) -> Tuple[bool, Optional[str]]:
        """
        Deletar empreendedor
        
        Returns:
            Tuple[bool, Optional[str]]: (sucesso, erro)
        """
        session = self.get_session()
        try:
            empreendedor = session.query(Empreendedor).filter(
                Empreendedor.id == empreendedor_id
            ).first()
            
            if not empreendedor:
                return False, "Empreendedor não encontrado"
            
            session.delete(empreendedor)
            session.commit()
            
            logger.info(f"Empreendedor deletado: ID={empreendedor_id}")
            return True, None
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao deletar empreendedor: {e}")
            return False, str(e)
        
        finally:
            session.close()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas gerais dos empreendedores"""
        session = self.get_session()
        try:
            stats = {
                'total_empreendedores': session.query(func.count(Empreendedor.id)).scalar(),
                'total_ativos_ludos': session.query(func.count(Empreendedor.id)).filter(
                    Empreendedor.ativo_na_ludos == True
                ).scalar(),
                'total_em_mentoria': session.query(func.count(Empreendedor.id)).filter(
                    Empreendedor.fazendo_mentoria == True
                ).scalar(),
                'media_nps_geral': session.query(func.avg(Empreendedor.nps_geral)).filter(
                    Empreendedor.nps_geral.isnot(None)
                ).scalar(),
                'media_nps_mentoria': session.query(func.avg(Empreendedor.nps_mentoria)).filter(
                    Empreendedor.nps_mentoria.isnot(None)
                ).scalar(),
                'media_nps_ludos': session.query(func.avg(Empreendedor.nps_ludos)).filter(
                    Empreendedor.nps_ludos.isnot(None)
                ).scalar(),
            }
            
            # Total por comunidade
            stats['total_por_comunidade'] = dict(
                session.query(
                    Empreendedor.comunidade_originadora,
                    func.count(Empreendedor.id)
                ).filter(
                    Empreendedor.comunidade_originadora.isnot(None)
                ).group_by(Empreendedor.comunidade_originadora).all()
            )
            
            # Total por estado
            stats['total_por_estado'] = dict(
                session.query(
                    Empreendedor.estado,
                    func.count(Empreendedor.id)
                ).filter(
                    Empreendedor.estado.isnot(None)
                ).group_by(Empreendedor.estado).all()
            )
            
            # Total por segmento
            stats['total_por_segmento'] = dict(
                session.query(
                    Empreendedor.segmento_atuacao,
                    func.count(Empreendedor.id)
                ).filter(
                    Empreendedor.segmento_atuacao.isnot(None)
                ).group_by(Empreendedor.segmento_atuacao).all()
            )
            
            return stats
            
        finally:
            session.close()
    
    def bulk_create(
        self, 
        empreendedores_data: List[EmpreendedorCreateRequest]
    ) -> Tuple[int, int, List[str]]:
        """
        Criar múltiplos empreendedores em lote
        
        Returns:
            Tuple[int, int, List[str]]: (total_sucesso, total_erro, lista_de_erros)
        """
        sucesso = 0
        erros = []
        
        for idx, data in enumerate(empreendedores_data):
            success, _, error = self.create_empreendedor(data)
            if success:
                sucesso += 1
            else:
                erros.append(f"Registro {idx + 1}: {error}")
        
        return sucesso, len(erros), erros

