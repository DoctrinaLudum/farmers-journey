APP_VERSION = "0.1.0"

# ==============================================================================
#  GAME DATA DICTIONARIES
#  Source of truth based on the game's internal data files.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. INVENTORY_ITEMS: Describes all items that can exist in the inventory.
#    This is the master catalogue for every single item.
# ------------------------------------------------------------------------------
INVENTORY_ITEMS = {
    # --- Resources ---
    "Wood":      {"type": "Resource", "source": "Tree",           "api_node_key": "trees"},
    "Stone":     {"type": "Resource", "source": "Stone Rock",     "api_node_key": "stones"},
    "Iron":      {"type": "Resource", "source": "Iron Rock",      "api_node_key": "iron"},
    "Gold":      {"type": "Resource", "source": "Gold Rock",      "api_node_key": "gold"},
    "Crimstone": {"type": "Resource", "source": "Crimstone Rock", "api_node_key": "crimstones"},
    "Sunstone":  {"type": "Resource", "source": "Sunstone Rock",  "api_node_key": "sunstones"},
    "Oil":       {"type": "Resource", "source": "Oil Reserve",    "api_node_key": "oilReserves"},
    "Diamond":   {"type": "Resource", "source": "Boulder",        "api_node_key": None},
    "Obsidian":  {"type": "Resource", "source": "Lava Pit",       "api_node_key": None},

    # --- Animal Products ---
    "Egg":         {"type": "Animal Product"},
    "Leather":     {"type": "Animal Product"},
    "Wool":        {"type": "Animal Product"},
    "Merino Wool": {"type": "Animal Product"},
    "Feather":     {"type": "Animal Product"},
    "Milk":        {"type": "Animal Product"},
    "Honey":       {"type": "Animal Product"},

    # --- Mushrooms ---
    "Wild Mushroom":  {"type": "Mushroom"},
    "Magic Mushroom": {"type": "Mushroom"},

    # --- Crops (The final produce from regular farming) ---
    "Sunflower":   {"type": "Crop", "sell_price": 0.02, "season": ["Spring", "Summer", "Autumn", "Winter"], "growtime": 60},        # 1 minute
    "Potato":      {"type": "Crop", "sell_price": 0.14, "season": ["Summer", "Autumn", "Winter"], "growtime": 300},       # 5 minutes
    "Rhubarb":     {"type": "Crop", "sell_price": 0.24, "season": ["Spring"], "growtime": 600},       # 10 minutes
    "Pumpkin":     {"type": "Crop", "sell_price": 0.4, "season": ["Autumn"], "growtime": 1800},      # 30 minutes
    "Zucchini":    {"type": "Crop", "sell_price": 0.4, "season": ["Summer"], "growtime": 1800},      # 30 minutes
    "Carrot":      {"type": "Crop", "sell_price": 0.8, "season": ["Spring", "Autumn"], "growtime": 3600},      # 1 hour
    "Yam":         {"type": "Crop", "sell_price": 0.8, "season": ["Autumn"], "growtime": 3600},      # 1 hour
    "Cabbage":     {"type": "Crop", "sell_price": 1.5, "season": ["Spring", "Winter"], "growtime": 7200},      # 2 hours
    "Broccoli":    {"type": "Crop", "sell_price": 1.5, "season": ["Autumn"], "growtime": 7200},      # 2 hours
    "Soybean":     {"type": "Crop", "sell_price": 2.3, "season": ["Spring", "Autumn"], "growtime": 10800},     # 3 hours
    "Beetroot":    {"type": "Crop", "sell_price": 2.8, "season": ["Summer", "Winter"], "growtime": 14400},     # 4 hours
    "Pepper":      {"type": "Crop", "sell_price": 3, "season": ["Summer"], "growtime": 14400},     # 4 hours
    "Cauliflower": {"type": "Crop", "sell_price": 4.25, "season": ["Summer", "Winter"], "growtime": 28800},     # 8 hours
    "Parsnip":     {"type": "Crop", "sell_price": 6.5, "season": ["Winter"], "growtime": 43200},     # 12 hours
    "Eggplant":    {"type": "Crop", "sell_price": 8, "season": ["Summer"], "growtime": 57600},     # 16 hours
    "Corn":        {"type": "Crop", "sell_price": 9, "season": ["Spring"], "growtime": 72000},     # 20 hours
    "Onion":       {"type": "Crop", "sell_price": 10, "season": ["Winter"], "growtime": 72000},     # 20 hours
    "Radish":      {"type": "Crop", "sell_price": 9.5, "season": ["Summer"], "growtime": 86400},     # 24 hours
    "Wheat":       {"type": "Crop", "sell_price": 7, "season": ["Spring", "Summer", "Autumn", "Winter"], "growtime": 86400}, # 24 hours
    "Turnip":      {"type": "Crop", "sell_price": 8, "season": ["Winter"], "growtime": 86400},     # 24 hours
    "Kale":        {"type": "Crop", "sell_price": 10, "season": ["Spring", "Winter"], "growtime": 129600},    # 36 hours
    "Artichoke":   {"type": "Crop", "sell_price": 12, "season": ["Autumn"], "growtime": 129600},    # 36 hours
    "Barley":      {"type": "Crop", "sell_price": 12, "season": ["Spring", "Autumn"], "growtime": 172800},    # 48 hours


    # --- Greenhouse Produce (Crops & Fruits) ---
    "Rice":  {"type": "GreenhouseCrop", "sell_price": 320, "season": ["Spring", "Summer", "Autumn", "Winter"], "growtime": 115200}, # 32 hours
    "Olive": {"type": "GreenhouseCrop", "sell_price": 400, "season": ["Spring", "Summer", "Autumn", "Winter"], "growtime": 158400}, # 44 hours
    "Grape": {"type": "GreenhouseFruit", "sell_price": 240, "season": ["Spring", "Summer", "Autumn", "Winter"], "growtime": 43200}, # 12 hours

    
    
    # --- Exotic Crops (from Magic Beans) ---
    "Black Magic":          {"type": "ExoticCrop", "sell_price": 32000},
    "Golden Helios":        {"type": "ExoticCrop", "sell_price": 16000},
    "Chiogga":              {"type": "ExoticCrop", "sell_price": 8000},
    "Purple Cauliflower":   {"type": "ExoticCrop", "sell_price": 3200},
    "Adirondack Potato":    {"type": "ExoticCrop", "sell_price": 2400},
    "Warty Goblin Pumpkin": {"type": "ExoticCrop", "sell_price": 1600},
    "White Carrot":         {"type": "ExoticCrop", "sell_price": 800},

    # --- Treasures ---
    "Sand":             {"type": "Treasure", "sell_price": 10},
    "Camel Bone":       {"type": "Treasure", "sell_price": 10},
    "Crab":             {"type": "Treasure", "sell_price": 15},
    "Old Bottle":       {"type": "Treasure", "sell_price": 22.5},
    "Sea Cucumber":     {"type": "Treasure", "sell_price": 22.5},
    "Vase":             {"type": "Treasure", "sell_price": 50},
    "Seaweed":          {"type": "Treasure", "sell_price": 75},
    "Cockle Shell":     {"type": "Treasure", "sell_price": 100},
    "Starfish":         {"type": "Treasure", "sell_price": 112.5},
    "Wooden Compass":   {"type": "Treasure", "sell_price": 131.25},
    "Iron Compass":     {"type": "Treasure", "sell_price": 187.5},
    "Emerald Compass":  {"type": "Treasure", "sell_price": 187.5},
    "Pipi":             {"type": "Treasure", "sell_price": 187.5},
    "Hieroglyph":       {"type": "Treasure", "sell_price": 250},
    "Clam Shell":       {"type": "Treasure", "sell_price": 375},
    "Coral":            {"type": "Treasure", "sell_price": 1500},
    "Pearl":            {"type": "Treasure", "sell_price": 3750},
    "Pirate Bounty":    {"type": "Treasure", "sell_price": 7500},
    "Scarab":           {"type": "Treasure", "sell_price": 200},
    "Cow Skull":        {"type": "Treasure", "sell_price": 200},
    "Ancient Clock":    {"type": "Treasure", "sell_price": 200},
    "Broken Pillar":    {"type": "Treasure", "sell_price": 200},

    # --- Tools ---
    "Axe":            {"type": "Tool", "price": 20, "ingredients": {}},
    "Pickaxe":        {"type": "Tool", "price": 20, "ingredients": {"Wood": 3}},
    "Stone Pickaxe":  {"type": "Tool", "price": 20, "ingredients": {"Wood": 3, "Stone": 5}},
    "Iron Pickaxe":   {"type": "Tool", "price": 80, "ingredients": {"Wood": 3, "Iron": 5}},
    "Gold Pickaxe":   {"type": "Tool", "price": 100, "ingredients": {"Wood": 3, "Gold": 3}},
    "Rod":            {"type": "Tool", "price": 20, "ingredients": {"Wood": 3, "Stone": 1}},
    "Oil Drill":      {"type": "Tool", "price": 100, "ingredients": {"Wood": 20, "Iron": 9, "Leather": 10}},
    "Sand Shovel":    {"type": "Tool", "price": 20, "ingredients": {"Wood": 2, "Stone": 1}},
    "Sand Drill":     {"type": "Tool", "price": 40, "ingredients": {"Oil": 1, "Crimstone": 1, "Wood": 3, "Leather": 1}},
    "Petting Hand":   {"type": "Tool", "price": 0, "ingredients": {}},
    "Brush":          {"type": "Tool", "price": 2000, "ingredients": {}},
    "Music Box":      {"type": "Tool", "price": 50000, "ingredients": {}},

    # --- Animal Food & Medicine ---
    "Kernel Blend": {"type": "AnimalFood", "ingredients": {"Corn": 1}},
    "Hay":          {"type": "AnimalFood", "ingredients": {"Wheat": 1}},
    "NutriBarley":  {"type": "AnimalFood", "ingredients": {"Barley": 1}},
    "Mixed Grain":  {"type": "AnimalFood", "ingredients": {"Wheat": 1, "Corn": 1, "Barley": 1}},
    "Barn Delight": {"type": "AnimalMedicine", "ingredients": {"Lemon": 5, "Honey": 3}},
    "Omnifeed":     {"type": "AnimalFood", "ingredients": {"Gem": 1}},

    

    # --- Seeds (The items you plant) ---
    "Sunflower Seed":   {"type": "Seed", "yields": "Sunflower", "cost_coins": 0.01, "bumpkin_level": 1, "planting_spot": "Crop Plot"},
    "Potato Seed":      {"type": "Seed", "yields": "Potato",    "cost_coins": 0.1,  "bumpkin_level": 1, "planting_spot": "Crop Plot"},
    "Rhubarb Seed":     {"type": "Seed", "yields": "Rhubarb",   "cost_coins": 0.15, "bumpkin_level": 1, "planting_spot": "Crop Plot"},
    "Pumpkin Seed":     {"type": "Seed", "yields": "Pumpkin",   "cost_coins": 0.2,  "bumpkin_level": 2, "planting_spot": "Crop Plot"},
    "Zucchini Seed":    {"type": "Seed", "yields": "Zucchini",  "cost_coins": 0.2,  "bumpkin_level": 2, "planting_spot": "Crop Plot"},
    "Carrot Seed":      {"type": "Seed", "yields": "Carrot",    "cost_coins": 0.5,  "bumpkin_level": 2, "planting_spot": "Crop Plot"},
    "Yam Seed":         {"type": "Seed", "yields": "Yam",       "cost_coins": 0.5,  "bumpkin_level": 2, "planting_spot": "Crop Plot"},
    "Cabbage Seed":     {"type": "Seed", "yields": "Cabbage",   "cost_coins": 1,    "bumpkin_level": 3, "planting_spot": "Crop Plot"},
    "Broccoli Seed":    {"type": "Seed", "yields": "Broccoli",  "cost_coins": 1,    "bumpkin_level": 3, "planting_spot": "Crop Plot"},
    "Soybean Seed":     {"type": "Seed", "yields": "Soybean",   "cost_coins": 1.5,  "bumpkin_level": 3, "planting_spot": "Crop Plot"},
    "Beetroot Seed":    {"type": "Seed", "yields": "Beetroot",  "cost_coins": 2,    "bumpkin_level": 3, "planting_spot": "Crop Plot"},
    "Pepper Seed":      {"type": "Seed", "yields": "Pepper",    "cost_coins": 2,    "bumpkin_level": 3, "planting_spot": "Crop Plot"},
    "Cauliflower Seed": {"type": "Seed", "yields": "Cauliflower", "cost_coins": 3,  "bumpkin_level": 4, "planting_spot": "Crop Plot"},
    "Parsnip Seed":     {"type": "Seed", "yields": "Parsnip",   "cost_coins": 5,    "bumpkin_level": 4, "planting_spot": "Crop Plot"},
    "Eggplant Seed":    {"type": "Seed", "yields": "Eggplant",  "cost_coins": 6,    "bumpkin_level": 5, "planting_spot": "Crop Plot"},
    "Corn Seed":        {"type": "Seed", "yields": "Corn",      "cost_coins": 7,    "bumpkin_level": 5, "planting_spot": "Crop Plot"},
    "Onion Seed":       {"type": "Seed", "yields": "Onion",     "cost_coins": 7,    "bumpkin_level": 5, "planting_spot": "Crop Plot"},
    "Radish Seed":      {"type": "Seed", "yields": "Radish",    "cost_coins": 7,    "bumpkin_level": 5, "planting_spot": "Crop Plot"},
    "Wheat Seed":       {"type": "Seed", "yields": "Wheat",     "cost_coins": 5,    "bumpkin_level": 5, "planting_spot": "Crop Plot"},
    "Turnip Seed":      {"type": "Seed", "yields": "Turnip",    "cost_coins": 5,    "bumpkin_level": 6, "planting_spot": "Crop Plot"},
    "Kale Seed":        {"type": "Seed", "yields": "Kale",      "cost_coins": 7,    "bumpkin_level": 7, "planting_spot": "Crop Plot"},
    "Artichoke Seed":   {"type": "Seed", "yields": "Artichoke", "cost_coins": 7,    "bumpkin_level": 8, "planting_spot": "Crop Plot"},
    "Barley Seed":      {"type": "Seed", "yields": "Barley",    "cost_coins": 10,   "bumpkin_level": 14,"planting_spot": "Crop Plot"},
    "Tomato Seed":    {"type": "Seed", "yields": "Tomato",    "cost_coins": 5,   "bumpkin_level": 13, "planting_spot": "Fruit Patch"},
    "Lemon Seed":     {"type": "Seed", "yields": "Lemon",     "cost_coins": 15,  "bumpkin_level": 12, "planting_spot": "Fruit Patch"},
    "Blueberry Seed": {"type": "Seed", "yields": "Blueberry", "cost_coins": 30,  "bumpkin_level": 13, "planting_spot": "Fruit Patch"},
    "Orange Seed":    {"type": "Seed", "yields": "Orange",    "cost_coins": 50,  "bumpkin_level": 14, "planting_spot": "Fruit Patch"},
    "Apple Seed":     {"type": "Seed", "yields": "Apple",     "cost_coins": 70,  "bumpkin_level": 15, "planting_spot": "Fruit Patch"},
    "Banana Plant":   {"type": "Seed", "yields": "Banana",    "cost_coins": 70,  "bumpkin_level": 16, "planting_spot": "Fruit Patch"},
    "Celestine Seed": {"type": "Seed", "yields": "Celestine", "cost_coins": 300, "bumpkin_level": 12, "planting_spot": "Fruit Patch"},
    "Lunara Seed":    {"type": "Seed", "yields": "Lunara",    "cost_coins": 750, "bumpkin_level": 12, "planting_spot": "Fruit Patch"},
    "Duskberry Seed": {"type": "Seed", "yields": "Duskberry", "cost_coins": 1250,"bumpkin_level": 12, "planting_spot": "Fruit Patch"},
    "Grape Seed": {"type": "Seed", "yields": "Grape", "cost_coins": 160, "bumpkin_level": 40, "planting_spot": "Greenhouse"},
    "Rice Seed":  {"type": "Seed", "yields": "Rice",  "cost_coins": 240, "bumpkin_level": 40, "planting_spot": "Greenhouse"},
    "Olive Seed": {"type": "Seed", "yields": "Olive", "cost_coins": 320, "bumpkin_level": 40, "planting_spot": "Greenhouse"},
    "Sunpetal Seed":  {"type": "Seed", "yields": "Flower", "cost_coins": 16, "bumpkin_level": 13, "planting_spot": "Flower Bed", "growtime": 86400},
    "Bloom Seed":     {"type": "Seed", "yields": "Flower", "cost_coins": 32, "bumpkin_level": 22, "planting_spot": "Flower Bed", "growtime": 172800},
    "Lily Seed":      {"type": "Seed", "yields": "Flower", "cost_coins": 48, "bumpkin_level": 27, "planting_spot": "Flower Bed", "growtime": 432000},
    "Edelweiss Seed": {"type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35, "planting_spot": "Flower Bed", "growtime": 259200},
    "Gladiolus Seed": {"type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35, "planting_spot": "Flower Bed", "growtime": 259200},
    "Lavender Seed":  {"type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35, "planting_spot": "Flower Bed", "growtime": 259200},
    "Clover Seed":    {"type": "Seed", "yields": "Flower", "cost_coins": 96, "bumpkin_level": 35, "planting_spot": "Flower Bed", "growtime": 259200},
    "Magic Bean": {"type": "Seed", "yields": "ExoticCrop", "cost_coins": 0, "bumpkin_level": 0, "planting_spot": "Special", "growtime": 172800},
}

# ------------------------------------------------------------------------------
# 2. RESOURCE_NODES: Describes the objects on the farm that yield resources.
# ------------------------------------------------------------------------------
RESOURCE_NODES = {
    "Tree": {"name": "Tree", "yields": "Wood", "dimensions": {"width": 2, "height": 2}, "respawn_time_seconds": 7200},
    "Stone Rock": {"name": "Stone Rock", "yields": "Stone", "dimensions": {"width": 1, "height": 1}, "respawn_time_seconds": 14400},
    "Iron Rock": {"name": "Iron Rock", "yields": "Iron", "dimensions": {"width": 1, "height": 1}, "respawn_time_seconds": 28800},
    "Gold Rock": {"name": "Gold Rock", "yields": "Gold", "dimensions": {"width": 1, "height": 1}, "respawn_time_seconds": 43200},
    "Crimstone Rock": {"name": "Crimstone Rock", "yields": "Crimstone", "dimensions": {"width": 2, "height": 2}, "respawn_time_seconds": 86400},
    "Sunstone Rock": {"name": "Sunstone Rock", "yields": "Sunstone", "dimensions": {"width": 2, "height": 2}, "respawn_time_seconds": 172800},
    "Oil Reserve": {"name": "Oil Reserve", "yields": "Oil", "dimensions": {"width": 2, "height": 2}, "respawn_time_seconds": 345600},
    "Boulder": {"name": "Boulder", "yields": "Diamond", "dimensions": {"width": 2, "height": 2}, "respawn_time_seconds": None},
    "Lava Pit": {"name": "Lava Pit", "yields": "Obsidian", "dimensions": {"width": 2, "height": 2}, "respawn_time_seconds": None},
    "Crop Plot": {"name": "Crop Plot", "yields_category": "Crop", "dimensions": {"width": 1, "height": 1}, "respawn_time_seconds": None},
    "Fruit Patch": {"name": "Fruit Patch", "yields_category": "Fruit", "dimensions": {"width": 2, "height": 2}, "respawn_time_seconds": None},
    "Flower Bed": {"name": "Flower Bed", "yields_category": "Flower", "dimensions": {"width": 3, "height": 1}, "respawn_time_seconds": None},
    "Hen House": {"name": "Hen House", "yields_category": "Animal", "dimensions": {"width": 4, "height": 3}, "respawn_time_seconds": None},
    "Barn": {"name": "Barn", "yields_category": "Animal", "dimensions": {"width": 4, "height": 4}, "respawn_time_seconds": None},
    "Beehive": {"name": "Beehive", "yields": "Honey", "dimensions": {"width": 1, "height": 1}, "respawn_time_seconds": None},
    "Compost Bin": {"name": "Compost Bin", "yields": "Sprout Mix", "dimensions": {"width": 2, "height": 2}, "time_to_finish_seconds": 21600},
    "Turbo Composter": {"name": "Turbo Composter", "yields": "Fruitful Blend", "dimensions": {"width": 2, "height": 2}, "time_to_finish_seconds": 28800},
    "Premium Composter": {"name": "Premium Composter", "yields": "Rapid Root", "dimensions": {"width": 2, "height": 2}, "time_to_finish_seconds": 43200},
}

# ------------------------------------------------------------------------------
# 3. BUILDINGS: Details for constructing buildings.
# ------------------------------------------------------------------------------
BUILDINGS = {
    # --- Main Buildings ---
    "Town Center": {
        "unlocks_at_level": 99,
        "coins": 0,
        "construction_seconds": 30,
        "ingredients": {},
        "dimensions": {"width": 4, "height": 3}
    },
    "Market": {
        "unlocks_at_level": 99,
        "coins": 0,
        "construction_seconds": 30,
        "ingredients": {},
        "dimensions": {"width": 3, "height": 2}
    },
    "Workbench": {
        "unlocks_at_level": 99,
        "coins": 5,
        "construction_seconds": 60,
        "ingredients": {},
        "dimensions": {"width": 3, "height": 2}
    },
    "Warehouse": {
        "unlocks_at_level": 20,
        "coins": 0,
        "construction_seconds": 7200,
        "ingredients": {"Wood": 250, "Stone": 150, "Potato": 5000, "Pumpkin": 2000, "Wheat": 500, "Kale": 100},
        "dimensions": {"width": 3, "height": 2}
    },
    "Toolshed": {
        "unlocks_at_level": 25,
        "coins": 0,
        "construction_seconds": 7200,
        "ingredients": {"Wood": 500, "Iron": 30, "Gold": 25, "Axe": 100, "Pickaxe": 50},
        "dimensions": {"width": 2, "height": 3}
    },
    "Water Well": {
        "unlocks_at_level": 2,
        "coins": 100,
        "construction_seconds": 300,
        "ingredients": {"Wood": 5},
        "dimensions": {"width": 2, "height": 2}
    },
     "Crafting Box": {
        "unlocks_at_level": 6,
        "coins": 0,
        "construction_seconds": 3600,
        "ingredients": {"Wood": 100, "Stone": 5},
        "dimensions": {"width": 3, "height": 2}
    },

    # --- Cooking Buildings ---
    "Fire Pit": {
        "unlocks_at_level": 99,
        "coins": 0,
        "construction_seconds": 0,
        "ingredients": {"Wood": 3, "Stone": 2},
        "dimensions": {"width": 3, "height": 2}
    },
    "Kitchen": {
        "unlocks_at_level": 5,
        "coins": 10,
        "construction_seconds": 1800,
        "ingredients": {"Wood": 30, "Stone": 5},
        "dimensions": {"width": 4, "height": 3}
    },
    "Bakery": {
        "unlocks_at_level": 8,
        "coins": 200,
        "construction_seconds": 14400,
        "ingredients": {"Wood": 50, "Stone": 20, "Gold": 5},
        "dimensions": {"width": 4, "height": 3}
    },
    "Deli": {
        "unlocks_at_level": 16,
        "coins": 300,
        "construction_seconds": 43200,
        "ingredients": {"Wood": 50, "Stone": 50, "Gold": 10},
        "dimensions": {"width": 4, "height": 3}
    },
    "Smoothie Shack": {
        "unlocks_at_level": 23,
        "coins": 0,
        "construction_seconds": 43200,
        "ingredients": {"Wood": 25, "Stone": 25, "Iron": 10},
        "dimensions": {"width": 3, "height": 2}
    },

    # --- Animal Buildings ---
    "Hen House": {
        "unlocks_at_level": 6,
        "coins": 100,
        "construction_seconds": 7200,
        "ingredients": {"Wood": 30, "Iron": 5, "Gold": 5},
        "dimensions": {"width": 4, "height": 3}
    },
    "Barn": {
        "unlocks_at_level": 30,
        "coins": 200,
        "construction_seconds": 7200,
        "ingredients": {"Wood": 150, "Iron": 10, "Gold": 10},
        "dimensions": {"width": 4, "height": 4}
    },

    # --- Farming Buildings ---
    "Greenhouse": {
        "unlocks_at_level": 46,
        "coins": 4800,
        "construction_seconds": 14400,
        "ingredients": {"Wood": 500, "Stone": 100, "Crimstone": 25, "Oil": 100},
        "dimensions": {"width": 4, "height": 4}
    },
    "Compost Bin": {
        "unlocks_at_level": 7,
        "coins": 0,
        "construction_seconds": 3600,
        "ingredients": {"Wood": 5, "Stone": 5},
        "dimensions": {"width": 2, "height": 2}
    },
    "Turbo Composter": {
        "unlocks_at_level": 12,
        "coins": 0,
        "construction_seconds": 7200,
        "ingredients": {"Wood": 50, "Stone": 25},
        "dimensions": {"width": 2, "height": 2}
    },
    "Premium Composter": {
        "unlocks_at_level": 18,
        "coins": 0,
        "construction_seconds": 14400,
        "ingredients": {"Gold": 50},
        "dimensions": {"width": 2, "height": 2}
    },
    "Crop Machine": {
        "unlocks_at_level": 35,
        "coins": 8000,
        "construction_seconds": 7200,
        "ingredients": {"Wood": 1250, "Iron": 125, "Crimstone": 50},
        "dimensions": {"width": 5, "height": 4}
    },
    
    # --- Homes & Beds (Decoration Buildings) ---
    "Tent": {
        "unlocks_at_level": 99,
        "coins": 20,
        "construction_seconds": 3600,
        "ingredients": {"Wood": 50},
        "dimensions": {"width": 3, "height": 2}
    },
    "House": {
        "unlocks_at_level": 99,
        "coins": 0,
        "construction_seconds": 30,
        "ingredients": {},
        "dimensions": {"width": 4, "height": 4}
    },
    "Manor": {
        "unlocks_at_level": 99,
        "coins": 0,
        "construction_seconds": 30,
        "ingredients": {},
        "dimensions": {"width": 5, "height": 4}
    },
    "Mansion": {
        "unlocks_at_level": 99,
        "coins": 0,
        "construction_seconds": 30,
        "ingredients": {},
        "dimensions": {"width": 6, "height": 5}
    },
    "Basic Bed": {
        "farmhand_count": 1
    },
    "Fisher Bed": {
        "farmhand_count": 2
    },
    "Floral Bed": {
        "farmhand_count": 3
    },
    "Sturdy Bed": {
        "farmhand_count": 4
    },
    "Desert Bed": {
        "farmhand_count": 5
    },
    "Cow Bed": {
        "farmhand_count": 6
    },
    "Pirate Bed": {
        "farmhand_count": 7
    },
    "Royal Bed": {
        "farmhand_count": 8
    },
}

# ==============================================================================
# 4. ANIMALS: Details about purchasable animals.
# ==============================================================================
ANIMALS = {
    "Chicken": {
        "coins": 50,
        "level_required": 6,
        "building_required": "Hen House",
        "dimensions": {"width": 2, "height": 2},
        "resource_drops": { # Level: {Resource: Amount}
            1: {"Egg": 1}, 2: {"Egg": 1},
            3: {"Egg": 1, "Feather": 1},
            4: {"Egg": 2, "Feather": 1}, 5: {"Egg": 2, "Feather": 1}, 6: {"Egg": 2, "Feather": 1}, 7: {"Egg": 2, "Feather": 1},
            8: {"Egg": 3, "Feather": 1},
            9: {"Egg": 3, "Feather": 2}, 10: {"Egg": 3, "Feather": 2}, 11: {"Egg": 3, "Feather": 2}, 12: {"Egg": 3, "Feather": 2},
            13: {"Egg": 4, "Feather": 2}, 14: {"Egg": 4, "Feather": 2},
            15: {"Egg": 5, "Feather": 3}
        }
    },
    "Cow": {
        "coins": 100,
        "level_required": 14,
        "building_required": "Barn",
        "dimensions": {"width": 2, "height": 2},
        "resource_drops": { # Level: {Resource: Amount}
            1: {"Milk": 1},
            2: {"Milk": 1, "Leather": 1},
            3: {"Milk": 2},
            4: {"Milk": 2, "Leather": 1},
            5: {"Milk": 2, "Leather": 2},
            6: {"Milk": 3},
            7: {"Milk": 3, "Leather": 1},
            8: {"Milk": 3, "Leather": 2},
            9: {"Milk": 3, "Leather": 3}, 10: {"Milk": 3, "Leather": 3}, 11: {"Milk": 3, "Leather": 3}, 12: {"Milk": 3, "Leather": 3}, 13: {"Milk": 3, "Leather": 3}, 14: {"Milk": 3, "Leather": 3}, 15: {"Milk": 3, "Leather": 3}
        }
    },
    "Sheep": {
        "coins": 120,
        "level_required": 18,
        "building_required": "Barn",
        "dimensions": {"width": 2, "height": 2},
        "resource_drops": { # Level: {Resource: Amount}
            1: {"Wool": 1},
            2: {"Wool": 1, "Merino Wool": 1},
            3: {"Wool": 2},
            4: {"Wool": 2, "Merino Wool": 1},
            5: {"Wool": 2, "Merino Wool": 2},
            6: {"Wool": 3},
            7: {"Wool": 3, "Merino Wool": 1},
            8: {"Wool": 3, "Merino Wool": 2},
            9: {"Wool": 3, "Merino Wool": 3}, 10: {"Wool": 3, "Merino Wool": 3}, 11: {"Wool": 3, "Merino Wool": 3}, 12: {"Wool": 3, "Merino Wool": 3}, 13: {"Wool": 3, "Merino Wool": 3}, 14: {"Wool": 3, "Merino Wool": 3}, 15: {"Wool": 3, "Merino Wool": 3}
        }
    }
}

# ------------------------------------------------------------------------------
# 5. CONSUMABLES: Crafting recipes for food items.
# ------------------------------------------------------------------------------
CONSUMABLES = {
    # --- Fire Pit ---
    "Mashed Potato":  {"experience": 3,    "cooking_seconds": 30,    "building": "Fire Pit", "ingredients": {"Potato": 8}},
    "Pumpkin Soup":   {"experience": 24,   "cooking_seconds": 180,   "building": "Fire Pit", "ingredients": {"Pumpkin": 10}},
    "Reindeer Carrot":{"experience": 36,   "cooking_seconds": 300,   "building": "Fire Pit", "ingredients": {"Carrot": 5}},
    "Mushroom Soup":  {"experience": 56,   "cooking_seconds": 600,   "building": "Fire Pit", "ingredients": {"Wild Mushroom": 5}},
    "Popcorn":        {"experience": 200,  "cooking_seconds": 720,   "building": "Fire Pit", "ingredients": {"Sunflower": 100, "Corn": 5}},
    "Bumpkin Broth":  {"experience": 96,   "cooking_seconds": 1200,  "building": "Fire Pit", "ingredients": {"Carrot": 10, "Cabbage": 5}},
    "Cabbers n Mash": {"experience": 250,  "cooking_seconds": 2400,  "building": "Fire Pit", "ingredients": {"Mashed Potato": 10, "Cabbage": 20}},
    "Boiled Eggs":    {"experience": 90,   "cooking_seconds": 3600,  "building": "Fire Pit", "ingredients": {"Egg": 10}},
    "Kale Stew":      {"experience": 400,  "cooking_seconds": 7200,  "building": "Fire Pit", "ingredients": {"Kale": 10}},
    "Kale Omelette":  {"experience": 1250, "cooking_seconds": 12600, "building": "Fire Pit", "ingredients": {"Egg": 40, "Kale": 5}},
    "Gumbo":          {"experience": 600,  "cooking_seconds": 14400, "building": "Fire Pit", "ingredients": {"Potato": 50, "Pumpkin": 30, "Carrot": 20, "Red Snapper": 3}},
    "Fried Tofu":     {"experience": 400,  "cooking_seconds": 5400,  "building": "Fire Pit", "ingredients": {"Soybean": 15, "Sunflower": 200}},
    "Rice Bun":       {"experience": 2600, "cooking_seconds": 18000, "building": "Fire Pit", "ingredients": {"Rice": 2, "Wheat": 50}},
    "Antipasto":      {"experience": 3000, "cooking_seconds": 10800, "building": "Fire Pit", "ingredients": {"Olive": 2, "Grape": 2}},
    "Pizza Margherita":{"experience": 25000,"cooking_seconds": 72000, "building": "Fire Pit", "ingredients": {"Tomato": 30, "Cheese": 5, "Wheat": 20}},
    "Rhubarb Tart":   {"experience": 5,    "cooking_seconds": 60,    "building": "Fire Pit", "ingredients": {"Rhubarb": 3}},
    
    # --- Kitchen ---
    "Sunflower Crunch":       {"experience": 50,   "cooking_seconds": 600,   "building": "Kitchen", "ingredients": {"Sunflower": 300}},
    "Mushroom Jacket Potatoes":{"experience": 240,  "cooking_seconds": 600,   "building": "Kitchen", "ingredients": {"Wild Mushroom": 10, "Potato": 5}},
    "Fruit Salad":            {"experience": 225,  "cooking_seconds": 1800,  "building": "Kitchen", "ingredients": {"Apple": 1, "Orange": 1, "Blueberry": 1}},
    "Pancakes":               {"experience": 1000, "cooking_seconds": 3600,  "building": "Kitchen", "ingredients": {"Wheat": 10, "Egg": 10, "Honey": 6}},
    "Roast Veggies":          {"experience": 170,  "cooking_seconds": 7200,  "building": "Kitchen", "ingredients": {"Cauliflower": 15, "Carrot": 10}},
    "Cauliflower Burger":     {"experience": 255,  "cooking_seconds": 10800, "building": "Kitchen", "ingredients": {"Cauliflower": 15, "Wheat": 5}},
    "Club Sandwich":          {"experience": 170,  "cooking_seconds": 10800, "building": "Kitchen", "ingredients": {"Sunflower": 100, "Carrot": 25, "Wheat": 5}},
    "Bumpkin Salad":          {"experience": 290,  "cooking_seconds": 12600, "building": "Kitchen", "ingredients": {"Beetroot": 20, "Parsnip": 10}},
    "Bumpkin ganoush":        {"experience": 1000, "cooking_seconds": 18000, "building": "Kitchen", "ingredients": {"Eggplant": 30, "Potato": 50, "Parsnip": 10}},
    "Goblin's Treat":         {"experience": 500,  "cooking_seconds": 21600, "building": "Kitchen", "ingredients": {"Pumpkin": 10, "Radish": 20, "Cabbage": 10}},
    "Chowder":                {"experience": 1000, "cooking_seconds": 28800, "building": "Kitchen", "ingredients": {"Beetroot": 10, "Wheat": 10, "Parsnip": 5, "Anchovy": 3}},
    "Bumpkin Roast":          {"experience": 2500, "cooking_seconds": 43200, "building": "Kitchen", "ingredients": {"Mashed Potato": 20, "Roast Veggies": 5}},
    "Goblin Brunch":          {"experience": 2500, "cooking_seconds": 43200, "building": "Kitchen", "ingredients": {"Boiled Eggs": 5, "Goblin's Treat": 1}},
    "Steamed Red Rice":       {"experience": 3000, "cooking_seconds": 14400, "building": "Kitchen", "ingredients": {"Rice": 3, "Beetroot": 50}},
    "Tofu Scramble":          {"experience": 1000, "cooking_seconds": 10800, "building": "Kitchen", "ingredients": {"Soybean": 20, "Egg": 20, "Cauliflower": 10}},
    "Fried Calamari":         {"experience": 1500, "cooking_seconds": 18000, "building": "Kitchen", "ingredients": {"Sunflower": 200, "Wheat": 15, "Squid": 1}},
    "Fish Burger":            {"experience": 1300, "cooking_seconds": 7200,  "building": "Kitchen", "ingredients": {"Beetroot": 10, "Wheat": 10, "Horse Mackerel": 1}},
    "Fish Omelette":          {"experience": 1500, "cooking_seconds": 18000, "building": "Kitchen", "ingredients": {"Egg": 40, "Surgeonfish": 1, "Butterflyfish": 2}},
    "Ocean's Olive":          {"experience": 2000, "cooking_seconds": 7200,  "building": "Kitchen", "ingredients": {"Olive Flounder": 1, "Olive": 2}},
    "Seafood Basket":         {"experience": 2200, "cooking_seconds": 18000, "building": "Kitchen", "ingredients": {"Blowfish": 2, "Napoleanfish": 2, "Sunfish": 2}},
    "Fish n Chips":           {"experience": 2000, "cooking_seconds": 14400, "building": "Kitchen", "ingredients": {"Fancy Fries": 1, "Halibut": 1}},
    "Sushi Roll":             {"experience": 2000, "cooking_seconds": 3600,  "building": "Kitchen", "ingredients": {"Angelfish": 1, "Seaweed": 1, "Rice": 2}},
    "Caprese Salad":          {"experience": 6000, "cooking_seconds": 10800, "building": "Kitchen", "ingredients": {"Cheese": 1, "Tomato": 25, "Kale": 20}},
    "Spaghetti al Limone":    {"experience": 15000,"cooking_seconds": 54000, "building": "Kitchen", "ingredients": {"Wheat": 10, "Lemon": 15, "Cheese": 3}},

    # --- Bakery ---
    "Apple Pie":             {"experience": 720,  "cooking_seconds": 14400, "building": "Bakery", "ingredients": {"Apple": 5, "Wheat": 10, "Egg": 20}},
    "Orange Cake":           {"experience": 730,  "cooking_seconds": 14400, "building": "Bakery", "ingredients": {"Orange": 5, "Egg": 30, "Wheat": 10}},
    "Kale & Mushroom Pie":   {"experience": 720,  "cooking_seconds": 14400, "building": "Bakery", "ingredients": {"Wild Mushroom": 10, "Kale": 5, "Wheat": 5}},
    "Sunflower Cake":        {"experience": 525,  "cooking_seconds": 23400, "building": "Bakery", "ingredients": {"Sunflower": 1000, "Wheat": 10, "Egg": 30}},
    "Honey Cake":            {"experience": 4000, "cooking_seconds": 28800, "building": "Bakery", "ingredients": {"Honey": 10, "Wheat": 10, "Egg": 20}},
    "Potato Cake":           {"experience": 650,  "cooking_seconds": 37800, "building": "Bakery", "ingredients": {"Potato": 500, "Wheat": 10, "Egg": 30}},
    "Pumpkin Cake":          {"experience": 625,  "cooking_seconds": 37800, "building": "Bakery", "ingredients": {"Pumpkin": 130, "Wheat": 10, "Egg": 30}},
    "Cornbread":             {"experience": 600,  "cooking_seconds": 43200, "building": "Bakery", "ingredients": {"Corn": 15, "Wheat": 5, "Egg": 10}},
    "Carrot Cake":           {"experience": 750,  "cooking_seconds": 46800, "building": "Bakery", "ingredients": {"Carrot": 120, "Wheat": 10, "Egg": 30}},
    "Cabbage Cake":          {"experience": 860,  "cooking_seconds": 54000, "building": "Bakery", "ingredients": {"Cabbage": 90, "Wheat": 10, "Egg": 30}},
    "Beetroot Cake":         {"experience": 1250, "cooking_seconds": 79200, "building": "Bakery", "ingredients": {"Beetroot": 100, "Wheat": 10, "Egg": 30}},
    "Cauliflower Cake":      {"experience": 1190, "cooking_seconds": 79200, "building": "Bakery", "ingredients": {"Cauliflower": 60, "Wheat": 10, "Egg": 30}},
    "Parsnip Cake":          {"experience": 1300, "cooking_seconds": 86400, "building": "Bakery", "ingredients": {"Parsnip": 45, "Wheat": 10, "Egg": 30}},
    "Eggplant Cake":         {"experience": 1400, "cooking_seconds": 86400, "building": "Bakery", "ingredients": {"Eggplant": 30, "Wheat": 10, "Egg": 30}},
    "Radish Cake":           {"experience": 1200, "cooking_seconds": 86400, "building": "Bakery", "ingredients": {"Radish": 25, "Wheat": 10, "Egg": 30}},
    "Wheat Cake":            {"experience": 1100, "cooking_seconds": 86400, "building": "Bakery", "ingredients": {"Wheat": 35, "Egg": 30}},
    "Lemon Cheesecake":      {"experience": 30000,"cooking_seconds": 108000,"building": "Bakery", "ingredients": {"Lemon": 20, "Cheese": 5, "Egg": 40}},

    # --- Deli ---
    "Blueberry Jam":     {"experience": 500,  "cooking_seconds": 43200, "building": "Deli", "ingredients": {"Blueberry": 5}},
    "Fermented Carrots": {"experience": 250,  "cooking_seconds": 86400, "building": "Deli", "ingredients": {"Carrot": 20}},
    "Sauerkraut":        {"experience": 500,  "cooking_seconds": 86400, "building": "Deli", "ingredients": {"Cabbage": 20}},
    "Fancy Fries":       {"experience": 1000, "cooking_seconds": 86400, "building": "Deli", "ingredients": {"Sunflower": 500, "Potato": 500}},
    "Fermented Fish":    {"experience": 3000, "cooking_seconds": 86400, "building": "Deli", "ingredients": {"Tuna": 6}},
    "Cheese":            {"experience": 1,    "cooking_seconds": 1200,  "building": "Deli", "ingredients": {"Milk": 3}},
    "Blue Cheese":       {"experience": 6000, "cooking_seconds": 10800, "building": "Deli", "ingredients": {"Cheese": 2, "Blueberry": 10}},
    "Honey Cheddar":     {"experience": 15000,"cooking_seconds": 43200, "building": "Deli", "ingredients": {"Cheese": 3, "Honey": 5}},

    # --- Smoothie Shack ---
    "Purple Smoothie": {"experience": 310,  "cooking_seconds": 1800, "building": "Smoothie Shack", "ingredients": {"Blueberry": 5, "Cabbage": 10}},
    "Orange Juice":    {"experience": 375,  "cooking_seconds": 2700, "building": "Smoothie Shack", "ingredients": {"Orange": 5}},
    "Apple Juice":     {"experience": 500,  "cooking_seconds": 3600, "building": "Smoothie Shack", "ingredients": {"Apple": 5}},
    "Power Smoothie":  {"experience": 775,  "cooking_seconds": 5400, "building": "Smoothie Shack", "ingredients": {"Blueberry": 10, "Kale": 5}},
    "Bumpkin Detox":   {"experience": 975,  "cooking_seconds": 7200, "building": "Smoothie Shack", "ingredients": {"Apple": 5, "Orange": 5, "Carrot": 10}},
    "Banana Blast":    {"experience": 1200, "cooking_seconds": 10800,"building": "Smoothie Shack", "ingredients": {"Banana": 10, "Egg": 10}},
    "Grape Juice":     {"experience": 3300, "cooking_seconds": 10800,"building": "Smoothie Shack", "ingredients": {"Grape": 5, "Radish": 20}},
    "Carrot Juice":    {"experience": 200,  "cooking_seconds": 3600, "building": "Smoothie Shack", "ingredients": {"Carrot": 30}},
    "Sour Shake":      {"experience": 1000, "cooking_seconds": 3600, "building": "Smoothie Shack", "ingredients": {"Lemon": 20}},
}