# ==============================================================================
#  SKILLS & BADGES DATA
#  Source of truth based on the game's internal data files.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. BUMPKIN_REVAMP_SKILLS: The most current and active skill system.
#    This dictionary includes standardized keys for automated processing of buffs
#    and debuffs, essential for calculating final farm productivity.
#
#    Crop Tiers classification based on config.py bumpkin_level:
#    - Basic: Levels 1-2
#    - Medium: Levels 3-4
#    - Advanced: Level 5+
# ------------------------------------------------------------------------------
BUMPKIN_REVAMP_SKILLS = {
    # --- Crops ---
    "Green Thumb": {
        "tree": "Crops",
        "tier": 1,
        "island": "basic",
        "description": "-5% plot crop growth time",
        "effects": [
            {
                "type": "CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.95,
            },
        ],
    },
    "Young Farmer": {
        "tree": "Crops",
        "tier": 1,
        "island": "basic",
        "description": "+0.1 Basic Crop yield",
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop_tier": "basic"},
            },
        ],
    },
    "Experienced Farmer": {
        "tree": "Crops",
        "tier": 1,
        "island": "basic",
        "description": "+0.1 Medium Crop yield",
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop_tier": "medium"},
            },
        ],
    },
    "Old Farmer": {
        "tree": "Crops",
        "tier": 1,
        "island": "basic",
        "description": "+0.1 Advanced Crop yield",
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop_tier": "advanced"},
            },
        ],
    },
    "Betty's Friend": {
        "tree": "Crops",
        "tier": 1,
        "island": "basic",
        "description": "Betty Coin delivery revenue increased by 30%",
        "effects": [
            {
                "type": "DELIVERY_REWARD",
                "operation": "multiply",
                "value": 1.30,
                "conditions": {"npc": "betty"},
            },
        ],
    },
    "Strong Roots": {
        "tree": "Crops",
        "tier": 2,
        "island": "basic",
        "description": "-10% Advanced crop growth time",
        "effects": [
            {
                "type": "CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"crop_tier": "advanced"},
            },
        ],
    },
    "Coin Swindler": {
        "tree": "Crops",
        "tier": 2,
        "island": "basic",
        "description": "+10% coins when selling plot crops at the Market",
        "effects": [
            {
                "type": "SELL_PRICE",
                "operation": "multiply",
                "value": 1.10,
                "conditions": {"category": "Crop", "building": "Market"},
            },
        ],
    },
    "Golden Sunflower": {
        "tree": "Crops",
        "tier": 2,
        "island": "basic",
        "description": "1/700 chance for 0.35 gold when harvesting sunflowers (excluding Crop Machine)",
        "effects": [
            {
                "type": "SPECIAL_RESOURCE_CHANCE",
                "operation": "set_chance",
                "value": 1 / 700,
                "yield_item": "Gold",
                "yield_amount": 0.35,
                "conditions": {"item": "Sunflower"},
            },
        ],
    },
    "Chonky Scarecrow": {
        "tree": "Crops",
        "tier": 1,
        "island": "basic",
        "description": "Increases Basic Scarecrow's area of effect (AOE) to a 7x7 area; Additional -10% basic crop growth time",
        "effects": [
            {
                "type": "SCARECROW_AOE",
                "operation": "set",
                "value": "7x7",
                "conditions": {"item": "Basic Scarecrow"},
            },
            {
                "type": "CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"crop_tier": "basic"},
            },
        ],
    },
    "Horror Mike": {
        "tree": "Crops",
        "tier": 2,
        "island": "basic",
        "description": "Increases Scary Mike's area of effect (AOE) to a 7x7 area; Additional +0.1 medium crop yield",
        "effects": [
            {
                "type": "SCARECROW_AOE",
                "operation": "set",
                "value": "7x7",
                "conditions": {"item": "Scary Mike"},
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop_tier": "medium"},
            },
        ],
    },
    "Laurie's Gains": {
        "tree": "Crops",
        "tier": 2,
        "island": "basic",
        "description": "Increases Laurie the Chuckle Crow's area of effect (AOE) to a 7x7 area; Additional +0.1 advanced crop yield",
        "effects": [
            {
                "type": "SCARECROW_AOE",
                "operation": "set",
                "value": "7x7",
                "conditions": {"item": "Laurie the Chuckle Crow"},
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"crop_tier": "advanced"},
            },
        ],
    },
    "Instant Growth": {
        "tree": "Crops",
        "tier": 3,
        "island": "basic",
        "is_power_skill": True,
        "description": "Grants the ability to instantly harvest all currently growing crops in plots",
        "effects": [
            {
                "type": "INSTANT_GROWTH",
                "target": "AllCrops",
                "cooldown_hours": 72,
            },
        ],
    },
    "Acre Farm": {
        "tree": "Crops",
        "tier": 3,
        "island": "basic",
        "description": "+1 Advanced crop yield; -0.5 Basic and Medium crop yield",
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"crop_tier": "advanced"},
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": -0.5,
                "conditions": {"crop_tier": ["basic", "medium"]},
            },
        ],
    },
    "Hectare Farm": {
        "tree": "Crops",
        "tier": 3,
        "island": "basic",
        "description": "+1 Basic and Medium crop yield; -0.5 Advanced crop yield",
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"crop_tier": ["basic", "medium"]},
            },
            {
                "type": "CROP_YIELD",
                "operation": "add",
                "value": -0.5,
                "conditions": {"crop_tier": "advanced"},
            },
        ],
    },

    # --- Fruit Patch ---
    "Fruitful Fumble": {
        "tree": "Fruit Patch",
        "tier": 1,
        "island": "spring",
        "description": "+0.1 fruit yield",
        "effects": [
            {
                "type": "FRUIT_YIELD",
                "operation": "add",
                "value": 0.1,
            },
        ],
    },
    "Fruity Heaven": {
        "tree": "Fruit Patch",
        "tier": 1,
        "island": "spring",
        "description": "-10% fruit seeds cost",
        "effects": [
            {
                "type": "SEED_COST",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"category": "FruitSeed"},
            },
        ],
    },
    "Fruity Profit": {
        "tree": "Fruit Patch",
        "tier": 1,
        "island": "spring",
        "description": "+50% coins from Tango's deliveries",
        "effects": [
            {
                "type": "DELIVERY_REWARD",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"npc": "tango"},
            },
        ],
    },
    "Loyal Macaw": {
        "tree": "Fruit Patch",
        "tier": 1,
        "island": "spring",
        "description": "Double Macaw's effect",
        "effects": [
            {
                "type": "COLLECTIBLE_EFFECT_MULTIPLIER",
                "operation": "multiply",
                "value": 2,
                "conditions": {"item": "Macaw"},
            },
        ],
    },
    "Catchup": {
        "tree": "Fruit Patch",
        "tier": 2,
        "island": "spring",
        "description": "-10% fruit growth time",
        "effects": [
            {
                "type": "FRUIT_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "No Axe No Worries": {
        "tree": "Fruit Patch",
        "tier": 1,
        "island": "spring",
        "description": "Chop fruit branches and stems without axes; -1 wood from fruit branches and stems",
        "effects": [
            {
                "type": "AXELESS_FRUIT_CHOpping",
                "operation": "set",
                "value": True,
            },
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": -1,
                "conditions": {"item": "Wood", "source": "FruitTree"},
            },
        ],
    },
    "Fruity Woody": {
        "tree": "Fruit Patch",
        "tier": 2,
        "island": "spring",
        "description": "+1 wood from fruit branches and stems",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"item": "Wood", "source": "FruitTree"},
            },
        ],
    },
    "Pear Turbocharge": {
        "tree": "Fruit Patch",
        "tier": 2,
        "island": "spring",
        "description": "Double Immortal Pear's effect",
        "effects": [
            {
                "type": "COLLECTIBLE_EFFECT_MULTIPLIER",
                "operation": "multiply",
                "value": 2,
                "conditions": {"item": "Immortal Pear"},
            },
        ],
    },
    "Crime Fruit": {
        "tree": "Fruit Patch",
        "tier": 2,
        "island": "spring",
        "description": "+10 Tomato and Lemon seeds stock",
        "effects": [
            {
                "type": "SHOP_STOCK",
                "operation": "add",
                "value": 10,
                "conditions": {"items": ["Tomato Seed", "Lemon Seed"]},
            },
        ],
    },
    "Generous Orchard": {
        "tree": "Fruit Patch",
        "tier": 3,
        "island": "spring",
        "description": "20% chance of +1 fruit yield",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.20,
                "bonus_amount": 1,
                "conditions": {"category": "Fruit"},
            },
        ],
    },
    "Long Pickings": {
        "tree": "Fruit Patch",
        "tier": 3,
        "island": "spring",
        "description": "-50% Apple and Banana growth time; +100% growth time for all other fruits",
        "effects": [
            {
                "type": "FRUIT_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.50,
                "conditions": {"items": ["Apple", "Banana"]},
            },
            {
                "type": "FRUIT_GROWTH_TIME",
                "operation": "multiply",
                "value": 2.0,
                "conditions": {"exclude_items": ["Apple", "Banana"]},
            },
        ],
    },
    "Short Pickings": {
        "tree": "Fruit Patch",
        "tier": 3,
        "island": "spring",
        "description": "-50% Blueberry and Orange growth time; +100% growth time for all other fruits",
        "effects": [
            {
                "type": "FRUIT_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.50,
                "conditions": {"items": ["Blueberry", "Orange"]},
            },
            {
                "type": "FRUIT_GROWTH_TIME",
                "operation": "multiply",
                "value": 2.0,
                "conditions": {"exclude_items": ["Blueberry", "Orange"]},
            },
        ],
    },
    "Zesty Vibes": {
        "tree": "Fruit Patch",
        "tier": 3,
        "island": "spring",
        "description": "+1 Tomato and Lemon yield; -0.25 yield for all other fruits",
        "effects": [
            {
                "type": "FRUIT_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"items": ["Tomato", "Lemon"]},
            },
            {
                "type": "FRUIT_YIELD",
                "operation": "add",
                "value": -0.25,
                "conditions": {"exclude_items": ["Tomato", "Lemon"]},
            },
        ],
    },

    # --- Trees ---
    "Lumberjack's Extra": {
        "tree": "Trees",
        "tier": 1,
        "island": "basic",
        "description": "+0.1 wood yield",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"item": "Wood"},
            },
        ],
    },
    "Tree Charge": {
        "tree": "Trees",
        "tier": 1,
        "island": "basic",
        "description": "-10% tree growth time",
        "effects": [
            {
                "type": "TREE_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "More Axes": {
        "tree": "Trees",
        "tier": 1,
        "island": "basic",
        "description": "+50 axe stock",
        "effects": [
            {
                "type": "SHOP_STOCK",
                "operation": "add",
                "value": 50,
                "conditions": {"item": "Axe"},
            },
        ],
    },
    "Insta-Chop": {
        "tree": "Trees",
        "tier": 1,
        "island": "basic",
        "description": "1 Tap Trees",
        "effects": [
            {
                "type": "INSTANT_CHOP",
                "operation": "set",
                "value": True,
            },
        ],
    },
    "Tough Tree": {
        "tree": "Trees",
        "tier": 2,
        "island": "basic",
        "description": "1/10 chance of x3 wood yield",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.10,
                "bonus_multiplier": 3,
                "conditions": {"item": "Wood"},
            },
        ],
    },
    "Feller's Discount": {
        "tree": "Trees",
        "tier": 2,
        "island": "basic",
        "description": "-20% axe cost",
        "effects": [
            {
                "type": "CRAFTING_COST",
                "operation": "multiply",
                "value": 0.80,
                "conditions": {"item": "Axe"},
            },
        ],
    },
    "Money Tree": {
        "tree": "Trees",
        "tier": 2,
        "island": "basic",
        "description": "1% chance of finding 200 Coins when chopping trees",
        "effects": [
            {
                "type": "COIN_DROP_CHANCE",
                "operation": "set_chance",
                "value": 0.01,
                "coin_amount": 200,
                "conditions": {"action": "ChopTree"},
            },
        ],
    },
    "Tree Turnaround": {
        "tree": "Trees",
        "tier": 3,
        "island": "basic",
        "description": "15% chance for trees to grow instantly",
        "effects": [
            {
                "type": "INSTANT_GROWTH_CHANCE",
                "operation": "set_chance",
                "value": 0.15,
                "conditions": {"category": "Tree"},
            },
        ],
    },
    "Tree Blitz": {
        "tree": "Trees",
        "tier": 3,
        "island": "basic",
        "is_power_skill": True,
        "description": "Ability to make all trees instantly grow",
        "effects": [
            {
                "type": "INSTANT_GROWTH",
                "target": "AllTrees",
                "cooldown_hours": 24,
            },
        ],
    },

    # --- Fishing ---
    "Fisherman's FiveFold": {
        "tree": "Fishing",
        "tier": 1,
        "island": "basic",
        "description": "+5 daily fishing limit",
        "effects": [
            {
                "type": "FISHING_LIMIT",
                "operation": "add",
                "value": 5,
            },
        ],
    },
    "Fishy Chance": {
        "tree": "Fishing",
        "tier": 1,
        "island": "basic",
        "description": "10% chance of +1 basic fish",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.10,
                "bonus_amount": 1,
                "conditions": {"fish_tier": "basic"},
            },
        ],
    },
    "Fishy Roll": {
        "tree": "Fishing",
        "tier": 1,
        "island": "basic",
        "description": "10% chance of +1 advanced fish",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.10,
                "bonus_amount": 1,
                "conditions": {"fish_tier": "advanced"},
            },
        ],
    },
    "Reel Deal": {
        "tree": "Fishing",
        "tier": 1,
        "island": "basic",
        "description": "-50% rod coin cost",
        "effects": [
            {
                "type": "CRAFTING_COST",
                "operation": "multiply",
                "value": 0.50,
                "conditions": {"item": "Rod", "currency": "SFL"},
            },
        ],
    },
    "Fisherman's TenFold": {
        "tree": "Fishing",
        "tier": 2,
        "island": "basic",
        "description": "+10 daily fishing limit",
        "effects": [
            {
                "type": "FISHING_LIMIT",
                "operation": "add",
                "value": 10,
            },
        ],
    },
    "Fishy Fortune": {
        "tree": "Fishing",
        "tier": 2,
        "island": "basic",
        "description": "+100% coins from Corale's deliveries",
        "effects": [
            {
                "type": "DELIVERY_REWARD",
                "operation": "multiply",
                "value": 2.0,
                "conditions": {"npc": "corale"},
            },
        ],
    },
    "Big Catch": {
        "tree": "Fishing",
        "tier": 2,
        "island": "basic",
        "description": "Increase bar for catching game",
        "effects": [
            {
                "type": "FISHING_MINIGAME_BAR_SIZE",
                "operation": "multiply",
                "value": 1.20, # Assuming a 20% increase
            },
        ],
    },
    "Fishy Gamble": {
        "tree": "Fishing",
        "tier": 2,
        "island": "basic",
        "description": "20% chance of +1 expert fish",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.20,
                "bonus_amount": 1,
                "conditions": {"fish_tier": "expert"},
            },
        ],
    },
    "Frenzied Fish": {
        "tree": "Fishing",
        "tier": 3,
        "island": "basic",
        "description": "During fish frenzy, +1 fish and 50% chance of +1 fish",
        "effects": [
            {
                "type": "FRENZY_YIELD",
                "operation": "add",
                "value": 1,
            },
            {
                "type": "FRENZY_BONUS_CHANCE",
                "operation": "set_chance",
                "value": 0.50,
                "bonus_amount": 1,
            },
        ],
    },
    "More With Less": {
        "tree": "Fishing",
        "tier": 3,
        "island": "basic",
        "description": "+15 daily fishing limit; -1 worm from all composters",
        "effects": [
            {
                "type": "FISHING_LIMIT",
                "operation": "add",
                "value": 15,
            },
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": -1,
                "conditions": {"item": "Worm"},
            },
        ],
    },
    "Fishy Feast": {
        "tree": "Fishing",
        "tier": 3,
        "island": "basic",
        "description": "+20% Fish XP",
        "effects": [
            {
                "type": "FISHING_XP",
                "operation": "multiply",
                "value": 1.20,
            },
        ],
    },

    # --- Animals ---
    "Abundant Harvest": {
        "tree": "Animals",
        "tier": 2,
        "island": "spring",
        "description": "+0.2 Egg, Wool and Milk yield",
        "effects": [
            {
                "type": "ANIMAL_PRODUCE_YIELD",
                "operation": "add",
                "value": 0.2,
                "conditions": {"items": ["Egg", "Wool", "Milk"]},
            },
        ],
    },
    "Efficient Feeding": {
        "tree": "Animals",
        "tier": 1,
        "island": "spring",
        "description": "-5% feed to feed all animals",
        "effects": [
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 0.95,
            },
        ],
    },
    "Restless Animals": {
        "tree": "Animals",
        "tier": 1,
        "island": "spring",
        "description": "-10% Animal sleep time",
        "effects": [
            {
                "type": "ANIMAL_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "Double Bale": {
        "tree": "Animals",
        "tier": 1,
        "island": "spring",
        "description": "Double Bale's Effect",
        "effects": [
            {
                "type": "COLLECTIBLE_EFFECT_MULTIPLIER",
                "operation": "multiply",
                "value": 2,
                "conditions": {"item": "Bale"},
            },
        ],
    },
    "Bale Economy": {
        "tree": "Animals",
        "tier": 1,
        "island": "spring",
        "description": "Bale affects milk and wool production",
        "effects": [
            {
                "type": "BALE_AFFECTS_ITEMS",
                "operation": "add_items",
                "value": ["Milk", "Wool"],
            },
        ],
    },
    "Fine Fibers": {
        "tree": "Animals",
        "tier": 1,
        "island": "spring",
        "description": "+0.1 Feather, Leather and Merino Wool yield",
        "effects": [
            {
                "type": "ANIMAL_PRODUCE_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"items": ["Feather", "Leather", "Merino Wool"]},
            },
        ],
    },
    "Bountiful Bounties": {
        "tree": "Animals",
        "tier": 1,
        "island": "spring",
        "description": "+50% Coins from Animal Bounties",
        "effects": [
            {
                "type": "DELIVERY_REWARD",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"delivery_type": "AnimalBounty"},
            },
        ],
    },
    "Heartwarming Instruments": {
        "tree": "Animals",
        "tier": 2,
        "island": "spring",
        "description": "+50% Animal XP from Animal Affection tools",
        "effects": [
            {
                "type": "ANIMAL_XP",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"source": "AffectionTool"},
            },
        ],
    },
    "Kale Mix": {
        "tree": "Animals",
        "tier": 2,
        "island": "spring",
        "description": "Mixed Grain requires 3 kale to mix instead",
        "effects": [
            {
                "type": "CRAFTING_RECIPE_CHANGE",
                "item": "Mixed Grain",
                "new_recipe": {"Kale": 3},
            },
        ],
    },
    "Alternate Medicine": {
        "tree": "Animals",
        "tier": 2,
        "island": "spring",
        "description": "Barn Delight requires 1 less Lemon and Honey to mix",
        "effects": [
            {
                "type": "CRAFTING_COST_REDUCTION",
                "item": "Barn Delight",
                "ingredient_reductions": {"Lemon": 1, "Honey": 1},
            },
        ],
    },
    "Healthy Livestock": {
        "tree": "Animals",
        "tier": 2,
        "island": "spring",
        "description": "-50% chance of sickness",
        "effects": [
            {
                "type": "ANIMAL_SICKNESS_CHANCE",
                "operation": "multiply",
                "value": 0.50,
            },
        ],
    },
    "Clucky Grazing": {
        "tree": "Animals",
        "tier": 3,
        "island": "spring",
        "description": "-25% feed to feed Chickens; +50% feed to feed other animals",
        "effects": [
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 0.75,
                "conditions": {"animal": "Chicken"},
            },
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"exclude_animal": "Chicken"},
            },
        ],
    },
    "Sheepwise Diet": {
        "tree": "Animals",
        "tier": 3,
        "island": "spring",
        "description": "-25% feed to feed Sheep; +50% feed to feed other animals",
        "effects": [
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 0.75,
                "conditions": {"animal": "Sheep"},
            },
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"exclude_animal": "Sheep"},
            },
        ],
    },
    "Cow-Smart Nutrition": {
        "tree": "Animals",
        "tier": 3,
        "island": "spring",
        "description": "-25% feed to feed Cows; +50% feed to feed other animals",
        "effects": [
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 0.75,
                "conditions": {"animal": "Cow"},
            },
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"exclude_animal": "Cow"},
            },
        ],
    },
    "Chonky Feed": {
        "tree": "Animals",
        "tier": 3,
        "island": "spring",
        "description": "2x animal xp from animal feed; +50% feed to feed all animals",
        "effects": [
            {
                "type": "ANIMAL_XP",
                "operation": "multiply",
                "value": 2.0,
                "conditions": {"source": "AnimalFeed"},
            },
            {
                "type": "ANIMAL_FEED_COST",
                "operation": "multiply",
                "value": 1.50,
            },
        ],
    },
    "Barnyard Rouse": {
        "tree": "Animals",
        "tier": 3,
        "island": "spring",
        "is_power_skill": True,
        "description": "Instantly wakes up all animals",
        "effects": [
            {
                "type": "INSTANT_WAKE_UP",
                "target": "AllAnimals",
                "cooldown_hours": 120,
            },
        ],
    },
    # --- Greenhouse ---
    "Victoria's Secretary": {
        "tree": "Greenhouse",
        "tier": 1,
        "island": "desert",
        "description": "+50% Coins from Victoria's deliveries",
        "effects": [
            {
                "type": "DELIVERY_REWARD",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"npc": "victoria"},
            },
        ],
    },
    "Glass Room": {
        "tree": "Greenhouse",
        "tier": 1,
        "island": "desert",
        "description": "+0.1 Greenhouse produce yield",
        "effects": [
            {
                "type": "GREENHOUSE_YIELD",
                "operation": "add",
                "value": 0.1,
            },
        ],
    },
    "Seedy Business": {
        "tree": "Greenhouse",
        "tier": 1,
        "island": "desert",
        "description": "-15% Greenhouse seeds cost",
        "effects": [
            {
                "type": "SEED_COST",
                "operation": "multiply",
                "value": 0.85,
                "conditions": {"category": "GreenhouseSeed"},
            },
        ],
    },
    "Rice and Shine": {
        "tree": "Greenhouse",
        "tier": 1,
        "island": "desert",
        "description": "-5% growth time for greenhouse produce",
        "effects": [
            {
                "type": "GREENHOUSE_CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.95,
            },
        ],
    },
    "Olive Express": {
        "tree": "Greenhouse",
        "tier": 2,
        "island": "desert",
        "description": "-10% Olive growth time",
        "effects": [
            {
                "type": "GREENHOUSE_CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"item": "Olive"},
            },
        ],
    },
    "Rice Rocket": {
        "tree": "Greenhouse",
        "tier": 2,
        "island": "desert",
        "description": "-10% Rice growth time",
        "effects": [
            {
                "type": "GREENHOUSE_CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"item": "Rice"},
            },
        ],
    },
    "Vine Velocity": {
        "tree": "Greenhouse",
        "tier": 2,
        "island": "desert",
        "description": "-10% Grape growth time",
        "effects": [
            {
                "type": "GREENHOUSE_CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"item": "Grape"},
            },
        ],
    },
    "Seeded Bounty": {
        "tree": "Greenhouse",
        "tier": 2,
        "island": "desert",
        "description": "+0.5 Greenhouse produce yield; +1 Greenhouse seed to plant",
        "effects": [
            {
                "type": "GREENHOUSE_YIELD",
                "operation": "add",
                "value": 0.5,
            },
            {
                "type": "SEED_COST",
                "operation": "add",
                "value": 1,
                "conditions": {"category": "GreenhouseSeed"},
            },
        ],
    },
    "Greasy Plants": {
        "tree": "Greenhouse",
        "tier": 3,
        "island": "desert",
        "description": "+1 Greenhouse produce yield; +100% Oil consumption in greenhouse",
        "effects": [
            {
                "type": "GREENHOUSE_YIELD",
                "operation": "add",
                "value": 1,
            },
            {
                "type": "GREENHOUSE_OIL_COST",
                "operation": "multiply",
                "value": 2.0,
            },
        ],
    },
    "Greenhouse Guru": {
        "tree": "Greenhouse",
        "tier": 3,
        "island": "desert",
        "is_power_skill": True,
        "description": "Ability to make all greenhouse produce currently growing ready to be harvested",
        "effects": [
            {
                "type": "INSTANT_GROWTH",
                "target": "AllGreenhouse",
                "cooldown_hours": 96,
            },
        ],
    },
    "Greenhouse Gamble": {
        "tree": "Greenhouse",
        "tier": 3,
        "island": "desert",
        "description": "25% chance of +1 greenhouse produce",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.25,
                "bonus_amount": 1,
                "conditions": {"category": "GreenhouseProduce"},
            },
        ],
    },
    "Slick Saver": {
        "tree": "Greenhouse",
        "tier": 3,
        "island": "desert",
        "description": "-1 Oil to grow greenhouse produce",
        "effects": [
            {
                "type": "GREENHOUSE_OIL_COST",
                "operation": "add",
                "value": -1,
            },
        ],
    },

    # --- Mining ---
    "Rock'N'Roll": {
        "tree": "Mining",
        "tier": 1,
        "island": "basic",
        "description": "+0.1 Stone Yield",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"item": "Stone"},
            },
        ],
    },
    "Iron Bumpkin": {
        "tree": "Mining",
        "tier": 1,
        "island": "basic",
        "description": "+0.1 Iron Yield",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"item": "Iron"},
            },
        ],
    },
    "Speed Miner": {
        "tree": "Mining",
        "tier": 1,
        "island": "basic",
        "description": "-20% Stone recovery time",
        "effects": [
            {
                "type": "ROCK_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.80,
                "conditions": {"item": "Stone Rock"},
            },
        ],
    },
    "Tap Prospector": {
        "tree": "Mining",
        "tier": 1,
        "island": "basic",
        "description": "1 tap small mineral nodes",
        "effects": [
            {
                "type": "INSTANT_MINE",
                "operation": "set",
                "value": True,
                "conditions": {"rock_size": "small"},
            },
        ],
    },
    "Forge-Ward Profits": {
        "tree": "Mining",
        "tier": 1,
        "island": "basic",
        "description": "+20% Blacksmith deliveries revenue",
        "effects": [
            {
                "type": "DELIVERY_REWARD",
                "operation": "multiply",
                "value": 1.20,
                "conditions": {"npc": "blacksmith"},
            },
        ],
    },
    "Iron Hustle": {
        "tree": "Mining",
        "tier": 2,
        "island": "basic",
        "description": "-30% Iron recovery time",
        "effects": [
            {
                "type": "ROCK_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.70,
                "conditions": {"item": "Iron Rock"},
            },
        ],
    },
    "Frugal Miner": {
        "tree": "Mining",
        "tier": 2,
        "island": "basic",
        "description": "-20% coin cost for all pickaxes",
        "effects": [
            {
                "type": "CRAFTING_COST",
                "operation": "multiply",
                "value": 0.80,
                "conditions": {"category": "Pickaxe", "currency": "SFL"},
            },
        ],
    },
    "Rocky Favor": {
        "tree": "Mining",
        "tier": 2,
        "island": "basic",
        "description": "+1 Stone yield; -0.5 Iron yield",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"item": "Stone"},
            },
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": -0.5,
                "conditions": {"item": "Iron"},
            },
        ],
    },
    "Ferrous Favor": {
        "tree": "Mining",
        "tier": 3,
        "island": "basic",
        "description": "+1 Iron yield; -0.5 Stone yield",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"item": "Iron"},
            },
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": -0.5,
                "conditions": {"item": "Stone"},
            },
        ],
    },
    "Midas Sprint": {
        "tree": "Mining",
        "tier": 2,
        "island": "basic",
        "description": "-10% Gold recovery time",
        "effects": [
            {
                "type": "ROCK_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"item": "Gold Rock"},
            },
        ],
    },
    "Midas Rush": {
        "tree": "Mining",
        "tier": 3,
        "island": "basic",
        "description": "-20% Gold recovery time",
        "effects": [
            {
                "type": "ROCK_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.80,
                "conditions": {"item": "Gold Rock"},
            },
        ],
    },
    "Golden Touch": {
        "tree": "Mining",
        "tier": 3,
        "island": "basic",
        "description": "+0.5 Gold Yield",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 0.5,
                "conditions": {"item": "Gold"},
            },
        ],
    },
    "More Picks": {
        "tree": "Mining",
        "tier": 3,
        "island": "basic",
        "description": "Increased stock: +70 Pickaxe, +20 Stone Pickaxe, +7 Iron Pickaxe, +2 Gold Pickaxe",
        "effects": [
            {"type": "SHOP_STOCK", "operation": "add", "value": 70, "conditions": {"item": "Pickaxe"}},
            {"type": "SHOP_STOCK", "operation": "add", "value": 20, "conditions": {"item": "Stone Pickaxe"}},
            {"type": "SHOP_STOCK", "operation": "add", "value": 7, "conditions": {"item": "Iron Pickaxe"}},
            {"type": "SHOP_STOCK", "operation": "add", "value": 2, "conditions": {"item": "Gold Pickaxe"}},
        ],
    },
    "Fire Kissed": {
        "tree": "Mining",
        "tier": 2,
        "island": "basic",
        "description": "+1 Crimstone yield on 5th consecutive mine",
        "effects": [
            {
                "type": "CONSECUTIVE_MINING_BONUS",
                "operation": "set",
                "value": { "consecutive_count": 5, "item": "Crimstone", "bonus_yield": 1 },
            },
        ],
    },
    "Fireside Alchemist": {
        "tree": "Mining",
        "tier": 3,
        "island": "basic",
        "description": "-15% Crimstone recovery time",
        "effects": [
            {
                "type": "ROCK_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.85,
                "conditions": {"item": "Crimstone Rock"},
            },
        ],
    },

    # --- Cooking ---
    "Fast Feasts": {
        "tree": "Cooking",
        "tier": 1,
        "island": "basic",
        "description": "-10% Firepit and Kitchen cooking time",
        "effects": [
            {
                "type": "COOKING_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"buildings": ["Fire Pit", "Kitchen"]},
            },
        ],
    },
    "Nom Nom": {
        "tree": "Cooking",
        "tier": 1,
        "island": "basic",
        "description": "+10% Food deliveries revenue",
        "effects": [
            {
                "type": "DELIVERY_REWARD",
                "operation": "multiply",
                "value": 1.10,
                "conditions": {"category": "Food"},
            },
        ],
    },
    "Munching Mastery": {
        "tree": "Cooking",
        "tier": 1,
        "island": "basic",
        "description": "+5% Experience from eating meals",
        "effects": [
            {
                "type": "CONSUME_XP",
                "operation": "multiply",
                "value": 1.05,
            },
        ],
    },
    "Swift Sizzle": {
        "tree": "Cooking",
        "tier": 1,
        "island": "basic",
        "description": "-40% Fire Pit cooking time with oil",
        "effects": [
            {
                "type": "COOKING_TIME",
                "operation": "multiply",
                "value": 0.60,
                "conditions": {"building": "Fire Pit", "ingredient": "Oil"},
            },
        ],
    },
    "Frosted Cakes": {
        "tree": "Cooking",
        "tier": 2,
        "island": "basic",
        "description": "-10% Cakes cooking time",
        "effects": [
            {
                "type": "COOKING_TIME",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"category": "Cake"},
            },
        ],
    },
    "Juicy Boost": {
        "tree": "Cooking",
        "tier": 2,
        "island": "basic",
        "description": "+10% experience for drinks from the Smoothie Shack",
        "effects": [
            {
                "type": "CONSUME_XP",
                "operation": "multiply",
                "value": 1.10,
                "conditions": {"building": "Smoothie Shack"},
            },
        ],
    },
    "Double Nom": {
        "tree": "Cooking",
        "tier": 3,
        "island": "basic",
        "description": "+1 food from cooking; 2x ingredients required for cooking",
        "effects": [
            {
                "type": "CRAFTING_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"category": "Food"},
            },
            {
                "type": "CRAFTING_COST",
                "operation": "multiply",
                "value": 2.0,
                "conditions": {"category": "Food"},
            },
        ],
    },
    "Turbo Fry": {
        "tree": "Cooking",
        "tier": 2,
        "island": "basic",
        "description": "-50% Kitchen cooking time with oil",
        "effects": [
            {
                "type": "COOKING_TIME",
                "operation": "multiply",
                "value": 0.50,
                "conditions": {"building": "Kitchen", "ingredient": "Oil"},
            },
        ],
    },
    "Instant Gratification": {
        "tree": "Cooking",
        "tier": 3,
        "island": "basic",
        "is_power_skill": True,
        "description": "Ability to make all meals currently cooking ready to be eaten",
        "effects": [
            {
                "type": "INSTANT_COOK",
                "target": "AllMeals",
                "cooldown_hours": 96,
            },
        ],
    },
    "Drive-Through Deli": {
        "tree": "Cooking",
        "tier": 2,
        "island": "basic",
        "description": "+15% experience for meals from the Deli",
        "effects": [
            {
                "type": "CONSUME_XP",
                "operation": "multiply",
                "value": 1.15,
                "conditions": {"building": "Deli"},
            },
        ],
    },
    "Fiery Jackpot": {
        "tree": "Cooking",
        "tier": 3,
        "island": "basic",
        "description": "+20% Chance of +1 food from Firepit",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.20,
                "bonus_amount": 1,
                "conditions": {"building": "Fire Pit"},
            },
        ],
    },
    "Fry Frenzy": {
        "tree": "Cooking",
        "tier": 3,
        "island": "basic",
        "description": "-60% Deli cooking time with oil",
        "effects": [
            {
                "type": "COOKING_TIME",
                "operation": "multiply",
                "value": 0.40,
                "conditions": {"building": "Deli", "ingredient": "Oil"},
            },
        ],
    },

    # --- Bees & Flowers ---
    "Sweet Bonus": {
        "tree": "Bees & Flowers",
        "tier": 1,
        "island": "spring",
        "description": "+0.1 Honey per hive",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 0.1,
                "conditions": {"item": "Honey"},
            },
        ],
    },
    "Hyper Bees": {
        "tree": "Bees & Flowers",
        "tier": 1,
        "island": "spring",
        "description": "+0.1 Honey production speed",
        "effects": [
            {
                "type": "BEEHIVE_PRODUCTION_SPEED",
                "operation": "multiply",
                "value": 1.10,
            },
        ],
    },
    "Blooming Boost": {
        "tree": "Bees & Flowers",
        "tier": 1,
        "island": "spring",
        "description": "-10% Flower growth time",
        "effects": [
            {
                "type": "FLOWER_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "Flower Sale": {
        "tree": "Bees & Flowers",
        "tier": 1,
        "island": "spring",
        "description": "-20% Flower Seeds cost",
        "effects": [
            {
                "type": "SEED_COST",
                "operation": "multiply",
                "value": 0.80,
                "conditions": {"category": "FlowerSeed"},
            },
        ],
    },
    "Buzzworthy Treats": {
        "tree": "Bees & Flowers",
        "tier": 2,
        "island": "spring",
        "description": "+10% Experience on food made with Honey",
        "effects": [
            {
                "type": "CONSUME_XP",
                "operation": "multiply",
                "value": 1.10,
                "conditions": {"ingredient": "Honey"},
            },
        ],
    },
    "Blossom Bonding": {
        "tree": "Bees & Flowers",
        "tier": 2,
        "island": "spring",
        "description": "+2 relationship points for gifting flowers",
        "effects": [
            {
                "type": "GIFTING_RELATIONSHIP_POINTS",
                "operation": "add",
                "value": 2,
                "conditions": {"category": "Flower"},
            },
        ],
    },
    "Pollen Power Up": {
        "tree": "Bees & Flowers",
        "tier": 2,
        "island": "spring",
        "description": "Additional +0.1 crop yield after pollination (total +0.3)",
        "effects": [
            {
                "type": "POLLINATION_YIELD_BOOST",
                "operation": "add",
                "value": 0.1,
            },
        ],
    },
    "Petalled Perk": {
        "tree": "Bees & Flowers",
        "tier": 2,
        "island": "spring",
        "description": "10% chance of +1 Flower",
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.10,
                "bonus_amount": 1,
                "conditions": {"category": "Flower"},
            },
        ],
    },
    "Bee Collective": {
        "tree": "Bees & Flowers",
        "tier": 3,
        "island": "spring",
        "description": "+20% Bee Swarm chance",
        "effects": [
            {
                "type": "BEE_SWARM_CHANCE",
                "operation": "multiply",
                "value": 1.20,
            },
        ],
    },
    "Flower Power": {
        "tree": "Bees & Flowers",
        "tier": 3,
        "island": "spring",
        "description": "-20% Flower growth time",
        "effects": [
            {
                "type": "FLOWER_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.80,
            },
        ],
    },
    "Flowery Abode": {
        "tree": "Bees & Flowers",
        "tier": 3,
        "island": "spring",
        "description": "+0.5 Honey production speed; +50% Flower growth time",
        "effects": [
            {
                "type": "BEEHIVE_PRODUCTION_SPEED",
                "operation": "multiply",
                "value": 1.50,
            },
            {
                "type": "FLOWER_GROWTH_TIME",
                "operation": "multiply",
                "value": 1.50,
            },
        ],
    },
    "Petal Blessed": {
        "tree": "Bees & Flowers",
        "tier": 3,
        "island": "spring",
        "is_power_skill": True,
        "description": "Ability to make all flowers currently growing ready to be harvested",
        "effects": [
            {
                "type": "INSTANT_GROWTH",
                "target": "AllFlowers",
                "cooldown_hours": 96,
            },
        ],
    },

    # --- Machinery ---
    "Crop Processor Unit": {
        "tree": "Machinery",
        "tier": 1,
        "island": "desert",
        "description": "-5% Crop Machine growth time; +10% Oil consumption in Crop Machine",
        "effects": [
            {
                "type": "CROP_MACHINE_TIME",
                "operation": "multiply",
                "value": 0.95,
            },
            {
                "type": "CROP_MACHINE_OIL_COST",
                "operation": "multiply",
                "value": 1.10,
            },
        ],
    },
    "Oil Gadget": {
        "tree": "Machinery",
        "tier": 1,
        "island": "desert",
        "description": "-10% Oil consumption in Crop Machine",
        "effects": [
            {
                "type": "CROP_MACHINE_OIL_COST",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "Oil Extraction": {
        "tree": "Machinery",
        "tier": 1,
        "island": "desert",
        "description": "+1 Oil when collecting from reserves",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"item": "Oil", "source": "Oil Reserve"},
            },
        ],
    },
    "Leak-Proof Tank": {
        "tree": "Machinery",
        "tier": 1,
        "island": "desert",
        "description": "Triple oil tank capacity in crop machine",
        "effects": [
            {
                "type": "OIL_TANK_CAPACITY",
                "operation": "multiply",
                "value": 3,
            },
        ],
    },
    "Crop Extension Module I": {
        "tree": "Machinery",
        "tier": 1,
        "island": "desert",
        "description": "Allow Rhubarb and Zucchini seeds to be used in crop machine",
        "effects": [
            {
                "type": "CROP_MACHINE_ELIGIBILITY",
                "operation": "add_items",
                "value": ["Rhubarb", "Zucchini"],
            },
        ],
    },
    "Crop Extension Module II": {
        "tree": "Machinery",
        "tier": 2,
        "island": "desert",
        "description": "Allow Carrot and Cabbage seeds to be used in crop machine",
        "effects": [
            {
                "type": "CROP_MACHINE_ELIGIBILITY",
                "operation": "add_items",
                "value": ["Carrot", "Cabbage"],
            },
        ],
    },
    "Crop Extension Module III": {
        "tree": "Machinery",
        "tier": 2,
        "island": "desert",
        "description": "Allow Yam and Broccoli seeds to be used in crop machine",
        "effects": [
            {
                "type": "CROP_MACHINE_ELIGIBILITY",
                "operation": "add_items",
                "value": ["Yam", "Broccoli"],
            },
        ],
    },
    "Rapid Rig": {
        "tree": "Machinery",
        "tier": 2,
        "island": "desert",
        "description": "-20% Crop Machine growth time; +40% Oil consumption in Crop Machine",
        "effects": [
            {
                "type": "CROP_MACHINE_TIME",
                "operation": "multiply",
                "value": 0.80,
            },
            {
                "type": "CROP_MACHINE_OIL_COST",
                "operation": "multiply",
                "value": 1.40,
            },
        ],
    },
    "Oil Be Back": {
        "tree": "Machinery",
        "tier": 2,
        "island": "desert",
        "description": "-20% Oil refill time",
        "effects": [
            {
                "type": "ROCK_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.80,
                "conditions": {"item": "Oil Reserve"},
            },
        ],
    },
    "Field Expansion Module": {
        "tree": "Machinery",
        "tier": 3,
        "island": "desert",
        "description": "+5 packs added to machine queue system",
        "effects": [
            {
                "type": "CROP_MACHINE_QUEUE",
                "operation": "add",
                "value": 5,
            },
        ],
    },
    "Field Extension Module": {
        "tree": "Machinery",
        "tier": 3,
        "island": "desert",
        "description": "+5 plots added to machine",
        "effects": [
            {
                "type": "CROP_MACHINE_PLOT_COUNT",
                "operation": "add",
                "value": 5,
            },
        ],
    },
    "Efficiency Extension Module": {
        "tree": "Machinery",
        "tier": 3,
        "island": "desert",
        "description": "-30% Oil consumption in Crop Machine",
        "effects": [
            {
                "type": "CROP_MACHINE_OIL_COST",
                "operation": "multiply",
                "value": 0.70,
            },
        ],
    },
    "Grease Lightning": {
        "tree": "Machinery",
        "tier": 3,
        "island": "desert",
        "is_power_skill": True,
        "description": "Ability to make empty oil wells instantly refill",
        "effects": [
            {
                "type": "INSTANT_REFILL",
                "target": "OilWell",
                "cooldown_hours": 96,
            },
        ],
    },

    # --- Compost ---
    "Efficient Bin": {
        "tree": "Compost",
        "tier": 1,
        "island": "basic",
        "description": "+5 Sprout Mix",
        "effects": [
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": 5,
                "conditions": {"item": "Sprout Mix"},
            },
        ],
    },
    "Turbo Charged": {
        "tree": "Compost",
        "tier": 1,
        "island": "basic",
        "description": "+5 Fruitful Blend",
        "effects": [
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": 5,
                "conditions": {"item": "Fruitful Blend"},
            },
        ],
    },
    "Wormy Treat": {
        "tree": "Compost",
        "tier": 1,
        "island": "basic",
        "description": "+1 Worm",
        "effects": [
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": 1,
                "conditions": {"item": "Worm"},
            },
        ],
    },
    "Feathery Business": {
        "tree": "Compost",
        "tier": 1,
        "island": "basic",
        "description": "Use feathers instead of eggs to boost composters; 2x feathers to boost composters",
        "effects": [
            {
                "type": "COMPOST_BOOST_INGREDIENT",
                "operation": "replace",
                "from": "Egg",
                "to": "Feather",
            },
            {
                "type": "COMPOST_BOOST_COST",
                "operation": "multiply",
                "value": 2.0,
                "conditions": {"ingredient": "Feather"},
            },
        ],
    },
    "Swift Decomposer": {
        "tree": "Compost",
        "tier": 2,
        "island": "basic",
        "description": "-10% compost time",
        "effects": [
            {
                "type": "COMPOST_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "Composting Bonanza": {
        "tree": "Compost",
        "tier": 2,
        "island": "basic",
        "description": "Speed up composters by an additional hour when boosting; 2x resources to boost composters",
        "effects": [
            {
                "type": "COMPOST_BOOST_SPEED_INCREASE",
                "operation": "add_hours",
                "value": 1,
            },
            {
                "type": "COMPOST_BOOST_COST",
                "operation": "multiply",
                "value": 2.0,
            },
        ],
    },
    "Premium Worms": {
        "tree": "Compost",
        "tier": 2,
        "island": "basic",
        "description": "+10 Rapid Root",
        "effects": [
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": 10,
                "conditions": {"item": "Rapid Root"},
            },
        ],
    },
    "Fruitful Bounty": {
        "tree": "Compost",
        "tier": 2,
        "island": "basic",
        "description": "Double Fruitful Blend's Effect",
        "effects": [
            {
                "type": "COLLECTIBLE_EFFECT_MULTIPLIER",
                "operation": "multiply",
                "value": 2,
                "conditions": {"item": "Fruitful Blend"},
            },
        ],
    },
    "Composting Overhaul": {
        "tree": "Compost",
        "tier": 3,
        "island": "basic",
        "description": "+2 Worms; -5 fertilisers",
        "effects": [
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": 2,
                "conditions": {"item": "Worm"},
            },
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": -5,
                "conditions": {"category": "Fertiliser"},
            },
        ],
    },
    "Composting Revamp": {
        "tree": "Compost",
        "tier": 3,
        "island": "basic",
        "description": "+5 fertilisers; -3 Worms",
        "effects": [
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": 5,
                "conditions": {"category": "Fertiliser"},
            },
            {
                "type": "COMPOST_YIELD",
                "operation": "add",
                "value": -3,
                "conditions": {"item": "Worm"},
            },
        ],
    },

}

