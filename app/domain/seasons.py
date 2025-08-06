# ==============================================================================
#  SEASONS DOMAIN
#  Dados e regras de negócio para as temporadas do jogo, em um formato unificado.
# ==============================================================================

SEASONS_DATA = {
    "Solar Flare": {
        "start_date": "2023-01-01T00:00:00.000Z",
        "end_date": "2023-05-01T00:00:00.000Z",
        "ticket_name": "Solar Flare Ticket",
        "artefact_name": "Scarab",
        "chapter_fish": "Crimson Carp",
    },
    "Dawn Breaker": {
        "start_date": "2023-05-01T00:00:00.000Z",
        "end_date": "2023-08-01T00:00:00.000Z",
        "ticket_name": "Dawn Breaker Ticket",
        "artefact_name": "Scarab",
        "chapter_fish": "Crimson Carp",
    },
    "Witches' Eve": {
        "start_date": "2023-08-01T00:00:00.000Z",
        "end_date": "2023-11-01T00:00:00.000Z",
        "ticket_name": "Crow Feather",
        "artefact_name": "Scarab",
        "chapter_fish": "Crimson Carp",
    },
    "Catch the Kraken": {
        "start_date": "2023-11-01T00:00:00.000Z",
        "end_date": "2024-02-01T00:00:00.000Z",
        "ticket_name": "Mermaid Scale",
        "artefact_name": "Scarab",
        "chapter_fish": "Crimson Carp",
    },
    "Spring Blossom": {
        "start_date": "2024-02-01T00:00:00.000Z",
        "end_date": "2024-05-01T00:00:00.000Z",
        "ticket_name": "Tulip Bulb",
        "artefact_name": "Scarab",
        "chapter_fish": "Crimson Carp",
    },
    "Clash of Factions": {
        "start_date": "2024-05-01T00:00:00.000Z",
        "end_date": "2024-08-01T00:00:00.000Z",
        "ticket_name": "Scroll",
        "artefact_name": "Scarab",
        "chapter_fish": "Battle Fish",
    },
    "Pharaoh's Treasure": {
        "start_date": "2024-08-01T00:00:00.000Z",
        "end_date": "2024-11-01T00:00:00.000Z",
        "ticket_name": "Amber Fossil",
        "artefact_name": "Scarab",
        "chapter_fish": "Lemon Shark",
    },
    "Bull Run": {
        "start_date": "2024-11-01T00:00:00.000Z",
        "end_date": "2025-02-03T00:00:00.000Z",
        "ticket_name": "Horseshoe",
        "artefact_name": "Cow Skull",
        "chapter_fish": "Longhorn Cowfish",
    },
    "Winds of Change": {
        "start_date": "2025-02-03T00:00:00.000Z",
        "end_date": "2025-05-01T00:00:00.000Z",
        "ticket_name": "Timeshard",
        "artefact_name": "Ancient Clock",
        "chapter_fish": "Jellyfish",
    },
    "Great Bloom": {
        "start_date": "2025-05-01T00:00:00.000Z",
        "end_date": "2025-08-04T00:00:00.000Z",
        "ticket_name": "Geniseed",
        "artefact_name": "Broken Pillar",
        "chapter_fish": "Pink Dolphin",
    },
    "Better Together": {
        "start_date": "2025-08-04T00:00:00.000Z",
        "end_date": "2025-11-03T00:00:00.000Z",
        "start_date_gain_ticket": "2025-08-11T00:00:00.000Z",
        "ticket_name": "Bracelet",
        "artefact_name": "Coprolite",
        "chapter_fish": "Jellyfish",
    },
}

# Constante para a regra do Grub Shop
SEASONAL_TICKETS_PER_GRUB_SHOP_ORDER = 10