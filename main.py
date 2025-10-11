"""
Dashboard Impulso Stone - API de Webhook
API para receber e processar dados de empreendedores do Jotform
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from datetime import datetime

from core.config import settings
from api import webhook

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciar ciclo de vida da aplicação"""
    # Startup
    logger.info("="*80)
    logger.info("🚀 Dashboard Impulso Stone API - Iniciando...")
    logger.info("="*80)
    logger.info("📋 Configurações:")
    logger.info(f"   - Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"   - Debug: {settings.DEBUG}")
    logger.info(f"   - SQL Server: {settings.SQL_SERVER}")
    logger.info(f"   - Database: {settings.SQL_DATABASE}")
    logger.info("="*80)
    logger.info("✅ API iniciada e pronta para receber webhooks!")
    logger.info("📡 Endpoint: POST /api/v1/webhook/jotform")
    logger.info("="*80)
    
    yield
    
    # Shutdown
    logger.info("="*80)
    logger.info("🔄 Encerrando Dashboard Impulso Stone API...")
    logger.info("✅ API encerrada com sucesso!")
    logger.info("="*80)


# Criar aplicação FastAPI
app = FastAPI(
    title="Dashboard Impulso Stone - API de Webhook",
    version="1.0.0",
    description="API para receber e processar dados de empreendedores do formulário Jotform",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log de todas as requisições"""
    start_time = time.time()
    
    # Log da requisição
    logger.info(f"Request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        
        # Calcular tempo de processamento
        process_time = time.time() - start_time
        
        # Log da resposta
        logger.info(
            f"Response: {response.status_code} - "
            f"Time: {process_time:.3f}s - "
            f"Path: {request.url.path}"
        )
        
        # Adicionar header de tempo de processamento
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url} - Error: {e} - Time: {process_time:.3f}s")
        raise


# Handler global de exceções
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "path": str(request.url.path)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "error_code": "INTERNAL_ERROR",
            "path": str(request.url.path)
        }
    )


# Incluir routers
app.include_router(webhook.router, prefix=settings.API_V1_STR)


# Endpoints básicos
@app.get("/")
async def root():
    """Endpoint raiz - Informações da API"""
    return {
        "api": "Dashboard Impulso Stone",
        "version": "1.0.0",
        "status": "online",
        "description": "API de Webhook para processar dados de empreendedores do Jotform",
        "docs": "/docs",
        "health": "/health",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check da aplicação"""
    try:
        # Testar conexão com banco
        from data.empreendedor_repository import EmpreendedorRepository
        repo = EmpreendedorRepository()
        stats = repo.get_stats()
        
        return {
            "status": "healthy",
            "api": "Dashboard Impulso Stone",
            "version": "1.0.0",
            "database": "connected",
            "total_empreendedores": stats['total_empreendedores'],
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check falhou: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "api": "Dashboard Impulso Stone",
                "version": "1.0.0",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
