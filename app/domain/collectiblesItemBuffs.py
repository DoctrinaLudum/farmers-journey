COLLECTIBLES_ITEM_BUFFS = {
    "Basic Scarecrow": {
        "id": 462,
        "description": "Choosy defender of your farm's VIP (Very Important Plants)",
        "boost_category": "Crop",
        "size": { "width": 1, "height": 1 },
        "aoe": {
            "shape": "custom",
            "plots": [
                # Linha 1 (imediatamente abaixo do espantalho)
                { "x": -1, "y": -1 }, { "x": 0, "y": -1 }, { "x": 1, "y": -1 },
                # Linha 2
                { "x": -1, "y": -2 }, { "x": 0, "y": -2 }, { "x": 1, "y": -2 },
                # Linha 3
                { "x": -1, "y": -3 }, { "x": 0, "y": -3 }, { "x": 1, "y": -3 }
            ]
        },
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.20,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            }
        ]
    },
    "Scary Mike": {
        "id": 467,
        "description": "The veggie whisperer and champion of frightfully good harvests!",
        "boost_category": "Crop",
        "size": { "width": 1, "height": 1 },
        "aoe": {
            "shape": "custom",
            "plots": [
                # Linha 1 (imediatamente abaixo do espantalho)
                { "x": -1, "y": -1 }, { "x": 0, "y": -1 }, { "x": 1, "y": -1 },
                # Linha 2
                { "x": -1, "y": -2 }, { "x": 0, "y": -2 }, { "x": 1, "y": -2 },
                # Linha 3
                { "x": -1, "y": -3 }, { "x": 0, "y": -3 }, { "x": 1, "y": -3 }
            ]
        },
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {"crop_tier": "medium"}
            }
        ]
    },
    "Laurie the Chuckle Crow": {
        "id": 468,
        "description": "With her disconcerting chuckle, she shooes peckers away from your crops!",
        "boost_category": "Crop",
        "size": { "width": 1, "height": 1 },
        "aoe": {
            "shape": "custom",
            "plots": [
                # Linha 1 (imediatamente abaixo do espantalho)
                { "x": -1, "y": -1 }, { "x": 0, "y": -1 }, { "x": 1, "y": -1 },
                # Linha 2
                { "x": -1, "y": -2 }, { "x": 0, "y": -2 }, { "x": 1, "y": -2 },
                # Linha 3
                { "x": -1, "y": -3 }, { "x": 0, "y": -3 }, { "x": 1, "y": -3 }
            ]
        },
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {"crop_tier": "advanced"}
            }
        ]
    },
    "Nancy": {
        "id": 420,
        "description": "A brave scarecrow that keeps your crops safe from crows. Ensures your crops grow faster when placed on your farm.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.15,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            }
        ]
    },
    "Scarecrow": {
        "id": 404,
        "description": "Ensures your crops grow faster when placed on your farm.\n\nRumour has it that it is crafted with a Goblin head from the great war.\n\nIncludes boosts from [Nancy](https://opensea.io/assets/matic/0x22d5f9b75c524fec1d6619787e582644cd4d7422/420).",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.15,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            },
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.20,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            }
        ]
    },
    "Kuebiko": {
        "id": 421,
        "description": "An extremely rare item in Sunflower Land. This scarecrow cannot move but has in-depth knowledge of the history of the Sunflower Wars.\n\nThis scarecrow is so scary that it even frightens Bumpkins. If you have this item, all seeds are free from the market.\n\nIncludes boosts from [Scarecrow](https://opensea.io/assets/matic/0x22d5f9b75c524fec1d6619787e582644cd4d7422/404) and [Nancy](https://opensea.io/assets/matic/0x22d5f9b75c524fec1d6619787e582644cd4d7422/420).",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.15,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            },
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.20,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            },
            {
                "type": "SEED_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {"category": "Seed"}
            }
        ]
    },
    "Gnome": {
        "id": 407,
        "description": "A lucky gnome. Currently used for decoration purposes\n\n~~You can craft a gnome at the Goblin Blacksmith in the game.~~ **Sold out!**",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.10,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            }
        ],
        "aoe": {
            "shape": "custom",
            "plots": [{"x": 0, "y": -1}]
        }
    },
    "Sir Goldensnout": {
        "id": 466,
        "description": "A royal member, Sir GoldenSnout infuses your farm with sovereign prosperity through its golden manure.",
        "boost_category": "Crop",
        "size": { "width": 2, "height": 2 },
        "aoe": {
            "shape": "custom",
            "plots": [
                # CORREÇÃO: Área de 4x4 deslocada, conforme collisionDetection.ts
                # Coordenadas relativas à posição (X, Y) do item.
                # Gera as 16 coordenadas (de x=-1 a x=2 e de y=-2 a y=1)
                *[{ "x": dx, "y": dy } for dy in range(-2, 2) for dx in range(-1, 3)]
            ]
        },
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            }
        ]
    },
    "Lunar Calendar": {
        "id": 448,
        "description": "Crops now follow the lunar cycle! 10% reduction in growth time.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.10,
                "conditions": {
                    "resource": ["Sunflower", "Potato", "Pumpkin", "Carrot", "Cabbage", "Beetroot", "Cauliflower", "Parsnip", "Radish", "Wheat", "Kale", "Rhubarb", "Zucchini", "Yam", "Broccoli", "Pepper", "Onion", "Turnip", "Artichoke", "Barley", "Corn", "Soybean"]
                }
            }
        ]
    },
    "Peeled Potato": {
        "id": 433,
        "description": "A prized possession. Discover a bonus potato 20% of harvests.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "resource": ["Potato"]
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {
                    "resource": ["Potato"]
                }
            }
        ]
    },
    "Victoria Sisters": {
        "id": 432,
        "description": "A Halloween collectible. Increase Pumpkin yield by 20% and summon the necromancer.\n\nTo craft this item you must collect 50 Jack-o-lantern's and trade with the Traveling Salesman.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.20,
                "conditions": {
                    "resource": ["Pumpkin"]
                }
            }
        ]
    },
    "Freya Fox": {
        "id": 469,
        "description": "Enchanting guardian, boosts pumpkin growth with her mystical charm. Harvest abundant pumpkins under her watchful gaze.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {
                    "resource": ["Pumpkin"]
                }
            }
        ]
    },
    "Easter Bunny": {
        "id": 909,
        "description": "A limited edition bunny that can be crafted by those who collect all 7 eggs in the Easter Egg Hunt.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.20,
                "conditions": {
                    "resource": ["Carrot"]
                }
            }
        ]
    },
    "Pablo The Bunny": {
        "id": 926,
        "description": "The magical bunny that increases your carrot harvests",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": ["Carrot"]
                }
            }
        ]
    },
    "Cabbage Boy": {
        "id": 434,
        "description": "Don't wake the baby!",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "resource": ["Cabbage"],
                }
            },
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {
                    "resource": ["Cabbage"],
                    "placed": "Cabbage Girl"
                }
            }
        ]
    },
    "Cabbage Girl": {
        "id": 435,
        "description": "Don't wake the baby!",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "crop": "Cabbage"
                }
            }
        ]
    },
    "Karkinos": {
        "id": 455,
        "description": "Pinchy but kind, the crabby cabbage-boosting addition to your farm!",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "crop": "Cabbage"
                }
            }
        ]
    },
    "Golden Cauliflower": {
        "id": 410,
        "description": "It is rumoured that a farmer created a golden fertiliser which produced this magical Cauliflower.\n\nFor some reason, when this Cauliflower is on your farm you receive twice the rewards from growing Cauliflowers.\n\n~~You can craft a Golden Cauliflower at the Goblin Farmer in the game.~~ **Sold out!**",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "multiply",
                "value": 2,
                "conditions": {
                    "crop": "Cauliflower"
                }
            }
        ]
    },
    "Mysterious Parsnip": {
        "id": 418,
        "description": "No one knows where this parsnip came from, but when it is on your farm Parsnips grow 50% faster.\n\n~~You can craft this item at the Goblin Farmer in the game.~~ **Sold out!**",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "crop": "Parsnip"
                }
            }
        ]
    },
    "Purple Trail": {
        "id": 457,
        "description": "Leave your opponents in a trail of envy with the mesmerizing and unique Purple Trail",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "crop": "Eggplant"
                }
            }
        ]
    },
    "Obie": {
        "id": 458,
        "description": "A fierce eggplant soldier",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "crop": "Eggplant"
                }
            }
        ]
    },
    "Maximus": {
        "id": 459,
        "description": "Squash the competition with plump Maximus",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "crop": "Eggplant"
                }
            }
        ]
    },
    "Poppy": {
        "id": 471,
        "description": "The mystical corn kernel. +0.1 Corn per harvest.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "crop": "Corn"
                }
            }
        ]
    },
    "Kernaldo": {
        "id": 473,
        "description": "The magical corn whisperer.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "crop": "Corn"
                }
            }
        ]
    },
    "Queen Cornelia": {
        "id": 474,
        "description": "Command the regal power of Queen Cornelia and experience a magnificent Area of Effect boost to your corn production. +1 Corn.",
        "boost_category": "Crop",
        "size": { "width": 1, "height": 2 },
        "aoe": {
            "shape": "custom",
            "plots": [
                # CORREÇÃO: Área retangular de 3x4, conforme collisionDetection.ts
                # Coordenadas relativas à posição (X, Y) do item.
                # Gera as 12 coordenadas (de x=-1 a x=1 e de y=-2 a y=1)
                *[{ "x": dx, "y": dy } for dy in range(-2, 2) for dx in range(-1, 2)]
            ]
        },
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "crop": "Corn"
                }
            }
        ]
    },
    "Foliant": {
        "id": 1227,
        "description": "A book of spells.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "crop": "Kale"
                }
            }
        ]
    },
    "Hoot": {
        "id": 461,
        "description": "Hoot hoot! Have you solved my riddle yet?",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {
                    "crop": ["Radish", "Wheat", "Kale", "Rice", "Barley"]
                }
            }
        ]
    },
    "Hungry Caterpillar": {
        "id": 493,
        "description": "Munching through leaves, the Hungry Caterpillar is always ready for a tasty adventure.",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "SEED_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "category": "Flower"
                }
            }
        ]
    },
    "Turbo Sprout": {
        "id": 495,
        "description": "An engine that reduces the Greenhouse's growth time by 50%.",
        "boost_category": ["Crop", "Fruit"],
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.5,
                "conditions": {
                    "building": "Greenhouse"
                }
            }
        ]
    },
    "Soybliss": {
        "id": 496,
        "description": "A unique soy creature that gives +1 Soybean yield.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "crop": "Soybean"
                }
            }
        ]
    },
    "Grape Granny": {
        "id": 497,
        "description": "Wise matriarch nurturing grapes to flourish with +1 yield.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "crop": "Grape"
                }
            }
        ]
    },
    "Vinny": {
        "id": 2016,
        "description": "Vinny, a friendly grapevine, is always ready for a chat.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "crop": "Grape"
                }
            }
        ]
    },
    "Rice Panda": {
        "id": 2034,
        "description": "A smart panda never forgets to water the rice.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "crop": "Rice"
                }
            }
        ]
    },
    # Fruit Boosts
    "Immortal Pear": {
        "id": 441,
        "description": "This long-lived pear ensures your fruit tree survives +1 bonus harvest.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "EXTRA_HARVEST",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Fruit"
                }
            }
        ]
    },
    "Black Bearry": {
        "id": 444,
        "description": "His favorite treat - plump, juicy blueberries. Gobbles them up by the handful! +1 Blueberry each Harvest",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "crop": "Blueberry"
                }
            }
        ]
    },
    "Squirrel Monkey": {
        "id": 443,
        "description": "A natural orange predator. Orange Trees are scared when a Squirrel Monkey is around. 1/2 Orange Tree grow time.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "crop": "Orange"
                }
            }
        ]
    },
    "Lady Bug": {
        "id": 442,
        "description": "An incredible bug that feeds on aphids. Improves Apple quality. +0.25 Apples each harvest",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "crop": "Apple"
                }
            }
        ]
    },
    "Banana Chicken": {
        "id": 488,
        "description": "A chicken that boosts bananas. What a world we live in.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "crop": "Banana"
                }
            }
        ]
    },
    "Nana": {
        "id": 487,
        "description": "This rare beauty is a surefire way to boost your banana harvests.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.10,
                "conditions": {
                    "crop": "Banana"
                }
            }
        ]
    },

    # Mutant Crops
    "Carrot Sword": {
        "id": 419,
        "description": "Legend has it that only a true farmer can yield this sword.\n\nIncreases the chance of finding a mutant crop by 300%!\n\n~~You can craft this item at the Goblin Farmer in the game.~~ **Sold out!**",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "MUTANT_CHANCE",
                "operation": "multiply",
                "value": 4, # 300% increase means 4x the chance
                "conditions": {
                    "category": "Crop"
                }
            }
        ]
    },
    "Stellar Sunflower": {
        "id": 437,
        "description": "Stellar! Grants a 3% chance to get +10 sunflowers on harvest.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 10,
                "conditions": {
                    "crop": "Sunflower"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.03,
                "conditions": {
                    "crop": "Sunflower"
                }
            }
        ]
    },
    "Potent Potato": {
        "id": 438,
        "description": "Potent! Grants a 3% chance to get +10 potatoes on harvest.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 10,
                "conditions": {
                    "crop": "Potato"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.03,
                "conditions": {
                    "crop": "Potato"
                }
            }
        ]
    },
    "Radical Radish": {
        "id": 439,
        "description": "Radical! Grants a 3% chance to get +10 radishes on harvest.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 10,
                "conditions": {
                    "crop": "Radish"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.03,
                "conditions": {
                    "crop": "Radish"
                }
            }
        ]
    },
    "Lab Grown Pumpkin": {
        "id": 476,
        "description": "A lab grown pumpkin! +0.3 Pumpkin Yield.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.3,
                "conditions": {
                    "crop": "Pumpkin"
                }
            }
        ]
    },
    "Lab Grown Carrot": {
        "id": 475,
        "description": "A lab grown carrot! +0.2 Carrot Yield.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "crop": "Carrot"
                }
            }
        ]
    },
    "Lab Grown Radish": {
        "id": 477,
        "description": "A lab grown radish! +0.4 Radish Yield.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.4,
                "conditions": {
                    "crop": "Radish"
                }
            }
        ]
    },
    # Animals
    "Fat Chicken": {
        "id": 611,
        "description": "A mutant chicken that can be found by chance when collecting an egg.\n\nThis mutant reduces the food required to feed a chicken by 10%.\n\nThere is a 1/1000 chance of producing a mutant chicken.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "FEED_COST",
                "operation": "percentage",
                "value": -0.10,
                "conditions": {
                    "animal": "Chicken"
                }
            }
        ]
    },
    "Rich Chicken": {
        "id": 612,
        "description": "A mutant chicken that can be found by chance when collecting an egg.\n\nThis mutant adds a boost of +0.1 egg yield.\n\nThere is a 1/1000 chance of producing a mutant chicken.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Egg"
                }
            }
        ]
    },
    "Speed Chicken": {
        "id": 610,
        "description": "A mutant chicken that can be found by chance when collecting an egg.\n\nThis mutant increases the speed of egg production by 10%.\n\nThere is a 1/1000 chance of producing a mutant chicken.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PRODUCE_TIME",
                "operation": "percentage",
                "value": -0.10,
                "conditions": {
                    "resource": "Egg"
                }
            }
        ]
    },
    "Ayam Cemani": {
        "id": 445,
        "description": "The rarest chicken in Sunflower Land. This mutant adds a boost of +0.2 egg yield.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "resource": "Egg"
                }
            }
        ]
    },
    "El Pollo Veloz": {
        "id": 470,
        "description": "Give me those eggs, fast! Chickens sleep 2 hours shorter.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PRODUCE_TIME",
                "operation": "subtract_hours",
                "value": 2,
                "conditions": {
                    "resource": "Egg"
                }
            }
        ]
    },
    "Rooster": {
        "id": 613,
        "description": "Rooster increases the chance of getting a mutant chicken 2x.\n\nYou can craft this item at the Goblin Farmer in the game.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "MUTANT_CHANCE",
                "operation": "multiply",
                "value": 2,
                "conditions": {
                    "animal": "Chicken"
                }
            }
        ]
    },
    "Undead Rooster": {
        "id": 1114,
        "description": "An unfortunate casualty of the war. +0.1 egg yield.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Egg"
                }
            }
        ]
    },
    "Chicken Coop": {
        "id": 408,
        "description": "A chicken coop that can be used to raise chickens. Increase egg production with this rare coop.\n\n~~You can craft a chicken coop at the Goblin Farmer in the game.~~ **Sold out!**",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "resource": "Egg"
                }
            },
            {
                "type": "BASE_CAPACITY",
                "operation": "add",
                "value": 5,
                "conditions": {
                    "animal": "Chicken"
                }
            },
            {
                "type": "UPGRADE_CAPACITY",
                "operation": "add",
                "value": 5,
                "conditions": {
                    "animal": "Chicken"
                }
            }
        ]
    },
    "Farm Dog": {
        "id": 406,
        "description": "Sheep are no longer lazy when this farm dog is around.\n\n~~You can craft a dog at the Goblin Farmer in the game.~~ **Sold out!**",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PRODUCE_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "animal": "Sheep"
                }
            }
        ]
    },
    "Gold Egg": {
        "id": 409,
        "description": "A golden egg. What lays inside is known to be the bearer of good fortune.\n\n\n\nFeed chickens for free.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "FEED_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "animal": "Chicken"
                }
            }
        ]
    },
    "Bale": {
        "id": 465,
        "description": "A poultry's favorite neighbor, providing a cozy retreat for chickens",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Egg"
                }
            }
        ]
    },

    # Resources
    "Woody the Beaver": {
        "id": 415,
        "description": "During the great wood shortage, Bumpkins created an alliance with the Beaver population.\n\nIncreases wood production by 20%.\n\nYou can craft this item at the Goblin Blacksmith in the game.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "multiply",
                "value": 1.2,
                "conditions": {
                    "resource": "Wood"
                }
            }
        ]
    },
    "Apprentice Beaver": {
        "id": 416,
        "description": "A well trained Beaver who has aspirations of creating a wood monopoly.\n\nIncreases wood replenishment rates.\n\n~~You can craft this item at the Goblin Blacksmith in the game.~~ **Sold out!**\n\nIncludes boosts from [Woody the Beaver](https://opensea.io/assets/matic/0x22d5f9b75c524fec1d6619787e582644cd4d7422/415).",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "multiply",
                "value": 1.2,
                "conditions": {
                    "resource": "Wood"
                }
            },
            {
                "type": "RECOVERY_TIME",
                "operation": "percentage",
                "value": -0.5,
                "conditions": {
                    "resource": "Tree"
                }
            }
        ]
    },
    "Foreman Beaver": {
        "id": 417,
        "description": "A master of construction, carving and all things wood related.\n\nChop trees without axes.\n\nIncludes boosts from [Apprentice Beaver](https://opensea.io/assets/matic/0x22d5f9b75c524fec1d6619787e582644cd4d7422/416) and [Woody the Beaver](https://opensea.io/assets/matic/0x22d5f9b75c524fec1d6619787e582644cd4d7422/415).",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "multiply",
                "value": 1.2,
                "conditions": {
                    "resource": "Wood"
                }
            },
            {
                "type": "RECOVERY_TIME",
                "operation": "percentage",
                "value": -0.5,
                "conditions": {
                    "resource": "Tree"
                }
            },
            {
                "type": "NO_TOOL_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "tool": "Axe"
                }
            }
        ]
    },
    "Wood Nymph Wendy": {
        "id": 436,
        "description": "Cast an enchantment to entice the wood fairies.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "resource": "Wood"
                }
            }
        ]
    },
    "Tiki Totem": {
        "id": 447,
        "description": "The Tiki Totem adds 0.1 wood to every tree you chop.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Wood"
                }
            }
        ]
    },
    "Tunnel Mole": {
        "id": 428,
        "description": "The tunnel mole gives a 0.25 increase to stone mines' yield.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "resource": "Stone"
                }
            }
        ]
    },
    "Rocky the Mole": {
        "id": 429,
        "description": "\"Life's not about how much iron you can mine... it's about how much more you can mine, and still keep mining.\" - Rocky the Mole\n\nRocky the Mole gives a 0.25 increase to iron mines' yield.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "resource": "Iron"
                }
            }
        ]
    },
    "Nugget": {
        "id": 430,
        "description": "Seldom seen above ground, this gold digger burrows day and night searching for the next gold rush.\n\nStrike gold with this little critter! Eureka!\n\nNugget gives a 0.25 increase to gold mines' yield.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "resource": "Gold"
                }
            }
        ]
    },
    "Rock Golem": {
        "id": 427,
        "description": "The Rock Golem is the protector of Stone.\n\nMining stone causes the Golem to be become enraged giving a 10% chance to get +2 Stone from stone mines.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {
                    "resource": "Stone"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {
                    "resource": "Stone"
                }
            }
        ]
    },
    "Iron Idol": {
        "id": 454,
        "description": "The Idol adds 1 iron every time you mine iron.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "resource": "Iron"
                }
            }
        ]
    },
    "Tin Turtle": {
        "id": 464,
        "description": "The Tin Turtle gives +0.1 to Stones you mine within its Area of Effect.",
        "boost_category": "Resource",
        "aoe": {
            "shape": "circle",
            "radius": 1
        },
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Stone"
                }
            }
        ]
    },
    "Emerald Turtle": {
        "id": 463,
        "description": "The Emerald Turtle gives +0.5 to any minerals you mine within its Area of Effect.",
        "boost_category": "Resource",
        "aoe": {
            "shape": "circle",
            "radius": 1
        },
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {
                    "resource": ["Stone", "Iron", "Gold"]
                }
            }
        ]
    },
    "Crimson Carp": {
        "id": 1537,
        "description": "A rare, vibrant jewel of the Spring waters.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.05,
                "conditions": {
                    "resource": "Crimstone"
                }
            }
        ]
    },
    "Battle Fish": {
        "id": 1538,
        "description": "The rare armored swimmer of faction season!",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.05,
                "conditions": {
                    "resource": "Oil"
                }
            }
        ]
    },
    "Lemon Shark": {
        "id": 1539,
        "description": "A zesty, zippy swimmer of the Summer seas. Only available during Pharaoh's Treasure season.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "crop": "Lemon"
                }
            }
        ]
    },
    "Longhorn Cowfish": {
        "id": 1540,
        "description": "A peculiar boxfish with horn-like spines, swimming through the seas with bovine grace.",
        "boost_category": "Milk",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "resource": "Milk"
                }
            }
        ]
    },
    "Crim Peckster": {
        "id": 494,
        "description": "A gem detective with a knack for unearthing Crimstones.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Crimstone"
                }
            }
        ]
    },
    "Knight Chicken": {
        "id": 500,
        "description": "A strong and noble chicken boosting your oil yield.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Oil"
                }
            }
        ]
    },
    "Mushroom House": {
        "id": 456,
        "description": "A whimsical, fungi-abode where the walls sprout with charm and even the furniture has a 'spore-tacular' flair!",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "resource": "Mushroom"
                }
            }
        ]
    },
    "Queen Bee": {
        "id": 491,
        "description": "Majestic ruler of the hive, the Queen Bee buzzes with regal authority.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "PRODUCE_TIME",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "resource": "Honey"
                }
            }
        ]
    },
    "Humming Bird": {
        "id": 490,
        "description": "A tiny jewel of the sky, the Humming Bird flits with colorful grace.",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {
                    "category": "Flower"
                }
            },
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Flower"
                }
            }
        ]
    },
    "Beehive": {
        "id": 633,
        "description": "A bustling beehive, producing honey from actively growing flowers; 10% chance upon Honey harvest to summon a bee swarm which will pollinate all growing crops with a +0.2 boost!",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {
                    "category": "Crop"
                }
            },
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "category": "Crop"
                }
            }
        ]
    },
    "Pharaoh Chicken": {
        "id": 2116,
        "description": "A ruling chicken, +1 Dig.",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "DAILY_DIGS",
                "operation": "add",
                "value": 1,
                "conditions": {}
            }
        ]
    },
    # Fish
    "Skill Shrimpy": {
        "id": 485,
        "description": "Shrimpy's here to help! He'll ensure you get that extra XP from fish.",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "XP",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {
                    "category": "Fish"
                }
            }
        ]
    },
    "Walrus": {
        "id": 478,
        "description": "With his trusty tusks and love for the deep, he'll ensure you reel in an extra fish every time",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Fish"
                }
            }
        ]
    },
    "Alba": {
        "id": 479,
        "description": "With her keen instincts, she ensures you get a little extra splash in your catch. 50% chance of +1 Basic Fish!",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Basic Fish"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.50,
                "conditions": {
                    "category": "Basic Fish"
                }
            }
        ]
    },

    # Other
    "Soil Krabby": {
        "id": 486,
        "description": "Speedy sifting with a smile! Enjoy a 10% composter speed boost with this crustaceous champ.",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "COMPOST_TIME",
                "operation": "percentage",
                "value": -0.10,
                "conditions": {}
            }
        ]
    },
    "Knowledge Crab": {
        "id": 480,
        "description": "The Knowledge Crab doubles your Sprout Mix effect, making your soil treasures as rich as sea plunder!",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "FERTILISER_EFFECT",
                "operation": "multiply",
                "value": 2,
                "conditions": {
                    "fertiliser": "Sprout Mix"
                }
            }
        ]
    },
    "Maneki Neko": {
        "id": 446,
        "description": "The beckoning cat. Pull its arm and good luck will come. A special event item from Lunar New Year!",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "DAILY_FREE_FOOD",
                "operation": "add",
                "value": 1,
                "conditions": {}
            }
        ]
    },
    "Treasure Map": {
        "id": 449,
        "description": "An enchanted map that leads the holder to valuable treasure. +20% profit from beach bounty items.",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "SELL_PRICE",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {
                    "category": "Beach Bounty"
                }
            }
        ]
    },
    "Heart of Davy Jones": {
        "id": 450,
        "description": "Whoever possesses it holds immense power over the seven seas, can dig for treasure without tiring.",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "DAILY_DIGS",
                "operation": "add",
                "value": 20,
                "conditions": {}
            }
        ]
    },
    "Genie Lamp": {
        "id": 460,
        "description": "A magical lamp that contains a genie who will grant you three wishes and burn the lamp after the third wish. Wish list: Genie Bear, Pirate Bounty, Pearl, Bumpkin Roast, Goblin Brunch and Sand Drill x10",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "WISHES",
                "operation": "add",
                "value": 3,
                "conditions": {}
            }
        ]
    },
    "Grain Grinder": {
        "id": 472,
        "description": "Grind your grain and experience a delectable surge in Cake XP.",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "XP",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {
                    "category": "Cake"
                }
            }
        ]
    },
    "Observatory": {
        "id": 911,
        "description": "A limited edition Observatory gained from completing the mission from Million on Mars x Sunflower Land crossover event.",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "XP",
                "operation": "percentage",
                "value": 0.05,
                "conditions": {}
            }
        ]
    },
    "Blossombeard": {
        "id": 2010,
        "description": "The Blossombeard Gnome is a powerful companion for your farming adventures.",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "XP",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {}
            }
        ]
    },
    "Desert Gnome": {
        "id": 2017,
        "description": "A gnome that can survive the harshest of conditions.",
        "boost_category": "Cooking",
        "boosts": [
            {
                "type": "COOKING_TIME",
                "operation": "percentage",
                "value": -0.10,
                "conditions": {}
            }
        ]
    },
    "Christmas Tree": {
        "id": 403,
        "description": "Place on your farm during the Festive Season to get a spot and Santa's nice list!",
        "boost_category": "Other",
        "boosts": [] # Sem boost específico definido nos atributos
    },
    "Festive Tree": {
        "id": 1299,
        "description": "A festive tree that can be attained each festive season. I wonder if it is big enough for santa to see?",
        # A descrição sugere um boost, mas não há um `trait_type` de boost nos atributos
        "boost_category": None, 
        "boosts": []
    },
    "Grinx's Hammer": {
        "id": 489,
        "description": "The magical hammer from Grinx, the legendary Goblin Blacksmith. Halves expansion natural resource requirements.",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "EXPANSION_COST",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "category": "Resource"
                }
            }
        ]
    },
    "Time Warp Totem": {
        "id": 1297,
        "description": "The Time Warp Totem temporarily boosts your cooking, crops, fruits, trees & mineral time. Make the most of it!",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "GLOBAL_RECOVERY_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "duration_hours": 2,
                    "resource": ["Stone Rock", "Iron Rock", "Gold Rock", "Tree", "Crop", "Fruit Patchs", "COOKING_BUILD"]
                },
                "is_temporal": True
            }
        ]
    },

    # Marine Marvels with Boosts
    "Radiant Ray": {
        "id": 1530,
        "description": "A ray that prefers to glow in the dark, with a shimmering secret to share.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Iron"
                }
            }
        ]
    },
    "Gilded Swordfish": {
        "id": 1532,
        "description": "A swordfish with scales that sparkle like gold, the ultimate catch!",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Gold"
                }
            }
        ]
    },
    "Flower Fox": {
        "id": 492,
        "description": "The Flower Fox, a playful creature adorned with petals, brings joy to the garden.",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.10,
                "conditions": {
                    "category": "Flower"
                }
            }
        ]
    },
    "Hungry Hare": {
        "id": 938,
        "description": "This ravenous rabbit hops through your farm. A special event item from Easter 2024",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "XP",
                "operation": "multiply",
                "value": 2, # 100% increase
                "conditions": {
                    "food": "Fermented Carrots"
                }
            }
        ]
    },
    # Faction Shop
    "Gourmet Hourglass": {
        "id": 2071,
        "description": "Reduces cooking time by 50% for 4 hours.",
        "boost_category": "Cooking",
        "boosts": [
            {
                "type": "COOKING_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "duration_hours": 4,
                },
                "is_temporal": True
            }
        ]
    },
    "Harvest Hourglass": {
        "id": 2072,
        "description": "Reduces crop growth time by 25% for 6 hours.",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "category": "Crop",
                    "duration_hours": 6,
                },
                "is_temporal": True
            }
        ]
    },
    "Timber Hourglass": {
        "id": 2073,
        "description": "Reduces tree recovery time by 25% for 4 hours.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "RECOVERY_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "resource": "Tree",
                    "duration_hours": 4,
                },
                "is_temporal": True
            }
        ]
    },
    "Ore Hourglass": {
        "id": 2074,
        "description": "Reduces mineral replenish cooldown by 50% for 3 hours.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "RECOVERY_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "category": "Mineral",
                    "duration_hours": 3,
                },
                "is_temporal": True
            }
        ]
    },
    "Orchard Hourglass": {
        "id": 2075,
        "description": "Reduces fruit growth time by 25% for 6 hours.",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "category": "Fruit",
                    "duration_hours": 6,
                },
                "is_temporal": True
            }
        ]
    },
    "Fisher's Hourglass": {
        "id": 2077,
        "description": "Gives a 50% chance of +1 fish for 4 hours.",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Fish",
                    "duration_hours": 4,
                },
                "is_temporal": True
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.50,
                "conditions": {
                    "category": "Fish",
                    "duration_hours": 4,
                },
                "is_temporal": True
            }
        ]
    },
    "Blossom Hourglass": {
        "id": 2076,
        "description": "Reduces flower growth time by 25% for 4 hours.",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "category": "Flower",
                    "duration_hours": 4,
                },
                "is_temporal": True
            }
        ]
    },
    "Desert Rose": {
        "id": 2100,
        "description": "A mutant flower that can be found during the Pharaoh's Treasure season.",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Flower"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {
                    "category": "Flower"
                }
            }
        ]
    },
    "Chicory": {
        "id": 2159,
        "description": "A mutant flower that can be found during the Bull Run season.",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "CRITICAL_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Flower"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.10,
                "conditions": {
                    "category": "Flower"
                }
            }
        ]
    },
    "Pharaoh Gnome": {
        "id": 2120,
        "description": "",
        "boost_category": ["Crop", "Fruit"],
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {
                    "building": "Greenhouse"
                }
            }
        ]
    },
    "Lemon Tea Bath": {
        "id": 2121,
        "description": "",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "crop": "Lemon"
                }
            }
        ]
    },
    "Tomato Clown": {
        "id": 2122,
        "description": "",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "crop": "Tomato"
                }
            }
        ]
    },
    "Cannonball": {
        "id": 2105,
        "description": "Cannonball is ferocious being. Residing in Tomato Bombard, it's ready to strike anyone who gets in its way",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "crop": "Tomato"
                }
            }
        ]
    },
    "Tomato Bombard": {
        "id": 2128,
        "description": "Home to Cannonball, and is ready to strike anyone who gets in its way",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "crop": "Tomato"
                }
            }
        ]
    },
    "Camel": {
        "id": 2127,
        "description": "A mean looking camel!",
        "boost_category": "Treasure",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "resource": "Sand"
                }
            },
            {
                "type": "SELL_PRICE",
                "operation": "percentage",
                "value": 0.30,
                "conditions": {
                    "category": "Artefact Shop Bounty"
                }
            }
        ]
    },
    "Reveling Lemon": {
        "id": 2109,
        "description": "",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "crop": "Lemon"
                }
            }
        ]
    },
    "Lemon Frog": {
        "id": 2114,
        "description": "",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "GROWTH_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "crop": "Lemon"
                }
            }
        ]
    },
    "Stone Beetle": {
        "id": 2129,
        "description": "Beetle made of stone. +0.1 Stone",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Stone"
                }
            }
        ]
    },
    "Iron Beetle": {
        "id": 2130,
        "description": "Beetle made of iron. +0.1 Iron",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Iron"
                }
            }
        ]
    },
    "Gold Beetle": {
        "id": 2131,
        "description": "Beetle made of gold. +0.1 Gold",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Gold"
                }
            }
        ]
    },
    "Fairy Circle": {
        "id": 2132,
        "description": "Circle of fairy mushrooms. +0.2 Wild Mushroom",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {
                    "resource": "Wild Mushroom"
                }
            }
        ]
    },
    "Squirrel": {
        "id": 2133,
        "description": "Squirrel likes hanging out in the forest. +0.1 Wood",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Wood"
                }
            }
        ]
    },
    "Butterfly": {
        "id": 2135,
        "description": "Butterfly loves the scent of flowers. 20% chance of +1 Flower",
        "boost_category": "Flower",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Flower"
                }
            },
            {
                "type": "CRITICAL_CHANCE",
                "operation": "percentage",
                "value": 0.20,
                "conditions": {
                    "category": "Flower"
                }
            }
        ]
    },
    "Macaw": {
        "id": 2134,
        "description": "Macaw loves picking fruits. +0.1 Fruit Patch Yield",
        "boost_category": "Fruit",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "category": "Fruit Patch"
                }
            }
        ]
    },
    # Bull Run
    "Sheaf of Plenty": {
        "id": 2152,
        "description": "A bundle of barley harvested at peak ripeness, symbolizing abundance and the hard work of the season. +2 Barley",
        "boost_category": "Crop",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {
                    "crop": "Barley"
                }
            }
        ]
    },
    "Moo-ver": {
        "id": 2155,
        "description": "A unique contraption that keeps cows active and healthy. +0.25 Leather",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "resource": "Leather"
                }
            }
        ]
    },
    "Swiss Whiskers": {
        "id": 2156,
        "description": "A culinary genius in miniature form, this skilled chef elevates every cheese recipe with his expert touch. +500 Cheese Recipe XP",
        "boost_category": "XP",
        "boosts": [
            {
                "type": "XP",
                "operation": "add",
                "value": 500,
                "conditions": {
                    "category": "Cheese"
                }
            }
        ]
    },
    "Cluckulator": {
        "id": 2157,
        "description": "This specialized scale accurately weighs each chicken, ensuring they receive the ideal feed portion for balanced growth and health, making poultry care more efficient and sustainable. -25% Feed to Chicken",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "FEED_COST",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "animal": "Chicken"
                }
            }
        ]
    },
    "Alien Chicken": {
        "id": 2162,
        "description": "A peculiar chicken from another galaxy, here to boost your feather production!",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Feather"
                }
            }
        ]
    },
    "Toxic Tuft": {
        "id": 2164,
        "description": "A mutated sheep whose toxic fleece produces the finest merino wool in the land!",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Merino Wool"
                }
            }
        ]
    },
    "Mootant": {
        "id": 2163,
        "description": "This genetically enhanced bovine here to boost your leather production!",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": "Leather"
                }
            }
        ]
    },
    "King of Bears": {
        "id": 2154,
        "description": "The king of all bears. It has the power to generate more honey for its own consumption.",
        "boost_category": "Resource",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.25,
                "conditions": {
                    "resource": "Honey",
                    "requirement": "Full Beehive"
                }
            }
        ]
    },
    "Super Totem": {
        "id": 2168,
        "description": "2x speed for crops, trees, fruits, cooking & minerals. Lasts for 7 days",
        "boost_category": "Other",
        "boosts": [
            {
                "type": "SUPER_TOTEM_TIME_BOOST", # <-- NOVO TIPO ESPECÍFICO
                "operation": "percentage",
                "value": -0.50,
                "conditions": {
                    "duration_days": 7,
                },
                "is_temporal": True
            }
        ]
    },
    "Golden Cow": {
        "id": 2178,
        "description": "Feed cows for free!",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "FEED_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "animal": "Cow"
                }
            }
        ]
    },
    "Volcano Gnome": {
        "id": 2018,
        "description": "A mineral obsessed gnome that can survive the harshest of conditions.",
        "boost_category": "Minerals",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {
                    "resource": ["Stone", "Iron", "Gold"]
                }
            }
        ]
    },
    "Mammoth": {
        "id": 2191,
        "description": "An ancient giant, standing strong through the test of time.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PRODUCE_TIME",
                "operation": "percentage",
                "value": -0.25,
                "conditions": {
                    "animal": "Cow"
                }
            }
        ]
    },
    "Frozen Sheep": {
        "id": 2200,
        "description": "A frosty sheep mutation that prevents sheep from getting sick during winter months!",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PREVENT_SICKNESS",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "animal": "Sheep",
                    "season": "Winter"
                }
            }
        ]
    },
    "Jellyfish": {
        "id": 2203,
        "description": "A marine marvel from the Winds of Change chapter that grants +1 fish during summer months!",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Fish",
                    "season": "Summer"
                }
            }
        ]
    },
    "Frozen Cow": {
        "id": 2199,
        "description": "A frosty bovine mutation that prevents cows from getting sick during winter months!",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PREVENT_SICKNESS",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "animal": "Cow",
                    "season": "Winter"
                }
            }
        ]
    },
    "Summer Chicken": {
        "id": 2201,
        "description": "A chicken mutation that prevents chickens from getting sick during summer months!",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PREVENT_SICKNESS",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "animal": "Chicken",
                    "season": "Summer"
                }
            }
        ]
    },
    "Golden Sheep": {
        "id": 2193,
        "description": "A dazzling wonder, worth more than its weight in wool. Feed Sheeps for free!",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "FEED_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "animal": "Sheep"
                }
            }
        ]
    },
    "Barn Blueprint": {
        "id": 2194,
        "description": "The foundation of every great farm begins with a solid plan.",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "BASE_CAPACITY",
                "operation": "add",
                "value": 5,
                "conditions": {
                    "building": "Barn"
                }
            },
            {
                "type": "UPGRADE_CAPACITY",
                "operation": "add",
                "value": 5,
                "conditions": {
                    "building": "Barn"
                }
            }
        ]
    },
    "Giant Yam": {
        "id": 2268,
        "description": "A root so massive it could feed a village—or at least make one impressive stew.",
        "boost_category": "Crop",
        "boosts": [
        {
            "type": "YIELD",
            "operation": "add",
            "value": 0.5,
            "conditions": {
                "crop": "Yam"
            }
        }
    ]
    },
    "Giant Zucchini": {
        "id": 2270,
        "description": "Impossibly large and suspiciously green, this veggie is a true garden marvel.",
        "boost_category": "Crop",
        "boosts": [
        {
            "type": "GROWTH_TIME",
            "operation": "percentage",
            "value": -0.50,
            "conditions": {
                "crop": "Zucchini"
            }
        }
    ]
    },
    "Giant Kale": {
        "id": 2272,
        "description": "?",
        "boost_category": "Crop",
        "boosts": [
        {
            "type": "YIELD",
            "operation": "add",
            "value": 2.0,
            "conditions": {
                "crop": "Kale"
            }
        }
    ]
    },
    "Obsidian Turtle": {
        "id": 2260,
        "description": "Steady and silent, this ancient creature gathers traces of volcanic stone wherever it roams.",
        "boost_category": "Resource",
        "boosts": [
        {
            "type": "YIELD",
            "operation": "add",
            "value": 0.5,
            "conditions": {
                "resource": "Obsidian"
            }
        }
    ]
    },
    "Quarry": {
        "id": 2259,
        "description": "An age-old stone site that never runs dry—perfect for those seeking a steady supply of free stone.",
        "boost_category": "Resource",
        "boosts": [
        {
                "type": "NO_TOOL_COST",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "tool": "Pickaxe"
                }
            }
    ]
    },
    "Winter Guardian": {
        "id": 2261,
        "description": "Summoned from a land where snow never melts, this frostbound protector now watches over the skies—an honored guest in unfamiliar winds.",
        # Este item não tem um boost explícito nos atributos do arquivo metadata.ts
        "boost_category": None,
        "boosts": []
    },
    "Autumn Guardian": {
        "id": 2264,
        "description": "With harvest hues and a wistful gaze, this Guardian carries the essence of changing seasons from distant lands into the realm above.",
        # Este item não tem um boost explícito nos atributos do arquivo metadata.ts
        "boost_category": None,
        "boosts": []
    },
    "Spring Guardian": {
        "id": 2263,
        "description": "Awakened from fertile fields far below, this gentle spirit now nurtures life among the drifting gardens of the sky.",
        # Este item não tem um boost explícito nos atributos do arquivo metadata.ts
        "boost_category": None,
        "boosts": []
    },
    "Summer Guardian": {
        "id": 2262,
        "description": "A blazing figure born under endless sun, this Guardian brings the heat of its homeland to the cooler heights of Sky Island.",
        # Este item não tem um boost explícito nos atributos do arquivo metadata.ts
        "boost_category": None,
        "boosts": []
    },
    "Nurse Sheep": {
        "id": 2257,
        "description": "A mutant sheep dressed as a caring nurse, prevents sheep from getting sick during summer",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "PREVENT_SICKNESS",
                "operation": "equals",
                "value": 0,
                "conditions": {
                    "animal": "Sheep",
                    "season": "Summer"
                }
            }
        ]
    },
    "Dr Cow": {
        "id": 2256,
        "description": "A mutant cow dressed as a caring doctor, gives 5% less feeding cost for cows",
        "boost_category": "Animal",
        "boosts": [
            {
                "type": "FEED_COST",
                "operation": "percentage",
                "value": -0.05,
                "conditions": {
                    "animal": "Cow"
                }
            }
        ]
    },
    "Pink Dolphin": {
        "id": 2254,
        "description": "A rare dolphin with a beautiful pink hue, increases fish catch by 1 during spring",
        "boost_category": "Fish",
        "boosts": [
            {
                "type": "YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {
                    "category": "Fish",
                    "season": "Spring"
                }
            },
        ]
    },
    "Toolshed": {
        "id": 1011,
        "description": "A Toolshed increases your tool stocks by 50%",
        "boost_category": None,
        "boosts": []
    },
    "Warehouse": {
        "id": 1012,
        "description": "A Warehouse increases your seed stocks by 20%",
        # Este item não tem um boost explícito nos atributos do arquivo metadata.ts
        "boost_category": None,
        "boosts": []
    },
}