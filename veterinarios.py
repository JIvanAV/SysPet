#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Veterinários - SysPet
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
    obter_str_opcional,
)


# Lista global em memória para armazenar veterinários
veterinarios: list[dict] = []

# Contador para IDs auto-incrementais
_proximo_id_vet: int = 1

# Especialidades disponíveis
ESPECIALIDADES = (
    "Clínica Geral",
    "Cirurgia",
    "Dermatologia",
    "Oftalmologia",
    "Cardiologia",
    "Ortopedia",
    "Oncologia",
    "Comportamento",
    "Exóticos/Silvestres",
    "Outra",
)


def _gerar_id() -> int:
    """Gera um ID único sequencial para novo veterinário."""
    global _proximo_id_vet
    id_atual = _proximo_id_vet
    _proximo_id_vet += 1
    return id_atual


def _vet_para_dict(
    id_vet: int,
    nome: str,
    crmv: str,
    telefone: str,
    email: str,
    especialidade: str,
    observacoes: str,
) -> dict:
    """Cria dicionário padronizado de veterinário."""
    return {
        "id": id_vet,
        "nome": nome,
        "crmv": crmv,
        "telefone": telefone,
        "email": email,
        "especialidade": especialidade,
        "observacoes": observacoes,
    }


def cadastrar_veterinario() -> None:
    """Cadastra um novo veterinário no sistema."""
    limpar_tela()
    print("👨‍⚕️ CADASTRAR NOVO VETERINÁRIO")
    print("-" * 40)

    try:
        nome = obter_str_obrigatorio("Nome completo: ")

        crmv = obter_str_obrigatorio("CRMV (Registro Conselho): ").upper().strip()
        # Verifica se CRMV já existe
        for v in veterinarios:
            if v["crmv"] == crmv:
                print(f"\n❌ CRMV {crmv} já cadastrado para {v['nome']}.")
                pausar()
                return

        telefone = obter_str_obrigatorio("Telefone (com DDD): ")
        while not validar_telefone(telefone):
            print("⚠️  Telefone inválido. Use formato: (XX) XXXXX-XXXX")
            telefone = obter_str_obrigatorio("Telefone (com DDD): ")

        email = obter_str_obrigatorio("E-mail: ")
        while not validar_email(email):
            print("⚠️  E-mail inválido. Exemplo: vet@clinica.com")
            email = obter_str_obrigatorio("E-mail: ")

        print(f"\nEspecialidades disponíveis:")
        for i, esp in enumerate(ESPECIALIDADES, 1):
            print(f"  {i:2d}. {esp}")

        while True:
            try:
                escolha = obter_int("\nEscolha o número da especialidade: ")
                if 1 <= escolha <= len(ESPECIALIDADES):
                    especialidade = ESPECIALIDADES[escolha - 1]
                    break
                print(f"⚠️  Opção inválida. Digite 1 a {len(ESPECIALIDADES)}.")
            except ValueError:
                print("❌ Digite um número válido.")

        observacoes = obter_str_opcional("Observações (opcional): ")

        id_vet = _gerar_id()
        vet = _vet_para_dict(id_vet, nome, crmv, telefone, email, especialidade, observacoes)
        veterinarios.append(vet)

        print(f"\n✅ Veterinário cadastrado com sucesso! (ID: {id_vet})")
        print(f"   Nome: {nome}")
        print(f"   CRMV: {crmv}")
        print(f"   Especialidade: {especialidade}")
        print(f"   Telefone: {telefone}")
        print(f"   E-mail: {email}")

    except ValueError:
        print("\n❌ Valor inválido.")
    except Exception as e:
        print(f"\n❌ Erro inesperado ao cadastrar: {e}")

    pausar()


