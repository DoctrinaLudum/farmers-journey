# app/services/flower_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import collectiblesItemBuffs as collectibles_domain
from ..domain import flowers as flower_domain
from ..domain import seeds as seeds_domain
from ..domain import skills as skills_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA FLORES
# ==============================================================================

FLOWER_RESOURCE_CONDITIONS = {
    'yield_resource_names': list(flower_domain.FLOWER_DATA.keys()),
    'recovery_resource_names': list(flower_domain.FLOWER_DATA.keys()), # Mesmo que yield para flores
    'skill_tree_name': 'Bees & Flowers',
    'boost_category_names': ['Flower']
}

FLOWER_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(FLOWER_RESOURCE_CONDITIONS)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA COLMEIAS (BEEHIVES)
# ==============================================================================

BEEHIVE_RESOURCE_CONDITIONS = {
    'yield_resource_names': ['Honey'],
    'recovery_resource_names': ['Beehive'], # 'Beehive' pode ser usado para bônus de tempo
    'skill_tree_name': 'Bees & Flowers',
    'boost_category_names': ['Honey']
}

BEEHIVE_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(BEEHIVE_RESOURCE_CONDITIONS)
DEFAULT_HONEY_PRODUCTION_TIME_SECONDS = 24 * 60 * 60 # 24 horas

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _get_flower_yield_amount(game_state: dict, critical_drop: callable) -> dict:
    """
    Calcula o rendimento de uma flor, espelhando a lógica de `getFlowerAmount` de harvestFlower.ts.
    O rendimento de flores é inteiramente baseado em bônus de acertos críticos.
    """
    base_amount = Decimal('1')
    additive_bonus = Decimal('0')
    applied_buffs_details = []

    # Get player's collectibles and skills
    collectibles = set(game_state.get("collectibles", {}).keys())
    skills = set(game_state.get("bumpkin", {}).get("skills", {}).keys())

    def apply_boost(source, value, operation='add', source_type='collectible'):
        nonlocal additive_bonus
        if operation == 'add':
            additive_bonus += Decimal(str(value))
        applied_buffs_details.append({"source_item": source, "value": value, "operation": operation, "source_type": source_type})

    # Bônus de Críticos de Coletáveis
    if "Humming Bird" in collectibles and critical_drop("Humming Bird"): apply_boost("Humming Bird (Critical)", 1, 'add', 'collectible')
    if "Butterfly" in collectibles and critical_drop("Butterfly"): apply_boost("Butterfly (Critical)", 1, 'add', 'collectible')
    if "Desert Rose" in collectibles and critical_drop("Desert Rose"): apply_boost("Desert Rose (Critical)", 1, 'add', 'collectible')
    if "Chicory" in collectibles and critical_drop("Chicory"): apply_boost("Chicory (Critical)", 1, 'add', 'collectible')

    # Bônus de Críticos de Skills
    if "Petalled Perk" in skills and critical_drop("Petalled Perk"):
        apply_boost("Petalled Perk (Critical)", 1, 'add', 'skill')

    final_yield = base_amount + additive_bonus
    return {"final_deterministic": float(final_yield), "applied_buffs": applied_buffs_details}

def _get_flower_growth_time(game_state: dict, flower_name: str, base_time: int) -> dict:
    """Calcula o tempo de crescimento de uma flor a partir de um tempo base fornecido."""
    if base_time == 0: return {"final": 0, "applied_buffs": []}

    active_boosts = resource_analysis_service.get_active_player_boosts(
        resource_analysis_service._get_player_items(game_state),
        FLOWER_BOOST_CATALOGUE,
        {},
        game_state
    )
    
    return resource_analysis_service.calculate_final_recovery_time(base_time, active_boosts, flower_name)

def _get_honey_yield_amount(game_state: dict) -> dict:
    """
    Calcula o rendimento de mel por colmeia cheia, espelhando a lógica de `getHoneyMultiplier` de harvestBeehive.ts.
    """
    base_amount = Decimal('1')
    multiplier = Decimal('1')
    applied_buffs_details = []

    collectibles = {**game_state.get("collectibles", {}), **game_state.get("home", {}).get("collectibles", {})}
    skills = set(game_state.get("bumpkin", {}).get("skills", {}).keys())
    wearables = game_state.get("bumpkin", {}).get("equipped", {})

    def apply_boost(source, value, operation='add_to_multiplier', source_type='collectible'):
        nonlocal multiplier
        if operation == 'add_to_multiplier':
            multiplier += Decimal(str(value))
        applied_buffs_details.append({"source_item": source, "value": value, "operation": operation, "source_type": source_type})

    # Bônus de Wearables
    if "Bee Suit" in wearables.values(): apply_boost("Bee Suit", 0.1, 'add_to_multiplier', 'wearable')
    if "Honeycomb Shield" in wearables.values(): apply_boost("Honeycomb Shield", 1, 'add_to_multiplier', 'wearable')

    # Bônus de Skills
    if "Sweet Bonus" in skills: apply_boost("Sweet Bonus", 0.1, 'add_to_multiplier', 'skill')

    # Bônus de Coletáveis
    if "King of Bears" in collectibles: apply_boost("King of Bears", 0.25)

    final_yield = base_amount * multiplier
    return {"final_deterministic": float(final_yield), "applied_buffs": applied_buffs_details}

