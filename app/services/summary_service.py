# app/services/summary_service.py

import logging
import time
from decimal import Decimal

# Importa os domínios de dados necessários
from ..domain import (
    crops as crops_domain,
    fruits as fruits_domain,
    seeds as seeds_domain,
    collectiblesItemBuffs as collectibles_domain,  # Corrected import
    resources as resources_domain,
    skills as skills_domain,
    tools as tools_domain,
    wearablesItemBuffs as wearables_domain  # Corrected import
)
# Importa as funções de análise genéricas do serviço de análise de recursos
from . import resource_analysis_service as ras

log = logging.getLogger(__name__)

def _format_seconds_to_hhmmss(total_seconds):
    if not isinstance(total_seconds, (int, float, Decimal)) or total_seconds < 0:
        return "00:00:00"
    
    total_seconds = int(total_seconds)
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def _get_source_type(source_item_name: str) -> str:
    if source_item_name == "Native":
        return "game_mechanic"
    if source_item_name in skills_domain.BUMPKIN_REVAMP_SKILLS:
        return "skill"
    if source_item_name in collectibles_domain.COLLECTIBLES_ITEM_BUFFS: # Corrected usage
        return "collectible"
    if source_item_name in wearables_domain.WEARABLES_ITEM_BUFFS:     # Corrected usage
        return "wearable"
    if source_item_name.startswith("Bud #"): # Check if it's a bud from bud_service
        return "bud"
    return "unknown"

def _format_buffs(buff_list):
    """Formata uma lista de dicionários de bônus para um formato simplificado."""
    if not buff_list:
        return []
    
    formatted = []
    for buff in buff_list:
        # Para bônus de chance crítica, o valor relevante é a própria chance
        if buff.get("type") == "CRITICAL_CHANCE":
            value = buff.get("value", 0)
        # Para bônus de rendimento, pode ser um valor aditivo ou multiplicativo
        else:
            value = buff.get("value", 0)

        # Determine the formatted value based on operation type
        formatted_value = ""
        operation = buff.get("operation", "add")
        value_float = float(value)

        if operation == "add":
            formatted_value = f"{'+' if value_float >= 0 else ''}{value_float:.2f}"
        elif operation == "subtract":
            formatted_value = f"{-value_float:.2f}" # Display as negative if subtracting a positive value
        elif operation == "percentage":
            formatted_value = f"{value_float:.2f}%"
        elif operation == "multiply":
            formatted_value = f"x{value_float:.2f}"
        else:
            formatted_value = f"{value_float:.2f}" # Fallback

        formatted.append({
            "source_item": buff.get("source_item", "Unknown"),
            "source_type": _get_source_type(buff.get("source_item", "Unknown")),
            "value": formatted_value
        })
    return formatted

