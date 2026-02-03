# 🎹 Serum Preset Organizer

Automatize a organização da sua biblioteca de presets do sintetizador **Xfer Serum**, categorizando automaticamente por tipo de instrumento.

> ✅ **Testado com milhares de presets** e milhares de padrões de nomes diferentes para garantir precisão máxima na categorização.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 🔍 **Busca recursiva** | Encontra presets em todas as subpastas |
| 📁 **Organização automática** | Categoriza por tipo (Bass, Lead, Pad, etc.) |
| 🏷️ **Detecção inteligente** | Analisa keywords no nome do arquivo |
| 🔀 **Multi-categorização** | Arquivos podem ir para múltiplas categorias |
| 🔒 **Modo seguro** | Copia por padrão, move apenas em re-verificação |
| 🔄 **Detecção de duplicatas** | Hash MD5 evita cópias desnecessárias |
| 🎵 **Ignora gêneros** | "Future Bass" não categoriza como Bass |
| 📊 **Relatório visual** | Interface colorida com estatísticas |

---

## 📂 Categorias Suportadas

O programa reconhece **16 categorias** de instrumentos:

| Categoria | Exemplos de Keywords |
|-----------|---------------------|
| **Bass** | bass, 808, sub, growl, reese, wobble, lowend, rps |
| **Lead** | lead, solo, hook, melody, screamer, mono |
| **Pluck** | pluck, pizz, staccato, mallet, marimba |
| **Bell** | bell, chime, glockenspiel, tinkle |
| **Piano/Keys** | piano, keys, organ, rhodes, clav, wurlitzer |
| **Pad** | pad, atmosphere, drone, ambient, texture |
| **Synth** | synth, poly, analog, vintage, supersaw |
| **Acid** | acid, 303, tb303, squelch |
| **Zap** | zap, laser, pew |
| **Drums** | drum, kick, snare, clap, hat, perc, timpani |
| **Arp/Seq** | arp, sequence, pattern, arpeggio, gate |
| **FX** | sfx, noise, riser, impact, sweep, whoosh, glitch |
| **Vocals** | vocal, vox, choir, voice, formant |
| **Strings/Orch** | string, violin, brass, flute, cinematic, ensemble |
| **Chords** | chord, stab, harmonic |
| **Guitar** | guitar, acoustic, electric |
| **Dubstep** | dubstep, riddim, tearout, wub |
| **Arquivos_Corrompidos** | *(Nomes hexadecimais/hash)* |
| **Customizados** | *(Nomes em português)* |

---

## 🎵 Tratamento Inteligente

### Gêneros Musicais
O programa ignora nomes de gêneros para evitar falsos positivos:
- ✅ "Future Bass Lead 01" → Categoria: **Lead** (não Bass)
- ✅ "Drum and Bass Reese" → Categoria: **Bass** (não Drum)
- ✅ "Dubstep Growl" → Categoria: **Bass**

### Keywords Curtas
Keywords de 2-3 caracteres usam detecção por word boundary:
- ✅ `BA_HeavySub.fxp` → Categoria: **Bass** (BA é prefixo)
- ✅ `Alabama.fxp` → **Não** categoriza como Bass

---

## 🚀 Instalação

```bash
git clone https://github.com/seu-usuario/Serum-File-Sorter-Organizer.git
cd Serum-File-Sorter-Organizer
```

**Requisitos:** Python 3.6+ (usa apenas biblioteca padrão)

---

## 💻 Uso

### Modo Interativo (Recomendado)
```bash
python main.py
```

O programa exibirá:
1. Instruções de uso
2. Informações de segurança
3. Solicitação dos caminhos de origem e destino
4. Confirmação antes de executar
5. Progresso em tempo real
6. Relatório final com estatísticas

### Modo Pré-configurado
Edite as variáveis no topo do arquivo `main.py`:
```python
PASTA_ORIGEM = "C:/Users/SeuNome/Downloads/Serum Presets"
PASTA_DESTINO = "C:/Users/SeuNome/Documents/Serum Organized"
```

---

## 📁 Estrutura do Projeto

