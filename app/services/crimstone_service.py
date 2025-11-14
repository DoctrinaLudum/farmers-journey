# app/services/crimstone_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import (
    collectiblesItemBuffs as collectibles_domain,
    resources as resources_domain,
    skills as skills_domain,
    wearablesItemBuffs as wearables_domain,
    factions as factions_domain,
    game as game_domain
)
from . import bud_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA CRIMSTONE
# ==============================================================================

# Grupos onde apenas o bônus mais forte se aplica (ordenado do mais forte para o mais fraco)
NON_CUMULATIVE_GROUPS = {
    "time_totem": ["Super Totem", "Time Warp Totem"],
}

# Mapeamento de recursos e seus tempos de recuperação base em segundos
RESOURCE_NODE_MAP = {
    "crimstones": {"name": "Crimstone", "recovery_name": "Crimstone Rock", "base_yield": 1, "recovery_time": 24 * 3600},
}

# ==============================================================================
# FUNÇÃO DE AGREGAÇÃO DE BÔNUS (LÓGICA CENTRAL)
# ==============================================================================

def _get_player_items(farm_data: dict) -> set:
    """
    Extrai e unifica todos os itens que um jogador possui em um único conjunto.
    """
    player_items = set(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())
    
    bumpkin = farm_data.get("bumpkin", {})
    if bumpkin:
        player_items.update(bumpkin.get("equipped", {}).values())
        player_items.update(bumpkin.get("skills", {}).keys())

    player_items.update(farm_data.get("inventory", {}).keys())
    return player_items

def _get_crimstone_buffs(farm_data: dict) -> list:
    """
    Coleta e filtra todos os bônus relevantes para a mineração de Crimstone
    e recuperação de nós de Crimstone.
    """
    player_items = _get_player_items(farm_data)
    active_buffs = []

    all_item_data = {
        **skills_domain.LEGACY_BADGES,
        **skills_domain.BUMPKIN_REVAMP_SKILLS,
        **wearables_domain.WEARABLES_ITEM_BUFFS,
        **collectibles_domain.COLLECTIBLES_ITEM_BUFFS,
        **resources_domain.RESOURCES_DATA,
        **factions_domain.FACTION_ITEMS_DATA,
        **game_domain.GAME_TERMS
    }

    processed_non_cumulative = set()
    for group_name, ordered_items in NON_CUMULATIVE_GROUPS.items():
        for item_name in ordered_items:
            if item_name in player_items:
                processed_non_cumulative.update(ordered_items)
                item_details = all_item_data.get(item_name, {})
                boost_list = item_details.get("boosts", [])
                for boost in boost_list:
                    active_buffs.append({"source_item": item_name, **boost})
                break

    for item_name in player_items:
        if item_name in processed_non_cumulative:
            continue

        item_details = all_item_data.get(item_name, {})
        boost_list = item_details.get("boosts", [])
        for boost in boost_list:
            active_buffs.append({"source_item": item_name, **boost})

    crimstone_related_buffs = []
    crimstone_resource = "Crimstone"
    crimstone_recovery_resource = "Crimstone Rock"

    for buff in active_buffs:
        conditions = buff.get("conditions", {})
        resource = conditions.get("resource")
        category = conditions.get("category")

        is_yield = buff.get("type") == "YIELD" and (
            (resource and resource == crimstone_resource) or
            (category and category == "Mineral")
        )

        is_time = buff.get("type") in ["RECOVERY_TIME", "GROWTH_TIME"] and (
            (resource and resource == crimstone_recovery_resource) or
            (category and category == "Mineral")
        )

        if is_yield or is_time:
            crimstone_related_buffs.append(buff)

    bud_analysis = bud_service.analyze_bud_buffs(farm_data)
    if bud_analysis and "yield" in bud_analysis:
        if crimstone_resource in bud_analysis["yield"]:
            bud_yield_buff = bud_analysis["yield"][crimstone_resource]
            crimstone_related_buffs.append({
                "source_item": "Buds",
                "type": "YIELD",
                "operation": "add",
                "value": bud_yield_buff["total_boost"],
                "conditions": {"resource": crimstone_resource}
            })

    return crimstone_related_buffs

