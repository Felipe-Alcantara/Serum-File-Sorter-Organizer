# -*- coding: utf-8 -*-
"""
Módulo de Configuração - Serum Preset Organizer
================================================
Contém o mapeamento de categorias e keywords para classificação dos presets.
"""

# Extensões de arquivo suportadas pelo Serum
EXTENSOES_SUPORTADAS = ['.fxp', '.serumpreset']

# =============================================================================
# MAPEAMENTO DE CATEGORIAS -> KEYWORDS
# =============================================================================
# REGRAS IMPORTANTES:
# 1. Keywords devem ter pelo menos 3 caracteres para evitar falsos positivos
# 2. Evitar keywords que são parte de outras palavras comuns
# 3. A ordem das categorias NÃO importa mais (multi-match habilitado)
# 4. Keywords são case-insensitive
# =============================================================================

MAPA_CATEGORIAS = {
    "Bass": [
        # Keywords principais - termos claros de bass
        "bass", "subbass", "sub bass", "808", "reese", 
        "wobble", "growl", "riddim", "neuro", "dubstep bass",
        # Evitado: "bs", "bss", "log", "sub" (muito curtos ou ambíguos)
    ],
    
    "Lead": [
        # Keywords principais
        "lead", "melody", "solo", "hook", "screech", "scream",
        # Evitado: "ld", "lds", "main" (muito curtos ou ambíguos)
    ],
    
    "Pluck": [
        "pluck", "plucked", "pizz", "pizzicato", "staccato", "short"
    ],
    
    "Piano_Keys": [
        "piano", "keys", "keyboard", "organ", "e-piano", "epiano", 
        "rhodes", "wurlitzer", "clav", "clavinet", "electric piano"
        # Evitado: "pn", "ky", "org" (muito curtos)
    ],
    
    "Pad": [
        "pad", "pads", "atmosphere", "drone", "ambient", "atmospheric",
        "evolving", "lush", "warm pad", "soft pad", "dreamy", "ethereal",
        "texture", "soundscape"
        # Evitado: "pd", "atm", "amb" (muito curtos)
    ],
    
    "Synth": [
        "synth", "poly", "polysynth", "analog", "analogue",
        "vintage", "retro", "classic synth", "80s", "synthwave",
        "supersaw", "saw lead", "square"
        # Evitado: "syn", "saw" sozinho (muito curtos/ambíguos)
    ],
    
    "Drums": [
        "drum", "drums", "kick", "snare", "clap", "hihat", "hi-hat",
        "cymbal", "percussion", "perc", "tom", "808 drum", "one shot"
        # Evitado: "hat" sozinho (pode ser "what", etc)
    ],
    
    "Arp_Seq": [
        "arp", "arps", "arpeggio", "arpeggiated", "sequence", "sequencer",
        "rhythm", "rhythmic", "gated", "gate", "pattern", "step"
        # Evitado: "seq" sozinho (muito curto)
    ],
    
    "FX": [
        "sfx", "effect", "effects", "noise", "riser", "rise",
        "downlifter", "down lifter", "impact", "sweep", "swoosh",
        "transition", "trans", "whoosh", "hit", "tension", 
        "buildup", "build up", "drop", "cinematic fx"
        # Evitado: "fx" sozinho pois aparece em nomes de packs
    ],
    
    "Vocals": [
        "vox", "vocal", "vocals", "choir", "voice", "formant", 
        "talk", "talking", "speech", "sing", "singing", "human voice"
    ],
    
    "Strings_Orch": [
        "string", "strings", "violin", "cello", "orchestra", "orchestral",
        "brass", "horn", "horns", "flute", "woodwind", "wind",
        "cinematic", "epic", "trailer", "film", "movie score"
        # Evitado: "str", "orch" (muito curtos)
    ],
    
    "Chords": [
        "chord", "chords", "stab", "stabs", "harmonic", "harmony",
        "triads", "power chord"
        # Evitado: "ch", "chrd" (muito curtos)
    ]
}

# =============================================================================
# TERMOS A IGNORAR (não são categorias, são gêneros/estilos)
# =============================================================================
# Estes termos aparecem em nomes de presets mas indicam GÊNERO, não tipo de som
# Exemplo: "Future Bass LEAD 01" - o timbre é LEAD, não bass
# =============================================================================

TERMOS_GENERO_IGNORAR = [
    "future bass",      # Gênero musical, não categoria de timbre
    "drum and bass",    # Gênero musical
    "drum & bass",
    "dnb",
    "dubstep",          # Já tratado nas keywords específicas de bass
    "trap",
    "edm",
    "house",
    "techno",
    "trance",
    "hardstyle",
    "hardcore",
    "electro",
    "progressive",
]

# Categoria padrão para arquivos não classificados
CATEGORIA_PADRAO = "Uncategorized"

# Tamanho mínimo de keyword para match (evita falsos positivos)
TAMANHO_MINIMO_KEYWORD = 3
