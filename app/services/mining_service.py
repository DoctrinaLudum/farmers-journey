# app/services/mining_service.py

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
# CONSTANTES DE REGRAS DE NEGÓCIO PARA MINERAÇÃO
# ==============================================================================

# Grupos onde apenas o bônus mais forte se aplica (ordenado do mais forte para o mais fraco)
NON_CUMULATIVE_GROUPS = {
    "time_totem": ["Super Totem", "Time Warp Totem"],
    "mole": ["Rocky the Mole", "Tunnel Mole"],
}

# Mapeamento de recursos e seus tempos de recuperação base em segundos
RESOURCE_NODE_MAP = {
    "stones": {"name": "Stone", "recovery_name": "Stone Rock", "base_yield": 1, "recovery_time": 4 * 3600},
    "iron": {"name": "Iron", "recovery_name": "Iron Rock", "base_yield": 1, "recovery_time": 8 * 3600},
    "gold": {"name": "Gold", "recovery_name": "Gold Rock", "base_yield": 1, "recovery_time": 24 * 3600},
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

def _get_mining_buffs(farm_data: dict) -> list:
    """
    Coleta e filtra todos os bônus relevantes para a mineração (Stone, Iron, Gold)
    e recuperação de nós de mineração, espelhando a lógica do `chop_service`.

    Args:
        farm_data (dict): O estado completo da fazenda do jogador.

    Returns:
        list: Uma lista de dicionários de bônus ativos e relevantes para mineração.
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
    player_faction = farm_data.get("faction", {}).get("name")

    # Processa grupos não cumulativos
    processed_non_cumulative = set()
    for group_name, ordered_items in NON_CUMULATIVE_GROUPS.items():
        for item_name in ordered_items:
            if item_name in player_items:
                processed_non_cumulative.update(ordered_items)
                item_details = all_item_data.get(item_name, {})
                boost_list = item_details.get("boosts", []) + item_details.get("effects", [])
                for boost in boost_list:
                    active_buffs.append({"source_item": item_name, **boost})
                break

    # Processa itens cumulativos
    for item_name in player_items:
        if item_name in processed_non_cumulative:
            continue

        item_details = all_item_data.get(item_name, {})
        boost_list = item_details.get("boosts", []) + item_details.get("effects", [])
        for boost in boost_list:
            active_buffs.append({"source_item": item_name, **boost})

    # Filtra buffs que afetam 'Stone', 'Iron', 'Gold' ou 'Mineral'
    mining_related_buffs = []
    mining_resources = {"Stone", "Iron", "Gold"}
    mining_recovery_resources = {"Stone Rock", "Iron Rock", "Gold Rock"}

    for buff in active_buffs:
        conditions = buff.get("conditions", {})
        resource = conditions.get("resource")
        category = conditions.get("category")

        # Validação de facção
        required_faction = conditions.get("faction")
        if required_faction and required_faction != player_faction:
            continue

        # Lógica data-driven para ignorar bônus de YIELD de itens de crítico
        source_item_name = buff.get("source_item")
        if source_item_name:
            item_details = all_item_data.get(source_item_name, {})
            item_boosts = item_details.get("boosts", []) + item_details.get("effects", [])
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)
            if is_critical_item and buff.get("type") == "YIELD":
                continue

        is_yield = buff.get("type") == "YIELD" and (
            (isinstance(resource, str) and resource in mining_resources) or
            (isinstance(resource, list) and any(r in mining_resources for r in resource)) or
            (category and category == "Mineral") or
            (not resource and not category) # Bônus genérico
        )

        is_time = buff.get("type") in ["RECOVERY_TIME", "GROWTH_TIME"] and (
            (isinstance(resource, str) and resource in mining_recovery_resources) or
            (isinstance(resource, list) and any(r in mining_recovery_resources for r in resource)) or
            (category and category == "Mineral") or
            (not resource and not category) # Bônus genérico
        )

        if is_yield or is_time:
            mining_related_buffs.append(buff)

    # Adiciona buffs de Bud
    bud_analysis = bud_service.analyze_bud_buffs(farm_data)
    if bud_analysis:
        for resource in mining_resources:
            if resource in bud_analysis.get("yield", {}):
                bud_yield_buff = bud_analysis["yield"][resource]
                mining_related_buffs.append({
                    "source_item": "Buds",
                    "type": "YIELD",
                    "operation": "add",
                    "value": bud_yield_buff["total_boost"],
                    "conditions": {"resource": resource}
                })

    return mining_related_buffs

def _calculate_yield(base_yield: float, all_buffs: list, resource_name: str, critical_hits: dict, all_item_data: dict, node_context: dict = None) -> dict:
    """
    Calcula o rendimento final de um recurso mineral com base em todos os bônus.
    """
    base = Decimal(str(base_yield))
    additive_bonus = Decimal('0')
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    # Filtra apenas os buffs de yield para o recurso específico
    yield_buffs = [b for b in all_buffs if b.get("type") == "YIELD"]

    for buff in yield_buffs:
        conditions = buff.get("conditions", {})
        resource_in_cond = conditions.get("resource")
        category_in_cond = conditions.get("category")

        is_relevant = (
            (resource_in_cond and (resource_name == resource_in_cond or (isinstance(resource_in_cond, list) and resource_name in resource_in_cond))) or
            (category_in_cond and category_in_cond == "Mineral") or
            (not resource_in_cond and not category_in_cond) # Bônus genérico
        )

        if is_relevant:
            operation = buff.get("operation")
            value = Decimal(str(buff.get("value", 0)))

            if operation == "add":
                additive_bonus += value
            elif operation == "multiply":
                multiplicative_factor *= value
            
            applied_buffs_details.append(buff)

    final_yield = (base * multiplicative_factor) + additive_bonus

    # Adiciona bônus de rendimento com base no tier da rocha, conforme os arquivos .ts
    if node_context and node_context.get("tier"):
        rock_tier = node_context.get("tier")
        if rock_tier == 2:
            final_yield += Decimal('0.5')
            applied_buffs_details.append({"source_item": f"Tier 2 Rock", "type": "YIELD", "operation": "add", "value": 0.5, "source_type": "game_mechanic"})
        elif rock_tier == 3:
            final_yield += Decimal('2.5')
            applied_buffs_details.append({"source_item": f"Tier 3 Rock", "type": "YIELD", "operation": "add", "value": 2.5, "source_type": "game_mechanic"})

    # Aplica bônus de acerto crítico, se ocorreram
    if critical_hits:
        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0 and hit_name in all_item_data:
                crit_boost_info = next((b for b in (all_item_data[hit_name].get("boosts", []) + all_item_data[hit_name].get("effects", [])) if b.get("type") == "YIELD"), None)
                if crit_boost_info:
                    operation = crit_boost_info.get("operation")
                    value = Decimal(str(crit_boost_info.get("value", 0)))

                    if operation == "add":
                        final_yield += value
                    elif operation == "multiply":
                        final_yield *= value
                    
                    crit_boost_info['source_item'] = f"{hit_name} (Critical Hit)"
                    applied_buffs_details.append(crit_boost_info)

    return {
        "base": float(base),
        "final": float(final_yield),
        "applied_buffs": applied_buffs_details
    }

def _calculate_recovery_time(base_time: float, all_buffs: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o tempo final de recuperação do nó mineral com base em todos os bônus.
    """
    base_recovery_time = Decimal(str(base_time))
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    time_buffs = [b for b in all_buffs if b.get("type") in ["RECOVERY_TIME", "GROWTH_TIME"]]

    for buff in time_buffs:
        conditions = buff.get("conditions", {})
        resource_in_cond = conditions.get("resource")
        category_in_cond = conditions.get("category")

        is_relevant = (
            (resource_in_cond and (resource_name == resource_in_cond or (isinstance(resource_in_cond, list) and resource_name in resource_in_cond))) or
            (category_in_cond and category_in_cond == "Mineral") or
            (not resource_in_cond and not category_in_cond) # Bônus genérico
        )

        if is_relevant:
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

def analyze_mining_resources(farm_data: dict) -> dict:
    """
    Analisa todos os recursos de mineração, calcula bônus e retorna um relatório completo.
    """
    start_time = time.time()

    # 1. Coleta todos os bônus do jogador de uma só vez, filtrados para mineração.
    all_player_buffs = _get_mining_buffs(farm_data)

    # Catálogo de itens para consulta de bônus de crítico
    all_item_data_for_crit = {
        **skills_domain.LEGACY_BADGES,
        **skills_domain.BUMPKIN_REVAMP_SKILLS,
        **wearables_domain.WEARABLES_ITEM_BUFFS,
        **collectibles_domain.COLLECTIBLES_ITEM_BUFFS,
        **factions_domain.FACTION_ITEMS_DATA,
    }

    # Extrai nomes de itens ativos para a UI
    active_item_names = sorted(list(set(b['source_item'] for b in all_player_buffs)))

    analyzed_nodes_by_type = defaultdict(dict)
    summary_by_type = defaultdict(lambda: {"total": 0, "ready": 0, "recovering": 0, "total_yield": Decimal('0')})
    critical_hit_stats = defaultdict(int)
    current_timestamp_ms = int(time.time() * 1000)

    for api_key, node_info in RESOURCE_NODE_MAP.items():
        nodes_api_data = farm_data.get(api_key, {})
        resource_name = node_info["name"] # This is the resource produced, e.g., "Stone"
        recovery_name = node_info["recovery_name"] # This is the node name for recovery time, e.g., "Stone Rock"
        base_yield = node_info["base_yield"]
        base_recovery_time = node_info["recovery_time"]

        # Calcula o tempo de recuperação com todos os bônus do jogador (sem AOE)
        player_wide_recovery_info = _calculate_recovery_time(base_recovery_time, all_player_buffs, recovery_name)
        summary_by_type[resource_name]['final_recovery_time'] = player_wide_recovery_info.get('final', base_recovery_time)

        for node_id, node_data in nodes_api_data.items():
            summary_by_type[resource_name]["total"] += 1

            current_base_yield = base_yield
            node_context = {}
            node_context["tier"] = node_data.get("tier") # Adiciona o tier ao contexto
            
            stone_details = node_data.get("stone", {})
            mined_at_ms = stone_details.get("minedAt", 0)
            critical_hits = stone_details.get("criticalHit", {})
            for hit_name, hit_count in critical_hits.items():
                if hit_count > 0:
                    critical_hit_stats[hit_name] += hit_count

            # A lógica de AOE pode ser adicionada aqui se necessário no futuro

            yield_info = _calculate_yield(current_base_yield, all_player_buffs, resource_name, critical_hits, all_item_data_for_crit, node_context)
            summary_by_type[resource_name]['total_yield'] += Decimal(str(yield_info['final']))

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
                "critical_hits": critical_hits
            }            

            analyzed_nodes_by_type[resource_name][node_id] = analyzed_node

    end_time = time.time()
    log.info(f"Análise de mineração concluída em {end_time - start_time:.4f} segundos.")

    # Ordena os nós dentro de cada tipo
    for resource_type in analyzed_nodes_by_type:
        analyzed_nodes_by_type[resource_type] = dict(sorted(analyzed_nodes_by_type[resource_type].items()))

    # Converte o defaultdict para um dict normal para o JSON
    summary_by_type_final = {k: {**v, 'total_yield': float(v['total_yield'])} for k, v in summary_by_type.items()}

    view_data = {
        "summary_by_type": dict(sorted(summary_by_type_final.items())),
        "nodes_by_type": dict(sorted(analyzed_nodes_by_type.items())),
        "critical_hit_stats": dict(sorted(critical_hit_stats.items())),
        "active_boost_items": active_item_names,
    }

    return {"view": view_data}