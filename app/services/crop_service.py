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

BUD_BUFF_TO_CROP_BOOST_MAPPING = {
    'CROP_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'category': 'Crop'}},
    'CROP_GROWTH_TIME': {'type': 'GROWTH_TIME', 'operation': 'percentage', 'conditions': {'category': 'Crop'}},
    'FRUIT_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'category': 'Fruit'}},
    'FRUIT_GROWTH_TIME': {'type': 'GROWTH_TIME', 'operation': 'percentage', 'conditions': {'category': 'Fruit'}},
    'FLOWER_YIELD': {'type': 'YIELD', 'operation': 'add', 'conditions': {'category': 'Flower'}},
    'FLOWER_GROWTH_TIME': {'type': 'GROWTH_TIME', 'operation': 'percentage', 'conditions': {'category': 'Flower'}},
}

CROP_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(CROP_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _get_crop_yield_amount(game_state: dict, plot: dict, crop_name: str, critical_drop) -> dict:
    """
    Calcula o rendimento de uma cultura, espelhando getCropYieldAmount de harvest.ts.
    Esta função é complexa e contém a lógica de negócio específica para culturas.
    """
    # A lógica genérica de `calculate_final_yield` não é suficiente aqui.
    # Reimplementamos a lógica específica de `harvest.ts` para máxima fidelidade.
    
    base_amount = Decimal('1')
    multiplier = Decimal('1')
    additive_bonus = Decimal('0')
    applied_buffs_details = []

    inventory = game_state.get("inventory", {})
    collectibles = {**game_state.get("collectibles", {}), **game_state.get("home", {}).get("collectibles", {})}
    skills = set(game_state.get("bumpkin", {}).get("skills", {}).keys())
    
    # Função auxiliar para adicionar um bônus e rastreá-lo, agora com source_type
    def apply_boost(source, value, operation, source_type='collectible'):
        nonlocal base_amount, multiplier, additive_bonus
        if operation == 'add':
            additive_bonus += Decimal(str(value))
        elif operation == 'multiply':
            multiplier *= Decimal(str(value))
        applied_buffs_details.append({"source_item": source, "value": value, "operation": operation, "source_type": source_type})

    # Bônus específicos de itens
    if crop_name == "Cauliflower" and "Golden Cauliflower" in collectibles:
        apply_boost("Golden Cauliflower", 2, 'multiply', 'collectible')
    if crop_name == "Carrot" and "Easter Bunny" in collectibles:
        apply_boost("Easter Bunny", 1.2, 'multiply', 'collectible')
    if crop_name == "Pumpkin" and "Victoria Sisters" in collectibles:
        apply_boost("Victoria Sisters", 1.2, 'multiply', 'collectible')

    # Bônus de espantalhos (hierárquico)
    if "Kuebiko" in collectibles:
        apply_boost("Kuebiko", 1.2, 'multiply', 'collectible')
    elif "Scarecrow" in collectibles:
        apply_boost("Scarecrow", 1.2, 'multiply', 'collectible')
    elif "Nancy" in collectibles:
        # Nancy não tem bônus de yield, apenas de tempo
        pass

    # Bônus de Fertilizante
    if plot.get("fertiliser", {}).get("name") == "Sprout Mix":
        apply_boost("Sprout Mix", 0.2, 'add', 'fertiliser')
        if "Knowledge Crab" in collectibles:
            apply_boost("Knowledge Crab", 0.2, 'add', 'collectible')

    # Bônus de Enxame de Abelhas
    if plot.get("beeSwarm"):
        bee_bonus = Decimal('0.2')
        if "Pollen Power Up" in skills:
            bee_bonus += Decimal('0.1')
            apply_boost("Pollen Power Up", 0.1, 'add', 'skill')
        apply_boost("Bee Swarm", float(bee_bonus), 'add', 'game_mechanic')

    # Outros bônus aditivos e de skills
    if crop_name == "Cabbage":
        if "Cabbage Boy" in collectibles:
            cabbage_bonus = Decimal('0.25')
            if "Cabbage Girl" in collectibles:
                cabbage_bonus += Decimal('0.25')
                apply_boost("Cabbage Girl", 0.25, 'add', 'collectible')
            apply_boost("Cabbage Boy", float(cabbage_bonus), 'add', 'collectible')
        elif "Karkinos" in collectibles:
            apply_boost("Karkinos", 0.1, 'add', 'collectible')

    # ... (Adicionar todos os outros `if` statements de `harvest.ts` aqui) ...
    # Exemplo:
    if crop_name == "Kale" and "Foliant" in collectibles:
        apply_boost("Foliant", 0.2, 'add', 'collectible')
    if "Infernal Pitchfork" in inventory:
        apply_boost("Infernal Pitchfork", 3, 'add', 'tool')

    # Bônus de AOE (reutilizando a lógica genérica)
    plot_position = {"x": plot.get("x"), "y": plot.get("y")}
    aoe_boosts = resource_analysis_service.get_aoe_boosts_for_resource(plot_position, collectibles, skills, game_state)
    for boost in aoe_boosts:
        if resource_analysis_service._conditions_are_met(boost.get("conditions", {}), crop_name, {}):
            apply_boost(boost['source_item'], boost['value'], boost['operation'])

    # Bônus de Críticos (lidos do estado do plot)
    critical_hits = plot.get("crop", {}).get("criticalHit", {})
    if critical_hits.get("Potent Potato") and critical_drop("Potent Potato"):
        apply_boost("Potent Potato (Critical)", 10, 'add', 'collectible')
    if critical_hits.get("Stellar Sunflower") and critical_drop("Stellar Sunflower"):
        apply_boost("Stellar Sunflower (Critical)", 10, 'add', 'collectible')
    if critical_hits.get("Radical Radish") and critical_drop("Radical Radish"):
        apply_boost("Radical Radish (Critical)", 10, 'add', 'collectible')
    # ... (adicionar outros críticos) ...

    # Bônus de Eventos
    # ... (lógica para `bountifulHarvest`, `insectPlague`, etc.) ...

    final_yield = (base_amount * multiplier) + additive_bonus
    return {"final_deterministic": float(final_yield), "applied_buffs": applied_buffs_details}

def _get_crop_growth_time(game_state: dict, crop_name: str, plot: dict) -> dict:
    """
    Calcula o tempo de crescimento de uma cultura, espelhando a lógica de `plant.ts`.
    """
    base_time = crops_domain.CROPS.get(crop_name, {}).get("harvestSeconds", 0)
    if base_time == 0:
        return {"final": 0, "applied_buffs": []}

    # A lógica de cálculo de tempo pode ser reutilizada do `resource_analysis_service`
    # pois é principalmente multiplicativa.
    active_boosts = resource_analysis_service.get_active_player_boosts(
        resource_analysis_service._get_player_items(game_state),
        CROP_BOOST_CATALOGUE,
        NON_CUMULATIVE_BOOST_GROUPS,
        game_state
    )
    
    return resource_analysis_service.calculate_final_recovery_time(base_time, active_boosts, crop_name)

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_crop_resources(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todos os canteiros de culturas, calcula os bônus e retorna um
    relatório completo, usando a lógica de cálculo interna.
    """
    player_items = resource_analysis_service._get_player_items(farm_data)
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items, CROP_BOOST_CATALOGUE, NON_CUMULATIVE_BOOST_GROUPS, farm_data
    )
    
    # ... (lógica para adicionar buffs de Bud, similar a outros serviços) ...

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
        
        # Adiciona o tempo base de crescimento ao sumário
        base_growth_seconds = crops_domain.CROPS.get(crop_name, {}).get("harvestSeconds", 0)
        summary[crop_name]['base_recovery_time'] = base_growth_seconds
        
        # Lógica de cálculo de tempo de crescimento
        growth_time_info = _get_crop_growth_time(farm_data, crop_name, plot_data)
        final_growth_ms = growth_time_info["final"] * 1000
        
        planted_at_ms = crop_details.get("plantedAt", 0)
        ready_at_ms = planted_at_ms + final_growth_ms

        # Lógica correta para 'Rapid Root', que reduz o tempo restante em 50%.
        # Isso é aplicado após o cálculo do tempo de crescimento com todos os outros bônus.
        fertiliser_details = plot_data.get("fertiliser")
        if fertiliser_details and fertiliser_details.get("name") == "Rapid Root":
            fertilised_at_ms = fertiliser_details.get("fertilisedAt", 0)
            
            # Só aplica se foi fertilizado após o plantio e antes de estar pronto
            if fertilised_at_ms > planted_at_ms and current_timestamp_ms < ready_at_ms:
                time_remaining_at_fertilisation_ms = ready_at_ms - fertilised_at_ms
                
                if time_remaining_at_fertilisation_ms > 0:
                    time_reduction_ms = time_remaining_at_fertilisation_ms / 2
                    ready_at_ms -= time_reduction_ms
                    
                    # Adiciona o bônus à lista para ser exibido na UI
                    growth_time_info["applied_buffs"].append({"source_item": "Rapid Root", "value": "-50% Tempo Restante", "operation": "special"})

        # Verifica se há um fertilizante de rendimento para o ícone do mapa
        has_yield_fertiliser = False
        if fertiliser_details and fertiliser_details.get("name") == "Sprout Mix":
            has_yield_fertiliser = True

        is_ready = current_timestamp_ms >= ready_at_ms

        state_name = "Pronta" if is_ready else "Crescendo"
        summary[crop_name]["ready" if is_ready else "growing"] += 1

        # Lógica de cálculo de rendimento
        critical_hits = crop_details.get("criticalHit", {})
        critical_hits_tracker = (crop_details.get("criticalHit") or {}).copy()
        def critical_drop_simulator(name: str) -> bool:
            if critical_hits_tracker.get(name, 0) > 0:
                critical_hits_tracker[name] -= 1
                return True
            return False

        yield_info = _get_crop_yield_amount(
            game_state=farm_data,
            plot=plot_data,
            crop_name=crop_name,
            critical_drop=critical_drop_simulator
        )
        summary[crop_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        # Extrai as recompensas bônus (ex: sementes extras)
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
        }

    view_data = {
        "summary_by_crop": dict(sorted(summary.items())),
        "plot_status": dict(sorted(analyzed_plots.items())),
        # ... (outros dados para a view como active_boost_items, etc.) ...
    }

    return {"view": view_data}