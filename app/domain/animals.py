# app/domain/animals.py
"""
Fonte da Verdade para os dados dos Animais.
"""

ANIMALS_DATA = {
    "Chicken": {
        "coins": 50,
        "level_required": 6,
        "building_required": "Hen House",
        "dimensions": {"width": 2, "height": 2},
        "resource_drops": { # Level: {Resource: Amount}
            1: {"Egg": 1}, 2: {"Egg": 1},
            3: {"Egg": 1, "Feather": 1},
            4: {"Egg": 2, "Feather": 1}, 5: {"Egg": 2, "Feather": 1}, 6: {"Egg": 2, "Feather": 1}, 7: {"Egg": 2, "Feather": 1},
            8: {"Egg": 3, "Feather": 1},
            9: {"Egg": 3, "Feather": 2}, 10: {"Egg": 3, "Feather": 2}, 11: {"Egg": 3, "Feather": 2}, 12: {"Egg": 3, "Feather": 2},
            13: {"Egg": 4, "Feather": 2}, 14: {"Egg": 4, "Feather": 2},
            15: {"Egg": 5, "Feather": 3}
        }
    },
    "Cow": {
        "coins": 100,
        "level_required": 14,
        "building_required": "Barn",
        "dimensions": {"width": 2, "height": 2},
        "resource_drops": { # Level: {Resource: Amount}
            1: {"Milk": 1},
            2: {"Milk": 1, "Leather": 1},
            3: {"Milk": 2},
            4: {"Milk": 2, "Leather": 1},
            5: {"Milk": 2, "Leather": 2},
            6: {"Milk": 3},
            7: {"Milk": 3, "Leather": 1},
            8: {"Milk": 3, "Leather": 2},
            9: {"Milk": 3, "Leather": 3}, 10: {"Milk": 3, "Leather": 3}, 11: {"Milk": 3, "Leather": 3}, 12: {"Milk": 3, "Leather": 3}, 13: {"Milk": 3, "Leather": 3}, 14: {"Milk": 3, "Leather": 3}, 15: {"Milk": 3, "Leather": 3}
        }
    },
    "Sheep": {
        "coins": 120,
        "level_required": 18,
        "building_required": "Barn",
        "dimensions": {"width": 2, "height": 2},
        "resource_drops": { # Level: {Resource: Amount}
            1: {"Wool": 1},
            2: {"Wool": 1, "Merino Wool": 1},
            3: {"Wool": 2},
            4: {"Wool": 2, "Merino Wool": 1},
            5: {"Wool": 2, "Merino Wool": 2},
            6: {"Wool": 3},
            7: {"Wool": 3, "Merino Wool": 1},
            8: {"Wool": 3, "Merino Wool": 2},
            9: {"Wool": 3, "Merino Wool": 3}, 10: {"Wool": 3, "Merino Wool": 3}, 11: {"Wool": 3, "Merino Wool": 3}, 12: {"Wool": 3, "Merino Wool": 3}, 13: {"Wool": 3, "Merino Wool": 3}, 14: {"Wool": 3, "Merino Wool": 3}, 15: {"Wool": 3, "Merino Wool": 3}
        }
    }
}
