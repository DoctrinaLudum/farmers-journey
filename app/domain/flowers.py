# app/domain/flowers.py
"""
Contém os dados estáticos e a lógica de negócio para as flores,
baseado nos arquivos do jogo, como flowers.ts e giftFlowers.ts.
Esta versão foi reestruturada para incluir dados das sementes e valor de presente.
"""

# Mapeamento de quais flores cada NPC aceita como presente.
# Fonte: giftFlowers.ts
NPC_FLOWER_GIFTS = {
    "betty": ["Red Pansy", "Yellow Pansy", "Purple Pansy", "White Pansy", "Blue Pansy"],
    "grubnug": ["Red Pansy", "Yellow Pansy", "Purple Pansy", "White Pansy", "Blue Pansy"],
    "hazel": ["Red Cosmos", "Yellow Cosmos", "Purple Cosmos", "White Cosmos", "Blue Cosmos", "Prismalys", "Prism Petal"],
    "raven": ["Red Balloon Flower", "Yellow Balloon Flower", "Purple Balloon Flower", "White Balloon Flower", "Blue Balloon Flower", "Celestial Frostbloom"],
    "tywin": ["Red Carnation", "Yellow Carnation", "Purple Carnation", "White Carnation", "Blue Carnation", "Primula Enigma"],
    "tango": ["Red Daffodil", "Yellow Daffodil", "Purple Daffodil", "White Daffodil", "Blue Daffodil"],
}

# Dados completos sobre as sementes de flores.
# Fonte: FLOWER_SEEDS em flowers.ts
FLOWER_SEEDS_DATA = {
    "Sunpetal Seed": {
        "price": 16,
        "bumpkinLevel": 13,
        "plantSeconds": 1 * 24 * 60 * 60, # 1 dia
        "plantingSpot": "Flower Bed",
        "seasons": ["spring", "summer", "autumn", "winter"],

    },
    "Bloom Seed": {
        "price": 32,
        "bumpkinLevel": 22,
        "plantSeconds": 2 * 24 * 60 * 60, # 2 dias
        "plantingSpot": "Flower Bed",
        "seasons": ["spring", "summer", "autumn", "winter"],
    },
    "Lily Seed": {
        "price": 48,
        "bumpkinLevel": 27,
        "plantSeconds": 5 * 24 * 60 * 60, # 5 dias
        "plantingSpot": "Flower Bed",
        "seasons": ["spring", "summer", "autumn", "winter"],
    },
    "Edelweiss Seed": {
        "price": 96,
        "bumpkinLevel": 35,
        "plantSeconds": 3 * 24 * 60 * 60, # 3 dias
        "plantingSpot": "Flower Bed",
        "seasons": ["winter"],
    },
    "Gladiolus Seed": {
        "price": 96,
        "bumpkinLevel": 35,
        "plantSeconds": 3 * 24 * 60 * 60, # 3 dias
        "plantingSpot": "Flower Bed",
        "seasons": ["summer"],
    },
    "Lavender Seed": {
        "price": 96,
        "bumpkinLevel": 35,
        "plantSeconds": 3 * 24 * 60 * 60, # 3 dias
        "plantingSpot": "Flower Bed",
        "seasons": ["spring"],
    },
    "Clover Seed": {
        "price": 96,
        "bumpkinLevel": 35,
        "plantSeconds": 3 * 24 * 60 * 60, # 3 dias
        "plantingSpot": "Flower Bed",
        "seasons": ["autumn"],
    },
}

