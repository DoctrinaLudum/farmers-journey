# app/services/crop_machine_service.py

import logging
from datetime import datetime, timezone
from decimal import Decimal

from ..analysis import get_item_image_path
from ..domain import crops as crops_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA A CROP MACHINE
# ==============================================================================

# Define quais recursos e bônus são relevantes para a Crop Machine.
CROP_MACHINE_RESOURCE_CONDITIONS = {
    'yield_resource_names': list(crops_domain.CROPS.keys()), # Todas as culturas
    'recovery_resource_names': [], # O tempo de crescimento é baseado em óleo, não em buffs de tempo de colheita.
    'skill_tree_name': 'Machinery',
    'boost_category_names': ['Crop']
}

CROP_MACHINE_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(CROP_MACHINE_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_crop_machine(farm_data: dict) -> dict:
    """
    Analisa o estado da Crop Machine, calculando o rendimento de cada pacote na fila.
    """
    crop_machine_building = farm_data.get("buildings", {}).get("Crop Machine")
    if not crop_machine_building:
        return {"view": None}

    # 1. Obter todos os bônus de jogador aplicáveis à Crop Machine.
    player_items = resource_analysis_service._get_player_items(farm_data)
    base_active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        CROP_MACHINE_BOOST_CATALOGUE,
        {},
        farm_data
    )

    machine_data = crop_machine_building[0]
    queue = machine_data.get("queue", [])
    processed_queue = []
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    # Adicionado: Custo total de óleo e skills do bumpkin para o cálculo
    total_queue_oil_cost = Decimal('0')
    bumpkin_skills = farm_data.get("bumpkin", {}).get("skills", {})

    # 2. Processar cada pacote na fila individualmente.
    for i, pack in enumerate(queue):
        crop_name = pack.get("crop")
        seeds_count = pack.get("seeds", 0)
        critical_hits = pack.get("criticalHit", {})

        # Adicionado: Cálculo do custo de óleo para o pacote
        pack_grow_time_seconds = pack.get("totalGrowTime", 0) / 1000
        base_oil_cost = Decimal(str(pack_grow_time_seconds))
        
        oil_reduction_factor = Decimal('1.0')
        applied_oil_skills = []

        if bumpkin_skills.get("Oil Gadget"):
            oil_reduction_factor -= Decimal('0.10')
            applied_oil_skills.append("Oil Gadget (-10%)")

        if bumpkin_skills.get("Efficiency Extension Module"):
            oil_reduction_factor -= Decimal('0.30')
            applied_oil_skills.append("Efficiency Extension Module (-30%)")
        
        final_oil_cost = base_oil_cost * oil_reduction_factor
        total_queue_oil_cost += final_oil_cost

        if not crop_name or seeds_count <= 0:
            processed_pack = {
                **pack, "pack_index": i, "is_ready": False, 
                "oil_cost": float(final_oil_cost), "applied_oil_skills": applied_oil_skills,
                "yield_info": {"final_deterministic": 0, "applied_buffs": [], "breakdown": {}}
            }
            processed_queue.append(processed_pack)
            continue

        # 3. Calcular o rendimento de forma analítica para eficiência.
        #    Isso é matematicamente equivalente a iterar por cada semente, mas muito mais rápido.
        
        # 3.1. Rendimento de uma semente normal
        yield_info_normal = resource_analysis_service.calculate_final_yield(
            base_yield=1.0, active_boosts=base_active_boosts, resource_name=crop_name
        )
        yield_per_normal_seed = Decimal(str(yield_info_normal.get('final_deterministic', 1.0)))
        applied_buffs = list(yield_info_normal.get('applied_buffs', []))
        
        total_yield = Decimal('0')
        total_critical_seeds = 0

        # Estruturas para o detalhamento (breakdown)
        total_yield_from_crits_map = {}

        # 3.2. Rendimento de sementes com acerto crítico
        if critical_hits:
            for hit_name, hit_count in critical_hits.items():
                if not (hit_count > 0 and hit_name in CROP_MACHINE_BOOST_CATALOGUE):
                    continue

                crit_boost_info = next((b for b in CROP_MACHINE_BOOST_CATALOGUE[hit_name].get("boosts", []) if b.get("type") == "YIELD"), None)
                if not crit_boost_info:
                    continue

                boosts_with_crit = base_active_boosts + [crit_boost_info]
                yield_info_crit = resource_analysis_service.calculate_final_yield(
                    base_yield=1.0, active_boosts=boosts_with_crit, resource_name=crop_name
                )
                yield_per_crit_seed = Decimal(str(yield_info_crit.get('final_deterministic', 1.0)))
                yield_from_this_crit = yield_per_crit_seed * Decimal(str(hit_count))

                total_yield += yield_from_this_crit
                total_critical_seeds += hit_count
                
                # Adiciona ao mapa de detalhamento
                total_yield_from_crits_map[hit_name] = {
                    "count": hit_count,
                    "yield_per_seed": float(yield_per_crit_seed),
                    "total_yield": float(yield_from_this_crit)
                }

                # Adiciona o buff à lista de buffs aplicados
                source_type = CROP_MACHINE_BOOST_CATALOGUE[hit_name].get("source_type")
                applied_buffs.append({
                    **crit_boost_info, "source_item": f"{hit_name} (Critical)", "source_type": source_type, "count": hit_count
                })

        # 3.3. Rendimento das sementes normais restantes
        normal_seeds_count = max(0, seeds_count - total_critical_seeds)
        total_yield_from_normal = Decimal('0')
        if normal_seeds_count > 0:
            total_yield_from_normal = yield_per_normal_seed * Decimal(str(normal_seeds_count))
            total_yield += total_yield_from_normal

        # Adicionado: Cálculo da média de rendimento por semente.
        average_yield_per_seed = total_yield / Decimal(str(seeds_count)) if seeds_count > 0 else Decimal('0')

        # 4. Montar o objeto do pacote processado
        processed_pack = {
            **pack,
            "pack_index": i,
            "is_ready": now_ms >= pack.get("readyAt", float('inf')),
            "oil_cost": float(final_oil_cost),
            "applied_oil_skills": applied_oil_skills,
            "icon_path": get_item_image_path(crop_name), # ADICIONADO: Caminho do ícone da cultura
            "yield_info": {
                "final_deterministic": float(total_yield),
                "average_yield_per_seed": float(average_yield_per_seed),
                "applied_buffs": applied_buffs,
                "breakdown": {
                    "normal_seeds": {
                        "count": normal_seeds_count,
                        "yield_per_seed": float(yield_per_normal_seed),
                        "total_yield": float(total_yield_from_normal)
                    },
                    "critical_hits": total_yield_from_crits_map
                }
            },
        }
        processed_queue.append(processed_pack)

    return {
        "view": {
            "queue": processed_queue,
            "unallocatedOilTime": machine_data.get("unallocatedOilTime", 0),
            "total_oil_cost": float(total_queue_oil_cost)
        }
    }