# ==============================================================================
#  TREASURE & DIGGING DATA
#  Dados aprimorados e validados com base nos arquivos do jogo (desert.ts).
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. TREASURES: Detalhes para cada tesouro encontrado no jogo.
#    - sell_price: O valor em SFL quando vendido.
#    - type: A categoria do tesouro.
# ------------------------------------------------------------------------------
TREASURES = {
    # --- Beach Bounty Treasures (Vendáveis) ---
    "Sand": {"sell_price": 10, "type": "BeachBounty"},
    "Camel Bone": {"sell_price": 10, "type": "BeachBounty"},
    "Crab": {"sell_price": 15, "type": "BeachBounty"},
    "Old Bottle": {"sell_price": 22.5, "type": "BeachBounty"},
    "Sea Cucumber": {"sell_price": 22.5, "type": "BeachBounty"},
    "Vase": {"sell_price": 50, "type": "BeachBounty"},
    "Seaweed": {"sell_price": 75, "type": "BeachBounty"},
    "Cockle Shell": {"sell_price": 100, "type": "BeachBounty"},
    "Starfish": {"sell_price": 112.5, "type": "BeachBounty"},
    "Wooden Compass": {"sell_price": 131.25, "type": "BeachBounty"},
    "Iron Compass": {"sell_price": 187.5, "type": "BeachBounty"},
    "Emerald Compass": {"sell_price": 187.5, "type": "BeachBounty"},
    "Pipi": {"sell_price": 187.5, "type": "BeachBounty"},
    "Hieroglyph": {"sell_price": 250, "type": "BeachBounty"},
    "Clam Shell": {"sell_price": 375, "type": "BeachBounty"},
    "Coral": {"sell_price": 1500, "type": "BeachBounty"},
    "Pearl": {"sell_price": 3750, "type": "BeachBounty"},
    "Pirate Bounty": {"sell_price": 7500, "type": "BeachBounty"},

    # --- Beach Bounty Seasonal Artefacts (Vendáveis) ---
    "Scarab": {
        "sell_price": 200,
        "type": "BeachBountySeasonalArtefact"
    },
    "Cow Skull": {
        "sell_price": 200,
        "type": "BeachBountySeasonalArtefact"
    },
    "Ancient Clock": {
        "sell_price": 200,
        "type": "BeachBountySeasonalArtefact"
    },
    "Broken Pillar": {
        "sell_price": 200,
        "type": "BeachBountySeasonalArtefact"
    },
    "Coprolite": {
        "sell_price": 200,
        "type": "BeachBountySeasonalArtefact"
    },

    # --- Itens de Utilidade (Não vendáveis diretamente) ---
    "Wood": {"sell_price": None, "type": "Utility"},
    "Stone": {"sell_price": None, "type": "Utility"},
}

# ------------------------------------------------------------------------------
# 2. SEASONAL ARTEFACT: Define qual artefato é o especial da temporada.
#    Esta estrutura espelha a lógica de `desert.ts`.
# ------------------------------------------------------------------------------
SEASONAL_ARTEFACT = {
    "Bull Run": "Cow Skull",
    "Pharaoh's Treasure": "Scarab",
    "Solar Flare": "Scarab",
    "Dawn Breaker": "Scarab",
    "Witches' Eve": "Scarab",
    "Catch the Kraken": "Scarab",
    "Spring Blossom": "Scarab",
    "Clash of Factions": "Scarab",
    "Winds of Change": "Ancient Clock",
    "Great Bloom": "Broken Pillar",
    "Better Together": "Coprolite",
}

# ------------------------------------------------------------------------------
# 3. DIGGING_TOOLS: Detalhes de criação e uso das ferramentas de escavação.
# ------------------------------------------------------------------------------
DIGGING_TOOLS = {
    "Sand Shovel": {
        "sfl_price": 20,
        "ingredients": {"Wood": 2, "Stone": 1},
        "function": "Escava um único local em busca de tesouro.",
    },
    "Sand Drill": {
        "sfl_price": 40,
        "ingredients": {
            "Oil": 1,
            "Crimstone": 1,
            "Wood": 3,
            "Leather": 1
        },
        "function": (
            "Escava uma área de 3x3, aumentando a chance de achados raros."
        ),
    },
}

