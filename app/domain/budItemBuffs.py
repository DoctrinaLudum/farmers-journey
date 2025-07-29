BUD_BUFFS = {
    # Buffs por TYPE
    "Plaza": {
        "boost_category": "XP",
        "boosts": [{
            "type": "XP",
            "operation": "percentage",
            "value": 0.10,
            "conditions": {}
        }]
    },
    "Woodlands": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "resource": "Wood" }
        }]
    },
    "Cave": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "category": "Mineral" }
        }]
    },
    "Sea": {
        "boost_category": "Fish",
        "boosts": [{
            "type": "MARINE_MARVEL_CHANCE",
            "operation": "percentage",
            "value": 1.05, # +5% Chance
            "conditions": {}
        }]
    },
    "Castle": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "resource": "Iron" }
        }]
    },
    "Port": {
        "boost_category": "Fish",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "category": "Fish" }
        }]
    },
    "Retreat": {
        "boost_category": "Cooking",
        "boosts": [{
            "type": "MEAL_XP",
            "operation": "percentage",
            "value": 0.10,
            "conditions": {}
        }]
    },
    "Saphiro": {
        "boost_category": "Flower",
        "boosts": [{
            "type": "GROWTH_TIME",
            "operation": "percentage",
            "value": -0.10,
            "conditions": { "category": "Flower" }
        }]
    },
    "Snow": {
        "boost_category": "Crop",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "season": "Winter" }
        }]
    },
    "Beach": {
        "boost_category": "Treasure",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "category": "Beach Bounty" }
        }]
    },

    # Buffs por STEM (Haste)
    "3 Leaf Clover": {
        "boost_category": "Crop",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "crop": "Basic" }
        }]
    },
    "Fish Hat": {
        "boost_category": "Fish",
        "boosts": [{
            "type": "CRITICAL_CHANCE",
            "operation": "percentage",
            "value": 0.10,
            "conditions": { "category": "Fish" }
        }]
    },
    "Diamond Gem": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "resource": "Diamond" }
        }]
    },
    "Gold Gem": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.05,
            "conditions": { "resource": "Gold" }
        }]
    },
    "Miner Hat": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.05,
            "conditions": { "resource": "Iron" }
        }]
    },
    "Carrot Head": {
        "boost_category": "Crop",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "crop": "Carrot" }
        }]
    },
    "Sunflower Hat": {
        "boost_category": "Crop",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "crop": "Sunflower" }
        }]
    },
    "Basic Leaf": {
        "boost_category": "Crop",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": { "category": "Basic Crops" }
        }]
    },
    "Ruby Gem": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.05,
            "conditions": { "resource": "Stone" }
        }]
    },
    "Mushroom": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "resource": "Wild Mushroom" }
        }]
    },
    "Magic Mushroom": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.2,
            "conditions": { "resource": "Magic Mushroom" }
        }]
    },
    "Acorn Hat": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "resource": "Wood" }
        }]
    },
    "Banana": {
        "boost_category": "Fruit",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "crop": "Banana" }
        }]
    },
    "Tree Hat": {
        "boost_category": "Resource",
        "boosts": [{
            "type": "RECOVERY_TIME",
            "operation": "percentage",
            "value": -0.20,
            "conditions": { "resource": "Tree" }
        }]
    },
    "Egg Head": {
        "boost_category": "Animal",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "resource": "Egg" }
        }]
    },
    "Apple Head": {
        "boost_category": "Fruit",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 0.1,
            "conditions": { "crop": "Apple" }
        }]
    },

    # Buffs por AURA
    "Basic": {
        "boost_category": "Bud",
        "boosts": [{
            "type": "BUD_BOOST_INCREASE",
            "operation": "percentage",
            "value": 0.05, # +5%
            "conditions": {}
        }]
    },
    "Green": {
        "boost_category": "Bud",
        "boosts": [{
            "type": "BUD_BOOST_INCREASE",
            "operation": "percentage",
            "value": 0.10, # +10%
            "conditions": {}
        }]
    },
    "Rare": {
        "boost_category": "Bud",
        "boosts": [{
            "type": "BUD_BOOST_INCREASE",
            "operation": "percentage",
            "value": 0.20, # +20%
            "conditions": {}
        }]
    },
    "Mythical": {
        "boost_category": "Bud",
        "boosts": [{
            "type": "BUD_BOOST_INCREASE",
            "operation": "percentage",
            "value": 0.50, # +50%
            "conditions": {}
        }]
    }
}