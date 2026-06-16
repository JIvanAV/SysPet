#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Clientes (Tutores) - SysPet
Funcionalidades: Cadastro, Alteração, Exclusão, Listagem, Busca.
"""

from typing import Optional
from utils import (
    limpar_tela,
    pausar,
    confirmar,
    validar_email,
    validar_telefone,
    obter_int,
    obter_str_obrigatorio,
)


# Lista global em memória para armazenar clientes
clientes: list[dict] = []

# Contador para IDs auto-incrementais
_proximo_id_cliente: int = 1


def _gerar_id() -> int:
    """Gera um ID único sequencial para novo cliente."""
    global _proximo_id_cliente
    id_atual = _proximo_id_cliente
    _proximo_id_cliente += 1
    return id_atual


def _cliente_para_dict(
    id_cliente: int,
    nome: str,
    telefone: str,
    email: str,
    endereco: str,
) -> dict:
    """Cria dicionário padronizado de cliente."""
    return {
        "id": id_cliente,
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "endereco": endereco,
    }


def cadastrar_cliente() -> None:
    """Cadastra um novo cliente (tutor) no sistema."""
    limpar_tela()
    print("📝 CADASTRAR NOVO CLIENTE")
    print("-" * 40)

    try:
        nome = obter_str_obrigatorio("Nome completo: ")
        telefone = obter_str_obrigatorio("Telefone (com DDD): ")
        while not validar_telefone(telefone):
            print("⚠️  Telefone inválido. Use formato: (XX) XXXXX-XXXX")
            telefone = obter_str_obrigatorio("Telefone (com DDD): ")

        email = obter_str_obrigatorio("E-mail: ")
        while not validar_email(email):
            print("⚠️  E-mail inválido. Exemplo: tutor@email.com")
            email = obter_str_obrigatorio("E-mail: ")

        endereco = obter_str_obrigatorio("Endereço completo: ")

        id_cliente = _gerar_id()
        cliente = _cliente_para_dict(id_cliente, nome, telefone, email, endereco)
        clientes.append(cliente)

        print(f"\n✅ Cliente cadastrado com sucesso! (ID: {id_cliente})")
        print(f"   Nome: {nome}")
        print(f"   Telefone: {telefone}")
        print(f"   E-mail: {email}")

    except ValueError as e:
        print(f"\n❌ Erro de validação: {e}")
    except Exception as e:
        print(f"\n❌ Erro inesperado ao cadastrar: {e}")

    pausar()


def listar_clientes() -> None:
    """Lista todos os clientes cadastrados."""
    limpar_tela()
    print("📋 LISTA DE CLIENTES")
    print("-" * 60)

    if not clientes:
        print("📭 Nenhum cliente cadastrado.")
        pausar()
        return

    print(f"{'ID':<4} {'Nome':<30} {'Telefone':<16} {'E-mail':<25}")
    print("-" * 80)

    for cliente in clientes:
        nome = cliente["nome"][:28] + ".." if len(cliente["nome"]) > 30 else cliente["nome"]
        email = cliente["email"][:23] + ".." if len(cliente["email"]) > 25 else cliente["email"]
        print(f"{cliente['id']:<4} {nome:<30} {cliente['telefone']:<16} {email:<25}")

    print(f"\n📊 Total: {len(clientes)} cliente(s)")
    pausar()


def buscar_cliente(id_busca: Optional[int] = None) -> Optional[dict]:
    """Busca um cliente pelo ID. Retorna o dicionário do cliente ou None."""
    if id_busca is None:
        limpar_tela()
        print("🔍 BUSCAR CLIENTE")
        print("-" * 30)
        try:
            id_busca = obter_int("Digite o ID do cliente: ")
        except ValueError:
            print("❌ ID inválido.")
            pausar()
            return None

    for cliente in clientes:
        if cliente["id"] == id_busca:
            limpar_tela()
            print("🔎 CLIENTE ENCONTRADO")
            print("-" * 40)
            print(f"ID:         {cliente['id']}")
            print(f"Nome:       {cliente['nome']}")
            print(f"Telefone:   {cliente['telefone']}")
            print(f"E-mail:     {cliente['email']}")
            print(f"Endereço:   {cliente['endereco']}")
            pausar()
            return cliente

    print(f"\n❌ Cliente com ID {id_busca} não encontrado.")
    pausar()
    return None


def atualizar_cliente() -> None:
    """Atualiza os dados de um cliente existente."""
    limpar_tela()
    print("✏️  ATUALIZAR CLIENTE")
    print("-" * 30)

    try:
        id_cliente = obter_int("Digite o ID do cliente a atualizar: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    cliente = None
    for c in clientes:
        if c["id"] == id_cliente:
            cliente = c
            break

    if not cliente:
        print(f"\n❌ Cliente com ID {id_cliente} não encontrado.")
        pausar()
        return

    print(f"\nCliente atual: {cliente['nome']}")
    print("Deixe em branco para manter o valor atual.\n")

    try:
        novo_nome = input(f"Novo nome [{cliente['nome']}]: ").strip()
        if novo_nome:
            cliente["nome"] = novo_nome

        novo_telefone = input(f"Novo telefone [{cliente['telefone']}]: ").strip()
        if novo_telefone:
            while not validar_telefone(novo_telefone):
                print("⚠️  Telefone inválido. Use formato: (XX) XXXXX-XXXX")
                novo_telefone = input(f"Novo telefone [{cliente['telefone']}]: ").strip()
                if not novo_telefone:
                    break
            if novo_telefone:
                cliente["telefone"] = novo_telefone

        novo_email = input(f"Novo e-mail [{cliente['email']}]: ").strip()
        if novo_email:
            while not validar_email(novo_email):
                print("⚠️  E-mail inválido.")
                novo_email = input(f"Novo e-mail [{cliente['email']}]: ").strip()
                if not novo_email:
                    break
            if novo_email:
                cliente["email"] = novo_email

        novo_endereco = input(f"Novo endereço [{cliente['endereco']}]: ").strip()
        if novo_endereco:
            cliente["endereco"] = novo_endereco

        print("\n✅ Cliente atualizado com sucesso!")

    except Exception as e:
        print(f"\n❌ Erro ao atualizar: {e}")

    pausar()


def excluir_cliente() -> None:
    """Exclui um cliente do sistema."""
    limpar_tela()
    print("🗑️  EXCLUIR CLIENTE")
    print("-" * 30)

    try:
        id_cliente = obter_int("Digite o ID do cliente a excluir: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_cliente:
            print(f"\nCliente encontrado: {cliente['nome']} (ID: {cliente['id']})")
            if confirmar("Tem certeza que deseja excluir? (s/n): "):
                clientes.pop(i)
                print("\n✅ Cliente excluído com sucesso!")
            else:
                print("\n❌ Exclusão cancelada.")
            pausar()
            return

    print(f"\n❌ Cliente com ID {id_cliente} não encontrado.")
    pausar()


def menu_clientes() -> None:
    """Menu específico do módulo de clientes."""
    while True:
        limpar_tela()
        print("👥 MÓDULO: CLIENTES (TUTORES)")
        print("-" * 40)
        print("1. ➕ Cadastrar Cliente")
        print("2. 📋 Listar Clientes")
        print("3. 🔍 Buscar Cliente por ID")
        print("4. ✏️  Atualizar Cliente")
        print("5. 🗑️  Excluir Cliente")
        print("0. ↩️  Voltar ao Menu Principal")
        print("-" * 40)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            buscar_cliente()
        elif opcao == "4":
            atualizar_cliente()
        elif opcao == "5":
            excluir_cliente()
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")
            pausar()


# Dados de exemplo para teste rápido
def _carregar_dados_exemplo() -> None:
    """Carrega dados de exemplo para demonstração."""
    global _proximo_id_cliente
    exemplos = [
        ("João Silva Santos", "(83) 99999-1111", "joao@email.com", "Rua das Flores, 123 - Centro"),
        ("Maria Oliveira Costa", "(83) 98888-2222", "maria@email.com", "Av. Principal, 456 - Bairro Novo"),
        ("Carlos Eduardo Lima", "(83) 97777-3333", "carlos@email.com", "Rua do Comércio, 789 - Centro"),
    ]
    for nome, tel, email, end in exemplos:
        clientes.append(_cliente_para_dict(_gerar_id(), nome, tel, email, end))


# Carrega dados de exemplo ao importar o módulo
_carregar_dados_exemplo()