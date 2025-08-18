# app/services/mining_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import resources as resources_domain
from ..domain import skills as skills_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA MINERAÇÃO
# ==============================================================================

MINING_RESOURCE_CONDITIONS = {
    'yield_resource_names': ['Stone', 'Iron', 'Gold', 'Crimstone', 'Sunstone', 'Obsidian', 'Oil'],
    'recovery_resource_names': ['Stone Rock', 'Iron Rock', 'Gold Rock', 'Crimstone Rock', 'Sunstone Rock', 'Lava Pit', 'Oil Reserve'],
    'boost_category_names': ['Mineral', 'Resource']
}

NON_CUMULATIVE_BOOST_GROUPS = {
    "midas_recovery": [],
}

BUD_BUFF_TO_MINING_BOOST_MAPPING = {
    'STONE_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'resource': 'Stone'}},
    'IRON_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'resource': 'Iron'}},
    'GOLD_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'resource': 'Gold'}},
    'CRIMSTONE_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'resource': 'Crimstone'}},
    'SUNSTONE_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'resource': 'Sunstone'}},
    'OIL_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'resource': 'Oil'}},
    'MINERAL_RECOVERY_TIME': {'type': 'RECOVERY_TIME', 'operation': 'percentage', 'conditions': {'category': 'Mineral'}},
    'MINERAL_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'category': 'Mineral'}},
}

MINING_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(MINING_RESOURCE_CONDITIONS)

