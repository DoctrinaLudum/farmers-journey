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

GREENHOUSE_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(GREENHOUSE_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _calculate_greenhouse_yield(active_boosts: list, plant_name: str, critical_hits: dict) -> dict:
    """
    Calcula o rendimento de uma planta na estufa, usando o serviço de análise genérico.
    """
    # Cria uma cópia dos bônus para este cálculo específico, para não alterar a lista original.
    boosts_for_this_pot = list(active_boosts)

    # Adiciona os bônus de acerto crítico que já estão definidos para este vaso.
    if critical_hits:
        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0 and hit_name in GREENHOUSE_BOOST_CATALOGUE:
                source_type = GREENHOUSE_BOOST_CATALOGUE[hit_name].get("source_type")
                for boost in GREENHOUSE_BOOST_CATALOGUE[hit_name].get("boosts", []):
                    if boost.get("type") == "YIELD":
                        # Adiciona o bônus para cada acerto crítico contado.
                        for _ in range(hit_count):
                            boosts_for_this_pot.append({**boost, "source_item": f"{hit_name} (Critical)", "source_type": source_type})

    # O rendimento base para qualquer planta na estufa é 1.
    return resource_analysis_service.calculate_final_yield(
        base_yield=1.0,
        # Usa a lista de bônus específica para este vaso, que inclui os acertos críticos.
        active_boosts=boosts_for_this_pot,
        resource_name=plant_name
    )

def _calculate_greenhouse_growth_time(active_boosts: list, plant_name: str) -> dict:
    """
    Calcula o tempo de crescimento de uma planta na estufa, usando o serviço de análise genérico.
    """
    base_time = 0
    if plant_name in crops_domain.GREENHOUSE_CROPS:
        base_time = crops_domain.GREENHOUSE_CROPS[plant_name]["harvestSeconds"]
    elif plant_name in fruit_domain.GREENHOUSE_FRUIT:
        # A estrutura de dados para frutas é diferente, precisamos buscar o tempo da semente.
        seed_name = fruit_domain.FRUIT_DATA[plant_name].get("seed_name")
        if seed_name:
            base_time = fruit_domain.FRUIT_SEEDS[seed_name].get("plantSeconds", 0)
    
    if base_time == 0:
        log.warning(f"Não foi possível encontrar o tempo de crescimento base para a planta da estufa: {plant_name}")
        return {"final": 0, "applied_buffs": []}

    return resource_analysis_service.calculate_final_recovery_time(
        base_time=base_time,
        active_boosts=active_boosts,
        resource_name=plant_name
    )

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_greenhouse_resources(farm_data: dict) -> dict:
    """
    Analisa todos os vasos da estufa, calcula bônus e retorna um relatório completo.
    Esta função foi refatorada para usar o `resource_analysis_service` padronizado,
    garantindo que todos os bônus (de skills, itens, buds, etc.) sejam aplicados
    de forma consistente e correta.    """
    greenhouse_data = farm_data.get("greenhouse")
    if not greenhouse_data:
        return None

    # 1. Obter todos os bônus ativos do jogador que se aplicam à estufa.
    # Estes bônus são globais e se aplicam a todas as plantas.
    player_items = resource_analysis_service._get_player_items(farm_data)
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        GREENHOUSE_BOOST_CATALOGUE,
        {}, # A estufa não possui grupos de bônus não cumulativos definidos.
        farm_data
    )

    # 3. Analisar cada vaso individualmente.
    pots = greenhouse_data.get("pots", {})
    analyzed_pots = {}
    current_timestamp_ms = int(time.time() * 1000)

    for pot_id, pot_data in pots.items():
        plant_details = pot_data.get("plant")
        if not plant_details:
            continue

        plant_name = plant_details.get("name")
        planted_at_ms = plant_details.get("plantedAt", 0)
        critical_hits = plant_details.get("criticalHit", {})
        
        # 4. Calcular o rendimento e o tempo de crescimento para a planta neste vaso.
        yield_info = _calculate_greenhouse_yield(active_boosts, plant_name, critical_hits)
        growth_time_info = _calculate_greenhouse_growth_time(active_boosts, plant_name)
        
        final_growth_ms = growth_time_info.get("final", 0) * 1000
        ready_at_ms = planted_at_ms + final_growth_ms
        is_ready = current_timestamp_ms >= ready_at_ms
        state_name = "Pronta" if is_ready else "Crescendo"

        # 5. Montar o dicionário de dados analisados para este vaso.
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
            "icon_path": analysis.get_item_image_path(plant_name)
        }

    # 6. Preparar dados para a exibição no mapa da fazenda.
    growing_plants = sorted(list(set(p['plant_name'] for p in analyzed_pots.values() if p.get('plant_name'))))

    map_display_data = {
        "growing_plants": growing_plants,
    }

    # 7. Retornar a estrutura de dados final para a view.
    return {
        "view": {
            "type": "Greenhouse",
            "pots": dict(sorted(analyzed_pots.items())),
            "map_display": map_display_data
        }
    }