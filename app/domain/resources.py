# app/domain/resources.py
"""
Fonte da Verdade para dados de recursos, produtos de animais e cogumelos.
Este módulo consolida todos os itens básicos que não se enquadram em outras
categorias de domínio mais específicas (como ferramentas, frutas ou flores).
"""

RESOURCES_DATA = {
    # --- Resources ---
    "Wood": {
        "type": "Resource",
        "source": "Tree",
        "enabled": True,
        "tool_required": "Axe",
        "skill_tree": "Trees",
        "boost_categories": ["Resource", "Wood"],
        "details": {
            "cycle": {
                # O ciclo de vida de uma árvore
                "Tree": {
                    "yield_amount": 1,
                    "recovery_time_seconds": 7200,  # 2 horas
                    "hp": 3,
                },
            },
        }
    },
    "Stone": {
        "type": "Resource",
        "source": "Stone Rock",
        "enabled": True,
        "tool_required": "Pickaxe",
        "skill_tree": "Mining",
        "boost_categories": ["Resource", "Mining"],
        "details": {
            "cycle": {
                "Stone Rock": {
                    "yield_amount": 1,
                    "recovery_time_seconds": 14400  # 4 horas
                }
            }
        }
    },
    "Iron": {
        "type": "Resource",
        "source": "Iron Rock",
        "enabled": True,
        "tool_required": "Stone Pickaxe",
        "skill_tree": "Mining",
        "boost_categories": ["Resource", "Mining"],
        "details": {
            "cycle": {
                "Iron Rock": {
                    "yield_amount": 1,
                    "recovery_time_seconds": 28800  # 8 horas
                }
            }
        }
    },
    "Gold": {
        "type": "Resource",
        "source": "Gold Rock",
        "enabled": True,
        "tool_required": "Iron Pickaxe",
        "skill_tree": "Mining",
        "boost_categories": ["Resource", "Mining"],
        "details": {
            "cycle": {
                "Gold Rock": {
                    "yield_amount": 1,
                    "recovery_time_seconds": 86400  # 24 horas
                }
            }
        }
    },
    "Crimstone": {
        "type": "Resource", 
        "source": "Crimstone Rock", 
        "enabled": True,
        "tool_required": "Gold Pickaxe",
        "skill_tree": "Mining",
        "boost_categories": ["Resource", "Mining"],
        "details": { 
            "cycle": { 
                "Crimstone Rock": { 
                    "yield_amount": 1, 
                    "recovery_time_seconds": 86400 #24hrs
                }
            }
        } 
    },
    "Sunstone": {
        "type": "Resource", 
        "source": "Sunstone Rock", 
        "enabled": True,
        "tool_required": "Gold Pickaxe",
        "skill_tree": "Mining",
        "boost_categories": ["Resource", "Mining"],
        "details": { 
            "cycle": { 
                "Sunstone Rock": { 
                    "yield_amount": 1, 
                    "recovery_time_seconds": 259200 #72hrs 
                }
            }
        }
    },
    "Oil": {
        "type": "Resource", 
        "source": "Oil Reserve", 
        "enabled": True,
        "tool_required": "Oil Drill",
        "skill_tree": "Machinery",
        "boost_categories": ["Resource", "Machinery"],
        "details": { 
            "cycle": { 
                "Oil Reserve": { 
                    "yield_amount": 10, 
                    "recovery_time_seconds": 72000 # 20hrs
                }
            }
        } 
    },
    "Diamond": {
        "type": "Resource", 
        "source": "Boulder", 
        "enabled": False,
        "details": { 
            "cycle": { 
                "Boulder": { 
                    "yield_amount": 1, 
                    "recovery_time_seconds": 0 
                }
            }
        }
    },
    "Obsidian": {
        "type": "Resource", 
        "source": "Lava Pit", 
        "enabled": True,
        "details": { 
            "cycle": { 
                "Lava Pit": { 
                    "yield_amount": 1, 
                    "recovery_time_seconds": 0 
                }
            }
        }
    },

    # --- Animal Products ---
    "Egg":            {"type": "Animal Product", "enabled": True},
    "Leather":        {"type": "Animal Product", "enabled": True},
    "Wool":           {"type": "Animal Product", "enabled": True},
    "Merino Wool":    {"type": "Animal Product", "enabled": True},
    "Feather":        {"type": "Animal Product", "enabled": True},
    "Milk":           {"type": "Animal Product", "enabled": True},
    "Honey": {
        "type": "Animal Product",
        "source": "Beehive",
        "enabled": True,
        "skill_tree": "Bees & Flowers",
        "boost_categories": ["Honey", "Animal"],
        "details": {
            "cycle": {
                "Beehive": {
                    "yield_amount": 1,
                    "recovery_time_seconds": 86400  # 24 horas
                }
            }
        }
    },

    # --- Mushrooms ---
    "Wild Mushroom":  {"type": "Mushroom",       "enabled": True},
    "Magic Mushroom": {"type": "Mushroom",       "enabled": True},

    # --- Compost & Fertiliser ---
    "Earthworm":      {"type": "CompostWorm",    "enabled": True},
    "Grub":           {"type": "CompostWorm",    "enabled": True},
    "Red Wiggler":    {"type": "CompostWorm",    "enabled": True},
    "Fishing Lure":   {"type": "CompostWorm",    "enabled": True},
        "Sprout Mix": {
        "type": "Fertiliser",
        "composter": "Compost Bin",
        "boost_category": "Crop",
        "enabled": True,
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.20,
            "conditions": {"category": "Crop"}
        }]
    },
    "Fruitful Blend": {
        "type": "Fertiliser",
        "composter": "Turbo Composter",
        "boost_category": "Fruit",
        "enabled": True,
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.10,
            "conditions": {"category": "Fruit"}
        }]
    },
    "Rapid Root": {
        "type": "Fertiliser",
        "composter": "Premium Composter",
        "boost_category": "Crop",
        "enabled": True,
        "boosts": [{
            "type": "RECOVERY_TIME",
            "operation": "multiply",
            "value": 0.50,
            "conditions": {"category": "Crop"}
        }]
    },

    # --- Animal Food & Medicine ---
    "Kernel Blend":   {"type": "AnimalFood",     "ingredients": {"Corn": 1}, "enabled": True},
    "Hay":            {"type": "AnimalFood",     "ingredients": {"Wheat": 1}, "enabled": True},
    "NutriBarley":    {"type": "AnimalFood",     "ingredients": {"Barley": 1}, "enabled": True},
    "Mixed Grain":    {"type": "AnimalFood",     "ingredients": {"Wheat": 1, "Corn": 1, "Barley": 1}, "enabled": True},
    "Barn Delight":   {"type": "AnimalMedicine", "ingredients": {"Lemon": 5, "Honey": 3}, "enabled": True},
    "Omnifeed":       {"type": "AnimalFood",     "ingredients": {"Gem": 1}, "enabled": True},
}