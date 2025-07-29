# ==============================================================================
#  TREASURE & DIGGING DATA
#  Cross-referenced data from treasure.ts, game.ts, and config.py.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. TREASURES: Details for each treasure found in the game.
#    - sell_price: The SFL value when sold.
#    - type: The category of the treasure.
# ------------------------------------------------------------------------------
TREASURES = {   
    # --- Beach Bounty Treasures (Sellable) ---
    "Sand": {
        "sell_price": 10,  #
        "type": "BeachBounty",  #
    },
    "Camel Bone": {
        "sell_price": 10,  #
        "type": "BeachBounty",  #
    },
    "Crab": {
        "sell_price": 15,  #
        "type": "BeachBounty",  #
    },
    "Old Bottle": {
        "sell_price": 22.5,  #
        "type": "BeachBounty",  #
    },
    "Sea Cucumber": {
        "sell_price": 22.5,  #
        "type": "BeachBounty",  #
    },
    "Vase": {
        "sell_price": 50,  #
        "type": "BeachBounty",  #
    },
    "Seaweed": {
        "sell_price": 75,  #
        "type": "BeachBounty",  #
    },
    "Cockle Shell": {
        "sell_price": 100,  #
        "type": "BeachBounty",  #
    },
    "Starfish": {
        "sell_price": 112.5,  #
        "type": "BeachBounty",  #
    },
    "Wooden Compass": {
        "sell_price": 131.25,  #
        "type": "BeachBounty",  #
    },
    "Iron Compass": {
        "sell_price": 187.5,  #
        "type": "BeachBounty",  #
    },
    "Emerald Compass": {
        "sell_price": 187.5,  #
        "type": "BeachBounty",  #
    },
    "Pipi": {
        "sell_price": 187.5,  #
        "type": "BeachBounty",  #
    },
    "Hieroglyph": {
        "sell_price": 250,  #
        "type": "BeachBounty",  #
    },
    "Clam Shell": {
        "sell_price": 375,  #
        "type": "BeachBounty",  #
    },
    "Coral": {
        "sell_price": 1500,  #
        "type": "BeachBounty",  #
    },
    "Pearl": {
        "sell_price": 3750,  #
        "type": "BeachBounty",  #
    },
    "Pirate Bounty": {
        "sell_price": 7500,  #
        "type": "BeachBounty",  #
    },

    # --- Beach Bounty Seasonal Artefacts (Sellable) ---
    "Scarab": {
        "sell_price": 200,  #
        "type": "BeachBountySeasonalArtefact",  #
    },
    "Cow Skull": {
        "sell_price": 200,  #
        "type": "BeachBountySeasonalArtefact",  #
    },
    "Ancient Clock": {
        "sell_price": 200,  #
        "type": "BeachBountySeasonalArtefact",  #
    },
    "Broken Pillar": {
        "sell_price": 200,  #
        "type": "BeachBountySeasonalArtefact",  #
    },

    # --- Other Treasure Types (Not directly sellable this way) ---
    "Pirate Cake": {
        "sell_price": None,
        "type": "ConsumableTreasure",  #
    },
    "Abandoned Bear": {
        "sell_price": None,
        "type": "DecorationTreasure",  #
    },
    "Tiki Totem": {
        "sell_price": None,
        "type": "BoostTreasure",  #
    },
}

# ------------------------------------------------------------------------------
# 2. DIGGING_TOOLS: Crafting and usage details for digging tools.
#    - sfl_price: Cost in SFL to craft.
#    - ingredients: Resource cost to craft.
#    - function: Description of the tool's purpose.
# ------------------------------------------------------------------------------
DIGGING_TOOLS = {
    "Sand Shovel": {
        "sfl_price": 20,  #
        "ingredients": {"Wood": 2, "Stone": 1},  #
        "function": "Digs a single spot for treasure.",
    },
    "Sand Drill": {
        "sfl_price": 40,  #
        "ingredients": {"Oil": 1, "Crimstone": 1, "Wood": 3, "Leather": 1},  #
        "function": "Digs a 3x3 area for treasure, increasing chances of rare finds.",
    },
}

# ------------------------------------------------------------------------------
# 3. DIGGING_PATTERNS: Defines the shape of treasure patterns.
#    The shapes are based on the daily patterns found in the game and are used
#    by the simulator's logic to check if a pattern has been completed.
#    Each shape is represented by a list of relative coordinates (x, y)
#    from a starting point (0, 0).
# ------------------------------------------------------------------------------
DIGGING_PATTERNS = {
    "HIEROGLYPH_LINE": {
        "description": "A Vase, a Hieroglyph, and another Vase in a horizontal line.",
        "items": ["Vase", "Hieroglyph"],
        "shape": [
            {"item": "Vase", "coords": (0, 0)},
            {"item": "Hieroglyph", "coords": (1, 0)},
            {"item": "Vase", "coords": (2, 0)},
        ],
    },
    "COCKLE_SHELL_SQUARE": {
        "description": "A 2x2 square of Cockle Shells.",
        "items": ["Cockle Shell"],
        "shape": [
            {"item": "Cockle Shell", "coords": (0, 0)},
            {"item": "Cockle Shell", "coords": (1, 0)},
            {"item": "Cockle Shell", "coords": (0, 1)},
            {"item": "Cockle Shell", "coords": (1, 1)},
        ],
    },
    "PILLAR_LINE": {
        "description": "A vertical line of three Broken Pillars.",
        "items": ["Broken Pillar"],
        "shape": [
            {"item": "Broken Pillar", "coords": (0, 0)},
            {"item": "Broken Pillar", "coords": (0, 1)},
            {"item": "Broken Pillar", "coords": (0, 2)},
        ],
    },
    "BONES_AND_STONE_CLUSTER": {
        "description": "A cluster of five Camel Bones and one Stone.",
        "items": ["Camel Bone", "Stone"],
        "shape": [
            {"item": "Camel Bone", "coords": (0, 0)},
            {"item": "Camel Bone", "coords": (1, 0)},
            {"item": "Camel Bone", "coords": (2, 0)},
            {"item": "Camel Bone", "coords": (0, 1)},
            {"item": "Stone", "coords": (1, 1)},
            {"item": "Camel Bone", "coords": (2, 1)},
        ],
    },
    # Note: The file contains other possible patterns. Below are representative
    # structures for other pattern names found in the game data.
    "SEA_CUCUMBER_LINE": {
        "description": "A horizontal line of three Sea Cucumbers.",
        "items": ["Sea Cucumber"],
        "shape": [
            {"item": "Sea Cucumber", "coords": (0, 0)},
            {"item": "Sea Cucumber", "coords": (1, 0)},
            {"item": "Sea Cucumber", "coords": (2, 0)},
        ],
    },
    "DIAGONAL_CROSS": {
        "description": "A unique artefact pattern shaped like a cross.",
        "items": ["Ancient Clock"], # Example item
        "shape": [
            {"item": "Ancient Clock", "coords": (1, 0)},
            {"item": "Ancient Clock", "coords": (0, 1)},
            {"item": "Ancient Clock", "coords": (1, 1)},
            {"item": "Ancient Clock", "coords": (2, 1)},
            {"item": "Ancient Clock", "coords": (1, 2)},
        ],
    },
}