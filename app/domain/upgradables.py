# app/domain/upgradables.py
"""
Fonte da Verdade para os dados de itens que são resultado de um upgrade.

Este módulo centraliza os nós de recursos avançados (árvores, rochas, etc.)
que podem existir tanto como um nó físico na fazenda quanto como um item
contável no inventário do jogador.

A principal informação aqui é o 'multiplier', que é crucial para calcular
o rendimento final desses nós.

Fonte: `resources.ts` -> RESOURCE_MULTIPLIER
"""

UPGRADABLE_NODES = {
    # --- Árvores ---
    "Ancient Tree": {
        "name": "Ancient Tree",
        "type": "Tree",
        "multiplier": 4,
    },
    "Sacred Tree": {
        "name": "Sacred Tree",
        "type": "Tree",
        "multiplier": 16,
    },

    # --- Rochas ---
    "Fused Stone Rock": {"name": "Fused Stone Rock", "type": "Stone Rock", "multiplier": 4},
    "Reinforced Stone Rock": {"name": "Reinforced Stone Rock", "type": "Stone Rock", "multiplier": 16},
    "Refined Iron Rock": {"name": "Refined Iron Rock", "type": "Iron Rock", "multiplier": 4},
    "Tempered Iron Rock": {"name": "Tempered Iron Rock", "type": "Iron Rock", "multiplier": 16},
    "Pure Gold Rock": {"name": "Pure Gold Rock", "type": "Gold Rock", "multiplier": 4},
    "Prime Gold Rock": {"name": "Prime Gold Rock", "type": "Gold Rock", "multiplier": 16},
}

# Para facilitar a integração com o item_map, unificamos em um só dicionário
ALL_UPGRADABLES = {
    **UPGRADABLE_NODES
}