def listar_veterinarios() -> None:
    """Lista todos os veterinários cadastrados."""
    limpar_tela()
    print("📋 LISTA DE VETERINÁRIOS")
    print("-" * 80)

    if not veterinarios:
        print("📭 Nenhum veterinário cadastrado.")
        pausar()
        return

    print(f"{'ID':<4} {'Nome':<25} {'CRMV':<12} {'Especialidade':<20} {'Telefone':<16}")
    print("-" * 85)

    for vet in veterinarios:
        nome = vet["nome"][:23] + ".." if len(vet["nome"]) > 25 else vet["nome"]
        esp = vet["especialidade"][:18] + ".." if len(vet["especialidade"]) > 20 else vet["especialidade"]
        print(f"{vet['id']:<4} {nome:<25} {vet['crmv']:<12} {esp:<20} {vet['telefone']:<16}")

    print(f"\n📊 Total: {len(veterinarios)} veterinário(s)")
    pausar()


def buscar_veterinario(id_busca: Optional[int] = None) -> Optional[dict]:
    """Busca um veterinário pelo ID."""
    if id_busca is None:
        limpar_tela()
        print("🔍 BUSCAR VETERINÁRIO")
        print("-" * 30)
        try:
            id_busca = obter_int("Digite o ID do veterinário: ")
        except ValueError:
            print("❌ ID inválido.")
            pausar()
            return None

    for vet in veterinarios:
        if vet["id"] == id_busca:
            limpar_tela()
            print("🔎 VETERINÁRIO ENCONTRADO")
            print("-" * 40)
            print(f"ID:            {vet['id']}")
            print(f"Nome:          {vet['nome']}")
            print(f"CRMV:          {vet['crmv']}")
            print(f"Especialidade: {vet['especialidade']}")
            print(f"Telefone:      {vet['telefone']}")
            print(f"E-mail:        {vet['email']}")
            print(f"Observações:   {vet['observacoes'] or 'Nenhuma'}")
            pausar()
            return vet

    print(f"\n❌ Veterinário com ID {id_busca} não encontrado.")
    pausar()
    return None


def buscar_veterinario_por_crmv(crmv: str) -> Optional[dict]:
    """Busca veterinário pelo CRMV."""
    for vet in veterinarios:
        if vet["crmv"] == crmv.upper():
            return vet
    return None


