# -*- coding: utf-8 -*-
"""
Utilitário para listar todos os arquivos de uma pasta
======================================================
Gera um arquivo .txt com todos os nomes de arquivos encontrados.
Útil para testar e analisar quais arquivos precisam de tratamento.
"""

import os
from pathlib import Path
from datetime import datetime


def listar_arquivos_pasta(pasta: str, extensoes: list = None) -> list:
    """
    Lista todos os arquivos em uma pasta recursivamente.
    
    Args:
        pasta: Caminho da pasta
        extensoes: Lista de extensões para filtrar (ex: ['.fxp', '.serumpreset'])
                   Se None, lista todos os arquivos
    
    Returns:
        Lista de nomes de arquivos
    """
    arquivos = []
    pasta_path = Path(pasta)
    
    if not pasta_path.exists():
        print(f"❌ Pasta não encontrada: {pasta}")
        return []
    
    for arquivo in pasta_path.rglob('*'):
        if arquivo.is_file():
            if extensoes:
                if arquivo.suffix.lower() in [ext.lower() for ext in extensoes]:
                    arquivos.append(arquivo.name)
            else:
                arquivos.append(arquivo.name)
    
    return sorted(arquivos)


def salvar_lista(arquivos: list, pasta_origem: str, arquivo_saida: str = None):
    """
    Salva a lista de arquivos em um arquivo .txt
    
    Args:
        arquivos: Lista de nomes de arquivos
        pasta_origem: Pasta que foi escaneada (para referência)
        arquivo_saida: Nome do arquivo de saída (opcional)
    """
    if arquivo_saida is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_saida = f"lista_arquivos_{timestamp}.txt"
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(f"# Lista de arquivos\n")
        f.write(f"# Pasta: {pasta_origem}\n")
        f.write(f"# Total: {len(arquivos)} arquivos\n")
        f.write(f"# Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"# {'=' * 60}\n\n")
        
        for arquivo in arquivos:
            f.write(f"{arquivo}\n")
    
    return arquivo_saida


def main():
    print("\n" + "=" * 60)
    print("  📋 LISTADOR DE ARQUIVOS")
    print("=" * 60)
    
    # Solicita pasta
    print("\n  Digite o caminho da pasta:")
    pasta = input("  > ").strip().strip('"').strip("'")
    
    if not pasta:
        print("  ❌ Caminho não pode estar vazio.")
        return
    
    # Pergunta se quer filtrar por extensão
    print("\n  Filtrar por extensões de preset? (.fxp, .serumpreset)")
    print("  [S] Sim - apenas presets")
    print("  [N] Não - todos os arquivos")
    filtrar = input("  > ").strip().lower()
    
    extensoes = None
    if filtrar in ['s', 'sim', 'y', 'yes']:
        extensoes = ['.fxp', '.serumpreset']
        print("  ✅ Filtrando apenas arquivos .fxp e .serumpreset")
    else:
        print("  ✅ Listando todos os arquivos")
    
    # Lista arquivos
    print(f"\n  🔍 Escaneando pasta...")
    arquivos = listar_arquivos_pasta(pasta, extensoes)
    
    if not arquivos:
        print("  ⚠️ Nenhum arquivo encontrado!")
        return
    
    print(f"  ✅ Encontrados {len(arquivos)} arquivos")
    
    # Salva em arquivo
    arquivo_saida = salvar_lista(arquivos, pasta)
    caminho_completo = os.path.abspath(arquivo_saida)
    
    print(f"\n  📄 Lista salva em: {caminho_completo}")
    
    # Mostra prévia
    print(f"\n  📋 Prévia (primeiros 20 arquivos):")
    print("  " + "-" * 50)
    for i, arquivo in enumerate(arquivos[:20], 1):
        print(f"  {i:3}. {arquivo}")
    
    if len(arquivos) > 20:
        print(f"  ... e mais {len(arquivos) - 20} arquivos")
    
    print("\n  ✅ Concluído!\n")


if __name__ == "__main__":
    main()
