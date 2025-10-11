"""
Exemplos de uso da API de Webhook
Demonstra como interagir com os endpoints
"""
import requests
import json
from datetime import datetime
from typing import Dict, Any

# Base URL da API
BASE_URL = "http://localhost:8000/api/v1/webhook"


class WebhookClient:
    """Cliente para interagir com a API de Webhook"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def enviar_webhook_jotform(self, dados_empreendedor: Dict[str, Any]) -> Dict:
        """
        Enviar dados de empreendedor via webhook
        
        Args:
            dados_empreendedor: Dados do formulário Jotform
            
        Returns:
            Dict com resposta da API
        """
        url = f"{self.base_url}/jotform"
        response = requests.post(url, json=dados_empreendedor)
        return response.json()
    
    def buscar_por_id(self, empreendedor_id: int) -> Dict:
        """Buscar empreendedor por ID"""
        url = f"{self.base_url}/empreendedores/{empreendedor_id}"
        response = requests.get(url)
        return response.json()
    
    def buscar_com_filtros(self, filtros: Dict[str, Any]) -> Dict:
        """Buscar empreendedores com filtros"""
        url = f"{self.base_url}/empreendedores/search"
        response = requests.post(url, json=filtros)
        return response.json()
    
    def atualizar_empreendedor(self, empreendedor_id: int, updates: Dict[str, Any]) -> Dict:
        """Atualizar dados de empreendedor"""
        url = f"{self.base_url}/empreendedores/{empreendedor_id}"
        response = requests.put(url, json=updates)
        return response.json()
    
    def obter_estatisticas(self) -> Dict:
        """Obter estatísticas gerais"""
        url = f"{self.base_url}/empreendedores/stats"
        response = requests.get(url)
        return response.json()
    
    def health_check(self) -> Dict:
        """Verificar saúde da API"""
        url = f"{self.base_url}/health"
        response = requests.get(url)
        return response.json()


# ===== EXEMPLO 1: Enviar dados do Jotform =====
def exemplo_1_enviar_webhook():
    """Exemplo de envio de webhook do Jotform"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Enviar Webhook do Jotform")
    print("="*60 + "\n")
    
    client = WebhookClient()
    
    # Dados do formulário (estrutura do Jotform)
    dados = {
        "Nome": {
            "first": "Maria",
            "last": "Silva Santos"
        },
        "E-mail": "maria.santos@gmail.com",
        "Telefone": {
            "area": "21",
            "phone": "987654321"
        },
        "CPF": "98765432100",
        "Cidade": "Rio de Janeiro",
        "Estado": "RJ",
        "Idade": "35 a 44 anos",
        "Gênero": "Feminino",
        "Raça/cor": "Parda",
        "Escolaridade": "Ensino Médio completo",
        "Faixa de renda familiar mensal": "Entre 1 e 2 salários mínimos",
        "Quais são as suas fontes de renda atualmente?": [
            "Trabalho com carteira assinada (CLT)",
            "Meu próprio negócio informal"
        ],
        "Tempo de funcionamento do negócio": "Menos de 6 meses",
        "Segmento de atuação": "Alimentação",
        "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Impulso Stone"
    }
    
    try:
        resposta = client.enviar_webhook_jotform(dados)
        
        if resposta.get("success"):
            print("✅ Empreendedor cadastrado com sucesso!")
            print(f"   ID: {resposta['empreendedor_id']}")
            print(f"   Nome: {resposta['data']['nome']}")
            print(f"   Telefone: {resposta['data']['telefone']}")
            print(f"   Email: {resposta['data']['email']}")
            return resposta['empreendedor_id']
        else:
            print("❌ Erro ao cadastrar:")
            print(f"   {resposta.get('message')}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


# ===== EXEMPLO 2: Buscar empreendedor =====
def exemplo_2_buscar_por_id(empreendedor_id: int):
    """Exemplo de busca por ID"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Buscar Empreendedor por ID")
    print("="*60 + "\n")
    
    client = WebhookClient()
    
    try:
        resposta = client.buscar_por_id(empreendedor_id)
        
        print(f"📋 Dados do empreendedor ID {empreendedor_id}:")
        print(f"   Nome: {resposta['nome']}")
        print(f"   Telefone: {resposta['telefone']}")
        print(f"   Email: {resposta['email']}")
        print(f"   Cidade: {resposta['cidade']}")
        print(f"   Estado: {resposta['estado']}")
        print(f"   Data inscrição: {resposta['data_inscricao']}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


# ===== EXEMPLO 3: Buscar com filtros =====
def exemplo_3_buscar_com_filtros():
    """Exemplo de busca com filtros"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Buscar com Filtros")
    print("="*60 + "\n")
    
    client = WebhookClient()
    
    # Buscar empreendedores do Rio de Janeiro
    filtros = {
        "estado": "RJ",
        "page": 1,
        "page_size": 10
    }
    
    try:
        resposta = client.buscar_com_filtros(filtros)
        
        if resposta.get("success"):
            print(f"📊 Resultados da busca:")
            print(f"   Total encontrado: {resposta['total']}")
            print(f"   Página: {resposta['page']}/{resposta['total_pages']}")
            print(f"   Registros retornados: {len(resposta['data'])}")
            
            if resposta['data']:
                print("\n   Empreendedores:")
                for emp in resposta['data'][:5]:  # Mostrar apenas 5
                    print(f"   - {emp['nome']} ({emp['cidade']}/{emp['estado']})")
        else:
            print("❌ Erro na busca")
            
    except Exception as e:
        print(f"❌ Erro: {e}")


