# app/services/resource_analysis_service.py

import logging
from decimal import Decimal

from ..domain import (collectiblesItemBuffs as collectibles_domain,
                      skills as skills_domain,
                      wearablesItemBuffs as wearables_domain)

log = logging.getLogger(__name__)

# ==============================================================================
# FUNÇÕES GENÉRICAS DE ANÁLISE DE RECURSOS
# ==============================================================================

def _get_all_item_data():
    """Unifica todos os dicionários de domínio em um único lugar."""
    return {
        **skills_domain.LEGACY_BADGES,
        **skills_domain.BUMPKIN_REVAMP_SKILLS,
        **wearables_domain.WEARABLES_ITEM_BUFFS,
        **collectibles_domain.COLLECTIBLES_ITEM_BUFFS
    }

def filter_boosts_from_domains(resource_conditions: dict):
    """
    Varre todos os domínios e cria um dicionário otimizado contendo
    apenas os itens e bônus que afetam um conjunto específico de recursos.

    Args:
        resource_conditions (dict): Um dicionário de configuração que define
                                    quais recursos e tipos de bônus procurar.
                                    Ex: {'yield_resource_names': ['Wood'], ...}
    """
    boost_catalogue = {}
    log.info(f"Iniciando a catalogação de bônus para as condições: {resource_conditions}")
    all_item_data = _get_all_item_data()

    yield_names = resource_conditions.get('yield_resource_names', [])
    recovery_names = resource_conditions.get('recovery_resource_names', [])
    skill_tree = resource_conditions.get('skill_tree_name')

    for item_name, item_details in all_item_data.items():
        boost_list = item_details.get("boosts") or item_details.get("effects")

        if not item_details or not boost_list or not item_details.get("enabled", True):
            continue

        # CORREÇÃO: Apenas filtra se a skill TIVER uma árvore definida. Skills gerais (sem árvore) não são filtradas.
        # Isto garante que "Native" seja incluído nos catálogos de madeira e mineração.
        if skill_tree and item_name in skills_domain.BUMPKIN_REVAMP_SKILLS and item_details.get("tree") and item_details.get("tree") != skill_tree:
            continue

        relevant_boosts = []
        for boost in boost_list:
            conditions = boost.get("conditions", {})
            # Lida com o fato de que a condição pode ser uma string ou uma lista de strings.
            resource_name_or_list = conditions.get("resource") or conditions.get("item")
            
            # Garante que estamos sempre a trabalhar com uma lista para simplificar a lógica.
            resource_names_to_check = resource_name_or_list if isinstance(resource_name_or_list, list) else [resource_name_or_list]

            # Verifica se QUALQUER um dos recursos na lista do bônus é relevante para esta categoria.
            is_yield_boost = (
                boost.get("type") in ["YIELD", "RESOURCE_YIELD", "BONUS_YIELD_CHANCE", "CRITICAL_YIELD_BONUS", "CRITICAL_CHANCE"] and
                any(name in yield_names for name in resource_names_to_check)
            )
            
            is_recovery_boost = (
                boost.get("type") in ["RECOVERY_TIME", "TREE_RECOVERY_TIME"] and
                any(name in recovery_names for name in resource_names_to_check)
            )

            if is_yield_boost or is_recovery_boost:
                standardized_boost = boost.copy()
                if boost.get("type") in ["YIELD", "RESOURCE_YIELD"]:
                    standardized_boost['type'] = 'YIELD'
                elif boost.get("type") in ["RECOVERY_TIME", "TREE_RECOVERY_TIME"]:
                    standardized_boost['type'] = 'RECOVERY_TIME'
                
                relevant_boosts.append(standardized_boost)

        if relevant_boosts:
            source_type = "wearable" if item_name in wearables_domain.WEARABLES_ITEM_BUFFS else \
                          "collectible" if item_name in collectibles_domain.COLLECTIBLES_ITEM_BUFFS else \
                          "skill"
            
            boost_catalogue[item_name] = {
                "boosts": relevant_boosts,
                "source_type": source_type,
                "has_aoe": "aoe" in item_details
            }

    log.info(f"Catalogação concluída. Total de itens encontrados: {len(boost_catalogue)}")
    return boost_catalogue

