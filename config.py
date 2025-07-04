APP_VERSION = "0.1.0"

# ---> INÍCIO: REQUISITOS COMPLETOS PARA EXPANSÃO DE TERRA ---
# Estrutura:
# "tipo_da_ilha": {
#   Nível da Expansão: { "Bumpkin Level": Nível, "Time": "HH:MM:SS", "Recurso": Quantidade, ... }
# }
LAND_EXPANSION_REQUIREMENTS = {
    "basic": {
        4: { "Bumpkin Level": 1, "Time": "00:00:05", "Wood": 3 },
        5: { "Bumpkin Level": 1, "Time": "00:00:05", "Coins": 0.25, "Wood": 5 },
        6: { "Bumpkin Level": 2, "Time": "00:01:00", "Coins": 60, "Stone": 1 },
        7: { "Bumpkin Level": 5, "Time": "00:30:00", "Stone": 5, "Iron": 1 },
        8: { "Bumpkin Level": 8, "Time": "04:00:00", "Iron": 3, "Gold": 1 },
        9: { "Bumpkin Level": 11, "Time": "12:00:00", "Wood": 100, "Stone": 40, "Iron": 5 }
    },
    "petal": {
        5: { "Bumpkin Level": 11, "Time": "00:01:00", "Wood": 20 },
        6: { "Bumpkin Level": 13, "Time": "00:05:00", "Wood": 10, "Stone": 5, "Gold": 2 },
        7: { "Bumpkin Level": 16, "Time": "00:30:00", "Wood": 30, "Stone": 20, "Iron": 5, "Gem": 15 },
        8: { "Bumpkin Level": 20, "Time": "02:00:00", "Wood": 20, "Crimstone": 1, "Gem": 15 },
        9: { "Bumpkin Level": 23, "Time": "02:00:00", "Wood": 50, "Gold": 5, "Gem": 15 },
        10: { "Bumpkin Level": 25, "Time": "04:00:00", "Stone": 10, "Crimstone": 3, "Gem": 15 },
        11: { "Bumpkin Level": 27, "Time": "08:00:00", "Wood": 100, "Stone": 25, "Gold": 5, "Crimstone": 1, "Gem": 15 },
        12: { "Bumpkin Level": 29, "Time": "12:00:00", "Wood": 50, "Iron": 5, "Crimstone": 3, "Gem": 30 },
        13: { "Bumpkin Level": 32, "Time": "12:00:00", "Wood": 50, "Stone": 25, "Iron": 10, "Gold": 10, "Gem": 30 },
        14: { "Bumpkin Level": 36, "Time": "24:00:00", "Wood": 100, "Stone": 10, "Crimstone": 5, "Gem": 30 },
        15: { "Bumpkin Level": 40, "Time": "24:00:00", "Wood": 150, "Stone": 10, "Iron": 10, "Gold": 5, "Crimstone": 5, "Gem": 30 },
        16: { "Bumpkin Level": 43, "Time": "24:00:00", "Wood": 100, "Stone": 10, "Gold": 5, "Crimstone": 8, "Gem": 30 }
    },
    "desert": {
        5: { "Bumpkin Level": 40, "Time": "00:01:00", "Wood": 50, "Stone": 10, "Iron": 5, "Gold": 5 },
        6: { "Bumpkin Level": 40, "Time": "00:05:00", "Wood": 100, "Stone": 20, "Iron": 10, "Gold": 5 },
        7: { "Bumpkin Level": 41, "Time": "00:30:00", "Wood": 150, "Stone": 20, "Iron": 10, "Gold": 5, "Gem": 15 },
        8: { "Bumpkin Level": 42, "Time": "02:00:00", "Wood": 150, "Stone": 10, "Iron": 5, "Gold": 5, "Crimstone": 3, "Oil": 5, "Gem": 30 },
        9: { "Bumpkin Level": 43, "Time": "02:00:00", "Wood": 50, "Stone": 5, "Iron": 5, "Gold": 5, "Crimstone": 6, "Oil": 5, "Gem": 30 },
        10: { "Bumpkin Level": 44, "Time": "08:00:00", "Coins": 320, "Wood": 100, "Stone": 50, "Iron": 10, "Gold": 5, "Crimstone": 12, "Oil": 10, "Gem": 45 },
        11: { "Bumpkin Level": 45, "Time": "12:00:00", "Coins": 640, "Wood": 150, "Stone": 75, "Iron": 10, "Gold": 5, "Crimstone": 15, "Oil": 30, "Gem": 45 },
        12: { "Bumpkin Level": 47, "Time": "12:00:00", "Coins": 1280, "Wood": 100, "Stone": 100, "Iron": 5, "Gold": 10, "Crimstone": 18, "Oil": 30, "Gem": 45 },
        13: { "Bumpkin Level": 50, "Time": "24:00:00", "Coins": 2560, "Wood": 200, "Stone": 50, "Iron": 15, "Gold": 10, "Crimstone": 21, "Oil": 40, "Gem": 45 },
        14: { "Bumpkin Level": 53, "Time": "24:00:00", "Coins": 3200, "Wood": 200, "Stone": 100, "Iron": 15, "Gold": 10, "Crimstone": 24, "Oil": 50, "Gem": 45 },
        15: { "Bumpkin Level": 56, "Time": "24:00:00", "Coins": 3200, "Wood": 300, "Stone": 50, "Iron": 20, "Gold": 10, "Crimstone": 27, "Oil": 75, "Gem": 45 },
        16: { "Bumpkin Level": 58, "Time": "36:00:00", "Coins": 3200, "Wood": 250, "Stone": 125, "Iron": 15, "Gold": 15, "Crimstone": 30, "Oil": 100, "Gem": 60 },
        17: { "Bumpkin Level": 60, "Time": "36:00:00", "Coins": 4800, "Wood": 350, "Stone": 75, "Iron": 20, "Gold": 10, "Crimstone": 33, "Oil": 125, "Gem": 60 },
        18: { "Bumpkin Level": 63, "Time": "36:00:00", "Coins": 4800, "Wood": 400, "Stone": 125, "Iron": 25, "Gold": 15, "Crimstone": 36, "Oil": 150, "Gem": 75 },
        19: { "Bumpkin Level": 65, "Time": "36:00:00", "Coins": 6400, "Wood": 450, "Stone": 150, "Iron": 30, "Gold": 20, "Crimstone": 39, "Oil": 200, "Gem": 60 },
        20: { "Bumpkin Level": 68, "Time": "48:00:00", "Coins": 6400, "Wood": 525, "Stone": 200, "Iron": 35, "Gold": 30, "Crimstone": 42, "Oil": 250, "Gem": 60 },
        21: { "Bumpkin Level": 70, "Time": "48:00:00", "Coins": 8000, "Wood": 550, "Stone": 150, "Iron": 30, "Gold": 25, "Crimstone": 45, "Oil": 350, "Gem": 60 },
        22: { "Bumpkin Level": 72, "Time": "48:00:00", "Coins": 8000, "Wood": 600, "Stone": 200, "Iron": 35, "Gold": 30, "Crimstone": 48, "Oil": 450, "Gem": 75 },
        23: { "Bumpkin Level": 73, "Time": "60:00:00", "Coins": 8000, "Wood": 650, "Stone": 250, "Iron": 40, "Gold": 35, "Crimstone": 51, "Oil": 500, "Gem": 75 },
        24: { "Bumpkin Level": 74, "Time": "60:00:00", "Coins": 9600, "Wood": 700, "Stone": 300, "Iron": 50, "Gold": 45, "Crimstone": 54, "Oil": 550, "Gem": 75 },
        25: { "Bumpkin Level": 75, "Time": "60:00:00", "Coins": 11200, "Wood": 750, "Stone": 350, "Iron": 50, "Gold": 50, "Crimstone": 60, "Oil": 650, "Gem": 75 }
    },
    "volcano": {
        6: { "Bumpkin Level": 70, "Time": "00:00:10", "Wood": 100, "Stone": 50, "Iron": 30, "Gold": 10 },
        7: { "Bumpkin Level": 72, "Time": "00:05:00", "Coins": 320, "Wood": 200, "Stone": 75, "Iron": 25, "Gold": 15, "Crimstone": 4, "Oil": 30, "Gem": 30 },
        8: { "Bumpkin Level": 74, "Time": "00:30:00", "Coins": 640, "Wood": 300, "Stone": 100, "Iron": 40, "Gold": 20, "Crimstone": 8, "Oil": 60, "Gem": 30 },
        9: { "Bumpkin Level": 76, "Time": "01:00:00", "Coins": 960, "Wood": 400, "Stone": 150, "Iron": 35, "Gold": 25, "Crimstone": 12, "Oil": 90, "Gem": 60 },
        10: { "Bumpkin Level": 78, "Time": "02:00:00", "Coins": 1600, "Wood": 450, "Stone": 200, "Iron": 30, "Gold": 20, "Crimstone": 16, "Oil": 120, "Obsidian": 1, "Gem": 60 },
        11: { "Bumpkin Level": 80, "Time": "04:00:00", "Coins": 2500, "Wood": 500, "Stone": 175, "Iron": 30, "Gold": 30, "Crimstone": 20, "Oil": 100, "Gem": 90 },
        12: { "Bumpkin Level": 82, "Time": "08:00:00", "Coins": 3200, "Wood": 650, "Stone": 225, "Iron": 25, "Gold": 25, "Crimstone": 24, "Oil": 100, "Obsidian": 2, "Gem": 150 },
        13: { "Bumpkin Level": 84, "Time": "12:00:00", "Coins": 4000, "Wood": 550, "Stone": 200, "Iron": 40, "Gold": 30, "Crimstone": 28, "Oil": 100, "Gem": 150 },
        14: { "Bumpkin Level": 86, "Time": "12:00:00", "Coins": 4800, "Wood": 700, "Stone": 250, "Iron": 35, "Gold": 35, "Crimstone": 32, "Oil": 100, "Obsidian": 1, "Gem": 150 },
        15: { "Bumpkin Level": 88, "Time": "24:00:00", "Coins": 5600, "Wood": 650, "Stone": 200, "Iron": 30, "Gold": 40, "Crimstone": 36, "Oil": 200, "Obsidian": 2, "Gem": 150 },
        16: { "Bumpkin Level": 90, "Time": "24:00:00", "Coins": 6400, "Wood": 750, "Stone": 250, "Iron": 40, "Gold": 30, "Crimstone": 40, "Oil": 200, "Obsidian": 4, "Gem": 150 },
        17: { "Bumpkin Level": 92, "Time": "24:00:00", "Coins": 8000, "Wood": 700, "Stone": 200, "Iron": 35, "Gold": 35, "Crimstone": 44, "Oil": 200, "Obsidian": 4, "Gem": 150 },
        18: { "Bumpkin Level": 94, "Time": "36:00:00", "Coins": 10000, "Wood": 800, "Stone": 300, "Iron": 45, "Gold": 45, "Crimstone": 48, "Oil": 200, "Obsidian": 6, "Gem": 180 },
        19: { "Bumpkin Level": 96, "Time": "36:00:00", "Coins": 12800, "Wood": 750, "Stone": 250, "Iron": 40, "Gold": 40, "Crimstone": 52, "Oil": 200, "Obsidian": 6, "Gem": 180 },
        20: { "Bumpkin Level": 98, "Time": "48:00:00", "Coins": 15000, "Wood": 850, "Stone": 300, "Iron": 45, "Gold": 30, "Crimstone": 56, "Oil": 200, "Obsidian": 8, "Gem": 180 },
        21: { "Bumpkin Level": 100, "Time": "48:00:00", "Coins": 18000, "Wood": 900, "Stone": 325, "Iron": 50, "Gold": 35, "Crimstone": 60, "Oil": 200, "Obsidian": 8, "Gem": 180 },
        22: { "Bumpkin Level": 102, "Time": "48:00:00", "Coins": 21000, "Wood": 800, "Stone": 300, "Iron": 45, "Gold": 30, "Crimstone": 64, "Oil": 200, "Obsidian": 10, "Gem": 180 },
        23: { "Bumpkin Level": 104, "Time": "48:00:00", "Coins": 25000, "Wood": 950, "Stone": 350, "Iron": 50, "Gold": 35, "Crimstone": 68, "Oil": 200, "Obsidian": 10, "Gem": 180 },
        24: { "Bumpkin Level": 106, "Time": "48:00:00", "Coins": 28000, "Wood": 1000, "Stone": 400, "Iron": 55, "Gold": 40, "Crimstone": 72, "Oil": 300, "Obsidian": 12, "Gem": 180 },
        25: { "Bumpkin Level": 108, "Time": "60:00:00", "Coins": 32000, "Wood": 1100, "Stone": 450, "Iron": 60, "Gold": 35, "Crimstone": 80, "Oil": 300, "Obsidian": 12, "Gem": 180 },
        26: { "Bumpkin Level": 110, "Time": "60:00:00", "Coins": 35000, "Wood": 1200, "Stone": 350, "Iron": 65, "Gold": 30, "Crimstone": 85, "Oil": 300, "Obsidian": 18, "Gem": 180 },
        27: { "Bumpkin Level": 112, "Time": "60:00:00", "Coins": 38000, "Wood": 1250, "Stone": 450, "Iron": 70, "Gold": 40, "Crimstone": 95, "Oil": 300, "Obsidian": 24, "Gem": 225 },
        28: { "Bumpkin Level": 114, "Time": "60:00:00", "Coins": 42000, "Wood": 1150, "Stone": 500, "Iron": 60, "Gold": 45, "Crimstone": 100, "Oil": 300, "Obsidian": 30, "Gem": 225 },
        29: { "Bumpkin Level": 116, "Time": "72:00:00", "Coins": 45000, "Wood": 1350, "Stone": 550, "Iron": 65, "Gold": 40, "Crimstone": 105, "Oil": 300, "Obsidian": 36, "Gem": 225 },
        30: { "Bumpkin Level": 120, "Time": "72:00:00", "Coins": 50000, "Wood": 1500, "Stone": 600, "Iron": 70, "Gold": 50, "Crimstone": 125, "Oil": 300, "Obsidian": 42, "Gem": 225 }
    }
}
# ---> FIM REQUISITOS DE EXPANSÃO ---

