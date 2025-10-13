# app/domain/calendar_events.py
"""
Define os eventos de calendário estáticos do jogo, seus nomes de exibição,
descrições e os bônus que eles fornecem.

Esta estrutura de dados é a fonte da verdade para os efeitos de cada evento.
O `calendar_service` lê estes dados para determinar os bônus ativos.

Estrutura de um Evento:
- "display_name": Nome amigável para exibição na interface.
- "description": Texto descritivo sobre o evento.
- "category": "positive" ou "negative".
- "boosts": Uma lista de dicionários de bônus.
    - "type": O atributo que o bônus afeta (ex: "YIELD", "GROWTH_TIME").
    - "item": (Opcional) A categoria de item que o bônus afeta (ex: "Crop", "Fruit").
              Se omitido, o bônus é considerado genérico para o `type`.
    - "operation": Como o bônus é aplicado ("add" para adição, "mul" para multiplicação).
    - "value": O valor do bônus.
"""

from .fishing import FISHING_DATA

CALENDAR_EVENTS = {
    # Eventos Positivos
    "bountifulHarvest": {
        "display_name": "Bountiful Harvest",
        "description": "Crops, fruits, greenhouse plants and crop machine produce extra yield.",
        "category": "positive",
        "boosts": [
            {
                "type": "YIELD",
                "item": "Crop",
                "operation": "add",
                "value": 1.0
            },
            {
                "type": "YIELD",
                "item": "Fruit",
                "operation": "add",
                "value": 1.0
            },
            {
                "type": "YIELD",
                "item": "Greenhouse",
                "operation": "add",
                "value": 1.0
            },
            {
                "type": "YIELD",
                "item": "CropMachine",
                "operation": "add",
                "value": 1.0
            }
        ]
    },
    "sunshower": {
        "display_name": "Sunshower",
        "description": "A luminous rain brings good fortune to your crops.",
        "category": "positive",
        "boosts": [{
            "type": "RECOVERY_TIME",
            "item": "Crop",
            "operation": "percentage",
            "value": -0.50
        }]
    },
    "doubleDelivery": {
        "display_name": "Double Delivery",
        "description": "Get double the rewards for deliveries.",
        "category": "positive"
    },
    "fishFrenzy": {
        "display_name": "Fish Frenzy",
        "description": "+1 fish per catch.",
        "category": "positive",
        "boosts": [{
            "type": "YIELD",
            "operation": "add",
            "value": 1,
            "conditions": {
                "resource_names": list(FISHING_DATA.keys())
            }
        }]
    },

    # Eventos Negativos
    "tsunami": {
        "display_name": "Tsunami",
        "description": "A massive wave threatens to wash away your crops.",
        "category": "negative"
    },
    "insectPlague": {
        "display_name": "Insect Plague",
        "description": "A swarm of insects descends, potentially damaging crops.",
        "category": "negative"
    },
    "tornado": {
        "display_name": "Tornado",
        "description": "A powerful tornado that can destroy buildings and resources.",
        "category": "negative"
    },
    "greatFreeze": {
        "display_name": "Great Freeze",
        "description": "A severe frost that can kill unprotected crops.",
        "category": "negative"
    }
}