# Base de dados completa das flores, com a nova estrutura de receitas
# e valores exatos dos arquivos do jogo.
FLOWER_DATA = {
    # --- GRUPO SUNPETAL ---
    "Red Pansy": {
        "name": "Red Pansy",
        "seed": "Sunpetal Seed",
        "type": "Pansy",
        "gift_value": 3,
        "recipes": {
            "Radish": 5,
            "Banana": 3,
            "Red Cosmos": 1,
            "Purple Daffodil": 1,
            "Red Balloon Flower": 1,
            "Red Lotus": 1,
            "Primula Enigma": 1,
        },
    },
    "Yellow Pansy": {
        "name": "Yellow Pansy",
        "seed": "Sunpetal Seed",
        "type": "Pansy",
        "gift_value": 3,
        "recipes": {
            "Sunflower": 50,
            "Apple": 3,
            "Red Pansy": 1,
            "Red Daffodil": 1,
            "Yellow Balloon Flower": 1,
            "Yellow Carnation": 1,
        },
    },
    "Purple Pansy": {
        "name": "Purple Pansy",
        "seed": "Sunpetal Seed",
        "type": "Pansy",
        "gift_value": 3,
        "recipes": {
            "Blue Pansy": 1,
            "Purple Balloon Flower": 1,
            "Purple Carnation": 1,
        },
    },
    "White Pansy": {
        "name": "White Pansy",
        "seed": "Sunpetal Seed",
        "type": "Pansy",
        "gift_value": 3,
        "cross_breed": ["Red Pansy", "Yellow Pansy"],
        "recipes": {
            "Yellow Cosmos": 1,
            "Yellow Pansy": 1,
            "White Pansy": 1,
        },
    },
    "Blue Pansy": {
        "name": "Blue Pansy",
        "seed": "Sunpetal Seed",
        "type": "Pansy",
        "gift_value": 3,
        "cross_breed": ["Purple Pansy", "Yellow Pansy"],
        "recipes": {
            "Purple Cosmos": 1,
            "White Pansy": 1,
            "White Cosmos": 1,
            "White Daffodil": 1,
            "Blue Daffodil": 1,
            "White Carnation": 1,
        },
    },
    "Red Cosmos": {
        "name": "Red Cosmos",
        "seed": "Sunpetal Seed",
        "type": "Cosmos",
        "gift_value": 3,
        "cross_breed": ["Red Pansy", "Purple Pansy"],
        "recipes": {
            "Yellow Daffodil": 1,
            "Purple Lotus": 1,
        },
    },
    "Yellow Cosmos": {
        "name": "Yellow Cosmos",
        "seed": "Sunpetal Seed",
        "type": "Cosmos",
        "gift_value": 3,
        "cross_breed": ["Yellow Pansy", "White Pansy"],
        "recipes": {
            "Yellow Pansy": 1,
            "White Balloon Flower": 1,
            "Red Carnation": 1,
        },
    },
    "Purple Cosmos": {
        "name": "Purple Cosmos",
        "seed": "Sunpetal Seed",
        "type": "Cosmos",
        "gift_value": 3,
        "cross_breed": ["Purple Pansy", "White Pansy"],
        "recipes": {
            "Beetroot": 10,
            "Eggplant": 5,
            "Kale": 5,
            "Blue Cosmos": 1,
            "Blue Balloon Flower": 1,
            "Celestial Frostbloom": 1,
        },
    },
    "White Cosmos": {
        "name": "White Cosmos",
        "seed": "Sunpetal Seed",
        "type": "Cosmos",
        "gift_value": 3,
        "cross_breed": ["Red Cosmos", "Yellow Cosmos"],
        "recipes": {
            "Prism Petal": 1,
            "Yellow Lotus": 1,
        },
    },
    "Blue Cosmos": {
        "name": "Blue Cosmos",
        "seed": "Sunpetal Seed",
        "type": "Cosmos",
        "gift_value": 3,
        "cross_breed": ["Purple Cosmos", "Yellow Cosmos"],
        "recipes": {
            "Cauliflower": 5,
            "Parsnip": 5,
            "Blueberry": 3,
            "Purple Pansy": 1,
            "White Lotus": 1,
            "Blue Carnation": 1,
        },
    },
    "Prism Petal": {
        "name": "Prism Petal",
        "seed": "Sunpetal Seed",
        "type": "Epic",
        "gift_value": 12,
        "cross_breed": ["White Cosmos", "Blue Cosmos"],
        "recipes": {
            "Blue Lotus": 1,
        },
    },

# --- GRUPO BLOOM ---
    "Red Balloon Flower": {
        "name": "Red Balloon Flower",
        "seed": "Bloom Seed",
        "type": "Balloon",
        "gift_value": 5, 
        "cross_breed": ["Red Cosmos", "White Cosmos"],
        "recipes": {
            "Sunflower": 50,
            "Beetroot": 10,
            "Apple": 3,
            "Banana": 3,
            "Purple Pansy": 1,
            "Red Pansy": 1,
            "Red Daffodil": 1,
            "Yellow Daffodil": 1,
            "Purple Daffodil": 1,
            "Yellow Carnation": 1,
        },
    },
    "Yellow Balloon Flower": {
        "name": "Yellow Balloon Flower",
        "seed": "Bloom Seed",
        "type": "Balloon",
        "gift_value": 5, 
        "cross_breed": ["Yellow Cosmos", "White Cosmos"],
        "recipes": {
            "Yellow Lotus": 1,
        },
    },
    "Purple Balloon Flower": {
        "name": "Purple Balloon Flower",
        "seed": "Bloom Seed",
        "type": "Balloon",
        "gift_value": 5, 
        "cross_breed": ["Purple Cosmos", "White Cosmos"],
        "recipes": {
            "Blue Carnation": 1,
        },
    },
    "White Balloon Flower": {
        "name": "White Balloon Flower",
        "seed": "Bloom Seed",
        "type": "Balloon",
        "gift_value": 5,
        "cross_breed": ["Red Balloon Flower", "Yellow Balloon Flower"],
        "recipes": {
            "White Cosmos": 1,
            "Blue Daffodil": 1,
            "White Daffodil": 1,
            "White Balloon Flower": 1,
        },
    },
    "Blue Balloon Flower": {
        "name": "Blue Balloon Flower",
        "seed": "Bloom Seed",
        "type": "Balloon",
        "gift_value": 5,
        "cross_breed": ["Yellow Balloon Flower", "Purple Balloon Flower"],
        "recipes": {
            "Cauliflower": 5,
            "Parsnip": 5,
            "Eggplant": 5,
            "Kale": 5,
            "Blue Pansy": 1,
            "Blue Cosmos": 1,
            "Purple Cosmos": 1,
            "Blue Balloon Flower": 1,
            "Celestial Frostbloom": 1,
        },
    },
    "Red Daffodil": {
        "name": "Red Daffodil",
        "seed": "Bloom Seed",
        "type": "Daffodil",
        "gift_value": 7,
        "cross_breed": ["Red Balloon Flower", "Blue Balloon Flower"],
        "recipes": {
            "Yellow Pansy": 1,
            "Yellow Balloon Flower": 1,
            "Red Carnation": 1,
            "Primula Enigma": 1,
        },
    },
    "Yellow Daffodil": {
        "name": "Yellow Daffodil",
        "seed": "Bloom Seed",
        "type": "Daffodil",
        "gift_value": 7,
        "cross_breed": ["Yellow Balloon Flower", "White Balloon Flower"],
        "recipes": {
            "Red Cosmos": 1,
            "White Carnation": 1,
            "White Lotus": 1,
        },
    },
    "Purple Daffodil": {
        "name": "Purple Daffodil",
        "seed": "Bloom Seed",
        "type": "Daffodil",
        "gift_value": 7,
        "cross_breed": ["Purple Balloon Flower", "White Balloon Flower"],
        "recipes": {
            "Radish": 5,
            "Blueberry": 3,
            "Red Balloon Flower": 1,
            "Red Lotus": 1,
            "Blue Lotus": 1,
        },
    },
    "White Daffodil": {
        "name": "White Daffodil",
        "seed": "Bloom Seed",
        "type": "Daffodil",
        "gift_value": 7,
        "cross_breed": ["Red Daffodil", "Yellow Daffodil"],
        "recipes": {
            "Yellow Cosmos": 1,
            "Prism Petal": 1,
        },
    },
    "Blue Daffodil": {
        "name": "Blue Daffodil",
        "seed": "Bloom Seed",
        "type": "Daffodil",
        "gift_value": 7,
        "cross_breed": ["Yellow Daffodil", "Purple Daffodil"],
        "recipes": {
            "Purple Balloon Flower": 1,
            "Purple Carnation": 1,
            "Purple Lotus": 1,
        },
    },
    "Celestial Frostbloom": {
        "name": "Celestial Frostbloom",
        "seed": "Bloom Seed",
        "type": "Epic",
        "gift_value": 12,
        "cross_breed": ["White Daffodil", "Blue Daffodil"],
        "recipes": {
            "White Pansy": 1,
        },
    },

# --- GRUPO LILY ---
    "Red Carnation": {
        "name": "Red Carnation",
        "seed": "Lily Seed",
        "type": "Carnation",
        "gift_value": 5,
        "cross_breed": ["Red Daffodil", "White Daffodil"],
        "recipes": {
            "Purple Pansy": 1,
        },
    },
    "Yellow Carnation": {
        "name": "Yellow Carnation",
        "seed": "Lily Seed",
        "type": "Carnation",
        "gift_value": 5,
        "cross_breed": ["Yellow Daffodil", "White Daffodil"],
        "recipes": {
            "Sunflower": 50,
            "Yellow Cosmos": 1,
            "Red Lotus": 1,
            "White Carnation": 1,
        },
    },
    "Purple Carnation": {
        "name": "Purple Carnation",
        "seed": "Lily Seed",
        "type": "Carnation",
        "gift_value": 5,
        "cross_breed": ["Purple Daffodil", "White Daffodil"],
        "recipes": {
            "Eggplant": 5,
            "Blueberry": 3,
            "Apple": 3,
            "Blue Cosmos": 1,
            "Blue Balloon Flower": 1,
            "Purple Lotus": 1,
        },
    },
    "White Carnation": {
        "name": "White Carnation",
        "seed": "Lily Seed",
        "type": "Carnation",
        "gift_value": 5,
        "cross_breed": ["Red Carnation", "Yellow Carnation"],
        "recipes": {
            "Yellow Pansy": 1,
            "White Cosmos": 1,
            "Prism Petal": 1,
            "Yellow Daffodil": 1,
            "Celestial Frostbloom": 1,
        },
    },
    "Blue Carnation": {
        "name": "Blue Carnation",
        "seed": "Lily Seed",
        "type": "Carnation",
        "gift_value": 5,
        "cross_breed": ["Purple Carnation", "Yellow Carnation"],
        "recipes": {
            "Purple Daffodil": 1,
            "White Balloon Flower": 1,
            "Primula Enigma": 1,
        },
    },
    "Red Lotus": {
        "name": "Red Lotus",
        "seed": "Lily Seed",
        "type": "Lotus",
        "gift_value": 7,
        "cross_breed": ["Red Carnation", "Blue Carnation"],
        "recipes": {
            "Beetroot": 10,
            "Radish": 5,
            "Purple Cosmos": 1,
            "Red Balloon Flower": 1,
            "Yellow Balloon Flower": 1,
            "Purple Carnation": 1,
            "Yellow Carnation": 1,
            "Red Carnation": 1,
        },
    },
    "Yellow Lotus": {
        "name": "Yellow Lotus",
        "seed": "Lily Seed",
        "type": "Lotus",
        "gift_value": 7,
        "cross_breed": ["Yellow Carnation", "White Carnation"],
        "recipes": {
            "Red Pansy": 1,
            "Red Cosmos": 1,
            "Red Daffodil": 1,
            "Yellow Lotus": 1,
        },
    },
    "Purple Lotus": {
        "name": "Purple Lotus",
        "seed": "Lily Seed",
        "type": "Lotus",
        "gift_value": 7,
        "cross_breed": ["Purple Carnation", "White Carnation"],
        "recipes": {
            "Blue Carnation": 1,
        },
    },
    "White Lotus": {
        "name": "White Lotus",
        "seed": "Lily Seed",
        "type": "Lotus",
        "gift_value": 7,
        "cross_breed": ["Red Lotus", "Yellow Lotus"],
        "recipes": {
            "Cauliflower": 5,
            "Parsnip": 5,
            "Kale": 5,
            "Banana": 3,
            "White Pansy": 1,
            "Blue Daffodil": 1,
            "Blue Lotus": 1,
            # A API menciona "White Lotus" como receita para si mesma
            "White Lotus": 1,
        },
    },
    "Blue Lotus": {
        "name": "Blue Lotus",
        "seed": "Lily Seed",
        "type": "Lotus",
        "gift_value": 7,
        "cross_breed": ["Yellow Lotus", "Purple Lotus"],
        "recipes": {
            "Blue Pansy": 1,
            "White Daffodil": 1,
        },
    },
    "Primula Enigma": {
        "name": "Primula Enigma",
        "seed": "Lily Seed",
        "type": "Epic",
        "gift_value": 12,
        "cross_breed": ["White Lotus", "Blue Lotus"],
        "recipes": {
            "Purple Balloon Flower": 1,
        },
    },

 # --- GRUPO EDELWEISS ---
    "Red Edelweiss": {
        "name": "Red Edelweiss",
        "seed": "Edelweiss Seed",
        "type": "Edelweiss",
        "gift_value": 4,
        "recipes": {
            "Artichoke": 8,
            "Barley": 5,
            "Yellow Edelweiss": 1,
            "Yellow Lavender": 1,
            "Purple Lavender": 1,
            "Red Clover": 1,
        },
    },
    "Yellow Edelweiss": {
        "name": "Yellow Edelweiss",
        "seed": "Edelweiss Seed",
        "type": "Edelweiss",
        "gift_value": 4,
        "recipes": {
            "Onion": 10,
            "Red Edelweiss": 1,
            "Yellow Gladiolus": 1,
            "Red Lavender": 1,
            "White Lavender": 1,
        },
    },
    "Purple Edelweiss": {
        "name": "Purple Edelweiss",
        "seed": "Edelweiss Seed",
        "type": "Edelweiss",
        "gift_value": 4,
        "recipes": {
            "Rhubarb": 25,
            "Pepper": 15,
            "Red Gladiolus": 1,
            "Purple Gladiolus": 1,
            "Blue Gladiolus": 1,
            "Blue Lavender": 1,
            "Blue Clover": 1,
        },
    },
    "White Edelweiss": {
        "name": "White Edelweiss",
        "seed": "Edelweiss Seed",
        "type": "Edelweiss",
        "gift_value": 4,
        "recipes": {
            "Blue Edelweiss": 1,
            "Yellow Clover": 1,
        },
    },
    "Blue Edelweiss": {
        "name": "Blue Edelweiss",
        "seed": "Edelweiss Seed",
        "type": "Edelweiss",
        "gift_value": 4,
        "recipes": {
            "Purple Edelweiss": 1,
            "White Edelweiss": 1,
            "White Gladiolus": 1,
            "Purple Clover": 1,
            "White Clover": 1,
        },
    },

    # --- GRUPO GLADIOLUS ---
    "Red Gladiolus": {
        "name": "Red Gladiolus",
        "seed": "Gladiolus Seed",
        "type": "Gladiolus",
        "gift_value": 4,
        "recipes": {
            "Yellow Edelweiss": 1,
        },
    },
    "Yellow Gladiolus": {
        "name": "Yellow Gladiolus",
        "seed": "Gladiolus Seed",
        "type": "Gladiolus",
        "gift_value": 4,
        "recipes": {
            "Pepper": 15,
            "Onion": 10,
            "Barley": 5,
            "Yellow Gladiolus": 1,
            "White Gladiolus": 1,
            "Red Lavender": 1,
            "Yellow Lavender": 1,
            "White Lavender": 1,
            "Yellow Clover": 1,
        },
    },
    "Purple Gladiolus": {
        "name": "Purple Gladiolus",
        "seed": "Gladiolus Seed",
        "type": "Gladiolus",
        "gift_value": 4,
        "recipes": {
            "Artichoke": 8,
            "Red Edelweiss": 1,
            "Red Gladiolus": 1,
            "Purple Gladiolus": 1,
            "Red Clover": 1,
            "Purple Clover": 1,
        },
    },
    "White Gladiolus": {
        "name": "White Gladiolus",
        "seed": "Gladiolus Seed",
        "type": "Gladiolus",
        "gift_value": 4,
        "recipes": {
            "White Edelweiss": 1,
            "Blue Edelweiss": 1,
            "Blue Gladiolus": 1,
        },
    },
    "Blue Gladiolus": {
        "name": "Blue Gladiolus",
        "seed": "Gladiolus Seed",
        "type": "Gladiolus",
        "gift_value": 4,
        "recipes": {
            "Rhubarb": 25,
            "Purple Edelweiss": 1,
            "Purple Lavender": 1,
            "Blue Lavender": 1,
            "White Clover": 1,
            "Blue Clover": 1,
        },
    },

     # --- GRUPO LAVENDER ---
    "Red Lavender": {
        "name": "Red Lavender",
        "seed": "Lavender Seed",
        "type": "Lavender",
        "gift_value": 4,
        "recipes": {
            "Pepper": 15,
            "Artichoke": 8,
            "Red Edelweiss": 1,
            "Purple Edelweiss": 1,
            "Red Lavender": 1,
            "Purple Lavender": 1,
            "Yellow Clover": 1,
        },
    },
    "Yellow Lavender": {
        "name": "Yellow Lavender",
        "seed": "Lavender Seed",
        "type": "Lavender",
        "gift_value": 4,
        "recipes": {
            "Red Gladiolus": 1,
            "Yellow Gladiolus": 1,
            "White Gladiolus": 1,
            "Yellow Lavender": 1,
            "Red Clover": 1,
        },
    },
    "Purple Lavender": {
        "name": "Purple Lavender",
        "seed": "Lavender Seed",
        "type": "Lavender",
        "gift_value": 4,
        "recipes": {
            "Blue Lavender": 1,
            "Purple Gladiolus": 1,
        },
    },
    "White Lavender": {
        "name": "White Lavender",
        "seed": "Lavender Seed",
        "type": "Lavender",
        "gift_value": 4,
        "recipes": {
            "Rhubarb": 25,
            "Onion": 10,
            "Barley": 5,
            "Yellow Edelweiss": 1,
            "Blue Gladiolus": 1,
            "White Lavender": 1,
        },
    },
    "Blue Lavender": {
        "name": "Blue Lavender",
        "seed": "Lavender Seed",
        "type": "Lavender",
        "gift_value": 4,
        "recipes": {
            "White Edelweiss": 1,
            "Blue Edelweiss": 1,
            "Purple Clover": 1,
            "White Clover": 1,
            "Blue Clover": 1,
        },
    },

    # --- GRUPO CLOVER ---
    "Red Clover": {
        "name": "Red Clover",
        "seed": "Clover Seed",
        "type": "Clover",
        "gift_value": 4,
        "recipes": {
            "Red Edelweiss": 1,
            "Purple Clover": 1,
        },
    },
    "Yellow Clover": {
        "name": "Yellow Clover",
        "seed": "Clover Seed",
        "type": "Clover",
        "gift_value": 4,
        "recipes": {
            "Pepper": 15,
            "Onion": 10,
            "Barley": 5,
            "Yellow Edelweiss": 1,
            "Red Gladiolus": 1,
            "Yellow Lavender": 1,
            "White Lavender": 1,
            "Yellow Clover": 1,
        },
    },
    "Purple Clover": {
        "name": "Purple Clover",
        "seed": "Clover Seed",
        "type": "Clover",
        "gift_value": 4,
        "recipes": {
            "Red Lavender": 1,
            "Red Clover": 1,
        },
    },
    "White Clover": {
        "name": "White Clover",
        "seed": "Clover Seed",
        "type": "Clover",
        "gift_value": 4,
        "recipes": {
            "Blue Edelweiss": 1,
            "Yellow Gladiolus": 1,
            "Blue Lavender": 1,
        },
    },
    "Blue Clover": {
        "name": "Blue Clover",
        "seed": "Clover Seed",
        "type": "Clover",
        "gift_value": 4,
        "recipes": {
            "Rhubarb": 25,
            "Artichoke": 8,
            "Purple Edelweiss": 1,
            "White Edelweiss": 1,
            "Purple Gladiolus": 1,
            "White Gladiolus": 1,
            "Blue Gladiolus": 1,
            "Purple Lavender": 1,
            "White Clover": 1,
            "Blue Clover": 1,
        },
    },
}