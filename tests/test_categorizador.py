# -*- coding: utf-8 -*-
"""
Testes do Módulo Categorizador - Serum Preset Organizer
========================================================
Testes para as funções de identificação de categoria e validação de extensões.
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.categorizador import identificar_categoria, validar_extensao
from src.config import CATEGORIA_PADRAO


def test_identificar_categoria_bass():
    """Testa identificação de presets de Bass."""
    assert identificar_categoria("TSP_S2PH_Bass_alum.fxp") == "Bass"
    assert identificar_categoria("808_Hard.fxp") == "Bass"
    assert identificar_categoria("Deep_Sub_Wobble.fxp") == "Bass"
    assert identificar_categoria("GROWL_Monster.serumpreset") == "Bass"
    print("✅ test_identificar_categoria_bass passou")


def test_identificar_categoria_lead():
    """Testa identificação de presets de Lead."""
    assert identificar_categoria("Epic_Lead_01.fxp") == "Lead"
    assert identificar_categoria("LD_Screamer.fxp") == "Lead"
    assert identificar_categoria("Main_Melody.serumpreset") == "Lead"
    print("✅ test_identificar_categoria_lead passou")


def test_identificar_categoria_pad():
    """Testa identificação de presets de Pad."""
    assert identificar_categoria("Lush_Pad_Soft.fxp") == "Pad"
    assert identificar_categoria("Atmosphere_Dark.fxp") == "Pad"
    assert identificar_categoria("PD_Dreamy.serumpreset") == "Pad"
    print("✅ test_identificar_categoria_pad passou")


def test_identificar_categoria_case_insensitive():
    """Testa que a busca é case-insensitive."""
    assert identificar_categoria("BASS_LOUD.fxp") == "Bass"
    assert identificar_categoria("bass_quiet.fxp") == "Bass"
    assert identificar_categoria("BaSs_MiXeD.fxp") == "Bass"
    print("✅ test_identificar_categoria_case_insensitive passou")


def test_identificar_categoria_uncategorized():
    """Testa que arquivos sem keywords vão para Uncategorized."""
    assert identificar_categoria("Random_Name_123.fxp") == CATEGORIA_PADRAO
    assert identificar_categoria("XYZ_ABC.serumpreset") == CATEGORIA_PADRAO
    print("✅ test_identificar_categoria_uncategorized passou")


def test_validar_extensao():
    """Testa validação de extensões de arquivo."""
    extensoes = ['.fxp', '.serumpreset']
    assert validar_extensao("preset.fxp", extensoes) == True
    assert validar_extensao("preset.SerumPreset", extensoes) == True
    assert validar_extensao("preset.SERUMPRESET", extensoes) == True
    assert validar_extensao("preset.wav", extensoes) == False
    assert validar_extensao("preset.txt", extensoes) == False
    print("✅ test_validar_extensao passou")


def executar_testes_categorizador():
    """Executa todos os testes do categorizador."""
    print("\n📂 TESTES DO CATEGORIZADOR")
    print("─" * 40)
    
    testes = [
        test_identificar_categoria_bass,
        test_identificar_categoria_lead,
        test_identificar_categoria_pad,
        test_identificar_categoria_case_insensitive,
        test_identificar_categoria_uncategorized,
        test_validar_extensao,
    ]
    
    passou = 0
    falhou = 0
    
    for teste in testes:
        try:
            teste()
            passou += 1
        except AssertionError as e:
            print(f"❌ {teste.__name__} FALHOU: {e}")
            falhou += 1
        except Exception as e:
            print(f"❌ {teste.__name__} ERRO: {e}")
            falhou += 1
    
    return passou, falhou


if __name__ == "__main__":
    passou, falhou = executar_testes_categorizador()
    print(f"\n📊 Resultado: {passou} passaram, {falhou} falharam")
