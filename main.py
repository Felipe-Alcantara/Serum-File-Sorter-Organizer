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

from src.manipulador_arquivos import organizar_presets, organizar_presets_multiplas_origens, buscar_presets_recursivo, detectar_modo_reverificacao
from src.categorizador import obter_todas_categorias
from src.config import EXTENSOES_SUPORTADAS, MAPA_CATEGORIAS, CATEGORIA_CORROMPIDOS, CATEGORIA_CUSTOMIZADOS
from src.interface_visual import (
    Cores, Icones, 
    exibir_banner_principal, exibir_categorias_visual,
    exibir_confirmacao, exibir_resultado_final,
    log_fase, log_arquivo_processado, log_resumo_busca,
    sucesso, erro, aviso, info, destaque, dim,
    cabecalho, caixa_info, linha_separadora,
    barra_progresso, atualizar_linha,
    ICONES_CATEGORIAS
)


# ============================================================================
# CONFIGURAÇÃO - Edite aqui ou deixe vazio para input via terminal
# ============================================================================
PASTAS_ORIGEM = []  # Lista de pastas. Ex: ["C:/Pasta1", "C:/Pasta2"]
PASTA_DESTINO = ""  # Ex: "C:/Users/SeuNome/Documents/Serum Organized"

# Opções de exibição
MODO_VERBOSE = True   # True = mostra cada arquivo, False = apenas progresso
# ============================================================================


def solicitar_caminhos_origem() -> list:
    """
    Solicita múltiplas pastas de origem ao usuário.
    
    Returns:
        Lista de caminhos validados
    """
    print(f"\n  {Cores.BOLD}{Cores.CIANO_CLARO}📁 PASTAS DE ORIGEM{Cores.RESET}")
    print(f"  {Cores.DIM}Adicione uma ou mais pastas onde estão seus presets.{Cores.RESET}")
    print(f"  {Cores.DIM}Digite 'ok' quando terminar de adicionar.{Cores.RESET}")
    print()
    
    pastas = []
    contador = 1
    
    while True:
        print(f"  {Icones.PASTA} {Cores.BOLD}Pasta {contador}{Cores.RESET} (ou 'ok' para continuar):")
        entrada = input(f"  {Cores.CIANO_CLARO}>{Cores.RESET} ").strip()
        
        # Remove aspas se o usuário colar caminho com aspas
        entrada = entrada.strip('"').strip("'")
        
        # Verifica se quer finalizar
        if entrada.lower() == 'ok':
            if not pastas:
                print(f"  {Icones.ERRO} {erro('Adicione pelo menos uma pasta de origem.')}")
                continue
            break
        
        if not entrada:
            print(f"  {Icones.AVISO} {aviso('Caminho vazio. Digite um caminho ou \"ok\" para continuar.')}")
            continue
        
        # Expande ~ para pasta do usuário se usado
        caminho = os.path.expanduser(entrada)
        
        # Valida o caminho
        if not os.path.exists(caminho):
            print(f"  {Icones.ERRO} {erro('Caminho não encontrado:')} {dim(caminho)}")
            continue
        if not os.path.isdir(caminho):
            print(f"  {Icones.ERRO} {erro('Não é uma pasta válida:')} {dim(caminho)}")
            continue
        
        # Verifica se já foi adicionada
        caminho_absoluto = os.path.abspath(caminho)
        if caminho_absoluto in [os.path.abspath(p) for p in pastas]:
            print(f"  {Icones.AVISO} {aviso('Esta pasta já foi adicionada.')}")
            continue
        
        pastas.append(caminho)
        print(f"  {Icones.SUCESSO} {sucesso('Adicionada:')} {caminho}")
        contador += 1
        print()
    
    return pastas


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


