# app/domain/seeds.py
"""
Fonte da Verdade para os dados das Sementes (Seeds).

Este módulo centraliza todas as informações sobre as sementes
disponíveis no jogo, incluindo o seu custo, a colheita que produzem,
o nível necessário e o local de plantio.
"""

SEEDS_DATA = {
    # --- Seeds (The items you plant) ---
    "Sunflower Seed": {
        "type": "Seed", "yields": "Sunflower", "cost_coins": 0.01,
        "bumpkin_level": 1, "planting_spot": "Crop Plot", "enabled": True
    },
    "Potato Seed": {
        "type": "Seed", "yields": "Potato", "cost_coins": 0.1,
        "bumpkin_level": 1, "planting_spot": "Crop Plot", "enabled": True
    },
    "Rhubarb Seed": {
        "type": "Seed", "yields": "Rhubarb", "cost_coins": 0.15,
        "bumpkin_level": 1, "planting_spot": "Crop Plot", "enabled": True
    },
    "Pumpkin Seed": {
        "type": "Seed", "yields": "Pumpkin", "cost_coins": 0.2,
        "bumpkin_level": 2, "planting_spot": "Crop Plot", "enabled": True
    },
    "Zucchini Seed": {
        "type": "Seed", "yields": "Zucchini", "cost_coins": 0.2,
        "bumpkin_level": 2, "planting_spot": "Crop Plot", "enabled": True
    },
    "Carrot Seed": {
        "type": "Seed", "yields": "Carrot", "cost_coins": 0.5,
        "bumpkin_level": 2, "planting_spot": "Crop Plot", "enabled": True
    },
    "Yam Seed": {
        "type": "Seed", "yields": "Yam", "cost_coins": 0.5,
        "bumpkin_level": 2, "planting_spot": "Crop Plot", "enabled": True
    },
    "Cabbage Seed": {
        "type": "Seed", "yields": "Cabbage", "cost_coins": 1,
        "bumpkin_level": 3, "planting_spot": "Crop Plot", "enabled": True
    },
    "Broccoli Seed": {
        "type": "Seed", "yields": "Broccoli", "cost_coins": 1,
        "bumpkin_level": 3, "planting_spot": "Crop Plot", "enabled": True
    },
    "Soybean Seed": {
        "type": "Seed", "yields": "Soybean", "cost_coins": 1.5,
        "bumpkin_level": 3, "planting_spot": "Crop Plot", "enabled": True
    },
    "Beetroot Seed": {
        "type": "Seed", "yields": "Beetroot", "cost_coins": 2,
        "bumpkin_level": 3, "planting_spot": "Crop Plot", "enabled": True
    },
    "Pepper Seed": {
        "type": "Seed", "yields": "Pepper", "cost_coins": 2,
        "bumpkin_level": 3, "planting_spot": "Crop Plot", "enabled": True
    },
    "Cauliflower Seed": {
        "type": "Seed", "yields": "Cauliflower", "cost_coins": 3,
        "bumpkin_level": 4, "planting_spot": "Crop Plot", "enabled": True
    },
    "Parsnip Seed": {
        "type": "Seed", "yields": "Parsnip", "cost_coins": 5,
        "bumpkin_level": 4, "planting_spot": "Crop Plot", "enabled": True
    },
    "Eggplant Seed": {
        "type": "Seed", "yields": "Eggplant", "cost_coins": 6,
        "bumpkin_level": 5, "planting_spot": "Crop Plot", "enabled": True
    },
    "Corn Seed": {
        "type": "Seed", "yields": "Corn", "cost_coins": 7,
        "bumpkin_level": 5, "planting_spot": "Crop Plot", "enabled": True
    },
    "Onion Seed": {
        "type": "Seed", "yields": "Onion", "cost_coins": 7,
        "bumpkin_level": 5, "planting_spot": "Crop Plot", "enabled": True
    },
    "Radish Seed": {
        "type": "Seed", "yields": "Radish", "cost_coins": 7,
        "bumpkin_level": 5, "planting_spot": "Crop Plot", "enabled": True
    },
    "Wheat Seed": {
        "type": "Seed", "yields": "Wheat", "cost_coins": 5,
        "bumpkin_level": 5, "planting_spot": "Crop Plot", "enabled": True
    },
    "Turnip Seed": {
        "type": "Seed", "yields": "Turnip", "cost_coins": 5,
        "bumpkin_level": 6, "planting_spot": "Crop Plot", "enabled": True
    },
    "Kale Seed": {
        "type": "Seed", "yields": "Kale", "cost_coins": 7,
        "bumpkin_level": 7, "planting_spot": "Crop Plot", "enabled": True
    },
    "Artichoke Seed": {
        "type": "Seed", "yields": "Artichoke", "cost_coins": 7,
        "bumpkin_level": 8, "planting_spot": "Crop Plot", "enabled": True
    },
    "Barley Seed": {
        "type": "Seed", "yields": "Barley", "cost_coins": 10,
        "bumpkin_level": 14, "planting_spot": "Crop Plot", "enabled": True
    },

    # --- Fruit Seeds ---
    "Tomato Seed": {
        "type": "Seed", "yields": "Tomato", "cost_coins": 5,
        "bumpkin_level": 13, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Lemon Seed": {
        "type": "Seed", "yields": "Lemon", "cost_coins": 15,
        "bumpkin_level": 12, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Blueberry Seed": {
        "type": "Seed", "yields": "Blueberry", "cost_coins": 30,
        "bumpkin_level": 13, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Orange Seed": {
        "type": "Seed", "yields": "Orange", "cost_coins": 50,
        "bumpkin_level": 14, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Apple Seed": {
        "type": "Seed", "yields": "Apple", "cost_coins": 70,
        "bumpkin_level": 15, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Banana Plant": {
        "type": "Seed", "yields": "Banana", "cost_coins": 70,
        "bumpkin_level": 16, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Celestine Seed": {
        "type": "Seed", "yields": "Celestine", "cost_coins": 300,
        "bumpkin_level": 12, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Lunara Seed": {
        "type": "Seed", "yields": "Lunara", "cost_coins": 750,
        "bumpkin_level": 12, "planting_spot": "Fruit Patch", "enabled": True
    },
    "Duskberry Seed": {
        "type": "Seed", "yields": "Duskberry", "cost_coins": 1250,
        "bumpkin_level": 12, "planting_spot": "Fruit Patch", "enabled": True
    },

    # --- Greenhouse Seeds ---
    "Grape Seed": {
        "type": "Seed", "yields": "Grape", "cost_coins": 160,
        "bumpkin_level": 40, "planting_spot": "Greenhouse", "enabled": True
    },
    "Rice Seed": {
        "type": "Seed", "yields": "Rice", "cost_coins": 240,
        "bumpkin_level": 40, "planting_spot": "Greenhouse", "enabled": True
    },
    "Olive Seed": {
        "type": "Seed", "yields": "Olive", "cost_coins": 320,
        "bumpkin_level": 40, "planting_spot": "Greenhouse", "enabled": True
    },

    # --- Flower Seeds ---
    "Sunpetal Seed": {
        "type": "Seed", "yields": "Flower", "cost_coins": 16, "bumpkin_level": 13,
        "planting_spot": "Flower Bed", "plant_seconds": 86400, "enabled": True,
        "seasons": ["spring", "summer", "autumn", "winter"]
    },
    "Bloom Seed": {
        "type": "Seed", "yields": "Flower", "cost_coins": 32, "bumpkin_level": 22,
        "planting_spot": "Flower Bed", "plant_seconds": 172800, "enabled": True,
        "seasons": ["spring", "summer", "autumn", "winter"]
    },
    "Lily Seed": {
        "type": "Seed", "yields": "Flower", "cost_coins": 48, "bumpkin_level": 27,
        "planting_spot": "Flower Bed", "plant_seconds": 432000, "enabled": True,
        "seasons": ["spring", "summer", "autumn", "winter"]
    },
    "Edelweiss Seed": {
        "type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35,
        "planting_spot": "Flower Bed", "plant_seconds": 259200, "enabled": True,
        "seasons": ["winter"]
    },
    "Gladiolus Seed": {
        "type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35,
        "planting_spot": "Flower Bed", "plant_seconds": 259200, "enabled": True,
        "seasons": ["summer"]
    },
    "Lavender Seed": {
        "type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35,
        "planting_spot": "Flower Bed", "plant_seconds": 259200, "enabled": True,
        "seasons": ["spring"]
    },
    "Clover Seed": {
        "type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35,
        "planting_spot": "Flower Bed", "plant_seconds": 259200, "enabled": True,
        "seasons": ["autumn"]
    },

    # --- Special Seeds ---
    "Magic Bean": {
        "type": "Seed", "yields": "ExoticCrop", "cost_coins": 0, "bumpkin_level": 0,
        "planting_spot": "Special", "plant_seconds": 172800, "enabled": True
    },
}