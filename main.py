# -*- coding: utf-8 -*-
"""
Serum Preset Organizer - Script Principal
==========================================
Organiza automaticamente sua biblioteca de presets do Serum,
categorizando por tipo de instrumento baseado no nome do arquivo.

Autor: Serum File Sorter Organizer
Versão: 1.0.0

USO:
    python main.py
    
    O script solicitará os caminhos de origem e destino via terminal.
    Ou edite as variáveis PASTA_ORIGEM e PASTA_DESTINO abaixo.
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Adiciona o diretório atual ao path para importar módulos locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manipulador_arquivos import organizar_presets
from categorizador import obter_todas_categorias
from config import EXTENSOES_SUPORTADAS, MAPA_CATEGORIAS


# ============================================================================
# CONFIGURAÇÃO - Edite aqui ou deixe vazio para input via terminal
# ============================================================================
PASTA_ORIGEM = ""   # Ex: "C:/Users/SeuNome/Downloads/Serum Presets"
PASTA_DESTINO = ""  # Ex: "C:/Users/SeuNome/Documents/Serum Organized"
# ============================================================================


def exibir_banner():
    """Exibe o banner inicial do programa."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                  SERUM PRESET ORGANIZER                       ║
    ║              Organize sua biblioteca de presets               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def exibir_categorias_disponiveis():
    """Exibe as categorias e keywords configuradas."""
    print("\n📂 Categorias disponíveis:")
    print("-" * 50)
    for categoria, keywords in MAPA_CATEGORIAS.items():
        # Mostra apenas as 5 primeiras keywords como exemplo
        keywords_preview = ", ".join(keywords[:5])
        if len(keywords) > 5:
            keywords_preview += f", ... (+{len(keywords) - 5})"
        print(f"  • {categoria}: {keywords_preview}")
    print(f"  • Uncategorized: (arquivos não classificados)")
    print("-" * 50)


def solicitar_caminho(mensagem: str, deve_existir: bool = True) -> str:
    """
    Solicita um caminho ao usuário via terminal.
    
    Args:
        mensagem: Mensagem a exibir
        deve_existir: Se True, valida que o caminho existe
        
    Returns:
        Caminho validado
    """
    while True:
        caminho = input(mensagem).strip()
        
        # Remove aspas se o usuário colar caminho com aspas
        caminho = caminho.strip('"').strip("'")
        
        if not caminho:
            print("❌ Caminho não pode estar vazio. Tente novamente.")
            continue
        
        # Expande ~ para pasta do usuário se usado
        caminho = os.path.expanduser(caminho)
        
        if deve_existir:
            if not os.path.exists(caminho):
                print(f"❌ Caminho não encontrado: {caminho}")
                continue
            if not os.path.isdir(caminho):
                print(f"❌ O caminho não é uma pasta: {caminho}")
                continue
        
        return caminho


def confirmar_operacao(pasta_origem: str, pasta_destino: str) -> bool:
    """
    Solicita confirmação do usuário antes de iniciar.
    
    Args:
        pasta_origem: Caminho da origem
        pasta_destino: Caminho do destino
        
    Returns:
        True se confirmado, False caso contrário
    """
    print("\n" + "=" * 60)
    print("📋 RESUMO DA OPERAÇÃO")
    print("=" * 60)
    print(f"  📁 Origem:  {pasta_origem}")
    print(f"  📁 Destino: {pasta_destino}")
    print(f"  📄 Extensões: {', '.join(EXTENSOES_SUPORTADAS)}")
    print("=" * 60)
    print("\n⚠️  ATENÇÃO: Os arquivos serão COPIADOS (não movidos).")
    print("    Seus arquivos originais permanecerão intactos.\n")
    
    resposta = input("Deseja continuar? (s/n): ").strip().lower()
    return resposta in ['s', 'sim', 'y', 'yes']


def exibir_resultados(estatisticas: dict, tempo_execucao: float):
    """
    Exibe o relatório final da operação.
    
    Args:
        estatisticas: Dicionário com estatísticas da operação
        tempo_execucao: Tempo total em segundos
    """
    print("\n" + "=" * 60)
    print("✅ OPERAÇÃO CONCLUÍDA")
    print("=" * 60)
    print(f"  ⏱️  Tempo de execução: {tempo_execucao:.2f} segundos")
    print(f"  📄 Total de presets processados: {estatisticas['total_processados']}")
    print(f"  🔄 Duplicatas renomeadas: {estatisticas['total_duplicatas']}")
    
    if estatisticas['por_categoria']:
        print("\n  📊 Presets por categoria:")
        # Ordena por quantidade (decrescente)
        categorias_ordenadas = sorted(
            estatisticas['por_categoria'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        for categoria, quantidade in categorias_ordenadas:
            barra = "█" * min(quantidade // 5, 20)  # Barra proporcional
            print(f"      {categoria:20} {quantidade:5} {barra}")
    
    if estatisticas['erros']:
        print(f"\n  ⚠️  Erros encontrados: {len(estatisticas['erros'])}")
        for erro in estatisticas['erros'][:5]:  # Mostra até 5 erros
            print(f"      • {erro['arquivo']}: {erro['erro']}")
        if len(estatisticas['erros']) > 5:
            print(f"      ... e mais {len(estatisticas['erros']) - 5} erros")
    
    print("=" * 60)


def main():
    """Função principal do programa."""
    exibir_banner()
    
    # Determina os caminhos (variáveis ou input)
    if PASTA_ORIGEM and PASTA_DESTINO:
        pasta_origem = PASTA_ORIGEM
        pasta_destino = PASTA_DESTINO
        print("📌 Usando caminhos configurados no código.")
    else:
        exibir_categorias_disponiveis()
        print("\n")
        pasta_origem = solicitar_caminho(
            "📂 Digite o caminho da pasta de ORIGEM (onde estão os presets):\n> "
        )
        pasta_destino = solicitar_caminho(
            "\n📂 Digite o caminho da pasta de DESTINO (onde serão organizados):\n> ",
            deve_existir=False  # Será criada se não existir
        )
    
    # Confirmação do usuário
    if not confirmar_operacao(pasta_origem, pasta_destino):
        print("\n❌ Operação cancelada pelo usuário.")
        return
    
    # Executa a organização
    print("\n🔄 Processando presets...")
    print("   (Isso pode demorar dependendo da quantidade de arquivos)\n")
    
    inicio = datetime.now()
    
    try:
        estatisticas = organizar_presets(pasta_origem, pasta_destino)
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        return
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return
    
    fim = datetime.now()
    tempo_execucao = (fim - inicio).total_seconds()
    
    # Exibe resultados
    exibir_resultados(estatisticas, tempo_execucao)
    
    # Mensagem final
    if estatisticas['total_processados'] > 0:
        print(f"\n🎉 Seus presets foram organizados em: {pasta_destino}")
    else:
        print("\n⚠️  Nenhum preset foi encontrado na pasta de origem.")
        print("   Verifique se o caminho está correto e se há arquivos .fxp ou .SerumPreset")


if __name__ == "__main__":
    main()
