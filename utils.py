#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários Compartilhados - SysPet
Funções auxiliares reutilizáveis em todo o projeto.
"""

import os
import sys
import re
from typing import Optional


def limpar_tela() -> None:
    """Limpa a tela do terminal (Windows/Linux/macOS)."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar(mensagem: str = "\nPressione ENTER para continuar...") -> None:
    """Pausa a execução aguardando o usuário pressionar ENTER."""
    try:
        input(mensagem)
    except (EOFError, KeyboardInterrupt):
        pass


def confirmar(mensagem: str = "Confirmar? (s/n): ") -> bool:
    """Solicita confirmação do usuário (sim/não)."""
    while True:
        try:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "sim", "y", "yes"):
                return True
            if resposta in ("n", "nao", "não", "no"):
                return False
            print("⚠️  Responda 's' para sim ou 'n' para não.")
        except (EOFError, KeyboardInterrupt):
            return False


def validar_email(email: str) -> bool:
    """Valida formato básico de e-mail."""
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email))


def validar_telefone(telefone: str) -> bool:
    """Valida formato de telefone brasileiro: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX."""
    # Remove espaços e caracteres extras para validação
    telefone_limpo = re.sub(r"[\s\-\(\)]", "", telefone)
    # Padrão: 2 dígitos DDD + 8 ou 9 dígitos
    padrao = r"^\d{10,11}$"
    return bool(re.match(padrao, telefone_limpo))


def validar_cpf(cpf: str) -> bool:
    """Valida CPF (formato básico com 11 dígitos)."""
    cpf_limpo = re.sub(r"[\.\-]", "", cpf)
    return bool(re.match(r"^\d{11}$", cpf_limpo))


def obter_int(mensagem: str = "Digite um número: ") -> int:
    """Obtém um inteiro do usuário com validação."""
    while True:
        try:
            valor = input(mensagem).strip()
            if not valor:
                raise ValueError("Entrada vazia")
            return int(valor)
        except ValueError:
            print("❌ Valor inválido. Digite um número inteiro.")


def obter_float(mensagem: str = "Digite um valor: ") -> float:
    """Obtém um float do usuário com validação."""
    while True:
        try:
            valor = input(mensagem).strip()
            if not valor:
                raise ValueError("Entrada vazia")
            # Aceita vírgula como separador decimal
            valor = valor.replace(",", ".")
            return float(valor)
        except ValueError:
            print("❌ Valor inválido. Digite um número (ex: 10.50 ou 10,50).")


def obter_str_obrigatorio(mensagem: str) -> str:
    """Obtém uma string não vazia do usuário."""
    while True:
        try:
            valor = input(mensagem).strip()
            if valor:
                return valor
            print("⚠️  Este campo é obrigatório.")
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Operação cancelada.")
            raise


def obter_str_opcional(mensagem: str, padrao: str = "") -> str:
    """Obtém uma string opcional do usuário (retorna padrão se vazio)."""
    try:
        valor = input(mensagem).strip()
        return valor if valor else padrao
    except (EOFError, KeyboardInterrupt):
        return padrao


def formatar_moeda(valor: float) -> str:
    """Formata valor float como moeda brasileira (R$)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def truncar_texto(texto: str, max_len: int) -> str:
    """Trunca texto adicionando '..' se exceder tamanho máximo."""
    if len(texto) <= max_len:
        return texto
    return texto[: max_len - 2] + ".."