"""
API de Webhook para receber dados do Jotform
Endpoints para processar formulários de empreendedores
"""
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import logging
import time
import json
from datetime import datetime

from app.dto.webhook_dtos import (
    JotformWebhookPayload,
    EmpreendedorCreateRequest,
    EmpreendedorResponse,
    WebhookResponse,
    BulkWebhookResponse,
    EmpreendedorSearchRequest,
    EmpreendedorUpdateRequest,
    EmpreendedorStatsResponse
)
from app.data.empreendedor_repository import EmpreendedorRepository
from app.utils.jotform_processor import JotformProcessor
from app.models.impulso_models import Empreendedor

logger = logging.getLogger(__name__)

# Criar router
router = APIRouter(
    prefix="/webhook",
    tags=["Webhook Jotform"]
)

# Instância do repositório
repo = EmpreendedorRepository()
processor = JotformProcessor()


@router.post("/jotform")
async def receber_webhook_jotform(request: Request):
    """
    Receber webhook do Jotform com dados de empreendedor
    
    Este endpoint aceita QUALQUER formato JSON do Jotform e processa automaticamente.
    A API é totalmente flexível e se adapta ao formato recebido.
    
    **Retorna:**
    - success: boolean indicando sucesso
    - message: mensagem descritiva
    - empreendedor_id: ID do empreendedor criado (se sucesso)
    - data: dados completos do empreendedor (se sucesso)
    - raw_payload: payload original recebido (em caso de erro)
    """
    start_time = time.time()
    
    try:
        # LOG DO REQUEST RECEBIDO
        logger.info("="*80)
        logger.info("🎯 WEBHOOK JOTFORM RECEBIDO")
        logger.info("="*80)
        logger.info(f"📋 Headers recebidos:")
        for key, value in request.headers.items():
            logger.info(f"   {key}: {value}")
        logger.info("-"*80)
        
        # Capturar body bruto
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8')
        
        logger.info(f"📦 Body bruto (tamanho: {len(body_str)} bytes):")
        logger.info(f"{body_str[:1000]}")  # Primeiros 1000 caracteres
        logger.info("-"*80)
        
        # Verificar se body está vazio
        if not body_str or body_str.strip() == "":
            logger.error("❌ Body vazio recebido!")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": "Body vazio recebido. Verifique a configuração do webhook no Jotform.",
                    "headers": dict(request.headers)
                }
            )
        
        # Tentar parsear como JSON
        try:
            raw_payload = json.loads(body_str)
            logger.info("✅ Body parseado como JSON com sucesso")
        except json.JSONDecodeError as e:
            # Pode ser form-data
            logger.warning(f"⚠️ Body não é JSON válido: {e}")
            logger.info("🔄 Tentando parsear como form-data...")
            
            # Tentar pegar do form
            form_data = await request.form()
            if form_data:
                raw_payload = dict(form_data)
                logger.info("✅ Body parseado como form-data com sucesso")
            else:
                logger.error("❌ Não conseguiu parsear como JSON nem form-data")
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "message": "Não foi possível parsear o body. Formato não suportado.",
                        "body_recebido": body_str[:500],
                        "headers": dict(request.headers)
                    }
                )
        
        # LOG DO PAYLOAD PARSEADO
        logger.info(f"📥 Payload parseado:")
        logger.info(json.dumps(raw_payload, indent=2, ensure_ascii=False))
        logger.info("="*80)
        
        # ⚠️ JOTFORM PODE ENVIAR EM DIFERENTES FORMATOS
        
        # CASO 1: Array [{...}]
        if isinstance(raw_payload, list):
            logger.info(f"🔄 Payload é um ARRAY com {len(raw_payload)} item(s)")
            if len(raw_payload) == 0:
                logger.error("❌ Array vazio recebido!")
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "message": "Array vazio recebido",
                        "raw_payload": raw_payload
                    }
                )
            
            raw_payload = raw_payload[0]
            logger.info("✅ Extraído primeiro elemento do array")
        
        # CASO 2: Form-data do Jotform com rawRequest
        if isinstance(raw_payload, dict) and "rawRequest" in raw_payload:
            logger.info("🔄 Detectado formato form-data do Jotform com rawRequest")
            logger.info(f"📋 Metadados: formID={raw_payload.get('formID')}, submissionID={raw_payload.get('submissionID')}")
            
            try:
                # Parsear rawRequest (é uma string JSON)
                raw_request_str = raw_payload.get("rawRequest", "{}")
                raw_request_data = json.loads(raw_request_str)
                logger.info("✅ rawRequest parseado com sucesso")
                
                # Mapear campos q2_nome, q3_email, etc. para formato esperado
                mapped_payload = {}
                
                # Mapear cada campo do Jotform
                for key, value in raw_request_data.items():
                    # Nome (q2_nome, q5_nome, etc.)
                    if "nome" in key.lower() and isinstance(value, dict) and "first" in value:
                        mapped_payload["Nome"] = value
                    elif "nome" in key.lower() and isinstance(value, str):
                        mapped_payload["nome"] = value
                    
                    # Email (q3_email, etc.)
                    elif "email" in key.lower():
                        mapped_payload["E-mail"] = value
                    
                    # Telefone (q4_telefone, etc.)
                    elif "telefone" in key.lower() and isinstance(value, dict):
                        mapped_payload["Telefone"] = value
                    elif "telefone" in key.lower():
                        mapped_payload["telefone"] = value
                    
                    # CPF
                    elif "cpf" in key.lower() or "aqui" in key.lower():
                        mapped_payload["CPF"] = value
                    
                    # Cidade
                    elif "cidade" in key.lower():
                        mapped_payload["Cidade"] = value
                    
                    # Estado
                    elif "estado" in key.lower():
                        mapped_payload["Estado"] = value
                    
                    # Idade
                    elif "idade" in key.lower():
                        mapped_payload["Idade"] = value
                    
                    # Gênero
                    elif "genero" in key.lower():
                        mapped_payload["Gênero"] = value
                    
                    # Raça/cor
                    elif "raca" in key.lower() or "cor" in key.lower():
                        mapped_payload["Raça/cor"] = value
                    
                    # Escolaridade
                    elif "escolaridade" in key.lower():
                        mapped_payload["Escolaridade"] = value
                    
                    # Renda
                    elif "renda" in key.lower() and "insira" in key.lower():
                        mapped_payload["Faixa de renda familiar mensal"] = value
                    
                    # Fontes de renda
                    elif "quaissao" in key.lower().replace("_", "").replace(" ", ""):
                        mapped_payload["Quais são as suas fontes de renda atualmente?"] = value
                    
                    # Tempo de funcionamento
                    elif "tempode" in key.lower().replace("_", "").replace(" ", ""):
                        mapped_payload["Tempo de funcionamento do negócio"] = value
                    
                    # Segmento
                    elif "segmentode" in key.lower().replace("_", "").replace(" ", ""):
                        mapped_payload["Segmento de atuação"] = value
                    elif "seoutros" in key.lower().replace("_", "").replace(" ", ""):
                        mapped_payload["Se outros, qual o segmento de atuação do seu négocio?"] = value
                    
                    # Organização Stone
                    elif "insirauma58" in key.lower().replace("_", "").replace(" ", ""):
                        mapped_payload["Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?"] = value
                
                # Adicionar metadados úteis
                mapped_payload["submissionID"] = raw_payload.get("submissionID")
                mapped_payload["formID"] = raw_payload.get("formID")
                
                raw_payload = mapped_payload
                logger.info("✅ Campos mapeados com sucesso")
                logger.info(f"📦 Payload mapeado:")
                logger.info(json.dumps(raw_payload, indent=2, ensure_ascii=False))
                logger.info("-"*80)
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ Erro ao parsear rawRequest: {e}")
            except Exception as e:
                logger.error(f"❌ Erro ao mapear campos: {e}")
        
        logger.info(f"📦 Payload final para processar:")
        logger.info(json.dumps(raw_payload, indent=2, ensure_ascii=False))
        logger.info("-"*80)
        
        # Tentar converter para JotformWebhookPayload (flexível)
        try:
            payload = JotformWebhookPayload(**raw_payload)
            logger.info("✅ Payload validado com sucesso")
        except Exception as e:
            logger.warning(f"⚠️ Payload não segue formato esperado, mas vamos tentar processar: {e}")
            # Mesmo assim, vamos tentar processar
            payload = JotformWebhookPayload(**raw_payload)
        
        # Validar campos mínimos
        if not processor.validar_payload(raw_payload):
            logger.error("❌ Payload não possui campos mínimos obrigatórios (Nome e Telefone)")
            logger.info(f"🔍 Campos disponíveis no payload: {list(raw_payload.keys())}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": "Payload inválido: campos obrigatórios ausentes (Nome e Telefone)",
                    "raw_payload": raw_payload,
                    "campos_disponiveis": list(raw_payload.keys()),
                    "campos_esperados": {
                        "nome": "Nome, nome, ou objeto {first, last}",
                        "telefone": "Telefone, telefone, ou objeto {area, phone}"
                    }
                }
            )
        
        # Processar payload do Jotform
        try:
            empreendedor_data = processor.payload_to_empreendedor(payload)
            logger.info(f"✅ Dados processados: Nome={empreendedor_data.nome}, Telefone={empreendedor_data.telefone}")
        except Exception as e:
            logger.error(f"❌ Erro ao processar dados: {e}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": f"Erro ao processar dados: {str(e)}",
                    "raw_payload": raw_payload
                }
            )
        
        # Criar empreendedor no banco
        logger.info("💾 Tentando salvar no banco de dados...")
        success, empreendedor, error = repo.create_empreendedor(empreendedor_data)
        
        if not success:
            logger.error(f"❌ Erro ao salvar no banco: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "message": f"Erro ao criar empreendedor: {error}",
                    "raw_payload": raw_payload
                }
            )
        
        # Sucesso!
        processing_time = (time.time() - start_time) * 1000
        logger.info("="*80)
        logger.info(f"✅ SUCESSO! Empreendedor criado: ID={empreendedor.id}")
        logger.info(f"   Nome: {empreendedor.nome}")
        logger.info(f"   Telefone: {empreendedor.telefone}")
        logger.info(f"   Email: {empreendedor.email}")
        logger.info(f"   Tempo de processamento: {processing_time:.2f}ms")
        logger.info("="*80)
        
        # Preparar resposta
        empreendedor_response = EmpreendedorResponse(
            id=empreendedor.id,
            nome=empreendedor.nome,
            telefone=empreendedor.telefone,
            email=empreendedor.email,
            cpf=empreendedor.cpf,
            cidade=empreendedor.cidade,
            estado=empreendedor.estado,
            data_inscricao=empreendedor.data_inscricao,
            formulario_tipo=empreendedor.formulario_tipo
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Empreendedor cadastrado com sucesso",
                "empreendedor_id": empreendedor.id,
                "data": {
                    "id": empreendedor.id,
                    "nome": empreendedor.nome,
                    "telefone": empreendedor.telefone,
                    "email": empreendedor.email,
                    "cpf": empreendedor.cpf,
                    "cidade": empreendedor.cidade,
                    "estado": empreendedor.estado,
                    "data_inscricao": empreendedor.data_inscricao.isoformat() if empreendedor.data_inscricao else None,
                    "formulario_tipo": empreendedor.formulario_tipo
                },
                "tempo_processamento_ms": processing_time
            }
        )
        
    except Exception as e:
        logger.error("="*80)
        logger.error(f"❌ ERRO INESPERADO ao processar webhook")
        logger.error(f"Erro: {e}")
        logger.error("="*80, exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Erro interno: {str(e)}",
                "raw_payload": raw_payload if 'raw_payload' in locals() else None
            }
        )