def analyze_resources_summary(farm_data: dict) -> dict:
    """
    Cria um sumário de análise para recursos básicos (Wood, Stone, etc.),
    calculando o rendimento mínimo e médio, custo e tempo de ciclo com base
    nos bônus do jogador.
    """
    categorized_summary = {}
    player_items = ras._get_player_items(farm_data)

    # Análise de Recursos
    for resource_name, resource_info in resources_domain.RESOURCES_DATA.items():
        if not resource_info or not resource_info.get("enabled"):
            continue

        resource_type = resource_info.get("type")
        if not resource_type:
            continue

        source_node = resource_info.get("source")
        if not source_node or not resource_info.get("details", {}).get("cycle"):
            continue

        base_details = resource_info.get("details", {}).get("cycle", {}).get(source_node, {})
        base_yield = Decimal(str(base_details.get("yield_amount", 1)))
        base_recovery_time = Decimal(str(base_details.get("recovery_time_seconds", 0)))
        tool_name = resource_info.get("tool_required")

        resource_conditions = {
            'yield_resource_names': [resource_name],
            'recovery_resource_names': [source_node],
            'skill_tree_name': resource_info.get("skill_tree"),
            'boost_category_names': resource_info.get("boost_categories", [])
        }
        boost_catalogue = ras.filter_boosts_from_domains(resource_conditions)
        active_boosts = ras.get_active_player_boosts(player_items, boost_catalogue, farm_data=farm_data)

        min_yield_calc = ras.calculate_final_yield(float(base_yield), active_boosts, resource_name)
        min_yield = Decimal(str(min_yield_calc['final_deterministic']))

        all_potential_yield_boosts = list(active_boosts)
        crit_chance_boosts = []

        native_skill_data = skills_domain.BUMPKIN_REVAMP_SKILLS.get("Native")
        if native_skill_data:
            for boost in native_skill_data.get("effects", []):
                if ras._conditions_are_met(boost.get("conditions", {}), resource_name, {}):
                    if boost.get("type") == "YIELD":
                        all_potential_yield_boosts.append({"source_item": "Native (Critical)", "operation": "add", **boost})
                    elif boost.get("type") == "CRITICAL_CHANCE":
                        crit_chance_boosts.append({"source_item": "Native", "operation": "add", **boost})

        for item_name in player_items:
            if item_name in boost_catalogue:
                item_boosts = boost_catalogue[item_name].get("boosts", [])
                for boost in item_boosts:
                    if "type" in boost and "operation" in boost:
                        if boost.get("type") == "YIELD":
                            all_potential_yield_boosts.append({"source_item": item_name, **boost})
                        elif boost.get("type") == "CRITICAL_CHANCE":
                            crit_chance_boosts.append({"source_item": item_name, **boost})

        max_yield_calc = ras.calculate_final_yield(float(base_yield), all_potential_yield_boosts, resource_name)
        max_yield = Decimal(str(max_yield_calc['final_deterministic']))

        total_crit_chance = sum(Decimal(str(b.get("value", 0))) for b in crit_chance_boosts)
        total_crit_chance = min(total_crit_chance, Decimal('1'))

        avg_yield = (min_yield * (Decimal('1') - total_crit_chance)) + (max_yield * total_crit_chance)

        cycle_calc = ras.calculate_final_recovery_time(float(base_recovery_time), active_boosts, resource_name)
        final_cycle_seconds = int(cycle_calc['final'])

        tool_cost = Decimal('0')
        tool_buffs = []
        if tool_name:
            tool_info = tools_domain.TOOLS_DATA.get(tool_name)
            if tool_info:
                base_tool_cost = Decimal(str(tool_info.get("price", 0)))
                cost_reduction_factor = Decimal('1')
                for boost in active_boosts:
                    if boost.get("type") == "SALE_PRICE" and boost.get("conditions", {}).get("item") == tool_name:
                        cost_reduction_factor *= (Decimal('1') + Decimal(str(boost.get("value", 0))))
                        tool_buffs.append(boost)
                tool_cost = base_tool_cost * cost_reduction_factor

        resource_summary_data = {
            "min": f"{float(min_yield):.2f}",
            "avg": f"{float(avg_yield):.2f}",
            "max": f"{float(max_yield):.2f}",
            "tool_cost": f"{float(tool_cost):.2f}",
            "cycle": _format_seconds_to_hhmmss(final_cycle_seconds),
            "buffs_aplicados": {
                "yield_buffs": _format_buffs(min_yield_calc['applied_buffs'] + crit_chance_boosts),
                "recovery_buffs": _format_buffs(cycle_calc['applied_buffs']),
                "tools_buff": _format_buffs(tool_buffs)
            }
        }
        
        if resource_type not in categorized_summary:
            categorized_summary[resource_type] = {}
        categorized_summary[resource_type][resource_name.lower()] = resource_summary_data

    # Análise de Plantações (Crops)
    for crop_name, crop_info in crops_domain.CROPS.items():
        if not crop_info or not crop_info.get("enabled") or crop_info.get("type") != "Crop":
            continue

        base_yield = Decimal('1')
        base_recovery_time = Decimal(str(crop_info.get("harvestSeconds", 0)))
        seed_name = f"{crop_name} Seed"
        seed_info = seeds_domain.SEEDS_DATA.get(seed_name, {})
        tool_cost = Decimal(str(seed_info.get("cost_coins", 0)))

        resource_conditions = {
            'yield_resource_names': [crop_name],
            'recovery_resource_names': [crop_name],
            'skill_tree_name': "Crops",
            'boost_category_names': ["Crop"]
        }
        boost_catalogue = ras.filter_boosts_from_domains(resource_conditions)
        active_boosts = ras.get_active_player_boosts(player_items, boost_catalogue, farm_data=farm_data)

        min_yield_calc = ras.calculate_final_yield(float(base_yield), active_boosts, crop_name)
        min_yield = Decimal(str(min_yield_calc['final_deterministic']))

        all_potential_yield_boosts = list(active_boosts)
        crit_chance_boosts = []

        max_yield_calc = ras.calculate_final_yield(float(base_yield), all_potential_yield_boosts, crop_name)
        max_yield = Decimal(str(max_yield_calc['final_deterministic']))

        total_crit_chance = sum(Decimal(str(b.get("value", 0))) for b in crit_chance_boosts)
        total_crit_chance = min(total_crit_chance, Decimal('1'))

        avg_yield = (min_yield * (Decimal('1') - total_crit_chance)) + (max_yield * total_crit_chance)

        cycle_calc = ras.calculate_final_recovery_time(float(base_recovery_time), active_boosts, crop_name)
        final_cycle_seconds = int(cycle_calc['final'])

        crop_summary_data = {
            "min": f"{float(min_yield):.2f}",
            "avg": f"{float(avg_yield):.2f}",
            "max": f"{float(max_yield):.2f}",
            "tool_cost": f"{float(tool_cost):.2f}",
            "cycle": _format_seconds_to_hhmmss(final_cycle_seconds),
            "buffs_aplicados": {
                "yield_buffs": _format_buffs(min_yield_calc['applied_buffs'] + crit_chance_boosts),
                "recovery_buffs": _format_buffs(cycle_calc['applied_buffs']),
                "tools_buff": []
            }
        }

        if "Crop" not in categorized_summary:
            categorized_summary["Crop"] = {}
        categorized_summary["Crop"][crop_name.lower()] = crop_summary_data

    # Análise de Frutas
    for fruit_name, fruit_info in fruits_domain.FRUIT_DATA.items():
        if not fruit_info or fruit_info.get("type") != "Fruit":
            continue

        base_yield = Decimal('1')
        base_recovery_time = Decimal(str(fruit_info.get("plant_seconds", 0)))
        tool_cost = Decimal(str(fruit_info.get("seed_price", 0)))

        resource_conditions = {
            'yield_resource_names': [fruit_name],
            'recovery_resource_names': [fruit_name],
            'skill_tree_name': "Fruits",
            'boost_category_names': ["Fruit"]
        }
        boost_catalogue = ras.filter_boosts_from_domains(resource_conditions)
        active_boosts = ras.get_active_player_boosts(player_items, boost_catalogue, farm_data=farm_data)

        min_yield_calc = ras.calculate_final_yield(float(base_yield), active_boosts, fruit_name)
        min_yield = Decimal(str(min_yield_calc['final_deterministic']))

        all_potential_yield_boosts = list(active_boosts)
        crit_chance_boosts = []

        max_yield_calc = ras.calculate_final_yield(float(base_yield), all_potential_yield_boosts, fruit_name)
        max_yield = Decimal(str(max_yield_calc['final_deterministic']))

        total_crit_chance = sum(Decimal(str(b.get("value", 0))) for b in crit_chance_boosts)
        total_crit_chance = min(total_crit_chance, Decimal('1'))

        avg_yield = (min_yield * (Decimal('1') - total_crit_chance)) + (max_yield * total_crit_chance)

        cycle_calc = ras.calculate_final_recovery_time(float(base_recovery_time), active_boosts, fruit_name)
        final_cycle_seconds = int(cycle_calc['final'])

        fruit_summary_data = {
            "min": f"{float(min_yield):.2f}",
            "avg": f"{float(avg_yield):.2f}",
            "max": f"{float(max_yield):.2f}",
            "tool_cost": f"{float(tool_cost):.2f}",
            "cycle": _format_seconds_to_hhmmss(final_cycle_seconds),
            "buffs_aplicados": {
                "yield_buffs": _format_buffs(min_yield_calc['applied_buffs'] + crit_chance_boosts),
                "recovery_buffs": _format_buffs(cycle_calc['applied_buffs']),
                "tools_buff": []
            }
        }

        if "Fruit" not in categorized_summary:
            categorized_summary["Fruit"] = {}
        categorized_summary["Fruit"][fruit_name.lower()] = fruit_summary_data

    return categorized_summary