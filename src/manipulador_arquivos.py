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
from src.categorizador import identificar_categorias, validar_extensao, identificar_categoria_especial


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


def copiar_preset_seguro(arquivo_origem: Path, pasta_destino: Path, mover: bool = False, deletar_se_existe: bool = False) -> Tuple[Path, bool, bool]:
    """
    Copia ou move um preset para a pasta de destino de forma segura.
    
    - Preserva metadados usando shutil.copy2 ou shutil.move
    - Gera nome único se arquivo com mesmo nome já existir
    - Pode deletar origem se já existe no destino (modo re-verificação, comparando hash)
    
    Args:
        arquivo_origem: Path do arquivo a ser copiado/movido
        pasta_destino: Path da pasta de destino
        mover: Se True, move o arquivo em vez de copiar
        deletar_se_existe: Se True e arquivo IDÊNTICO já existe no destino, deleta da origem
        
    Returns:
        Tuple com (caminho_final, ja_existia, foi_deletado_origem)
    """
    # Cria a pasta de destino se não existir
    pasta_destino.mkdir(parents=True, exist_ok=True)
    
    # Define caminho de destino
    caminho_destino = pasta_destino / arquivo_origem.name
    
    # Se já existe no destino
    if caminho_destino.exists():
        # Verifica se são o mesmo arquivo (mesmo caminho absoluto)
        if arquivo_origem.resolve() == caminho_destino.resolve():
            # É o mesmo arquivo - não faz nada
            return caminho_destino, True, False
        
        # Compara hash para verificar se é duplicata real
        hash_origem = calcular_hash_arquivo(arquivo_origem)
        hash_destino = calcular_hash_arquivo(caminho_destino)
        
        if hash_origem == hash_destino:
            # Conteúdo idêntico - é duplicata real
            if deletar_se_existe and arquivo_origem.exists():
                arquivo_origem.unlink()
                return caminho_destino, True, True  # ja_existia=True, foi_deletado=True
            return caminho_destino, True, False
        else:
            # Nome igual mas conteúdo diferente - gera nome único
            caminho_destino = gerar_nome_unico(caminho_destino)
    
    # Copia ou move preservando metadados
    if mover:
        shutil.move(str(arquivo_origem), str(caminho_destino))
    else:
        shutil.copy2(arquivo_origem, caminho_destino)
    
    return caminho_destino, False, False


def detectar_modo_reverificacao(pasta_origem: str, pasta_destino: str) -> bool:
    """
    Detecta se é um modo de re-verificação (reorganização).
    
    É re-verificação quando:
    - Pasta de origem termina com "Uncategorized"
    - Pasta de destino é o diretório pai da origem
    
    Args:
        pasta_origem: Caminho da pasta de origem
        pasta_destino: Caminho da pasta de destino
        
    Returns:
        True se é modo de re-verificação (deve MOVER, não copiar)
    """
    origem = Path(pasta_origem).resolve()
    destino = Path(pasta_destino).resolve()
    
    # Verifica se origem termina com "Uncategorized"
    if origem.name.lower() != "uncategorized":
        return False
    
    # Verifica se destino é o pai da origem
    if origem.parent == destino:
        return True
    
    return False


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


def organizar_presets_multiplas_origens(
    pastas_origem: List[str],
    pasta_destino: str,
    callback_progresso: Optional[Callable] = None,
    callback_arquivo: Optional[Callable] = None,
    callback_scan: Optional[Callable] = None,
    callback_pasta: Optional[Callable] = None
) -> dict:
    """
    Organiza presets de MÚLTIPLAS pastas de origem para um único destino.
    
    Args:
        pastas_origem: Lista de caminhos das pastas com presets
        pasta_destino: Caminho da pasta onde será criada a estrutura organizada
        callback_progresso: Função chamada com (atual, total) para atualizar progresso
        callback_arquivo: Função chamada com (arquivo, categorias, info)
        callback_scan: Função chamada durante o scan com (contador)
        callback_pasta: Função chamada ao iniciar cada pasta (pasta, indice, total)
        
    Returns:
        Dicionário com estatísticas consolidadas de todas as origens
    """
    # Estatísticas consolidadas
    estatisticas_total = {
        "total_arquivos_origem": 0,
        "total_copias_realizadas": 0,
        "total_duplicatas_ignoradas": 0,
        "total_multi_categoria": 0,
        "por_categoria": {},
        "erros": [],
        "arquivos_processados": [],
        "modo_mover": False,
        "pastas_processadas": [],
        "estatisticas_por_pasta": {}
    }
    
    # Hashes globais para detectar duplicatas entre pastas
    hashes_globais: Dict[str, str] = {}
    
    for idx, pasta_origem in enumerate(pastas_origem, 1):
        if callback_pasta:
            callback_pasta(pasta_origem, idx, len(pastas_origem))
        
        # Organiza esta pasta
        stats = organizar_presets(
            pasta_origem,
            pasta_destino,
            callback_progresso=callback_progresso,
            callback_arquivo=callback_arquivo,
            callback_scan=callback_scan,
            hashes_existentes=hashes_globais  # Passa hashes acumulados
        )
        
        # Consolida estatísticas
        estatisticas_total["total_arquivos_origem"] += stats["total_arquivos_origem"]
        estatisticas_total["total_copias_realizadas"] += stats["total_copias_realizadas"]
        estatisticas_total["total_duplicatas_ignoradas"] += stats["total_duplicatas_ignoradas"]
        estatisticas_total["total_multi_categoria"] += stats["total_multi_categoria"]
        estatisticas_total["erros"].extend(stats["erros"])
        estatisticas_total["arquivos_processados"].extend(stats["arquivos_processados"])
        estatisticas_total["pastas_processadas"].append(pasta_origem)
        estatisticas_total["estatisticas_por_pasta"][pasta_origem] = stats
        
        # Consolida contagem por categoria
        for cat, qtd in stats["por_categoria"].items():
            if cat not in estatisticas_total["por_categoria"]:
                estatisticas_total["por_categoria"][cat] = 0
            estatisticas_total["por_categoria"][cat] += qtd
        
        # Atualiza hashes globais
        hashes_globais.update(stats.get("_hashes", {}))
    
    return estatisticas_total


