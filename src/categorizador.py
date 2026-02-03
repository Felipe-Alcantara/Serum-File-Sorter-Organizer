# -*- coding: utf-8 -*-
"""
Módulo de Categorização - Serum Preset Organizer
=================================================
Contém a lógica de identificação de categoria baseada no nome do arquivo.
"""

from pathlib import Path

from src.config import MAPA_CATEGORIAS, CATEGORIA_PADRAO


def identificar_categoria(nome_arquivo: str) -> str:
    """
    Identifica a categoria de um preset baseado no nome do arquivo.
    
    A busca é case-insensitive e procura keywords em qualquer parte do nome.
    Retorna a primeira categoria encontrada ou CATEGORIA_PADRAO se nenhuma match.
    
    Args:
        nome_arquivo: Nome do arquivo de preset (com ou sem extensão)
        
    Returns:
        Nome da categoria identificada
    """
    # Remove a extensão para evitar falsos positivos (ex: .fxp contém "fx")
    nome_sem_extensao = Path(nome_arquivo).stem
    
    # Converte para minúsculas para busca case-insensitive
    nome_lower = nome_sem_extensao.lower()
    
    # Itera sobre cada categoria e suas keywords
    for categoria, lista_keywords in MAPA_CATEGORIAS.items():
        for keyword in lista_keywords:
            # Verifica se a keyword está em qualquer parte do nome
            if keyword.lower() in nome_lower:
                return categoria
    
    # Nenhuma keyword encontrada
    return CATEGORIA_PADRAO


def obter_todas_categorias() -> list:
    """
    Retorna uma lista com todas as categorias disponíveis, incluindo Uncategorized.
    
    Returns:
        Lista de nomes de categorias
    """
    categorias = list(MAPA_CATEGORIAS.keys())
    categorias.append(CATEGORIA_PADRAO)
    return categorias


def validar_extensao(nome_arquivo: str, extensoes_validas: list) -> bool:
    """
    Verifica se o arquivo possui uma das extensões válidas.
    
    Args:
        nome_arquivo: Nome do arquivo a verificar
        extensoes_validas: Lista de extensões aceitas (com ponto, ex: ['.fxp'])
        
    Returns:
        True se a extensão é válida, False caso contrário
    """
    nome_lower = nome_arquivo.lower()
    return any(nome_lower.endswith(ext.lower()) for ext in extensoes_validas)