def get_active_player_boosts(player_items: set, boost_catalogue: dict, non_cumulative_groups: dict = None) -> list:
    """
    Pega um conjunto de itens do jogador e os cruza com um catálogo de bônus
    para retornar uma lista de bônus ativos, respeitando hierarquias.
    """
    active_boosts = []
    non_cumulative_groups = non_cumulative_groups or {}
    
    items_in_any_group = set()
    for group_items in non_cumulative_groups.values():
        items_in_any_group.update(group_items)

    # 1. Processa os grupos hierárquicos
    for group_name, ordered_items in non_cumulative_groups.items():
        for item_name in ordered_items:
            if item_name in player_items and item_name in boost_catalogue:
                # CORREÇÃO: Ignora itens com AOE, pois eles são tratados por posição.
                if boost_catalogue[item_name].get("has_aoe"):
                    log.debug(f"Item hierárquico '{item_name}' tem AOE, será tratado por posição.")
                    continue

                item_boosts = boost_catalogue[item_name]["boosts"]
                is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)

                log.debug(f"Aplicando bônus hierárquico de '{group_name}': '{item_name}'.")
                for boost in item_boosts:
                    if is_critical_item and boost.get("type") == "YIELD":
                        continue
                    active_boosts.append({"source_item": item_name, **boost})
                break

    # 2. Processa todos os outros bônus que não são hierárquicos
    for item_name in player_items:
        if item_name in boost_catalogue and item_name not in items_in_any_group:
            # CORREÇÃO: Ignora itens com AOE, pois eles são tratados por posição.
            if boost_catalogue[item_name].get("has_aoe"):
                log.debug(f"Item '{item_name}' tem AOE, será tratado por posição.")
                continue

            item_boosts = boost_catalogue[item_name]["boosts"]
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)
            for boost in item_boosts:
                if is_critical_item and boost.get("type") == "YIELD":
                    continue
                active_boosts.append({"source_item": item_name, **boost})

    return active_boosts

def get_aoe_boosts_for_resource(resource_position: dict, placed_items: dict, player_skills: set) -> list:
    """
    Calcula os bônus de Área de Efeito (AOE) que se aplicam a uma posição específica,
    considerando modificações de skills.

    Args:
        resource_position: As coordenadas {'x': int, 'y': int} do recurso a ser verificado.
        placed_items: Um dicionário de todos os itens colocados na fazenda (ex: farm_data['collectibles']).
        player_skills: Um conjunto com os nomes de todas as habilidades que o jogador possui.

    Returns:
        Uma lista de dicionários de bônus que se aplicam àquela posição.
    """
    active_aoe_boosts = []
    if not resource_position or resource_position.get('x') is None or resource_position.get('y') is None:
        return active_aoe_boosts

    rx, ry = resource_position['x'], resource_position['y']

    # Unifica todos os itens que podem ter AOE para fácil consulta
    all_aoe_items = {**collectibles_domain.COLLECTIBLES_ITEM_BUFFS}

    for item_name, placements in placed_items.items():
        item_details = all_aoe_items.get(item_name)
        if not item_details or "aoe" not in item_details:
            continue

        # --- Lógica de Modificação de AOE por Skills ---
        final_aoe = item_details["aoe"]
        for skill_name in player_skills:
            skill_details = skills_domain.BUMPKIN_REVAMP_SKILLS.get(skill_name)
            if not skill_details: continue
            
            for effect in skill_details.get("effects", []):
                if effect.get("name") == "MODIFY_ITEM_AOE" and effect.get("target_item") == item_name:
                    final_aoe = effect["new_aoe"]
                    log.info(f"Skill '{skill_name}' modificou a AOE de '{item_name}'.")
                    break

        # Itera sobre cada instância do item colocada na fazenda
        for placement in placements:
            placement_coords = placement.get("coordinates", {})
            ax, ay = placement_coords.get("x"), placement_coords.get("y")
            if ax is None or ay is None: continue

            is_within_range = False
            if final_aoe.get("shape") == "circle":
                radius = final_aoe.get("radius", 0)
                if abs(rx - ax) <= radius and abs(ry - ay) <= radius:
                    is_within_range = True
            elif final_aoe.get("shape") == "custom":
                for plot in final_aoe.get("plots", []):
                    if rx == (ax + plot["x"]) and ry == (ay + plot["y"]):
                        is_within_range = True
                        break
            
            if is_within_range:
                for boost in item_details.get("boosts", []):
                    active_aoe_boosts.append({"source_item": f"{item_name} (AOE)", **boost})
                break

    return active_aoe_boosts

