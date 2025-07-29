# app/domain/crops.py
"""
Fonte da Verdade para os dados de plantações (Crops).

Este módulo centraliza todas as informações sobre as plantações,
incluindo o seu tipo, preço de venda, tempo de crescimento e estações.
Os dados foram combinados a partir do ficheiro 'crops.ts' do jogo e
de dados complementares.
"""

CROPS_DATA = {
    # --- Crops (The final produce from regular farming) ---
    "Sunflower": {
        "type": "Crop", "sell_price": 0.02,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "plant_seconds": 60, "enabled": True
    },
    "Potato": {
        "type": "Crop", "sell_price": 0.14,
        "season": ["Summer", "Autumn", "Winter"],
        "plant_seconds": 300, "enabled": True
    },
    "Rhubarb": {
        "type": "Crop", "sell_price": 0.24,
        "season": ["Spring"],
        "plant_seconds": 600, "enabled": True
    },
    "Pumpkin": {
        "type": "Crop", "sell_price": 0.4,
        "season": ["Autumn"],
        "plant_seconds": 1800, "enabled": True
    },
    "Zucchini": {
        "type": "Crop", "sell_price": 0.4,
        "season": ["Summer"],
        "plant_seconds": 1800, "enabled": True
    },
    "Carrot": {
        "type": "Crop", "sell_price": 0.8,
        "season": ["Spring", "Autumn"],
        "plant_seconds": 3600, "enabled": True
    },
    "Yam": {
        "type": "Crop", "sell_price": 0.8,
        "season": ["Autumn"],
        "plant_seconds": 3600, "enabled": True
    },
    "Cabbage": {
        "type": "Crop", "sell_price": 1.5,
        "season": ["Spring", "Winter"],
        "plant_seconds": 7200, "enabled": True
    },
    "Broccoli": {
        "type": "Crop", "sell_price": 1.5,
        "season": ["Autumn"],
        "plant_seconds": 7200, "enabled": True
    },
    "Soybean": {
        "type": "Crop", "sell_price": 2.3,
        "season": ["Spring", "Autumn"],
        "plant_seconds": 10800, "enabled": True
    },
    "Beetroot": {
        "type": "Crop", "sell_price": 2.8,
        "season": ["Summer", "Winter"],
        "plant_seconds": 14400, "enabled": True
    },
    "Pepper": {
        "type": "Crop", "sell_price": 3,
        "season": ["Summer"],
        "plant_seconds": 14400, "enabled": True
    },
    "Cauliflower": {
        "type": "Crop", "sell_price": 4.25,
        "season": ["Summer", "Winter"],
        "plant_seconds": 28800, "enabled": True
    },
    "Parsnip": {
        "type": "Crop", "sell_price": 6.5,
        "season": ["Winter"],
        "plant_seconds": 43200, "enabled": True
    },
    "Eggplant": {
        "type": "Crop", "sell_price": 8,
        "season": ["Summer"],
        "plant_seconds": 57600, "enabled": True
    },
    "Corn": {
        "type": "Crop", "sell_price": 9,
        "season": ["Spring"],
        "plant_seconds": 72000, "enabled": True
    },
    "Onion": {
        "type": "Crop", "sell_price": 10,
        "season": ["Winter"],
        "plant_seconds": 72000, "enabled": True
    },
    "Radish": {
        "type": "Crop", "sell_price": 9.5,
        "season": ["Summer"],
        "plant_seconds": 86400, "enabled": True
    },
    "Wheat": {
        "type": "Crop", "sell_price": 7,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "plant_seconds": 86400, "enabled": True
    },
    "Turnip": {
        "type": "Crop", "sell_price": 8,
        "season": ["Winter"],
        "plant_seconds": 86400, "enabled": True
    },
    "Kale": {
        "type": "Crop", "sell_price": 10,
        "season": ["Spring", "Winter"],
        "plant_seconds": 129600, "enabled": True
    },
    "Artichoke": {
        "type": "Crop", "sell_price": 12,
        "season": ["Autumn"],
        "plant_seconds": 129600, "enabled": True
    },
    "Barley": {
        "type": "Crop", "sell_price": 12,
        "season": ["Spring", "Autumn"],
        "plant_seconds": 172800, "enabled": True
    },

    # --- Greenhouse Produce (Crops & Fruits) ---
    "Rice": {
        "type": "GreenhouseCrop", "sell_price": 320,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "plant_seconds": 115200, "enabled": True
    },
    "Olive": {
        "type": "GreenhouseCrop", "sell_price": 400,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "plant_seconds": 158400, "enabled": True
    },

    # --- Exotic Crops (from Magic Beans) ---
    "Black Magic": {
        "type": "ExoticCrop", "sell_price": 32000,
        "season": [], "plant_seconds": 0, "enabled": True
    },
    "Golden Helios": {
        "type": "ExoticCrop", "sell_price": 16000,
        "season": [], "plant_seconds": 0, "enabled": True
    },
    "Chiogga": {
        "type": "ExoticCrop", "sell_price": 8000,
        "season": [], "plant_seconds": 0, "enabled": True
    },
    "Purple Cauliflower": {
        "type": "ExoticCrop", "sell_price": 3200,
        "season": [], "plant_seconds": 0, "enabled": True
    },
    "Adirondack Potato": {
        "type": "ExoticCrop", "sell_price": 2400,
        "season": [], "plant_seconds": 0, "enabled": True
    },
    "Warty Goblin Pumpkin": {
        "type": "ExoticCrop", "sell_price": 1600,
        "season": [], "plant_seconds": 0, "enabled": True
    },
    "White Carrot": {
        "type": "ExoticCrop", "sell_price": 800,
        "season": [], "plant_seconds": 0, "enabled": True
    },
}