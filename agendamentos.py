#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Agendamentos - SysPet
Funcionalidades: Cadastro, Alteração, Exclusão, Listagem, Busca.
Vincula: Cliente (Tutor) + Pet + Veterinário + Data/Hora + Serviço.
"""

from datetime import datetime, date
from typing import Optional
from utils import (
    limpar_tela,
    pausar,
    confirmar,
    obter_int,
    obter_str_obrigatorio,
    obter_str_opcional,
)
from clientes import clientes, _buscar_cliente_por_id
from pets import pets, _buscar_cliente_por_id as _buscar_cliente_pets, buscar_pet
from veterinarios import veterinarios, buscar_veterinario


# Lista global em memória para armazenar agendamentos
agendamentos: list[dict] = []

# Contador para IDs auto-incrementais
_proximo_id_agend: int = 1

# Tipos de serviço
TIPOS_SERVICO = (
    "Consulta",
    "Vacinação",
    "Banho e Tosa",
    "Cirurgia",
    "Exames",
    "Emergência",
    "Retorno",
    "Outro",
)

# Status de agendamento
STATUS_AGENDAMENTO = (
    "Agendado",
    "Confirmado",
    "Em Atendimento",
    "Concluído",
    "Cancelado",
    "Não Compareceu",
)


def _gerar_id() -> int:
    """Gera um ID único sequencial para novo agendamento."""
    global _proximo_id_agend
    id_atual = _proximo_id_agend
    _proximo_id_agend += 1
    return id_atual


def _agend_para_dict(
    id_agend: int,
    id_cliente: int,
    id_pet: int,
    id_veterinario: int,
    data_hora: str,
    tipo_servico: str,
    status: str,
    observacoes: str,
) -> dict:
    """Cria dicionário padronizado de agendamento."""
    return {
        "id": id_agend,
        "id_cliente": id_cliente,
        "id_pet": id_pet,
        "id_veterinario": id_veterinario,
        "data_hora": data_hora,
        "tipo_servico": tipo_servico,
        "status": status,
        "observacoes": observacoes,
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }


def _validar_data_hora(data_str: str) -> Optional[datetime]:
    """Valida e converte string de data/hora para objeto datetime.
    Formato esperado: DD/MM/AAAA HH:MM"""
    try:
        return datetime.strptime(data_str.strip(), "%d/%m/%Y %H:%M")
    except ValueError:
        return None


def _formatar_data_hora(dt: datetime) -> str:
    """Formata datetime para string DD/MM/AAAA HH:MM."""
    return dt.strftime("%d/%m/%Y %H:%M")


def _data_hora_atual_str() -> str:
    """Retorna data/hora atual formatada."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def _listar_clientes_com_pets() -> bool:
    """Lista clientes que têm pets. Retorna True se houver."""
    clientes_com_pets = []
    for cliente in clientes:
        pets_cliente = [p for p in pets if p["id_cliente"] == cliente["id"]]
        if pets_cliente:
            clientes_com_pets.append((cliente, pets_cliente))

    if not clientes_com_pets:
        print("⚠️  Nenhum cliente com pets cadastrado.")
        return False

    print("\n👥 CLIENTES COM PETS:")
    for cliente, pets_cli in clientes_com_pets:
        print(f"  ID:{cliente['id']:3d} | {cliente['nome']:<25} ({len(pets_cli)} pet(s))")
        for pet in pets_cli:
            print(f"         └─ Pet ID:{pet['id']:3d} | {pet['nome']:<15} ({pet['tipo']})")
    return True


def _listar_veterinarios_disponiveis() -> bool:
    """Lista veterinários disponíveis."""
    if not veterinarios:
        print("⚠️  Nenhum veterinário cadastrado.")
        return False

    print("\n👨‍⚕️ VETERINÁRIOS DISPONÍVEIS:")
    for vet in veterinarios:
        print(f"  ID:{vet['id']:3d} | {vet['nome']:<25} | {vet['especialidade']:<20} | {vet['telefone']}")
    return True


