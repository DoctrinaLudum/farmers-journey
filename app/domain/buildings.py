# app/domain/buildings.py (VERSÃO COMPLETA E CORRIGIDA)

"""
Fonte de Verdade para os dados dos edifícios, incluindo em que nível e ILHA
eles são desbloqueados e se estão atualmente habilitados no jogo.
"""

BUILDING_REQUIREMENTS = {
    # Edifícios da Ilha Basic
    "Town Center": {"unlocksAtLevel": 0, "unlocksOnIsland": "basic", "enabled": True},
    "Market": {"unlocksAtLevel": 0, "unlocksOnIsland": "basic", "enabled": True},
    "Fire Pit": {"unlocksAtLevel": 0, "unlocksOnIsland": "basic", "enabled": True},
    "Workbench": {"unlocksAtLevel": 0, "unlocksOnIsland": "basic", "enabled": True},
    "Water Well": {"unlocksAtLevel": 1, "unlocksOnIsland": "basic", "enabled": True},
    "Kitchen": {"unlocksAtLevel": 2, "unlocksOnIsland": "basic", "enabled": True},
    "Hen House": {"unlocksAtLevel": 4, "unlocksOnIsland": "basic", "enabled": True},
    "Bakery": {"unlocksAtLevel": 5, "unlocksOnIsland": "basic", "enabled": True},
    "Deli": {"unlocksAtLevel": 7, "unlocksOnIsland": "basic", "enabled": True},
    "Smoothie Shack": {"unlocksAtLevel": 9, "unlocksOnIsland": "basic", "enabled": True},

    # Edifícios da Ilha Petal (Spring)
    "Toolshed": {"unlocksAtLevel": 10, "unlocksOnIsland": "petal", "enabled": True},
    "Warehouse": {"unlocksAtLevel": 10, "unlocksOnIsland": "petal", "enabled": True},
    "Compost Bin": {"unlocksAtLevel": 10, "unlocksOnIsland": "petal", "enabled": True},
    "Turbo Composter": {"unlocksAtLevel": 11, "unlocksOnIsland": "petal", "enabled": True},
    "Premium Composter": {"unlocksAtLevel": 12, "unlocksOnIsland": "petal", "enabled": True},

    # Edifícios da Ilha Desert
    "Manor": {"unlocksAtLevel": 17, "unlocksOnIsland": "desert", "enabled": False},
    "Greenhouse": {"unlocksAtLevel": 19, "unlocksOnIsland": "desert", "enabled": True},
    "Barn": {"unlocksAtLevel": 21, "unlocksOnIsland": "desert", "enabled": True},
    "Crop Machine": {"unlocksAtLevel": 23, "unlocksOnIsland": "desert", "enabled": True},
    
}