RESOURCE_NODE_MAP = {
    "stones": {"name": "Stone", "recovery_name": "Stone Rock", "base_yield": 1, "recovery_time": 4 * 3600},
    "iron": {"name": "Iron", "recovery_name": "Iron Rock", "base_yield": 1, "recovery_time": 8 * 3600},
    "gold": {"name": "Gold", "recovery_name": "Gold Rock", "base_yield": 1, "recovery_time": 24 * 3600},
    "crimstones": {"name": "Crimstone", "recovery_name": "Crimstone Rock", "base_yield": 1, "recovery_time": 24 * 3600, "special_logic": "minesLeft"},
    "sunstones": {"name": "Sunstone", "recovery_name": "Sunstone Rock", "base_yield": 1, "recovery_time": 72 * 3600, "special_logic": "minesLeft"},
    "lavaPits": {"name": "Obsidian", "recovery_name": "Lava Pit", "base_yield": 1, "recovery_time": 72 * 3600, "special_logic": "lavaPit"}, # Obsidian yield is handled in its own file
    "oilReserves": {"name": "Oil", "recovery_name": "Oil Reserve", "base_yield": 10, "recovery_time": 20 * 3600, "special_logic": "oilReserve"},
}

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _calculate_yield(base_yield: float, active_boosts: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o rendimento de um recurso mineral, espelhando a lógica dos arquivos .ts.
    """
    return resource_analysis_service.calculate_final_yield(base_yield, active_boosts, resource_name, node_context)

def _calculate_recovery_time(base_time: float, active_boosts: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o tempo de recuperação de um nó mineral, espelhando a lógica dos arquivos .ts.
    """
    return resource_analysis_service.calculate_final_recovery_time(base_time, active_boosts, resource_name, node_context)

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_mining_resources(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todos os recursos de mineração, calcula bônus e retorna um relatório completo.
    """
    player_items = resource_analysis_service._get_player_items(farm_data)

    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        MINING_BOOST_CATALOGUE,
        NON_CUMULATIVE_BOOST_GROUPS,
        farm_data
    )

    active_item_names = {item for item in player_items if item in MINING_BOOST_CATALOGUE}
    if active_bud_buffs:
        active_item_names.add("Buds")

    if active_bud_buffs:
        for bud_buff_name, mapping in BUD_BUFF_TO_MINING_BOOST_MAPPING.items():
            if bud_buff_name in active_bud_buffs and active_bud_buffs[bud_buff_name] != 0:
                boost = mapping.copy()
                boost["source_item"] = "Buds"
                boost["value"] = active_bud_buffs[bud_buff_name]
                boost["source_type"] = "bud"
                active_boosts.append(boost)

    temporal_boosts, active_boosts, temporal_item_names = resource_analysis_service.extract_and_process_temporal_boosts(
        active_boosts, farm_data
    )
    active_item_names.update(temporal_item_names)

    processed_temporal_boosts = []
    if temporal_boosts:
        now_ts = int(time.time() * 1000)
        latest_expirations = defaultdict(int)
        for temp_boost_info in temporal_boosts:
            boost = temp_boost_info['boost']
            item_name = boost['source_item']
            activation_ts = temp_boost_info['activation_ts']
            conditions = boost.get("conditions", {})
            duration_hours = conditions.get("duration_hours", 0)
            duration_ms = (duration_hours * 60 * 60 * 1000)
            expires_at_ts = activation_ts + duration_ms
            if now_ts < expires_at_ts and expires_at_ts > latest_expirations[item_name]:
                latest_expirations[item_name] = expires_at_ts
        
        for name, expires_at in latest_expirations.items():
            processed_temporal_boosts.append({'name': name, 'expires_at_ms': expires_at})
        processed_temporal_boosts.sort(key=lambda x: x['name'])

    min_max_yield_analysis = resource_analysis_service.analyze_player_min_max_yields(
        player_items, active_boosts, MINING_BOOST_CATALOGUE,
        resource_conditions={
            'yield_resource_names': ['Stone', 'Iron', 'Gold'],
            'base_yield_logic': lambda r: 1
        }
    )

    analyzed_nodes_by_type = defaultdict(dict)
    summary_by_type = defaultdict(lambda: {"total": 0, "ready": 0, "recovering": 0, "total_yield": Decimal('0')})
    critical_hit_stats = defaultdict(int)
    placed_collectibles = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}
    player_skills = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())
    current_timestamp_ms = int(time.time() * 1000)

    for api_key, node_info in RESOURCE_NODE_MAP.items():
        nodes_api_data = farm_data.get(api_key, {})
        resource_name = node_info["name"] # This is the resource produced, e.g., "Stone"
        recovery_name = node_info["recovery_name"]
        base_yield = node_info["base_yield"]
        base_recovery_time = node_info["recovery_time"]

        # Calcula o tempo de recuperação com todos os bônus do jogador (sem AOE)
        player_wide_recovery_info = _calculate_recovery_time(base_recovery_time, active_boosts, recovery_name)
        summary_by_type[resource_name]['final_recovery_time'] = player_wide_recovery_info.get('final', base_recovery_time)

        special_logic = node_info.get("special_logic")

        for node_id, node_data in nodes_api_data.items():
            summary_by_type[resource_name]["total"] += 1

            current_base_yield = base_yield
            node_context = {}
            # CORREÇÃO: Inicializa as flags a cada iteração para evitar UnboundLocalError.
            has_oil_bonus = False
            crimstone_reset_at_ms = None

            if special_logic == "lavaPit":
                mined_at_ms = node_data.get("collectedAt", 0)
                if not mined_at_ms: # Se não foi coletado, está ativo
                    mined_at_ms = node_data.get("startedAt", 0)
                critical_hits = {}
            elif special_logic == "oilReserve":
                oil_details = node_data.get("oil", {})
                mined_at_ms = oil_details.get("drilledAt", 0)
                critical_hits = {} # Oil reserves não têm critical hits
                # Special yield logic for Oil Reserves
                drilled_count = node_data.get("drilled", 0)
                if (drilled_count + 1) % 3 == 0:
                    has_oil_bonus = True
            else:
                stone_details = node_data.get("stone", {})
                mined_at_ms = stone_details.get("minedAt", 0)
                critical_hits = stone_details.get("criticalHit", {})
                if special_logic == "minesLeft":
                    current_mines_left = node_data.get("minesLeft", 0)
                    
                    # Lógica de reset para Crimstone se não for minerada por muito tempo
                    # Conforme mineCrimstone.ts
                    if resource_name == "Crimstone":
                        time_since_mined_ms = current_timestamp_ms - mined_at_ms
                        time_to_reset_ms = (base_recovery_time + 24 * 3600) * 1000
                        
                        # Apenas aplica o reset se a rocha já foi minerada antes
                        if mined_at_ms > 0 and time_since_mined_ms > time_to_reset_ms:
                            current_mines_left = 5 # Valor máximo para Crimstone
                        # Calcula o timestamp de reset se a rocha não estiver pronta para resetar
                        elif mined_at_ms > 0:
                            crimstone_reset_at_ms = mined_at_ms + time_to_reset_ms
                    node_context["minesLeft"] = current_mines_left
            for hit_name, hit_count in critical_hits.items():
                if hit_count > 0:
                    critical_hit_stats[hit_name] += hit_count

            node_specific_boosts = list(active_boosts)
            has_aoe_buff = False

            node_position = {"x": node_data.get("x"), "y": node_data.get("y")}
            if node_position["x"] is not None and node_position["y"] is not None:
                aoe_boosts = resource_analysis_service.get_aoe_boosts_for_resource(
                    resource_position=node_position,
                    placed_items=placed_collectibles,
                    player_skills=player_skills,
                    farm_data=farm_data
                )
                if aoe_boosts:
                    node_specific_boosts.extend(aoe_boosts)
                    has_aoe_buff = True

            for temporal_info in temporal_boosts:
                if mined_at_ms > temporal_info['activation_ts']:
                    node_specific_boosts.append(temporal_info['boost'])

            for hit_name, hit_count in critical_hits.items():
                if hit_count > 0 and hit_name in MINING_BOOST_CATALOGUE:
                    source_type = MINING_BOOST_CATALOGUE[hit_name].get("source_type")
                    # CORREÇÃO: O bônus "Nativo" é uma mecânica do jogo, não uma skill.
                    if hit_name == "Native":
                        source_type = "game_mechanic"

                    for boost in MINING_BOOST_CATALOGUE[hit_name].get("boosts", []):
                        if boost.get("type") == "YIELD":
                            # Evita redundância como "(Nativo) Native"
                            source_item_text = "(Critical Hit)" if hit_name == "Native" else f"{hit_name} (Critical Hit)"
                            node_specific_boosts.append({
                                "type": "YIELD", "operation": boost["operation"], 
                                "value": boost["value"], "source_item": source_item_text,
                                "source_type": source_type
                            })

            # Lógica especial para o bônus de +2 na última picaretada de Crimstone,
            # que é uma mecânica do jogo não associada a um item específico.
            if resource_name == "Crimstone" and node_context.get("minesLeft") == 1:
                node_specific_boosts.append({
                    "type": "YIELD",
                    "operation": "add",
                    "value": 2, # O bônus é +2, não +3
                    "source_item": "Bônus da Última Picaretada",
                    "source_type": "game_mechanic"
                })

            # Adiciona o bônus de óleo como um boost, para que apareça na lista de bônus.
            if has_oil_bonus:
                node_specific_boosts.append({
                    "type": "YIELD",
                    "operation": "add",
                    "value": 20,
                    "source_item": "Bônus de Reserva de Óleo",
                    "source_type": "game_mechanic"
                })

            yield_info = _calculate_yield(current_base_yield, node_specific_boosts, resource_name, node_context)
            summary_by_type[resource_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

            recovery_info = _calculate_recovery_time(base_recovery_time, node_specific_boosts, recovery_name, node_context)
            final_recovery_ms = recovery_info["final"] * 1000

            is_ready = not mined_at_ms or current_timestamp_ms >= (mined_at_ms + final_recovery_ms)
            state_name = "Pronto" if is_ready else "Recuperando"
            summary_by_type[resource_name]["ready" if is_ready else "recovering"] += 1
            ready_at_ms = mined_at_ms + final_recovery_ms if not is_ready else current_timestamp_ms

            analyzed_node = {
                "id": node_id, "state_name": state_name,
                "ready_at_timestamp_ms": int(ready_at_ms),
                "calculations": {"yield": yield_info, "recovery": recovery_info},
                "has_aoe_buff": has_aoe_buff,
                "critical_hits": critical_hits
            }
            if crimstone_reset_at_ms:
                analyzed_node["crimstone_reset_at_ms"] = int(crimstone_reset_at_ms)

            if "minesLeft" in node_context:
                analyzed_node["mines_left"] = node_context["minesLeft"]

            analyzed_nodes_by_type[resource_name][node_id] = analyzed_node

    # Ordena os nós dentro de cada tipo
    for resource_type in analyzed_nodes_by_type:
        analyzed_nodes_by_type[resource_type] = dict(sorted(analyzed_nodes_by_type[resource_type].items()))

    view_data = {
        "summary_by_type": dict(sorted(summary_by_type.items())),
        "nodes_by_type": dict(sorted(analyzed_nodes_by_type.items())),
        "critical_hit_stats": dict(sorted(critical_hit_stats.items())),
        "active_boost_items": sorted(list(active_item_names)),
        "all_catalogued_items": sorted(list(MINING_BOOST_CATALOGUE.keys())),
        "active_temporal_boosts": processed_temporal_boosts,
        "min_max_yields": min_max_yield_analysis
    }

    return {"view": view_data}