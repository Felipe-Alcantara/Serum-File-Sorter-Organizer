# -*- coding: utf-8 -*-
"""
Módulo de Interface Visual - Serum Preset Organizer
=====================================================
Contém funções para exibição formatada no terminal com cores e estilos.
"""

import os
import sys
import time
from datetime import datetime


# ============================================================================
# CONFIGURAÇÃO DE CORES ANSI (Funciona no Windows 10+ e Linux/Mac)
# ============================================================================

class Cores:
    """Códigos ANSI para colorir texto no terminal."""
    
    # Cores básicas
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Cores de texto
    PRETO = "\033[30m"
    VERMELHO = "\033[31m"
    VERDE = "\033[32m"
    AMARELO = "\033[33m"
    AZUL = "\033[34m"
    MAGENTA = "\033[35m"
    CIANO = "\033[36m"
    BRANCO = "\033[37m"
    
    # Cores brilhantes
    VERMELHO_CLARO = "\033[91m"
    VERDE_CLARO = "\033[92m"
    AMARELO_CLARO = "\033[93m"
    AZUL_CLARO = "\033[94m"
    MAGENTA_CLARO = "\033[95m"
    CIANO_CLARO = "\033[96m"
    
    # Cores de fundo
    BG_VERDE = "\033[42m"
    BG_AZUL = "\033[44m"
    BG_MAGENTA = "\033[45m"


def habilitar_cores_windows():
    """Habilita suporte a cores ANSI no Windows."""
    if os.name == 'nt':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass


# Habilita cores ao importar o módulo
habilitar_cores_windows()


# ============================================================================
# SÍMBOLOS E ÍCONES
# ============================================================================

class Icones:
    """Ícones Unicode para decoração do terminal."""
    
    # Status
    SUCESSO = "✅"
    ERRO = "❌"
    AVISO = "⚠️"
    INFO = "ℹ️"
    PROCESSANDO = "⏳"
    CONCLUIDO = "🎉"
    
    # Arquivos e pastas
    PASTA = "📁"
    ARQUIVO = "📄"
    MUSICA = "🎵"
    PRESET = "🎹"
    
    # Ações
    COPIAR = "📋"
    BUSCAR = "🔍"
    ORGANIZAR = "📂"
    DUPLICATA = "🔄"
    
    # Categorias musicais
    BASS = "🔊"
    LEAD = "🎸"
    PAD = "🌊"
    DRUMS = "🥁"
    FX = "✨"
    VOCAL = "🎤"
    KEYS = "🎹"
    SYNTH = "🎛️"
    
    # Progresso
    BARRA_CHEIA = "█"
    BARRA_VAZIA = "░"
    SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


# Mapeamento de categoria para ícone
ICONES_CATEGORIAS = {
    "Bass": Icones.BASS,
    "Lead": Icones.LEAD,
    "Pad": Icones.PAD,
    "Drums": Icones.DRUMS,
    "FX": Icones.FX,
    "Vocals": Icones.VOCAL,
    "Piano_Keys": Icones.KEYS,
    "Synth": Icones.SYNTH,
    "Pluck": "🎯",
    "Arp_Seq": "🔁",
    "Strings_Orch": "🎻",
    "Chords": "🎶",
    "Uncategorized": "❓"
}


# ============================================================================
# FUNÇÕES DE FORMATAÇÃO
# ============================================================================

def colorir(texto: str, cor: str, negrito: bool = False) -> str:
    """
    Aplica cor a um texto.
    
    Args:
        texto: Texto a colorir
        cor: Código de cor da classe Cores
        negrito: Se True, aplica negrito também
        
    Returns:
        Texto formatado com códigos ANSI
    """
    prefixo = Cores.BOLD if negrito else ""
    return f"{prefixo}{cor}{texto}{Cores.RESET}"


def sucesso(texto: str) -> str:
    """Formata texto como mensagem de sucesso (verde)."""
    return colorir(texto, Cores.VERDE_CLARO, negrito=True)