def _conditions_are_met(conditions: dict, resource_name: str, node_context: dict = None) -> bool:
    """
    Função auxiliar local para verificar se todas as condições de um bônus são atendidas
    para um determinado recurso e contexto de nó.
    """
    context = node_context or {}

    for condition_key, required_value in conditions.items():
        # Condição de Recurso/Item/Categoria
        if condition_key in ["resource", "item", "category"]:
            required_list = required_value if isinstance(required_value, list) else [required_value]
            if resource_name not in required_list and category != "Mineral":
                return False
        
        # Condição de Minas Restantes (para Crimstone)
        elif condition_key == "minesLeft":
            current_value = context.get("minesLeft")
            if current_value != required_value:
                return False

    return True # Todas as condições foram atendidas.

def _calculate_yield(base_yield: float, all_buffs: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o rendimento final de Crimstone com base em todos os bônus,
    de forma genérica e data-driven, interpretando as condições de cada bônus.
    """
    base = Decimal(str(base_yield))
    additive_bonus = Decimal('0')
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []
    chance_bonuses = []
    
    # Filtra apenas os bônus de rendimento
    yield_buffs = [b for b in all_buffs if b.get("type") == "YIELD"]

    for buff in yield_buffs:
        conditions = buff.get("conditions", {})
        # Verifica se as condições do bônus (incluindo 'minesLeft') são atendidas
        if _conditions_are_met(conditions, resource_name, node_context):
            operation = buff.get("operation")
            value = Decimal(str(buff.get("value", 0)))

            if operation == "add":
                additive_bonus += value
            elif operation == "multiply":
                multiplicative_factor *= value
            
            applied_buffs_details.append(buff)

    # O bônus de +2 da última picaretada é uma mecânica do jogo, não de um item,
    # então ele pode permanecer aqui, pois é uma regra fundamental de Crimstone.
    if node_context and node_context.get("minesLeft") == 1:
        additive_bonus += 2

    final_deterministic = (base * multiplicative_factor) + additive_bonus

    return {
        "base": float(base),
        "final_deterministic": float(final_deterministic),
        "chance_bonuses": chance_bonuses,
        "applied_buffs": applied_buffs_details
    }
    # Adiciona o bônus de +2 da mecânica do jogo à lista de bônus aplicados para exibição, se for o caso.
    if node_context and node_context.get("minesLeft") == 1:
        result["applied_buffs"].append({
            "source_item": "Bônus da Última Picaretada", "type": "YIELD",
            "operation": "add", "value": 2, "source_type": "game_mechanic"
        })

    return result

def _calculate_recovery_time(base_time: float, all_buffs: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o tempo final de recuperação do nó de Crimstone com base em todos os bônus.
    """
    base_recovery_time = Decimal(str(base_time))
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    time_buffs = [b for b in all_buffs if b.get("type") in ["RECOVERY_TIME", "GROWTH_TIME"] and (not b.get("conditions") or b.get("conditions", {}).get("resource") == resource_name or b.get("conditions", {}).get("category") == "Mineral")]
    
    for buff in time_buffs:
        conditions = buff.get("conditions", {})
        if _conditions_are_met(conditions, resource_name, node_context):
            operation = buff.get("operation")
            value = Decimal(str(buff.get("value", 0)))

            if operation == "percentage":
                multiplicative_factor *= (Decimal('1') + value)
            elif operation == "multiply":
                multiplicative_factor *= value
            
            applied_buffs_details.append(buff)

    final_time = base_recovery_time * multiplicative_factor

    return {
        "base": float(base_recovery_time),
        "final": float(final_time),
        "applied_buffs": applied_buffs_details
    }

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_crimstone_resources(farm_data: dict) -> dict:
    """
    Analisa todos os recursos de Crimstone, calcula bônus e retorna um relatório completo.
    """
    start_time = time.time()

    all_player_buffs = _get_crimstone_buffs(farm_data)
    active_item_names = sorted(list(set(b['source_item'] for b in all_player_buffs)))

    analyzed_nodes_by_type = defaultdict(dict)
    summary_by_type = defaultdict(lambda: {"total": 0, "ready": 0, "recovering": 0, "total_yield": Decimal('0')})
    critical_hit_stats = defaultdict(int)
    current_timestamp_ms = int(time.time() * 1000)

    for api_key, node_info in RESOURCE_NODE_MAP.items():
        nodes_api_data = farm_data.get(api_key, {})
        resource_name = node_info["name"]
        recovery_name = node_info["recovery_name"]
        base_yield = node_info["base_yield"]
        base_recovery_time = node_info["recovery_time"]

        player_wide_recovery_info = _calculate_recovery_time(base_recovery_time, all_player_buffs, recovery_name)
        summary_by_type[resource_name]['final_recovery_time'] = player_wide_recovery_info.get('final', base_recovery_time)

        for node_id, node_data in nodes_api_data.items():
            summary_by_type[resource_name]["total"] += 1

            current_base_yield = base_yield
            node_context = {}
            
            stone_details = node_data.get("stone", {})
            mined_at_ms = stone_details.get("minedAt", 0)
            critical_hits = stone_details.get("criticalHit", {})
            for hit_name, hit_count in critical_hits.items():
                if hit_count > 0:
                    critical_hit_stats[hit_name] += hit_count

            # Lógica de minesLeft para Crimstone
            current_mines_left = node_data.get("minesLeft", 0)
            node_context["minesLeft"] = current_mines_left

            # Lógica de reset para Crimstone se não for minerada por muito tempo
            # Conforme mineCrimstone.ts (base_recovery_time + 24 * 3600)
            crimstone_reset_at_ms = None
            if mined_at_ms > 0:
                time_since_mined_ms = current_timestamp_ms - mined_at_ms
                time_to_reset_ms = (base_recovery_time + 24 * 3600) * 1000
                
                if time_since_mined_ms > time_to_reset_ms:
                    node_context["minesLeft"] = 5 # Reseta para o valor máximo
                else:
                    crimstone_reset_at_ms = mined_at_ms + time_to_reset_ms

            node_specific_boosts = list(all_player_buffs)

            for hit_name, hit_count in critical_hits.items():
                if hit_count > 0:
                    item_details = {**collectibles_domain.COLLECTIBLES_ITEM_BUFFS, **skills_domain.BUMPKIN_REVAMP_SKILLS, **wearables_domain.WEARABLES_ITEM_BUFFS}.get(hit_name, {})
                    for boost in item_details.get("boosts", []):
                        if boost.get("type") == "YIELD":
                            source_item_text = "(Critical Hit)" if hit_name == "Native" else f"{hit_name} (Critical Hit)"
                            node_specific_boosts.append({
                                "type": "YIELD", "operation": boost["operation"], 
                                "value": boost["value"], "source_item": source_item_text,
                                "source_type": "critical_hit"
                            })

            yield_info = _calculate_yield(current_base_yield, node_specific_boosts, resource_name, node_context)
            summary_by_type[resource_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

            recovery_info = _calculate_recovery_time(base_recovery_time, all_player_buffs, recovery_name, node_context)
            final_recovery_ms = recovery_info["final"] * 1000

            is_ready = not mined_at_ms or current_timestamp_ms >= (mined_at_ms + final_recovery_ms)
            state_name = "Pronto" if is_ready else "Recuperando"
            summary_by_type[resource_name]["ready" if is_ready else "recovering"] += 1
            ready_at_ms = mined_at_ms + final_recovery_ms if not is_ready else current_timestamp_ms

            analyzed_node = {
                "id": node_id, "state_name": state_name,
                "ready_at_timestamp_ms": int(ready_at_ms),
                "calculations": {"yield": yield_info, "recovery": recovery_info}, "has_aoe_buff": False,
                "critical_hits": critical_hits,
                "mines_left": node_context["minesLeft"]
            }
            if crimstone_reset_at_ms:
                analyzed_node["crimstone_reset_at_ms"] = int(crimstone_reset_at_ms)
            
            analyzed_nodes_by_type[resource_name][node_id] = analyzed_node

    end_time = time.time()
    log.info(f"Análise de Crimstone concluída em {end_time - start_time:.4f} segundos.")

    for resource_type in analyzed_nodes_by_type:
        analyzed_nodes_by_type[resource_type] = dict(sorted(analyzed_nodes_by_type[resource_type].items()))

    view_data = {
        "summary_by_type": dict(sorted(summary_by_type.items())),
        "nodes_by_type": dict(sorted(analyzed_nodes_by_type.items())),
        "critical_hit_stats": dict(sorted(critical_hit_stats.items())),
        "active_boost_items": active_item_names,
    }

    return {"view": view_data}
