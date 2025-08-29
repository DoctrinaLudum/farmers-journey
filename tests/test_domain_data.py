# tests/test_domain_data.py
import os

import pytest

from app.domain import bumpkin, skills, wearablesItemBuffs

# --- Conjunto de valores válidos para os testes ---

VALID_PARTS = set(bumpkin.SLOTS_ORDER.keys())

# Estes conjuntos devem ser mantidos atualizados à medida que novos boosts são adicionados.
# Eles são a "fonte da verdade" para a validação.
VALID_BOOST_TYPES = {
    "SELL_PRICE", "CROP_YIELD", "CROP_GROWTH_TIME", "CRITICAL_HIT", "SEED_COST",
    "XP", "INSTANT_GROWTH", "FRUIT_YIELD", "RESOURCE_YIELD", "TREASURE_YIELD",
    "FREE_GIFT", "CAST_FISHING_ROD", "FISH_CRITICAL", "BAIT_YIELD",
    "FISHING_ATTEMPTS", "DAILY_DIGS", "DIG_TREASURE", "DRILL_OIL", "MARKS_GAIN",
    "RESOURCE_COOLDOWN", "ANIMAL_PRODUCE_YIELD", "ANIMAL_RECOVERY_TIME",
    "BEE_SWARM_CHANCE", "FLOWER_GROWTH_TIME", "BEEHIVE_PRODUCTION_SPEED",
    "POLLINATION_YIELD_BOOST", "RESOURCE_PRODUCTION_SPEED", "ANIMAL_FEED_REDUCTION",
    "DELIVERY_REWARD", "SPECIAL_RESOURCE_CHANCE", "SCARECROW_AOE",
    "COLLECTIBLE_EFFECT_MULTIPLIER", "AXELESS_FRUIT_CHOpping", "FRUIT_GROWTH_TIME",
    "SHOP_STOCK", "BONUS_YIELD_CHANCE", "TREE_RECOVERY_TIME", "INSTANT_CHOP",
    "CRAFTING_COST", "COIN_DROP_CHANCE", "INSTANT_GROWTH_CHANCE", "FISHING_LIMIT",
    "FISHING_MINIGAME_BAR_SIZE", "FRENZY_YIELD", "FRENZY_BONUS_CHANCE",
    "COMPOST_YIELD", "FISHING_XP", "ANIMAL_FEED_COST", "BALE_AFFECTS_ITEMS",
    "ANIMAL_XP", "CRAFTING_RECIPE_CHANGE", "CRAFTING_COST_REDUCTION",
    "ANIMAL_SICKNESS_CHANCE", "INSTANT_WAKE_UP", "GREENHOUSE_YIELD",
    "GREENHOUSE_CROP_GROWTH_TIME", "GREENHOUSE_OIL_COST", "ROCK_RECOVERY_TIME",
    "INSTANT_MINE", "CONSECUTIVE_MINING_BONUS", "COOKING_TIME", "CONSUME_XP",
    "INSTANT_COOK", "GIFTING_RELATIONSHIP_POINTS", "CROP_MACHINE_TIME",
    "CROP_MACHINE_OIL_COST", "OIL_TANK_CAPACITY", "CROP_MACHINE_ELIGIBILITY",
    "CROP_MACHINE_QUEUE", "CROP_MACHINE_PLOT_COUNT", "INSTANT_REFILL",
    "COMPOST_BOOST_INGREDIENT", "COMPOST_BOOST_SPEED_INCREASE",
    "COMPOST_BOOST_COST", "FACTION_PET_SATIATION", "BONUS_FISHING_BOUNTY",
    "CROP_COST"
}

VALID_BOOST_OPERATIONS = {
    "multiply", "add", "set_chance", "set", "add_items", "replace", "add_hours"
}

# --- Testes ---

# @pytest.mark.parametrize("item_id, data", wearablesItemBuffs.WEARABLES_ITEM_BUFFS.items())
# def test_wearable_item_buffs_schema(item_id, data):
#     """Testa se cada entrada em WEARABLES_ITEM_BUFFS segue o schema esperado."""
#     # 1. Validação da Estrutura Principal e Tipos
#     assert isinstance(item_id, int), f"A chave do dicionário '{item_id}' deveria ser um inteiro."
#     assert item_id == data.get('id'), f"A chave '{item_id}' não corresponde ao 'id' interno {data.get('id')}."
#
#     # Validação cruzada com a "fonte da verdade" dos IDs em bumpkin.py
#     item_name = data.get('name')
#     expected_id = bumpkin.ITEM_IDS.get(item_name)
#     assert expected_id is not None, f"O item '{item_name}' (ID {item_id}) não foi encontrado em bumpkin.ITEM_IDS."
#     assert item_id == expected_id, (
#         f"O ID para '{item_name}' está inconsistente. "
#         f"WEARABLES_DATA usa o ID {item_id}, mas bumpkin.ITEM_IDS espera {expected_id}."
#     )
#
#     expected_keys = {"id", "name", "description", "image_path", "part", "tradable", "boosts", "enabled"}
#     assert expected_keys.issubset(data.keys()), f"Faltam chaves no item ID {item_id}. Esperado: {expected_keys}"
#
#     assert all(isinstance(data[key], str) for key in ["name", "description", "image_path", "part"])
#     assert all(isinstance(data[key], bool) for key in ["tradable", "enabled"])
#     assert isinstance(data['boosts'], (dict, list))
#
#     # 2. Validação de Valores Específicos
#     assert data['part'] in VALID_PARTS, f"'{data['part']}' não é uma parte válida para o item ID {item_id}."
#
#     image_path = data['image_path']
#     image_full_path = os.path.join('app/static/images/', image_path)
#
#     # Validação do caminho da imagem, com mensagem de erro útil para a migração para .webp
#     if not os.path.exists(image_full_path):
#         base, ext = os.path.splitext(image_path)
#         # Se o ficheiro .png não existe, verifica se existe uma versão .webp
#         if ext.lower() == '.png':
#             webp_path = base + '.webp'
#             webp_full_path = os.path.join('app/static/images/', webp_path)
#             if os.path.exists(webp_full_path):
#                 # A falha aqui é intencional para forçar a atualização do dicionário de dados.
#                 pytest.fail(
#                     f"O ficheiro '{image_path}' para o item ID {item_id} não foi encontrado, "
#                     f"mas '{webp_path}' existe. Por favor, atualize o caminho em WEARABLES_DATA."
#                 )
#     assert os.path.exists(image_full_path), f"O caminho da imagem '{image_full_path}' para o item ID {item_id} não existe."
#
#     # 3. Validação da Estrutura de Boosts
#     if isinstance(data['boosts'], list):
#         for boost in data['boosts']:
#             assert isinstance(boost, dict), f"Cada boost no item ID {item_id} deveria ser um dicionário."
#
#             boost_type = boost.get('type')
#             assert boost_type in VALID_BOOST_TYPES, f"'{boost_type}' não é um tipo de boost válido no item ID {item_id}."
#
#             operation = boost.get('operation')
#             assert operation in VALID_BOOST_OPERATIONS, f"'{operation}' não é uma operação de boost válida no item ID {item_id}."