def erro(texto: str) -> str:
    """Formata texto como mensagem de erro (vermelho)."""
    return colorir(texto, Cores.VERMELHO_CLARO, negrito=True)


def aviso(texto: str) -> str:
    """Formata texto como mensagem de aviso (amarelo)."""
    return colorir(texto, Cores.AMARELO_CLARO)


def info(texto: str) -> str:
    """Formata texto como mensagem informativa (ciano)."""
    return colorir(texto, Cores.CIANO_CLARO)


def destaque(texto: str) -> str:
    """Formata texto com destaque (magenta negrito)."""
    return colorir(texto, Cores.MAGENTA_CLARO, negrito=True)


def dim(texto: str) -> str:
    """Formata texto como secundário/dim."""
    return f"{Cores.DIM}{texto}{Cores.RESET}"


# ============================================================================
# COMPONENTES VISUAIS
# ============================================================================

def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def linha_separadora(caractere: str = "─", tamanho: int = 70, cor: str = Cores.CIANO):
    """Imprime uma linha separadora decorativa."""
    print(f"{cor}{caractere * tamanho}{Cores.RESET}")


def cabecalho(titulo: str, subtitulo: str = ""):
    """
    Exibe um cabeçalho estilizado.
    
    Args:
        titulo: Título principal
        subtitulo: Subtítulo opcional
    """
    largura = 70
    print()
    print(f"{Cores.CIANO}{Cores.BOLD}╔{'═' * (largura - 2)}╗{Cores.RESET}")
    
    # Título centralizado
    titulo_formatado = titulo.center(largura - 4)
    print(f"{Cores.CIANO}║{Cores.RESET} {Cores.BOLD}{Cores.AMARELO_CLARO}{titulo_formatado}{Cores.RESET} {Cores.CIANO}║{Cores.RESET}")
    
    if subtitulo:
        subtitulo_formatado = subtitulo.center(largura - 4)
        print(f"{Cores.CIANO}║{Cores.RESET} {Cores.DIM}{subtitulo_formatado}{Cores.RESET} {Cores.CIANO}║{Cores.RESET}")
    
    print(f"{Cores.CIANO}{Cores.BOLD}╚{'═' * (largura - 2)}╝{Cores.RESET}")
    print()


def caixa_info(titulo: str, linhas: list, icone: str = "📋"):
    """
    Exibe uma caixa de informações estilizada.
    
    Args:
        titulo: Título da caixa
        linhas: Lista de linhas de texto
        icone: Ícone para o título
    """
    largura = 68
    
    print(f"\n{Cores.AZUL_CLARO}┌{'─' * largura}┐{Cores.RESET}")
    print(f"{Cores.AZUL_CLARO}│{Cores.RESET} {icone} {Cores.BOLD}{titulo}{Cores.RESET}{' ' * (largura - len(titulo) - 4)}{Cores.AZUL_CLARO}│{Cores.RESET}")
    print(f"{Cores.AZUL_CLARO}├{'─' * largura}┤{Cores.RESET}")
    
    for linha in linhas:
        # Remove códigos ANSI para calcular o padding corretamente
        texto_limpo = linha
        for attr in dir(Cores):
            if not attr.startswith('_'):
                texto_limpo = texto_limpo.replace(getattr(Cores, attr), '')
        
        padding = largura - len(texto_limpo) - 1
        print(f"{Cores.AZUL_CLARO}│{Cores.RESET} {linha}{' ' * max(0, padding)}{Cores.AZUL_CLARO}│{Cores.RESET}")
    
    print(f"{Cores.AZUL_CLARO}└{'─' * largura}┘{Cores.RESET}\n")


