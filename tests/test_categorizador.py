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

from src.categorizador import identificar_categoria, identificar_categorias, validar_extensao
from src.config import CATEGORIA_PADRAO


def test_identificar_categoria_bass():
    """Testa identificação de presets de Bass."""
    assert "Bass" in identificar_categorias("TSP_S2PH_Bass_alum.fxp")
    assert "Bass" in identificar_categorias("808_Hard.fxp")
    assert "Bass" in identificar_categorias("Deep_Sub_Wobble.fxp")
    assert "Bass" in identificar_categorias("GROWL_Monster.serumpreset")
    print("✅ test_identificar_categoria_bass passou")


def test_identificar_categoria_lead():
    """Testa identificação de presets de Lead."""
    assert "Lead" in identificar_categorias("Epic_Lead_01.fxp")
    assert "Lead" in identificar_categorias("LD_Screamer.fxp")
    assert "Lead" in identificar_categorias("Main_Melody.serumpreset")
    print("✅ test_identificar_categoria_lead passou")


def test_identificar_categoria_pad():
    """Testa identificação de presets de Pad."""
    assert "Pad" in identificar_categorias("Lush_Pad_Soft.fxp")
    assert "Pad" in identificar_categorias("Atmosphere_Dark.fxp")
    assert "Pad" in identificar_categorias("PD_Dreamy.serumpreset")
    print("✅ test_identificar_categoria_pad passou")


def test_identificar_categoria_case_insensitive():
    """Testa que a busca é case-insensitive."""
    assert "Bass" in identificar_categorias("BASS_LOUD.fxp")
    assert "Bass" in identificar_categorias("bass_quiet.fxp")
    assert "Bass" in identificar_categorias("BaSs_MiXeD.fxp")
    print("✅ test_identificar_categoria_case_insensitive passou")


def test_identificar_categoria_uncategorized():
    """Testa que arquivos sem keywords vão para Uncategorized."""
    result = identificar_categorias("Random_Name_123.fxp")
    assert len(result) == 0  # identificar_categorias retorna lista vazia, main.py adiciona Uncategorized
    result = identificar_categorias("XYZ_ABC.serumpreset")
    assert len(result) == 0
    print("✅ test_identificar_categoria_uncategorized passou")


def test_genero_future_bass_nao_afeta():
    """Testa que 'Future Bass' como gênero NÃO marca como Bass."""
    # Arquivo claramente LEAD com gênero "Future Bass"
    cats = identificar_categorias("Future Bass - LEAD 13.fxp")
    assert "Lead" in cats, f"Esperado 'Lead' em {cats}"
    assert "Bass" not in cats, f"'Bass' não deveria estar em {cats} - falso positivo por 'Future Bass'"
    
    # Arquivo claramente Keys com gênero "Future Bass"
    cats = identificar_categorias("Future Bass - KEYS - Analog Movement.fxp")
    # "Keys" pode virar "Piano_Keys" dependendo das keywords
    assert "Piano_Keys" in cats or "Synth" in cats, f"Esperado 'Piano_Keys' ou 'Synth' em {cats}"
    assert "Bass" not in cats, f"'Bass' não deveria estar em {cats}"
    
    print("✅ test_genero_future_bass_nao_afeta passou")


def test_genero_drum_and_bass_nao_afeta():
    """Testa que 'Drum and Bass' ou 'DnB' como gênero NÃO marca como Bass ou Drum."""
    cats = identificar_categorias("DnB - LEAD Heavy.fxp")
    assert "Lead" in cats, f"Esperado 'Lead' em {cats}"
    assert "Bass" not in cats, f"'Bass' não deveria estar em {cats}"
    
    cats = identificar_categorias("Drum and Bass - PAD Atmospheric.fxp")
    assert "Pad" in cats, f"Esperado 'Pad' em {cats}"
    assert "Bass" not in cats, f"'Bass' não deveria estar em {cats}"
    
    print("✅ test_genero_drum_and_bass_nao_afeta passou")


def test_multi_categoria():
    """Testa que arquivos com múltiplas keywords retornam múltiplas categorias."""
    # Arquivo que menciona Bass E Lead
    cats = identificar_categorias("Bass_Lead_Hybrid.fxp")
    assert "Bass" in cats, f"Esperado 'Bass' em {cats}"
    assert "Lead" in cats, f"Esperado 'Lead' em {cats}"
    
    print("✅ test_multi_categoria passou")


def test_extensao_fxp_nao_afeta_fx():
    """Testa que a extensão .fxp NÃO causa falso positivo para FX."""
    # Arquivo Bass com extensão .fxp
    cats = identificar_categorias("Pure_Bass_Sound.fxp")
    assert "FX" not in cats, f"'FX' não deveria estar em {cats} - falso positivo pela extensão .fxp"
    assert "Bass" in cats, f"Esperado 'Bass' em {cats}"
    
    print("✅ test_extensao_fxp_nao_afeta_fx passou")


def test_validar_extensao():
    """Testa validação de extensões de arquivo."""
    extensoes = ['.fxp', '.serumpreset']
    assert validar_extensao("preset.fxp", extensoes) == True
    assert validar_extensao("preset.SerumPreset", extensoes) == True
    assert validar_extensao("preset.SERUMPRESET", extensoes) == True
    assert validar_extensao("preset.wav", extensoes) == False
    assert validar_extensao("preset.txt", extensoes) == False
    print("✅ test_validar_extensao passou")


def test_compatibilidade_identificar_categoria():
    """Testa que a função antiga ainda funciona (compatibilidade)."""
    # Deve retornar a primeira categoria ou Uncategorized
    result = identificar_categoria("Bass_Lead_Hybrid.fxp")
    assert result in ["Bass", "Lead"]  # Depende da ordem
    
    result = identificar_categoria("Random_Name.fxp")
    assert result == CATEGORIA_PADRAO
    
    print("✅ test_compatibilidade_identificar_categoria passou")


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
        test_genero_future_bass_nao_afeta,
        test_genero_drum_and_bass_nao_afeta,
        test_multi_categoria,
        test_extensao_fxp_nao_afeta_fx,
        test_validar_extensao,
        test_compatibilidade_identificar_categoria,
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
