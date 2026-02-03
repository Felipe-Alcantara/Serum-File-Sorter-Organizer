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
import time
from datetime import datetime
from pathlib import Path

# Adiciona o diretório atual ao path para importar módulos locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.manipulador_arquivos import organizar_presets, contar_presets, buscar_presets_recursivo
from src.categorizador import obter_todas_categorias
from src.config import EXTENSOES_SUPORTADAS, MAPA_CATEGORIAS
from src.interface_visual import (
    Cores, Icones, 
    exibir_banner_principal, exibir_categorias_visual,
    exibir_confirmacao, exibir_resultado_final,
    log_fase, log_arquivo_processado, log_resumo_busca,
    sucesso, erro, aviso, info, destaque, dim,
    cabecalho, caixa_info, linha_separadora,
    barra_progresso, atualizar_linha, animacao_processando,
    ICONES_CATEGORIAS
)


# ============================================================================
# CONFIGURAÇÃO - Edite aqui ou deixe vazio para input via terminal
# ============================================================================
PASTA_ORIGEM = ""   # Ex: "C:/Users/SeuNome/Downloads/Serum Presets"
PASTA_DESTINO = ""  # Ex: "C:/Users/SeuNome/Documents/Serum Organized"

# Opções de exibição
MODO_VERBOSE = True   # True = mostra cada arquivo, False = apenas progresso
# ============================================================================


def solicitar_caminho(mensagem: str, deve_existir: bool = True) -> str:
    """
    Solicita um caminho ao usuário via terminal com validação.
    
    Args:
        mensagem: Mensagem a exibir
        deve_existir: Se True, valida que o caminho existe
        
    Returns:
        Caminho validado
    """
    while True:
        print(f"\n  {Icones.PASTA} {Cores.BOLD}{mensagem}{Cores.RESET}")
        caminho = input(f"  {Cores.CIANO_CLARO}>{Cores.RESET} ").strip()
        
        # Remove aspas se o usuário colar caminho com aspas
        caminho = caminho.strip('"').strip("'")
        
        if not caminho:
            print(f"  {Icones.ERRO} {erro('Caminho não pode estar vazio.')}")
            continue
        
        # Expande ~ para pasta do usuário se usado
        caminho = os.path.expanduser(caminho)
        
        if deve_existir:
            if not os.path.exists(caminho):
                print(f"  {Icones.ERRO} {erro('Caminho não encontrado:')} {dim(caminho)}")
                continue
            if not os.path.isdir(caminho):
                print(f"  {Icones.ERRO} {erro('Não é uma pasta válida:')} {dim(caminho)}")
                continue
        
        # Confirmação visual do caminho
        print(f"  {Icones.SUCESSO} {sucesso('Caminho válido:')} {caminho}")
        return caminho


def fase_busca_presets(pasta_origem: str) -> tuple:
    """
    Fase 1: Busca e conta os presets na origem.
    
    Args:
        pasta_origem: Caminho da pasta de origem
        
    Returns:
        Tuple com (lista_de_arquivos, tempo_busca)
    """
    log_fase(1, "ANÁLISE DA ORIGEM", "Escaneando pasta e subpastas em busca de presets...")
    
    print(f"  {Icones.BUSCAR} Buscando arquivos {Cores.CIANO_CLARO}.fxp{Cores.RESET} e {Cores.CIANO_CLARO}.SerumPreset{Cores.RESET}...")
    print(f"  {Icones.PASTA} Origem: {dim(pasta_origem)}")
    print()
    
    inicio = time.time()
    
    # Animação enquanto conta
    animacao_processando("Escaneando diretórios", 0.8)
    
    # Conta os arquivos
    arquivos = list(buscar_presets_recursivo(pasta_origem))
    total = len(arquivos)
    
    tempo_busca = time.time() - inicio
    
    log_resumo_busca(total, EXTENSOES_SUPORTADAS, tempo_busca)
    
    return arquivos, tempo_busca


def fase_organizacao(pasta_origem: str, pasta_destino: str, total_arquivos: int) -> tuple:
    """
    Fase 2: Organiza os presets nas categorias.
    
    Args:
        pasta_origem: Caminho da origem
        pasta_destino: Caminho do destino
        total_arquivos: Total de arquivos a processar
        
    Returns:
        Tuple com (estatisticas, tempo_execucao)
    """
    log_fase(2, "ORGANIZANDO PRESETS", f"Copiando e categorizando {total_arquivos} arquivos...")
    
    print(f"  {Icones.INFO} {info('Legenda:')}")
    print(f"      {Cores.VERDE_CLARO}→{Cores.RESET} Arquivo copiado com sucesso")
    print(f"      {Cores.AMARELO_CLARO}(renomeado){Cores.RESET} Duplicata detectada e renomeada")
    print()
    
    # Contador para exibição
    arquivos_mostrados = 0
    max_mostrar = 50  # Limite de linhas para não poluir muito
    
    def callback_arquivo(arquivo, categoria, duplicata, contador, total):
        """Callback chamado para cada arquivo processado."""
        nonlocal arquivos_mostrados
        
        if MODO_VERBOSE and arquivos_mostrados < max_mostrar:
            log_arquivo_processado(arquivo, categoria, duplicata, contador, total)
            arquivos_mostrados += 1
        elif arquivos_mostrados == max_mostrar:
            print(f"\n  {Cores.DIM}... continuando em modo silencioso ({total - max_mostrar} restantes){Cores.RESET}\n")
            arquivos_mostrados += 1
        
        # Sempre atualiza a barra de progresso
        if not MODO_VERBOSE or arquivos_mostrados >= max_mostrar:
            porcentagem = (contador / total * 100) if total > 0 else 100
            barra_visual = barra_progresso(contador, total, largura=35)
            atualizar_linha(f"  {barra_visual} ({contador}/{total})")
    
    inicio = time.time()
    
    estatisticas = organizar_presets(
        pasta_origem, 
        pasta_destino,
        callback_arquivo=callback_arquivo
    )
    
    tempo_execucao = time.time() - inicio
    
    # Limpa a linha de progresso e mostra conclusão
    print()
    print(f"\n  {Icones.SUCESSO} {sucesso('Organização concluída!')}")
    
    return estatisticas, tempo_execucao


