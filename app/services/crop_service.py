# app/services/crop_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import crops as crops_domain
from ..domain import resources as resources_domain
from ..domain import skills as skills_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA CULTURAS
# ==============================================================================

CROP_RESOURCE_CONDITIONS = {
    'yield_resource_names': list(crops_domain.CROPS.keys()),
    'recovery_resource_names': list(crops_domain.CROPS.keys()),
    'skill_tree_name': 'Crops',
    'boost_category_names': ['Crop', 'Fruit', 'Flower']
}

NON_CUMULATIVE_BOOST_GROUPS = {
    "scarecrow": ["Kuebiko", "Scarecrow", "Nancy"],
}

CROP_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(CROP_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _get_crop_yield_amount(game_state: dict, plot: dict, crop_name: str, calendar_boosts: list = None) -> dict:
    """
    Calcula o rendimento final de uma cultura, aplicando bônus de itens, habilidades,
    fertilizantes, AOE, eventos de calendário e acertos críticos, seguindo o padrão 
    data-driven do sistema.

    Args:
        game_state (dict): O estado completo do jogo do jogador.
        plot (dict): Os dados específicos do canteiro de cultura (plot) sendo analisado.
        crop_name (str): O nome da cultura plantada no canteiro.
        calendar_boosts (list, optional): Lista de bônus de eventos de calendário ativos.

    Returns:
        dict: Um dicionário contendo o rendimento final e uma lista detalhada de bônus.
    """
    base_yield = Decimal('1')

    player_items = resource_analysis_service._get_player_items(game_state)
    player_skills = set(game_state.get("bumpkin", {}).get("skills", {}).keys())
    collectibles = {**game_state.get("collectibles", {}), **game_state.get("home", {}).get("collectibles", {})}

    # 1. Obter bônus ativos, incluindo os de calendário, para processamento unificado.
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items=player_items,
        boost_catalogue=CROP_BOOST_CATALOGUE,
        non_cumulative_groups=NON_CUMULATIVE_BOOST_GROUPS,
        farm_data=game_state,
        external_boosts=calendar_boosts
    )

    # 2. Inicia a lista de bônus para este plot.
    plot_specific_boosts = list(active_boosts)

    # 3. Adiciona o fertilizante específico do plot, se houver.
    applied_fertiliser = plot.get("fertiliser", {}).get("name")
    if applied_fertiliser and applied_fertiliser in CROP_BOOST_CATALOGUE:
        fertiliser_details = CROP_BOOST_CATALOGUE[applied_fertiliser]
        for boost in fertiliser_details.get("boosts", []):
            plot_specific_boosts.append({"source_item": applied_fertiliser, "source_type": "fertiliser", **boost})

    # 4. Adiciona bônus de AOE (Área de Efeito) que afetam este plot.
    plot_position = {"x": plot.get("x"), "y": plot.get("y")}
    aoe_boosts = resource_analysis_service.get_aoe_boosts_for_resource(
        plot_position, collectibles, player_skills, game_state
    )
    filtered_aoe_boosts = [
        b for b in aoe_boosts
        if resource_analysis_service._conditions_are_met(b.get("conditions", {}), crop_name, {})
    ]
    plot_specific_boosts.extend(filtered_aoe_boosts)
    
    # 5. Adiciona bônus de acertos críticos que realmente ocorreram neste plot.
    critical_hits_data = plot.get("crop", {}).get("criticalHit", {})
    if critical_hits_data:
        for hit_name, hit_count in critical_hits_data.items():
            if hit_count > 0 and hit_name in CROP_BOOST_CATALOGUE:
                item_details = CROP_BOOST_CATALOGUE[hit_name]
                source_type = item_details.get("source_type")
                for boost in item_details.get("boosts", []):
                    if boost.get("type") == "YIELD":
                        plot_specific_boosts.append({
                            "type": "YIELD",
                            "operation": boost["operation"],
                            "value": boost["value"],
                            "source_item": f"{hit_name} (Critical Hit)",
                            "source_type": source_type,
                            "conditions": boost.get("conditions", {})
                        })

    # 6. Calcula o rendimento final com a lista completa e correta de bônus.
    yield_calculation = resource_analysis_service.calculate_final_yield(
        base_yield=float(base_yield),
        active_boosts=plot_specific_boosts,
        resource_name=crop_name
    )
    final_yield = Decimal(str(yield_calculation['final_deterministic']))
    applied_buffs_details = yield_calculation['applied_buffs']

    # 7. Lógica para bônus especiais (hardcoded quando necessário)
    if plot.get("beeSwarm"):
        bee_bonus_value = Decimal('0.2')
        final_yield += bee_bonus_value
        
        bee_swarm_buff = {
            "source_item": "Bee Swarm",
            "value": float(bee_bonus_value),
            "operation": "add",
            "source_type": "game_mechanic"
        }

        if "Pollen Power Up" in player_skills:
            pollen_power_up_value = Decimal('0.1')
            final_yield += pollen_power_up_value
            
            bee_swarm_buff["value"] += float(pollen_power_up_value)
            
            bee_swarm_buff["modifiers"] = [{
                "source_item": "Pollen Power Up",
                "value": f"+{pollen_power_up_value}",
                "operation": "special",
                "source_type": "skill"
            }]
        
        applied_buffs_details.append(bee_swarm_buff)

    return {"final_deterministic": float(final_yield), "applied_buffs": applied_buffs_details}

