# app/domain/bud_rules.py

# Este arquivo define as regras de bônus para os Buds, separadas por Type, Stem e Aura.
# A lógica de cálculo é: (Type Bonus + Stem Bonus) * Aura Multiplier.

BUD_TYPE_BUFFS = {
    "Plaza": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0.3,
            "conditions": {"category": "Basic Crop", "planting_spot": "Crop Plot"}
        }]
    },
    "Woodlands": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0.2,
            "conditions": {"resource": "Wood"}
        }]
    },
    "Cave": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0.2,
            "conditions": {"category": "Mineral"}
        }]
    },
    "Sea": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0, # TODO: Bônus de pesca
            "conditions": {"category": "Fish"}
        }]
    },
    "Castle": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0.3,
            "conditions": {"category": "Medium Crop", "planting_spot": "Crop Plot"}
        }]
    },
    "Port": {
        "boosts": [{
            "type": "XP", "operation": "percentage", "value": 0.1,
            "conditions": {"category": "Fish Food"}
        }]
    },
    "Retreat": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0.2,
            "conditions": {"category": "Animal Produce"}
        }]
    },
    "Saphiro": {
        "boosts": [{
            "type": "RECOVERY_TIME", "operation": "percentage", "value": -0.1,
            "conditions": {"category": "Crop"}
        }]
    },
    "Snow": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0.3,
            "conditions": {"category": "Advanced Crop", "planting_spot": "Crop Plot"}
        }]
    },
    "Beach": {
        "boosts": [{
            "type": "YIELD", "operation": "add", "value": 0.2,
            "conditions": {"category": "Fruit"}
        }]
    }
}

BUD_STEM_BUFFS = {
    "3 Leaf Clover": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.5, "conditions": {"category": "Crop"}}]
    },
    "Basic Leaf": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"category": "Basic Crop", "planting_spot": "Crop Plot"}}]
    },
    "Carrot Head": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.3, "conditions": {"resource": "Carrot"}}]
    },
    "Sunflower Hat": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.5, "conditions": {"resource": "Sunflower"}}]
    },
    "Diamond Gem": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"category": "Mineral"}}]
    },
    "Ruby Gem": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"resource": "Stone"}}]
    },
    "Miner Hat": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"resource": "Iron"}}]
    },
    "Gold Gem": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"resource": "Gold"}}]
    },
    "Mushroom": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.3, "conditions": {"resource": "Wild Mushroom"}}]
    },
    "Magic Mushroom": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"resource": "Magic Mushroom"}}]
    },
    "Acorn Hat": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.1, "conditions": {"resource": "Wood"}}]
    },
    "Tree Hat": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"resource": "Wood"}}]
    },
    "Banana": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"category": "Fruit"}}]
    },
    "Apple Head": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"category": "Fruit"}}]
    },
    "Egg Head": {
        "boosts": [{"type": "YIELD", "operation": "add", "value": 0.2, "conditions": {"resource": "Egg"}}]
    }
}

BUD_AURA_BUFFS = {
    "Basic": {
        "boosts": [{"type": "MULTIPLIER", "operation": "multiply", "value": 1.05}]
    },
    "Green": {
        "boosts": [{"type": "MULTIPLIER", "operation": "multiply", "value": 1.2}]
    },
    "Rare": {
        "boosts": [{"type": "MULTIPLIER", "operation": "multiply", "value": 2.0}]
    },
    "Mythical": {
        "boosts": [{"type": "MULTIPLIER", "operation": "multiply", "value": 5.0}]
    }
}