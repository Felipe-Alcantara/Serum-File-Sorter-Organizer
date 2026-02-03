# -*- coding: utf-8 -*-
"""
Serum Preset Organizer
======================
Pacote principal para organização de presets do sintetizador Serum.

Módulos:
    - config: Configurações e mapeamento de categorias
    - categorizador: Lógica de identificação de categoria
    - manipulador_arquivos: Funções de busca e cópia
    - interface_visual: Interface colorida para terminal
"""

from src.config import MAPA_CATEGORIAS, EXTENSOES_SUPORTADAS, CATEGORIA_PADRAO
from src.categorizador import identificar_categoria, validar_extensao
from src.manipulador_arquivos import organizar_presets, buscar_presets_recursivo

__version__ = "1.0.0"
__author__ = "Serum File Sorter Organizer"

__all__ = [
    "MAPA_CATEGORIAS",
    "EXTENSOES_SUPORTADAS", 
    "CATEGORIA_PADRAO",
    "identificar_categoria",
    "validar_extensao",
    "organizar_presets",
    "buscar_presets_recursivo"
]
