# app/domain/prices.py
import logging

from . import crops, foods, seeds, tools, treasure_dig

log = logging.getLogger(__name__)

MASTER_PRICE_MAP = {}

def _process_domain(domain_dict, price_keys):
    """
    Processa um dicionário de domínio e extrai os preços.
    price_keys é um dicionário mapeando a chave de preço no domínio para a nossa chave padrão.
    Ex: {"sell_price": "coins", "cost_coins": "coins", "price": "coins"}
    """
    for item_name, item_data in domain_dict.items():
        if item_name not in MASTER_PRICE_MAP:
            MASTER_PRICE_MAP[item_name] = {}

        for source_key, target_key in price_keys.items():
            if source_key in item_data and item_data[source_key] is not None:
                price_value = item_data[source_key]
                # Evita sobrescrever um preço já definido, a menos que seja zero.
                if target_key not in MASTER_PRICE_MAP[item_name] or MASTER_PRICE_MAP[item_name][target_key] == 0:
                    MASTER_PRICE_MAP[item_name][target_key] = float(price_value)

def _build_master_price_map():
    """
    Constrói um mapa mestre de preços a partir de todos os domínios de itens.
    Este mapa unificado será a fonte da verdade para todos os preços no sistema.
    """
    log.info("Construindo o mapa mestre de preços...")

    price_key_mappings = {"sell_price": "coins", "cost_coins": "coins", "price": "coins", "sfl_price": "sfl"}

    domains_to_process = [
        crops.CROPS,
        foods.CONSUMABLES_DATA,
        seeds.SEEDS_DATA,
        tools.TOOLS_DATA,
        treasure_dig.TREASURES,
    ]

    for domain in domains_to_process:
        _process_domain(domain, price_key_mappings)

    log.info(f"Mapa mestre de preços construído com {len(MASTER_PRICE_MAP)} itens.")

if not MASTER_PRICE_MAP:
    _build_master_price_map()

