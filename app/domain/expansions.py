# app/domain/expansions.py

"""
Fonte Única da Verdade para os dados de expansão da terra.
Combina os requisitos para desbloquear um nível e os recursos (nodes)
que esse nível fornece, numa única estrutura de dados.
"""

# Coordenadas para cada lote de expansão para o mini-mapa
EXPANSION_COORDINATES = {
    # Lote 0 é omitido, pois não é uma expansão comprável
    1: {"x": 0, "y": 0}, 2: {"x": 0, "y": 1}, 3: {"x": -1, "y": 1},
    4: {"x": -2, "y": 1}, 5: {"x": -2, "y": 0}, 6: {"x": -2, "y": -1},
    7: {"x": -1, "y": -1}, 8: {"x": 0, "y": -1}, 9: {"x": 1, "y": -1},
    10: {"x": 1, "y": 0}, 11: {"x": 1, "y": 1}, 12: {"x": 1, "y": 2},
    13: {"x": 0, "y": 2}, 14: {"x": -1, "y": 2}, 15: {"x": -2, "y": 2},
    16: {"x": -3, "y": 2}, 17: {"x": -3, "y": 1}, 18: {"x": -3, "y": 0},
    19: {"x": -3, "y": -1}, 20: {"x": -3, "y": -2}, 21: {"x": -2, "y": -2},
    22: {"x": -1, "y": -2}, 23: {"x": 0, "y": -2}, 24: {"x": 1, "y": -2},
    25: {"x": 2, "y": -2}, 26: {"x": 2, "y": -1}, 27: {"x": 2, "y": 0},
    28: {"x": 2, "y": 1}, 29: {"x": 2, "y": 2}, 30: {"x": 2, "y": 3}
}

