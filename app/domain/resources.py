# app/domain/resources.py
"""
Fonte da Verdade para dados de recursos, produtos de animais e cogumelos.
Este módulo consolida todos os itens básicos que não se enquadram em outras
categorias de domínio mais específicas (como ferramentas, frutas ou flores).
"""

RESOURCES_DATA = {
    # --- Resources ---
    "Wood":           {"type": "Resource",       "source": "Tree", "enabled": True},
    "Stone":          {"type": "Resource",       "source": "Stone Rock", "enabled": True},
    "Iron":           {"type": "Resource",       "source": "Iron Rock", "enabled": True},
    "Gold":           {"type": "Resource",       "source": "Gold Rock", "enabled": True},
    "Crimstone":      {"type": "Resource",       "source": "Crimstone Rock", "enabled": True},
    "Sunstone":       {"type": "Resource",       "source": "Sunstone Rock", "enabled": True},
    "Oil":            {"type": "Resource",       "source": "Oil Reserve", "enabled": True},
    "Diamond":        {"type": "Resource",       "source": "Boulder", "enabled": True},
    "Obsidian":       {"type": "Resource",       "source": "Lava Pit", "enabled": True},

    # --- Animal Products ---
    "Egg":            {"type": "Animal Product", "enabled": True},
    "Leather":        {"type": "Animal Product", "enabled": True},
    "Wool":           {"type": "Animal Product", "enabled": True},
    "Merino Wool":    {"type": "Animal Product", "enabled": True},
    "Feather":        {"type": "Animal Product", "enabled": True},
    "Milk":           {"type": "Animal Product", "enabled": True},
    "Honey":          {"type": "Animal Product", "enabled": True},

    # --- Mushrooms ---
    "Wild Mushroom":  {"type": "Mushroom",       "enabled": True},
    "Magic Mushroom": {"type": "Mushroom",       "enabled": True},

    # --- Compost & Fertiliser ---
    "Earthworm":      {"type": "CompostWorm",    "enabled": True},
    "Grub":           {"type": "CompostWorm",    "enabled": True},
    "Red Wiggler":    {"type": "CompostWorm",    "enabled": True},
    "Fishing Lure":   {"type": "CompostWorm",    "enabled": True},
    "Sprout Mix":     {"type": "Fertiliser",     "composter": "Compost Bin", "enabled": True},
    "Fruitful Blend": {"type": "Fertiliser",     "composter": "Turbo Composter", "enabled": True},
    "Rapid Root":     {"type": "Fertiliser",     "composter": "Premium Composter", "enabled": True},

    # --- Animal Food & Medicine ---
    "Kernel Blend":   {"type": "AnimalFood",     "ingredients": {"Corn": 1}, "enabled": True},
    "Hay":            {"type": "AnimalFood",     "ingredients": {"Wheat": 1}, "enabled": True},
    "NutriBarley":    {"type": "AnimalFood",     "ingredients": {"Barley": 1}, "enabled": True},
    "Mixed Grain":    {"type": "AnimalFood",     "ingredients": {"Wheat": 1, "Corn": 1, "Barley": 1}, "enabled": True},
    "Barn Delight":   {"type": "AnimalMedicine", "ingredients": {"Lemon": 5, "Honey": 3}, "enabled": True},
    "Omnifeed":       {"type": "AnimalFood",     "ingredients": {"Gem": 1}, "enabled": True},
}