def _get_crop_growth_time(game_state: dict, crop_name: str, plot: dict, calendar_boosts: list = None) -> dict:
    """
    Calcula o tempo de crescimento de uma cultura, espelhando a lógica de `plant.ts`,
    e aplicando bônus de eventos de calendário como 'sunshower'.
    O fertilizante "Rapid Root" é excluído deste cálculo, pois sua lógica é aplicada
    separadamente no orquestrador principal.
    """
    base_time = crops_domain.CROPS.get(crop_name, {}).get("harvestSeconds", 0)
    if base_time == 0:
        return {"final": 0, "applied_buffs": []}

    player_items = resource_analysis_service._get_player_items(game_state)
    player_skills = set(game_state.get("bumpkin", {}).get("skills", {}).keys())
    collectibles = {**game_state.get("collectibles", {}), **game_state.get("home", {}).get("collectibles", {})}

    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items=player_items,
        boost_catalogue=CROP_BOOST_CATALOGUE,
        non_cumulative_groups=NON_CUMULATIVE_BOOST_GROUPS,
        farm_data=game_state,
        external_boosts=calendar_boosts
    )
    
    plot_specific_boosts = list(active_boosts)

    # Adiciona o fertilizante específico do plot, se houver, exceto "Rapid Root".
    applied_fertiliser = plot.get("fertiliser", {}).get("name")
    if applied_fertiliser and applied_fertiliser in CROP_BOOST_CATALOGUE and applied_fertiliser != "Rapid Root":
        fertiliser_details = CROP_BOOST_CATALOGUE[applied_fertiliser]
        for boost in fertiliser_details.get("boosts", []):
            plot_specific_boosts.append({"source_item": applied_fertiliser, "source_type": "fertiliser", **boost})

    # Adiciona bônus de AOE (Área de Efeito) que afetam este plot.
    plot_position = {"x": plot.get("x"), "y": plot.get("y")}
    aoe_boosts = resource_analysis_service.get_aoe_boosts_for_resource(
        plot_position, collectibles, player_skills, game_state
    )
    filtered_aoe_boosts = [
        b for b in aoe_boosts
        if resource_analysis_service._conditions_are_met(b.get("conditions", {}), crop_name, {})
    ]
    plot_specific_boosts.extend(filtered_aoe_boosts)

    return resource_analysis_service.calculate_final_recovery_time(base_time, plot_specific_boosts, crop_name, node_context={"building": "plot"})

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_crop_resources(farm_data: dict, calendar_boosts: list = None) -> dict:
    """
    Analisa todos os canteiros de culturas na fazenda do jogador, calcula seus
    tempos de crescimento e rendimentos potenciais, e retorna um relatório
    detalhado e um sumário por tipo de cultura.

    Esta função orquestra a análise de cada canteiro individualmente, aplicando
    todos os bônus relevantes (itens, habilidades, fertilizantes, AOE, críticos, eventos)
    através de funções auxiliares e do `resource_analysis_service`.

    Args:
        farm_data (dict): O estado completo do jogo da fazenda do jogador.
        calendar_boosts (list, optional): Lista de bônus de eventos de calendário ativos.

    Returns:
        dict: Um dicionário contendo:
              - 'summary_by_crop': Um sumário agregado por tipo de cultura (total,
                                   pronto, crescendo, rendimento total).
              - 'plot_status': Um dicionário detalhado do status de cada canteiro,
                               incluindo cálculos de rendimento e crescimento, fertilizantes,
                               bônus de abelhas, acertos críticos e recompensas bônus.
    """
    player_items = resource_analysis_service._get_player_items(farm_data)
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items, CROP_BOOST_CATALOGUE, NON_CUMULATIVE_BOOST_GROUPS, farm_data
    )
    
    plots_api_data = farm_data.get("crops", {})
    analyzed_plots = {}
    summary = defaultdict(lambda: {"total": 0, "ready": 0, "growing": 0, "total_yield": Decimal('0')})
    current_timestamp_ms = int(time.time() * 1000)

    for plot_id, plot_data in plots_api_data.items():
        crop_details = plot_data.get("crop")
        if not crop_details:
            continue

        crop_name = crop_details.get("name")
        if not crop_name:
            continue

        summary[crop_name]["total"] += 1
        
        base_growth_seconds = crops_domain.CROPS.get(crop_name, {}).get("harvestSeconds", 0)
        summary[crop_name]['base_recovery_time'] = base_growth_seconds
        
        growth_time_info = _get_crop_growth_time(farm_data, crop_name, plot_data, calendar_boosts)
        final_growth_ms = growth_time_info["final"] * 1000
        
        planted_at_ms = crop_details.get("plantedAt", 0)
        original_ready_at_ms = planted_at_ms + final_growth_ms
        ready_at_ms = original_ready_at_ms

        has_yield_fertiliser = False
        has_time_fertiliser = False
        fertiliser_details = plot_data.get("fertiliser")

        if fertiliser_details:
            fertiliser_name = fertiliser_details.get("name")
            if fertiliser_name == "Rapid Root":
                has_time_fertiliser = True
                fertilised_at_ms = fertiliser_details.get("fertilisedAt", 0)
                
                if fertilised_at_ms > planted_at_ms and fertilised_at_ms < original_ready_at_ms:
                    time_remaining_at_fertilisation = original_ready_at_ms - fertilised_at_ms
                    time_reduction = time_remaining_at_fertilisation / 2
                    ready_at_ms = original_ready_at_ms - time_reduction
                    
                    growth_time_info["applied_buffs"].append({
                        "source_item": "Rapid Root", 
                        "value": "-50% Tempo Restante", 
                        "operation": "special",
                        "source_type": "fertiliser"
                    })

            elif fertiliser_name in CROP_BOOST_CATALOGUE:
                if any(b.get("type") == "YIELD" for b in CROP_BOOST_CATALOGUE[fertiliser_name].get("boosts", [])):
                    has_yield_fertiliser = True

        is_ready = current_timestamp_ms >= ready_at_ms

        state_name = "Pronta" if is_ready else "Crescendo"
        summary[crop_name]["ready" if is_ready else "growing"] += 1

        critical_hits = crop_details.get("criticalHit", {})
        yield_info = _get_crop_yield_amount(
            game_state=farm_data,
            plot=plot_data,
            crop_name=crop_name,
            calendar_boosts=calendar_boosts
        )
        summary[crop_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        bonus_reward_raw = crop_details.get("reward", {}).get("items", [])
        bonus_reward = {item['name']: item['amount'] for item in bonus_reward_raw}

        analyzed_plots[plot_id] = {
            "id": plot_id,
            "crop_name": crop_name,
            "state_name": state_name,
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "growth": growth_time_info},
            "fertiliser": plot_data.get("fertiliser"),
            "beeSwarm": plot_data.get("beeSwarm", False),
            "critical_hits": critical_hits,
            "bonus_reward": bonus_reward,
            "has_yield_fertiliser": has_yield_fertiliser,
            "has_time_fertiliser": has_time_fertiliser,
        }

    view_data = {
        "summary_by_crop": dict(sorted(summary.items())),
        "plot_status": dict(sorted(analyzed_plots.items())),
        # ... (outros dados para a view como active_boost_items, etc.) ...
    }

    return {"view": view_data}