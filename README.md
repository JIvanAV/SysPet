# SysPet - Sistema de Gestão de PetShop

Projeto acadêmico da disciplina **Programação Estruturada em Python** — FASE 1  
Instituição: **FACISA** | Curso: **Sistemas de Informação**

---

## 📋 Descrição

O **SysPet** é um sistema de gestão para a rede **PetShop Amigo Fiel**, desenvolvido para automatizar e otimizar processos administrativos e operacionais: cadastro de tutores, pets, veterinários e agendamentos de serviços.

> **Contexto do projeto:** A rede Amigo Fiel cresceu 45% no início de 2026, gerando desafios no controle de atendimentos, agendamentos, histórico dos animais, estoque e organização financeira. O SysPet resolve isso com menus interativos no terminal, usando apenas estruturas em memória (listas, dicionários, tuplas) — sem banco de dados.

---

## ✨ Funcionalidades

| Módulo | Operações |
|--------|-----------|
| **Clientes (Tutores)** | Cadastrar, Listar, Buscar por ID, Atualizar, Excluir |
| **Pets (Pacientes)** | Cadastrar (vinculado a tutor), Listar, Buscar, Listar por tutor, Atualizar, Excluir |
| **Veterinários** | Cadastrar (com CRMV e especialidade), Listar, Buscar por ID/CRMV, Atualizar, Excluir |
| **Agendamentos** | Novo agendamento (tutor + pet + vet + data/hora + serviço), Listar todos, Ver agenda de hoje, Filtrar por status, Atualizar status/data/vet/obs, Excluir |

### Serviços disponíveis
- Consulta
- Vacinação
- Banho e Tosa
- Cirurgia
- Exames
- Emergência
- Retorno
- Outro

### Status de agendamento
- Agendado → Confirmado → Em Atendimento → Concluído
- Cancelado / Não Compareceu

---

## 🛠️ Tecnologias e Conceitos Aplicados

- **Python 3.11+** (apenas bibliotecas nativas)
- **Programação estruturada** + **modularização** (arquivos separados)
- **Estruturas de dados**: listas, dicionários, tuplas
- **Funções** com docstrings e type hints
- **Tratamento de exceções** (`try/except`)
- **Validação de entrada** (e-mail, telefone, datas, números)
- **Menus interativos** no terminal (CLI)
- **Dados de exemplo** carregados automaticamente para demonstração

---

## 📁 Estrutura do Projeto

```
syspet/
├── main.py              # Menu principal e orquestração
├── clientes.py          # Módulo de Clientes (Tutores)
├── pets.py              # Módulo de Pets (Pacientes)
├── veterinarios.py      # Módulo de Veterinários
├── agendamentos.py      # Módulo de Agendamentos
├── utils.py             # Utilitários compartilhados
├── pyproject.toml       # Configuração do projeto
├── README.md            # Este arquivo
└── .gitignore           # Arquivos ignorados pelo Git
```

---

## ▶️ Como Executar

### Pré-requisitos
- Python 3.11 ou superior

### Passos
```bash
# 1. Clone o repositório
git clone https://github.com/JIvanAV/SysPet.git
cd SysPet

# 2. Execute o sistema
python main.py
```

### Navegação
- Use **números** para selecionar opções nos menus
- Pressione **ENTER** para continuar nas pausas
- Digite **0** para voltar ao menu anterior ou sair

---

## 👥 Integrantes do Grupo

| Nome | RA | GitHub |
|------|-----|--------|
| José Ivan Abrantes Virgínio | [SEU RA] | [@JIvanAV](https://github.com/JIvanAV) |
| [Integrante 2] | [RA] | [GitHub] |
| [Integrante 3] | [RA] | [GitHub] |
| [Integrante 4] | [RA] | [GitHub] |
| [Integrante 5] | [RA] | [GitHub] |

> ⚠️ **Importante:** Segundo o edital, evidenciar os integrantes no cabeçalho do arquivo principal (`main.py`). Quem esquecer perde 1 ponto cada integrante da equipe.

---

## 📦 Entrega

- **Data limite:** 23/05/2026 (não será postergada)
- **Forma:** Arquivo compactado (`.zip`) ou link do repositório GitHub via Canvas
- **Critério:** Projeto rodando **sem erros**

---

## 📝 Licença

Projeto acadêmico — uso educacional.

---

**Desenvolvido com 🐶 para o PetShop Amigo Fiel**  
*FACISA - Sistemas de Informação - 2026.1*