def cadastrar_agendamento() -> None:
    """Cadastra um novo agendamento."""
    limpar_tela()
    print("📅 NOVO AGENDAMENTO")
    print("-" * 50)

    # 1. Selecionar cliente e pet
    if not _listar_clientes_com_pets():
        print("   Cadastre clientes e pets primeiro.")
        pausar()
        return

    try:
        id_cliente = obter_int("\nID do Cliente (Tutor): ")
        cliente = _buscar_cliente_por_id(id_cliente)
        if not cliente:
            print(f"❌ Cliente ID {id_cliente} não encontrado.")
            pausar()
            return

        # Filtrar pets do cliente
        pets_cliente = [p for p in pets if p["id_cliente"] == id_cliente]
        if not pets_cliente:
            print("❌ Este cliente não possui pets cadastrados.")
            pausar()
            return

        print(f"\n🐾 Pets de {cliente['nome']}:")
        for pet in pets_cliente:
            print(f"  ID:{pet['id']:3d} | {pet['nome']:<15} ({pet['tipo']}, {pet['raca']})")

        id_pet = obter_int("\nID do Pet: ")
        pet = None
        for p in pets_cliente:
            if p["id"] == id_pet:
                pet = p
                break
        if not pet:
            print(f"❌ Pet ID {id_pet} não pertence a este cliente.")
            pausar()
            return

        # 2. Selecionar veterinário
        if not _listar_veterinarios_disponiveis():
            print("   Cadastre veterinários primeiro.")
            pausar()
            return

        id_vet = obter_int("\nID do Veterinário: ")
        vet = None
        for v in veterinarios:
            if v["id"] == id_vet:
                vet = v
                break
        if not vet:
            print(f"❌ Veterinário ID {id_vet} não encontrado.")
            pausar()
            return

        # 3. Data e hora
        print(f"\n📅 Data/Hora atual: {_data_hora_atual_str()}")
        print("   Formato: DD/MM/AAAA HH:MM (ex: 25/06/2026 14:30)")
        while True:
            data_str = obter_str_obrigatorio("Data e Hora do agendamento: ")
            dt = _validar_data_hora(data_str)
            if dt is None:
                print("❌ Formato inválido. Use DD/MM/AAAA HH:MM")
                continue
            if dt < datetime.now():
                print("⚠️  Não é possível agendar no passado.")
                continue
            data_hora = _formatar_data_hora(dt)
            break

        # 4. Tipo de serviço
        print(f"\n🏥 Tipos de serviço:")
        for i, ts in enumerate(TIPOS_SERVICO, 1):
            print(f"  {i:2d}. {ts}")
        while True:
            try:
                escolha = obter_int("Escolha o tipo (número): ")
                if 1 <= escolha <= len(TIPOS_SERVICO):
                    tipo_servico = TIPOS_SERVICO[escolha - 1]
                    break
                print(f"⚠️  Opção 1 a {len(TIPOS_SERVICO)}.")
            except ValueError:
                print("❌ Digite um número.")

        # 5. Observações
        observacoes = obter_str_opcional("Observações (opcional): ")

        # Status inicial
        status = "Agendado"

        # Criar agendamento
        id_agend = _gerar_id()
        agend = _agend_para_dict(
            id_agend, id_cliente, id_pet, id_vet, data_hora, tipo_servico, status, observacoes
        )
        agendamentos.append(agend)

        print(f"\n✅ Agendamento criado com sucesso! (ID: {id_agend})")
        print(f"   📅 Data/Hora: {data_hora}")
        print(f"   👤 Tutor: {cliente['nome']}")
        print(f"   🐾 Pet: {pet['nome']} ({pet['tipo']})")
        print(f"   👨‍⚕️ Vet: {vet['nome']} ({vet['especialidade']})")
        print(f"   🏥 Serviço: {tipo_servico}")
        print(f"   📌 Status: {status}")

    except ValueError:
        print("\n❌ Valor inválido.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

    pausar()


def listar_agendamentos(filtrar_status: Optional[str] = None) -> None:
    """Lista todos os agendamentos, opcionalmente filtrados por status."""
    limpar_tela()
    titulo = "📋 LISTA DE AGENDAMENTOS"
    if filtrar_status:
        titulo += f" - Status: {filtrar_status}"
    print(titulo)
    print("-" * 100)

    if not agendamentos:
        print("📭 Nenhum agendamento cadastrado.")
        pausar()
        return

    # Filtrar se necessário
    lista = agendamentos
    if filtrar_status:
        lista = [a for a in agendamentos if a["status"] == filtrar_status]

    if not lista:
        print(f"📭 Nenhum agendamento com status '{filtrar_status}'.")
        pausar()
        return

    print(f"{'ID':<4} {'Data/Hora':<16} {'Tutor':<18} {'Pet':<15} {'Veterinário':<20} {'Serviço':<15} {'Status':<12}")
    print("-" * 110)

    for ag in sorted(lista, key=lambda x: x["data_hora"]):
        cliente = _buscar_cliente_por_id(ag["id_cliente"])
        pet = next((p for p in pets if p["id"] == ag["id_pet"]), None)
        vet = next((v for v in veterinarios if v["id"] == ag["id_veterinario"]), None)

        tutor = cliente["nome"][:16] + ".." if cliente and len(cliente["nome"]) > 18 else (cliente["nome"] if cliente else "?")
        pet_nome = pet["nome"][:13] + ".." if pet and len(pet["nome"]) > 15 else (pet["nome"] if pet else "?")
        vet_nome = vet["nome"][:18] + ".." if vet and len(vet["nome"]) > 20 else (vet["nome"] if vet else "?")
        serv = ag["tipo_servico"][:13] + ".." if len(ag["tipo_servico"]) > 15 else ag["tipo_servico"]
        status = ag["status"][:10] + ".." if len(ag["status"]) > 12 else ag["status"]

        print(f"{ag['id']:<4} {ag['data_hora']:<16} {tutor:<18} {pet_nome:<15} {vet_nome:<20} {serv:<15} {status:<12}")

    print(f"\n📊 Total: {len(lista)} agendamento(s)")
    pausar()


def listar_agendamentos_hoje() -> None:
    """Lista agendamentos de hoje."""
    limpar_tela()
    hoje = date.today().strftime("%d/%m/%Y")
    print(f"📅 AGENDAMENTOS DE HOJE ({hoje})")
    print("-" * 100)

    hoje_agends = [a for a in agendamentos if a["data_hora"].startswith(hoje)]

    if not hoje_agends:
        print("📭 Nenhum agendamento para hoje.")
        pausar()
        return

    for ag in sorted(hoje_agends, key=lambda x: x["data_hora"]):
        cliente = _buscar_cliente_por_id(ag["id_cliente"])
        pet = next((p for p in pets if p["id"] == ag["id_pet"]), None)
        vet = next((v for v in veterinarios if v["id"] == ag["id_veterinario"]), None)
        print(f"  {ag['data_hora'][11:]} | {ag['tipo_servico']:<15} | {pet['nome'] if pet else '?'}({cliente['nome'] if cliente else '?'}) | Dr(a). {vet['nome'] if vet else '?'} | {ag['status']}")

    pausar()


def buscar_agendamento(id_busca: Optional[int] = None) -> Optional[dict]:
    """Busca um agendamento pelo ID."""
    if id_busca is None:
        limpar_tela()
        print("🔍 BUSCAR AGENDAMENTO")
        print("-" * 30)
        try:
            id_busca = obter_int("Digite o ID do agendamento: ")
        except ValueError:
            print("❌ ID inválido.")
            pausar()
            return None

    for ag in agendamentos:
        if ag["id"] == id_busca:
            cliente = _buscar_cliente_por_id(ag["id_cliente"])
            pet = next((p for p in pets if p["id"] == ag["id_pet"]), None)
            vet = next((v for v in veterinarios if v["id"] == ag["id_veterinario"]), None)

            limpar_tela()
            print("🔎 AGENDAMENTO ENCONTRADO")
            print("-" * 50)
            print(f"ID:            {ag['id']}")
            print(f"Data/Hora:     {ag['data_hora']}")
            print(f"Tutor:         {cliente['nome'] if cliente else 'Desconhecido'} (ID: {ag['id_cliente']})")
            print(f"Pet:           {pet['nome'] if pet else 'Desconhecido'} (ID: {ag['id_pet']})")
            print(f"Veterinário:   {vet['nome'] if vet else 'Desconhecido'} (ID: {ag['id_veterinario']})")
            print(f"Serviço:       {ag['tipo_servico']}")
            print(f"Status:        {ag['status']}")
            print(f"Observações:   {ag['observacoes'] or 'Nenhuma'}")
            print(f"Criado em:     {ag['criado_em']}")
            pausar()
            return ag

    print(f"\n❌ Agendamento com ID {id_busca} não encontrado.")
    pausar()
    return None


def atualizar_agendamento() -> None:
    """Atualiza um agendamento (principalmente status)."""
    limpar_tela()
    print("✏️  ATUALIZAR AGENDAMENTO")
    print("-" * 30)

    try:
        id_agend = obter_int("Digite o ID do agendamento: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    ag = None
    for a in agendamentos:
        if a["id"] == id_agend:
            ag = a
            break

    if not ag:
        print(f"\n❌ Agendamento ID {id_agend} não encontrado.")
        pausar()
        return

    cliente = _buscar_cliente_por_id(ag["id_cliente"])
    pet = next((p for p in pets if p["id"] == ag["id_pet"]), None)
    vet = next((v for v in veterinarios if v["id"] == ag["id_veterinario"]), None)

    print(f"\nAgendamento: {ag['data_hora']} | {pet['nome'] if pet else '?'} | {vet['nome'] if vet else '?'} | {ag['tipo_servico']}")
    print(f"Status atual: {ag['status']}")
    print("\nO que deseja alterar?")
    print("1. Status")
    print("2. Data/Hora")
    print("3. Veterinário")
    print("4. Observações")
    print("0. Cancelar")

    opcao = input("Escolha: ").strip()

    try:
        if opcao == "1":
            print(f"\nStatus atuais: {', '.join(STATUS_AGENDAMENTO)}")
            print(f"Atual: {ag['status']}")
            novo_status = input("Novo status: ").strip().capitalize()
            if novo_status in STATUS_AGENDAMENTO:
                ag["status"] = novo_status
                print("✅ Status atualizado!")
            else:
                print("⚠️  Status inválido.")

        elif opcao == "2":
            print(f"Atual: {ag['data_hora']}")
            print("Formato: DD/MM/AAAA HH:MM")
            while True:
                nova_data = input("Nova data/hora: ").strip()
                dt = _validar_data_hora(nova_data)
                if dt is None:
                    print("❌ Formato inválido.")
                    continue
                if dt < datetime.now():
                    print("⚠️  Não pode ser no passado.")
                    continue
                ag["data_hora"] = _formatar_data_hora(dt)
                print("✅ Data/Hora atualizada!")
                break

        elif opcao == "3":
            print(f"Atual: {vet['nome'] if vet else 'N/A'}")
            if _listar_veterinarios_disponiveis():
                try:
                    id_vet = obter_int("Novo veterinário ID: ")
                    novo_vet = next((v for v in veterinarios if v["id"] == id_vet), None)
                    if novo_vet:
                        ag["id_veterinario"] = id_vet
                        print("✅ Veterinário atualizado!")
                    else:
                        print("❌ Veterinário não encontrado.")
                except ValueError:
                    print("❌ ID inválido.")

        elif opcao == "4":
            print(f"Atual: {ag['observacoes'] or 'Nenhuma'}")
            nova_obs = input("Novas observações: ").strip()
            ag["observacoes"] = nova_obs
            print("✅ Observações atualizadas!")

        elif opcao == "0":
            print("❌ Cancelado.")
        else:
            print("❌ Opção inválida.")

    except Exception as e:
        print(f"\n❌ Erro: {e}")

    pausar()


def excluir_agendamento() -> None:
    """Exclui um agendamento."""
    limpar_tela()
    print("🗑️  EXCLUIR AGENDAMENTO")
    print("-" * 30)

    try:
        id_agend = obter_int("Digite o ID do agendamento: ")
    except ValueError:
        print("❌ ID inválido.")
        pausar()
        return

    for i, ag in enumerate(agendamentos):
        if ag["id"] == id_agend:
            cliente = _buscar_cliente_por_id(ag["id_cliente"])
            pet = next((p for p in pets if p["id"] == ag["id_pet"]), None)
            print(f"\nAgendamento: {ag['data_hora']} | {pet['nome'] if pet else '?'} | {ag['tipo_servico']} | {ag['status']}")
            print(f"Tutor: {cliente['nome'] if cliente else 'Desconhecido'}")
            if confirmar("Excluir definitivamente? (s/n): "):
                agendamentos.pop(i)
                print("\n✅ Agendamento excluído!")
            else:
                print("\n❌ Cancelado.")
            pausar()
            return

    print(f"\n❌ Agendamento ID {id_agend} não encontrado.")
    pausar()


def menu_agendamentos() -> None:
    """Menu específico do módulo de agendamentos."""
    while True:
        limpar_tela()
        print("📅 MÓDULO: AGENDAMENTOS")
        print("-" * 50)
        print("1. ➕ Novo Agendamento")
        print("2. 📋 Listar Todos")
        print("3. 📅 Ver Agendamentos de Hoje")
        print("4. 🔍 Buscar por ID")
        print("5. 📋 Filtrar por Status")
        print("6. ✏️  Atualizar Agendamento")
        print("7. 🗑️  Excluir Agendamento")
        print("0. ↩️  Voltar ao Menu Principal")
        print("-" * 50)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_agendamento()
        elif opcao == "2":
            listar_agendamentos()
        elif opcao == "3":
            listar_agendamentos_hoje()
        elif opcao == "4":
            buscar_agendamento()
        elif opcao == "5":
            limpar_tela()
            print("📋 FILTRAR POR STATUS")
            print("-" * 30)
            for i, s in enumerate(STATUS_AGENDAMENTO, 1):
                print(f"  {i}. {s}")
            try:
                esc = obter_int("Escolha: ")
                if 1 <= esc <= len(STATUS_AGENDAMENTO):
                    listar_agendamentos(STATUS_AGENDAMENTO[esc - 1])
                else:
                    print("❌ Opção inválida.")
                    pausar()
            except ValueError:
                print("❌ Inválido.")
                pausar()
        elif opcao == "6":
            atualizar_agendamento()
        elif opcao == "7":
            excluir_agendamento()
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida.")
            pausar()


def _carregar_dados_exemplo() -> None:
    """Carrega agendamentos de exemplo."""
    global _proximo_id_agend
    # Só cria se houver clientes, pets e veterinários
    if not (clientes and pets and veterinarios):
        return

    from datetime import timedelta

    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    exemplos = [
        (1, 1, 1, base + timedelta(days=1, hours=2), "Consulta", "Agendado", "Check-up anual"),
        (2, 3, 2, base + timedelta(days=1, hours=4), "Vacinação", "Confirmado", "V10 + Raiva"),
        (1, 2, 1, base + timedelta(days=2, hours=1), "Banho e Tosa", "Agendado", "Tosa higiênica"),
        (3, 4, 3, base + timedelta(days=3, hours=3), "Retorno", "Agendado", "Pós-cirúrgico"),
    ]

    for id_cli, id_pet, id_vet, dt, serv, status, obs in exemplos:
        # Verificar se IDs existem
        cli = _buscar_cliente_por_id(id_cli)
        pt = next((p for p in pets if p["id"] == id_pet), None)
        vt = next((v for v in veterinarios if v["id"] == id_vet), None)
        if cli and pt and vt:
            agendamentos.append(_agend_para_dict(
                _gerar_id(), id_cli, id_pet, id_vet,
                _formatar_data_hora(dt), serv, status, obs
            ))


_carregar_dados_exemplo()