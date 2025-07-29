# app/domain/npcs.py
"""
Fonte da Verdade para os dados dos NPCs (Non-Player Characters).

Este módulo centraliza todas as informações sobre os NPCs, incluindo os 
presentes que eles aceitam (com os respectivos pontos de amizade) e as 
recompensas que oferecem ao atingir certos níveis de amizade.

Os dados foram cruzados e compilados a partir dos seguintes ficheiros do jogo:
- gifts.ts: Contém os bónus de flores, pontos padrão e a estrutura de recompensas.
- flowers.ts: Utilizado para validar a lista de flores e os valores base.
"""

NPC_DATA = {
    "betty": {
        "name": "Betty",
        "flowers": {
            "Red Pansy": 5, "Yellow Pansy": 5, "Purple Pansy": 5,
            "White Pansy": 5, "Blue Pansy": 5,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 10,
                    "reward": {"items": {}, "coins": 120, "wearables": {}},
                },
                {
                    "points_required": 20,
                    "reward": {"items": {}, "coins": 960, "wearables": {}},
                },
                {
                    "points_required": 40,
                    "reward": {"items": {"Treasure Key": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 110,
                    "reward": {"items": {"Radish Cake": 1}, "coins": 0, "wearables": {}},
                },
            ],
            "repeats": {
                "points_required": 100,
                "reward": {"items": {"Treasure Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
    "blacksmith": {
        "name": "Blacksmith",
        "flowers": {"Red Carnation": 5},
        "rewards": {
            "planned": [
                {
                    "points_required": 50,
                    "reward": {"items": {"Treasure Key": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 110,
                    "reward": {"items": {}, "coins": 760, "wearables": {}},
                },
                {
                    "points_required": 200,
                    "reward": {"items": {}, "coins": 1600, "wearables": {}},
                },
                {
                    "points_required": 320,
                    "reward": {"items": {"Pickaxe": 10}, "coins": 0, "wearables": {}},
                },
            ],
            "repeats": {
                "points_required": 150,
                "reward": {"items": {"Treasure Key": 1}, "coins": 960, "wearables": {}},
            },
        },
    },
    "bert": {
        "name": "Bert",
        "flowers": {
            "Red Lotus": 6, "Yellow Lotus": 6, "Purple Lotus": 6,
            "White Lotus": 6, "Blue Lotus": 6,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 60,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Tattered Jacket": 1}},
                },
                {
                    "points_required": 100,
                    "reward": {"items": {"Gem": 25}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 210,
                    "reward": {"items": {"Pirate Cake": 3}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 330,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Greyed Glory": 1}},
                },
            ],
            "repeats": {
                "points_required": 150,
                "reward": {"items": {"Rare Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
    "finn": {
        "name": "Finn",
        "flowers": {
            "Red Daffodil": 5, "Yellow Daffodil": 5, "Purple Daffodil": 5,
            "White Daffodil": 5, "Blue Daffodil": 5, "White Cosmos": 5,
            "Blue Cosmos": 5,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 40,
                    "reward": {"items": {"Rod": 10}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 150,
                    "reward": {"items": {}, "coins": 960, "wearables": {}},
                },
            ],
            "repeats": {
                "points_required": 130,
                "reward": {"items": {"Rare Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
    "finley": {
        "name": "Finley",
        "flowers": {
            "Red Daffodil": 5, "Yellow Daffodil": 5, "Purple Daffodil": 5,
            "White Daffodil": 5, "Blue Daffodil": 5,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 25,
                    "reward": {"items": {"Fishing Lure": 3}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 95,
                    "reward": {"items": {}, "coins": 3200, "wearables": {}},
                },
                {
                    "points_required": 150,
                    "reward": {"items": {"Tuna": 5}, "coins": 0, "wearables": {}},
                },
            ],
            "repeats": {
                "points_required": 100,
                "reward": {"items": {"Fishing Lure": 5}, "coins": 0, "wearables": {}},
            },
        },
    },
    "raven": {
        "name": "Raven",
        "flowers": {
            "Purple Carnation": 6, "Purple Lotus": 5, "Purple Daffodil": 4,
            "Purple Pansy": 4, "Purple Cosmos": 4, "Purple Balloon Flower": 4,
            "Purple Gladiolus": 3, "Purple Lavender": 4, "Purple Clover": 3,
            "Purple Edelweiss": 4,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 50,
                    "reward": {"items": {"Time Warp Totem": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 140,
                    "reward": {"items": {}, "coins": 2560, "wearables": {}},
                },
                {
                    "points_required": 220,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Victorian Hat": 1}},
                },
                {
                    "points_required": 330,
                    "reward": {"items": {"Eggplant Seed": 50}, "coins": 1600, "wearables": {}},
                },
                {
                    "points_required": 700,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Bat Wings": 1}},
                },
            ],
            "repeats": {
                "points_required": 160,
                "reward": {"items": {"Rare Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
    "miranda": {
        "name": "Miranda",
        "flowers": {
            "Yellow Carnation": 6, "Yellow Lotus": 5, "Yellow Daffodil": 4,
            "Yellow Pansy": 4, "Yellow Balloon Flower": 5, "Yellow Cosmos": 4,
            "Yellow Gladiolus": 4, "Yellow Lavender": 4, "Yellow Clover": 4,
            "Yellow Edelweiss": 4,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 30,
                    "reward": {"items": {"Time Warp Totem": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 90,
                    "reward": {"items": {}, "coins": 960, "wearables": {"Fruit Picker Shirt": 1}},
                },
                {
                    "points_required": 260,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Fruit Picker Apron": 1}},
                },
                {
                    "points_required": 500,
                    "reward": {"items": {}, "coins": 6400, "wearables": {"Fruit Bowl": 1}},
                },
            ],
            "repeats": {
                "points_required": 100,
                "reward": {
                    "items": {
                        "Blueberry Seed": 5, "Apple Seed": 5,
                        "Banana Plant": 5, "Orange Seed": 5
                    }, "coins": 0, "wearables": {}
                },
            },
        },
    },
    "cornwell": {
        "name": "Cornwell",
        "flowers": {
            "Red Balloon Flower": 5, "Yellow Balloon Flower": 5,
            "Purple Balloon Flower": 5, "White Balloon Flower": 5,
            "Blue Balloon Flower": 5,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 65,
                    "reward": {"items": {"Rare Key": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 175,
                    "reward": {"items": {"Gem": 25}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 340,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Wise Robes": 1}},
                },
                {
                    "points_required": 600,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Wise Beard": 1}},
                },
            ],
            "repeats": {
                "points_required": 200,
                "reward": {"items": {"Luxury Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
    "tywin": {
        "name": "Tywin",
        "flowers": {"Primula Enigma": 7, "Celestial Frostbloom": 6},
        "rewards": {
            "planned": [
                {
                    "points_required": 35,
                    "reward": {"items": {"Rare Key": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 175,
                    "reward": {"items": {}, "coins": 3200, "wearables": {}},
                },
                {
                    "points_required": 330,
                    "reward": {"items": {"Pirate Cake": 5}, "coins": 0, "wearables": {}},
                },
            ],
            "repeats": {
                "points_required": 160,
                "reward": {"items": {"Luxury Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
    "jester": {
        "name": "Jester",
        "flowers": {"Red Balloon Flower": 6, "Red Carnation": 6},
        "rewards": {
            "planned": [
                {
                    "points_required": 50,
                    "reward": {"items": {"Time Warp Totem": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 140,
                    "reward": {"items": {"Rare Key": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 340,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Cap n Bells": 1}},
                },
                {
                    "points_required": 520,
                    "reward": {"items": {}, "coins": 16000, "wearables": {}},
                },
                {
                    "points_required": 740,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Motley": 1}},
                },
            ],
            "repeats": {
                "points_required": 90,
                "reward": {"items": {"Treasure Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
    "pumpkin' pete": {
        "name": "Pumpkin' Pete",
        "flowers": {"Yellow Cosmos": 6},
        "rewards": {
            "planned": [
                {
                    "points_required": 5,
                    "reward": {"items": {}, "coins": 160, "wearables": {}},
                },
                {
                    "points_required": 12,
                    "reward": {"items": {"Treasure Key": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 50,
                    "reward": {"items": {}, "wearables": {"Pumpkin Hat": 1}, "coins": 0},
                },
                {
                    "points_required": 100,
                    "reward": {"items": {}, "coins": 640, "wearables": {}},
                },
            ],
            "repeats": {
                "points_required": 100,
                "reward": {"items": {"Treasure Key": 1}, "coins": 640, "wearables": {}},
            },
        },
    },
    "old salty": {
        "name": "Old Salty",
        "flowers": {
            "Blue Carnation": 6, "Blue Lotus": 5, "Blue Daffodil": 4,
            "Blue Pansy": 4, "Blue Balloon Flower": 5, "Blue Cosmos": 4,
            "Blue Gladiolus": 4, "Blue Lavender": 3, "Blue Clover": 4,
            "Blue Edelweiss": 3,
        },
        "rewards": {
            "planned": [
                {
                    "points_required": 30,
                    "reward": {"items": {}, "coins": 80, "wearables": {"Striped Blue Shirt": 1}},
                },
                {
                    "points_required": 90,
                    "reward": {"items": {}, "coins": 260, "wearables": {"Peg Leg": 1}},
                },
                {
                    "points_required": 500,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Pirate Potion": 1}},
                },
                {
                    "points_required": 850,
                    "reward": {"items": {"Pirate Bounty": 1}, "coins": 0, "wearables": {"Pirate Hat": 1}},
                },
            ],
            "repeats": {
                "points_required": 250,
                "reward": {"items": {}, "coins": 2500, "wearables": {}},
            },
        },
    },
    "corale": {
        "name": "Corale",
        "flowers": {"Prism Petal": 6},
        "rewards": {
            "planned": [
                {
                    "points_required": 45,
                    "reward": {"items": {}, "coins": 960, "wearables": {}},
                },
                {
                    "points_required": 150,
                    "reward": {"items": {"Gem": 50}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 320,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Pink Ponytail": 1}},
                },
            ],
            "repeats": {
                "points_required": 200,
                "reward": {"items": {}, "coins": 3200, "wearables": {}},
            },
        },
    },
    "victoria": {
        "name": "Victoria",
        "flowers": {"Primula Enigma": 8},
        "rewards": {
            "planned": [
                {
                    "points_required": 50,
                    "reward": {"items": {}, "coins": 2560, "wearables": {}},
                },
                {
                    "points_required": 140,
                    "reward": {"items": {"Time Warp Totem": 1}, "coins": 0, "wearables": {}},
                },
                {
                    "points_required": 340,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Royal Dress": 1}},
                },
                {
                    "points_required": 520,
                    "reward": {"items": {}, "coins": 16000, "wearables": {}},
                },
                {
                    "points_required": 850,
                    "reward": {"items": {}, "coins": 0, "wearables": {"Queen's Crown": 1}},
                },
            ],
            "repeats": {
                "points_required": 160,
                "reward": {"items": {"Rare Key": 1}, "coins": 0, "wearables": {}},
            },
        },
    },
}