@router.post("/jotform/bulk", response_model=BulkWebhookResponse)
async def receber_webhook_jotform_bulk(payloads: List[JotformWebhookPayload]):
    """
    Receber múltiplos webhooks do Jotform em lote
    
    Este endpoint processa múltiplos formulários de uma vez.
    Útil para importações em massa ou sincronizações.
    
    **Retorna:**
    - total_processados: total de registros processados
    - total_sucesso: total de sucessos
    - total_erros: total de erros
    - resultados: lista detalhada de cada resultado
    """
    start_time = time.time()
    
    try:
        logger.info(f"Webhook bulk recebido: {len(payloads)} registros")
        
        resultados = []
        total_sucesso = 0
        total_erros = 0
        
        for idx, payload in enumerate(payloads):
            try:
                # Validar payload
                if not processor.validar_payload(payload.dict()):
                    resultados.append(WebhookResponse(
                        success=False,
                        message=f"Registro {idx + 1}: Payload inválido",
                        errors=["Campos obrigatórios ausentes"]
                    ))
                    total_erros += 1
                    continue
                
                # Processar payload
                empreendedor_data = processor.payload_to_empreendedor(payload)
                
                # Criar empreendedor
                success, empreendedor, error = repo.create_empreendedor(empreendedor_data)
                
                if success:
                    resultados.append(WebhookResponse(
                        success=True,
                        message=f"Registro {idx + 1}: Sucesso",
                        empreendedor_id=empreendedor.id,
                        data=EmpreendedorResponse(
                            id=empreendedor.id,
                            nome=empreendedor.nome,
                            telefone=empreendedor.telefone,
                            email=empreendedor.email,
                            cpf=empreendedor.cpf,
                            cidade=empreendedor.cidade,
                            estado=empreendedor.estado,
                            data_inscricao=empreendedor.data_inscricao,
                            formulario_tipo=empreendedor.formulario_tipo
                        )
                    ))
                    total_sucesso += 1
                else:
                    resultados.append(WebhookResponse(
                        success=False,
                        message=f"Registro {idx + 1}: Erro",
                        errors=[error]
                    ))
                    total_erros += 1
                
            except Exception as e:
                logger.error(f"Erro ao processar registro {idx + 1}: {e}")
                resultados.append(WebhookResponse(
                    success=False,
                    message=f"Registro {idx + 1}: Erro inesperado",
                    errors=[str(e)]
                ))
                total_erros += 1
        
        processing_time = (time.time() - start_time) * 1000
        logger.info(
            f"Webhook bulk processado: {total_sucesso} sucessos, "
            f"{total_erros} erros em {processing_time:.2f}ms"
        )
        
        return BulkWebhookResponse(
            success=total_erros == 0,
            total_processados=len(payloads),
            total_sucesso=total_sucesso,
            total_erros=total_erros,
            resultados=resultados,
            tempo_processamento_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Erro fatal ao processar webhook bulk: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )


