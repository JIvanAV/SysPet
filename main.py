#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SysPet - Sistema de Gestão de PetShop
Projeto: Programação Estruturada em Python - FASE 1
Disciplina: Programação Estruturada
Instituição: FACISA
Grupo: [NOMES DOS INTEGRANTES]
Data: Junho 2026

Arquivo principal - Menu do sistema e orquestração dos módulos.
"""

from clientes import (
    cadastrar_cliente,
    listar_clientes,
    buscar_cliente,
    atualizar_cliente,
    excluir_cliente,
    menu_clientes,
)
from pets import (
    cadastrar_pet,
    listar_pets,
    buscar_pet,
    atualizar_pet,
    excluir_pet,
    menu_pets,
)
from veterinarios import (
    cadastrar_veterinario,
    listar_veterinarios,
    buscar_veterinario,
    atualizar_veterinario,
    excluir_veterinario,
    menu_veterinarios,
)
from agendamentos import (
    cadastrar_agendamento,
    listar_agendamentos,
    buscar_agendamento,
    atualizar_agendamento,
    excluir_agendamento,
    menu_agendamentos,
)


def exibir_cabecalho() -> None:
    """Exibe o cabeçalho padrão do sistema."""
    print("\n" + "=" * 60)
    print("           SysPet - Gestão de PetShop Amigo Fiel")
    print("=" * 60)


def exibir_menu_principal() -> None:
    """Exibe o menu principal do sistema."""
    print("\n📋 MENU PRINCIPAL")
    print("-" * 30)
    print("1. 👥 Clientes (Tutores)")
    print("2. 🐾 Pets (Pacientes)")
    print("3. 👨‍⚕️ Veterinários")
    print("4. 📅 Agendamentos")
    print("0. 🚪 Sair do Sistema")
    print("-" * 30)


def obter_opcao(mensagem: str = "Escolha uma opção: ") -> str:
    """Obtém a opção do usuário com tratamento de entrada vazia."""
    while True:
        try:
            opcao = input(mensagem).strip()
            if opcao:
                return opcao
            print("⚠️  Entrada vazia. Digite uma opção válida.")
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Saindo do sistema...")
            return "0"


def main() -> None:
    """Função principal - Loop do menu do sistema."""
    print("\n🐶 Bem-vindo ao SysPet!")
    print("   Sistema de gestão para a rede PetShop Amigo Fiel")

    while True:
        exibir_cabecalho()
        exibir_menu_principal()
        opcao = obter_opcao()

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_pets()
        elif opcao == "3":
            menu_veterinarios()
        elif opcao == "4":
            menu_agendamentos()
        elif opcao == "0":
            print("\n👋 Obrigado por usar o SysPet! Até logo!")
            break
        else:
            print(f"\n❌ Opção '{opcao}' inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("O sistema será encerrado.")