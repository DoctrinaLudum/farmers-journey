# app/domain/buildings.py

"""
Fonte de Verdade para os dados dos edifícios, incluindo em que nível
de expansão eles são desbloqueados e se estão atualmente habilitados no jogo.
"""

BUILDING_REQUIREMENTS = {
    # Edifícios da Ilha Basic
    "Town Center": {"unlocksAtLevel": 0, "enabled": True},
    "Market": {"unlocksAtLevel": 0, "enabled": True},
    "Fire Pit": {"unlocksAtLevel": 0, "enabled": True},
    "Workbench": {"unlocksAtLevel": 0, "enabled": True},
    "Water Well": {"unlocksAtLevel": 1, "enabled": True},
    "Kitchen": {"unlocksAtLevel": 2, "enabled": True},
    "Hen House": {"unlocksAtLevel": 4, "enabled": True},
    "Bakery": {"unlocksAtLevel": 5, "enabled": True},
    "Deli": {"unlocksAtLevel": 7, "enabled": True},
    "Smoothie Shack": {"unlocksAtLevel": 9, "enabled": True},

    # Edifícios da Ilha Petal (Spring)
    "Toolshed": {"unlocksAtLevel": 10, "enabled": True},
    "Warehouse": {"unlocksAtLevel": 10, "enabled": True},
    "Compost Bin": {"unlocksAtLevel": 10, "enabled": True},
    "Turbo Composter": {"unlocksAtLevel": 11, "enabled": True},
    "Premium Composter": {"unlocksAtLevel": 12, "enabled": True},

    # Edifícios da Ilha Desert
    "Manor": {"unlocksAtLevel": 17, "enabled": False},
    "Greenhouse": {"unlocksAtLevel": 19, "enabled": True},
    "Barn": {"unlocksAtLevel": 21, "enabled": True},
}