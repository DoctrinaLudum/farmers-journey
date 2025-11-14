# app/services/sunstone_service.py

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
# CONSTANTES DE REGRAS DE NEGÓCIO PARA SUNSTONE
# ==============================================================================

# Grupos onde apenas o bônus mais forte se aplica (ordenado do mais forte para o mais fraco)
NON_CUMULATIVE_GROUPS = {
    "time_totem": ["Super Totem", "Time Warp Totem"],
}

# Mapeamento de recursos e seus tempos de recuperação base em segundos
RESOURCE_NODE_MAP = {
    "sunstones": {"name": "Sunstone", "recovery_name": "Sunstone Rock", "base_yield": 1, "recovery_time": 72 * 3600},
}

# ==============================================================================
# FUNÇÃO DE AGREGAÇÃO DE BÔNUS (LÓGICA CENTRAL)
# ==============================================================================

def _get_player_items(farm_data: dict) -> set:
    # Esta função é genérica e pode permanecer, mas seus resultados não serão usados para buffs de Sunstone.
    return set() # Retorna vazio para indicar que não há itens relevantes para buffs de Sunstone

def _get_sunstone_buffs(farm_data: dict) -> list:
    """
    Coleta e filtra todos os bônus relevantes para a mineração de Sunstone
    e recuperação de nós de Sunstone.
    Baseado em mineSunstone.ts, Sunstone não recebe buffs de yield ou recovery time.
    """
    return [] # Retorna uma lista vazia, pois não há buffs aplicados no TS.

def _calculate_yield(base_yield: float, all_buffs: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o rendimento final de Sunstone com base em todos os bônus.
    Baseado em mineSunstone.ts, o rendimento é sempre o base_yield (1).
    """
    return {
        "base": float(base_yield),
        "final_deterministic": float(base_yield),
        "chance_bonuses": [],
        "applied_buffs": []
    }

def _calculate_recovery_time(base_time: float, all_buffs: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o tempo final de recuperação do nó de Sunstone com base em todos os bônus.
    Baseado em mineSunstone.ts, o tempo de recuperação é o base_time sem buffs.
    """
    return {
        "base": float(base_time),
        "final": float(base_time),
        "applied_buffs": []
    }

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_sunstone_resources(farm_data: dict) -> dict:
    """
    Analisa todos os recursos de Sunstone, calcula bônus e retorna um relatório completo.
    """
    start_time = time.time()

    all_player_buffs = [] # mineSunstone.ts não aplica buffs
    active_item_names = [] # Nenhuma buff ativa

    analyzed_nodes_by_type = defaultdict(dict)
    summary_by_type = defaultdict(lambda: {"total": 0, "ready": 0, "recovering": 0, "total_yield": Decimal('0')})
    critical_hit_stats = defaultdict(int) # mineSunstone.ts não tem critical hits
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
            critical_hits = {} # mineSunstone.ts não tem critical hits

            # Lógica de minesLeft para Sunstone
            current_mines_left = node_data.get("minesLeft", 0)
            node_context["minesLeft"] = current_mines_left

            node_specific_boosts = [] # Nenhuma buff para Sunstone

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
            
            analyzed_nodes_by_type[resource_name][node_id] = analyzed_node

    end_time = time.time()
    log.info(f"Análise de Sunstone concluída em {end_time - start_time:.4f} segundos.")

    for resource_type in analyzed_nodes_by_type:
        analyzed_nodes_by_type[resource_type] = dict(sorted(analyzed_nodes_by_type[resource_type].items()))

    view_data = {
        "summary_by_type": dict(sorted(summary_by_type.items())),
        "nodes_by_type": dict(sorted(analyzed_nodes_by_type.items())),
        "critical_hit_stats": dict(sorted(critical_hit_stats.items())), # Será vazio
        "active_boost_items": active_item_names, # Será vazio
    }

    return {"view": view_data}