def _conditions_are_met(conditions: dict, resource_name: str, node_context: dict) -> bool:
    """
    Função auxiliar para verificar se todas as condições de um bônus são atendidas.
    """
    node_context = node_context or {}

    # Condição 1: Recurso/Item
    required_resource_or_item = conditions.get("resource") or conditions.get("item")
    if required_resource_or_item:
        names_to_check = required_resource_or_item if isinstance(required_resource_or_item, list) else [required_resource_or_item]
        if resource_name not in names_to_check:
            return False

    # Condição 2: Minas Restantes (minesLeft)
    required_mines_left = conditions.get("minesLeft")
    if required_mines_left is not None:
        current_mines_left = node_context.get("minesLeft")
        if current_mines_left != required_mines_left:
            return False

    # Se todas as condições passaram, retorna True.
    return True

def calculate_final_yield(base_yield: float, active_boosts: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o rendimento final, separando bônus determinísticos de bônus de chance.
    Filtra os bônus com base no nome do recurso e no contexto do nó.
    """
    base = Decimal(str(base_yield))
    additive_bonus = Decimal('0')
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []
    chance_bonuses = []

    for boost in active_boosts:
        conditions = boost.get("conditions", {})
        if _conditions_are_met(conditions, resource_name, node_context):
            boost_type = boost.get("type")
            if boost_type == "YIELD":
                operation = boost["operation"]
                value = Decimal(str(boost["value"]))

                if operation == "add":
                    additive_bonus += value
                elif operation == "subtract":
                    additive_bonus -= value
                elif operation == "percentage":
                    multiplicative_factor *= (Decimal('1') + value)
                elif operation == "multiply":
                    multiplicative_factor *= value

                applied_buffs_details.append(boost)
            elif boost_type == "BONUS_YIELD_CHANCE":
                chance_bonuses.append({
                    "source_item": boost.get("source_item", "Unknown"),
                    "chance": float(boost.get("value", 0)),
                    "multiplier": float(boost.get("bonus_multiplier", 1)),
                })
                applied_buffs_details.append(boost)

    final_deterministic = (base * multiplicative_factor) + additive_bonus

    return {
        "base": float(base),
        "final_deterministic": float(final_deterministic),
        "chance_bonuses": chance_bonuses,
        "applied_buffs": applied_buffs_details
    }

def calculate_final_recovery_time(base_time: float, active_boosts: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o tempo de recuperação final com base nos bônus ativos.
    Filtra os bônus com base no nome do recurso e no contexto do nó.
    """
    base_recovery_time = Decimal(str(base_time))
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    for boost in active_boosts:
        conditions = boost.get("conditions", {})
        if _conditions_are_met(conditions, resource_name, node_context) and boost.get("type") == "RECOVERY_TIME":
                operation = boost["operation"]
                value = Decimal(str(boost["value"]))

                if operation == "percentage":
                    multiplicative_factor *= (Decimal('1') + value)

                applied_buffs_details.append(boost)

    final_time = base_recovery_time * multiplicative_factor

    return {
        "base": float(base_recovery_time),
        "final": float(final_time),
        "applied_buffs": applied_buffs_details
    }