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

CROP_MACHINE_YIELD_CONDITIONS = {
    'yield_resource_names': list(crops_domain.CROPS.keys()),
    'recovery_resource_names': [],
    'skill_tree_name': 'Machinery',
    'boost_category_names': ['Crop']
}
CROP_MACHINE_YIELD_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(CROP_MACHINE_YIELD_CONDITIONS)

OIL_COST_CONDITIONS = {
    'yield_resource_names': [],
    'recovery_resource_names': [],
    'skill_tree_name': 'Machinery',
    'boost_type_names': ['OIL_COST']
}
OIL_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(OIL_COST_CONDITIONS)

CROP_MACHINE_TIME_CONDITIONS = {
    'boost_type_names': ['CROP_MACHINE_GROWTH_TIME']
}
CROP_MACHINE_TIME_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(CROP_MACHINE_TIME_CONDITIONS)


# ==============================================================================
# FUNÇÕES DE FORMATAÇÃO E CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _format_buff_for_display(buff: dict) -> dict:
    """
    Formata um objeto de bônus bruto em um dicionário estruturado para exibição.

    Args:
        buff: O dicionário de bônus bruto.

    Returns:
        Um dicionário formatado com 'source_item', 'source_type', 'effect_str' e 'sentiment'.
    """
    source_item = buff.get("source_item", "Unknown")
    source_type = buff.get("source_type", "N/A")
    operation = buff.get("operation")
    value = Decimal(str(buff.get("value", 0)))
    buff_type = buff.get("type")

    effect_str = ""
    sentiment = "neutral"

    if buff_type == "OIL_COST":
        if operation == "factor_add":
            effect_str = f"+{value:.0%}"
            sentiment = "negative"  # Aumenta o custo, é uma penalidade
        elif operation == "factor_sub":
            effect_str = f"-{value:.0%}"
            sentiment = "positive"  # Reduz o custo, é um bônus
    
    elif buff_type == "CROP_MACHINE_GROWTH_TIME":
        percentage = Decimal('0')
        if operation == "multiply":
            percentage = (value - 1)
        elif operation == "percentage":
            percentage = value

        if percentage < 0:
            effect_str = f"{percentage:.0%}"
            sentiment = "positive"  # Reduz o tempo, é um bônus
        elif percentage > 0:
            effect_str = f"+{percentage:.0%}"
            sentiment = "negative"  # Aumenta o tempo, é uma penalidade

    return {
        "source_item": source_item,
        "source_type": source_type,
        "effect_str": effect_str,
        "sentiment": sentiment
    }

