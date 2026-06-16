#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Pets (Pacientes) - SysPet
Funcionalidades: Cadastro, Alteração, Exclusão, Listagem, Busca.
Vincula pets aos clientes (tutores).
"""

from typing import Optional
from utils import (
    limpar_tela,
    pausar,
    confirmar,
    obter_int,
    obter_str_obrigatorio,
    obter_str_opcional,
)
from clientes import clientes, buscar_cliente


# Lista global em memória para armazenar pets
pets: list[dict] = []

# Contador para IDs auto-incrementais
_proximo_id_pet: int = 1

# Tipos de pet permitidos
TIPOS_PET = ("Cachorro", "Gato", "Pássaro", "Roedor", "Réptil", "Outro")

# Portes permitidos
PORTES = ("Pequeno", "Médio", "Grande")


def _gerar_id() -> int:
    """Gera um ID único sequencial para novo pet."""
    global _proximo_id_pet
    id_atual = _proximo_id_pet
    _proximo_id_pet += 1
    return id_atual


def _pet_para_dict(
    id_pet: int,
    id_cliente: int,
    nome: str,
    tipo: str,
    raca: str,
    idade: int,
    peso: float,
    porte: str,
    observacoes: str,
) -> dict:
    """Cria dicionário padronizado de pet."""
    return {
        "id": id_pet,
        "id_cliente": id_cliente,
        "nome": nome,
        "tipo": tipo,
        "raca": raca,
        "idade": idade,
        "peso": peso,
        "porte": porte,
        "observacoes": observacoes,
    }


def _buscar_cliente_por_id(id_cliente: int) -> Optional[dict]:
    """Busca cliente na lista global de clientes."""
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return None


def _listar_clientes_disponiveis() -> bool:
    """Lista clientes para seleção. Retorna True se houver clientes."""
    if not clientes:
        print("⚠️  Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
        return False

    print("\n👥 CLIENTES DISPONÍVEIS:")
    print(f"{'ID':<4} {'Nome':<30} {'Telefone':<16}")
    print("-" * 55)
    for c in clientes:
        nome = c["nome"][:28] + ".." if len(c["nome"]) > 30 else c["nome"]
        print(f"{c['id']:<4} {nome:<30} {c['telefone']:<16}")
    return True


def cadastrar_pet() -> None:
    """Cadastra um novo pet vinculado a um cliente."""
    limpar_tela()
    print("🐾 CADASTRAR NOVO PET")
    print("-" * 40)

    if not _listar_clientes_disponiveis():
        pausar()
        return

    try:
        id_cliente = obter_int("\nID do tutor (cliente): ")
        cliente = _buscar_cliente_por_id(id_cliente)
        if not cliente:
            print(f"\n❌ Cliente com ID {id_cliente} não encontrado.")
            pausar()
            return

        print(f"\nTutor selecionado: {cliente['nome']}")

        nome = obter_str_obrigatorio("Nome do pet: ")

        print(f"\nTipos disponíveis: {', '.join(TIPOS_PET)}")
        tipo = obter_str_obrigatorio("Tipo: ").capitalize()
        while tipo not in TIPOS_PET:
            print(f"⚠️  Tipo inválido. Opções: {', '.join(TIPOS_PET)}")
            tipo = obter_str_obrigatorio("Tipo: ").capitalize()

        raca = obter_str_obrigatorio("Raça: ")

        idade = obter_int("Idade (anos): ")
        while idade < 0 or idade > 30:
            print("⚠️  Idade inválida (0 a 30 anos).")
            idade = obter_int("Idade (anos): ")

        peso = float(input("Peso (kg): ").strip().replace(",", "."))
        while peso <= 0 or peso > 100:
            print("⚠️  Peso inválido (0.1 a 100 kg).")
            peso = float(input("Peso (kg): ").strip().replace(",", "."))

        print(f"\nPortes disponíveis: {', '.join(PORTES)}")
        porte = obter_str_obrigatorio("Porte: ").capitalize()
        while porte not in PORTES:
            print(f"⚠️  Porte inválido. Opções: {', '.join(PORTES)}")
            porte = obter_str_obrigatorio("Porte: ").capitalize()

        observacoes = obter_str_opcional("Observações (opcional): ")

        id_pet = _gerar_id()
        pet = _pet_para_dict(
            id_pet, id_cliente, nome, tipo, raca, idade, peso, porte, observacoes
        )
        pets.append(pet)

        print(f"\n✅ Pet cadastrado com sucesso! (ID: {id_pet})")
        print(f"   Nome: {nome} | Tipo: {tipo} | Raça: {raca}")
        print(f"   Idade: {idade} anos | Peso: {peso} kg | Porte: {porte}")
        print(f"   Tutor: {cliente['nome']}")

    except ValueError:
        print("\n❌ Valor numérico inválido.")
    except Exception as e:
        print(f"\n❌ Erro inesperado ao cadastrar: {e}")

    pausar()


def listar_pets() -> None:
    """Lista todos os pets cadastrados."""
    limpar_tela()
    print("📋 LISTA DE PETS (PACIENTES)")
    print("-" * 80)

    if not pets:
        print("📭 Nenhum pet cadastrado.")
        pausar()
        return

    print(f"{'ID':<4} {'Nome':<15} {'Tipo':<10} {'Raça':<15} {'Idade':<6} {'Peso':<6} {'Tutor':<20}")
    print("-" * 90)

    for pet in pets:
        cliente = _buscar_cliente_por_id(pet["id_cliente"])
        tutor_nome = cliente["nome"][:18] + ".." if cliente and len(cliente["nome"]) > 20 else (cliente["nome"] if cliente else "Desconhecido")

        nome = pet["nome"][:13] + ".." if len(pet["nome"]) > 15 else pet["nome"]
        raca = pet["raca"][:13] + ".." if len(pet["raca"]) > 15 else pet["raca"]

        print(f"{pet['id']:<4} {nome:<15} {pet['tipo']:<10} {raca:<15} {pet['idade']:<6} {pet['peso']:<6.1f} {tutor_nome:<20}")

    print(f"\n📊 Total: {len(pets)} pet(s)")
    pausar()


def listar_pets_por_cliente(id_cliente: int) -> None:
    """Lista pets de um cliente específico."""
    limpar_tela()
    cliente = _buscar_cliente_por_id(id_cliente)
    if not cliente:
        print(f"❌ Cliente ID {id_cliente} não encontrado.")
        pausar()
        return

    pets_cliente = [p for p in pets if p["id_cliente"] == id_cliente]

    print(f"🐾 PETS DO TUTOR: {cliente['nome']}")
    print("-" * 60)

    if not pets_cliente:
        print("📭 Este tutor não possui pets cadastrados.")
        pausar()
        return

    for pet in pets_cliente:
        print(f"  ID: {pet['id']} | {pet['nome']} ({pet['tipo']}, {pet['raca']}, {pet['idade']}a, {pet['peso']}kg)")

    print(f"\n📊 Total: {len(pets_cliente)} pet(s)")
    pausar()


def buscar_pet(id_busca: Optional[int] = None) -> Optional[dict]:
    """Busca um pet pelo ID."""
    if id_busca is None:
        limpar_tela()
        print("🔍 BUSCAR PET")
        print("-" * 30)
        try:
            id_busca = obter_int("Digite o ID do pet: ")
        except ValueError:
            print("❌ ID inválido.")
            pausar()
            return None

    for pet in pets:
        if pet["id"] == id_busca:
            cliente = _buscar_cliente_por_id(pet["id_cliente"])
            limpar_tela()
            print("🔎 PET ENCONTRADO")
            print("-" * 40)
            print(f"ID:           {pet['id']}")
            print(f"Nome:         {pet['nome']}")
            print(f"Tipo:         {pet['tipo']}")
            print(f"Raça:         {pet['raca']}")
            print(f"Idade:        {pet['idade']} anos")
            print(f"Peso:         {pet['peso']} kg")
            print(f"Porte:        {pet['porte']}")
            print(f"Observações:  {pet['observacoes'] or 'Nenhuma'}")
            print(f"Tutor:        {cliente['nome'] if cliente else 'Desconhecido'} (ID: {pet['id_cliente']})")
            pausar()
            return pet

    print(f"\n❌ Pet com ID {id_busca} não encontrado.")
    pausar()
    return None


def atualizar_pet() -> None:
    """Atualiza os dados de um pet existente."""
    limpar_tela()
    print("✏️  ATUALIZAR PET")
    print("-" * 30)

    try:
        id_pet = obter_int("Digite o ID do pet a atualizar: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    pet = None
    for p in pets:
        if p["id"] == id_pet:
            pet = p
            break

    if not pet:
        print(f"\n❌ Pet com ID {id_pet} não encontrado.")
        pausar()
        return

    print(f"\nPet atual: {pet['nome']} ({pet['tipo']})")
    print("Deixe em branco para manter o valor atual.\n")

    try:
        novo_nome = input(f"Novo nome [{pet['nome']}]: ").strip()
        if novo_nome:
            pet["nome"] = novo_nome

        print(f"Tipos: {', '.join(TIPOS_PET)}")
        novo_tipo = input(f"Novo tipo [{pet['tipo']}]: ").strip().capitalize()
        if novo_tipo and novo_tipo in TIPOS_PET:
            pet["tipo"] = novo_tipo
        elif novo_tipo:
            print("⚠️  Tipo inválido, mantendo o atual.")

        nova_raca = input(f"Nova raça [{pet['raca']}]: ").strip()
        if nova_raca:
            pet["raca"] = nova_raca

        nova_idade_str = input(f"Nova idade [{pet['idade']}]: ").strip()
        if nova_idade_str:
            try:
                nova_idade = int(nova_idade_str)
                if 0 <= nova_idade <= 30:
                    pet["idade"] = nova_idade
                else:
                    print("⚠️  Idade inválida, mantendo a atual.")
            except ValueError:
                print("⚠️  Valor inválido, mantendo o atual.")

        novo_peso_str = input(f"Novo peso [{pet['peso']}]: ").strip().replace(",", ".")
        if novo_peso_str:
            try:
                novo_peso = float(novo_peso_str)
                if 0 < novo_peso <= 100:
                    pet["peso"] = novo_peso
                else:
                    print("⚠️  Peso inválido, mantendo o atual.")
            except ValueError:
                print("⚠️  Valor inválido, mantendo o atual.")

        print(f"Portes: {', '.join(PORTES)}")
        novo_porte = input(f"Novo porte [{pet['porte']}]: ").strip().capitalize()
        if novo_porte and novo_porte in PORTES:
            pet["porte"] = novo_porte
        elif novo_porte:
            print("⚠️  Porte inválido, mantendo o atual.")

        novas_obs = input(f"Novas observações [{pet['observacoes'] or ''}]: ").strip()
        if novas_obs is not None:
            pet["observacoes"] = novas_obs

        print("\n✅ Pet atualizado com sucesso!")

    except Exception as e:
        print(f"\n❌ Erro ao atualizar: {e}")

    pausar()


def excluir_pet() -> None:
    """Exclui um pet do sistema."""
    limpar_tela()
    print("🗑️  EXCLUIR PET")
    print("-" * 30)

    try:
        id_pet = obter_int("Digite o ID do pet a excluir: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    for i, pet in enumerate(pets):
        if pet["id"] == id_pet:
            cliente = _buscar_cliente_por_id(pet["id_cliente"])
            tutor = cliente["nome"] if cliente else "Desconhecido"
            print(f"\nPet encontrado: {pet['nome']} (ID: {pet['id']}) - Tutor: {tutor}")
            if confirmar("Tem certeza que deseja excluir? (s/n): "):
                pets.pop(i)
                print("\n✅ Pet excluído com sucesso!")
            else:
                print("\n❌ Exclusão cancelada.")
            pausar()
            return

    print(f"\n❌ Pet com ID {id_pet} não encontrado.")
    pausar()


def menu_pets() -> None:
    """Menu específico do módulo de pets."""
    while True:
        limpar_tela()
        print("🐾 MÓDULO: PETS (PACIENTES)")
        print("-" * 40)
        print("1. ➕ Cadastrar Pet")
        print("2. 📋 Listar Todos os Pets")
        print("3. 🔍 Buscar Pet por ID")
        print("4. 📋 Listar Pets por Tutor")
        print("5. ✏️  Atualizar Pet")
        print("6. 🗑️  Excluir Pet")
        print("0. ↩️  Voltar ao Menu Principal")
        print("-" * 40)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_pet()
        elif opcao == "2":
            listar_pets()
        elif opcao == "3":
            buscar_pet()
        elif opcao == "4":
            if _listar_clientes_disponiveis():
                try:
                    id_cli = obter_int("\nID do tutor: ")
                    listar_pets_por_cliente(id_cli)
                except ValueError:
                    print("❌ ID inválido.")
                    pausar()
            else:
                pausar()
        elif opcao == "5":
            atualizar_pet()
        elif opcao == "6":
            excluir_pet()
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")
            pausar()


def _carregar_dados_exemplo() -> None:
    """Carrega dados de exemplo para demonstração."""
    global _proximo_id_pet
    if not clientes:
        return

    exemplos = [
        (1, "Rex", "Cachorro", "Golden Retriever", 3, 28.5, "Grande", "Vacinas em dia"),
        (1, "Mimi", "Gato", "Siamês", 2, 4.2, "Pequeno", "Castrada"),
        (2, "Bolinha", "Cachorro", "Poodle", 5, 8.0, "Médio", "Alergia a pulgas"),
        (3, "Pedro", "Pássaro", "Calopsita", 1, 0.1, "Pequeno", ""),
    ]
    for id_cli, nome, tipo, raca, idade, peso, porte, obs in exemplos:
        if _buscar_cliente_por_id(id_cli):
            pets.append(_pet_para_dict(_gerar_id(), id_cli, nome, tipo, raca, idade, peso, porte, obs))


_carregar_dados_exemplo()