# app/services/fruit_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import collectiblesItemBuffs as collectibles_domain
from ..domain import fruits as fruit_domain
from ..domain import skills as skills_domain
from ..domain import wearablesItemBuffs as wearables_domain
from . import resource_analysis_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA FRUTAS
# ==============================================================================

FRUIT_RESOURCE_CONDITIONS = {
    'yield_resource_names': list(fruit_domain.FRUIT_SEEDS.keys()),
    'recovery_resource_names': list(fruit_domain.FRUIT_SEEDS.keys()),
    'skill_tree_name': 'Fruit Patch',
    'boost_category_names': ['Fruit']
}

FRUIT_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(FRUIT_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _get_fruit_yield_amount(game_state: dict, fruit_name: str, fertiliser: str, critical_drop) -> dict:
    """
    Calcula o rendimento de uma fruta, espelhando a lógica de `getFruitYield` de fruitHarvested.ts.
    """
    base_amount = Decimal('1')
    additive_bonus = Decimal('0')
    applied_buffs_details = []

    inventory = game_state.get("inventory", {})
    collectibles = {**game_state.get("collectibles", {}), **game_state.get("home", {}).get("collectibles", {})}
    skills = set(game_state.get("bumpkin", {}).get("skills", {}).keys())
    wearables = game_state.get("bumpkin", {}).get("equipped", {})

    def apply_boost(source, value, operation='add', source_type='collectible'):
        nonlocal additive_bonus
        if operation == 'add':
            additive_bonus += Decimal(str(value))
        applied_buffs_details.append({"source_item": source, "value": value, "operation": operation, "source_type": source_type})

    # Bônus de Coletáveis
    if fruit_name == "Apple" and "Lady Bug" in collectibles: apply_boost("Lady Bug", 0.25, 'add', 'collectible')
    if fruit_name == "Blueberry" and "Black Bearry" in collectibles: apply_boost("Black Bearry", 1, 'add', 'collectible')
    if fruit_name == "Banana" and "Banana Chicken" in collectibles: apply_boost("Banana Chicken", 0.1, 'add', 'collectible')
    if fruit_name == "Lemon" and "Lemon Shark" in collectibles: apply_boost("Lemon Shark", 0.2, 'add', 'collectible')
    if fruit_name == "Tomato" and "Tomato Bombard" in collectibles: apply_boost("Tomato Bombard", 1, 'add', 'collectible')
    if fruit_name == "Grape":
        if "Grape Granny" in collectibles: apply_boost("Grape Granny", 1, 'add', 'collectible')
        if "Vinny" in collectibles: apply_boost("Vinny", 0.25, 'add', 'collectible')
    if "Macaw" in collectibles:
        macaw_bonus = 0.2 if "Loyal Macaw" in skills else 0.1
        apply_boost("Macaw" + (" (Loyal)" if "Loyal Macaw" in skills else ""), macaw_bonus)

    # Bônus de Wearables
    if "Camel Onesie" in wearables.values(): apply_boost("Camel Onesie", 0.1, 'add', 'wearable')
    if "Fruit Picker Apron" in wearables.values() and fruit_name in ["Apple", "Orange", "Blueberry", "Banana"]:
        apply_boost("Fruit Picker Apron", 0.1, 'add', 'wearable')
    if fruit_name == "Banana" and "Banana Amulet" in wearables.values(): apply_boost("Banana Amulet", 0.5, 'add', 'wearable')
    if fruit_name == "Lemon" and "Lemon Shield" in wearables.values(): apply_boost("Lemon Shield", 1, 'add', 'wearable')
    if fruit_name == "Grape" and "Grape Pants" in wearables.values(): apply_boost("Grape Pants", 0.2, 'add', 'wearable')

    # Bônus de Skills
    if "Fruitful Fumble" in skills: apply_boost("Fruitful Fumble", 0.1, 'add', 'skill')
    if "Zesty Vibes" in skills:
        zesty_bonus = 1 if fruit_name in ["Tomato", "Lemon"] else -0.25
        apply_boost("Zesty Vibes", zesty_bonus, 'add', 'skill')

    # Bônus de Fertilizante
    if fertiliser == "Fruitful Blend":
        fruitful_blend_bonus = Decimal('0.1')
        if "Fruitful Bounty" in skills:
            fruitful_blend_bonus *= 2
            # Adiciona uma nota sobre o bônus da skill para clareza no popover
            applied_buffs_details.append({"source_item": "Fruitful Bounty", "value": "x2 on Fruitful Blend", "operation": "special", "source_type": "skill"})
        
        apply_boost("Fruitful Blend", float(fruitful_blend_bonus), 'add', 'fertiliser')


    # Bônus de Críticos
    if "Generous Orchard" in skills and critical_drop("Generous Orchard"):
        apply_boost("Generous Orchard (Critical)", 1, 'add', 'skill')

    # Bônus de Eventos (Exemplo)
    # if getActiveCalendarEvent({ game }) === "bountifulHarvest":
    #     apply_boost("Bountiful Harvest", 1)

    final_yield = base_amount + additive_bonus
    return {"final_deterministic": float(final_yield), "applied_buffs": applied_buffs_details}

def _get_fruit_patch_recovery_time(game_state: dict, fruit_name: str) -> dict:
    """
    Calcula o tempo de recuperação de um fruit patch.
    """
    seed_name = fruit_domain.FRUIT_DATA.get(fruit_name, {}).get("seed_name")
    if not seed_name: return {"final": 0, "applied_buffs": []}
    
    base_time = fruit_domain.FRUIT_SEEDS.get(seed_name, {}).get("plantSeconds", 0)
    if base_time == 0: return {"final": 0, "applied_buffs": []}

    active_boosts = resource_analysis_service.get_active_player_boosts(
        resource_analysis_service._get_player_items(game_state),
        FRUIT_BOOST_CATALOGUE,
        {},
        game_state
    )
    
    return resource_analysis_service.calculate_final_recovery_time(base_time, active_boosts, fruit_name)

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_fruit_patches(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todos os fruit patches, calcula bônus e retorna um relatório completo.
    """
    fruit_patches_api_data = farm_data.get("fruitPatches", {})
    analyzed_patches = {}
    summary = defaultdict(lambda: {"total": 0, "ready": 0, "growing": 0, "total_yield": Decimal('0')})
    current_timestamp_ms = int(time.time() * 1000)

    for patch_id, patch_data in fruit_patches_api_data.items():
        fruit_details = patch_data.get("fruit")
        if not fruit_details:
            continue

        fruit_name = fruit_details.get("name")
        if not fruit_name:
            continue

        summary[fruit_name]["total"] += 1
        
        recovery_info = _get_fruit_patch_recovery_time(farm_data, fruit_name)
        final_recovery_ms = recovery_info["final"] * 1000
        
        # Adiciona o tempo de recuperação final (com bônus) ao sumário, se ainda não estiver lá.
        if 'final_recovery_time' not in summary[fruit_name]:
            summary[fruit_name]['final_recovery_time'] = recovery_info.get('final', 0)

        last_harvested_at = fruit_details.get("harvestedAt", fruit_details.get("plantedAt", 0))
        ready_at_ms = last_harvested_at + final_recovery_ms
        is_ready = current_timestamp_ms >= ready_at_ms

        state_name = "Pronto" if is_ready else "Crescendo"
        summary[fruit_name]["ready" if is_ready else "growing"] += 1

        fertiliser_name = patch_data.get("fertiliser", {}).get("name")
        has_yield_fertiliser = False
        if fertiliser_name == "Fruitful Blend":
            has_yield_fertiliser = True

        critical_hits = fruit_details.get("criticalHit", {})
        critical_hits_tracker = (fruit_details.get("criticalHit") or {}).copy()
        def critical_drop_simulator(name: str) -> bool:
            if critical_hits_tracker.get(name, 0) > 0:
                critical_hits_tracker[name] -= 1
                return True
            return False

        yield_info = _get_fruit_yield_amount(
            game_state=farm_data,
            fruit_name=fruit_name,
            fertiliser=fertiliser_name,
            critical_drop=critical_drop_simulator
        )
        summary[fruit_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        analyzed_patches[patch_id] = {
            "id": patch_id,
            "fruit_name": fruit_name,
            "state_name": state_name,
            "harvests_left": fruit_details.get("harvestsLeft", 0),
            "ready_at_timestamp_ms": int(ready_at_ms),
            "harvests_left": fruit_details.get("harvestsLeft", 0),
            "calculations": {"yield": yield_info, "recovery": recovery_info},
            "fertiliser": patch_data.get("fertiliser"),
            "critical_hits": critical_hits,
            "has_yield_fertiliser": has_yield_fertiliser,
        }

    view_data = {
        "summary_by_fruit": dict(sorted(summary.items())),
        "patch_status": dict(sorted(analyzed_patches.items())),
    }

    return {"view": view_data}