```
Serum-File-Sorter-Organizer/
│
├── 📄 main.py                  # Ponto de entrada principal
│
├── 📁 src/                     # Código fonte
│   ├── __init__.py
│   ├── config.py               # Categorias e keywords
│   ├── categorizador.py        # Lógica de categorização
│   ├── manipulador_arquivos.py # Operações de arquivo
│   └── interface_visual.py     # Interface colorida
│
├── 📁 tests/                   # Testes unitários
│   ├── __init__.py
│   ├── test_categorizador.py
│   └── test_manipulador.py
│
├── 📁 utils/                   # Utilitários
│   ├── __init__.py
│   ├── listar_arquivos.py      # Exportar lista de arquivos
│   ├── testar_categorizacao.py # Testar antes de executar
│   └── run_tests.py            # Executor de testes
│
├── 📄 README.md
├── 📄 LICENSE
└── 📄 .gitignore
```

---

## 🧪 Testes

O projeto inclui **21 testes unitários** cobrindo:

### Categorizador (13 testes)
- Categorização por keywords (Bass, Lead, Pad, etc.)
- Tratamento de gêneros musicais (Future Bass, Drum and Bass)
- Multi-categorização
- Keywords curtas com word boundary
- Validação de extensões

### Manipulador de Arquivos (8 testes)
- Geração de nomes únicos
- Busca recursiva de presets
- Organização completa
- Tratamento de duplicatas (nome e hash)
- **Re-verificação segura** (não deleta arquivos sem categoria)
- Prevenção de duplicatas em re-verificação

```bash
# Executar todos os testes
python utils/run_tests.py

# Ou individualmente
python -m tests.test_categorizador
python -m tests.test_manipulador
```

### Utilitários de Teste

```bash
# Listar arquivos de uma pasta
python utils/listar_arquivos.py

# Testar categorização sem copiar
python utils/testar_categorizacao.py
```

---

## 📋 Exemplo de Execução

```
╔═══════════════════════════════════════════════════════════════════╗
║   ███████╗███████╗██████╗ ██╗   ██╗███╗   ███╗                    ║
║   ██╔════╝██╔════╝██╔══██╗██║   ██║████╗ ████║                    ║
║   ███████╗█████╗  ██████╔╝██║   ██║██╔████╔██║                    ║
║          🎹  P R E S E T   O R G A N I Z E R  🎹                  ║
╚═══════════════════════════════════════════════════════════════════╝

  ═══════════════════════════════════════════════════════════════
    📖 BEM-VINDO AO SERUM PRESET ORGANIZER!
  ═══════════════════════════════════════════════════════════════

  ✨ O QUE ESTE PROGRAMA FAZ:
  
     Este programa organiza automaticamente seus presets do Serum
     em pastas por categoria (Bass, Lead, Pad, FX, etc.)
     
  🔒 SEGURANÇA:
  
     • Seus arquivos originais NUNCA serão modificados ou deletados
     • O programa apenas COPIA os presets para novas pastas
     • Detecção de duplicatas: arquivos idênticos não são copiados 2x
     
  🧪 TESTES REALIZADOS:
  
     • ✅ Testado com milhares de presets reais
     • ✅ Milhares de padrões de nomes diferentes validados
     • ✅ 21 testes unitários automatizados (todos passando)
```

---

## ⚙️ Personalizando Categorias

Edite o arquivo `src/config.py`:

```python
MAPA_CATEGORIAS = {
    "MinhaCategoria": ["keyword1", "keyword2", "keyword3"],
    # ...
}

# Para keywords curtas (2-3 chars), adicione também:
KEYWORDS_CURTAS = {"k1", "k2", "k3"}
```

---

## 🔒 Segurança

| Garantia | Descrição |
|----------|-----------|
| ✅ Modo cópia padrão | Arquivos de origem permanecem intactos |
| ✅ Preserva metadados | Usa `shutil.copy2` para manter timestamps |
| ✅ Hash MD5 | Detecta duplicatas pelo conteúdo, não nome |
| ✅ Idempotente | Execute quantas vezes quiser sem problemas |
| ✅ Validação | Confirma caminhos antes de executar |
| ✅ Re-verificação segura | Arquivos sem categoria nunca são deletados |
| ✅ Verificação de mesmo arquivo | Detecta quando origem e destino são o mesmo |

---

## 📄 Extensões Suportadas

- `.fxp` - Preset padrão do Serum
- `.SerumPreset` - Formato alternativo

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

**Feito com ❤️ para produtores musicais**

🎹 🎧 🎵

</div>
