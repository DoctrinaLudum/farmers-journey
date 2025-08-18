# app/domain/fruits.py
"""
Contém os dados estáticos e completos sobre as frutas do jogo,
combinando informações dos arquivos fruits.ts, seeds.ts e dados legados.
"""

FRUIT_DATA = {
    "Tomato": {
        "name": "Tomato",
        "type": "Fruit",
        "sell_price": 2,
        "seed_name": "Tomato Seed",
        "seed_price": 5,
        "plant_seconds": 2 * 60 * 60,
        "bumpkin_level": 13,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Spring", "Autumn"], 
    },
    "Lemon": {
        "name": "Lemon",
        "type": "Fruit",
        "sell_price": 6,
        "seed_name": "Lemon Seed",
        "seed_price": 15,
        "plant_seconds": 4 * 60 * 60,
        "bumpkin_level": 12,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Summer", "Winter"], 
    },
    "Blueberry": {
        "name": "Blueberry",
        "type": "Fruit",
        "sell_price": 12,
        "seed_name": "Blueberry Seed",
        "seed_price": 30,
        "plant_seconds": 6 * 60 * 60,
        "bumpkin_level": 13,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Spring", "Winter"], 
    },
    "Orange": {
        "name": "Orange",
        "type": "Fruit",
        "sell_price": 18,
        "seed_name": "Orange Seed",
        "seed_price": 50,
        "plant_seconds": 8 * 60 * 60,
        "bumpkin_level": 14,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Spring", "Summer"], 
    },
    "Apple": {
        "name": "Apple",
        "type": "Fruit",
        "sell_price": 25,
        "seed_name": "Apple Seed",
        "seed_price": 70,
        "plant_seconds": 12 * 60 * 60,
        "bumpkin_level": 15,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Autumn", "Winter"], 
    },
    "Banana": {
        "name": "Banana",
        "type": "Fruit",
        "sell_price": 25,
        "seed_name": "Banana Plant",
        "seed_price": 70,
        "plant_seconds": 12 * 60 * 60,
        "bumpkin_level": 16,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Summer", "Autumn"], 
    },
    "Celestine": {
        "name": "Celestine",
        "type": "Fruit",
        "sell_price": 200,
        "seed_name": "Celestine Seed",
        "seed_price": 300,
        "plant_seconds": 6 * 60 * 60,
        "bumpkin_level": 12,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Spring", "Summer", "Autumn", "Winter"],
    },
    "Lunara": {
        "name": "Lunara",
        "type": "Fruit",
        "sell_price": 500,
        "seed_name": "Lunara Seed",
        "seed_price": 750,
        "plant_seconds": 12 * 60 * 60,
        "bumpkin_level": 12,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Spring", "Summer", "Autumn", "Winter"],
    },
    "Duskberry": {
        "name": "Duskberry",
        "type": "Fruit",
        "sell_price": 1000,
        "seed_name": "Duskberry Seed",
        "seed_price": 1250,
        "plant_seconds": 24 * 60 * 60,
        "bumpkin_level": 12,                 
        "planting_spot": "Fruit Patch",    
        "seasons": ["Spring", "Summer", "Autumn", "Winter"],
    },
    # Frutas da Estufa (Greenhouse)
    "Grape": {
        "name": "Grape",
        "type": "Fruit",
        "sell_price": 240,
        "seed_name": "Grape Seed",
        "seed_price": 160,
        "plant_seconds": 12 * 60 * 60,
        "bumpkin_level": 40,                 
        "planting_spot": "Greenhouse",     
        "seasons": ["Spring", "Summer", "Autumn", "Winter"],
    },
}

# --- DADOS DERIVADOS ---
# Para manter a consistência com a estrutura do jogo e facilitar o acesso
# pelos serviços, criamos dicionários derivados a partir de FRUIT_DATA.

PATCH_FRUIT = {
    name: data for name, data in FRUIT_DATA.items()
    if data.get("planting_spot") == "Fruit Patch"
}

GREENHOUSE_FRUIT = {
    name: data for name, data in FRUIT_DATA.items()
    if data.get("planting_spot") == "Greenhouse"
}

FRUIT_SEEDS = {
    data["seed_name"]: {
        "price": data.get("seed_price", 0),
        "plantSeconds": data.get("plant_seconds", 0),
        "bumpkinLevel": data.get("bumpkin_level", 1),
        "yield": name,
        "plantingSpot": data.get("planting_spot"),
    }
    for name, data in FRUIT_DATA.items() if "seed_name" in data
}