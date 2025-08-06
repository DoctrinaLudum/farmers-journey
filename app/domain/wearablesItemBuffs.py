WEARABLES_ITEM_BUFFS = {
    "Chef Apron": {
        "id": 16,
        "part": "Coat",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "SELL_PRICE",
                "operation": "multiply",
                "value": 1.20,
                "conditions": {"category": "Cake"}
            }
        ],
        "enabled": True
    },
    "Sunflower Amulet": {
        "id": 27,
        "part": "Necklace",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.10,
                "conditions": {"crop": "Sunflower"}
            }
        ],
        "enabled": True
    },
        "Carrot Amulet": {
            "id": 28,
            "part": "Necklace",
            "boost_category": "Crop",
            "boosts": [
                {
                    "type": "GROWTH_TIME",
                    "operation": "percentage",
                    "value": -0.20,
                    "conditions": {"crop": "Carrot"}
                }
            ],
            "enabled": True
        },
    "Beetroot Amulet": {
        "id": 29,
        "part": "Necklace",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.20,
                "conditions": {"crop": "Beetroot"}
            }
        ],
        "enabled": True
    },
    "Green Amulet": {
        "id": 30,
        "part": "Necklace",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "CRITICAL_YIELD",
                "operation": "percentage",
                "value": 9.00,
                "conditions": {"category": "Crop"}
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"category": "Crop"}
            }
        ],
        "enabled": True
    },
    "Sunflower Shield": {
        "id": 31,
        "part": "SecondaryTool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "SEED_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {"crop": "Sunflower"}
            }
        ],
        "enabled": True
    },
    "Golden Spatula": {
        "id": 58,
        "part": "Tool",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "EXPERIENCE",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Parsnip": {
        "id": 56,
        "part": "Tool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.20,
                "conditions": {"crop": "Parsnip"}
            }
        ],
        "enabled": True
    },
    "Angel Wings": {
        "id": 73,
        "part": "Wings",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "INSTANT_GROW",
                "operation": "percentage",
                "value": 0.30,
                "conditions": {"category": "Crop"}
            }
        ],
        "enabled": True
    },
    "Devil Wings": {
        "id": 72,
        "part": "Wings",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "INSTANT_GROW",
                "operation": "percentage",
                "value": 0.30,
                "conditions": {"category": "Crop"}
            }
        ],
        "enabled": True
    },
    "Fruit Picker Apron": {
        "id": 86,
        "part": "Coat",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"category": "Fruit"}
            }
        ],
        "enabled": True
    },
    "Pirate Potion": {
        "id": 90,
        "part": "Body",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "DAILY_FREE_GIFT",
                "operation": "add",
                "value": 1,
                "conditions": {"area": "Beach"}
            }
        ],
        "enabled": True
    },
    "Eggplant Onesie": {
        "id": 124,
        "part": "Onesie",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop": "Eggplant"}
            }
        ],
        "enabled": True
    },
    "Mushroom Hat": {
        "id": 128,
        "part": "Hat",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"resource": "Mushroom"}
            }
        ],
        "enabled": True
    },
    "Luna's Hat": {
        "id": 161,
        "part": "Hat",
        "boost_category": "Cooking",
        "boosts": [
            {
                "type": "COOKING_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Infernal Pitchfork": {
        "id": 162,
        "part": "Tool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 3,
                "conditions": {"category": "Crop"}
            }
        ],
        "enabled": True
    },
    "Cattlegrim": {
        "id": 164,
        "part": "Hat",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"category": "Animal"}
            }
        ],
        "enabled": True
    },
    "Corn Onesie": {
        "id": 174,
        "part": "Onesie",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop": "Corn"}
            }
        ],
        "enabled": True
    },
    "Luminous Anglerfish Topper": {
        "id": 221,
        "part": "Hat",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "FISH_XP",
                "operation": "percentage",
                "value": 0.50,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Ancient Rod": {
        "id": 224,
        "part": "Tool",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "CAST_WITHOUT_ROD",
                "operation": "equals",
                "value": 0,
                "conditions": {"category": "Fish"}
            }
        ],
        "enabled": True
    },
    "Trident": {
        "id": 226,
        "part": "Tool",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {"category": "Fish"}
            },
            {
                "type": "CRITICAL_AMOUNT",
                "operation": "add",
                "value": 1,
                "conditions": {"category": "Fish"}
            }
        ],
        "enabled": True
    },
    "Bucket O' Worms": {
        "id": 228,
        "part": "SecondaryTool",
        "boost_category": "Bait",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"resource": "Worm"}
            }
        ],
        "enabled": True
    },
    "Crab Trap": {
        "id": 230,
        "part": "SecondaryTool",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "BONUS_CRAB",
                "operation": "add",
                "value": 1,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Angler Waders": {
        "id": 234,
        "part": "Pants",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "DAILY_FISHING_ATTEMPTS",
                "operation": "add",
                "value": 10,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Sunflower Rod": {
        "id": 240,
        "part": "Tool",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"category": "Fish"}
            },
            {
                "type": "CRITICAL_AMOUNT",
                "operation": "add",
                "value": 1,
                "conditions": {"category": "Fish"}
            }
        ],
        "enabled": True
    },
    "Banana Amulet": {
        "id": 250,
        "part": "Necklace",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {"crop": "Banana"}
            }
        ],
        "enabled": True
    },
    "Banana Onesie": {
        "id": 251,
        "part": "Onesie",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.20,
                "conditions": {"crop": "Banana"}
            }
        ],
        "enabled": True
    },
    "Deep Sea Helm": {
        "id": 255,
        "part": "Hat",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "MARINE_MARVEL_CHANCE",
                "operation": "percentage",
                "value": 2.00,
                "conditions": {"category": "Fish"}
            }
        ],
        "enabled": True
    },
    "Bee Suit": {
        "id": 276,
        "part": "Suit",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "HONEY_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Beekeeper Hat": {
        "id": 278,
        "part": "Hat",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "HONEY_PRODUCTION_SPEED",
                "operation": "percentage",
                "value": 0.2,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Crimstone Armor": {
        "id": 282,
        "part": "Shirt",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"resource": "Crimstone"}
            }
        ],
        "enabled": True
    },
    "Crimstone Hammer": {
        "id": 284,
        "part": "Tool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {
                    "resource": "Crimstone", 
                    "minesLeft":1
                }
            }
        ],
        "enabled": True
    },
    "Crimstone Amulet": {
        "id": 285,
        "part": "Necklace",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "RECOVERY_TIME",
                "operation": "percentage",
                "value": -0.20,
                "conditions": {"resource": "Crimstone Rock"}
            }
        ],
        "enabled": True
    },
    "Honeycomb Shield": {
        "id": 291,
        "part": "SecondaryTool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "HONEY_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Hornet Mask": {
        "id": 292,
        "part": "Hat",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "BEE_SWARM_CHANCE",
                "operation": "percentage",
                "value": 1.00,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Flower Crown": {
        "id": 293,
        "part": "Hat",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {"category": "Flower"}
            }
        ],
        "enabled": True
    },
    "Non La Hat": {
        "id": 309,
        "part": "Hat",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"crop": "Rice"}
            }
        ],
        "enabled": True
    },
    "Oil Can": {
        "id": 308,
        "part": "Tool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {"resource": "Oil"}
            }
        ],
        "enabled": True
    },
    "Olive Shield": {
        "id": 310,
        "part": "SecondaryTool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"crop": "Olive"}
            }
        ],
        "enabled": True
    },
    "Paw Shield": {
        "id": 311,
        "part": "SecondaryTool",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "FACTION_PET_SATIATION",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {}
            },
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Pan": {
        "id": 314,
        "part": "Tool",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "XP_GAINS",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Olive Royalty Shirt": {
        "id": 317,
        "part": "Shirt",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"crop": "Olive"}
            }
        ],
        "enabled": True
    },
    "Tofu Mask": {
        "id": 319,
        "part": "Hat",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop": "Soybean"}
            }
        ],
        "enabled": True
    },
    "Goblin Armor": {
        "id": 320,
        "part": "Shirt",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Goblin Helmet": {
        "id": 321,
        "part": "Hat",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Goblin Pants": {
        "id": 322,
        "part": "Pants",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Goblin Sabatons": {
        "id": 323,
        "part": "Shoes",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Goblin Axe": {
        "id": 324,
        "part": "Tool",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Nightshade Armor": {
        "id": 325,
        "part": "Shirt",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Nightshade Helmet": {
        "id": 326,
        "part": "Hat",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Nightshade Pants": {
        "id": 327,
        "part": "Pants",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Nightshade Sabatons": {
        "id": 328,
        "part": "Shoes",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Nightshade Sword": {
        "id": 329,
        "part": "Tool",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Armor": {
        "id": 330,
        "part": "Shirt",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Helmet": {
        "id": 331,
        "part": "Hat",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Sword": {
        "id": 332,
        "part": "Tool",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Pants": {
        "id": 333,
        "part": "Pants",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Sabatons": {
        "id": 334,
        "part": "Shoes",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Armor": {
        "id": 335,
        "part": "Shirt",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Sword": {
        "id": 336,
        "part": "Tool",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Helmet": {
        "id": 337,
        "part": "Hat",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Pants": {
        "id": 338,
        "part": "Pants",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Sabatons": {
        "id": 339,
        "part": "Shoes",
        "boost_category": "Faction",
        "boosts": [
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Camel Onesie": {
        "id": 350,
        "part": "Onesie",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"category": "Fruit Patch"}
            }
        ],
        "enabled": True
    },
    "Dev Wrench": {
        "id": 354,
        "part": "Tool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "RECOVERY_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {"resource": "Oil Reserve"}
            }
        ],
        "enabled": True
    },
    "Oil Overalls": {
        "id": 360,
        "part": "Pants",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 10,
                "conditions": {"resource": "Oil"}
            }
        ],
        "enabled": True
    },
    "Ancient Shovel": {
        "id": 369,
        "part": "Tool",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "DIG_WITHOUT_SHOVEL",
                "operation": "equals",
                "value": 0,
                "conditions": {"category": "Treasure"}
            }
        ],
        "enabled": True
    },
    "Infernal Drill": {
        "id": 370,
        "part": "SecondaryTool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "DRILL_WITHOUT_OIL_DRILL",
                "operation": "equals",
                "value": 0,
                "conditions": {"resource": "Oil"}
            }
        ],
        "enabled": True
    },
    "Lemon Shield": {
        "id": 371,
        "part": "SecondaryTool",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"crop": "Lemon"}
            }
        ],
        "enabled": True
    },
    "Grape Pants": {
        "id": 373,
        "part": "Pants",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {"crop": "Grape"}
            }
        ],
        "enabled": True
    },
    "Bionic Drill": {
        "id": 374,
        "part": "Wings",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "DAILY_DIGS",
                "operation": "add",
                "value": 5,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Bumpkin Crown": {
        "id": 376,
        "part": "Hat",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "FLOWER_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "COINS_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Goblin Crown": {
        "id": 377,
        "part": "Hat",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "FLOWER_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "COINS_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Nightshade Crown": {
        "id": 378,
        "part": "Hat",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "FLOWER_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "COINS_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Crown": {
        "id": 379,
        "part": "Hat",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "FLOWER_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "COINS_GAINED",
                "operation": "percentage",
                "value": 0.25,
                "conditions": {"category": "Deliveries"}
            },
            {
                "type": "MARKS_GAINED",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Shield": {
        "id": 380,
        "part": "SecondaryTool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": "Wood", "faction": "Bumpkins"}
            },
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": ["Stone", "Iron", "Gold"], "faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Goblin Shield": {
        "id": 381,
        "part": "SecondaryTool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": "Wood", "faction": "Goblins"}
            },
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": ["Stone", "Iron", "Gold"], "faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Nightshade Shield": {
        "id": 382,
        "part": "SecondaryTool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": "Wood", "faction": "Nightshades"}
            },
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": ["Stone", "Iron", "Gold"], "faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Shield": {
        "id": 383,
        "part": "SecondaryTool",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": "Wood", "faction": "Sunflorians"}
            },
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": ["Stone", "Iron", "Gold"], "faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Quiver": {
        "id": 384,
        "part": "Wings",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "FRUIT_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Bumpkins"}
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Goblin Quiver": {
        "id": 385,
        "part": "Wings",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "FRUIT_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Goblins"}
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Nightshade Quiver": {
        "id": 386,
        "part": "Wings",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "FRUIT_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Nightshades"}
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Quiver": {
        "id": 387,
        "part": "Wings",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "FRUIT_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Sunflorians"}
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Bumpkin Medallion": {
        "id": 388,
        "part": "Necklace",
        "boost_category": "Cooking",
        "boosts": [
            {
                "type": "COOKING_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {"faction": "Bumpkins"}
            }
        ],
        "enabled": True
    },
    "Goblin Medallion": {
        "id": 389,
        "part": "Necklace",
        "boost_category": "Cooking",
        "boosts": [
            {
                "type": "COOKING_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {"faction": "Goblins"}
            }
        ],
        "enabled": True
    },
    "Nightshade Medallion": {
        "id": 390,
        "part": "Necklace",
        "boost_category": "Cooking",
        "boosts": [
            {
                "type": "COOKING_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {"faction": "Nightshades"}
            }
        ],
        "enabled": True
    },
    "Sunflorian Medallion": {
        "id": 391,
        "part": "Necklace",
        "boost_category": "Cooking",
        "boosts": [
            {
                "type": "COOKING_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {"faction": "Sunflorians"}
            }
        ],
        "enabled": True
    },
    "Infernal Bullwhip": {
        "id": 400,
        "part": "Tool",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "BARN_ANIMAL_FEED_REDUCTION",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "White Sheep Onesie": {
        "id": 401,
        "part": "Onesie",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {"resource": "Wool"}
            }
        ],
        "enabled": True
    },
    "Black Sheep Onesie": {
        "id": 402,
        "part": "Onesie",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {"resource": "Wool"}
            }
        ],
        "enabled": True
    },
    "Chicken Suit": {
        "id": 403,
        "part": "Suit",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"resource": "Feather"}
            }
        ],
        "enabled": True
    },
    "Merino Jumper": {
        "id": 405,
        "part": "Shirt",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"resource": "Merino Wool"}
            }
        ],
        "enabled": True
    },
    "Dream Scarf": {
        "id": 406,
        "part": "Necklace",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PRODUCE_TIME",
                "operation": "percentage",
                "value": -0.20,
                "conditions": {"animal": "Sheep"}
            }
        ],
        "enabled": True
    },
    "Cowbell Necklace": {
        "id": 407,
        "part": "Necklace",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {"resource": "Milk"}
            }
        ],
        "enabled": True
    },
    "Milk Apron": {
        "id": 408,
        "part": "Coat",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {"resource": "Milk"}
            }
        ],
        "enabled": True
    },
    "Sickle": {
        "id": 414,
        "part": "Tool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {"crop": "Wheat"}
            }
        ],
        "enabled": True
    },
    "Ladybug Suit": {
        "id": 422,
        "part": "Suit",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "COIN_COST",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {"crop": "Onion"}
            }
        ],
        "enabled": True
    },
    "Crab Hat": {
        "id": 424,
        "part": "Hat",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "BONUS_FISHING_BOUNTY",
                "operation": "add",
                "value": 1,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Solflare Aegis": {
        "id": 431,
        "part": "SecondaryTool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {"season": "Summer"}
            }
        ],
        "enabled": True
    },
    "Blossom Ward": {
        "id": 432,
        "part": "SecondaryTool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"season": "Spring"}
            }
        ],
        "enabled": True
    },
    "Autumn's Embrace": {
        "id": 433,
        "part": "SecondaryTool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {"season": "Autumn"}
            }
        ],
        "enabled": True
    },
    "Frozen Heart": {
        "id": 434,
        "part": "SecondaryTool",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"season": "Winter"}
            }
        ],
        "enabled": True
    },

        "Oracle Syringe": {
        "id": 461,
        "part": "Wings",
        "description": "Infused with the Barn Delight, this curious tool channels healing to every ailing animals with a burst of magical care.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "HEAL_COST", 
                "operation": "equals",   
                "value": 0,             
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Obsidian Necklace": {
        "id": 457,
        "part": "Necklace",
        "description": "A shard of molten earth turned elegant charm, pulsing softly with ancient, dormant power.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "COOLDOWN",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "resource": "Obsidian"
                }
            }
        ],
        "enabled": True
    },
    "Medic Apron": {
        "id": 456,
        "part": "Coat",
        "description": "Worn by the caretakers of the sick and small, this apron carries the scent of healing herbs and kindness",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "MEDICINE_COST",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {}
            }
        ],
        "enabled": True
    },
    "Broccoli Hat": {
        "id": 454,
        "part": "Hat",
        "description": "crunchy crown for the veggie lover — surprisingly comfortable and extremely nutritious-looking!",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "crop": "Broccoli"
                }
            }
        ],
        "enabled": True
    },
    "Red Pepper Onesie": {
        "id": 458,
        "part": "Onesie",
        "description": "Spicy, snuggly, and absolutely sizzling with personality — it’s the hottest onesie in the land!",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "crop": "Pepper"
                }
            }
        ],
        "enabled": True
    },
}