# -*- coding: utf-8 -*-
"""
Módulo de Categorização - Serum Preset Organizer
=================================================
Contém a lógica de identificação de categoria baseada no nome do arquivo.
"""

import re
from pathlib import Path
from typing import List, Set

from src.config import (
    MAPA_CATEGORIAS, 
    CATEGORIA_PADRAO, 
    TERMOS_GENERO_IGNORAR,
    KEYWORDS_CURTAS
)


def limpar_nome_para_analise(nome_arquivo: str) -> str:
    """
    Limpa o nome do arquivo removendo termos de gênero que causam falsos positivos.
    
    Por exemplo: "Future Bass LEAD 01.fxp" -> "LEAD 01" (remove "Future Bass")
    
    Args:
        nome_arquivo: Nome do arquivo original
        
    Returns:
        Nome limpo para análise
    """
    # Remove a extensão
    nome = Path(nome_arquivo).stem
    nome_lower = nome.lower()
    
    # Remove termos de gênero que podem confundir
    for termo in TERMOS_GENERO_IGNORAR:
        # Usa regex para remover o termo com word boundaries
        pattern = re.compile(re.escape(termo), re.IGNORECASE)
        nome_lower = pattern.sub(' ', nome_lower)
    
    # Remove caracteres especiais e normaliza espaços
    nome_lower = re.sub(r'[_\-\.\[\]\(\)]', ' ', nome_lower)
    nome_lower = re.sub(r'\s+', ' ', nome_lower).strip()
    
    return nome_lower


def verificar_keyword_valida(keyword: str, nome: str) -> bool:
    """
    Verifica se uma keyword é um match válido no nome.
    
    Keywords curtas (definidas em KEYWORDS_CURTAS) usam word boundary estrito.
    Keywords maiores podem ser substring.
    
    Args:
        keyword: A keyword a procurar
        nome: O nome do arquivo (já em lowercase)
        
    Returns:
        True se é um match válido
    """
    keyword_lower = keyword.lower()
    
    # Keywords definidas como curtas precisam de word boundary estrito
    if keyword_lower in KEYWORDS_CURTAS:
        # Usa regex para garantir que é uma palavra completa
        # Word boundary aceita separadores como _, -, espaço
        pattern = r'(?:^|[\s_\-])' + re.escape(keyword_lower) + r'(?:[\s_\-]|$)'
        return bool(re.search(pattern, nome, re.IGNORECASE))
    else:
        # Keywords maiores/normais podem ser substring
        return keyword_lower in nome


def identificar_categorias(nome_arquivo: str) -> List[str]:
    """
    Identifica TODAS as categorias de um preset baseado no nome do arquivo.
    
    Diferente da versão anterior, esta retorna MÚLTIPLAS categorias
    quando o nome contém keywords de categorias diferentes.
    
    Exemplo: "Bass Lead Hybrid.fxp" -> ["Bass", "Lead"]
    
    Args:
        nome_arquivo: Nome do arquivo de preset (com ou sem extensão)
        
    Returns:
        Lista de categorias identificadas (pode ser vazia se nenhuma)
    """
    # Limpa o nome removendo termos de gênero
    nome_limpo = limpar_nome_para_analise(nome_arquivo)
    
    categorias_encontradas: Set[str] = set()
    
    # Itera sobre cada categoria e suas keywords
    for categoria, lista_keywords in MAPA_CATEGORIAS.items():
        for keyword in lista_keywords:
            # Verifica se a keyword é um match válido
            if verificar_keyword_valida(keyword, nome_limpo):
                categorias_encontradas.add(categoria)
                break  # Uma keyword por categoria é suficiente
    
    return list(categorias_encontradas)


def identificar_categoria(nome_arquivo: str) -> str:
    """
    Identifica a categoria principal de um preset (compatibilidade).
    
    Retorna a primeira categoria encontrada ou CATEGORIA_PADRAO.
    Para multi-categorização, use identificar_categorias().
    
    Args:
        nome_arquivo: Nome do arquivo de preset
        
    Returns:
        Nome da categoria identificada
    """
    categorias = identificar_categorias(nome_arquivo)
    return categorias[0] if categorias else CATEGORIA_PADRAO


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