def barra_progresso(atual: int, total: int, largura: int = 40, prefixo: str = "", sufixo: str = "") -> str:
    """
    Gera uma barra de progresso visual.
    
    Args:
        atual: Valor atual
        total: Valor total
        largura: Largura da barra em caracteres
        prefixo: Texto antes da barra
        sufixo: Texto depois da barra
        
    Returns:
        String formatada com a barra de progresso
    """
    if total == 0:
        porcentagem = 100
    else:
        porcentagem = (atual / total) * 100
    
    preenchido = int(largura * atual / total) if total > 0 else largura
    vazio = largura - preenchido
    
    # Cores baseadas na porcentagem
    if porcentagem < 33:
        cor = Cores.VERMELHO_CLARO
    elif porcentagem < 66:
        cor = Cores.AMARELO_CLARO
    else:
        cor = Cores.VERDE_CLARO
    
    barra = f"{cor}{Icones.BARRA_CHEIA * preenchido}{Cores.DIM}{Icones.BARRA_VAZIA * vazio}{Cores.RESET}"
    
    return f"{prefixo} [{barra}] {porcentagem:5.1f}% {sufixo}"


def atualizar_linha(texto: str):
    """
    Atualiza a linha atual do terminal (sem criar nova linha).
    
    Args:
        texto: Texto a exibir
    """
    sys.stdout.write(f"\r{texto}")
    sys.stdout.flush()


def spinner_animado(frame: int) -> str:
    """
    Retorna o caractere atual do spinner animado.
    
    Args:
        frame: Número do frame atual
        
    Returns:
        Caractere do spinner
    """
    return Icones.SPINNER[frame % len(Icones.SPINNER)]


# ============================================================================
# FUNÇÕES DE LOG
# ============================================================================

def log_arquivo_processado(arquivo: str, categoria: str, duplicata: bool = False, contador: int = 0, total: int = 0):
    """
    Exibe log formatado de arquivo processado.
    
    Args:
        arquivo: Nome do arquivo
        categoria: Categoria identificada
        duplicata: Se o arquivo foi renomeado por duplicata
        contador: Número atual
        total: Total de arquivos
    """
    icone_categoria = ICONES_CATEGORIAS.get(categoria, "📄")
    
    # Trunca nome se muito longo
    nome_display = arquivo if len(arquivo) <= 40 else arquivo[:37] + "..."
    
    # Monta a linha de log
    num_info = f"[{contador:4d}/{total:4d}]" if total > 0 else ""
    
    status = ""
    if duplicata:
        status = f" {Cores.AMARELO_CLARO}(renomeado){Cores.RESET}"
    
    linha = (
        f"  {Cores.DIM}{num_info}{Cores.RESET} "
        f"{icone_categoria} {Cores.VERDE_CLARO}→{Cores.RESET} "
        f"{colorir(categoria, Cores.CIANO_CLARO):20} "
        f"{Cores.DIM}│{Cores.RESET} {nome_display}{status}"
    )
    
    print(linha)


def log_erro_arquivo(arquivo: str, erro_msg: str, contador: int = 0):
    """
    Exibe log formatado de erro em arquivo.
    
    Args:
        arquivo: Nome do arquivo
        erro_msg: Mensagem de erro
        contador: Número do arquivo
    """
    nome_display = arquivo if len(arquivo) <= 35 else arquivo[:32] + "..."
    
    print(
        f"  {Cores.VERMELHO_CLARO}{Icones.ERRO}{Cores.RESET} "
        f"[{contador:4d}] "
        f"{nome_display} "
        f"{Cores.DIM}│{Cores.RESET} {Cores.VERMELHO}{erro_msg}{Cores.RESET}"
    )


def log_fase(numero: int, titulo: str, descricao: str = ""):
    """
    Exibe início de uma fase do processo.
    
    Args:
        numero: Número da fase
        titulo: Título da fase
        descricao: Descrição opcional
    """
    print()
    print(f"  {Cores.BOLD}{Cores.MAGENTA_CLARO}╭{'─' * 60}╮{Cores.RESET}")
    print(f"  {Cores.MAGENTA_CLARO}│{Cores.RESET} {Cores.BOLD}FASE {numero}:{Cores.RESET} {destaque(titulo)}")
    if descricao:
        print(f"  {Cores.MAGENTA_CLARO}│{Cores.RESET} {dim(descricao)}")
    print(f"  {Cores.MAGENTA_CLARO}╰{'─' * 60}╯{Cores.RESET}")
    print()


