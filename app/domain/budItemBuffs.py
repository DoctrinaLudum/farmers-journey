# ==============================================================================
#  BUD BUFFS DOMAIN
#  Dados e regras de negócio para os bônus dos Buds.
#  Valores 100% validados com a documentação oficial do jogo.
# ==============================================================================

BUD_BUFFS = {
    # ------------------ Buffs por TYPE ------------------
    "Plaza": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "BASIC_CROP_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.3,
            "conditions": {"category": "Basic Crops"},
        }],
    },
    "Woodlands": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "WOOD_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"resource": "Wood"},
        }],
    },
    "Cave": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "MINERAL_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"category": "Minerals"},
        }],
    },
    "Sea": {
        "boost_category": "Fish",
        "boosts": [
            {
                "name": "FISH_CRITICAL_YIELD",
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 1,
            },
            {
                "name": "FISH_CRITICAL_CHANCE",
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
            },
        ],
    },
    "Castle": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "MEDIUM_CROP_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.3,
            "conditions": {"category": "Medium Crops"},
        }],
    },
    "Port": {
        "boost_category": "XP",
        "boosts": [{
            "name": "FISH_XP",
            "type": "XP",
            "operation": "percentage",
            "value": 0.10,
            "conditions": {"category": "Fish"},
        }],
    },
    "Retreat": {
        "boost_category": "Animal",
        "boosts": [{
            "name": "ANIMAL_PRODUCE_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"category": "Animal Produce"},
        }],
    },
    "Saphiro": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "CROP_GROWTH_TIME",
            "type": "GROWTH_TIME",
            "operation": "percentage",
            "value": -0.10,
            "conditions": {"category": "Crop"},
        }],
    },
    "Snow": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "ADVANCED_CROP_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.3,
            "conditions": {"category": "Advanced Crops"},
        }],
    },
    "Beach": {
        "boost_category": "Fruit",
        "boosts": [{
            "name": "FRUIT_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"category": "Fruit"},
        }],
    },

    # ------------------ Buffs por STEM (Haste) ------------------
    "3 Leaf Clover": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "CROP_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.5,
            "conditions": {"category": "Crop"},
        }],
    },
    "Fish Hat": {
        "boost_category": "Fish",
        "boosts": [
            {
                "name": "FISH_CRITICAL_YIELD",
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 1,
            },
            {
                "name": "FISH_CRITICAL_CHANCE",
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
            },
        ],
    },
    "Diamond Gem": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "MINERAL_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"category": "Mineral"},
        }],
    },
    "Gold Gem": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "GOLD_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"resource": "Gold"},
        }],
    },
    "Miner Hat": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "IRON_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"resource": "Iron"},
        }],
    },
    "Carrot Head": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "CARROT_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.3,
            "conditions": {"crop": "Carrot"},
        }],
    },
    "Basic Leaf": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "BASIC_CROP_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"category": "Basic Crops"},
        }],
    },
    "Sunflower Hat": {
        "boost_category": "Crop",
        "boosts": [{
            "name": "SUNFLOWER_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.5,
            "conditions": {"crop": "Sunflower"},
        }],
    },
    "Ruby Gem": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "STONE_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"resource": "Stone"},
        }],
    },
    "Mushroom": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "MUSHROOM_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.3,
            "conditions": {"resource": "Wild Mushroom"},
        }],
    },
    "Magic Mushroom": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "MAGIC_MUSHROOM_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"resource": "Magic Mushroom"},
        }],
    },
    "Acorn Hat": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "WOOD_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": {"resource": "Wood"},
        }],
    },
    "Banana": {
        "boost_category": "Fruit",
        "boosts": [{
            "name": "FRUIT_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"category": "Fruit"},
        }],
    },
    "Tree Hat": {
        "boost_category": "Resource",
        "boosts": [{
            "name": "WOOD_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"resource": "Wood"},
        }],
    },
    "Egg Head": {
        "boost_category": "Animal",
        "boosts": [{
            "name": "EGG_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"resource": "Egg"},
        }],
    },
    "Apple Head": {
        "boost_category": "Fruit",
        "boosts": [{
            "name": "FRUIT_YIELD",
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": {"category": "Fruit"},
        }],
    },

    # ------------------ Stems Cosméticos (Sem Bônus) ------------------
    "Axe Head": {"boost_category": "Cosmetic", "boosts": []},
    "Sunshield Foliage": {"boost_category": "Cosmetic", "boosts": []},
    "Sunflower Headband": {"boost_category": "Cosmetic", "boosts": []},
    "Seashell": {"boost_category": "Cosmetic", "boosts": []},
    "Tender Coral": {"boost_category": "Cosmetic", "boosts": []},
    "Red Bow": {"boost_category": "Cosmetic", "boosts": []},
    "Hibiscus": {"boost_category": "Cosmetic", "boosts": []},
    "Rainbow Horn": {"boost_category": "Cosmetic", "boosts": []},
    "Silver Horn": {"boost_category": "Cosmetic", "boosts": []},


    # ------------------ Buffs por AURA ------------------
    "Basic": {
        "boost_category": "Bud",
        "boosts": [{
            "name": "BUD_BOOST_MULTIPLIER",
            "type": "BUD_BOOST_MULTIPLIER",
            "operation": "multiply",
            "value": 1.05,
        }],
    },
    "Green": {
        "boost_category": "Bud",
        "boosts": [{
            "name": "BUD_BOOST_MULTIPLIER",
            "type": "BUD_BOOST_MULTIPLIER",
            "operation": "multiply",
            "value": 1.20,
        }],
    },
    "Rare": {
        "boost_category": "Bud",
        "boosts": [{
            "name": "BUD_BOOST_MULTIPLIER",
            "type": "BUD_BOOST_MULTIPLIER",
            "operation": "multiply",
            "value": 2.00,
        }],
    },
    "Mythical": {
        "boost_category": "Bud",
        "boosts": [{
            "name": "BUD_BOOST_MULTIPLIER",
            "type": "BUD_BOOST_MULTIPLIER",
            "operation": "multiply",
            "value": 5.00,
        }],
    },
}