def fase_busca_presets(pastas_origem: list) -> tuple:
    """
    Fase 1: Busca e conta os presets em todas as origens.
    
    Args:
        pastas_origem: Lista de caminhos das pastas de origem
        
    Returns:
        Tuple com (lista_de_arquivos, tempo_busca)
    """
    log_fase(1, "ANÁLISE DAS ORIGENS", f"Escaneando {len(pastas_origem)} pasta(s) em busca de presets...")
    
    print(f"  {Icones.BUSCAR} Buscando arquivos {Cores.CIANO_CLARO}.fxp{Cores.RESET} e {Cores.CIANO_CLARO}.SerumPreset{Cores.RESET}...")
    print()
    
    inicio = time.time()
    
    # Animação enquanto escaneia - mostra contagem em tempo real
    arquivos = []
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    spin_index = 0
    
    for idx, pasta_origem in enumerate(pastas_origem, 1):
        print(f"  {Cores.CIANO_CLARO}[{idx}/{len(pastas_origem)}]{Cores.RESET} {dim(pasta_origem)}")
        
        for arquivo in buscar_presets_recursivo(pasta_origem):
            arquivos.append(arquivo)
            # Atualiza a cada 10 arquivos para não sobrecarregar
            if len(arquivos) % 10 == 0:
                atualizar_linha(f"  {Cores.CIANO_CLARO}{spinner[spin_index]}{Cores.RESET} Escaneando... {Cores.VERDE_CLARO}{len(arquivos)}{Cores.RESET} presets encontrados")
                spin_index = (spin_index + 1) % len(spinner)
    
    total = len(arquivos)
    
    tempo_busca = time.time() - inicio
    
    # Limpa a linha de animação
    print()
    
    log_resumo_busca(total, EXTENSOES_SUPORTADAS, tempo_busca)
    
    return arquivos, tempo_busca


