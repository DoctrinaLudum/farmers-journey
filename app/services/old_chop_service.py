# app/services/chop_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import resources as resources_domain
from ..domain import skills as skills_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA MADEIRA
# ==============================================================================

# Define quais recursos e bônus são relevantes para a madeira.
WOOD_RESOURCE_CONDITIONS = {
    'yield_resource_names': ['Wood'],
    'recovery_resource_names': ['Tree'],
    'skill_tree_name': 'Trees',
}

# Itens que não se acumulam (ex: castores de níveis diferentes).
# A ordem é do melhor para o pior.
NON_CUMULATIVE_BOOST_GROUPS = {
    "beavers": ["Foreman Beaver", "Apprentice Beaver", "Woody the Beaver"],
}

# Mapeamento para bônus de Buds.
BUD_BUFF_TO_WOOD_BOOST_MAPPING = {
    'WOOD_YIELD': {'type': 'YIELD', 'operation': 'add'},
    'TREE_RECOVERY_TIME': {'type': 'RECOVERY_TIME', 'operation': 'percentage'}
}

# O catálogo de bônus de madeira é criado uma única vez.
WOOD_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(WOOD_RESOURCE_CONDITIONS)

TREE_RECOVERY_TIME_SECONDS = 2 * 60 * 60  # 2 horas em segundos

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _get_wood_drop_amount(active_boosts: list) -> dict:
    """
    Calcula o rendimento de madeira, espelhando getWoodDropAmount de chop.ts.
    """
    # Reutiliza a função genérica e mais robusta do serviço de análise.
    return resource_analysis_service.calculate_final_yield(
        base_yield=1.0,
        active_boosts=active_boosts,
        resource_name="Wood"
    )

def _get_tree_recovery_time(active_boosts: list) -> dict:
    """
    Calcula o tempo de recuperação da árvore, espelhando getChoppedAt de chop.ts.
    """
    return resource_analysis_service.calculate_final_recovery_time(
        base_time=TREE_RECOVERY_TIME_SECONDS,
        active_boosts=active_boosts,
        resource_name="Tree"
    )

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_wood_resources(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todas as árvores, calcula os bônus de madeira e retorna um
    relatório completo, espelhando a lógica de chop.ts.

    Este serviço é o orquestrador para a lógica de "corte de madeira".
    Ele utiliza:
    - Funções de cálculo internas (_get_wood_drop_amount, _get_tree_recovery_time) para a lógica específica de madeira.
    - `resource_analysis_service` para funções de ajuda genéricas (encontrar bônus, analisar AOE) que são compartilhadas com outros serviços.
    """
    player_items = resource_analysis_service._get_player_items(farm_data)

    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        WOOD_BOOST_CATALOGUE,
        NON_CUMULATIVE_BOOST_GROUPS,
        farm_data
    )

    active_item_names = {item for item in player_items if item in WOOD_BOOST_CATALOGUE}
    if active_bud_buffs:
        active_item_names.add("Buds")

    if active_bud_buffs:
        for bud_buff_name, mapping in BUD_BUFF_TO_WOOD_BOOST_MAPPING.items():
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
        player_items, active_boosts, WOOD_BOOST_CATALOGUE,
        resource_conditions={
            'yield_resource_names': ['Wood'],
            'base_yield_logic': lambda r: 1
        }
    )

    # Calcula o tempo de recuperação com todos os bônus do jogador (sem AOE)
    player_wide_recovery_info = _get_tree_recovery_time(active_boosts)

    trees_api_data = farm_data.get("trees", {})
    analyzed_trees = {}
    summary = {"total": 0, "ready": 0, "recovering": 0, "total_yield": Decimal('0')}
    summary['final_recovery_time'] = player_wide_recovery_info.get('final', TREE_RECOVERY_TIME_SECONDS)
    placed_collectibles = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}
    player_skills = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())
    critical_hit_stats = defaultdict(int)
    current_timestamp_ms = int(time.time() * 1000)

    for tree_id, tree_data in trees_api_data.items():
        summary["total"] += 1
        
        wood_details = tree_data.get("wood", {})
        chopped_at_ms = wood_details.get("choppedAt", 0)
        critical_hits = wood_details.get("criticalHit", {})

        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0:
                critical_hit_stats[hit_name] += hit_count

        tree_specific_boosts = list(active_boosts)
        has_aoe_buff = False

        # Lógica genérica para bônus de Área de Efeito (AOE).
        # Embora atualmente não existam bônus de AOE para madeira, esta estrutura
        # garante que, se um for adicionado no futuro, ele será aplicado corretamente.
        tree_position = {"x": tree_data.get("x"), "y": tree_data.get("y")}
        if tree_position["x"] is not None and tree_position["y"] is not None:
            aoe_boosts = resource_analysis_service.get_aoe_boosts_for_resource(
                resource_position=tree_position,
                placed_items=placed_collectibles,
                player_skills=player_skills
            )
            if aoe_boosts:
                tree_specific_boosts.extend(aoe_boosts)
                has_aoe_buff = True

        for temporal_info in temporal_boosts:
            if chopped_at_ms > temporal_info['activation_ts']:
                tree_specific_boosts.append(temporal_info['boost'])

        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0 and hit_name in WOOD_BOOST_CATALOGUE:
                source_type = WOOD_BOOST_CATALOGUE[hit_name].get("source_type")
                # CORREÇÃO: O bônus "Nativo" é uma mecânica do jogo, não uma skill.
                if hit_name == "Native":
                    source_type = "game_mechanic"

                for boost in WOOD_BOOST_CATALOGUE[hit_name].get("boosts", []):
                    if boost.get("type") == "YIELD":
                        # Evita redundância como "(Nativo) Native"
                        source_item_text = "(Critical Hit)" if hit_name == "Native" else f"{hit_name} (Critical Hit)"
                        tree_specific_boosts.append({
                            "type": "YIELD", "operation": boost["operation"], 
                            "value": boost["value"], "source_item": source_item_text,
                            "source_type": source_type
                        })

        yield_info = _get_wood_drop_amount(tree_specific_boosts)
        summary['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        recovery_info = _get_tree_recovery_time(tree_specific_boosts)
        final_recovery_ms = recovery_info["final"] * 1000 # O resultado já está em segundos

        is_ready = not chopped_at_ms or current_timestamp_ms >= (chopped_at_ms + final_recovery_ms)
        state_name = "Pronta" if is_ready else "Recuperando"
        summary["ready" if is_ready else "recovering"] += 1
        ready_at_ms = chopped_at_ms + final_recovery_ms if not is_ready else current_timestamp_ms

        analyzed_trees[tree_id] = {
            "id": tree_id, "state_name": state_name,
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "recovery": recovery_info},
            "has_aoe_buff": has_aoe_buff,
            "critical_hits": critical_hits
        }

    view_data = {
        "summary": summary,
        "tree_status": dict(sorted(analyzed_trees.items())),
        "critical_hit_stats": dict(sorted(critical_hit_stats.items())),
        "active_boost_items": sorted(list(active_item_names)),
        "all_catalogued_items": sorted(list(WOOD_BOOST_CATALOGUE.keys())),
        "active_temporal_boosts": processed_temporal_boosts,
        "min_max_yields": min_max_yield_analysis
    }

    return {"view": view_data}