def log_resumo_busca(total_encontrado: int, extensoes: list, tempo: float):
    """
    Exibe resumo da fase de busca.
    
    Args:
        total_encontrado: Total de arquivos encontrados
        extensoes: Extensões buscadas
        tempo: Tempo de execução
    """
    print()
    print(f"  {Icones.SUCESSO} {sucesso('Busca concluída!')}")
    print(f"     {Icones.ARQUIVO} Arquivos encontrados: {Cores.BOLD}{total_encontrado}{Cores.RESET}")
    print(f"     {Icones.BUSCAR} Extensões: {', '.join(extensoes)}")
    print(f"     ⏱️  Tempo: {tempo:.2f}s")
    print()


def exibir_banner_principal():
    """Exibe o banner principal do programa."""
    banner = f"""
{Cores.CIANO_CLARO}{Cores.BOLD}
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   {Cores.AMARELO_CLARO}███████╗███████╗██████╗ ██╗   ██╗███╗   ███╗{Cores.CIANO_CLARO}                    ║
    ║   {Cores.AMARELO_CLARO}██╔════╝██╔════╝██╔══██╗██║   ██║████╗ ████║{Cores.CIANO_CLARO}                    ║
    ║   {Cores.AMARELO_CLARO}███████╗█████╗  ██████╔╝██║   ██║██╔████╔██║{Cores.CIANO_CLARO}                    ║
    ║   {Cores.AMARELO_CLARO}╚════██║██╔══╝  ██╔══██╗██║   ██║██║╚██╔╝██║{Cores.CIANO_CLARO}                    ║
    ║   {Cores.AMARELO_CLARO}███████║███████╗██║  ██║╚██████╔╝██║ ╚═╝ ██║{Cores.CIANO_CLARO}                    ║
    ║   {Cores.AMARELO_CLARO}╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝{Cores.CIANO_CLARO}                    ║
    ║                                                                   ║
    ║          {Cores.BRANCO}🎹  P R E S E T   O R G A N I Z E R  🎹{Cores.CIANO_CLARO}               ║
    ║                                                                   ║
    ║   {Cores.DIM}Organize sua biblioteca de presets do Serum{Cores.CIANO_CLARO}                  ║
    ║   {Cores.DIM}de forma automática e inteligente{Cores.CIANO_CLARO}                            ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
{Cores.RESET}
"""
    print(banner)


def exibir_categorias_visual(mapa_categorias: dict):
    """
    Exibe as categorias disponíveis de forma visual.
    
    Args:
        mapa_categorias: Dicionário de categorias e keywords
    """
    print(f"\n  {Cores.BOLD}{Icones.ORGANIZAR} CATEGORIAS DISPONÍVEIS{Cores.RESET}")
    print(f"  {Cores.DIM}{'─' * 60}{Cores.RESET}\n")
    
    for categoria, keywords in mapa_categorias.items():
        icone = ICONES_CATEGORIAS.get(categoria, "📄")
        keywords_preview = ", ".join(keywords[:4])
        if len(keywords) > 4:
            keywords_preview += f" {Cores.DIM}(+{len(keywords) - 4} mais){Cores.RESET}"
        
        print(f"  {icone} {colorir(categoria, Cores.CIANO_CLARO, negrito=True):25} {Cores.DIM}│{Cores.RESET} {keywords_preview}")
    
    print(f"\n  {ICONES_CATEGORIAS['Uncategorized']} {colorir('Uncategorized', Cores.AMARELO_CLARO):25} {Cores.DIM}│{Cores.RESET} {dim('(arquivos não classificados)')}")
    print(f"  {Cores.DIM}{'─' * 60}{Cores.RESET}\n")


