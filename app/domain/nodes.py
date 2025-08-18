# app/domain/nodes.py
"""
Fonte da Verdade para os dados dos Nós de Recursos (Resource Nodes).

Este módulo centraliza todas as informações sobre os pontos de coleta
e produção de recursos no jogo, como árvores, rochas, canteiros e
construções especiais.
"""

RESOURCE_NODES = {
    "Tree": {
        "name": "Tree",
        "yields": "Wood",
        "dimensions": {"width": 2, "height": 2},
        "respawn_time_seconds": 7200,
    },
    "Stone Rock": {
        "name": "Stone Rock",
        "yields": "Stone",
        "dimensions": {"width": 1, "height": 1},
        "respawn_time_seconds": 14400,
    },
    "Iron Rock": {
        "name": "Iron Rock",
        "yields": "Iron",
        "dimensions": {"width": 1, "height": 1},
        "respawn_time_seconds": 28800,
    },
    "Gold Rock": {
        "name": "Gold Rock",
        "yields": "Gold",
        "dimensions": {"width": 1, "height": 1},
        "respawn_time_seconds": 43200,
    },
    "Crimstone Rock": {
        "name": "Crimstone Rock",
        "yields": "Crimstone",
        "dimensions": {"width": 2, "height": 2},
        "respawn_time_seconds": 86400,
    },
    "Sunstone Rock": {
        "name": "Sunstone Rock",
        "yields": "Sunstone",
        "dimensions": {"width": 2, "height": 2},
        "respawn_time_seconds": 172800,
    },
    "Oil Reserve": {
        "name": "Oil Reserve",
        "yields": "Oil",
        "dimensions": {"width": 2, "height": 2},
        "respawn_time_seconds": 72000,
    },
    "Boulder": {
        "name": "Boulder",
        "yields": "Diamond",
        "dimensions": {"width": 2, "height": 2},
        "respawn_time_seconds": None,
    },
    "Lava Pit": {
        "name": "Lava Pit",
        "yields": "Obsidian",
        "dimensions": {"width": 2, "height": 2},
        "respawn_time_seconds": None,
    },
    "Crop Plot": {
        "name": "Crop Plot",
        "yields_category": "Crop",
        "dimensions": {"width": 1, "height": 1},
        "respawn_time_seconds": None,
    },
    "Fruit Patch": {
        "name": "Fruit Patch",
        "yields_category": "Fruit",
        "dimensions": {"width": 2, "height": 2},
        "respawn_time_seconds": None,
    },
    "Flower Bed": {
        "name": "Flower Bed",
        "yields_category": "Flower",
        "dimensions": {"width": 3, "height": 1},
        "respawn_time_seconds": None,
    },
    "Hen House": {
        "name": "Hen House",
        "yields_category": "Animal",
        "dimensions": {"width": 4, "height": 3},
        "respawn_time_seconds": None,
    },
    "Barn": {
        "name": "Barn",
        "yields_category": "Animal",
        "dimensions": {"width": 4, "height": 4},
        "respawn_time_seconds": None,
    },
    "Beehive": {
        "name": "Beehive",
        "yields": "Honey",
        "dimensions": {"width": 1, "height": 1},
        "respawn_time_seconds": None,
    },
    "Compost Bin": {
        "name": "Compost Bin",
        "yields": "Sprout Mix",
        "dimensions": {"width": 2, "height": 2},
        "time_to_finish_seconds": 21600,
    },
    "Turbo Composter": {
        "name": "Turbo Composter",
        "yields": "Fruitful Blend",
        "dimensions": {"width": 2, "height": 2},
        "time_to_finish_seconds": 28800,
    },
    "Premium Composter": {
        "name": "Premium Composter",
        "yields": "Rapid Root",
        "dimensions": {"width": 2, "height": 2},
        "time_to_finish_seconds": 43200,
    },
}