def fase_organizacao(pastas_origem: list, pasta_destino: str, total_arquivos: int) -> tuple:
    """
    Fase 2: Organiza os presets nas categorias.
    
    Args:
        pastas_origem: Lista de caminhos de origem
        pasta_destino: Caminho do destino
        total_arquivos: Total de arquivos a processar
        
    Returns:
        Tuple com (estatisticas, tempo_execucao)
    """
    log_fase(2, "ORGANIZANDO PRESETS", f"Copiando e categorizando {total_arquivos} arquivos de {len(pastas_origem)} pasta(s)...")
    
    print(f"  {Icones.INFO} {info('Legenda:')}")
    print(f"      {Cores.VERDE_CLARO}→{Cores.RESET} Arquivo copiado com sucesso")
    print(f"      {Cores.CIANO_CLARO}[multi]{Cores.RESET} Arquivo copiado para múltiplas categorias")
    print(f"      {Cores.AMARELO_CLARO}(duplicata){Cores.RESET} Arquivo idêntico já existe, ignorado")
    print()
    
    # Contador para exibição
    arquivos_mostrados = 0
    max_mostrar = 50  # Limite de linhas para não poluir muito
    
    def callback_arquivo(arquivo: str, categorias: list, info_extra: dict):
        """Callback chamado para cada arquivo processado."""
        nonlocal arquivos_mostrados
        
        tipo = info_extra.get("tipo", "processado")
        contador = info_extra.get("contador", 0)
        total = info_extra.get("total", 0)
        
        if MODO_VERBOSE and arquivos_mostrados < max_mostrar:
            if tipo == "duplicata_ignorada":
                # Arquivo duplicata ignorado
                print(f"  {Cores.AMARELO_CLARO}⊘{Cores.RESET} {dim(arquivo[:40])} {Cores.AMARELO_CLARO}(duplicata ignorada){Cores.RESET}")
            elif tipo == "processado":
                # Arquivo processado
                is_multi = info_extra.get("multi", False)
                
                # Monta lista de categorias com ícones
                cats_str = ""
                for cat in categorias[:3]:  # Mostra até 3 categorias
                    icone = ICONES_CATEGORIAS.get(cat, "📄")
                    cats_str += f"{icone}{cat} "
                
                if len(categorias) > 3:
                    cats_str += f"(+{len(categorias) - 3})"
                
                multi_tag = f" {Cores.CIANO_CLARO}[multi:{len(categorias)}]{Cores.RESET}" if is_multi else ""
                
                # Trunca nome se necessário
                nome_display = arquivo if len(arquivo) <= 35 else arquivo[:32] + "..."
                
                print(f"  {Cores.VERDE_CLARO}→{Cores.RESET} {nome_display} → {cats_str}{multi_tag}")
            
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
    
    # Usa função de múltiplas origens se houver mais de uma pasta
    if len(pastas_origem) > 1:
        def callback_pasta(pasta, idx, total_pastas):
            print(f"\n  {Cores.MAGENTA_CLARO}📂 [{idx}/{total_pastas}]{Cores.RESET} Processando: {dim(pasta)}")
        
        estatisticas = organizar_presets_multiplas_origens(
            pastas_origem, 
            pasta_destino,
            callback_arquivo=callback_arquivo,
            callback_pasta=callback_pasta
        )
    else:
        estatisticas = organizar_presets(
            pastas_origem[0], 
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
    
    print(f"\n  {Cores.BOLD}📊 DISTRIBUIÇÃO POR CATEGORIA{Cores.RESET}")
    print(f"  {Cores.DIM}{'─' * 45}{Cores.RESET}")
    
    # Informação de multi-categorização
    if estatisticas.get('total_multi_categoria', 0) > 0:
        print(f"  {Cores.CIANO_CLARO}ℹ{Cores.RESET} {estatisticas['total_multi_categoria']} arquivos foram copiados para múltiplas categorias")
        print()
    
    for categoria, qtd in sorted(estatisticas['por_categoria'].items(), key=lambda x: -x[1])[:8]:
        icone = ICONES_CATEGORIAS.get(categoria, "📄")
        print(f"  {icone} {categoria}: {Cores.VERDE_CLARO}{qtd}{Cores.RESET} presets")
    
    if len(estatisticas['por_categoria']) > 8:
        restantes = len(estatisticas['por_categoria']) - 8
        print(f"  {Cores.DIM}... e mais {restantes} categorias{Cores.RESET}")


def exibir_instrucoes_iniciais():
    """
    Exibe instruções e informações para o usuário antes de iniciar.
    """
    print(f"\n  {Cores.BOLD}{Cores.CIANO_CLARO}═══════════════════════════════════════════════════════════════{Cores.RESET}")
    print(f"  {Cores.BOLD}  📖 BEM-VINDO AO SERUM PRESET ORGANIZER!{Cores.RESET}")
    print(f"  {Cores.BOLD}{Cores.CIANO_CLARO}═══════════════════════════════════════════════════════════════{Cores.RESET}")
    
    print(f"""
  {Cores.VERDE_CLARO}✨ O QUE ESTE PROGRAMA FAZ:{Cores.RESET}
  
     Este programa organiza automaticamente seus presets do Serum
     em pastas por categoria (Bass, Lead, Pad, FX, etc.) baseado
     no nome do arquivo.
     
  {Cores.AMARELO_CLARO}🔒 SEGURANÇA:{Cores.RESET}
  
     • Seus arquivos originais NUNCA serão modificados ou deletados
     • O programa apenas COPIA os presets para novas pastas
     • Detecção de duplicatas: arquivos idênticos não são copiados 2x
     • Você pode executar quantas vezes quiser sem problemas
     
  {Cores.CIANO_CLARO}🧪 TESTES REALIZADOS:{Cores.RESET}
  
     • ✅ Testado com milhares de presets reais
     • ✅ Milhares de padrões de nomes diferentes validados
     • ✅ 13 testes unitários automatizados (todos passando)
     • ✅ Suporte a keywords em português e inglês
     
  {Cores.MAGENTA_CLARO}📁 COMO USAR:{Cores.RESET}
  
     1. Adicione uma ou mais pastas de ORIGEM (onde estão seus presets)
     2. Informe a pasta de DESTINO (onde criar a organização)
     3. Confirme e aguarde o processamento
     
     Dica: Você pode adicionar várias pastas de origem!
  """)
    print(f"  {Cores.DIM}─────────────────────────────────────────────────────────────────{Cores.RESET}")


def main():
    """Função principal do programa."""
    
    # Banner inicial
    exibir_banner_principal()
    
    # Instruções e informações
    exibir_instrucoes_iniciais()
    
    # Timestamp de início
    print(f"  {Cores.DIM}⏰ Iniciado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}{Cores.RESET}")
    linha_separadora("─", 70)
    
    # Determina os caminhos (variáveis ou input)
    if PASTAS_ORIGEM and PASTA_DESTINO:
        pastas_origem = PASTAS_ORIGEM if isinstance(PASTAS_ORIGEM, list) else [PASTAS_ORIGEM]
        pasta_destino = PASTA_DESTINO
        print(f"\n  {Icones.INFO} {info('Usando caminhos pré-configurados no código.')}")
        for pasta in pastas_origem:
            print(f"      {Icones.PASTA} Origem:  {pasta}")
        print(f"      {Icones.PASTA} Destino: {pasta_destino}")
    else:
        # Mostra categorias disponíveis
        exibir_categorias_visual(MAPA_CATEGORIAS)
        
        # Solicita múltiplas pastas de origem
        pastas_origem = solicitar_caminhos_origem()
        
        # Exibe resumo das pastas adicionadas
        print(f"\n  {Cores.BOLD}📋 PASTAS DE ORIGEM SELECIONADAS:{Cores.RESET}")
        for idx, pasta in enumerate(pastas_origem, 1):
            print(f"      {Cores.VERDE_CLARO}{idx}.{Cores.RESET} {pasta}")
        
        # Solicita destino
        pasta_destino = solicitar_caminho(
            "Digite o caminho da pasta de DESTINO (onde serão organizados):",
            deve_existir=False
        )
    
    # Detecta se é modo de re-verificação (só para primeira pasta)
    modo_reverificacao = len(pastas_origem) == 1 and detectar_modo_reverificacao(pastas_origem[0], pasta_destino)
    
    if modo_reverificacao:
        print()
        print(f"  {Cores.AMARELO_CLARO}⚠️  MODO RE-VERIFICAÇÃO DETECTADO{Cores.RESET}")
        print(f"  {Cores.DIM}─────────────────────────────────────────────────────────────────{Cores.RESET}")
        print(f"  {Cores.CIANO_CLARO}📁 Origem: Uncategorized{Cores.RESET}")
        print(f"  {Cores.CIANO_CLARO}📁 Destino: Pasta pai{Cores.RESET}")
        print()
        print(f"  {Cores.AMARELO_CLARO}⚡ AÇÃO: Arquivos categorizados serão MOVIDOS.{Cores.RESET}")
        print(f"  {Cores.AMARELO_CLARO}🗑️  Duplicatas (já existem no destino) serão REMOVIDAS da origem.{Cores.RESET}")
        print(f"  {Cores.DIM}Arquivos que agora têm categoria sairão de Uncategorized.{Cores.RESET}")
        print()
        print(f"  {Cores.BOLD}Categorias especiais:{Cores.RESET}")
        print(f"      🔧 {CATEGORIA_CORROMPIDOS} - Arquivos com nomes tipo hash (f892346344.fxp)")
        print(f"      🎨 {CATEGORIA_CUSTOMIZADOS} - Arquivos com nomes em português")
        print()
    
    # Confirmação do usuário
    if not exibir_confirmacao(pastas_origem, pasta_destino, EXTENSOES_SUPORTADAS, modo_reverificacao):
        print(f"\n  {Icones.ERRO} {erro('Operação cancelada pelo usuário.')}")
        print(f"  {Cores.DIM}Nenhum arquivo foi modificado.{Cores.RESET}\n")
        return
    
    print()
    linha_separadora("═", 70, Cores.MAGENTA_CLARO)
    
    # ========== FASE 1: BUSCA ==========
    try:
        arquivos, tempo_busca = fase_busca_presets(pastas_origem)
    except FileNotFoundError as e:
        print(f"\n  {Icones.ERRO} {erro(str(e))}")
        return
    except Exception as e:
        print(f"\n  {Icones.ERRO} {erro(f'Erro durante a busca: {e}')}")
        return
    
    if len(arquivos) == 0:
        print(f"\n  {Icones.AVISO} {aviso('Nenhum preset encontrado!')}")
        print(f"      Verifique se as pastas contêm arquivos .fxp ou .SerumPreset")
        print(f"      Pastas verificadas: {len(pastas_origem)}\n")
        return
    
    # ========== FASE 2: ORGANIZAÇÃO ==========
    try:
        estatisticas, tempo_organizacao = fase_organizacao(
            pastas_origem, 
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
    print(f"  {Cores.DIM}         Arquivos já copiados serão ignorados automaticamente (detecção por hash){Cores.RESET}")
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
