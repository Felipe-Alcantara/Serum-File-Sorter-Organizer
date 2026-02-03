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
# REGRAS:
# 1. Keywords curtas (2-3 chars) usam word boundary estrito
# 2. A ordem das categorias NÃO importa (multi-match habilitado)
# 3. Keywords são case-insensitive
# 4. Se um arquivo match múltiplas categorias, vai para todas
# =============================================================================

MAPA_CATEGORIAS = {
    "Bass": [
        # Keywords principais
        "bass", "subbass", "sub bass", "808", "reese", 
        "wobble", "growl", "riddim", "neuro",
        # Keywords curtas (usam word boundary estrito)
        "bs", "sub",
    ],
    
    "Lead": [
        # Keywords principais
        "lead", "melody", "solo", "hook", "screech", "scream", "screamer",
        # Keywords curtas
        "ld",
    ],
    
    "Pluck": [
        "pluck", "plucked", "pizz", "pizzicato", "staccato", "short",
        "pl",  # Curta
    ],
    
    "Piano_Keys": [
        "piano", "keys", "keyboard", "organ", "e-piano", "epiano", 
        "rhodes", "wurlitzer", "clav", "clavinet", "electric piano",
        "pn", "ky",  # Curtas
    ],
    
    "Pad": [
        "pad", "pads", "atmosphere", "drone", "ambient", "atmospheric",
        "evolving", "lush", "warm pad", "soft pad", "dreamy", "ethereal",
        "texture", "soundscape",
        "pd", "atm",  # Curtas
    ],
    
    "Synth": [
        "synth", "poly", "polysynth", "analog", "analogue",
        "vintage", "retro", "classic synth", "80s", "synthwave",
        "supersaw", "saw lead", "square",
        "syn", "saw",  # Curtas
    ],
    
    "Drums": [
        "drum", "drums", "kick", "snare", "clap", "hihat", "hi-hat",
        "cymbal", "percussion", "perc", "tom", "808 drum", "one shot",
        "hat", "hh",  # Curtas
    ],
    
    "Arp_Seq": [
        "arp", "arps", "arpeggio", "arpeggiated", "sequence", "sequencer",
        "rhythm", "rhythmic", "gated", "gate", "pattern", "step",
        "seq",  # Curta
    ],
    
    "FX": [
        "sfx", "effect", "effects", "noise", "riser", "rise",
        "downlifter", "down lifter", "impact", "sweep", "swoosh",
        "transition", "trans", "whoosh", "hit", "tension", 
        "buildup", "build up", "drop", "cinematic fx",
        "fx",  # Curta - mas a extensão .fxp é removida antes da análise
    ],
    
    "Vocals": [
        "vox", "vocal", "vocals", "choir", "voice", "formant", 
        "talk", "talking", "speech", "sing", "singing", "human voice",
    ],
    
    "Strings_Orch": [
        "string", "strings", "violin", "cello", "orchestra", "orchestral",
        "brass", "horn", "horns", "flute", "woodwind", "wind",
        "cinematic", "epic", "trailer", "film", "movie score",
        "str", "orch",  # Curtas
    ],
    
    "Chords": [
        "chord", "chords", "stab", "stabs", "harmonic", "harmony",
        "triads", "power chord",
        "ch", "chrd",  # Curtas
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

# Keywords curtas que precisam de word boundary estrito
# (não podem ser parte de outra palavra)
KEYWORDS_CURTAS = {"bs", "ld", "pl", "pn", "ky", "pd", "atm", "syn", "saw", 
                   "hat", "hh", "seq", "fx", "str", "ch", "chrd", "sub", "orch"}
