"""
Modelos SQLAlchemy para Dashboard Impulso Stone
Tabelas: empreendedores, mentores, status_mentoria, creditos, nps_scores, ludos_atividades
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Empreendedor(Base):
    """Modelo para tabela empreendedores"""
    __tablename__ = 'empreendedores'
    
    # Campos Principais (OBRIGATÓRIOS)
    id = Column(Integer, primary_key=True, autoincrement=True)
    telefone = Column(String(20), nullable=False)  # SEM UNIQUE para permitir duplicatas
    nome = Column(String(100), nullable=False)
    email = Column(String(100))
    comunidade_originadora = Column(String(50))
    data_inscricao = Column(DateTime, default=func.now())
    
    # Campos do Formulário Jotform
    apelido = Column(String(100))
    cpf = Column(String(14))
    cidade = Column(String(100))
    estado = Column(String(50))
    idade = Column(String(20))
    genero = Column(String(50))
    raca_cor = Column(String(50))
    escolaridade = Column(String(100))
    faixa_renda = Column(String(100))
    fonte_renda = Column(Text)
    tempo_funcionamento = Column(String(50))
    segmento_atuacao = Column(String(100))
    segmento_outros = Column(String(100))
    organizacao_stone = Column(String(100))
    formulario_tipo = Column(String(50))
    
    # Campos da Plataforma Ludos
    ludos_id = Column(Integer)
    ludos_login = Column(String(100))
    ludos_status = Column(String(20))
    ludos_pontos = Column(Integer, default=0)
    ludos_moedas = Column(Integer, default=0)
    ludos_nivel = Column(Integer, default=1)
    ludos_primeiro_login = Column(DateTime)
    ludos_ultimo_login = Column(DateTime)
    
    # Campos do MGM (WhatsApp)
    mgm_user_name = Column(String(100))
    mgm_whatsapp = Column(String(20))
    mgm_total_mensagens = Column(Integer, default=0)
    mgm_total_reacoes = Column(Integer, default=0)
    mgm_total_interacoes = Column(Integer, default=0)
    mgm_ultima_mensagem = Column(DateTime)
    mgm_ultima_reacao = Column(DateTime)
    mgm_engajamento_percent = Column(Float, default=0.0)
    
    # Status Flags (Booleanos)
    esta_na_comunidade = Column(Boolean, default=False)
    esta_no_grupo_mentoria = Column(Boolean, default=False)
    esta_no_papo_impulso = Column(Boolean, default=False)
    interacao_nos_grupos = Column(Integer, default=0)
    ativo_na_ludos = Column(Boolean, default=False)
    fazendo_mentoria = Column(Boolean, default=False)
    solicitou_credito = Column(Boolean, default=False)
    
    # NPS Scores
    nps_geral = Column(Integer)  # 0-10
    nps_mentoria = Column(Integer)  # 0-10
    nps_ludos = Column(Integer)  # 0-10
    
    # Relacionamentos
    status_mentorias = relationship("StatusMentoria", back_populates="empreendedor")
    creditos = relationship("Credito", back_populates="empreendedor")
    nps_scores = relationship("NPSScore", back_populates="empreendedor")
    ludos_atividades = relationship("LudosAtividade", back_populates="empreendedor")
    
    def __repr__(self):
        return f"<Empreendedor(id={self.id}, nome='{self.nome}', telefone='{self.telefone}')>"


class Mentor(Base):
    """Modelo para tabela mentores"""
    __tablename__ = 'mentores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    
    # Relacionamentos
    status_mentorias = relationship("StatusMentoria", back_populates="mentor")
    
    def __repr__(self):
        return f"<Mentor(id={self.id}, nome='{self.nome}')>"


class StatusMentoria(Base):
    """Modelo para tabela status_mentoria"""
    __tablename__ = 'status_mentoria'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    empreendedor_id = Column(Integer, ForeignKey('empreendedores.id'), nullable=False)
    mentor_id = Column(Integer, ForeignKey('mentores.id'))
    status = Column(String(50), nullable=False)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    horas_realizadas = Column(Float, default=0.0)
    observacoes = Column(Text)
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    empreendedor = relationship("Empreendedor", back_populates="status_mentorias")
    mentor = relationship("Mentor", back_populates="status_mentorias")
    
    def __repr__(self):
        return f"<StatusMentoria(id={self.id}, status='{self.status}')>"


class Credito(Base):
    """Modelo para tabela creditos"""
    __tablename__ = 'creditos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    empreendedor_id = Column(Integer, ForeignKey('empreendedores.id'), nullable=False)
    valor_solicitado = Column(Float, nullable=False)
    status = Column(String(50), default='Pendente')
    data_solicitacao = Column(DateTime, default=func.now())
    data_aprovacao = Column(DateTime)
    observacoes = Column(Text)
    
    # Relacionamentos
    empreendedor = relationship("Empreendedor", back_populates="creditos")
    
    def __repr__(self):
        return f"<Credito(id={self.id}, valor={self.valor_solicitado}, status='{self.status}')>"


class NPSScore(Base):
    """Modelo para tabela nps_scores"""
    __tablename__ = 'nps_scores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    empreendedor_id = Column(Integer, ForeignKey('empreendedores.id'), nullable=False)
    tipo_nps = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)  # 0-10
    comentario = Column(Text)
    data_avaliacao = Column(DateTime, default=func.now())
    
    # Relacionamentos
    empreendedor = relationship("Empreendedor", back_populates="nps_scores")
    
    def __repr__(self):
        return f"<NPSScore(id={self.id}, tipo='{self.tipo_nps}', score={self.score})>"


class LudosAtividade(Base):
    """Modelo para tabela ludos_atividades"""
    __tablename__ = 'ludos_atividades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    empreendedor_id = Column(Integer, ForeignKey('empreendedores.id'), nullable=False)
    player_id = Column(Integer)
    course_id = Column(Integer)
    course_name = Column(String(200))
    module_id = Column(Integer)
    module_name = Column(String(200))
    activity_id = Column(Integer)
    activity_name = Column(String(200))
    performance_first = Column(Integer)
    performance_best = Column(Integer)
    total_plays = Column(Integer, default=0)
    completed_plays = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    points_first = Column(Integer, default=0)
    points_best = Column(Integer, default=0)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    conclusion_time = Column(Integer)
    course_published = Column(Boolean, default=False)
    last_visit = Column(DateTime)
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    empreendedor = relationship("Empreendedor", back_populates="ludos_atividades")
    
    def __repr__(self):
        return f"<LudosAtividade(id={self.id}, course='{self.course_name}')>"

