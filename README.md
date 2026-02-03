# 🎹 Serum Preset Organizer

Automatize a organização da sua biblioteca de presets do sintetizador **Xfer Serum**, categorizando automaticamente por tipo de instrumento.

## ✨ Funcionalidades

- 🔍 **Busca recursiva** em todas as subpastas
- 📁 **Organização automática** por categoria (Bass, Lead, Pad, etc.)
- 🏷️ **Detecção inteligente** baseada em keywords no nome do arquivo
- 🔒 **100% seguro**: apenas copia arquivos, nunca move ou deleta
- 🔄 **Tratamento de duplicatas**: renomeia automaticamente para evitar sobrescrita
- 📊 **Relatório detalhado** após execução

## 📂 Categorias Suportadas

| Categoria | Keywords Detectadas |
|-----------|---------------------|
| Bass | bass, bs, 808, sub, growl, reese, wobble... |
| Lead | lead, ld, solo, hook, main, melody... |
| Pluck | pluck, pl, pizz, staccato... |
| Piano/Keys | piano, keys, organ, rhodes, clav... |
| Pad | pad, atmosphere, drone, ambient... |
| Synth | synth, poly, saw, analog, vintage... |
| Drums | drum, kick, snare, clap, hat, perc... |
| Arp/Seq | arp, seq, sequence, pattern... |
| FX | fx, noise, riser, impact, sweep... |
| Vocals | vox, vocal, choir, voice... |
| Strings/Orch | string, violin, orch, brass, flute... |
| Chords | chord, stab, harmonic... |
| Uncategorized | (arquivos não classificados) |

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Serum-File-Sorter-Organizer.git
cd Serum-File-Sorter-Organizer
```

2. Não requer dependências externas - usa apenas biblioteca padrão do Python 3.6+

## 💻 Uso

### Modo Interativo (Recomendado)
```bash
python main.py
```
O script solicitará os caminhos via terminal.

### Modo Configurado
Edite as variáveis no topo do arquivo `main.py`:
```python
PASTA_ORIGEM = "C:/Users/SeuNome/Downloads/Serum Presets"
PASTA_DESTINO = "C:/Users/SeuNome/Documents/Serum Organized"
MODO_VERBOSE = True  # True = mostra cada arquivo, False = apenas barra de progresso
```

## 📁 Estrutura do Projeto

```
Serum-File-Sorter-Organizer/
├── main.py                 # Script principal (ponto de entrada)
├── config.py               # Configurações e mapeamento de categorias
├── categorizador.py        # Lógica de identificação de categoria
├── manipulador_arquivos.py # Funções de busca e cópia de arquivos
├── interface_visual.py     # Interface colorida e formatação de terminal
├── tests.py                # Testes unitários
├── README.md               # Documentação
└── LICENSE                 # Licença do projeto
```

## 🧪 Executando Testes

```bash
python tests.py
```

Ou com pytest:
```bash
python -m pytest tests.py -v
```

## 📋 Exemplo de Saída

O programa exibe uma interface rica e colorida no terminal:

```
╔═══════════════════════════════════════════════════════════════════╗
║   ███████╗███████╗██████╗ ██╗   ██╗███╗   ███╗                    ║
║   ██╔════╝██╔════╝██╔══██╗██║   ██║████╗ ████║                    ║
║   ███████╗█████╗  ██████╔╝██║   ██║██╔████╔██║                    ║
║   ╚════██║██╔══╝  ██╔══██╗██║   ██║██║╚██╔╝██║                    ║
║   ███████║███████╗██║  ██║╚██████╔╝██║ ╚═╝ ██║                    ║
║          🎹  P R E S E T   O R G A N I Z E R  🎹                  ║
╚═══════════════════════════════════════════════════════════════════╝

  ╭────────────────────────────────────────────────────────────╮
  │ FASE 2: ORGANIZANDO PRESETS
  │ Copiando e categorizando 1247 arquivos...
  ╰────────────────────────────────────────────────────────────╯

  [   1/1247] 🔊 → Bass          │ Deep_Sub_Wobble.fxp
  [   2/1247] 🎸 → Lead          │ Epic_Screamer.fxp
  [   3/1247] 🌊 → Pad           │ Lush_Atmosphere.serumpreset
  [   4/1247] 🔊 → Bass          │ 808_Hard_Hit.fxp (renomeado)
  ...

═══════════════════════════════════════════════════════════════════

           OPERAÇÃO CONCLUÍDA
     Processamento finalizado em 2.35 segundos

  📊 ESTATÍSTICAS GERAIS
  ──────────────────────────────────────────────────
  📄  Total de presets processados: 1247
  🔄  Duplicatas renomeadas:        23
  ⏱️   Tempo de execução:           2.35s

  📁 DISTRIBUIÇÃO POR CATEGORIA
  ──────────────────────────────────────────────────
  🔊 Bass               342 █████████████████████████ (27.4%)
  🎸 Lead               256 ███████████████████ (20.5%)
  🌊 Pad                189 ██████████████ (15.1%)
  ✨ FX                 156 ███████████ (12.5%)
  🎛️ Synth              98 ███████ (7.9%)
  ...

═══════════════════════════════════════════════════════════════════

  🎉 Seus presets foram organizados com sucesso!
  📁 Pasta de destino: C:/Users/SeuNome/Documents/Serum Organized
```

## ⚙️ Personalizando Categorias

Edite o arquivo `config.py` para adicionar/remover categorias ou keywords:

```python
MAPA_CATEGORIAS = {
    "MinhaCategoria": ["keyword1", "keyword2", "keyword3"],
    # ...
}
```

## 🔒 Segurança

- ✅ Arquivos originais **nunca são modificados**
- ✅ Usa `shutil.copy2` para preservar metadados
- ✅ Duplicatas são **renomeadas**, não sobrescritas
- ✅ Validação de caminhos antes de executar

## 📄 Extensões Suportadas

- `.fxp` - Preset padrão do Serum
- `.SerumPreset` - Formato alternativo

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Feito com ❤️ para produtores musicais**
