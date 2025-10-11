"""
Script simples para testar conexão e verificar dados na tabela empreendedores
"""
import sys
import os
from datetime import datetime

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def testar_conexao():
    """Testar conexão com o banco Azure"""
    print("🔗 Testando conexão com Azure SQL...")
    print(f"📋 Connection String: {settings.sql_connection_string[:50]}...")
    
    try:
        engine = create_engine(settings.sql_connection_string)
        
        with engine.connect() as conn:
            print("✅ Conexão estabelecida com sucesso!")
            
            # Testar query simples
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            print(f"✅ Query de teste funcionou: {test_value}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def verificar_tabela_empreendedores():
    """Verificar se a tabela empreendedores existe e tem dados"""
    print("\n📊 Verificando tabela empreendedores...")
    
    try:
        engine = create_engine(settings.sql_connection_string)
        
        with engine.connect() as conn:
            # Verificar se a tabela existe
            result = conn.execute(text("""
                SELECT COUNT(*) as total 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'empreendedores'
            """))
            
            table_exists = result.fetchone()[0] > 0
            
            if not table_exists:
                print("❌ Tabela 'empreendedores' não existe!")
                return False
            
            print("✅ Tabela 'empreendedores' existe!")
            
            # Contar registros
            result = conn.execute(text("SELECT COUNT(*) as total FROM empreendedores"))
            total = result.fetchone()[0]
            
            print(f"📈 Total de registros na tabela: {total}")
            
            if total == 0:
                print("⚠️ Tabela está vazia!")
                return False
            
            # Mostrar últimos 5 registros
            print(f"\n📋 Últimos 5 registros:")
            result = conn.execute(text("""
                SELECT TOP 5 
                    id, nome, telefone, email, data_inscricao
                FROM empreendedores 
                ORDER BY id DESC
            """))
            
            print("-" * 80)
            print(f"{'ID':<8} {'Nome':<25} {'Telefone':<15} {'Email':<25} {'Data':<20}")
            print("-" * 80)
            
            for row in result:
                id_val = row[0]
                nome = row[1][:24] if row[1] else "N/A"
                telefone = row[2][:14] if row[2] else "N/A"
                email = row[3][:24] if row[3] else "N/A"
                data = row[4].strftime("%d/%m/%Y %H:%M") if row[4] else "N/A"
                
                print(f"{id_val:<8} {nome:<25} {telefone:<15} {email:<25} {data:<20}")
            
            print("-" * 80)
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {e}")
        return False

def buscar_por_id_especifico(id_busca):
    """Buscar empreendedor específico por ID"""
    print(f"\n🔍 Buscando empreendedor ID {id_busca}...")
    
    try:
        engine = create_engine(settings.sql_connection_string)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, nome, telefone, email, data_inscricao, comunidade_originadora
                FROM empreendedores 
                WHERE id = :id
            """), {"id": id_busca})
            
            row = result.fetchone()
            
            if row:
                print("✅ EMPREENDEDOR ENCONTRADO!")
                print(f"   ID: {row[0]}")
                print(f"   Nome: {row[1]}")
                print(f"   Telefone: {row[2]}")
                print(f"   Email: {row[3]}")
                print(f"   Data Inscrição: {row[4]}")
                print(f"   Comunidade: {row[5]}")
                return True
            else:
                print(f"❌ Empreendedor ID {id_busca} não encontrado!")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao buscar ID {id_busca}: {e}")
        return False

def main():
    print("=" * 80)
    print("🔍 DIAGNÓSTICO DO BANCO AZURE SQL")
    print("=" * 80)
    
    # 1. Testar conexão
    if not testar_conexao():
        print("\n❌ Falha na conexão. Verifique as configurações.")
        return
    
    # 2. Verificar tabela e dados
    if not verificar_tabela_empreendedores():
        print("\n❌ Problema com a tabela ou dados.")
        return
    
    # 3. Buscar ID específico (1754)
    buscar_por_id_especifico(1754)
    
    # 4. Buscar por telefone específico
    print(f"\n🔍 Buscando por telefone (45) 3353535353...")
    try:
        engine = create_engine(settings.sql_connection_string)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, nome, telefone, email, data_inscricao
                FROM empreendedores 
                WHERE telefone LIKE '%3353535353%'
            """))
            
            rows = result.fetchall()
            
            if rows:
                print(f"✅ Encontrados {len(rows)} registro(s) com esse telefone:")
                for row in rows:
                    print(f"   ID: {row[0]}, Nome: {row[1]}, Telefone: {row[2]}")
            else:
                print("❌ Nenhum registro encontrado com esse telefone!")
                
    except Exception as e:
        print(f"❌ Erro ao buscar telefone: {e}")
    
    print("\n" + "=" * 80)
    print("🏁 DIAGNÓSTICO CONCLUÍDO")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
