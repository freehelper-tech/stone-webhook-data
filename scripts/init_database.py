"""
Script para inicializar o banco de dados
Cria todas as tabelas necessárias
"""
import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.empreendedor_repository import EmpreendedorRepository
from models.impulso_models import Base
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Inicializar banco de dados"""
    try:
        logger.info("Iniciando criação das tabelas...")
        
        # Criar repositório (isso já cria as tabelas)
        repo = EmpreendedorRepository()
        
        logger.info("✓ Tabelas criadas/verificadas com sucesso!")
        
        # Verificar se consegue fazer query
        stats = repo.get_stats()
        logger.info(f"✓ Conexão com banco verificada!")
        logger.info(f"  Total de empreendedores: {stats['total_empreendedores']}")
        
        # Listar tabelas criadas
        logger.info("\nTabelas criadas:")
        logger.info("  - empreendedores")
        logger.info("  - mentores")
        logger.info("  - status_mentoria")
        logger.info("  - creditos")
        logger.info("  - nps_scores")
        logger.info("  - ludos_atividades")
        
        logger.info("\n✅ Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar banco: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

