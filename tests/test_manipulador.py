# -*- coding: utf-8 -*-
"""
Testes do Módulo Manipulador de Arquivos - Serum Preset Organizer
==================================================================
Testes para as funções de busca, cópia e organização de arquivos.
"""

import sys
import os
import tempfile
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.manipulador_arquivos import (
    gerar_nome_unico, 
    buscar_presets_recursivo, 
    organizar_presets
)


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
            
            # Cria presets de teste com conteúdo único
            (origem_path / "Deep_Bass_01.fxp").write_bytes(b"bass1")
            (origem_path / "Epic_Lead.fxp").write_bytes(b"lead1")
            (origem_path / "Lush_Pad.serumpreset").write_bytes(b"pad1")
            (origem_path / "Unknown_Sound.fxp").write_bytes(b"unknown1")
            
            # Organiza
            stats = organizar_presets(origem, destino)
            
            # Verifica estatísticas
            assert stats["total_arquivos_origem"] == 4
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
    """Testa que duplicatas de conteúdo idêntico são ignoradas (não renomeadas)."""
    with tempfile.TemporaryDirectory() as origem:
        with tempfile.TemporaryDirectory() as destino:
            origem_path = Path(origem)
            destino_path = Path(destino)
            
            # Cria presets com mesmo nome em subpastas diferentes
            # Com conteúdo DIFERENTE para serem tratados como arquivos distintos
            (origem_path / "Pack1").mkdir()
            (origem_path / "Pack2").mkdir()
            
            # Escreve conteúdo diferente em cada arquivo
            (origem_path / "Pack1" / "Bass_Wobble.fxp").write_bytes(b"conteudo1")
            (origem_path / "Pack2" / "Bass_Wobble.fxp").write_bytes(b"conteudo2")
            
            # Organiza
            stats = organizar_presets(origem, destino)
            
            # Verifica que ambos foram copiados (conteúdo diferente = arquivos diferentes)
            assert stats["total_copias_realizadas"] == 2
            
            # Verifica arquivos
            bass_folder = destino_path / "Bass"
            arquivos = list(bass_folder.glob("*.fxp"))
            assert len(arquivos) == 2
            nomes = [a.name for a in arquivos]
            assert "Bass_Wobble.fxp" in nomes
            assert "Bass_Wobble_1.fxp" in nomes
            
    print("✅ test_tratamento_duplicatas passou")


def test_duplicatas_conteudo_identico():
    """Testa que duplicatas de conteúdo IDÊNTICO são ignoradas."""
    with tempfile.TemporaryDirectory() as origem:
        with tempfile.TemporaryDirectory() as destino:
            origem_path = Path(origem)
            destino_path = Path(destino)
            
            # Cria presets com conteúdo IDÊNTICO
            (origem_path / "Pack1").mkdir()
            (origem_path / "Pack2").mkdir()
            
            conteudo = b"mesmo conteudo binario"
            (origem_path / "Pack1" / "Bass_Sound.fxp").write_bytes(conteudo)
            (origem_path / "Pack2" / "Bass_Outro.fxp").write_bytes(conteudo)  # Mesmo conteúdo!
            
            # Organiza
            stats = organizar_presets(origem, destino)
            
            # Verifica que só um foi copiado (o outro é duplicata por hash)
            assert stats["total_copias_realizadas"] == 1
            assert stats["total_duplicatas_ignoradas"] == 1
            
            # Verifica que só existe um arquivo
            bass_folder = destino_path / "Bass"
            arquivos = list(bass_folder.glob("*.fxp"))
            assert len(arquivos) == 1
            
    print("✅ test_duplicatas_conteudo_identico passou")


