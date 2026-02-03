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
        "wobble", "growl", "riddim", "neuro", "hoover",
        # Português
        "baixo",
        # Prefixos comuns de packs (sem word boundary)
        "RKU_VLM_BT3_",  # Pack específico de bass
        "rps",  # Recreations de presets (geralmente bass/dubstep)
        # Keywords curtas (usam word boundary estrito)
        "ba", "bs", "sub", "gw", "hv",
    ],
    
    "Lead": [
        # Keywords principais
        "lead", "melody", "solo", "hook", "screech", "scream", "screamer",
        # Keywords curtas
        "ld",
    ],
    
    "Pluck": [
        "pluck", "plucked", "pizz", "pizzicato", "staccato",
        "mallet", "marimba", "xylophone", "vibraphone",
        "pl", "pr",  # Curtas
    ],
    
    "Bell": [
        # Nova categoria para bells
        "bell", "bells", "chime", "chimes", "glockenspiel",
        "tubular", "campanella", "tinkle",
        # Português
        "sino",
        "bl", "bel",  # Curtas (bel = prefix BEL_)
    ],
    
    "Piano_Keys": [
        "piano", "keys", "keyboard", "organ", "e-piano", "epiano", 
        "rhodes", "wurlitzer", "clav", "clavinet", "electric piano",
        # Português
        "teclado",
        "pn", "ky", "key", "or",  # Curtas (or = Organ)
    ],
    
    "Pad": [
        "pad", "pads", "atmosphere", "atmos", "athmos", "drone", 
        "ambient", "atmospheric", "evolving", "lush", "warm pad", 
        "soft pad", "dreamy", "ethereal", "texture", "soundscape",
        "pd", "atm", "pa", "at",  # Curtas (at = Atmosphere)
    ],
    
    "Synth": [
        "synth", "poly", "polysynth", "analog", "analogue",
        "vintage", "retro", "classic synth", "80s", "synthwave",
        "supersaw", "saw lead", "square", "classic",
        "syn", "saw", "sy", "cl",  # Curtas (cl = Classic prefix)
    ],
    
    "Acid": [
        # Nova categoria para acid sounds (TB-303 style)
        "acid", "303", "tb303", "tb-303", "acidic", "squelch",
    ],
    
    "Zap": [
        # Nova categoria para zap/laser sounds
        "zap", "laser", "lazer", "pew", "zapper",
    ],
    
    "Drums": [
        "drum", "drums", "kick", "snare", "clap", "hihat", "hi-hat",
        "cymbal", "percussion", "perc", "tom", "808 drum", "one shot",
        "timpani",  # Timpani drums
        "loop", "kit",  # Drum loops e kits
        "hat", "hh", "cy", "dl", "dr",  # Curtas (dl = Drum Loop, dr = Drums Kit)
    ],
    
    "Arp_Seq": [
        "arp", "arps", "arpeggio", "arpeggiated", "sequence", "sequencer",
        "rhythm", "rhythmic", "gated", "gate", "pattern", "step",
        "seq", "sq", "ar", "tg",  # Curtas (ar = prefix AR_, tg = Trance Gate)
    ],
    
    "FX": [
        "sfx", "effect", "effects", "noise", "riser", "rise",
        "downlifter", "down lifter", "impact", "sweep", "swoosh",
        "transition", "trans", "whoosh", "hit", "tension", 
        "buildup", "build up", "cinematic fx", "glitch",
        "grid",  # Para os "Grid -" presets
        # Português
        "ruido", "destrui", "explosao", "explo",
        "fx", "rss",  # Curtas (rss = Risers)
    ],
    
    "Vocals": [
        "vox", "vocal", "vocals", "choir", "voice", "formant", 
        "talk", "talking", "speech", "sing", "singing", "human voice",
        "vc", "vo",  # Curtas
    ],
    
    "Strings_Orch": [
        "string", "strings", "violin", "cello", "orchestra", "orchestral",
        "brass", "horn", "horns", "flute", "woodwind", "wind",
        "cinematic", "epic", "trailer", "film", "movie score",
        "clarinet", "trumpet", "ney",  # Instrumentos específicos
        "ensemble", "church",  # Ensembles e sons de igreja
        "str", "orch", "br", "ww", "st",  # Curtas (ww = Woodwind, st = Strings)
    ],
    
    "Chords": [
        "chord", "chords", "stab", "stabs", "harmonic", "harmony",
        "triads", "power chord",
        "ch", "chrd",  # Curtas
    ],
    
    "Guitar": [
        # Nova categoria para guitarras
        "guitar", "guitars", "gtr", "acoustic guitar", "electric guitar",
        "gt",  # Curta
    ],
    
    "Instrument": [
        # Nova categoria para instrumentos étnicos/específicos
        "instr", "instrument", "ethnic", "world",
        "kalimba", "guzheng", "sitar", "didgeridoo", "pipe",
        "flute", "pan flute", "bamboo",
        # Português
        "flauta",
    ],
    
    "Dubstep": [
        # Nova categoria para dubstep específico
        "dub", "dubstep", "brostep", "riddim", "tearout",
        "wompy", "womp", "wub",
    ],
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
KEYWORDS_CURTAS = {
    # Bass
    "ba", "bs", "sub", "gw", "hv", "rps",
    # Lead
    "ld",
    # Pluck
    "pl", "pr",
    # Bell
    "bl", "bel",  # bel = prefix BEL_
    # Keys
    "pn", "ky", "key", "or",  # or = Organ
    # Pad
    "pd", "atm", "pa", "at",  # at = Atmosphere
    # Synth
    "syn", "saw", "sy", "tg", "cl",  # tg = Trance Gate, cl = Classic
    # Drums
    "hat", "hh", "cy", "dl", "dr",  # dl = Drum Loop, dr = Drums Kit
    # Arp/Seq
    "seq", "sq", "ar",  # ar = Arp prefix
    # FX
    "fx", "rss",  # rss = Risers
    # Vocals
    "vc", "vo",
    # Strings
    "str", "orch", "br", "ww", "st",  # ww = Woodwind, st = Strings
    # Chords
    "ch", "chrd",
    # Guitar
    "gt",
    # Dubstep
    "dub",
}