# ------------------------------------------------------------------------------
# 4. DIGGING_FORMATIONS: Define a composição e a forma exata de cada padrão
#    de tesouro, conforme extraído de `desert.ts`.
#    Cada padrão é uma lista de dicionários, onde cada um representa um item
#    e sua coordenada relativa (x, y) a um ponto de origem.
# ------------------------------------------------------------------------------
DIGGING_FORMATIONS = {
    # Padrões Diários
    "MONDAY_ARTEFACT_FORMATION": [
        {"name": "Camel Bone", "x": 0, "y": -1},
        {"name": "SEASONAL", "x": 1, "y": -1},
    ],
    "TUESDAY_ARTEFACT_FORMATION": [
        {"name": "SEASONAL", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 2},
    ],
    "WEDNESDAY_ARTEFACT_FORMATION": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "SEASONAL", "x": 1, "y": 0},
    ],
    "THURSDAY_ARTEFACT_FORMATION": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "SEASONAL", "x": 1, "y": -1},
    ],
    "FRIDAY_ARTEFACT_FORMATION": [
        {"name": "Camel Bone", "x": 2, "y": 0},
        {"name": "SEASONAL", "x": 3, "y": 0},
    ],
    "SATURDAY_ARTEFACT_FORMATION": [
        {"name": "SEASONAL", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": -1},
    ],
    "SUNDAY_ARTEFACT_FORMATION": [
        {"name": "SEASONAL", "x": 0, "y": -2},
    ],

    # Padrões de Artefatos
    "ARTEFACT_ONE": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 0, "y": 2},
    ],
    "ARTEFACT_TWO": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 2},
    ],
    "ARTEFACT_THREE": [{"name": "SEASONAL", "x": 0, "y": 0}],
    "ARTEFACT_FOUR": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 0, "y": 2},
        {"name": "Camel Bone", "x": 0, "y": 3},
    ],
    "ARTEFACT_FIVE": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": -1, "y": 0},
        {"name": "Camel Bone", "x": -2, "y": 0},
    ],
    "ARTEFACT_SIX": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": -1, "y": 0},
        {"name": "Camel Bone", "x": -2, "y": -1},
    ],
    "ARTEFACT_SEVEN": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 1},
    ],
    "ARTEFACT_EIGHT": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 2},
    ],
    "ARTEFACT_NINE": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 0, "y": -1},
        {"name": "Camel Bone", "x": -1, "y": -1},
    ],
    "ARTEFACT_TEN": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": -1, "y": 0},
        {"name": "Camel Bone", "x": -1, "y": 1},
    ],
    "ARTEFACT_ELEVEN": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 1, "y": 1},
    ],
    "ARTEFACT_TWELVE": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": -1, "y": 1},
        {"name": "Camel Bone", "x": 1, "y": 1},
    ],
    "ARTEFACT_THIRTEEN": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 2, "y": 0},
    ],
    "ARTEFACT_FOURTEEN": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 2},
    ],
    "ARTEFACT_FIFTEEN": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "SEASONAL", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 2, "y": 0},
    ],
    "ARTEFACT_SIXTEEN": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 1},
    ],
    "ARTEFACT_SEVENTEEN": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "SEASONAL", "x": 1, "y": 1},
    ],
    "ARTEFACT_EIGHTEEN": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 1, "y": 1},
    ],
    "ARTEFACT_NINETEEN": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 2, "y": 0},
        {"name": "SEASONAL", "x": 1, "y": 1},
    ],
    "ARTEFACT_TWENTY": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "SEASONAL", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 1, "y": 1},
    ],
    "ARTEFACT_TWENTY_ONE": [
        {"name": "SEASONAL", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 2, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 1, "y": 1},
    ],
    "ARTEFACT_TWENTY_TWO": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 2, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "SEASONAL", "x": 1, "y": 1},
    ],
    "ARTEFACT_TWENTY_THREE": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 2, "y": 0},
        {"name": "Camel Bone", "x": 1, "y": 1},
        {"name": "SEASONAL", "x": 2, "y": 1},
    ],
    "ARTEFACT_TWENTY_FOUR": [
        {"name": "Camel Bone", "x": 0, "y": 0},
        {"name": "SEASONAL", "x": 1, "y": 0},
        {"name": "Camel Bone", "x": 2, "y": 0},
        {"name": "Camel Bone", "x": 0, "y": 1},
        {"name": "Camel Bone", "x": 2, "y": 1},
    ],

    # Padrões de Tesouros Raros
    "HIEROGLYPH": [
        {"name": "Vase", "x": 0, "y": 0},
        {"name": "Vase", "x": 1, "y": 0},
        {"name": "Hieroglyph", "x": 0, "y": 1},
    ],
    "OLD_BOTTLE": [
        {"name": "Old Bottle", "x": 0, "y": 0},
        {"name": "Old Bottle", "x": 1, "y": 0},
        {"name": "Old Bottle", "x": 0, "y": 1},
        {"name": "Old Bottle", "x": 1, "y": 1},
    ],
    "COCKLE": [
        {"name": "Cockle Shell", "x": 0, "y": 0},
        {"name": "Cockle Shell", "x": 1, "y": 1},
        {"name": "Cockle Shell", "x": 2, "y": 2},
    ],
    "WOODEN_COMPASS": [
        {"name": "Wood", "x": 0, "y": 0},
        {"name": "Wooden Compass", "x": 1, "y": 0},
        {"name": "Wood", "x": 2, "y": 0},
    ],
    "SEA_CUCUMBERS": [
        {"name": "Sea Cucumber", "x": 0, "y": 0},
        {"name": "Sea Cucumber", "x": 1, "y": 0},
        {"name": "Sea Cucumber", "x": 2, "y": 0},
        {"name": "Pipi", "x": 3, "y": 0},
    ],
    "SEAWEED": [
        {"name": "Seaweed", "x": 0, "y": 0},
        {"name": "Seaweed", "x": 1, "y": 0},
        {"name": "Seaweed", "x": 2, "y": 0},
        {"name": "Starfish", "x": 2, "y": 1},
    ],
    "CLAM_SHELLS": [
        {"name": "Clam Shell", "x": 0, "y": 0},
        {"name": "Clam Shell", "x": 1, "y": 0},
        {"name": "Clam Shell", "x": 0, "y": -1},
        {"name": "Clam Shell", "x": 1, "y": -1},
    ],
    "CORAL": [
        {"name": "Stone", "x": 0, "y": 1},
        {"name": "Coral", "x": 0, "y": 0},
        {"name": "Stone", "x": 0, "y": -1},
    ],
    "PEARL": [
        {"name": "Stone", "x": 0, "y": 1},
        {"name": "Pearl", "x": 0, "y": 0},
        {"name": "Stone", "x": 0, "y": -1},
    ],
    "PIRATE_BOUNTY": [
        {"name": "Pirate Bounty", "x": 0, "y": 0},
    ],
}