def test_reverificacao_nao_deleta_sem_categoria():
    """
    TESTE CRÍTICO: Garante que re-verificação NÃO deleta arquivos sem categoria.
    
    Este teste previne o bug que causou perda de 378 arquivos.
    Quando rodamos re-verificação na pasta Uncategorized, arquivos que não têm
    categoria devem PERMANECER onde estão, não ser deletados.
    """
    with tempfile.TemporaryDirectory() as base_dir:
        base_path = Path(base_dir)
        
        # Simula estrutura após primeira organização
        # Destino = base_path (onde ficam as categorias)
        # Origem = base_path / Uncategorized (re-verificação)
        
        uncategorized = base_path / "Uncategorized"
        uncategorized.mkdir()
        
        # Cria arquivos na pasta Uncategorized (arquivos sem categoria)
        arquivo_sem_categoria = uncategorized / "Abstract_Sound.fxp"
        arquivo_sem_categoria.write_bytes(b"conteudo sem categoria")
        
        arquivo_com_categoria = uncategorized / "Deep_Bass.fxp"
        arquivo_com_categoria.write_bytes(b"conteudo bass")
        
        # Conta arquivos antes
        arquivos_antes = list(uncategorized.glob("*.fxp"))
        assert len(arquivos_antes) == 2
        
        # Roda re-verificação (origem=Uncategorized, destino=base)
        stats = organizar_presets(
            str(uncategorized),  # Origem: pasta Uncategorized
            str(base_path),      # Destino: pasta pai (estrutura de categorias)
            modo_mover=True      # Força modo mover (re-verificação)
        )
        
        # VERIFICAÇÃO CRÍTICA: O arquivo sem categoria DEVE continuar existindo!
        assert arquivo_sem_categoria.exists(), \
            "ERRO CRÍTICO: Arquivo sem categoria foi deletado!"
        
        # O arquivo com categoria (Bass) foi movido para pasta Bass
        assert (base_path / "Bass" / "Deep_Bass.fxp").exists(), \
            "Arquivo com categoria deveria ter sido movido para Bass"
        
        # Arquivo com categoria não deve mais estar em Uncategorized
        assert not arquivo_com_categoria.exists(), \
            "Arquivo com categoria deveria ter sido movido"
        
    print("✅ test_reverificacao_nao_deleta_sem_categoria passou")


def test_reverificacao_move_para_categoria_correta():
    """Testa que re-verificação move arquivos para categorias corretas."""
    with tempfile.TemporaryDirectory() as base_dir:
        base_path = Path(base_dir)
        
        uncategorized = base_path / "Uncategorized"
        uncategorized.mkdir()
        
        # Cria arquivos com categorias identificáveis
        (uncategorized / "Heavy_Bass_01.fxp").write_bytes(b"bass1")
        (uncategorized / "Bright_Lead_Solo.fxp").write_bytes(b"lead1")
        (uncategorized / "Warm_Pad.fxp").write_bytes(b"pad1")
        (uncategorized / "Random_Name.fxp").write_bytes(b"random")  # Sem categoria
        
        # Roda re-verificação
        stats = organizar_presets(
            str(uncategorized),
            str(base_path),
            modo_mover=True
        )
        
        # Verifica que arquivos foram para as categorias certas
        bass_path = base_path / "Bass" / "Heavy_Bass_01.fxp"
        lead_path = base_path / "Lead" / "Bright_Lead_Solo.fxp"
        pad_path = base_path / "Pad" / "Warm_Pad.fxp"
        
        # Debug: lista conteúdo das pastas
        lead_dir = base_path / "Lead"
        lead_contents = list(lead_dir.iterdir()) if lead_dir.exists() else []
        
        assert bass_path.exists(), \
            f"Bass nao existe. Pastas: {[p.name for p in base_path.iterdir() if p.is_dir()]}"
        assert lead_path.exists(), \
            f"Lead arquivo nao existe. Lead contents: {[f.name for f in lead_contents]}"
        assert pad_path.exists(), \
            f"Pad nao existe. Pastas: {[p.name for p in base_path.iterdir() if p.is_dir()]}"
        
        # Arquivo sem categoria PERMANECE em Uncategorized
        assert (uncategorized / "Random_Name.fxp").exists(), \
            f"Arquivo sem categoria deveria permanecer em Uncategorized! Uncategorized contents: {[f.name for f in uncategorized.iterdir()]}"
        
    print("✅ test_reverificacao_move_para_categoria_correta passou")


