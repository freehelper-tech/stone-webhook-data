"""
Script para verificar se um empreendedor está no banco de dados
Busca por ID, telefone, email, nome ou CPF
"""
import sys
import os
from datetime import datetime

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.data.empreendedor_repository import EmpreendedorRepository
import logging

logging.basicConfig(
    level=logging.WARNING,  # Menos verbose
    format='%(message)s'
)

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(label, value):
    print(f"{Colors.CYAN}{label:30}{Colors.END}: {Colors.BOLD}{value}{Colors.END}")

def print_empreendedor(emp):
    """Exibir dados do empreendedor"""
    print(f"\n{Colors.GREEN}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}EMPREENDEDOR ENCONTRADO{Colors.END}")
    print(f"{Colors.GREEN}{'─'*80}{Colors.END}\n")
    
    # Dados Principais
    print(f"{Colors.BOLD}{Colors.YELLOW}📋 DADOS PRINCIPAIS{Colors.END}")
    print_info("ID", emp.id)
    print_info("Nome", emp.nome)
    print_info("Telefone", emp.telefone)
    print_info("Email", emp.email or "Não informado")
    print_info("CPF", emp.cpf or "Não informado")
    
    # Localização
    print(f"\n{Colors.BOLD}{Colors.YELLOW}📍 LOCALIZAÇÃO{Colors.END}")
    print_info("Cidade", emp.cidade or "Não informado")
    print_info("Estado", emp.estado or "Não informado")
    
    # Dados Demográficos
    print(f"\n{Colors.BOLD}{Colors.YELLOW}👤 DADOS DEMOGRÁFICOS{Colors.END}")
    print_info("Idade", emp.idade or "Não informado")
    print_info("Gênero", emp.genero or "Não informado")
    print_info("Raça/Cor", emp.raca_cor or "Não informado")
    print_info("Escolaridade", emp.escolaridade or "Não informado")
    
    # Dados Socioeconômicos
    print(f"\n{Colors.BOLD}{Colors.YELLOW}💰 DADOS SOCIOECONÔMICOS{Colors.END}")
    print_info("Faixa de Renda", emp.faixa_renda or "Não informado")
    print_info("Fonte de Renda", emp.fonte_renda or "Não informado")
    
    # Negócio
    print(f"\n{Colors.BOLD}{Colors.YELLOW}🏢 NEGÓCIO{Colors.END}")
    print_info("Tempo de Funcionamento", emp.tempo_funcionamento or "Não informado")
    print_info("Segmento de Atuação", emp.segmento_atuacao or "Não informado")
    if emp.segmento_outros:
        print_info("Segmento (Outros)", emp.segmento_outros)
    print_info("Organização Stone", emp.organizacao_stone or "Não informado")
    
    # Status
    print(f"\n{Colors.BOLD}{Colors.YELLOW}📊 STATUS{Colors.END}")
    print_info("Na Comunidade", "✅ Sim" if emp.esta_na_comunidade else "❌ Não")
    print_info("Ativo na Ludos", "✅ Sim" if emp.ativo_na_ludos else "❌ Não")
    print_info("Fazendo Mentoria", "✅ Sim" if emp.fazendo_mentoria else "❌ Não")
    print_info("Solicitou Crédito", "✅ Sim" if emp.solicitou_credito else "❌ Não")
    
    # NPS
    if emp.nps_geral or emp.nps_mentoria or emp.nps_ludos:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⭐ NPS{Colors.END}")
        if emp.nps_geral:
            print_info("NPS Geral", f"{emp.nps_geral}/10")
        if emp.nps_mentoria:
            print_info("NPS Mentoria", f"{emp.nps_mentoria}/10")
        if emp.nps_ludos:
            print_info("NPS Ludos", f"{emp.nps_ludos}/10")
    
    # Metadados
    print(f"\n{Colors.BOLD}{Colors.YELLOW}📅 METADADOS{Colors.END}")
    print_info("Comunidade Originadora", emp.comunidade_originadora or "Não informado")
    print_info("Tipo de Formulário", emp.formulario_tipo or "Não informado")
    if emp.data_inscricao:
        print_info("Data de Inscrição", emp.data_inscricao.strftime("%d/%m/%Y %H:%M:%S"))
    
    print(f"\n{Colors.GREEN}{'─'*80}{Colors.END}\n")


def buscar_por_id(repo):
    """Buscar empreendedor por ID"""
    print_header("🔍 BUSCAR POR ID")
    
    try:
        emp_id = int(input("Digite o ID do empreendedor: "))
        
        print(f"\n{Colors.CYAN}Buscando empreendedor ID={emp_id}...{Colors.END}")
        emp = repo.get_empreendedor_by_id(emp_id)
        
        if emp:
            print_empreendedor(emp)
            return True
        else:
            print_error(f"Empreendedor com ID {emp_id} não encontrado")
            return False
            
    except ValueError:
        print_error("ID inválido. Digite apenas números.")
        return False
    except Exception as e:
        print_error(f"Erro ao buscar: {e}")
        return False


def buscar_por_telefone(repo):
    """Buscar empreendedor por telefone"""
    print_header("🔍 BUSCAR POR TELEFONE")
    
    telefone = input("Digite o telefone (ex: (11) 987654321): ").strip()
    
    if not telefone:
        print_error("Telefone não pode estar vazio")
        return False
    
    print(f"\n{Colors.CYAN}Buscando por telefone '{telefone}'...{Colors.END}")
    emp = repo.get_empreendedor_by_telefone(telefone)
    
    if emp:
        print_empreendedor(emp)
        return True
    else:
        print_error(f"Empreendedor com telefone '{telefone}' não encontrado")
        return False