def exibir_preview_categorias(estatisticas: dict):
    """
    Exibe uma prévia das categorias encontradas durante o processo.
    
    Args:
        estatisticas: Dicionário de estatísticas
    """
    if not estatisticas['por_categoria']:
        return
    
    print(f"\n  {Cores.BOLD}📊 PRÉVIA DAS CATEGORIAS ENCONTRADAS{Cores.RESET}")
    print(f"  {Cores.DIM}{'─' * 45}{Cores.RESET}")
    
    for categoria, qtd in sorted(estatisticas['por_categoria'].items(), key=lambda x: -x[1])[:5]:
        icone = ICONES_CATEGORIAS.get(categoria, "📄")
        print(f"  {icone} {categoria}: {Cores.VERDE_CLARO}{qtd}{Cores.RESET} presets")
    
    if len(estatisticas['por_categoria']) > 5:
        restantes = len(estatisticas['por_categoria']) - 5
        print(f"  {Cores.DIM}... e mais {restantes} categorias{Cores.RESET}")


def main():
    """Função principal do programa."""
    
    # Banner inicial
    exibir_banner_principal()
    
    # Timestamp de início
    print(f"  {Cores.DIM}⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}{Cores.RESET}")
    linha_separadora("─", 70)
    
    # Determina os caminhos (variáveis ou input)
    if PASTA_ORIGEM and PASTA_DESTINO:
        pasta_origem = PASTA_ORIGEM
        pasta_destino = PASTA_DESTINO
        print(f"\n  {Icones.INFO} {info('Usando caminhos pré-configurados no código.')}")
        print(f"      {Icones.PASTA} Origem:  {pasta_origem}")
        print(f"      {Icones.PASTA} Destino: {pasta_destino}")
    else:
        # Mostra categorias disponíveis
        exibir_categorias_visual(MAPA_CATEGORIAS)
        
        # Solicita caminhos
        pasta_origem = solicitar_caminho(
            "Digite o caminho da pasta de ORIGEM (onde estão os presets):"
        )
        pasta_destino = solicitar_caminho(
            "Digite o caminho da pasta de DESTINO (onde serão organizados):",
            deve_existir=False
        )
    
    # Confirmação do usuário
    if not exibir_confirmacao(pasta_origem, pasta_destino, EXTENSOES_SUPORTADAS):
        print(f"\n  {Icones.ERRO} {erro('Operação cancelada pelo usuário.')}")
        print(f"  {Cores.DIM}Nenhum arquivo foi modificado.{Cores.RESET}\n")
        return
    
    print()
    linha_separadora("═", 70, Cores.MAGENTA_CLARO)
    
    # ========== FASE 1: BUSCA ==========
    try:
        arquivos, tempo_busca = fase_busca_presets(pasta_origem)
    except FileNotFoundError as e:
        print(f"\n  {Icones.ERRO} {erro(str(e))}")
        return
    except Exception as e:
        print(f"\n  {Icones.ERRO} {erro(f'Erro durante a busca: {e}')}")
        return
    
    if len(arquivos) == 0:
        print(f"\n  {Icones.AVISO} {aviso('Nenhum preset encontrado!')}")
        print(f"      Verifique se a pasta contém arquivos .fxp ou .SerumPreset")
        print(f"      Pasta verificada: {dim(pasta_origem)}\n")
        return
    
    # ========== FASE 2: ORGANIZAÇÃO ==========
    try:
        estatisticas, tempo_organizacao = fase_organizacao(
            pasta_origem, 
            pasta_destino, 
            len(arquivos)
        )
    except Exception as e:
        print(f"\n  {Icones.ERRO} {erro(f'Erro durante a organização: {e}')}")
        return
    
    # ========== FASE 3: RELATÓRIO FINAL ==========
    log_fase(3, "RELATÓRIO FINAL", "Resumo completo da operação")
    
    tempo_total = tempo_busca + tempo_organizacao
    exibir_resultado_final(estatisticas, tempo_total, pasta_destino)
    
    # Dica final
    print(f"  {Cores.DIM}💡 Dica: Execute novamente para processar novos presets adicionados{Cores.RESET}")
    print(f"  {Cores.DIM}         Arquivos duplicados serão renomeados automaticamente{Cores.RESET}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Icones.AVISO} {aviso('Operação interrompida pelo usuário (Ctrl+C)')}")
        print(f"  {Cores.DIM}Alguns arquivos podem ter sido copiados parcialmente.{Cores.RESET}\n")
    except Exception as e:
        print(f"\n\n  {Icones.ERRO} {erro(f'Erro inesperado: {e}')}")
        print(f"  {Cores.DIM}Por favor, reporte este erro.{Cores.RESET}\n")
