# -*- coding: utf-8 -*-
"""
Módulo de Configuração - Serum Preset Organizer
================================================
Contém o mapeamento de categorias e keywords para classificação dos presets.
"""

# Extensões de arquivo suportadas pelo Serum
EXTENSOES_SUPORTADAS = ['.fxp', '.serumpreset']

# Mapeamento de Categorias -> Keywords
# A ordem importa: categorias mais específicas devem vir antes das genéricas
MAPA_CATEGORIAS = {
    "Bass": [
        "bass", "bs", "bss", "grave", "growl", "808", "sub", "reese", 
        "log", "wobble", "dubstep", "riddim", "neuro"
    ],
    
    "Lead": [
        "lead", "ld", "lds", "solo", "hook", "main", "melody", "screech"
    ],
    
    "Pluck": [
        "pluck", "pl", "plk", "pizz", "pizzicato", "staccato"
    ],
    
    "Piano_Keys": [
        "piano", "pn", "keys", "ky", "organ", "org", "e-piano", 
        "epiano", "rhodes", "wurlitzer", "clav", "clavinet"
    ],
    
    "Pad": [
        "pad", "pd", "atm", "atmosphere", "drone", "amb", "ambient",
        "evolving", "lush", "warm", "soft", "dreamy", "ethereal"
    ],
    
    "Synth": [
        "synth", "syn", "poly", "saw", "square", "analog", "analogue",
        "vintage", "retro", "classic", "80s", "synthwave"
    ],
    
    "Drums": [
        "drum", "kick", "snare", "clap", "hat", "cymbal", "perc",
        "tom", "hihat", "hi-hat", "percussion", "808drum"
    ],
    
    "Arp_Seq": [
        "arp", "seq", "sequence", "rhythm", "arpegg", "arpeggio",
        "gate", "gated", "pattern", "step"
    ],
    
    "FX": [
        "fx", "noise", "riser", "downlifter", "impact", "sweep",
        "trans", "transition", "sfx", "effect", "whoosh", "hit",
        "tension", "buildup", "drop"
    ],
    
    "Vocals": [
        "vox", "vocal", "choir", "voice", "formant", "talk",
        "speech", "sing", "singing", "human"
    ],
    
    "Strings_Orch": [
        "string", "str", "violin", "cello", "orch", "brass",
        "wind", "horn", "flute", "orchestra", "orchestral",
        "cinematic", "epic", "trailer", "woodwind"
    ],
    
    "Chords": [
        "chord", "ch", "stab", "chrd", "harmonic", "harmony"
    ]
}

# Categoria padrão para arquivos não classificados
CATEGORIA_PADRAO = "Uncategorized"
