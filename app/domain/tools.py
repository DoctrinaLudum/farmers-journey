# app/domain/tools.py
"""
Fonte da Verdade para os dados das ferramentas (Tools).

Este módulo centraliza todas as informações sobre as ferramentas do jogo,
agrupadas pelo local de obtenção ou fabrico (Workbench, Treasure, etc.).
Os dados foram extraídos e adaptados do ficheiro 'tools.ts' do jogo.
"""

TOOLS_DATA = {
    # --- GRUPO WORKBENCH ---
    "Axe": {
        "name": "Axe",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 20,
        "ingredients": {},
        "enabled": True,
    },
    "Pickaxe": {
        "name": "Pickaxe",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 20,
        "ingredients": {"Wood": 3},
        "enabled": True,
    },
    "Stone Pickaxe": {
        "name": "Stone Pickaxe",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 20,
        "ingredients": {"Wood": 3, "Stone": 5},
        "enabled": True,
    },
    "Iron Pickaxe": {
        "name": "Iron Pickaxe",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 80,
        "ingredients": {"Wood": 3, "Iron": 5},
        "enabled": True,
    },
    "Gold Pickaxe": {
        "name": "Gold Pickaxe",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 100,
        "ingredients": {"Wood": 3, "Gold": 3},
        "enabled": True,
    },
    "Rod": {
        "name": "Rod",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 20,
        "ingredients": {"Wood": 3, "Stone": 1},
        "enabled": True,
    },
    "Oil Drill": {
        "name": "Oil Drill",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 100,
        "ingredients": {"Wood": 20, "Iron": 9, "Leather": 10},
        "enabled": True,
    },
    "Pest Net": {
        "name": "Pest Net",
        "type": "Tool",
        "crafting_location": "Workbench",
        "price": 50,
        "ingredients": {"Wool": 2},
        "enabled": True,
    },

    # --- GRUPO TREASURE TOOLS ---
    "Sand Shovel": {
        "name": "Sand Shovel",
        "type": "Tool",
        "crafting_location": "Treasure",
        "price": 20,
        "ingredients": {"Wood": 2, "Stone": 1},
        "enabled": True,
    },
    "Sand Drill": {
        "name": "Sand Drill",
        "type": "Tool",
        "crafting_location": "Treasure",
        "price": 40,
        "ingredients": {"Oil": 1, "Crimstone": 1, "Wood": 3, "Leather": 1},
        "enabled": True,
    },

    # --- GRUPO ANIMAL AFFECTION ---
    "Petting Hand": {
        "name": "Petting Hand",
        "type": "Tool",
        "crafting_location": "Animal",
        "price": 0,
        "ingredients": {},
        "enabled": True,
    },
    "Brush": {
        "name": "Brush",
        "type": "Tool",
        "crafting_location": "Animal",
        "price": 2000,
        "ingredients": {},
        "enabled": True,
    },
    "Music Box": {
        "name": "Music Box",
        "type": "Tool",
        "crafting_location": "Animal",
        "price": 50000,
        "ingredients": {},
        "enabled": True,
    },
}