def exibir_confirmacao(pasta_origem: str, pasta_destino: str, extensoes: list, modo_mover: bool = False) -> bool:
    """
    Exibe painel de confirmação antes de iniciar.
    
    Args:
        pasta_origem: Caminho da origem
        pasta_destino: Caminho do destino
        extensoes: Lista de extensões
        modo_mover: Se True, indica que está no modo re-verificação (mover)
        
    Returns:
        True se confirmado
    """
    if modo_mover:
        acao_texto = f"{Cores.AMARELO_CLARO}Os arquivos serão MOVIDOS/LIMPOS da origem{Cores.RESET}"
    else:
        acao_texto = f"{Cores.DIM}Os arquivos serão COPIADOS (originais intactos){Cores.RESET}"
    
    linhas = [
        f"{Cores.VERDE_CLARO}📂 Origem:{Cores.RESET}  {pasta_origem}",
        f"{Cores.AZUL_CLARO}📂 Destino:{Cores.RESET} {pasta_destino}",
        f"{Cores.AMARELO_CLARO}📄 Extensões:{Cores.RESET} {', '.join(extensoes)}",
        "",
        acao_texto
    ]
    
    caixa_info("RESUMO DA OPERAÇÃO", linhas, "📋")
    
    print(f"  {Icones.AVISO} {aviso('Deseja continuar com a organização?')}")
    resposta = input(f"  {Cores.BOLD}Digite [S] para Sim ou [N] para Não:{Cores.RESET} ").strip().lower()
    
    return resposta in ['s', 'sim', 'y', 'yes']


