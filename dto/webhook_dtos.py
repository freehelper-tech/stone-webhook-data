"""
DTOs para Webhook do Jotform
Data Transfer Objects para receber e processar dados do formulário
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, validator


# ===== JOTFORM REQUEST DTOs =====

class JotformNomeObject(BaseModel):
    """Objeto de nome do Jotform"""
    first: str
    last: str


class JotformTelefoneObject(BaseModel):
    """Objeto de telefone do Jotform"""
    area: str
    phone: str


class JotformWebhookPayload(BaseModel):
    """
    Payload do webhook Jotform
    Estrutura recebida do formulário de empreendedores
    """
    # Campos obrigatórios
    Nome: Optional[JotformNomeObject] = None
    nome: Optional[str] = Field(None, description="Nome completo alternativo")
    
    # Contato
    email: Optional[str] = Field(None, alias="E-mail")
    Email: Optional[str] = None
    Telefone: Optional[JotformTelefoneObject] = None
    telefone: Optional[str] = None
    
    # Documentos
    CPF: Optional[str] = None
    cpf: Optional[str] = None
    
    # Localização
    Cidade: Optional[str] = None
    cidade: Optional[str] = None
    Estado: Optional[str] = None
    estado: Optional[str] = None
    
    # Demográficos
    Idade: Optional[str] = None
    idade: Optional[str] = None
    Genero: Optional[str] = Field(None, alias="Gênero")
    genero: Optional[str] = None
    raca_cor: Optional[str] = Field(None, alias="Raça/cor")
    
    # Educação
    Escolaridade: Optional[str] = None
    escolaridade: Optional[str] = None
    
    # Renda
    faixa_renda: Optional[str] = Field(None, alias="Faixa de renda familiar mensal")
    fontes_renda: Optional[List[str]] = Field(None, alias="Quais são as suas fontes de renda atualmente?")
    fonte_renda: Optional[str] = None
    
    # Negócio
    tempo_funcionamento: Optional[str] = Field(None, alias="Tempo de funcionamento do negócio")
    segmento_atuacao: Optional[str] = Field(None, alias="Segmento de atuação")
    segmento_outros: Optional[str] = Field(None, alias="Se outros, qual o segmento de atuação do seu négocio?")
    organizacao_stone: Optional[str] = Field(None, alias="Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?")
    
    # Apelido
    apelido: Optional[str] = None
    
    class Config:
        populate_by_name = True  # Pydantic 2.x
        extra = "allow"  # Permite campos extras - ACEITA QUALQUER CAMPO


class EmpreendedorCreateRequest(BaseModel):
    """DTO para criação de empreendedor processado"""
    # Campos obrigatórios
    nome: str = Field(..., min_length=1, max_length=100)
    telefone: str = Field(..., min_length=1, max_length=20)
    
    # Campos principais
    email: Optional[str] = Field(None, max_length=100)
    comunidade_originadora: Optional[str] = Field(None, max_length=50)
    data_inscricao: Optional[datetime] = None
    
    # Campos do formulário (limites aumentados para aceitar qualquer valor)
    apelido: Optional[str] = Field(None, max_length=200)
    cpf: Optional[str] = Field(None, max_length=50)
    cidade: Optional[str] = Field(None, max_length=200)
    estado: Optional[str] = Field(None, max_length=100)
    idade: Optional[str] = Field(None, max_length=100)
    genero: Optional[str] = Field(None, max_length=100)
    raca_cor: Optional[str] = Field(None, max_length=100)
    escolaridade: Optional[str] = Field(None, max_length=200)
    faixa_renda: Optional[str] = Field(None, max_length=200)
    fonte_renda: Optional[str] = None
    tempo_funcionamento: Optional[str] = Field(None, max_length=100)
    segmento_atuacao: Optional[str] = Field(None, max_length=200)
    segmento_outros: Optional[str] = Field(None, max_length=200)
    organizacao_stone: Optional[str] = Field(None, max_length=200)
    formulario_tipo: Optional[str] = Field(None, max_length=100)
    
    # Campos Ludos (opcionais)
    ludos_id: Optional[int] = None
    ludos_login: Optional[str] = Field(None, max_length=100)
    ludos_status: Optional[str] = Field(None, max_length=20)
    ludos_pontos: int = 0
    ludos_moedas: int = 0
    ludos_nivel: int = 1
    ludos_primeiro_login: Optional[datetime] = None
    ludos_ultimo_login: Optional[datetime] = None
    
    # Campos MGM (opcionais)
    mgm_user_name: Optional[str] = Field(None, max_length=100)
    mgm_whatsapp: Optional[str] = Field(None, max_length=20)
    mgm_total_mensagens: int = 0
    mgm_total_reacoes: int = 0
    mgm_total_interacoes: int = 0
    mgm_ultima_mensagem: Optional[datetime] = None
    mgm_ultima_reacao: Optional[datetime] = None
    mgm_engajamento_percent: float = 0.0
    
    # Status Flags
    esta_na_comunidade: bool = False
    esta_no_grupo_mentoria: bool = False
    esta_no_papo_impulso: bool = False
    interacao_nos_grupos: int = 0
    ativo_na_ludos: bool = False
    fazendo_mentoria: bool = False
    solicitou_credito: bool = False
    
    # NPS Scores
    nps_geral: Optional[int] = Field(None, ge=0, le=10)
    nps_mentoria: Optional[int] = Field(None, ge=0, le=10)
    nps_ludos: Optional[int] = Field(None, ge=0, le=10)


# ===== RESPONSE DTOs =====

class EmpreendedorResponse(BaseModel):
    """DTO de resposta com dados do empreendedor"""
    id: int
    nome: str
    telefone: str
    email: Optional[str]
    cpf: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    data_inscricao: Optional[datetime]
    formulario_tipo: Optional[str]
    
    class Config:
        from_attributes = True  # Pydantic 2.x (antes era orm_mode)


class WebhookResponse(BaseModel):
    """DTO de resposta do webhook"""
    success: bool
    message: str
    empreendedor_id: Optional[int] = None
    data: Optional[EmpreendedorResponse] = None
    errors: Optional[List[str]] = None


class BulkWebhookResponse(BaseModel):
    """DTO de resposta para webhook em lote"""
    success: bool
    total_processados: int
    total_sucesso: int
    total_erros: int
    resultados: List[WebhookResponse]
    tempo_processamento_ms: Optional[float] = None


# ===== QUERY/UPDATE DTOs =====

class EmpreendedorSearchRequest(BaseModel):
    """DTO para busca de empreendedores"""
    nome: Optional[str] = Field(None, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    cpf: Optional[str] = Field(None, max_length=14)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    comunidade_originadora: Optional[str] = Field(None, max_length=50)
    formulario_tipo: Optional[str] = Field(None, max_length=50)
    data_inscricao_inicio: Optional[datetime] = None
    data_inscricao_fim: Optional[datetime] = None
    ativo_na_ludos: Optional[bool] = None
    fazendo_mentoria: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class EmpreendedorUpdateRequest(BaseModel):
    """DTO para atualização de empreendedor"""
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    apelido: Optional[str] = Field(None, max_length=100)
    cidade: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    
    # Status flags
    esta_na_comunidade: Optional[bool] = None
    esta_no_grupo_mentoria: Optional[bool] = None
    esta_no_papo_impulso: Optional[bool] = None
    ativo_na_ludos: Optional[bool] = None
    fazendo_mentoria: Optional[bool] = None
    solicitou_credito: Optional[bool] = None
    
    # NPS
    nps_geral: Optional[int] = Field(None, ge=0, le=10)
    nps_mentoria: Optional[int] = Field(None, ge=0, le=10)
    nps_ludos: Optional[int] = Field(None, ge=0, le=10)


class EmpreendedorStatsResponse(BaseModel):
    """DTO para estatísticas de empreendedores"""
    total_empreendedores: int
    total_por_comunidade: Dict[str, int]
    total_por_estado: Dict[str, int]
    total_por_segmento: Dict[str, int]
    total_ativos_ludos: int
    total_em_mentoria: int
    media_nps_geral: Optional[float]
    media_nps_mentoria: Optional[float]
    media_nps_ludos: Optional[float]

