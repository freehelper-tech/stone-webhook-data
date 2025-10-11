"""
Script para testar conexão com o banco de dados
"""
import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import settings
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_connection():
    """Testar conexão com banco de dados"""
    try:
        logger.info("Testando conexão com banco de dados...")
        logger.info(f"Servidor: {settings.SQL_SERVER}")
        logger.info(f"Database: {settings.SQL_DATABASE}")
        logger.info(f"Usuario: {settings.SQL_USERNAME}")
        
        # Criar engine
        engine = create_engine(
            settings.sql_connection_string,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
            echo=False
        )
        
        # Testar conexão
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()
            
            if value == 1:
                logger.info("✅ Conexão estabelecida com sucesso!")
                
                # Obter versão do SQL Server
                result = connection.execute(text("SELECT @@VERSION"))
                version = result.scalar()
                logger.info(f"\nVersão do SQL Server:")
                logger.info(f"  {version[:100]}...")
                
                # Obter nome do database
                result = connection.execute(text("SELECT DB_NAME()"))
                db_name = result.scalar()
                logger.info(f"\nDatabase atual: {db_name}")
                
                # Listar tabelas existentes
                query = text("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                    AND TABLE_NAME IN (
                        'empreendedores', 'mentores', 'status_mentoria', 
                        'creditos', 'nps_scores', 'ludos_atividades'
                    )
                    ORDER BY TABLE_NAME
                """)
                result = connection.execute(query)
                tables = [row[0] for row in result]
                
                if tables:
                    logger.info(f"\nTabelas encontradas ({len(tables)}):")
                    for table in tables:
                        logger.info(f"  ✓ {table}")
                else:
                    logger.warning("\n⚠ Nenhuma tabela encontrada. Execute init_database.py para criar as tabelas.")
                
                return True
            else:
                logger.error("❌ Falha na conexão: resposta inesperada")
                return False
                
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {e}")
        logger.error("\nVerifique:")
        logger.error("  1. As credenciais no arquivo .env")
        logger.error("  2. Se o firewall permite conexões do seu IP")
        logger.error("  3. Se o driver ODBC está instalado")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