# ---> INÍCIO: CATEGORIAS DO INVENTÁRIO <---
INVENTORY_CATEGORIES = {
    "Sementes": [
        "Apple Seed", "Banana Plant", "Barley Seed", "Beetroot Seed", "Bloom Seed",
        "Blueberry Seed", "Broccoli Seed", "Cabbage Seed", "Carnation Seed", "Carrot Seed",
        "Cauliflower Seed", "Celestine Seed", "Clover Seed", "Corn Seed", "Cosmos Seed",
        "Daffodil Seed", "Duskberry Seed", "Edelweiss Seed", "Eggplant Seed", "Gladiolus Seed",
        "Grape Seed", "Kale Seed", "Lavender Seed", "Lily Seed", "Lotus Seed",
        "Lunara Seed", "Olive Seed", "Onion Seed", "Orange Seed", "Pansy Seed",
        "Parsnip Seed", "Pepper Seed", "Potato Seed", "Pumpkin Seed", "Radish Seed",
        "Rhubarb Seed", "Rice Seed", "Soybean Seed", "Sunflower Seed", "Tomato Seed",
        "Turnip Seed", "Wheat Seed", "Yam Seed", "Zucchini Seed"
    ],
    "Colheitas": [
        "Artichoke", "Barley", "Beetroot", "Broccoli", "Cabbage", "Carrot",
        "Cauliflower", "Celestine", "Corn", "Eggplant", "Kale", "Magic Mushroom",
        "Onion", "Parsnip", "Pepper", "Potato", "Pumpkin", "Radish", "Rhubarb",
        "Soybean", "Sunflower", "Tomato", "Turnip", "Wheat", "Wild Mushroom", "Yam",
        "Zucchini"
    ],
    "Frutas": [
        "Apple", "Banana", "Blueberry", "Duskberry", "Immortal Pear", "Lemon",
        "Orange"
    ],
    "Flores": [
        "Blue Balloon Flower", "Blue Carnation", "Blue Clover", "Blue Daffodil",
        "Blue Edelweiss", "Blue Lavender", "Blue Lotus", "Blue Pansy", "Chamomile",
        "Chicory", "Cozy Fireplace", "Desert Rose", "Prism Petal", "Purple Carnation",
        "Purple Cosmos", "Purple Edelweiss", "Purple Gladiolus", "Purple Pansy",
        "Red Carnation", "Red Cosmos", "Red Daffodil", "Red Edelweiss",
        "Red Gladiolus", "Red Lavender", "Red Lotus", "Red Pansy", "White Carnation",
        "White Cosmos", "White Daffodil", "White Edelweiss", "White Lavender",
        "White Lotus", "White Pansy", "Yellow Carnation", "Yellow Clover",
        "Yellow Daffodil", "Yellow Edelweiss", "Yellow Gladiolus", "Yellow Lavender",
        "Yellow Lotus", "Yellow Pansy"
    ],
    "Estufa": [
        "Grape", "Olive", "Rice"
    ],
    "Recursos": [
        "Crimstone", "Gem", "Gold", "Hardened Leather", "Iron", "Leather",
        "Oil", "Sand", "Stone", "Sunstone", "Wood"
    ],
    "Produtos_Animais": [
        "Egg", "Feather", "Honey", "Merino Wool", "Milk", "Wool"
    ],
    "Racao_Animal": [
        "Hay", "Kernel Blend", "Mixed Grain", "NutriBarley", "Omnifeed"
    ],
    "Animais_e_Mascotes": [
        "Autumn Duckling", "Baby Panda", "Badass Bear", "Basic Bear", "Brilliant Bear",
        "Butterfly", "Chicken", "Classy Bear", "Construction Bear", "Farmer Bear",
        "Fat Chicken", "Flower Fox", "Lunalist", "Macaw", "Mama Duck", "Mog",
        "Morty", "Pirate Bear", "Rich Chicken", "Speed Chicken", "Spring Duckling",
        "Squirrel", "Summer Duckling", "Ugly Duckling", "Vampire Bear", "Winter Duckling"
    ],

    "Peixes_e_Frutos_do_Mar": [
        "Angelfish", "Blue Marlin", "Blowfish", "Clownfish", "Crab",
        "Football fish", "Halibut", "Kraken Tentacle", "Moray Eel", "Napoleanfish",
        "Oarfish", "Olive Flounder", "Porgy", "Ray", "Red Snapper",
        "Rock Blackfish", "Sea Horse", "Squid", "Starlight Tuna", "Sunfish",
        "Surgeonfish", "Tilapia", "Tuna", "Walleye", "Weakfish",
        "Zebra Turkeyfish"
    ],
    "Tesouros_e_Achados": [
        "Amber Fossil", "Broken Pillar", "Camel Bone", "Clam Shell", "Cockle Shell",
        "Coral", "Cow Skull", "Hieroglyph", "Horseshoe", "Iron Compass",
        "Old Bottle", "Pearl", "Pirate Bounty", "Scarab", "Sea Cucumber",
        "Seaweed", "Starfish", "T-Rex Skull", "Treasure Key", "Treasure Map",
        "Vase", "Wooden Compass"
    ],
    "Comida_e_Bebidas": [
        "Apple Pie", "Banana Blast", "Beetroot Cake", "Blueberry Jam",
        "Bumpkin Broth", "Bumpkin Detox", "Bumpkin Roast", "Bumpkin Salad",
        "Cabbers n Mash", "Cabbage Cake", "Carrot Cake", "Carrot Juice",
        "Cauliflower Burger", "Cauliflower Cake", "Chowder", "Club Sandwich",
        "Cornbread", "Eggplant Cake", "Fermented Carrots", "Fermented Fish",
        "Fish Burger", "Fish n Chips", "Fish Omelette", "Fried Tofu", "Fruit Salad",
        "Goblin's Treat", "Gumbo", "Honey Cake", "Kale & Mushroom Pie",
        "Kale Omelette", "Kale Stew", "Lemon Cheesecake", "Mashed Potato",

        "Mushroom Jacket Potatoes", "Mushroom Soup", "Orange Cake", "Orange Juice",
        "Parsnip Cake", "Pirate Cake", "Pizza Margherita", "Popcorn",
        "Power Smoothie", "Pumpkin Cake", "Pumpkin Soup", "Purple Smoothie",
        "Quick Juice", "Radish Cake", "Rapid Roast", "Reindeer Carrot",
        "Roast Veggies", "Rhubarb Tart", "Sauerkraut", "Sour Shake",
        "Sunflower Cake", "The Lot", "Wheat Cake"
    ],
    "Ferramentas": [
        "Axe", "Brush", "Petting Hand", "Sand Drill", "Sand Shovel", "Shovel",
        "Stone Pickaxe"
    ],
    "Edificios_e_Itens_de_Fazenda": [
        "Bakery", "Bale", "Barn", "Basic Land", "Basic Scarecrow", "Beehive",
        "Compost Bin", "Crafting Box", "Crop Plot", "Deli", "Fire Pit", "Flower Bed",
        "Fruit Patch", "Greenhouse", "Hen House", "Kitchen", "Manor", "Market",
        "Premium Composter", "Smoothie Shack", "Spinning Wheel", "Time Warp Totem",
        "Toolshed", "Turbo Composter", "Water Well", "Workbench"
    ],
    "Decoração": [
        "Acorn House", "Aurora Lantern", "Basic Bed", "Blossombeard", "Bonnie's Tombstone",
        "Bumpkin Lantern", "Bumpkin Nutcracker", "Carrot House", "Christmas Stocking",
        "Cluckapult", "Cozy Fireplace", "Cushion", "Desert Gnome", "Fairy Circle",
        "Fence", "Festive Tree", "Fisher Bed", "Giant Potato", "Golden Maple",
        "Grubnash's Tombstone", "Igloo", "Kite", "Lake Rug", "Laurie the Chuckle Crow",
        "Luminous Lantern", "Mangrove", "Mini Floating Island", "Ocean Lantern",
        "Orange Bunny Lantern", "Orange Tunnel Bunny", "Potted Potato", "Potted Pumpkin",
        "Potted Sunflower", "Purple Trail", "Radiance Lantern", "Rug", "Scary Mike",
        "Skill Shrimpy", "Snowman", "Solar Lantern", "Spring Guardian", "Town Sign",
        "Tornado Pinwheel", "Twister Rug", "Wardrobe", "White Bunny Lantern",
        "White Tunnel Bunny"
    ],
    "Fertilizantes_e_Iscas": [
        "Earthworm", "Fishing Lure", "Fruitful Blend", "Grub", "Protective Pesticide",
        "Rapid Root", "Red Wiggler", "Sprout Mix"
    ],
    "Recursos_Naturais": [
        "Crimstone Rock", "Gold Beetle", "Gold Rock", "Iron Beetle", "Iron Rock",
        "Oil Reserve", "Stone Beetle", "Stone Rock", "Sunstone Rock", "Tree"
    ],
    "Itens_Especiais_e_Banners": [
        "Base Banner", "Easter Ticket 2025", "Gold Pass", "Great Bloom Banner",
        "Horseshoe", "Love Charm", "Mark", "Music Box", "Nightshade Emblem",
        "Nightshade Faction Banner", "Polygon Banner", "Potion Ticket", "Royal Bedding",
        "Timeshard", "Trade Point", "Winds of Change Banner"
    ]
}
# ---> FIM: CATEGORIAS DO INVENTÁRIO <---