def _get_honey_production_time(game_state: dict, hive_data: dict) -> dict:
    """
    Calcula o tempo de produção de mel para uma colmeia, considerando flores e bônus.
    """
    base_time = DEFAULT_HONEY_PRODUCTION_TIME_SECONDS
    speed_multiplier = Decimal('1')
    applied_buffs_details = []

    collectibles = {**game_state.get("collectibles", {}), **game_state.get("home", {}).get("collectibles", {})}
    wearables = game_state.get("bumpkin", {}).get("equipped", {})
    skills = set(game_state.get("bumpkin", {}).get("skills", {}).keys())

    def apply_boost(source, value, operation='add_to_speed', source_type='collectible'):
        nonlocal speed_multiplier
        if operation == 'add_to_speed':
            speed_multiplier += Decimal(str(value))
        applied_buffs_details.append({"source_item": source, "value": value, "operation": operation, "source_type": source_type})

    # Bônus de flores anexadas
    attached_flowers = len(hive_data.get("flowers", []))
    if attached_flowers > 0:
        flower_bonus = attached_flowers * 0.02
        apply_boost(f"{attached_flowers} Flores", flower_bonus, 'add_to_speed', 'game_mechanic')

    # Bônus de Coletáveis e Wearables
    if "Queen Bee" in collectibles: apply_boost("Queen Bee", 1, 'add_to_speed', 'collectible')
    if "Beekeeper Hat" in wearables.values(): apply_boost("Beekeeper Hat", 0.2, 'add_to_speed', 'wearable')
    
    # Bônus de Skills
    if "Hyper Bees" in skills: apply_boost("Hyper Bees", 0.1, 'add_to_speed', 'skill')

    final_time = base_time / float(speed_multiplier) if speed_multiplier > 0 else float('inf')

    return {"base": base_time, "final": final_time, "applied_buffs": applied_buffs_details, "speed_multiplier": float(speed_multiplier)}


# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_flower_beds(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todos os canteiros de flores, calcula bônus e retorna um relatório completo.
    """
    flower_beds_api_data = farm_data.get("flowers", {}).get("flowerBeds", {})
    analyzed_beds = {}
    summary = defaultdict(lambda: {"total": 0, "ready": 0, "growing": 0, "total_yield": Decimal('0')})
    current_timestamp_ms = int(time.time() * 1000)

    for bed_id, bed_data in flower_beds_api_data.items():
        flower_details = bed_data.get("flower")
        if not flower_details: continue

        flower_name = flower_details.get("name")
        if not flower_name: continue

        summary[flower_name]["total"] += 1
        
        planted_at_ms = flower_details.get("plantedAt", 0)

        # Busca o tempo base da fonte correta.
        seed_name = flower_domain.FLOWER_DATA.get(flower_name, {}).get("seed")
        base_growth_seconds = seeds_domain.SEEDS_DATA.get(seed_name, {}).get("plant_seconds", 0)

        # --- ALTERAÇÃO 1: CALCULAR O TIMESTAMP DE COLHEITA COM O TEMPO BASE ---
        # De acordo com a lógica do jogo (harvestFlower.ts), a colheita só depende do tempo base.
        base_growth_ms = base_growth_seconds * 1000
        harvest_ready_at_ms = planted_at_ms + base_growth_ms
        is_ready = current_timestamp_ms >= harvest_ready_at_ms
        
        summary[flower_name]["ready" if is_ready else "growing"] += 1

        # --- ALTERAÇÃO 2: CALCULAR O TEMPO TOTAL (COM BÔNUS) SEPARADAMENTE ---
        # Este valor continua a ser útil para o "Tempo Final" no sumário.
        growth_time_info_with_bonuses = _get_flower_growth_time(farm_data, flower_name, base_growth_seconds)
        final_growth_seconds = growth_time_info_with_bonuses.get('final', base_growth_seconds)

        # Adiciona o tempo de crescimento final (com bônus) ao sumário, se ainda não estiver lá.
        if 'final_recovery_time' not in summary[flower_name]:
            summary[flower_name]['final_recovery_time'] = final_growth_seconds

        # Simula os acertos críticos para o cálculo do rendimento
        critical_hits_tracker = (flower_details.get("criticalHit") or {}).copy()
        def critical_drop_simulator(name: str) -> bool:
            if critical_hits_tracker.get(name, 0) > 0:
                critical_hits_tracker[name] -= 1
                return True
            return False

        yield_info = _get_flower_yield_amount(farm_data, critical_drop_simulator)
        summary[flower_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        analyzed_beds[bed_id] = {
            "id": bed_id, "flower_name": flower_name,
            "state_name": "Pronta" if is_ready else "Crescendo",
            # --- ALTERAÇÃO 3: USAR O TIMESTAMP DE COLHEITA CORRETO ---
            "ready_at_timestamp_ms": int(harvest_ready_at_ms),
            "calculations": {
                "yield": yield_info,
                # Mantemos o cálculo com bônus aqui para fins de exibição detalhada se necessário
                "growth": growth_time_info_with_bonuses
            },
            "cross_breed": flower_details.get("crossbreed"),
            "critical_hits": flower_details.get("criticalHit", {}),
        }

    return {"view": {
        "beds": dict(sorted(analyzed_beds.items())),
        "summary_by_flower": dict(sorted(summary.items()))
    }}

def analyze_beehives(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todas as colmeias, calcula bônus e retorna um relatório completo.
    """
    beehives_api_data = farm_data.get("beehives", {})
    if not beehives_api_data:
        return None

    analyzed_hives = {}
    current_timestamp_ms = int(time.time() * 1000)

    for hive_id, hive_data in beehives_api_data.items():
        honey_details = hive_data.get("honey", {})
        
        # Calcula o tempo de produção de mel
        production_time_info = _get_honey_production_time(farm_data, hive_data)
        final_production_time_seconds = production_time_info.get("final", DEFAULT_HONEY_PRODUCTION_TIME_SECONDS)
        
        # Lógica de updateBeehives.ts para calcular o progresso atual
        honey_updated_at = honey_details.get("updatedAt", 0)
        honey_produced_at_last_update = honey_details.get("produced", 0)
        time_since_update_seconds = (current_timestamp_ms - honey_updated_at) / 1000
        new_honey_produced = honey_produced_at_last_update + time_since_update_seconds
        
        total_honey_produced_seconds = min(new_honey_produced, final_production_time_seconds)
        
        is_ready = total_honey_produced_seconds >= final_production_time_seconds
        state_name = "Pronta" if is_ready else "Produzindo"
        
        time_to_full_seconds = final_production_time_seconds - total_honey_produced_seconds
        ready_at_ms = current_timestamp_ms + (time_to_full_seconds * 1000)
            
        yield_info = _get_honey_yield_amount(farm_data)
        
        analyzed_hives[hive_id] = {
            "id": hive_id, "resource_name": "Beehive",
            "state_name": state_name, "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "recovery": production_time_info},
            "bonus_reward": None
        }

    return {"view": {"hives": dict(sorted(analyzed_hives.items()))}}

def analyze_beehives(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todas as colmeias, calcula bônus e retorna um relatório completo.
    """
    beehives_api_data = farm_data.get("beehives", {})
    if not beehives_api_data:
        return None

    analyzed_hives = {}
    current_timestamp_ms = int(time.time() * 1000)

    for hive_id, hive_data in beehives_api_data.items():
        honey_details = hive_data.get("honey", {})
        
        # Calcula o tempo de produção de mel
        production_time_info = _get_honey_production_time(farm_data, hive_data)
        final_production_time_seconds = production_time_info.get("final", DEFAULT_HONEY_PRODUCTION_TIME_SECONDS)
        
        # Lógica de updateBeehives.ts para calcular o progresso atual
        honey_updated_at = honey_details.get("updatedAt", 0)
        honey_produced_at_last_update = honey_details.get("produced", 0)
        time_since_update_seconds = (current_timestamp_ms - honey_updated_at) / 1000
        new_honey_produced = honey_produced_at_last_update + time_since_update_seconds
        
        total_honey_produced_seconds = min(new_honey_produced, final_production_time_seconds)
        
        is_ready = total_honey_produced_seconds >= final_production_time_seconds
        state_name = "Pronta" if is_ready else "Produzindo"
        
        time_to_full_seconds = final_production_time_seconds - total_honey_produced_seconds
        ready_at_ms = current_timestamp_ms + (time_to_full_seconds * 1000)
            
        yield_info = _get_honey_yield_amount(farm_data)
        
        analyzed_hives[hive_id] = {
            "id": hive_id, "resource_name": "Beehive",
            "state_name": state_name, "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "recovery": production_time_info},
            "bonus_reward": None
        }

    return {"view": {"hives": dict(sorted(analyzed_hives.items()))}}