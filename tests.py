# -*- coding: utf-8 -*-
"""
Testes Unitários - Serum Preset Organizer
==========================================
Execute com: python -m pytest tests.py -v
Ou simplesmente: python tests.py
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from categorizador import identificar_categoria, validar_extensao
from manipulador_arquivos import gerar_nome_unico, buscar_presets_recursivo, organizar_presets
from config import CATEGORIA_PADRAO


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


def test_gerar_nome_unico():
    """Testa geração de nomes únicos para duplicatas."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Cria arquivo original
        arquivo_original = temp_path / "preset.fxp"
        arquivo_original.touch()
        
        # Deve gerar nome único
        novo_caminho = gerar_nome_unico(arquivo_original)
        assert novo_caminho.name == "preset_1.fxp"
        
        # Cria o _1 e testa _2
        novo_caminho.touch()
        outro_caminho = gerar_nome_unico(arquivo_original)
        assert outro_caminho.name == "preset_2.fxp"
        
    print("✅ test_gerar_nome_unico passou")


def test_buscar_presets_recursivo():
    """Testa busca recursiva de presets."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Cria estrutura de pastas com presets
        (temp_path / "Pack1").mkdir()
        (temp_path / "Pack1" / "bass.fxp").touch()
        (temp_path / "Pack2" / "SubFolder").mkdir(parents=True)
        (temp_path / "Pack2" / "SubFolder" / "lead.serumpreset").touch()
        (temp_path / "outro.txt").touch()  # Não deve ser encontrado
        
        # Busca presets
        presets = list(buscar_presets_recursivo(temp_dir))
        
        assert len(presets) == 2
        nomes = [p.name for p in presets]
        assert "bass.fxp" in nomes
        assert "lead.serumpreset" in nomes
        assert "outro.txt" not in nomes
        
    print("✅ test_buscar_presets_recursivo passou")


def test_organizar_presets_completo():
    """Testa o fluxo completo de organização."""
    with tempfile.TemporaryDirectory() as origem:
        with tempfile.TemporaryDirectory() as destino:
            origem_path = Path(origem)
            destino_path = Path(destino)
            
            # Cria presets de teste
            (origem_path / "Deep_Bass_01.fxp").touch()
            (origem_path / "Epic_Lead.fxp").touch()
            (origem_path / "Lush_Pad.serumpreset").touch()
            (origem_path / "Unknown_Sound.fxp").touch()
            
            # Organiza
            stats = organizar_presets(origem, destino)
            
            # Verifica estatísticas
            assert stats["total_processados"] == 4
            assert stats["por_categoria"]["Bass"] == 1
            assert stats["por_categoria"]["Lead"] == 1
            assert stats["por_categoria"]["Pad"] == 1
            assert stats["por_categoria"]["Uncategorized"] == 1
            
            # Verifica estrutura de pastas
            assert (destino_path / "Bass" / "Deep_Bass_01.fxp").exists()
            assert (destino_path / "Lead" / "Epic_Lead.fxp").exists()
            assert (destino_path / "Pad" / "Lush_Pad.serumpreset").exists()
            assert (destino_path / "Uncategorized" / "Unknown_Sound.fxp").exists()
            
    print("✅ test_organizar_presets_completo passou")


def test_tratamento_duplicatas():
    """Testa que duplicatas são renomeadas corretamente."""
    with tempfile.TemporaryDirectory() as origem:
        with tempfile.TemporaryDirectory() as destino:
            origem_path = Path(origem)
            destino_path = Path(destino)
            
            # Cria presets com mesmo nome em subpastas diferentes
            (origem_path / "Pack1").mkdir()
            (origem_path / "Pack2").mkdir()
            (origem_path / "Pack1" / "Bass_Wobble.fxp").touch()
            (origem_path / "Pack2" / "Bass_Wobble.fxp").touch()  # Mesmo nome!
            
            # Organiza
            stats = organizar_presets(origem, destino)
            
            # Verifica que ambos foram copiados
            assert stats["total_processados"] == 2
            assert stats["total_duplicatas"] == 1  # Um foi renomeado
            
            # Verifica arquivos
            bass_folder = destino_path / "Bass"
            arquivos = list(bass_folder.glob("*.fxp"))
            assert len(arquivos) == 2
            nomes = [a.name for a in arquivos]
            assert "Bass_Wobble.fxp" in nomes
            assert "Bass_Wobble_1.fxp" in nomes
            
    print("✅ test_tratamento_duplicatas passou")


def executar_todos_testes():
    """Executa todos os testes."""
    print("\n" + "=" * 50)
    print("🧪 EXECUTANDO TESTES")
    print("=" * 50 + "\n")
    
    testes = [
        test_identificar_categoria_bass,
        test_identificar_categoria_lead,
        test_identificar_categoria_pad,
        test_identificar_categoria_case_insensitive,
        test_identificar_categoria_uncategorized,
        test_validar_extensao,
        test_gerar_nome_unico,
        test_buscar_presets_recursivo,
        test_organizar_presets_completo,
        test_tratamento_duplicatas,
    ]
    
    total = len(testes)
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
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {passou}/{total} testes passaram")
    if falhou == 0:
        print("🎉 Todos os testes passaram!")
    else:
        print(f"⚠️  {falhou} teste(s) falharam")
    print("=" * 50)


if __name__ == "__main__":
    executar_todos_testes()
