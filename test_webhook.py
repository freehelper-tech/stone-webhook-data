"""
Script de teste para a API de Webhook
Teste rápido dos endpoints principais
"""
import requests
import json
from datetime import datetime

# Configuração
BASE_URL = "http://localhost:8000/api/v1/webhook"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def test_health_check():
    """Testar health check"""
    print_info("Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check OK - Status: {data['status']}")
            print(f"  Total empreendedores: {data.get('total_empreendedores', 0)}")
            return True
        else:
            print_error(f"Health check falhou - Status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro ao conectar: {e}")
        return False


def test_criar_empreendedor():
    """Testar criação de empreendedor"""
    print_info("Testando criação de empreendedor...")
    
    payload = {
        "Nome": {
            "first": "João",
            "last": "Silva Teste"
        },
        "Telefone": {
            "area": "11",
            "phone": f"9{datetime.now().strftime('%H%M%S')}"
        },
        "E-mail": f"joao.teste.{datetime.now().strftime('%H%M%S')}@gmail.com",
        "CPF": "12345678900",
        "Cidade": "São Paulo",
        "Estado": "SP",
        "Idade": "25 a 34 anos",
        "Gênero": "Masculino",
        "Raça/cor": "Branca",
        "Escolaridade": "Ensino Superior completo",
        "Faixa de renda familiar mensal": "Entre 2 e 3 salários mínimos",
        "Quais são as suas fontes de renda atualmente?": [
            "Meu próprio negócio formalizado (MEI, ME, etc.)"
        ],
        "Tempo de funcionamento do negócio": "1 a 3 anos",
        "Segmento de atuação": "Tecnologia",
        "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Banco Pérola"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/jotform",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success(f"Empreendedor criado - ID: {data['empreendedor_id']}")
            print(f"  Nome: {data['data']['nome']}")
            print(f"  Telefone: {data['data']['telefone']}")
            print(f"  Email: {data['data']['email']}")
            return data['empreendedor_id']
        else:
            print_error(f"Falha ao criar - Status: {response.status_code}")
            print(f"  Resposta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Erro ao criar empreendedor: {e}")
        return None


def test_buscar_empreendedor(empreendedor_id):
    """Testar busca de empreendedor por ID"""
    print_info(f"Testando busca por ID {empreendedor_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/empreendedores/{empreendedor_id}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Empreendedor encontrado")
            print(f"  ID: {data['id']}")
            print(f"  Nome: {data['nome']}")
            print(f"  Telefone: {data['telefone']}")
            return True
        else:
            print_error(f"Falha na busca - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro ao buscar: {e}")
        return False


def test_buscar_com_filtros():
    """Testar busca com filtros"""
    print_info("Testando busca com filtros...")
    
    payload = {
        "estado": "SP",
        "page": 1,
        "page_size": 5
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/empreendedores/search",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Busca realizada - {data['total']} resultados")
            print(f"  Página: {data['page']}/{data['total_pages']}")
            print(f"  Registros retornados: {len(data['data'])}")
            return True
        else:
            print_error(f"Falha na busca - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro ao buscar: {e}")
        return False


def test_estatisticas():
    """Testar obtenção de estatísticas"""
    print_info("Testando estatísticas...")
    
    try:
        response = requests.get(f"{BASE_URL}/empreendedores/stats")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Estatísticas obtidas")
            print(f"  Total de empreendedores: {data['total_empreendedores']}")
            print(f"  Ativos na Ludos: {data['total_ativos_ludos']}")
            print(f"  Em mentoria: {data['total_em_mentoria']}")
            
            if data.get('media_nps_geral'):
                print(f"  NPS Geral médio: {data['media_nps_geral']:.2f}")
            
            return True
        else:
            print_error(f"Falha ao obter stats - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro ao obter estatísticas: {e}")
        return False


def test_atualizar_empreendedor(empreendedor_id):
    """Testar atualização de empreendedor"""
    print_info(f"Testando atualização do ID {empreendedor_id}...")
    
    payload = {
        "ativo_na_ludos": True,
        "nps_geral": 9
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/empreendedores/{empreendedor_id}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Empreendedor atualizado")
            print(f"  Mensagem: {data['message']}")
            return True
        else:
            print_error(f"Falha ao atualizar - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro ao atualizar: {e}")
        return False


def main():
    """Executar todos os testes"""
    print("\n" + "="*60)
    print("🧪 TESTES DA API DE WEBHOOK - JOTFORM")
    print("="*60 + "\n")
    
    resultados = {
        "total": 0,
        "sucesso": 0,
        "falha": 0
    }
    
    # 1. Health Check
    resultados["total"] += 1
    if test_health_check():
        resultados["sucesso"] += 1
    else:
        resultados["falha"] += 1
        print_warning("API não está respondendo. Verifique se está rodando.")
        return
    
    print("\n" + "-"*60 + "\n")
    
    # 2. Criar Empreendedor
    resultados["total"] += 1
    empreendedor_id = test_criar_empreendedor()
    if empreendedor_id:
        resultados["sucesso"] += 1
    else:
        resultados["falha"] += 1
    
    print("\n" + "-"*60 + "\n")
    
    # Se criou com sucesso, testar outros endpoints
    if empreendedor_id:
        # 3. Buscar por ID
        resultados["total"] += 1
        if test_buscar_empreendedor(empreendedor_id):
            resultados["sucesso"] += 1
        else:
            resultados["falha"] += 1
        
        print("\n" + "-"*60 + "\n")
        
        # 4. Atualizar
        resultados["total"] += 1
        if test_atualizar_empreendedor(empreendedor_id):
            resultados["sucesso"] += 1
        else:
            resultados["falha"] += 1
        
        print("\n" + "-"*60 + "\n")
    
    # 5. Buscar com filtros
    resultados["total"] += 1
    if test_buscar_com_filtros():
        resultados["sucesso"] += 1
    else:
        resultados["falha"] += 1
    
    print("\n" + "-"*60 + "\n")
    
    # 6. Estatísticas
    resultados["total"] += 1
    if test_estatisticas():
        resultados["sucesso"] += 1
    else:
        resultados["falha"] += 1
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    print(f"Total de testes: {resultados['total']}")
    print_success(f"Sucessos: {resultados['sucesso']}")
    if resultados['falha'] > 0:
        print_error(f"Falhas: {resultados['falha']}")
    else:
        print_success("Falhas: 0")
    
    taxa_sucesso = (resultados['sucesso'] / resultados['total']) * 100
    print(f"\nTaxa de sucesso: {taxa_sucesso:.1f}%")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

