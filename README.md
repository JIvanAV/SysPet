# SysPet - Sistema de Gestão para PetShops

O **SysPet** é um sistema CLI (interface por linha de comando) desenvolvido para simplificar a rotina de um petshop. O projeto surgiu na faculdade como uma forma de aplicar os conceitos de programação estruturada em Python, focando em manter a organização entre tutores, seus pets e o histórico de atendimentos.

> **Status:** Em evolução (fase acadêmica).

## 💡 Por que este projeto?
Gerenciar o dia a dia de um petshop pode ser caótico com papéis. O SysPet resolve isso centralizando as informações fundamentais em módulos simples e leves, rodando direto no terminal.

## 🛠 Funcionalidades
*   **Gestão de Tutores:** Cadastro, edição e remoção de clientes.
*   **Controle de Pets:** Registro dos pacientes com associações aos tutores.
*   **Veterinários:** Organização dos profissionais da clínica.
*   **Agenda:** Marcação de atendimentos para evitar filas.

## 🚀 Como rodar na sua máquina

Certifique-se de ter o [Python](https://python.org) instalado (versão 3.8+).

```bash
# Clone o repositório
git clone https://github.com/JIvanAV/SysPet.git

# Entre na pasta
cd SysPet

# Inicie o sistema
python main.py
```

## 📂 Arquitetura (Por trás dos panos)
O projeto é modularizado para ser fácil de manter:
- `main.py`: O "cérebro" do sistema, cuida de toda a navegação dos menus.
- `clientes.py` / `pets.py`: Módulos de dados dedicados a cada entidade.
- `utils.py`: Auxilia nas validações e limpezas de tela.

## 🤝 Contribuições
Este projeto é focado em estudos, mas sugestões de melhoria na estrutura ou validações são sempre bem-vindas! Se quiser propor algo, abra uma *Issue* ou mande um *Pull Request*.

---
*Desenvolvido por José Ivan Abrantes Virgínio (JIvanAV).*
