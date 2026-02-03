#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Executor de Testes - Serum Preset Organizer
=============================================
Execute este arquivo para rodar todos os testes do projeto.

USO:
    python run_tests.py
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.test_categorizador import executar_testes_categorizador
from tests.test_manipulador import executar_testes_manipulador


def main():
    """Executa todos os testes e exibe o resultado consolidado."""
    
    print("\n" + "=" * 60)
    print("🧪 SERUM PRESET ORGANIZER - SUITE DE TESTES")
    print("=" * 60)
    
    total_passou = 0
    total_falhou = 0
    
    # Testes do categorizador
    passou, falhou = executar_testes_categorizador()
    total_passou += passou
    total_falhou += falhou
    
    # Testes do manipulador
    passou, falhou = executar_testes_manipulador()
    total_passou += passou
    total_falhou += falhou
    
    # Resultado final
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO FINAL: {total_passou}/{total_passou + total_falhou} testes passaram")
    
    if total_falhou == 0:
        print("🎉 Todos os testes passaram!")
        exit_code = 0
    else:
        print(f"⚠️  {total_falhou} teste(s) falharam")
        exit_code = 1
    
    print("=" * 60 + "\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