def organizar_presets(
    pasta_origem: str, 
    pasta_destino: str,
    callback_progresso: Optional[Callable] = None,
    callback_arquivo: Optional[Callable] = None,
    callback_scan: Optional[Callable] = None,
    modo_mover: bool = None,
    hashes_existentes: Optional[Dict[str, str]] = None
) -> dict:
    """
    Função principal que organiza todos os presets da origem para o destino.
    
    CARACTERÍSTICAS:
    - Multi-categorização: arquivos podem ir para múltiplas categorias
    - Detecção de duplicatas por hash: arquivos idênticos são ignorados
    - Categorias especiais: Hash -> Arquivos_Corrompidos, Português -> Customizados
    - Modo re-verificação: detecta automaticamente se deve mover (origem=Uncategorized)
    - Nunca cria cópias desnecessárias
    
    Args:
        pasta_origem: Caminho da pasta com os presets desorganizados
        pasta_destino: Caminho da pasta onde será criada a estrutura organizada
        callback_progresso: Função chamada com (atual, total) para atualizar progresso
        callback_arquivo: Função chamada com (arquivo, categorias, info)
        callback_scan: Função chamada durante o scan com (contador)
        modo_mover: Se True, move arquivos. Se None, detecta automaticamente.
        hashes_existentes: Dicionário de hashes já processados (para múltiplas origens)
        
    Returns:
        Dicionário com estatísticas da operação
    """
    # Detecta se é modo de re-verificação (deve mover)
    if modo_mover is None:
        modo_mover = detectar_modo_reverificacao(pasta_origem, pasta_destino)
    
    # Inicializa estatísticas
    estatisticas = {
        "total_arquivos_origem": 0,
        "total_copias_realizadas": 0,
        "total_duplicatas_ignoradas": 0,
        "total_multi_categoria": 0,
        "por_categoria": {},
        "erros": [],
        "arquivos_processados": [],
        "modo_mover": modo_mover  # Registra o modo usado
    }
    
    pasta_destino_path = Path(pasta_destino)
    
    # Registro de hashes para detectar duplicatas de conteúdo
    # Usa hashes existentes se fornecido (para múltiplas origens)
    hashes_copiados: Dict[str, str] = dict(hashes_existentes) if hashes_existentes else {}
    
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
            
            # Primeiro, verifica categorias especiais (hash, português)
            categoria_especial = identificar_categoria_especial(arquivo_preset.name)
            
            # Identifica TODAS as categorias aplicáveis (keywords)
            categorias = identificar_categorias(arquivo_preset.name)
            
            # Se nenhuma categoria por keyword encontrada
            if not categorias:
                if categoria_especial:
                    # Usa categoria especial (Arquivos_Corrompidos ou Customizados)
                    categorias = [categoria_especial]
                else:
                    # Vai para Uncategorized
                    categorias = [CATEGORIA_PADRAO]
            
            # Se múltiplas categorias, registra
            if len(categorias) > 1:
                estatisticas["total_multi_categoria"] += 1
            
            # CORREÇÃO: Se a única categoria é Uncategorized e estamos em modo mover
            # da pasta Uncategorized, não faz nada (arquivo já está no lugar certo)
            if modo_mover and categorias == [CATEGORIA_PADRAO]:
                # Arquivo sem categoria, permanece onde está
                if CATEGORIA_PADRAO not in estatisticas["por_categoria"]:
                    estatisticas["por_categoria"][CATEGORIA_PADRAO] = 0
                estatisticas["por_categoria"][CATEGORIA_PADRAO] += 1
                
                if callback_arquivo:
                    callback_arquivo(
                        arquivo_preset.name,
                        categorias,
                        {
                            "tipo": "processado",
                            "multi": False,
                            "contador": contador,
                            "total": total_arquivos,
                            "movido": False
                        }
                    )
                
                if callback_progresso:
                    callback_progresso(contador, total_arquivos)
                continue  # Pula para o próximo arquivo
            
            # Copia/Move para cada categoria encontrada
            primeiro_destino = None
            arquivo_deletado = False
            for categoria in categorias:
                pasta_categoria = pasta_destino_path / categoria
                caminho_final, ja_existia, foi_deletado = copiar_preset_seguro(
                    arquivo_preset, 
                    pasta_categoria, 
                    mover=(modo_mover and primeiro_destino is None),  # Só move na primeira categoria
                    deletar_se_existe=(modo_mover and primeiro_destino is None)  # Deleta se já existe (re-verificação)
                )
                
                if foi_deletado:
                    arquivo_deletado = True
                    estatisticas["total_deletados_origem"] = estatisticas.get("total_deletados_origem", 0) + 1
                
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
                        "total": total_arquivos,
                        "movido": modo_mover
                    }
                )
            
            if callback_progresso:
                callback_progresso(contador, total_arquivos)
            
        except Exception as erro:
            estatisticas["erros"].append({
                "arquivo": str(arquivo_preset),
                "erro": str(erro)
            })
    
    # Retorna hashes para uso em múltiplas origens
    estatisticas["_hashes"] = hashes_copiados
    
    return estatisticas