# ------------------------------------------------------------------------------
# 2. LEGACY_BADGES: The original badge system from the game's early days.
#    Useful for historical player data and understanding legacy effects.
# ------------------------------------------------------------------------------
LEGACY_BADGES = {
    "Green Thumb": {
        "level": 5,
        "profession": "farming",
        "conflicts_with": "Barn Manager",
        "requires": None,
        "description": "Crops are worth 5% more; Increase mutant crop chance.",
        "effects": [
            {
                "type": "SELL_PRICE",
                "operation": "multiply",
                "value": 1.05,
                "conditions": {"category": "Crop"},
            },
            {
                "type": "MUTANT_CROP_CHANCE",
                "operation": "multiply",
                "value": 1.10, # Assuming a 10% increase
            },
        ],
    },
    "Barn Manager": {
        "level": 5,
        "profession": "farming",
        "conflicts_with": "Green Thumb",
        "requires": None,
        "description": "Animals yield 10% more goods; Increase mutant animal chance.",
        "effects": [
            {
                "type": "ANIMAL_PRODUCE_YIELD",
                "operation": "multiply",
                "value": 1.10,
            },
            {
                "type": "MUTANT_ANIMAL_CHANCE",
                "operation": "multiply",
                "value": 1.10, # Assuming a 10% increase
            },
        ],
    },
    "Seed Specialist": {
        "level": 10,
        "profession": "farming",
        "conflicts_with": "Wrangler",
        "requires": "Green Thumb",
        "description": "Crops take 10% less time to grow; Increase mutant crop chance.",
        "effects": [
            {
                "type": "CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
            {
                "type": "MUTANT_CROP_CHANCE",
                "operation": "multiply",
                "value": 1.10, # Assuming a 10% increase
            },
        ],
    },
    "Wrangler": {
        "level": 10,
        "profession": "farming",
        "conflicts_with": "Seed Specialist",
        "requires": "Barn Manager",
        "description": "Animals take 10% less time to produce goods; Increase mutant animal chance.",
        "effects": [
            {
                "type": "ANIMAL_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
            {
                "type": "MUTANT_ANIMAL_CHANCE",
                "operation": "multiply",
                "value": 1.10, # Assuming a 10% increase
            },
        ],
    },
    "Lumberjack": {
        "level": 5,
        "profession": "gathering",
        "conflicts_with": "Prospector",
        "requires": None,
        "description": "Increase wood drops by 10%.",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "multiply",
                "value": 1.10,
                "conditions": {"item": "Wood"},
            },
        ],
    },
    "Prospector": {
        "level": 5,
        "profession": "gathering",
        "conflicts_with": "Lumberjack",
        "requires": None,
        "description": "Increase stone drops by 20%.",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "multiply",
                "value": 1.20,
                "conditions": {"item": "Stone"},
            },
        ],
    },
    "Logger": {
        "level": 10,
        "profession": "gathering",
        "conflicts_with": "Gold Rush",
        "requires": "Lumberjack",
        "description": "Axes last 50% longer.",
        "effects": [
            {
                "type": "TOOL_DURABILITY",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"item": "Axe"},
            },
        ],
    },
    "Gold Rush": {
        "level": 10,
        "profession": "gathering",
        "conflicts_with": "Logger",
        "requires": "Prospector",
        "description": "Increase gold drops by 50%.",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "multiply",
                "value": 1.50,
                "conditions": {"item": "Gold"},
            },
        ],
    },
    "Artist": {
        "level": 1,
        "profession": "contributor",
        "description": "Save 10% on shop & blacksmith tools.",
        "effects": [
            {
                "type": "SHOP_COST",
                "operation": "multiply",
                "value": 0.90,
                "conditions": {"category": "Tool"},
            },
        ],
    },
    "Coder": {
        "level": 1,
        "profession": "contributor",
        "description": "Crops yield 20% more.",
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "multiply",
                "value": 1.20,
            },
        ],
    },
    "Discord Mod": {
        "level": 1,
        "profession": "contributor",
        "description": "Yield 35% more wood.",
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "multiply",
                "value": 1.35,
                "conditions": {"item": "Wood"},
            },
        ],
    },
    "Liquidity Provider": {
        "level": 1,
        "profession": "contributor",
        "description": "50% reduced SFL withdrawal fee.",
        "effects": [
            {
                "type": "WITHDRAWAL_FEE",
                "operation": "multiply",
                "value": 0.50,
                "conditions": {"currency": "SFL"},
            },
        ],
    },
    "Warrior": {
        "level": 1,
        "profession": "combat",
        "description": "Early access to land expansion.",
        "effects": [
            {
                "type": "EARLY_ACCESS",
                "operation": "set",
                "value": True,
                "conditions": {"feature": "LandExpansion"},
            },
        ],
    },
}

