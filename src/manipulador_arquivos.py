# -*- coding: utf-8 -*-
"""
Módulo de Manipulação de Arquivos - Serum Preset Organizer
===========================================================
Contém funções para busca, cópia e organização de arquivos.
"""

import os
import shutil
import time
import hashlib
from pathlib import Path
from typing import Generator, Tuple, Callable, Optional, List, Set, Dict

from src.config import EXTENSOES_SUPORTADAS, CATEGORIA_PADRAO
from src.categorizador import identificar_categorias, validar_extensao


def calcular_hash_arquivo(caminho_arquivo: Path, tamanho_bloco: int = 65536) -> str:
    """
    Calcula o hash MD5 de um arquivo para detectar duplicatas.
    
    Args:
        caminho_arquivo: Path do arquivo
        tamanho_bloco: Tamanho do bloco para leitura
        
    Returns:
        Hash MD5 do arquivo como string hexadecimal
    """
    hasher = hashlib.md5()
    with open(caminho_arquivo, 'rb') as f:
        for bloco in iter(lambda: f.read(tamanho_bloco), b''):
            hasher.update(bloco)
    return hasher.hexdigest()


def buscar_presets_recursivo(
    pasta_origem: str,
    callback_progresso: Optional[Callable] = None
) -> Generator[Path, None, None]:
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
    - Nunca sobrescreve arquivos existentes
    
    Args:
        arquivo_origem: Path do arquivo a ser copiado
        pasta_destino: Path da pasta de destino
        
    Returns:
        Tuple com (caminho_final, ja_existia)
    """
    # Cria a pasta de destino se não existir
    pasta_destino.mkdir(parents=True, exist_ok=True)
    
    # Define caminho de destino
    caminho_destino = pasta_destino / arquivo_origem.name
    
    # Se já existe, não copia (será tratado como duplicata)
    if caminho_destino.exists():
        return caminho_destino, True
    
    # Copia preservando metadados
    shutil.copy2(arquivo_origem, caminho_destino)
    
    return caminho_destino, False


def contar_presets_com_progresso(
    pasta_origem: str,
    callback_contagem: Optional[Callable] = None
) -> List[Path]:
    """
    Lista todos os presets na pasta de origem com callback de progresso.
    
    Args:
        pasta_origem: Caminho da pasta raiz
        callback_contagem: Função chamada com (contador) a cada arquivo encontrado
        
    Returns:
        Lista de Paths dos arquivos encontrados
    """
    arquivos = []
    contador = 0
    
    for arquivo in buscar_presets_recursivo(pasta_origem):
        arquivos.append(arquivo)
        contador += 1
        if callback_contagem:
            callback_contagem(contador)
    
    return arquivos


def organizar_presets(
    pasta_origem: str, 
    pasta_destino: str,
    callback_progresso: Optional[Callable] = None,
    callback_arquivo: Optional[Callable] = None,
    callback_scan: Optional[Callable] = None
) -> dict:
    """
    Função principal que organiza todos os presets da origem para o destino.
    
    CARACTERÍSTICAS:
    - Multi-categorização: arquivos podem ir para múltiplas categorias
    - Detecção de duplicatas por hash: arquivos idênticos são ignorados
    - Nunca cria cópias desnecessárias
    
    Args:
        pasta_origem: Caminho da pasta com os presets desorganizados
        pasta_destino: Caminho da pasta onde será criada a estrutura organizada
        callback_progresso: Função chamada com (atual, total) para atualizar progresso
        callback_arquivo: Função chamada com (arquivo, categorias, info)
        callback_scan: Função chamada durante o scan com (contador)
        
    Returns:
        Dicionário com estatísticas da operação
    """
    # Inicializa estatísticas
    estatisticas = {
        "total_arquivos_origem": 0,
        "total_copias_realizadas": 0,
        "total_duplicatas_ignoradas": 0,
        "total_multi_categoria": 0,
        "por_categoria": {},
        "erros": [],
        "arquivos_processados": []
    }
    
    pasta_destino_path = Path(pasta_destino)
    
    # Registro de hashes para detectar duplicatas de conteúdo
    hashes_copiados: Dict[str, str] = {}  # hash -> caminho do primeiro arquivo
    
    # Fase 1: Escaneia todos os arquivos
    arquivos = contar_presets_com_progresso(pasta_origem, callback_scan)
    total_arquivos = len(arquivos)
    estatisticas["total_arquivos_origem"] = total_arquivos
    
    # Fase 2: Processa cada arquivo
    for contador, arquivo_preset in enumerate(arquivos, 1):
        try:
            # Calcula hash do arquivo para detectar duplicatas
            hash_arquivo = calcular_hash_arquivo(arquivo_preset)
            
            # Verifica se já copiamos um arquivo com este conteúdo
            if hash_arquivo in hashes_copiados:
                estatisticas["total_duplicatas_ignoradas"] += 1
                
                if callback_arquivo:
                    callback_arquivo(
                        arquivo_preset.name,
                        [],  # Nenhuma categoria (duplicata)
                        {
                            "tipo": "duplicata_ignorada",
                            "original": hashes_copiados[hash_arquivo],
                            "contador": contador,
                            "total": total_arquivos
                        }
                    )
                continue
            
            # Identifica TODAS as categorias aplicáveis
            categorias = identificar_categorias(arquivo_preset.name)
            
            # Se nenhuma categoria encontrada, vai para Uncategorized
            if not categorias:
                categorias = [CATEGORIA_PADRAO]
            
            # Se múltiplas categorias, registra
            if len(categorias) > 1:
                estatisticas["total_multi_categoria"] += 1
            
            # Copia para cada categoria encontrada
            primeiro_destino = None
            for categoria in categorias:
                pasta_categoria = pasta_destino_path / categoria
                caminho_final, ja_existia = copiar_preset_seguro(arquivo_preset, pasta_categoria)
                
                if not ja_existia:
                    estatisticas["total_copias_realizadas"] += 1
                    
                    if primeiro_destino is None:
                        primeiro_destino = str(caminho_final)
                
                # Atualiza contagem por categoria
                if categoria not in estatisticas["por_categoria"]:
                    estatisticas["por_categoria"][categoria] = 0
                estatisticas["por_categoria"][categoria] += 1
            
            # Registra o hash com o primeiro destino
            if primeiro_destino:
                hashes_copiados[hash_arquivo] = primeiro_destino
            
            # Registra detalhes do arquivo
            estatisticas["arquivos_processados"].append({
                "origem": str(arquivo_preset),
                "categorias": categorias,
                "multi": len(categorias) > 1
            })
            
            # Callback para atualizar interface
            if callback_arquivo:
                callback_arquivo(
                    arquivo_preset.name,
                    categorias,
                    {
                        "tipo": "processado",
                        "multi": len(categorias) > 1,
                        "contador": contador,
                        "total": total_arquivos
                    }
                )
            
            if callback_progresso:
                callback_progresso(contador, total_arquivos)
            
        except Exception as erro:
            estatisticas["erros"].append({
                "arquivo": str(arquivo_preset),
                "erro": str(erro)
            })
    
    return estatisticas
