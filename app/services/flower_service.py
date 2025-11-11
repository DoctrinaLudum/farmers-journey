# app/services/flower_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import flowers as flower_domain
from ..domain import resources as resources_domain
from ..domain import seeds as seeds_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO
# ==============================================================================

FLOWER_RESOURCE_CONDITIONS = {
    'yield_resource_names': list(flower_domain.FLOWER_DATA.keys()),
    'recovery_resource_names': list(flower_domain.FLOWER_DATA.keys()),
    'skill_tree_name': 'Bees & Flowers',
    'boost_category_names': ['Flower']
}
FLOWER_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(FLOWER_RESOURCE_CONDITIONS)

BEEHIVE_RESOURCE_CONDITIONS = {
    'yield_resource_names': ['Honey'],
    'recovery_resource_names': ['Beehive'],
    'skill_tree_name': 'Bees & Flowers',
    'boost_category_names': ['Honey', 'Animal']
}
BEEHIVE_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(BEEHIVE_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _get_flower_yield_amount(active_boosts: list) -> dict:
    """
    Calcula o rendimento de uma flor de forma data-driven.
    O rendimento base é 1, e bônus (geralmente de acertos críticos) são adicionados.
    """
    return resource_analysis_service.calculate_final_yield(
        base_yield=1.0,
        active_boosts=active_boosts,
        resource_name="Flower"
    )

def _get_flower_growth_time(active_boosts: list, flower_name: str) -> dict:
    """Calcula o tempo de crescimento de uma flor de forma data-driven."""
    seed_name = flower_domain.FLOWER_DATA.get(flower_name, {}).get("seed")
    base_time = seeds_domain.SEEDS_DATA.get(seed_name, {}).get("plant_seconds", 0)
    if base_time == 0:
        return {"final": 0, "applied_buffs": []}

    return resource_analysis_service.calculate_final_recovery_time(base_time, active_boosts, flower_name)

def _get_honey_yield_amount(active_boosts: list) -> dict:
    """Calcula o rendimento de mel por colmeia cheia de forma data-driven."""
    return resource_analysis_service.calculate_final_yield(
        base_yield=1.0,
        active_boosts=active_boosts,
        resource_name="Honey"
    )

def _get_honey_production_time(game_state: dict, attached_flowers: int) -> dict:
    """
    Calcula o tempo de produção de mel para uma colmeia de forma data-driven.
    Espelha a lógica de `getHoneyProductionRate` de `updateBeehives.ts` e considera
    bônus de velocidade (PRODUCTION_SPEED) e redução de tempo (RECOVERY_TIME)
    provenientes de itens colecionáveis, vestíveis e habilidades.

    Args:
        game_state (dict): O estado atual do jogo.
        attached_flowers (int): O número de flores anexadas à colmeia, que afeta a velocidade.

    Returns:
        dict: Um dicionário contendo o tempo base, tempo final, detalhes dos buffs aplicados
              e o multiplicador de velocidade total.
    """
    base_time = resources_domain.RESOURCES_DATA['Honey']['details']['cycle']['Beehive']['recovery_time_seconds']
    speed_multiplier = Decimal('1')
    time_reduction_percentage = Decimal('0')
    applied_buffs_details = []

    # Bônus de flores anexadas: cada flor adiciona 0.02 à velocidade de produção
    if attached_flowers > 0:
        flower_bonus = attached_flowers * 0.02
        speed_multiplier += Decimal(str(flower_bonus))
        applied_buffs_details.append({
            "source_item": f"{attached_flowers} Flores",
            "value": f"+{flower_bonus} Speed",
            "operation": "speed_multiplier",
            "source_type": 'game_mechanic'
        })

    # Obter todos os bônus ativos relevantes para a produção de mel
    # Estes bônus são definidos nos arquivos de domínio (collectiblesItemBuffs, wearablesItemBuffs, skills)
    active_production_boosts = resource_analysis_service.get_active_player_boosts(
        game_state, BEEHIVE_BOOST_CATALOGUE, {}, game_state
    )

    for boost in active_production_boosts:
        source_item = boost.get("source_item", "Unknown")
        source_type = boost.get("source_type", "unknown")
        boost_type = boost.get("type")
        operation = boost.get("operation")
        value = Decimal(str(boost.get("value", 0)))

        if boost_type == "PRODUCTION_SPEED" and operation == "add":
            # Bônus que aumentam diretamente o multiplicador de velocidade
            speed_multiplier += value
            applied_buffs_details.append({
                "source_item": source_item,
                "value": f"+{value} Speed",
                "operation": "speed_multiplier",
                "source_type": source_type
            })
        elif boost_type == "RECOVERY_TIME" and operation == "percentage":
            # Bônus que reduzem o tempo de recuperação em porcentagem
            # O valor é negativo, então usamos o absoluto para a soma da redução total
            time_reduction_percentage += abs(value)
            applied_buffs_details.append({
                "source_item": source_item,
                "value": f"{value * 100}% Time Reduction",
                "operation": "percentage_reduction",
                "source_type": source_type
            })

    # Calcular o tempo final aplicando primeiro o multiplicador de velocidade e depois a redução percentual
    time_after_speed_multiplier = base_time / float(speed_multiplier) if speed_multiplier > 0 else float('inf')
    final_time = time_after_speed_multiplier * (1 - float(time_reduction_percentage))

    return {"base": base_time, "final": final_time, "applied_buffs": applied_buffs_details, "speed_multiplier": float(speed_multiplier)}

# ==============================================================================
# FUNÇÕES PRINCIPAIS (ORQUESTRADORES)
# ==============================================================================

def analyze_flower_beds(farm_data: dict) -> dict:
    """Analisa todos os canteiros de flores, calcula bônus e retorna um relatório completo."""
    flower_beds_api_data = farm_data.get("flowers", {}).get("flowerBeds", {})
    analyzed_beds = {}
    summary = defaultdict(lambda: {"total": 0, "ready": 0, "growing": 0, "total_yield": Decimal('0')})
    current_timestamp_ms = int(time.time() * 1000)

    player_items = resource_analysis_service._get_player_items(farm_data)
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items, FLOWER_BOOST_CATALOGUE, {}, farm_data
    )

    for bed_id, bed_data in flower_beds_api_data.items():
        flower_details = bed_data.get("flower")
        if not flower_details: continue

        flower_name = flower_details.get("name")
        if not flower_name: continue

        summary[flower_name]["total"] += 1
        
        growth_time_info = _get_flower_growth_time(active_boosts, flower_name)
        final_growth_ms = growth_time_info["final"] * 1000
        
        planted_at_ms = flower_details.get("plantedAt", 0)
        ready_at_ms = planted_at_ms + final_growth_ms
        is_ready = current_timestamp_ms >= ready_at_ms
        
        summary[flower_name]["ready" if is_ready else "growing"] += 1
        if 'final_recovery_time' not in summary[flower_name]:
            summary[flower_name]['final_recovery_time'] = growth_time_info.get('final', 0)

        bed_specific_boosts = list(active_boosts)
        critical_hits = flower_details.get("criticalHit", {})
        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0 and hit_name in FLOWER_BOOST_CATALOGUE:
                source_type = FLOWER_BOOST_CATALOGUE[hit_name].get("source_type", "collectible")
                for boost in FLOWER_BOOST_CATALOGUE[hit_name].get("boosts", []):
                    if boost.get("type") == "YIELD":
                        bed_specific_boosts.append({
                            **boost,
                            "source_item": f"{hit_name} (Critical Hit)",
                            "source_type": source_type,
                        })

        yield_info = _get_flower_yield_amount(bed_specific_boosts)
        summary[flower_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        analyzed_beds[bed_id] = {
            "id": bed_id, "flower_name": flower_name,
            "state_name": "Pronta" if is_ready else "Crescendo",
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "growth": growth_time_info},
            "cross_breed": flower_details.get("crossbreed"),
            "critical_hits": critical_hits,
        }

    return {"view": {
        "beds": dict(sorted(analyzed_beds.items())),
        "summary_by_flower": dict(sorted(summary.items()))
    }}