EXPANSION_DATA = {
    "basic": {
        3: {
            "requirements": {}, # Nível 3 não tem requisitos de expansão, apenas desbloqueia nodes
            "nodes": {"Crop Plot": 0, "Tree": 3, "Stone Rock": 2, "Iron Rock": 0, "Gold Rock": 0, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 0, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        4: {
            "requirements": {"Bumpkin Level": 1, "Time": "00:00:05", "Wood": 3},
            "nodes": {"Crop Plot": 9, "Tree": 5, "Stone Rock": 3, "Iron Rock": 1, "Gold Rock": 0, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 0, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        5: {
            "requirements": {"Bumpkin Level": 1, "Time": "00:00:05", "Coins": 0.25, "Wood": 5},
            "nodes": {"Crop Plot": 17, "Tree": 6, "Stone Rock": 4, "Iron Rock": 2, "Gold Rock": 1, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 0, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        6: {
            "requirements": {"Bumpkin Level": 2, "Time": "00:01:00", "Coins": 60, "Stone": 1},
            "nodes": {"Crop Plot": 25, "Tree": 7, "Stone Rock": 5, "Iron Rock": 2, "Gold Rock": 1, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 0, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        7: {
            "requirements": {"Bumpkin Level": 5, "Time": "00:30:00", "Stone": 5, "Iron": 1},
            "nodes": {"Crop Plot": 27, "Tree": 8, "Stone Rock": 6, "Iron Rock": 3, "Gold Rock": 1, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 0, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        8: {
            "requirements": {"Bumpkin Level": 8, "Time": "04:00:00", "Iron": 3, "Gold": 1},
            "nodes": {"Crop Plot": 29, "Tree": 9, "Stone Rock": 7, "Iron Rock": 3, "Gold Rock": 2, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 0, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        9: {
            "requirements": {"Bumpkin Level": 11, "Time": "12:00:00", "Wood": 100, "Stone": 40, "Iron": 5},
            "nodes": {"Crop Plot": 31, "Tree": 9, "Stone Rock": 7, "Iron Rock": 4, "Gold Rock": 2, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 0, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        10: {
            "requirements": {}, # Requisitos para o nível 10 estão na ilha "petal"
            "nodes": {"Crop Plot": 31, "Tree": 9, "Stone Rock": 7, "Iron Rock": 4, "Gold Rock": 2, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 2, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        11: {
            "requirements": {},
            "nodes": {"Crop Plot": 33, "Tree": 11, "Stone Rock": 9, "Iron Rock": 5, "Gold Rock": 3, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 3, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        12: {
            "requirements": {},
            "nodes": {"Crop Plot": 33, "Tree": 12, "Stone Rock": 10, "Iron Rock": 5, "Gold Rock": 3, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 4, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        13: {
            "requirements": {},
            "nodes": {"Crop Plot": 35, "Tree": 13, "Stone Rock": 11, "Iron Rock": 5, "Gold Rock": 3, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 4, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        14: {
            "requirements": {},
            "nodes": {"Crop Plot": 37, "Tree": 13, "Stone Rock": 12, "Iron Rock": 6, "Gold Rock": 4, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 5, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        15: {
            "requirements": {},
            "nodes": {"Crop Plot": 37, "Tree": 14, "Stone Rock": 12, "Iron Rock": 6, "Gold Rock": 4, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 6, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        16: {
            "requirements": {},
            "nodes": {"Crop Plot": 37, "Tree": 14, "Stone Rock": 12, "Iron Rock": 7, "Gold Rock": 5, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 7, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        17: {
            "requirements": {},
            "nodes": {"Crop Plot": 39, "Tree": 15, "Stone Rock": 13, "Iron Rock": 7, "Gold Rock": 5, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 8, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        18: {
            "requirements": {},
            "nodes": {"Crop Plot": 41, "Tree": 15, "Stone Rock": 13, "Iron Rock": 7, "Gold Rock": 5, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 8, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        19: {
            "requirements": {},
            "nodes": {"Crop Plot": 41, "Tree": 16, "Stone Rock": 14, "Iron Rock": 8, "Gold Rock": 5, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 9, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        20: {
            "requirements": {},
            "nodes": {"Crop Plot": 43, "Tree": 16, "Stone Rock": 14, "Iron Rock": 8, "Gold Rock": 5, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 10, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        21: {
            "requirements": {},
            "nodes": {"Crop Plot": 44, "Tree": 17, "Stone Rock": 15, "Iron Rock": 9, "Gold Rock": 5, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 11, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        22: {
            "requirements": {},
            "nodes": {"Crop Plot": 45, "Tree": 18, "Stone Rock": 15, "Iron Rock": 9, "Gold Rock": 6, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 11, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        },
        23: {
            "requirements": {},
            "nodes": {"Crop Plot": 46, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Crimstone Rock": 0, "Sunstone Rock": 0, "Fruit Patch": 12, "Flower Bed": 0, "Beehive": 0, "Oil Reserve": 0, "Lava Pit": 0}
        }
    },
    "petal": {
        4: {
            "requirements": {}, # Os requisitos para o nível 4 ainda são da ilha "basic"
            "nodes": {"Crop Plot": 31, "Fruit Patch": 2, "Tree": 9, "Stone Rock": 7, "Iron Rock": 4, "Gold Rock": 2, "Crimstone Rock": 0, "Sunstone Rock": 0, "Beehive": 0, "Oil Reserve": 0, "Flower Bed": 0, "Lava Pit": 0}
        },
        5: {
            "requirements": {"Bumpkin Level": 11, "Time": "00:01:00", "Wood": 20},
            "nodes": {"Crop Plot": 33, "Fruit Patch": 3, "Tree": 11, "Stone Rock": 9, "Iron Rock": 5, "Gold Rock": 3, "Crimstone Rock": 0, "Sunstone Rock": 0, "Beehive": 0, "Oil Reserve": 0, "Flower Bed": 0, "Lava Pit": 0}
        },
        6: {
            "requirements": {"Bumpkin Level": 13, "Time": "00:05:00", "Wood": 10, "Stone": 5, "Gold": 2},
            "nodes": {"Crop Plot": 33, "Fruit Patch": 4, "Tree": 12, "Stone Rock": 10, "Iron Rock": 5, "Gold Rock": 3, "Crimstone Rock": 0, "Sunstone Rock": 0, "Beehive": 1, "Flower Bed": 1, "Oil Reserve": 0, "Lava Pit": 0}
        },
        7: {
            "requirements": {"Bumpkin Level": 16, "Time": "00:30:00", "Wood": 30, "Stone": 20, "Iron": 5, "Gem": 15},
            "nodes": {"Crop Plot": 35, "Fruit Patch": 4, "Tree": 13, "Stone Rock": 11, "Iron Rock": 5, "Gold Rock": 3, "Crimstone Rock": 1, "Sunstone Rock": 0, "Beehive": 1, "Flower Bed": 1, "Oil Reserve": 0, "Lava Pit": 0}
        },
        8: {
            "requirements": {"Bumpkin Level": 20, "Time": "02:00:00", "Wood": 20, "Crimstone": 1, "Gem": 15},
            "nodes": {"Crop Plot": 37, "Fruit Patch": 5, "Tree": 13, "Stone Rock": 12, "Iron Rock": 6, "Gold Rock": 4, "Crimstone Rock": 1, "Sunstone Rock": 0, "Beehive": 1, "Flower Bed": 1, "Oil Reserve": 0, "Lava Pit": 0}
        },
        9: {
            "requirements": {"Bumpkin Level": 23, "Time": "02:00:00", "Wood": 50, "Gold": 5, "Gem": 15},
            "nodes": {"Crop Plot": 37, "Fruit Patch": 6, "Tree": 14, "Stone Rock": 12, "Iron Rock": 6, "Gold Rock": 4, "Crimstone Rock": 1, "Sunstone Rock": 1, "Beehive": 1, "Flower Bed": 1, "Oil Reserve": 0, "Lava Pit": 0}
        },
        10: {
            "requirements": {"Bumpkin Level": 25, "Time": "04:00:00", "Stone": 10, "Crimstone": 3, "Gem": 15},
            "nodes": {"Crop Plot": 37, "Fruit Patch": 7, "Tree": 14, "Stone Rock": 12, "Iron Rock": 7, "Gold Rock": 5, "Crimstone Rock": 1, "Sunstone Rock": 1, "Beehive": 2, "Flower Bed": 2, "Oil Reserve": 0, "Lava Pit": 0}
        },
        11: {
            "requirements": {"Bumpkin Level": 27, "Time": "08:00:00", "Wood": 100, "Stone": 25, "Gold": 5, "Crimstone": 1, "Gem": 15},
            "nodes": {"Crop Plot": 39, "Fruit Patch": 8, "Tree": 15, "Stone Rock": 13, "Iron Rock": 7, "Gold Rock": 5, "Crimstone Rock": 1, "Sunstone Rock": 1, "Beehive": 2, "Flower Bed": 2, "Oil Reserve": 0, "Lava Pit": 0}
        },
        12: {
            "requirements": {"Bumpkin Level": 29, "Time": "12:00:00", "Wood": 50, "Iron": 5, "Crimstone": 3, "Gem": 30},
            "nodes": {"Crop Plot": 41, "Fruit Patch": 8, "Tree": 15, "Stone Rock": 13, "Iron Rock": 7, "Gold Rock": 5, "Crimstone Rock": 1, "Sunstone Rock": 1, "Beehive": 2, "Flower Bed": 2, "Oil Reserve": 0, "Lava Pit": 0}
        },
        13: {
            "requirements": {"Bumpkin Level": 32, "Time": "12:00:00", "Wood": 50, "Stone": 25, "Iron": 10, "Gold": 10, "Gem": 30},
            "nodes": {"Crop Plot": 41, "Fruit Patch": 9, "Tree": 16, "Stone Rock": 14, "Iron Rock": 8, "Gold Rock": 5, "Crimstone Rock": 1, "Sunstone Rock": 2, "Beehive": 2, "Flower Bed": 2, "Oil Reserve": 0, "Lava Pit": 0}
        },
        14: {
            "requirements": {"Bumpkin Level": 36, "Time": "24:00:00", "Wood": 100, "Stone": 10, "Crimstone": 5, "Gem": 30},
            "nodes": {"Crop Plot": 43, "Fruit Patch": 10, "Tree": 16, "Stone Rock": 14, "Iron Rock": 8, "Gold Rock": 5, "Crimstone Rock": 1, "Sunstone Rock": 2, "Beehive": 2, "Flower Bed": 2, "Oil Reserve": 0, "Lava Pit": 0}
        },
        15: {
            "requirements": {"Bumpkin Level": 40, "Time": "24:00:00", "Wood": 150, "Stone": 10, "Iron": 10, "Gold": 5, "Crimstone": 5, "Gem": 30},
            "nodes": {"Crop Plot": 44, "Fruit Patch": 11, "Tree": 17, "Stone Rock": 15, "Iron Rock": 9, "Gold Rock": 5, "Crimstone Rock": 2, "Sunstone Rock": 2, "Beehive": 2, "Flower Bed": 2, "Oil Reserve": 0, "Lava Pit": 0}
        },
        16: {
            "requirements": {"Bumpkin Level": 43, "Time": "24:00:00", "Wood": 100, "Stone": 10, "Gold": 5, "Crimstone": 8, "Gem": 30},
            "nodes": {"Crop Plot": 45, "Fruit Patch": 11, "Tree": 18, "Stone Rock": 15, "Iron Rock": 9, "Gold Rock": 6, "Crimstone Rock": 2, "Sunstone Rock": 2, "Beehive": 3, "Flower Bed": 3, "Oil Reserve": 0, "Lava Pit": 0}
        },
        17: {
            "requirements": {},
            "nodes": {"Crop Plot": 46, "Fruit Patch": 12, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Crimstone Rock": 2, "Sunstone Rock": 2, "Beehive": 3, "Flower Bed": 3, "Oil Reserve": 0, "Lava Pit": 0}
        },
        18: {
            "requirements": {},
            "nodes": {"Crop Plot": 46, "Fruit Patch": 12, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Crimstone Rock": 2, "Sunstone Rock": 3, "Beehive": 3, "Flower Bed": 3, "Oil Reserve": 0, "Lava Pit": 0}
        },
        19: {
            "requirements": {},
            "nodes": {"Crop Plot": 48, "Fruit Patch": 12, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Crimstone Rock": 3, "Sunstone Rock": 3, "Beehive": 3, "Flower Bed": 3, "Oil Reserve": 0, "Lava Pit": 0}
        },
        20: {
            "requirements": {},
            "nodes": {"Crop Plot": 50, "Fruit Patch": 12, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Crimstone Rock": 3, "Sunstone Rock": 4, "Beehive": 3, "Flower Bed": 3, "Oil Reserve": 0, "Lava Pit": 0}
        },
    },

    "desert": {
        4: {
            "requirements": {}, # Requisitos para o nível 4 ainda são da ilha "petal"
            "nodes": {"Crop Plot": 45, "Fruit Patch": 11, "Tree": 18, "Stone Rock": 15, "Iron Rock": 9, "Gold Rock": 6, "Crimstone Rock": 2, "Sunstone Rock": 2, "Oil Reserve": 0, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        5: {
            "requirements": {"Bumpkin Level": 40, "Time": "00:01:00", "Wood": 50, "Stone": 10, "Iron": 5, "Gold": 5},
            "nodes": {"Crop Plot": 46, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Fruit Patch": 11, "Crimstone Rock": 2, "Sunstone Rock": 2, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        6: {
            "requirements": {"Bumpkin Level": 40, "Time": "00:05:00", "Wood": 100, "Stone": 20, "Iron": 10, "Gold": 5},
            "nodes": {"Crop Plot": 46, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Fruit Patch": 12, "Crimstone Rock": 2, "Sunstone Rock": 3, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        7: {
            "requirements": {"Bumpkin Level": 41, "Time": "00:30:00", "Wood": 150, "Stone": 20, "Iron": 10, "Gold": 5, "Gem": 15},
            "nodes": {"Crop Plot": 48, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Fruit Patch": 12, "Crimstone Rock": 3, "Sunstone Rock": 3, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        8: {
            "requirements": {"Bumpkin Level": 42, "Time": "02:00:00", "Wood": 150, "Stone": 10, "Iron": 5, "Gold": 5, "Crimstone": 3, "Oil": 5, "Gem": 30},
            "nodes": {"Crop Plot": 50, "Tree": 18, "Stone Rock": 16, "Iron Rock": 10, "Gold Rock": 6, "Fruit Patch": 12, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        9: {
            "requirements": {"Bumpkin Level": 43, "Time": "02:00:00", "Wood": 50, "Stone": 5, "Iron": 5, "Gold": 5, "Crimstone": 6, "Oil": 5, "Gem": 30},
            "nodes": {"Crop Plot": 50, "Tree": 19, "Stone Rock": 17, "Iron Rock": 10, "Gold Rock": 6, "Fruit Patch": 12, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        10: {
            "requirements": {"Bumpkin Level": 44, "Time": "08:00:00", "Coins": 320, "Wood": 100, "Stone": 50, "Iron": 10, "Gold": 5, "Crimstone": 12, "Oil": 10, "Gem": 45},
            "nodes": {"Crop Plot": 51, "Tree": 19, "Stone Rock": 17, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 12, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        11: {
            "requirements": {"Bumpkin Level": 45, "Time": "12:00:00", "Coins": 640, "Wood": 150, "Stone": 75, "Iron": 10, "Gold": 5, "Crimstone": 15, "Oil": 30, "Gem": 45},
            "nodes": {"Crop Plot": 52, "Tree": 19, "Stone Rock": 17, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        12: {
            "requirements": {"Bumpkin Level": 47, "Time": "12:00:00", "Coins": 1280, "Wood": 100, "Stone": 100, "Iron": 5, "Gold": 10, "Crimstone": 18, "Oil": 30, "Gem": 45},
            "nodes": {"Crop Plot": 54, "Tree": 19, "Stone Rock": 17, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        13: {
            "requirements": {"Bumpkin Level": 50, "Time": "24:00:00", "Coins": 2560, "Wood": 200, "Stone": 50, "Iron": 15, "Gold": 10, "Crimstone": 21, "Oil": 40, "Gem": 45},
            "nodes": {"Crop Plot": 54, "Tree": 20, "Stone Rock": 17, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        14: {
            "requirements": {"Bumpkin Level": 53, "Time": "24:00:00", "Coins": 3200, "Wood": 200, "Stone": 100, "Iron": 15, "Gold": 10, "Crimstone": 24, "Oil": 50, "Gem": 45},
            "nodes": {"Crop Plot": 55, "Tree": 20, "Stone Rock": 18, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 1, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        15: {
            "requirements": {"Bumpkin Level": 56, "Time": "24:00:00", "Coins": 3200, "Wood": 300, "Stone": 50, "Iron": 20, "Gold": 10, "Crimstone": 27, "Oil": 75, "Gem": 45},
            "nodes": {"Crop Plot": 56, "Tree": 20, "Stone Rock": 18, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 2, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        16: {
            "requirements": {"Bumpkin Level": 58, "Time": "36:00:00", "Coins": 3200, "Wood": 250, "Stone": 125, "Iron": 15, "Gold": 15, "Crimstone": 30, "Oil": 100, "Gem": 60},
            "nodes": {"Crop Plot": 57, "Tree": 21, "Stone Rock": 18, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 2, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        17: {
            "requirements": {"Bumpkin Level": 60, "Time": "36:00:00", "Coins": 4800, "Wood": 350, "Stone": 75, "Iron": 20, "Gold": 10, "Crimstone": 33, "Oil": 125, "Gem": 60},
            "nodes": {"Crop Plot": 59, "Tree": 21, "Stone Rock": 18, "Iron Rock": 11, "Gold Rock": 6, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 2, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        18: {
            "requirements": {"Bumpkin Level": 63, "Time": "36:00:00", "Coins": 4800, "Wood": 400, "Stone": 125, "Iron": 25, "Gold": 15, "Crimstone": 36, "Oil": 150, "Gem": 75},
            "nodes": {"Crop Plot": 60, "Tree": 21, "Stone Rock": 18, "Iron Rock": 11, "Gold Rock": 7, "Fruit Patch": 13, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 2, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        19: {
            "requirements": {"Bumpkin Level": 65, "Time": "36:00:00", "Coins": 6400, "Wood": 450, "Stone": 150, "Iron": 30, "Gold": 20, "Crimstone": 39, "Oil": 200, "Gem": 60},
            "nodes": {"Crop Plot": 61, "Tree": 21, "Stone Rock": 18, "Iron Rock": 11, "Gold Rock": 7, "Fruit Patch": 14, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 2, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        20: {
            "requirements": {"Bumpkin Level": 68, "Time": "48:00:00", "Coins": 6400, "Wood": 525, "Stone": 200, "Iron": 35, "Gold": 30, "Crimstone": 42, "Oil": 250, "Gem": 60},
            "nodes": {"Crop Plot": 61, "Tree": 22, "Stone Rock": 19, "Iron Rock": 11, "Gold Rock": 7, "Fruit Patch": 14, "Crimstone Rock": 3, "Sunstone Rock": 4, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        21: {
            "requirements": {"Bumpkin Level": 70, "Time": "48:00:00", "Coins": 8000, "Wood": 550, "Stone": 150, "Iron": 30, "Gold": 25, "Crimstone": 45, "Oil": 350, "Gem": 60},
            "nodes": {"Crop Plot": 62, "Tree": 22, "Stone Rock": 19, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 14, "Crimstone Rock": 3, "Sunstone Rock": 5, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        22: {
            "requirements": {"Bumpkin Level": 72, "Time": "48:00:00", "Coins": 8000, "Wood": 600, "Stone": 200, "Iron": 35, "Gold": 30, "Crimstone": 48, "Oil": 450, "Gem": 75},
            "nodes": {"Crop Plot": 62, "Tree": 23, "Stone Rock": 19, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 3, "Sunstone Rock": 5, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        23: {
            "requirements": {"Bumpkin Level": 73, "Time": "60:00:00", "Coins": 8000, "Wood": 650, "Stone": 250, "Iron": 40, "Gold": 35, "Crimstone": 51, "Oil": 500, "Gem": 75},
            "nodes": {"Crop Plot": 63, "Tree": 23, "Stone Rock": 19, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 5, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        24: {
            "requirements": {"Bumpkin Level": 74, "Time": "60:00:00", "Coins": 9600, "Wood": 700, "Stone": 300, "Iron": 50, "Gold": 45, "Crimstone": 54, "Oil": 550, "Gem": 75},
            "nodes": {"Crop Plot": 64, "Tree": 23, "Stone Rock": 19, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 6, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        25: {
            "requirements": {"Bumpkin Level": 75, "Time": "60:00:00", "Coins": 11200, "Wood": 750, "Stone": 350, "Iron": 50, "Gold": 50, "Crimstone": 60, "Oil": 650, "Gem": 75},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 6, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
    },

    "volcano": {
        5: {
            "requirements": {}, # Requisitos para o nível 5 ainda são da ilha "desert"
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 6, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        6: {
            "requirements": {"Bumpkin Level": 70, "Time": "00:00:10", "Wood": 100, "Stone": 50, "Iron": 30, "Gold": 10},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 6, "Oil Reserve": 3, "Lava Pit": 0, "Beehive": 3, "Flower Bed": 3}
        },
        7: {
            "requirements": {"Bumpkin Level": 72, "Time": "00:05:00", "Coins": 320, "Wood": 200, "Stone": 75, "Iron": 25, "Gold": 15, "Crimstone": 4, "Oil": 30, "Gem": 30},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 6, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        8: {
            "requirements": {"Bumpkin Level": 74, "Time": "00:30:00", "Coins": 640, "Wood": 300, "Stone": 100, "Iron": 40, "Gold": 20, "Crimstone": 8, "Oil": 60, "Gem": 30},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 7, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        9: {
            "requirements": {"Bumpkin Level": 76, "Time": "01:00:00", "Coins": 960, "Wood": 400, "Stone": 150, "Iron": 35, "Gold": 25, "Crimstone": 12, "Oil": 90, "Gem": 60},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 7, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 7, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        10: {
            "requirements": {"Bumpkin Level": 78, "Time": "02:00:00", "Coins": 1600, "Wood": 450, "Stone": 200, "Iron": 30, "Gold": 20, "Crimstone": 16, "Oil": 120, "Obsidian": 1, "Gem": 60},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 7, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        11: {
            "requirements": {"Bumpkin Level": 80, "Time": "04:00:00", "Coins": 2500, "Wood": 500, "Stone": 175, "Iron": 30, "Gold": 30, "Crimstone": 20, "Oil": 100, "Gem": 90},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 7, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        12: {
            "requirements": {"Bumpkin Level": 82, "Time": "08:00:00", "Coins": 3200, "Wood": 650, "Stone": 225, "Iron": 25, "Gold": 25, "Crimstone": 24, "Oil": 100, "Obsidian": 2, "Gem": 150},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 8, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        13: {
            "requirements": {"Bumpkin Level": 84, "Time": "12:00:00", "Coins": 4000, "Wood": 550, "Stone": 200, "Iron": 40, "Gold": 30, "Crimstone": 28, "Oil": 100, "Gem": 150},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 8, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        14: {
            "requirements": {"Bumpkin Level": 86, "Time": "12:00:00", "Coins": 4800, "Wood": 700, "Stone": 250, "Iron": 35, "Gold": 35, "Crimstone": 32, "Oil": 100, "Obsidian": 1, "Gem": 150},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 8, "Oil Reserve": 3, "Lava Pit": 1, "Beehive": 3, "Flower Bed": 3}
        },
        15: {
            "requirements": {"Bumpkin Level": 88, "Time": "24:00:00", "Coins": 5600, "Wood": 650, "Stone": 200, "Iron": 30, "Gold": 40, "Crimstone": 36, "Oil": 200, "Obsidian": 2, "Gem": 150},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 8, "Oil Reserve": 3, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        16: {
            "requirements": {"Bumpkin Level": 90, "Time": "24:00:00", "Coins": 6400, "Wood": 750, "Stone": 250, "Iron": 40, "Gold": 30, "Crimstone": 40, "Oil": 200, "Obsidian": 4, "Gem": 150},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 8, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        17: {
            "requirements": {"Bumpkin Level": 92, "Time": "24:00:00", "Coins": 8000, "Wood": 700, "Stone": 200, "Iron": 35, "Gold": 35, "Crimstone": 44, "Oil": 200, "Obsidian": 4, "Gem": 150},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 9, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        18: {
            "requirements": {"Bumpkin Level": 94, "Time": "36:00:00", "Coins": 10000, "Wood": 800, "Stone": 300, "Iron": 45, "Gold": 45, "Crimstone": 48, "Oil": 200, "Obsidian": 6, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 9, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        19: {
            "requirements": {"Bumpkin Level": 96, "Time": "36:00:00", "Coins": 12800, "Wood": 750, "Stone": 250, "Iron": 40, "Gold": 40, "Crimstone": 52, "Oil": 200, "Obsidian": 6, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 10, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        20: {
            "requirements": {"Bumpkin Level": 98, "Time": "48:00:00", "Coins": 15000, "Wood": 850, "Stone": 300, "Iron": 45, "Gold": 30, "Crimstone": 56, "Oil": 200, "Obsidian": 8, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 10, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        21: {
            "requirements": {"Bumpkin Level": 100, "Time": "48:00:00", "Coins": 18000, "Wood": 900, "Stone": 325, "Iron": 50, "Gold": 35, "Crimstone": 60, "Oil": 200, "Obsidian": 8, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 11, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        22: {
            "requirements": {"Bumpkin Level": 102, "Time": "48:00:00", "Coins": 21000, "Wood": 800, "Stone": 300, "Iron": 45, "Gold": 30, "Crimstone": 64, "Oil": 200, "Obsidian": 10, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 12, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 11, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        23: {
            "requirements": {"Bumpkin Level": 104, "Time": "48:00:00", "Coins": 25000, "Wood": 950, "Stone": 350, "Iron": 50, "Gold": 35, "Crimstone": 68, "Oil": 200, "Obsidian": 10, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 11, "Oil Reserve": 4, "Lava Pit": 2, "Beehive": 3, "Flower Bed": 3}
        },
        24: {
            "requirements": {"Bumpkin Level": 106, "Time": "48:00:00", "Coins": 28000, "Wood": 1000, "Stone": 400, "Iron": 55, "Gold": 40, "Crimstone": 72, "Oil": 300, "Obsidian": 12, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 4, "Sunstone Rock": 11, "Oil Reserve": 4, "Lava Pit": 3, "Beehive": 3, "Flower Bed": 3}
        },
        25: {
            "requirements": {"Bumpkin Level": 108, "Time": "60:00:00", "Coins": 32000, "Wood": 1100, "Stone": 450, "Iron": 60, "Gold": 35, "Crimstone": 80, "Oil": 300, "Obsidian": 12, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 5, "Sunstone Rock": 11, "Oil Reserve": 4, "Lava Pit": 3, "Beehive": 3, "Flower Bed": 3}
        },
        26: {
            "requirements": {"Bumpkin Level": 110, "Time": "60:00:00", "Coins": 35000, "Wood": 1200, "Stone": 350, "Iron": 65, "Gold": 30, "Crimstone": 85, "Oil": 300, "Obsidian": 18, "Gem": 180},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 5, "Sunstone Rock": 11, "Oil Reserve": 4, "Lava Pit": 3, "Beehive": 3, "Flower Bed": 3}
        },
        27: {
            "requirements": {"Bumpkin Level": 112, "Time": "60:00:00", "Coins": 38000, "Wood": 1250, "Stone": 450, "Iron": 70, "Gold": 40, "Crimstone": 95, "Oil": 300, "Obsidian": 24, "Gem": 225},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 5, "Sunstone Rock": 11, "Oil Reserve": 4, "Lava Pit": 3, "Beehive": 3, "Flower Bed": 3}
        },
        28: {
            "requirements": {"Bumpkin Level": 114, "Time": "60:00:00", "Coins": 42000, "Wood": 1150, "Stone": 500, "Iron": 60, "Gold": 45, "Crimstone": 100, "Oil": 300, "Obsidian": 30, "Gem": 225},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 5, "Sunstone Rock": 12, "Oil Reserve": 4, "Lava Pit": 3, "Beehive": 3, "Flower Bed": 3}
        },
        29: {
            "requirements": {"Bumpkin Level": 116, "Time": "72:00:00", "Coins": 45000, "Wood": 1350, "Stone": 550, "Iron": 65, "Gold": 40, "Crimstone": 105, "Oil": 300, "Obsidian": 36, "Gem": 225},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 5, "Sunstone Rock": 12, "Oil Reserve": 4, "Lava Pit": 3, "Beehive": 3, "Flower Bed": 3}
        },
        30: {
            "requirements": {"Bumpkin Level": 120, "Time": "72:00:00", "Coins": 50000, "Wood": 1500, "Stone": 600, "Iron": 70, "Gold": 50, "Crimstone": 125, "Oil": 300, "Obsidian": 42, "Gem": 225},
            "nodes": {"Crop Plot": 65, "Tree": 23, "Stone Rock": 20, "Iron Rock": 13, "Gold Rock": 8, "Fruit Patch": 15, "Crimstone Rock": 5, "Sunstone Rock": 13, "Oil Reserve": 4, "Lava Pit": 3, "Beehive": 3, "Flower Bed": 3}
        }
    }
}