@router.post("/jotform/raw", response_model=WebhookResponse)
async def receber_webhook_jotform_raw(request: Request):
    """
    Receber webhook do Jotform em formato bruto (raw JSON)
    
    Este endpoint aceita qualquer estrutura JSON e tenta processar.
    Útil quando a estrutura do formulário muda ou para debugging.
    """
    try:
        raw_data = await request.json()
        logger.info("Webhook raw recebido")
        logger.debug(f"Raw data: {raw_data}")
        
        # Tentar converter para JotformWebhookPayload
        try:
            payload = JotformWebhookPayload(**raw_data)
        except Exception as e:
            logger.error(f"Erro ao converter raw data: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Formato de dados inválido: {str(e)}"
            )
        
        # Processar normalmente
        return await receber_webhook_jotform(payload)
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erro ao processar webhook raw: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


# ===== ENDPOINTS DE GESTÃO DE EMPREENDEDORES =====

@router.get("/empreendedores/{empreendedor_id}", response_model=EmpreendedorResponse)
async def obter_empreendedor(empreendedor_id: int):
    """
    Obter dados de um empreendedor por ID
    """
    try:
        empreendedor = repo.get_empreendedor_by_id(empreendedor_id)
        
        if not empreendedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empreendedor {empreendedor_id} não encontrado"
            )
        
        return EmpreendedorResponse(
            id=empreendedor.id,
            nome=empreendedor.nome,
            telefone=empreendedor.telefone,
            email=empreendedor.email,
            cpf=empreendedor.cpf,
            cidade=empreendedor.cidade,
            estado=empreendedor.estado,
            data_inscricao=empreendedor.data_inscricao,
            formulario_tipo=empreendedor.formulario_tipo
        )
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erro ao buscar empreendedor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/empreendedores/search")
async def buscar_empreendedores(filters: EmpreendedorSearchRequest):
    """
    Buscar empreendedores com filtros
    
    Permite filtrar por:
    - nome, telefone, email, cpf
    - cidade, estado
    - comunidade_originadora, formulario_tipo
    - data_inscricao (range)
    - flags booleanas (ativo_na_ludos, fazendo_mentoria)
    """
    try:
        empreendedores, total = repo.search_empreendedores(filters)
        
        resultados = [
            EmpreendedorResponse(
                id=emp.id,
                nome=emp.nome,
                telefone=emp.telefone,
                email=emp.email,
                cpf=emp.cpf,
                cidade=emp.cidade,
                estado=emp.estado,
                data_inscricao=emp.data_inscricao,
                formulario_tipo=emp.formulario_tipo
            )
            for emp in empreendedores
        ]
        
        return {
            "success": True,
            "total": total,
            "page": filters.page,
            "page_size": filters.page_size,
            "total_pages": (total + filters.page_size - 1) // filters.page_size,
            "data": resultados
        }
        
    except Exception as e:
        logger.error(f"Erro ao buscar empreendedores: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/empreendedores/{empreendedor_id}")
