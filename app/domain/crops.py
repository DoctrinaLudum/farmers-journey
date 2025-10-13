# app/domain/crops.py
"""
Fonte da Verdade para os dados de plantações (Crops).

Este módulo centraliza todas as informações sobre as plantações,
incluindo o seu tipo, preço de venda, tempo de crescimento e estações.
Os dados foram combinados a partir do ficheiro 'crops.ts' do jogo e
de dados complementares.
"""

CROPS = {
    # --- Crops (The final produce from regular farming) ---
    "Sunflower": {
        "type": "Crop", "sell_price": 0.02,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "harvestSeconds": 60, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Potato": {
        "type": "Crop", "sell_price": 0.14,
        "season": ["Summer", "Autumn", "Winter"],
        "harvestSeconds": 300, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Rhubarb": {
        "type": "Crop", "sell_price": 0.24,
        "season": ["Spring"],
        "harvestSeconds": 600, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Pumpkin": {
        "type": "Crop", "sell_price": 0.4,
        "season": ["Autumn"],
        "harvestSeconds": 1800, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Zucchini": {
        "type": "Crop", "sell_price": 0.4,
        "season": ["Summer"],
        "harvestSeconds": 1800, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Carrot": {
        "type": "Crop", "sell_price": 0.8,
        "season": ["Spring", "Autumn"],
        "harvestSeconds": 3600, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Yam": {
        "type": "Crop", "sell_price": 0.8,
        "season": ["Autumn"],
        "harvestSeconds": 3600, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Cabbage": {
        "type": "Crop", "sell_price": 1.5,
        "season": ["Spring", "Winter"],
        "harvestSeconds": 7200, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Broccoli": {
        "type": "Crop", "sell_price": 1.5,
        "season": ["Autumn"],
        "harvestSeconds": 7200, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Soybean": {
        "type": "Crop", "sell_price": 2.3,
        "season": ["Spring", "Autumn"],
        "harvestSeconds": 10800, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Beetroot": {
        "type": "Crop", "sell_price": 2.8,
        "season": ["Summer", "Winter"],
        "harvestSeconds": 14400, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Pepper": {
        "type": "Crop", "sell_price": 3,
        "season": ["Summer"],
        "harvestSeconds": 14400, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Cauliflower": {
        "type": "Crop", "sell_price": 4.25,
        "season": ["Summer", "Winter"],
        "harvestSeconds": 28800, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Parsnip": {
        "type": "Crop", "sell_price": 6.5,
        "season": ["Winter"], "tier": "medium",
        "harvestSeconds": 43200, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Eggplant": {
        "type": "Crop", "sell_price": 8,
        "season": ["Summer"],
        "harvestSeconds": 57600, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Corn": {
        "type": "Crop", "sell_price": 9,
        "season": ["Spring"],
        "harvestSeconds": 72000, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Onion": {
        "type": "Crop", "sell_price": 10,
        "season": ["Winter"],
        "harvestSeconds": 72000, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Radish": {
        "type": "Crop", "sell_price": 9.5,
        "season": ["Summer"],
        "harvestSeconds": 86400, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Wheat": {
        "type": "Crop", "sell_price": 7,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "harvestSeconds": 86400, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Turnip": {
        "type": "Crop", "sell_price": 8,
        "season": ["Winter"],
        "harvestSeconds": 86400, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Kale": {
        "type": "Crop", "sell_price": 10,
        "season": ["Spring", "Winter"],
        "harvestSeconds": 129600, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Artichoke": {
        "type": "Crop", "sell_price": 12,
        "season": ["Autumn"],
        "harvestSeconds": 129600, "enabled": True,
        "planting_spot": "Crop Plot"
    },
    "Barley": {
        "type": "Crop", "sell_price": 12,
        "season": ["Spring", "Autumn"], "tier": "advanced",
        "harvestSeconds": 172800, "enabled": True,
        "planting_spot": "Crop Plot"
    },

    # --- Greenhouse Produce (Crops & Fruits) ---
    "Rice": {
        "type": "Crop", "sell_price": 320,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "harvestSeconds": 115200, "enabled": True,
        "planting_spot": "Greenhouse"
    },
    "Olive": {
        "type": "Crop", "sell_price": 400,
        "season": ["Spring", "Summer", "Autumn", "Winter"],
        "harvestSeconds": 158400, "enabled": True,
        "planting_spot": "Greenhouse"
    },

    # --- Exotic Crops (from Magic Beans) ---
    "Black Magic": {
        "type": "ExoticCrop", "sell_price": 32000,
        "season": [], "harvestSeconds": 0, "enabled": True
    },
    "Golden Helios": {
        "type": "ExoticCrop", "sell_price": 16000,
        "season": [], "harvestSeconds": 0, "enabled": True
    },
    "Chiogga": {
        "type": "ExoticCrop", "sell_price": 8000,
        "season": [], "harvestSeconds": 0, "enabled": True
    },
    "Purple Cauliflower": {
        "type": "ExoticCrop", "sell_price": 3200,
        "season": [], "harvestSeconds": 0, "enabled": True
    },
    "Adirondack Potato": {
        "type": "ExoticCrop", "sell_price": 2400,
        "season": [], "harvestSeconds": 0, "enabled": True
    },
    "Warty Goblin Pumpkin": {
        "type": "ExoticCrop", "sell_price": 1600,
        "season": [], "harvestSeconds": 0, "enabled": True
    },
    "White Carrot": {
        "type": "ExoticCrop", "sell_price": 800,
        "season": [], "harvestSeconds": 0, "enabled": True
    },
}

# --- DADOS DERIVADOS ---
GREENHOUSE_CROPS = {
    name: data for name, data in CROPS.items()
    if data.get("planting_spot") == "Greenhouse"
}

# --- DADOS DERIVADOS: TIERS DAS CULTURAS ---
# A lógica para determinar os tiers é baseada no tempo de crescimento,
# espelhando o código-fonte do jogo.

CROP_TIERS = {
    "basic": [],
    "medium": [],
    "advanced": []
}

def _calculate_crop_tiers():
    """
    Preenche o dicionário CROP_TIERS com base no tempo de crescimento das culturas.
    Esta função é executada uma única vez na inicialização do módulo.
    """
    try:
        pumpkin_seconds = CROPS["Pumpkin"]["harvestSeconds"]
        eggharvestSeconds = CROPS["Eggplant"]["harvestSeconds"]

        for crop_name, crop_data in CROPS.items():
            if crop_data.get("type") == "Crop" and "harvestSeconds" in crop_data:
                if crop_data["harvestSeconds"] <= pumpkin_seconds:
                    CROP_TIERS["basic"].append(crop_name)
                elif crop_data["harvestSeconds"] >= eggharvestSeconds:
                    CROP_TIERS["advanced"].append(crop_name)
                else:
                    CROP_TIERS["medium"].append(crop_name)
    except KeyError as e:
        pass # Em um ambiente de produção, um log seria mais apropriado.

_calculate_crop_tiers()
