# app/services/greenhouse_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from .. import analysis
from ..domain import crops as crops_domain
from ..domain import fruits as fruit_domain
from ..domain import skills as skills_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA ESTUFA
# ==============================================================================

# Define quais recursos e bônus são relevantes para a estufa.
# Inclui culturas e frutas que podem ser plantadas na estufa.
GREENHOUSE_RESOURCE_CONDITIONS = {
    'yield_resource_names': list(crops_domain.GREENHOUSE_CROPS.keys()) + list(fruit_domain.GREENHOUSE_FRUIT.keys()),
    'recovery_resource_names': list(crops_domain.GREENHOUSE_CROPS.keys()) + list(fruit_domain.GREENHOUSE_FRUIT.keys()),
    'skill_tree_name': 'Greenhouse',
    'boost_category_names': ['Crop', 'Fruit'] # Para bônus genéricos de categoria
}

NON_CUMULATIVE_BOOST_GROUPS = {
    "scarecrow": ["Kuebiko", "Scarecrow", "Nancy"],
}

GREENHOUSE_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(GREENHOUSE_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _calculate_greenhouse_yield(base_active_boosts: list, critical_hits: dict, plant_name: str, node_context: dict) -> dict:
    """
    Calcula o rendimento de uma planta na estufa de forma explícita,
    separando o cálculo de rendimento normal e de acertos críticos.
    """
    # 1. Calcula o rendimento normal (sem críticos)
    yield_info_normal = resource_analysis_service.calculate_final_yield(
        base_yield=1.0,
        active_boosts=base_active_boosts,
        resource_name=plant_name,
        node_context=node_context
    )
    yield_normal = Decimal(str(yield_info_normal.get('final_deterministic', 1.0)))
    
    # Inicia a lista de bônus aplicados com os bônus normais.
    applied_buffs = list(yield_info_normal.get('applied_buffs', []))
    
    total_yield = yield_normal
    
    # 2. Itera sobre os críticos que ocorreram e calcula o bônus adicional
    if critical_hits:
        for hit_name, hit_count in critical_hits.items():
            if not (hit_count > 0 and hit_name in GREENHOUSE_BOOST_CATALOGUE):
                continue

            # Encontra a definição do bônus de crítico no catálogo
            crit_boost_info = next((b for b in GREENHOUSE_BOOST_CATALOGUE[hit_name].get("boosts", []) if b.get("type") == "YIELD"), None)
            if not crit_boost_info:
                continue

            # Calcula o rendimento COM o bônus de crítico
            boosts_with_crit = base_active_boosts + [crit_boost_info]
            yield_info_crit = resource_analysis_service.calculate_final_yield(
                base_yield=1.0,
                active_boosts=boosts_with_crit,
                resource_name=plant_name,
                node_context=node_context
            )
            yield_with_crit = Decimal(str(yield_info_crit.get('final_deterministic', 1.0)))

            # O bônus real é a diferença
            bonus_per_crit = yield_with_crit - yield_normal
            total_bonus_from_this_crit = bonus_per_crit * Decimal(str(hit_count))
            
            # Adiciona o bônus ao rendimento total
            total_yield += total_bonus_from_this_crit

            # Adiciona o bônus formatado à lista para exibição no frontend
            source_type = GREENHOUSE_BOOST_CATALOGUE[hit_name].get("source_type")
            applied_buffs.append({
                **crit_boost_info, 
                "source_item": f"{hit_name} (Critical Hit)", 
                "source_type": source_type, 
                "count": hit_count,
                "total_bonus_yield": float(total_bonus_from_this_crit)
            })

    return {
        "final_deterministic": float(total_yield),
        "applied_buffs": applied_buffs,
        "breakdown": { # Adiciona um breakdown para depuração, se necessário
            "normal_yield": float(yield_normal),
        }
    }


def _calculate_greenhouse_growth_time(active_boosts: list, plant_name: str, node_context: dict) -> dict:
    """
    Calcula o tempo de crescimento de uma planta na estufa, usando o serviço de análise genérico.
    """
    base_time = 0
    # Acessa os domínios corretos para encontrar o tempo base
    if plant_name in crops_domain.CROPS and crops_domain.CROPS[plant_name].get("planting_spot") == "Greenhouse":
        base_time = crops_domain.CROPS[plant_name].get("harvestSeconds", 0)
    elif plant_name in fruit_domain.FRUIT_DATA and fruit_domain.FRUIT_DATA[plant_name].get("planting_spot") == "Greenhouse":
        seed_name = fruit_domain.FRUIT_DATA[plant_name].get("seed_name")
        if seed_name:
            base_time = fruit_domain.FRUIT_SEEDS.get(seed_name, {}).get("plantSeconds", 0)
    
    if base_time == 0:
        log.warning(f"Não foi possível encontrar o tempo de crescimento base para a planta da estufa: {plant_name}")
        return {"final": 0, "applied_buffs": []}

    return resource_analysis_service.calculate_final_recovery_time(
        base_time=base_time,
        active_boosts=active_boosts,
        resource_name=plant_name,
        node_context=node_context
    )

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_greenhouse_resources(farm_data: dict) -> dict:
    """
    Analisa todos os vasos da estufa, calcula bônus e retorna um relatório completo.
    """
    greenhouse_data = farm_data.get("greenhouse")
    if not greenhouse_data:
        return None

    # 1. Obter todos os bônus ativos do jogador que se aplicam à estufa.
    player_items = resource_analysis_service._get_player_items(farm_data)
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        GREENHOUSE_BOOST_CATALOGUE,
        NON_CUMULATIVE_BOOST_GROUPS, # A estufa não possui grupos de bônus não cumulativos definidos.
        farm_data
    )

    # 2. Analisar cada vaso individualmente.
    pots = greenhouse_data.get("pots", {})
    analyzed_pots = {}
    critical_hit_stats = defaultdict(int)
    current_timestamp_ms = int(time.time() * 1000)

    for pot_id, pot_data in pots.items():
        plant_details = pot_data.get("plant")
        if not plant_details:
            continue

        plant_name = plant_details.get("name")
        planted_at_ms = plant_details.get("plantedAt", 0)
        critical_hits = plant_details.get("criticalHit", {})

        # Contabiliza os acertos críticos para o resumo geral.
        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0:
                critical_hit_stats[hit_name] += hit_count
        
        # Define o contexto do nó para a verificação de condições
        node_context = {"building": "Greenhouse"}

        # 3. Calcular o rendimento e o tempo de crescimento para a planta neste vaso.
        yield_info = _calculate_greenhouse_yield(active_boosts, critical_hits, plant_name, node_context)
        growth_time_info = _calculate_greenhouse_growth_time(active_boosts, plant_name, node_context)
        
        final_growth_ms = growth_time_info.get("final", 0) * 1000
        ready_at_ms = planted_at_ms + final_growth_ms
        is_ready = current_timestamp_ms >= ready_at_ms
        state_name = "Pronta" if is_ready else "Crescendo"

        # 4. Montar o dicionário de dados analisados para este vaso.
        analyzed_pots[pot_id] = {
            "id": pot_id,
            "plant_name": plant_name,
            "icon_path": analysis.get_item_image_path(plant_name),
            "state_name": state_name,
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {
                "yield": yield_info,
                "growth": growth_time_info
            },
            "critical_hits": critical_hits,
        }

    # 5. Preparar dados para a exibição no mapa da fazenda.
    growing_plants = sorted(list(set(p['plant_name'] for p in analyzed_pots.values() if p.get('plant_name'))))

    map_display_data = {
        "growing_plants": growing_plants,
    }

    # 6. Retornar a estrutura de dados final para a view.
    return {
        "view": {
            "type": "Greenhouse",
            "pots": dict(sorted(analyzed_pots.items())),
            "map_display": map_display_data,
            "critical_hit_stats": dict(sorted(critical_hit_stats.items())),
        }
    }
