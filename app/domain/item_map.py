# app/domain/item_map.py
import logging

from . import (buildings, crops, fishing, flowers, foods, fruits, nodes,
               resources, seeds, tools, treasure_dig)

log = logging.getLogger(__name__)

# --- CONFIGURAÇÃO DO MAPA ---
# Mover a definição dos domínios para constantes no topo do ficheiro torna
# a configuração mais clara e fácil de modificar.

# Domínios onde a categoria é a mesma para todos os itens.
FIXED_CATEGORY_DOMAINS = [
    (seeds.SEEDS_DATA, "Seed"),
    (nodes.RESOURCE_NODES, "Nodes"),
    (fishing.FISHING_DATA, "Fish"),
    (flowers.FLOWER_DATA, "Flower"),
    (fruits.FRUIT_DATA, "Fruit"),
    (tools.TOOLS_DATA, "Tool"),
    (treasure_dig.DIGGING_TOOLS, "Tool"),
    (buildings.BUILDING_REQUIREMENTS, "Building"),
    (treasure_dig.TREASURES, "Treasure"), # Movido para aqui para usar uma categoria fixa.
]

# Domínios onde a categoria é extraída da chave 'type' de cada item.
# O segundo elemento da tupla é uma categoria padrão (fallback).
TYPED_DOMAINS = [
    (resources.RESOURCES_DATA, "Resource"),
    (crops.CROPS_DATA, "Crop"),
    (foods.CONSUMABLES_DATA, "Food"),
]

MASTER_ITEM_MAP = {}

def _add_to_map(item_name: str, category: str):
    """
    Adiciona um item ao mapa mestre, verificando a existência de duplicados.
    A verificação de duplicados é a chave para a robustez deste sistema.
    """
    if item_name in MASTER_ITEM_MAP:
        log.warning(
            f"Item duplicado encontrado ao construir o mapa mestre: '{item_name}'. "
            f"Categoria existente: '{MASTER_ITEM_MAP[item_name]}', "
            f"Nova categoria ignorada: '{category}'."
        )
    else:
        MASTER_ITEM_MAP[item_name] = category

def _process_fixed_domains():
    """Processa domínios com uma categoria fixa para todos os itens."""
    for domain_dict, category in FIXED_CATEGORY_DOMAINS:
        for item_name in domain_dict:
            _add_to_map(item_name, category)

def _process_typed_domains():
    """Processa domínios onde a categoria é definida pela chave 'type'."""
    for domain_dict, default_category in TYPED_DOMAINS:
        for item_name, item_data in domain_dict.items():
            category = item_data.get("type", default_category)
            _add_to_map(item_name, category)

def _build_master_item_map():
    """
    Orquestra a construção do mapa mestre chamando as funções de processamento.
    Executado apenas uma vez na inicialização da aplicação.
    """
    log.info("Construindo o mapa mestre de itens...")

    # A função principal agora apenas chama as funções auxiliares.
    _process_fixed_domains()
    _process_typed_domains()

    log.info(f"Mapa mestre de itens construído com {len(MASTER_ITEM_MAP)} itens únicos.")

# --- PONTO DE ENTRADA ---
# O mapa é construído assim que este módulo é importado pela primeira vez.
if not MASTER_ITEM_MAP:
    _build_master_item_map()