def _calculate_oil_consumption_info(active_boosts: list) -> dict:
    """
    Calcula a taxa de consumo de óleo e fornece um detalhamento dos bônus aplicados.
    A lógica replica a fórmula do jogo: (1 + aumentos) * (1 - reduções).
    """
    increase_factor = Decimal('1')
    decrease_factor = Decimal('1')
    increase_buffs = []
    decrease_buffs = []

    for boost in active_boosts:
        operation = boost.get("operation")
        value = Decimal(str(boost.get("value", 0)))

        if operation == "factor_add":
            increase_factor += value
            increase_buffs.append(_format_buff_for_display(boost))
        elif operation == "factor_sub":
            decrease_factor -= value
            decrease_buffs.append(_format_buff_for_display(boost))

    final_rate = increase_factor * decrease_factor
    
    return {
        "rate": final_rate,
        "increases": increase_buffs,
        "decreases": decrease_buffs,
        "disclaimer": "O custo final de óleo é calculado multiplicando os fatores de aumento pelos de redução. Fórmula: (1 + Soma dos Aumentos) × (1 - Soma das Reduções)."
    }

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_crop_machine(farm_data: dict) -> dict:
    """
    Analisa o estado da Crop Machine, calculando o rendimento e o custo de óleo de cada pacote na fila.
    """
    crop_machine_building = farm_data.get("buildings", {}).get("Crop Machine")
    if not crop_machine_building:
        return {"view": None}

    player_items = resource_analysis_service._get_player_items(farm_data)
    
    base_active_yield_boosts = resource_analysis_service.get_active_player_boosts(
        player_items, CROP_MACHINE_YIELD_BOOST_CATALOGUE, {}, farm_data
    )
    
    active_oil_boosts = resource_analysis_service.get_active_player_boosts(
        player_items, OIL_BOOST_CATALOGUE, {}, farm_data
    )

    active_time_boosts = resource_analysis_service.get_active_player_boosts(
        player_items, CROP_MACHINE_TIME_BOOST_CATALOGUE, {}, farm_data
    )

    # Adiciona um filtro para garantir que apenas os bônus de tempo corretos sejam processados.
    active_time_boosts = [b for b in active_time_boosts if b.get('type') == 'CROP_MACHINE_GROWTH_TIME']

    machine_data = crop_machine_building[0]
    queue = machine_data.get("queue", [])
    processed_queue = []
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    total_queue_oil_cost = Decimal('0')

    # Processar bônus globais para exibição
    oil_consumption_info = _calculate_oil_consumption_info(active_oil_boosts)
    oil_consumption_rate = oil_consumption_info['rate']

    formatted_time_buffs = [_format_buff_for_display(b) for b in active_time_boosts]
    global_time_buffs_info = {
        "buffs": formatted_time_buffs,
        "disclaimer": "Os bônus de tempo são aplicados de forma multiplicativa sobre o tempo base."
    }

    # Calcula o tamanho máximo da fila diretamente, verificando a skill do jogador
    skills = farm_data.get("bumpkin", {}).get("skills", {})
    max_queue_size = 10 if "Field Expansion Module" in skills else 5

    # Processar cada pacote na fila
    for i, pack in enumerate(queue):
        crop_name = pack.get("crop")
        seeds_count = pack.get("seeds", 0)
        critical_hits = pack.get("criticalHit", {})

        pack_grow_time_ms = Decimal(str(pack.get("totalGrowTime", 0)))
        base_oil_cost_in_hours = pack_grow_time_ms / Decimal(3600000)
        final_oil_cost = base_oil_cost_in_hours * oil_consumption_rate
        
        total_queue_oil_cost += final_oil_cost

        if not crop_name or seeds_count <= 0:
            processed_pack = {
                **pack, "pack_index": i, "is_ready": False, 
                "oil_cost": float(final_oil_cost), 
                "yield_info": {"final_deterministic": 0, "applied_buffs": [], "breakdown": {}}
            }
            processed_queue.append(processed_pack)
            continue

        yield_info_normal = resource_analysis_service.calculate_final_yield(
            base_yield=1.0, active_boosts=base_active_yield_boosts, resource_name=crop_name
        )
        yield_per_normal_seed = Decimal(str(yield_info_normal.get('final_deterministic', 1.0)))
        applied_yield_buffs = list(yield_info_normal.get('applied_buffs', []))
        
        total_yield = Decimal('0')
        total_critical_seeds = 0
        total_yield_from_crits_map = {}

        if critical_hits:
            for hit_name, hit_count in critical_hits.items():
                if not (hit_count > 0 and hit_name in CROP_MACHINE_YIELD_BOOST_CATALOGUE):
                    continue

                crit_boost_info = next((b for b in CROP_MACHINE_YIELD_BOOST_CATALOGUE[hit_name].get("boosts", []) if b.get("type") == "YIELD"), None)
                if not crit_boost_info:
                    continue

                boosts_with_crit = base_active_yield_boosts + [crit_boost_info]
                yield_info_crit = resource_analysis_service.calculate_final_yield(
                    base_yield=1.0, active_boosts=boosts_with_crit, resource_name=crop_name
                )
                yield_per_crit_seed = Decimal(str(yield_info_crit.get('final_deterministic', 1.0)))
                yield_from_this_crit = yield_per_crit_seed * Decimal(str(hit_count))

                total_yield += yield_from_this_crit
                total_critical_seeds += hit_count
                
                total_yield_from_crits_map[hit_name] = {
                    "count": hit_count,
                    "yield_per_seed": float(yield_per_crit_seed),
                    "total_yield": float(yield_from_this_crit)
                }

                source_type = CROP_MACHINE_YIELD_BOOST_CATALOGUE[hit_name].get("source_type")
                applied_yield_buffs.append({
                    **crit_boost_info, "source_item": f"{hit_name} (Critical)", "source_type": source_type, "count": hit_count
                })

        normal_seeds_count = max(0, seeds_count - total_critical_seeds)
        if normal_seeds_count > 0:
            total_yield += yield_per_normal_seed * Decimal(str(normal_seeds_count))

        average_yield_per_seed = total_yield / Decimal(str(seeds_count)) if seeds_count > 0 else Decimal('0')

        processed_pack = {
            **pack,
            "pack_index": i,
            "is_ready": now_ms >= pack.get("readyAt", float('inf')),
            "oil_cost": float(final_oil_cost),
            "icon_path": get_item_image_path(crop_name),
            "yield_info": {
                "final_deterministic": float(total_yield),
                "average_yield_per_seed": float(average_yield_per_seed),
                "applied_buffs": applied_yield_buffs,
                "breakdown": {
                    "normal_seeds": {
                        "count": normal_seeds_count,
                        "yield_per_seed": float(yield_per_normal_seed),
                        "total_yield": float(yield_per_normal_seed * Decimal(str(normal_seeds_count)))
                    },
                    "critical_hits": total_yield_from_crits_map
                }
            },
        }
        processed_queue.append(processed_pack)

    log.debug(f"Global Oil Buffs Info: {oil_consumption_info}")
    log.debug(f"Global Time Buffs Info: {global_time_buffs_info}")
    
    return {
        "view": {
            "queue": processed_queue,
            "unallocatedOilTime": machine_data.get("unallocatedOilTime", 0),
            "total_oil_cost": float(total_queue_oil_cost),
            "global_oil_buffs": oil_consumption_info,
            "global_time_buffs": global_time_buffs_info,
            "max_queue_size": max_queue_size,
            "used_queue_size": len(queue)
        }
    }