async def atualizar_empreendedor(
    empreendedor_id: int,
    updates: EmpreendedorUpdateRequest
):
    """
    Atualizar dados de um empreendedor
    """
    try:
        success, error = repo.update_empreendedor(empreendedor_id, updates)
        
        if not success:
            if "não encontrado" in error.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=error
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error
                )
        
        return {
            "success": True,
            "message": f"Empreendedor {empreendedor_id} atualizado com sucesso"
        }
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erro ao atualizar empreendedor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/empreendedores/{empreendedor_id}")
async def deletar_empreendedor(empreendedor_id: int):
    """
    Deletar um empreendedor
    
    ⚠️ ATENÇÃO: Esta operação não pode ser desfeita!
    """
    try:
        success, error = repo.delete_empreendedor(empreendedor_id)
        
        if not success:
            if "não encontrado" in error.lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=error
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error
                )
        
        return {
            "success": True,
            "message": f"Empreendedor {empreendedor_id} deletado com sucesso"
        }
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Erro ao deletar empreendedor: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/empreendedores/stats", response_model=EmpreendedorStatsResponse)
async def obter_estatisticas():
    """
    Obter estatísticas gerais dos empreendedores
    
    Retorna:
    - Total de empreendedores
    - Totais por comunidade, estado, segmento
    - Total de ativos na Ludos
    - Total em mentoria
    - Médias de NPS (geral, mentoria, ludos)
    """
    try:
        stats = repo.get_stats()
        return EmpreendedorStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health")
async def health_check():
    """
    Health check do serviço de webhook
    """
    try:
        # Tentar fazer query simples no banco
        stats = repo.get_stats()
        
        return {
            "status": "healthy",
            "service": "webhook-jotform",
            "timestamp": datetime.utcnow(),
            "database": "connected",
            "total_empreendedores": stats.get('total_empreendedores', 0)
        }
        
    except Exception as e:
        logger.error(f"Health check falhou: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "service": "webhook-jotform",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
        )

