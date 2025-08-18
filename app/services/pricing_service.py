# app/services/pricing_service.py
from ..domain.prices import MASTER_PRICE_MAP


def get_item_prices(item_name: str) -> dict:
    """
    Busca os preços de um item no mapa mestre de preços.

    Args:
        item_name (str): O nome do item a ser buscado.

    Returns:
        dict: Um dicionário contendo os preços do item para diferentes moedas
              (ex: {'coins': 10, 'sfl': 0.5}), ou um dicionário vazio se o
              item não for encontrado.
    """
    return MASTER_PRICE_MAP.get(item_name, {})