def test_nao_cria_duplicatas_em_reverificacao():
    """Testa que re-verificação não cria duplicatas de arquivos já categorizados."""
    with tempfile.TemporaryDirectory() as base_dir:
        base_path = Path(base_dir)
        
        # Cria estrutura com categoria já existente
        bass_folder = base_path / "Bass"
        bass_folder.mkdir()
        uncategorized = base_path / "Uncategorized"
        uncategorized.mkdir()
        
        # Arquivo já existe na categoria correta
        conteudo = b"mesmo arquivo"
        (bass_folder / "Deep_Bass.fxp").write_bytes(conteudo)
        
        # Mesmo arquivo está em Uncategorized (duplicata)
        (uncategorized / "Deep_Bass.fxp").write_bytes(conteudo)
        
        # Roda re-verificação
        stats = organizar_presets(
            str(uncategorized),
            str(base_path),
            modo_mover=True
        )
        
        # Não deve ter criado duplicata
        arquivos_bass = list(bass_folder.glob("*.fxp"))
        assert len(arquivos_bass) == 1, \
            f"Deveria ter só 1 arquivo em Bass, encontrou {len(arquivos_bass)}"
        
        # Arquivo duplicado foi removido de Uncategorized (ou contabilizado como duplicata)
        assert stats["total_duplicatas_ignoradas"] >= 1 or \
               stats.get("total_deletados_origem", 0) >= 1
        
    print("✅ test_nao_cria_duplicatas_em_reverificacao passou")


def test_multiplas_origens():
    """Testa organização de múltiplas pastas de origem."""
    from src.manipulador_arquivos import organizar_presets_multiplas_origens
    
    with tempfile.TemporaryDirectory() as destino:
        with tempfile.TemporaryDirectory() as origem1:
            with tempfile.TemporaryDirectory() as origem2:
                destino_path = Path(destino)
                origem1_path = Path(origem1)
                origem2_path = Path(origem2)
                
                # Cria presets na primeira origem
                (origem1_path / "Bass_Pack1.fxp").write_bytes(b"bass1")
                (origem1_path / "Lead_Pack1.fxp").write_bytes(b"lead1")
                
                # Cria presets na segunda origem
                (origem2_path / "Bass_Pack2.fxp").write_bytes(b"bass2")
                (origem2_path / "Pad_Pack2.fxp").write_bytes(b"pad2")
                
                # Cria duplicata de conteúdo entre as origens
                (origem2_path / "Bass_Duplicate.fxp").write_bytes(b"bass1")  # Mesmo conteúdo
                
                # Organiza de ambas origens
                stats = organizar_presets_multiplas_origens(
                    [origem1, origem2],
                    destino
                )
                
                # Verifica estatísticas consolidadas
                assert stats["total_arquivos_origem"] == 5, \
                    f"Esperava 5 arquivos, encontrou {stats['total_arquivos_origem']}"
                
                # A duplicata (bass1) deve ter sido ignorada
                assert stats["total_duplicatas_ignoradas"] >= 1, \
                    "Deveria ter detectado duplicata entre as origens"
                
                # Verifica arquivos criados
                assert (destino_path / "Bass" / "Bass_Pack1.fxp").exists()
                assert (destino_path / "Bass" / "Bass_Pack2.fxp").exists()
                assert (destino_path / "Lead" / "Lead_Pack1.fxp").exists()
                assert (destino_path / "Pad" / "Pad_Pack2.fxp").exists()
                
                # Verifica que 2 pastas foram processadas
                assert len(stats["pastas_processadas"]) == 2
                
    print("✅ test_multiplas_origens passou")


def executar_testes_manipulador():
    """Executa todos os testes do manipulador de arquivos."""
    print("\n📁 TESTES DO MANIPULADOR DE ARQUIVOS")
    print("─" * 40)
    
    testes = [
        test_gerar_nome_unico,
        test_buscar_presets_recursivo,
        test_organizar_presets_completo,
        test_tratamento_duplicatas,
        test_duplicatas_conteudo_identico,
        test_reverificacao_nao_deleta_sem_categoria,
        test_reverificacao_move_para_categoria_correta,
        test_nao_cria_duplicatas_em_reverificacao,
        test_multiplas_origens,
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
    passou, falhou = executar_testes_manipulador()
    print(f"\n📊 Resultado: {passou} passaram, {falhou} falharam")
