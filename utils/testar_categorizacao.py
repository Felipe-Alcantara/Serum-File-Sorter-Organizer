# -*- coding: utf-8 -*-
"""
Utilitário para testar categorização de arquivos
=================================================
Lê uma lista de arquivos e mostra como seriam categorizados.
"""

import sys
import os

# Adiciona diretório pai ao path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.categorizador import identificar_categorias
from src.config import CATEGORIA_PADRAO


def testar_lista_arquivos(caminho_lista: str):
    """
    Testa a categorização de uma lista de arquivos.
    
    Args:
        caminho_lista: Caminho do arquivo .txt com a lista
    """
    if not os.path.exists(caminho_lista):
        print(f"❌ Arquivo não encontrado: {caminho_lista}")
        return
    
    # Lê os arquivos
    with open(caminho_lista, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Filtra apenas nomes de arquivo (ignora comentários e linhas vazias)
    arquivos = [l.strip() for l in linhas if l.strip() and not l.startswith('#')]
    
    print(f"\n{'='*70}")
    print(f"  📋 TESTE DE CATEGORIZAÇÃO")
    print(f"  Total de arquivos: {len(arquivos)}")
    print(f"{'='*70}\n")
    
    # Categoriza cada arquivo
    categorizados = {}
    uncategorized = []
    multi_categoria = []
    
    for arquivo in arquivos:
        cats = identificar_categorias(arquivo)
        
        if not cats:
            uncategorized.append(arquivo)
        else:
            if len(cats) > 1:
                multi_categoria.append((arquivo, cats))
            
            for cat in cats:
                if cat not in categorizados:
                    categorizados[cat] = []
                categorizados[cat].append(arquivo)
    
    # Mostra resultados por categoria
    print("📊 DISTRIBUIÇÃO POR CATEGORIA:")
    print("-" * 50)
    
    for cat in sorted(categorizados.keys(), key=lambda x: -len(categorizados[x])):
        print(f"  {cat:20} {len(categorizados[cat]):5} arquivos")
    
    print(f"\n  {'Uncategorized':20} {len(uncategorized):5} arquivos")
    
    # Estatísticas
    total_cat = len(arquivos) - len(uncategorized)
    pct = (total_cat / len(arquivos) * 100) if arquivos else 0
    
    print(f"\n{'='*50}")
    print(f"  ✅ Categorizados: {total_cat} ({pct:.1f}%)")
    print(f"  ❌ Não categorizados: {len(uncategorized)} ({100-pct:.1f}%)")
    print(f"  🔀 Multi-categoria: {len(multi_categoria)}")
    print(f"{'='*50}")
    
    # Mostra Uncategorized
    if uncategorized:
        print(f"\n📋 ARQUIVOS NÃO CATEGORIZADOS ({len(uncategorized)}):")
        print("-" * 50)
        for i, arq in enumerate(uncategorized[:50], 1):
            print(f"  {i:3}. {arq}")
        if len(uncategorized) > 50:
            print(f"  ... e mais {len(uncategorized) - 50}")
    
    # Mostra multi-categoria (amostra)
    if multi_categoria:
        print(f"\n🔀 ARQUIVOS MULTI-CATEGORIA (amostra):")
        print("-" * 50)
        for arq, cats in multi_categoria[:15]:
            cats_str = ", ".join(cats)
            nome = arq if len(arq) <= 40 else arq[:37] + "..."
            print(f"  {nome:42} → {cats_str}")
        if len(multi_categoria) > 15:
            print(f"  ... e mais {len(multi_categoria) - 15}")
    
    # Salva uncategorized em arquivo
    if uncategorized:
        arquivo_saida = caminho_lista.replace('.txt', '_uncategorized.txt')
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(f"# Arquivos não categorizados\n")
            f.write(f"# Total: {len(uncategorized)}\n\n")
            for arq in uncategorized:
                f.write(f"{arq}\n")
        print(f"\n💾 Lista de não categorizados salva em: {arquivo_saida}")


def main():
    print("\n" + "=" * 60)
    print("  🧪 TESTADOR DE CATEGORIZAÇÃO")
    print("=" * 60)
    
    # Procura arquivos .txt no diretório
    arquivos_txt = [f for f in os.listdir('.') if f.startswith('lista_arquivos_') and f.endswith('.txt')]
    
    if arquivos_txt:
        print("\n  Arquivos de lista encontrados:")
        for i, arq in enumerate(arquivos_txt, 1):
            print(f"  [{i}] {arq}")
        print(f"  [0] Digitar caminho manualmente")
        
        escolha = input("\n  Escolha: ").strip()
        
        if escolha == '0' or not escolha.isdigit():
            caminho = input("  Caminho do arquivo .txt: ").strip().strip('"')
        else:
            idx = int(escolha) - 1
            if 0 <= idx < len(arquivos_txt):
                caminho = arquivos_txt[idx]
            else:
                print("  ❌ Opção inválida")
                return
    else:
        caminho = input("  Caminho do arquivo .txt com a lista: ").strip().strip('"')
    
    testar_lista_arquivos(caminho)


if __name__ == "__main__":
    main()
