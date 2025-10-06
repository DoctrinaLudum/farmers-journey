# app/domain/calendar_events.py

from .fishing import FISHING_DATA

CALENDAR_EVENTS = {
    # Eventos Positivos
    "bountifulHarvest": {
        "description": "Crops and fruits yield double the amount.",
        "category": "positive",
        "boosts": [
            {
                "type": "YIELD",
                "item": "Crop",
                "operation": "add",
                "value": 1
            },
            {
                "type": "YIELD",
                "item": "Fruit",
                "operation": "add",
                "value": 1
            }
        ]
    },
    "sunshower": {
        "description": "A luminous rain brings good fortune to your crops.",
        "category": "positive",
        "boosts": [{
            "type": "TIME",
            "operation": "mul",
            "value": 0.50
        }]
    },
    "doubleDelivery": {
        "description": "Get double the rewards for deliveries.",
        "category": "positive"
    },
    "fishFrenzy": {
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
        "description": "A massive wave threatens to wash away your crops.",
        "category": "negative"
    },
    "insectPlague": {
        "description": "A swarm of insects descends, potentially damaging crops.",
        "category": "negative"
    },
    "tornado": {
        "description": "A powerful tornado that can destroy buildings and resources.",
        "category": "negative"
    },
    "greatFreeze": {
        "description": "A severe frost that can kill unprotected crops.",
        "category": "negative"
    }
}