# ------------------------------------------------------------------------------
# 3. BUMPKIN_SKILLS: The first generation of Bumpkin skills.
# ------------------------------------------------------------------------------
BUMPKIN_SKILLS = {
    "Green Thumb": {
        "tree": "Crops",
        "description": "Crops yield 5% more",
        "disabled": False,
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "multiply",
                "value": 1.05,
            },
        ],
    },
    "Cultivator": {
        "tree": "Crops",
        "description": "Crops grow 5% quicker",
        "disabled": False,
        "effects": [
            {
                "type": "CROP_GROWTH_TIME",
                "operation": "multiply",
                "value": 0.95,
            },
        ],
    },
    "Master Farmer": {
        "tree": "Crops",
        "description": "Crops yield 10% more",
        "disabled": False,
        "effects": [
            {
                "type": "CROP_YIELD",
                "operation": "multiply",
                "value": 1.10,
            },
        ],
    },
    "Golden Flowers": {
        "tree": "Crops",
        "description": "Chance for Sunflowers to Drop Gold",
        "disabled": False,
        "effects": [
            {
                "type": "SPECIAL_RESOURCE_CHANCE",
                "operation": "set_chance",
                "value": 0.01, # Assuming 1% chance
                "yield_item": "Gold",
                "yield_amount": 1, # Assuming 1 Gold
                "conditions": {"item": "Sunflower"},
            },
        ],
    },
    "Happy Crop": {
        "tree": "Crops",
        "description": "Chance to get 2x crops",
        "disabled": False,
        "effects": [
            {
                "type": "DOUBLE_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.10, # Assuming 10% chance
                "conditions": {"category": "Crop"},
            },
        ],
    },
    "Lumberjack": {
        "tree": "Trees",
        "description": "Trees drop 10% more",
        "disabled": False,
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "multiply",
                "value": 1.10,
                "conditions": {"item": "Wood"},
            },
        ],
    },
    "Tree Hugger": {
        "tree": "Trees",
        "description": "Trees regrow 20% quicker",
        "disabled": False,
        "effects": [
            {
                "type": "TREE_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.80,
            },
        ],
    },
    "Tough Tree": {
        "tree": "Trees",
        "description": "Chance to get 3x wood drops",
        "disabled": False,
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.10, # Assuming 10% chance
                "bonus_multiplier": 3,
                "conditions": {"item": "Wood"},
            },
        ],
    },
    "Money Tree": {
        "tree": "Trees",
        "description": "Chance for coin drops",
        "disabled": False,
        "effects": [
            {
                "type": "COIN_DROP_CHANCE",
                "operation": "set_chance",
                "value": 0.05, # Assuming 5% chance
                "coin_amount": 1, # Assuming 1 Coin
                "conditions": {"action": "ChopTree"},
            },
        ],
    },
    "Digger": {
        "tree": "Rocks",
        "description": "Stone Drops 10% more",
        "disabled": False,
        "effects": [
            {
                "type": "RESOURCE_YIELD",
                "operation": "multiply",
                "value": 1.10,
                "conditions": {"item": "Stone"},
            },
        ],
    },
    "Coal Face": {
        "tree": "Rocks",
        "description": "Stones recover 20% quicker",
        "disabled": False,
        "effects": [
            {
                "type": "ROCK_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.80,
                "conditions": {"item": "Stone Rock"},
            },
        ],
    },
    "Gold Rush": {
        "tree": "Rocks",
        "description": "Chance to get 2.5x gold drops",
        "disabled": False,
        "effects": [
            {
                "type": "BONUS_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.05, # Assuming 5% chance
                "bonus_multiplier": 2.5,
                "conditions": {"item": "Gold"},
            },
        ],
    },
    "Rush Hour": {
        "tree": "Cooking",
        "description": "Cook meals 10% faster",
        "disabled": False,
        "effects": [
            {
                "type": "COOKING_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "Kitchen Hand": {
        "tree": "Cooking",
        "description": "Meals yield an extra 5% experience",
        "disabled": False,
        "effects": [
            {
                "type": "CONSUME_XP",
                "operation": "multiply",
                "value": 1.05,
            },
        ],
    },
    "Michelin Stars": {
        "tree": "Cooking",
        "description": "High quality food, earn additional 5% SFL",
        "disabled": False,
        "effects": [
            {
                "type": "SELL_PRICE",
                "operation": "multiply",
                "value": 1.05,
                "conditions": {"category": "Food"},
            },
        ],
    },
    "Curer": {
        "tree": "Cooking",
        "description": "Consuming deli goods adds extra 15% exp",
        "disabled": False,
        "effects": [
            {
                "type": "CONSUME_XP",
                "operation": "multiply",
                "value": 1.15,
                "conditions": {"building": "Deli"},
            },
        ],
    },
    "Stable Hand": {
        "tree": "Animals",
        "description": "Animals produce 10% quicker",
        "disabled": False,
        "effects": [
            {
                "type": "ANIMAL_RECOVERY_TIME",
                "operation": "multiply",
                "value": 0.90,
            },
        ],
    },
    "Free Range": {
        "tree": "Animals",
        "description": "+0.1 Animal Produce",
        "disabled": False,
        "effects": [
            {
                "type": "ANIMAL_PRODUCE_YIELD",
                "operation": "add",
                "value": 0.1,
            },
        ],
    },
    "Horse Whisperer": {
        "tree": "Animals",
        "description": "Increase chance of mutants",
        "disabled": False,
        "effects": [
            {
                "type": "MUTANT_ANIMAL_CHANCE",
                "operation": "multiply",
                "value": 1.20, # Assuming 20% increase
            },
        ],
    },
    "Buckaroo": {
        "tree": "Animals",
        "description": "Chance of double drops",
        "disabled": False,
        "effects": [
            {
                "type": "DOUBLE_YIELD_CHANCE",
                "operation": "set_chance",
                "value": 0.10, # Assuming 10% chance
                "conditions": {"category": "Animal"},
            },
        ],
    },
}