def analyze_beehives(farm_data: dict) -> dict:
    """Analisa todas as colmeias, calcula bônus e retorna um relatório completo."""
    beehives_api_data = farm_data.get("beehives", {})
    if not beehives_api_data:
        return None

    analyzed_hives = {}
    current_timestamp_ms = int(time.time() * 1000)

    player_items = resource_analysis_service._get_player_items(farm_data)
    active_yield_boosts = resource_analysis_service.get_active_player_boosts(
        player_items, BEEHIVE_BOOST_CATALOGUE, {}, farm_data
    )

    base_honey_time = resources_domain.RESOURCES_DATA['Honey']['details']['cycle']['Beehive']['recovery_time_seconds']

    for hive_id, hive_data in beehives_api_data.items():
        attached_flowers = len(hive_data.get("flowers", []))
        
        production_time_info = _get_honey_production_time(farm_data, attached_flowers)
        yield_info = _get_honey_yield_amount(active_yield_boosts)
        
        final_production_time_seconds = production_time_info.get("final", base_honey_time)
        
        honey_details = hive_data.get("honey", {})
        honey_updated_at = honey_details.get("updatedAt", 0)
        honey_produced_at_last_update = honey_details.get("produced", 0)
        
        time_since_update_seconds = (current_timestamp_ms - honey_updated_at) / 1000
        new_honey_produced = honey_produced_at_last_update + time_since_update_seconds
        
        total_honey_produced_seconds = min(new_honey_produced, final_production_time_seconds)
        
        is_ready = total_honey_produced_seconds >= final_production_time_seconds
        state_name = "Pronta" if is_ready else "Produzindo"
        
        time_to_full_seconds = final_production_time_seconds - total_honey_produced_seconds
        ready_at_ms = current_timestamp_ms + (time_to_full_seconds * 1000)
            
        analysis_details = {
            "id": hive_id, "resource_name": "Beehive",
            "state_name": state_name, "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "recovery": production_time_info},
            "bonus_reward": None,
            "beeSwarm": hive_data.get("swarm", False)
        }

        analyzed_hives[hive_id] = analysis_details

    return {"view": {"hives": dict(sorted(analyzed_hives.items()))}}