# ===== EXEMPLO 4: Atualizar empreendedor =====
def exemplo_4_atualizar_empreendedor(empreendedor_id: int):
    """Exemplo de atualização"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Atualizar Empreendedor")
    print("="*60 + "\n")
    
    client = WebhookClient()
    
    # Dados para atualizar
    updates = {
        "ativo_na_ludos": True,
        "esta_na_comunidade": True,
        "nps_geral": 10
    }
    
    try:
        resposta = client.atualizar_empreendedor(empreendedor_id, updates)
        
        if resposta.get("success"):
            print("✅ Empreendedor atualizado com sucesso!")
            print(f"   {resposta['message']}")
        else:
            print(f"❌ Erro: {resposta.get('message')}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")


# ===== EXEMPLO 5: Estatísticas =====
def exemplo_5_estatisticas():
    """Exemplo de obtenção de estatísticas"""
    print("\n" + "="*60)
    print("EXEMPLO 5: Estatísticas Gerais")
    print("="*60 + "\n")
    
    client = WebhookClient()
    
    try:
        stats = client.obter_estatisticas()
        
        print("📊 Estatísticas:")
        print(f"   Total de empreendedores: {stats['total_empreendedores']}")
        print(f"   Ativos na Ludos: {stats['total_ativos_ludos']}")
        print(f"   Em mentoria: {stats['total_em_mentoria']}")
        
        if stats.get('media_nps_geral'):
            print(f"   NPS Geral médio: {stats['media_nps_geral']:.2f}")
        
        # Top 5 estados
        if stats['total_por_estado']:
            print("\n   Top 5 Estados:")
            top_estados = sorted(
                stats['total_por_estado'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
            for estado, total in top_estados:
                print(f"   - {estado}: {total} empreendedores")
        
        # Top 5 segmentos
        if stats['total_por_segmento']:
            print("\n   Top 5 Segmentos:")
            top_segmentos = sorted(
                stats['total_por_segmento'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
            for segmento, total in top_segmentos:
                print(f"   - {segmento}: {total} empreendedores")
                
    except Exception as e:
        print(f"❌ Erro: {e}")


# ===== EXEMPLO 6: Health Check =====
def exemplo_6_health_check():
    """Exemplo de health check"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Health Check")
    print("="*60 + "\n")
    
    client = WebhookClient()
    
    try:
        health = client.health_check()
        
        status_icon = "✅" if health['status'] == 'healthy' else "❌"
        print(f"{status_icon} Status: {health['status']}")
        print(f"   Serviço: {health['service']}")
        print(f"   Database: {health['database']}")
        print(f"   Total de empreendedores: {health['total_empreendedores']}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


# ===== EXEMPLO 7: Busca avançada =====
def exemplo_7_busca_avancada():
    """Exemplo de busca com múltiplos filtros"""
    print("\n" + "="*60)
    print("EXEMPLO 7: Busca Avançada")
    print("="*60 + "\n")
    
    client = WebhookClient()
    
    # Buscar empreendedoras de SP que estão ativas na Ludos
    filtros = {
        "estado": "SP",
        "ativo_na_ludos": True,
        "page": 1,
        "page_size": 20
    }
    
    try:
        resposta = client.buscar_com_filtros(filtros)
        
        if resposta.get("success"):
            print(f"📊 Busca: Empreendedores de SP ativos na Ludos")
            print(f"   Total encontrado: {resposta['total']}")
            
            if resposta['data']:
                print(f"\n   Primeiros {len(resposta['data'][:3])} resultados:")
                for emp in resposta['data'][:3]:
                    print(f"   - {emp['nome']}")
                    print(f"     Cidade: {emp['cidade']}")
                    print(f"     Email: {emp['email']}")
                    print()
                    
    except Exception as e:
        print(f"❌ Erro: {e}")


# ===== EXECUTAR TODOS OS EXEMPLOS =====
def main():
    """Executar todos os exemplos"""
    print("\n" + "🚀 " + "="*58 + " 🚀")
    print("   EXEMPLOS DE USO - API DE WEBHOOK JOTFORM")
    print("🚀 " + "="*58 + " 🚀")
    
    # Verificar se API está rodando
    try:
        client = WebhookClient()
        client.health_check()
    except Exception as e:
        print("\n❌ ERRO: API não está respondendo!")
        print("   Certifique-se de que o servidor está rodando:")
        print("   python -m uvicorn app.main:app --reload --port 8000")
        return
    
    # Exemplo 6: Health Check primeiro
    exemplo_6_health_check()
    
    # Exemplo 1: Criar empreendedor
    empreendedor_id = exemplo_1_enviar_webhook()
    
    if empreendedor_id:
        # Exemplo 2: Buscar por ID
        exemplo_2_buscar_por_id(empreendedor_id)
        
        # Exemplo 4: Atualizar
        exemplo_4_atualizar_empreendedor(empreendedor_id)
    
    # Exemplo 3: Buscar com filtros
    exemplo_3_buscar_com_filtros()
    
    # Exemplo 5: Estatísticas
    exemplo_5_estatisticas()
    
    # Exemplo 7: Busca avançada
    exemplo_7_busca_avancada()
    
    print("\n" + "="*60)
    print("✅ Todos os exemplos executados!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