def buscar_por_email(repo):
    """Buscar empreendedor por email"""
    print_header("🔍 BUSCAR POR EMAIL")
    
    email = input("Digite o email: ").strip()
    
    if not email:
        print_error("Email não pode estar vazio")
        return False
    
    print(f"\n{Colors.CYAN}Buscando por email '{email}'...{Colors.END}")
    emp = repo.get_empreendedor_by_email(email)
    
    if emp:
        print_empreendedor(emp)
        return True
    else:
        print_error(f"Empreendedor com email '{email}' não encontrado")
        return False


def buscar_por_cpf(repo):
    """Buscar empreendedor por CPF"""
    print_header("🔍 BUSCAR POR CPF")
    
    cpf = input("Digite o CPF: ").strip()
    
    if not cpf:
        print_error("CPF não pode estar vazio")
        return False
    
    print(f"\n{Colors.CYAN}Buscando por CPF '{cpf}'...{Colors.END}")
    emp = repo.get_empreendedor_by_cpf(cpf)
    
    if emp:
        print_empreendedor(emp)
        return True
    else:
        print_error(f"Empreendedor com CPF '{cpf}' não encontrado")
        return False


def buscar_por_nome(repo):
    """Buscar empreendedores por nome (parcial)"""
    print_header("🔍 BUSCAR POR NOME")
    
    nome = input("Digite o nome (ou parte do nome): ").strip()
    
    if not nome:
        print_error("Nome não pode estar vazio")
        return False
    
    print(f"\n{Colors.CYAN}Buscando por nome contendo '{nome}'...{Colors.END}")
    
    from app.dto.webhook_dtos import EmpreendedorSearchRequest
    filtros = EmpreendedorSearchRequest(
        nome=nome,
        page=1,
        page_size=10
    )
    
    empreendedores, total = repo.search_empreendedores(filtros)
    
    if empreendedores:
        print_success(f"Encontrados {total} empreendedor(es)")
        
        for i, emp in enumerate(empreendedores, 1):
            if i > 1:
                print(f"\n{Colors.YELLOW}{'─'*80}{Colors.END}\n")
            print(f"{Colors.BOLD}#{i} de {min(len(empreendedores), total)}{Colors.END}")
            print_empreendedor(emp)
        
        if total > len(empreendedores):
            print(f"{Colors.YELLOW}⚠ Mostrando {len(empreendedores)} de {total} resultados{Colors.END}\n")
        
        return True
    else:
        print_error(f"Nenhum empreendedor encontrado com nome contendo '{nome}'")
        return False


def listar_ultimos(repo):
    """Listar últimos empreendedores cadastrados"""
    print_header("📋 ÚLTIMOS EMPREENDEDORES CADASTRADOS")
    
    try:
        limite = int(input("Quantos deseja ver? (padrão 5): ") or "5")
    except ValueError:
        limite = 5
    
    print(f"\n{Colors.CYAN}Buscando últimos {limite} empreendedores...{Colors.END}")
    
    from app.dto.webhook_dtos import EmpreendedorSearchRequest
    filtros = EmpreendedorSearchRequest(
        page=1,
        page_size=limite
    )
    
    empreendedores, total = repo.search_empreendedores(filtros)
    
    if empreendedores:
        print_success(f"Total no banco: {total} empreendedor(es)")
        print(f"\n{Colors.CYAN}Mostrando os {len(empreendedores)} mais recentes:{Colors.END}\n")
        
        for i, emp in enumerate(empreendedores, 1):
            if i > 1:
                print(f"\n{Colors.YELLOW}{'─'*80}{Colors.END}\n")
            print(f"{Colors.BOLD}#{i} de {len(empreendedores)}{Colors.END}")
            print_empreendedor(emp)
        
        return True
    else:
        print_error("Nenhum empreendedor encontrado no banco")
        return False


def main():
    """Menu principal"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'🔍 VERIFICAR EMPREENDEDOR NO BANCO DE DADOS':^80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")
    
    # Conectar ao banco
    print(f"{Colors.CYAN}Conectando ao banco de dados...{Colors.END}")
    try:
        repo = EmpreendedorRepository()
        print_success("Conectado com sucesso!\n")
    except Exception as e:
        print_error(f"Erro ao conectar ao banco: {e}")
        return
    
    while True:
        print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.END}")
        print(f"{Colors.BOLD}Escolha uma opção:{Colors.END}\n")
        print(f"  {Colors.BOLD}1{Colors.END} - Buscar por ID")
        print(f"  {Colors.BOLD}2{Colors.END} - Buscar por Telefone")
        print(f"  {Colors.BOLD}3{Colors.END} - Buscar por Email")
        print(f"  {Colors.BOLD}4{Colors.END} - Buscar por CPF")
        print(f"  {Colors.BOLD}5{Colors.END} - Buscar por Nome")
        print(f"  {Colors.BOLD}6{Colors.END} - Listar Últimos Cadastrados")
        print(f"  {Colors.BOLD}0{Colors.END} - Sair")
        print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.END}")
        
        opcao = input(f"\n{Colors.BOLD}Digite a opção: {Colors.END}").strip()
        
        if opcao == "1":
            buscar_por_id(repo)
        elif opcao == "2":
            buscar_por_telefone(repo)
        elif opcao == "3":
            buscar_por_email(repo)
        elif opcao == "4":
            buscar_por_cpf(repo)
        elif opcao == "5":
            buscar_por_nome(repo)
        elif opcao == "6":
            listar_ultimos(repo)
        elif opcao == "0":
            print(f"\n{Colors.GREEN}👋 Até logo!{Colors.END}\n")
            break
        else:
            print_error("Opção inválida!")
        
        input(f"\n{Colors.CYAN}Pressione ENTER para continuar...{Colors.END}")
        print("\n" * 2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠ Interrompido pelo usuário{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Erro fatal: {e}{Colors.END}\n")