def exibir_resultado_final(estatisticas: dict, tempo_execucao: float, pasta_destino: str):
    """
    Exibe o resultado final da operação de forma detalhada.
    
    Args:
        estatisticas: Dicionário com estatísticas
        tempo_execucao: Tempo total de execução
        pasta_destino: Pasta de destino
    """
    # Compatibilidade com novo e antigo formato de estatísticas
    total_origem = estatisticas.get('total_arquivos_origem', estatisticas.get('total_processados', 0))
    total_copias = estatisticas.get('total_copias_realizadas', total_origem)
    duplicatas_ignoradas = estatisticas.get('total_duplicatas_ignoradas', 0)
    multi_categoria = estatisticas.get('total_multi_categoria', 0)
    total_deletados = estatisticas.get('total_deletados_origem', 0)
    modo_mover = estatisticas.get('modo_mover', False)
    erros = len(estatisticas.get('erros', []))
    
    # Cabeçalho do resultado
    print()
    cabecalho("OPERAÇÃO CONCLUÍDA", f"Processamento finalizado em {tempo_execucao:.2f} segundos")
    
    # Estatísticas gerais
    print(f"  {Cores.BOLD}📊 ESTATÍSTICAS GERAIS{Cores.RESET}")
    print(f"  {Cores.DIM}{'─' * 50}{Cores.RESET}")
    print(f"  {Icones.ARQUIVO}  Arquivos analisados:          {Cores.BOLD}{Cores.VERDE_CLARO}{total_origem}{Cores.RESET}")
    
    if modo_mover:
        print(f"  🚀  Arquivos movidos:             {Cores.BOLD}{Cores.VERDE_CLARO}{total_copias}{Cores.RESET}")
        if total_deletados > 0:
            print(f"  🗑️   Duplicatas limpas da origem: {Cores.BOLD}{Cores.AMARELO_CLARO}{total_deletados}{Cores.RESET}")
    else:
        print(f"  📋  Cópias realizadas:           {Cores.BOLD}{Cores.VERDE_CLARO}{total_copias}{Cores.RESET}")
    
    if duplicatas_ignoradas > 0:
        print(f"  {Icones.DUPLICATA}  Duplicatas ignoradas (hash):  {Cores.BOLD}{Cores.AMARELO_CLARO}{duplicatas_ignoradas}{Cores.RESET}")
    
    if multi_categoria > 0:
        print(f"  🔀  Multi-categoria:             {Cores.BOLD}{Cores.CIANO_CLARO}{multi_categoria}{Cores.RESET} arquivos em múltiplas pastas")
    
    if erros > 0:
        print(f"  {Icones.ERRO}  Erros encontrados:           {Cores.BOLD}{Cores.VERMELHO_CLARO}{erros}{Cores.RESET}")
    print(f"  ⏱️   Tempo de execução:          {Cores.BOLD}{tempo_execucao:.2f}s{Cores.RESET}")
    
    # Distribuição por categoria
    if estatisticas['por_categoria']:
        print(f"\n  {Cores.BOLD}📁 DISTRIBUIÇÃO POR CATEGORIA{Cores.RESET}")
        print(f"  {Cores.DIM}{'─' * 50}{Cores.RESET}")
        
        # Ordena por quantidade
        categorias_ordenadas = sorted(
            estatisticas['por_categoria'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        max_qtd = max(estatisticas['por_categoria'].values()) if estatisticas['por_categoria'] else 1
        total_refs = sum(estatisticas['por_categoria'].values())
        
        for categoria, quantidade in categorias_ordenadas:
            icone = ICONES_CATEGORIAS.get(categoria, "📄")
            
            # Barra proporcional
            barra_tam = int((quantidade / max_qtd) * 25)
            barra = f"{Cores.VERDE_CLARO}{Icones.BARRA_CHEIA * barra_tam}{Cores.RESET}"
            
            # Porcentagem
            pct = (quantidade / total_refs * 100) if total_refs > 0 else 0
            
            print(f"  {icone} {categoria:18} {quantidade:5} {barra} {Cores.DIM}({pct:.1f}%){Cores.RESET}")
    
    # Erros (se houver)
    if estatisticas.get('erros'):
        print(f"\n  {Cores.BOLD}{Cores.VERMELHO_CLARO}⚠️ ERROS ENCONTRADOS{Cores.RESET}")
        print(f"  {Cores.DIM}{'─' * 50}{Cores.RESET}")
        for i, erro_info in enumerate(estatisticas['erros'][:5], 1):
            nome_arquivo = os.path.basename(erro_info['arquivo'])
            if len(nome_arquivo) > 30:
                nome_arquivo = nome_arquivo[:27] + "..."
            print(f"  {i}. {Cores.DIM}{nome_arquivo}{Cores.RESET}")
            print(f"     {Cores.VERMELHO}{erro_info['erro']}{Cores.RESET}")
        
        if len(estatisticas['erros']) > 5:
            print(f"  {Cores.DIM}... e mais {len(estatisticas['erros']) - 5} erros{Cores.RESET}")
    
    # Mensagem final
    print()
    linha_separadora("═", 70, Cores.VERDE_CLARO)
    
    if total_copias > 0:
        print(f"\n  {Icones.CONCLUIDO} {sucesso('Seus presets foram organizados com sucesso!')}")
        print(f"  {Icones.PASTA} {info('Pasta de destino:')} {pasta_destino}")
    elif duplicatas_ignoradas > 0:
        print(f"\n  {Icones.INFO} {info('Todos os arquivos já existem no destino.')}")
        print(f"     Nenhuma cópia foi necessária (detecção por hash).")
    else:
        print(f"\n  {Icones.AVISO} {aviso('Nenhum preset foi encontrado na pasta de origem.')}")
        print(f"     Verifique se o caminho está correto e se há arquivos .fxp ou .SerumPreset")
    
    print()


def exibir_progresso_tempo_real(mensagem: str, atual: int, total: int):
    """
    Atualiza o progresso em tempo real na mesma linha.
    
    Args:
        mensagem: Mensagem de status
        atual: Valor atual
        total: Valor total
    """
    barra = barra_progresso(atual, total, largura=30)
    atualizar_linha(f"  {barra} {mensagem}")


def animacao_processando(texto: str = "Processando", duracao: float = 0.5):
    """
    Exibe uma pequena animação de processamento.
    
    Args:
        texto: Texto a exibir
        duracao: Duração da animação
    """
    frames = len(Icones.SPINNER)
    inicio = time.time()
    
    while time.time() - inicio < duracao:
        for i in range(frames):
            if time.time() - inicio >= duracao:
                break
            spinner = f"{Cores.CIANO_CLARO}{Icones.SPINNER[i]}{Cores.RESET}"
            atualizar_linha(f"  {spinner} {texto}...")
            time.sleep(0.08)
    
    print()  # Nova linha ao final
