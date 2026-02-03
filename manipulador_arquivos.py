# -*- coding: utf-8 -*-
"""
Módulo de Manipulação de Arquivos - Serum Preset Organizer
===========================================================
Contém funções para busca, cópia e organização de arquivos.
"""

import os
import shutil
from pathlib import Path
from typing import Generator, Tuple

from config import EXTENSOES_SUPORTADAS
from categorizador import identificar_categoria, validar_extensao


def buscar_presets_recursivo(pasta_origem: str) -> Generator[Path, None, None]:
    """
    Busca recursivamente todos os arquivos de preset na pasta de origem.
    
    Args:
        pasta_origem: Caminho da pasta raiz para iniciar a busca
        
    Yields:
        Objetos Path para cada arquivo de preset encontrado
    """
    pasta_raiz = Path(pasta_origem)
    
    # Verifica se a pasta existe
    if not pasta_raiz.exists():
        raise FileNotFoundError(f"Pasta de origem não encontrada: {pasta_origem}")
    
    if not pasta_raiz.is_dir():
        raise NotADirectoryError(f"O caminho não é uma pasta: {pasta_origem}")
    
    # Busca recursiva usando rglob
    for arquivo in pasta_raiz.rglob("*"):
        if arquivo.is_file() and validar_extensao(arquivo.name, EXTENSOES_SUPORTADAS):
            yield arquivo


def gerar_nome_unico(caminho_destino: Path) -> Path:
    """
    Gera um nome único para o arquivo caso já exista no destino.
    
    Adiciona sufixo numérico incremental: arquivo.fxp -> arquivo_1.fxp -> arquivo_2.fxp
    
    Args:
        caminho_destino: Caminho completo do arquivo de destino
        
    Returns:
        Path com nome único (original se não existir duplicata)
    """
    if not caminho_destino.exists():
        return caminho_destino
    
    # Separa nome base e extensão
    nome_base = caminho_destino.stem
    extensao = caminho_destino.suffix
    pasta_pai = caminho_destino.parent
    
    # Incrementa contador até encontrar nome disponível
    contador = 1
    while True:
        novo_nome = f"{nome_base}_{contador}{extensao}"
        novo_caminho = pasta_pai / novo_nome
        
        if not novo_caminho.exists():
            return novo_caminho
        
        contador += 1
        
        # Proteção contra loop infinito (improvável mas seguro)
        if contador > 10000:
            raise RuntimeError(f"Muitas duplicatas para o arquivo: {nome_base}")


def copiar_preset_seguro(arquivo_origem: Path, pasta_destino: Path) -> Tuple[Path, bool]:
    """
    Copia um preset para a pasta de destino de forma segura.
    
    - Preserva metadados usando shutil.copy2
    - Trata duplicatas gerando nome único
    - Nunca sobrescreve arquivos existentes
    
    Args:
        arquivo_origem: Path do arquivo a ser copiado
        pasta_destino: Path da pasta de destino
        
    Returns:
        Tuple com (caminho_final, foi_renomeado)
    """
    # Cria a pasta de destino se não existir
    pasta_destino.mkdir(parents=True, exist_ok=True)
    
    # Define caminho inicial de destino
    caminho_destino = pasta_destino / arquivo_origem.name
    
    # Verifica e trata duplicatas
    caminho_final = gerar_nome_unico(caminho_destino)
    foi_renomeado = (caminho_final.name != arquivo_origem.name)
    
    # Copia preservando metadados
    shutil.copy2(arquivo_origem, caminho_final)
    
    return caminho_final, foi_renomeado


def organizar_presets(pasta_origem: str, pasta_destino: str) -> dict:
    """
    Função principal que organiza todos os presets da origem para o destino.
    
    Args:
        pasta_origem: Caminho da pasta com os presets desorganizados
        pasta_destino: Caminho da pasta onde será criada a estrutura organizada
        
    Returns:
        Dicionário com estatísticas da operação
    """
    # Inicializa estatísticas
    estatisticas = {
        "total_processados": 0,
        "total_duplicatas": 0,
        "por_categoria": {},
        "erros": []
    }
    
    pasta_destino_path = Path(pasta_destino)
    
    # Processa cada preset encontrado
    for arquivo_preset in buscar_presets_recursivo(pasta_origem):
        try:
            # Identifica a categoria baseado no nome
            categoria = identificar_categoria(arquivo_preset.name)
            
            # Define pasta de destino para esta categoria
            pasta_categoria = pasta_destino_path / categoria
            
            # Copia o arquivo
            caminho_final, foi_renomeado = copiar_preset_seguro(arquivo_preset, pasta_categoria)
            
            # Atualiza estatísticas
            estatisticas["total_processados"] += 1
            
            if foi_renomeado:
                estatisticas["total_duplicatas"] += 1
            
            if categoria not in estatisticas["por_categoria"]:
                estatisticas["por_categoria"][categoria] = 0
            estatisticas["por_categoria"][categoria] += 1
            
        except Exception as erro:
            estatisticas["erros"].append({
                "arquivo": str(arquivo_preset),
                "erro": str(erro)
            })
    
    return estatisticas