def atualizar_veterinario() -> None:
    """Atualiza os dados de um veterinário existente."""
    limpar_tela()
    print("✏️  ATUALIZAR VETERINÁRIO")
    print("-" * 30)

    try:
        id_vet = obter_int("Digite o ID do veterinário a atualizar: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    vet = None
    for v in veterinarios:
        if v["id"] == id_vet:
            vet = v
            break

    if not vet:
        print(f"\n❌ Veterinário com ID {id_vet} não encontrado.")
        pausar()
        return

    print(f"\nVeterinário atual: {vet['nome']} (CRMV: {vet['crmv']})")
    print("Deixe em branco para manter o valor atual.\n")

    try:
        novo_nome = input(f"Novo nome [{vet['nome']}]: ").strip()
        if novo_nome:
            vet["nome"] = novo_nome

        novo_crmv = input(f"Novo CRMV [{vet['crmv']}]: ").strip().upper()
        if novo_crmv:
            # Verifica se novo CRMV já existe em outro veterinário
            for v in veterinarios:
                if v["id"] != id_vet and v["crmv"] == novo_crmv:
                    print(f"⚠️  CRMV {novo_crmv} já cadastrado para {v['nome']}. Mantendo o atual.")
                    break
            else:
                vet["crmv"] = novo_crmv

        novo_telefone = input(f"Novo telefone [{vet['telefone']}]: ").strip()
        if novo_telefone:
            while not validar_telefone(novo_telefone):
                print("⚠️  Telefone inválido. Use formato: (XX) XXXXX-XXXX")
                novo_telefone = input(f"Novo telefone [{vet['telefone']}]: ").strip()
                if not novo_telefone:
                    break
            if novo_telefone:
                vet["telefone"] = novo_telefone

        novo_email = input(f"Novo e-mail [{vet['email']}]: ").strip()
        if novo_email:
            while not validar_email(novo_email):
                print("⚠️  E-mail inválido.")
                novo_email = input(f"Novo e-mail [{vet['email']}]: ").strip()
                if not novo_email:
                    break
            if novo_email:
                vet["email"] = novo_email

        print(f"\nEspecialidades disponíveis:")
        for i, esp in enumerate(ESPECIALIDADES, 1):
            marcador = " ← atual" if esp == vet["especialidade"] else ""
            print(f"  {i:2d}. {esp}{marcador}")

        escolha_str = input(f"\nNova especialidade [{vet['especialidade']}] (número): ").strip()
        if escolha_str:
            try:
                escolha = int(escolha_str)
                if 1 <= escolha <= len(ESPECIALIDADES):
                    vet["especialidade"] = ESPECIALIDADES[escolha - 1]
                else:
                    print("⚠️  Opção inválida, mantendo a atual.")
            except ValueError:
                print("⚠️  Valor inválido, mantendo a atual.")

        novas_obs = input(f"Novas observações [{vet['observacoes'] or ''}]: ").strip()
        if novas_obs is not None:
            vet["observacoes"] = novas_obs

        print("\n✅ Veterinário atualizado com sucesso!")

    except Exception as e:
        print(f"\n❌ Erro ao atualizar: {e}")

    pausar()


def excluir_veterinario() -> None:
    """Exclui um veterinário do sistema."""
    limpar_tela()
    print("🗑️  EXCLUIR VETERINÁRIO")
    print("-" * 30)

    try:
        id_vet = obter_int("Digite o ID do veterinário a excluir: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    for i, vet in enumerate(veterinarios):
        if vet["id"] == id_vet:
            print(f"\nVeterinário encontrado: {vet['nome']} (CRMV: {vet['crmv']})")
            if confirmar("Tem certeza que deseja excluir? (s/n): "):
                veterinarios.pop(i)
                print("\n✅ Veterinário excluído com sucesso!")
            else:
                print("\n❌ Exclusão cancelada.")
            pausar()
            return

    print(f"\n❌ Veterinário com ID {id_vet} não encontrado.")
    pausar()


def menu_veterinarios() -> None:
    """Menu específico do módulo de veterinários."""
    while True:
        limpar_tela()
        print("👨‍⚕️ MÓDULO: VETERINÁRIOS")
        print("-" * 40)
        print("1. ➕ Cadastrar Veterinário")
        print("2. 📋 Listar Veterinários")
        print("3. 🔍 Buscar por ID")
        print("4. 🔍 Buscar por CRMV")
        print("5. ✏️  Atualizar Veterinário")
        print("6. 🗑️  Excluir Veterinário")
        print("0. ↩️  Voltar ao Menu Principal")
        print("-" * 40)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_veterinario()
        elif opcao == "2":
            listar_veterinarios()
        elif opcao == "3":
            buscar_veterinario()
        elif opcao == "4":
            limpar_tela()
            print("🔍 BUSCAR POR CRMV")
            print("-" * 30)
            crmv = input("Digite o CRMV: ").strip().upper()
            if crmv:
                vet = buscar_veterinario_por_crmv(crmv)
                if vet:
                    print(f"\n✅ Encontrado: {vet['nome']} (ID: {vet['id']})")
                    print(f"   Especialidade: {vet['especialidade']}")
                    print(f"   Telefone: {vet['telefone']}")
                    print(f"   E-mail: {vet['email']}")
                else:
                    print(f"\n❌ Nenhum veterinário com CRMV {crmv}.")
            else:
                print("❌ CRMV não informado.")
            pausar()
        elif opcao == "5":
            atualizar_veterinario()
        elif opcao == "6":
            excluir_veterinario()
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")
            pausar()


def _carregar_dados_exemplo() -> None:
    """Carrega dados de exemplo para demonstração."""
    global _proximo_id_vet
    exemplos = [
        ("Dr. Carlos Mendes", "CRMV-PB 1234", "(83) 99999-0001", "carlos@amigofiel.com", "Clínica Geral", "Sócio fundador"),
        ("Dra. Ana Paula Silva", "CRMV-PB 5678", "(83) 99999-0002", "ana@amigofiel.com", "Dermatologia", "Especialista em alergias"),
        ("Dr. Rafael Oliveira", "CRMV-PB 9012", "(83) 99999-0003", "rafael@amigofiel.com", "Cirurgia", "Cirurgião de tecidos moles"),
    ]
    for nome, crmv, tel, email, esp, obs in exemplos:
        veterinarios.append(_vet_para_dict(_gerar_id(), nome, crmv, tel, email, esp, obs))


_carregar_dados_exemplo()