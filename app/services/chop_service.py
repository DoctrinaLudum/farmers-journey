# app/services/chop_service.py

import copy
import logging
import time
from collections import defaultdict
from decimal import Decimal

from ..domain import collectiblesItemBuffs as collectibles_domain
from ..domain import resources as resources_domain
from ..domain import skills as skills_domain
from ..domain import wearablesItemBuffs as wearables_domain, upgradables as upgradables_domain, tools as tools_domain
from . import bud_service

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA MADEIRA
# ==============================================================================

# Define quais recursos e bônus são relevantes para a madeira.
WOOD_RESOURCE_CONDITIONS = {
    'yield_resource_names': ['Wood'],
    'recovery_resource_names': ['Tree'],
    'cost_resource_names': ['Axe'],
    'skill_tree_name': 'Trees',
}

# Itens que não se acumulam (ex: castores de níveis diferentes).
# A ordem é do melhor para o pior.
NON_CUMULATIVE_BOOST_GROUPS = {
    "beavers": ["Foreman Beaver", "Apprentice Beaver", "Woody the Beaver"],
}

TREE_RECOVERY_TIME_SECONDS = 2 * 60 * 60  # 2 horas em segundos

# ==============================================================================
# FUNÇÕES AUXILIARES (LÓGICA INTERNALIZADA)
# ==============================================================================

def _get_all_item_data() -> dict:
    """Unifica todos os dicionários de domínio em um só para fácil acesso."""
    return {
        **skills_domain.LEGACY_BADGES,
        **skills_domain.BUMPKIN_REVAMP_SKILLS,
        **wearables_domain.WEARABLES_ITEM_BUFFS,
        **collectibles_domain.COLLECTIBLES_ITEM_BUFFS,
        **resources_domain.RESOURCES_DATA,
        **upgradables_domain.ALL_UPGRADABLES,
    }

def _get_player_items(farm_data: dict) -> set:
    """Extrai e unifica todos os itens que um jogador possui."""
    player_items = set(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())
    
    bumpkin = farm_data.get("bumpkin", {})
    if bumpkin:
        player_items.update(bumpkin.get("equipped", {}).values())
        player_items.update(bumpkin.get("skills", {}).keys())

    farm_hands_data = farm_data.get("farmHands", {}).get("bumpkins", {})
    if farm_hands_data:
        for hand in farm_hands_data.values():
            player_items.update(hand.get("equipped", {}).values())

    player_items.update(farm_data.get("inventory", {}).keys())
    return player_items

def _filter_boosts_for_wood(all_item_data: dict) -> dict:
    """
    Cria um catálogo contendo apenas os itens e bônus relevantes para madeira.
    """
    boost_catalogue = {}
    yield_names = WOOD_RESOURCE_CONDITIONS['yield_resource_names']
    recovery_names = WOOD_RESOURCE_CONDITIONS['recovery_resource_names']
    skill_tree = WOOD_RESOURCE_CONDITIONS['skill_tree_name']

    for item_name, item_details in all_item_data.items():
        boost_list = item_details.get("boosts") or item_details.get("effects")
        if not item_details or not boost_list or not item_details.get("enabled", True):
            continue

        # Filtra para incluir apenas skills da árvore 'Trees' ou skills sem árvore definida (como 'Native')
        if skill_tree and item_name in skills_domain.BUMPKIN_REVAMP_SKILLS and item_details.get("tree") and item_details.get("tree") != skill_tree:
            continue

        is_item_relevant = False
        relevant_boosts = []

        for boost in boost_list:
            conditions = boost.get("conditions", {})
            resource_name_or_list = conditions.get("resource") or conditions.get("item")
            boost_type = boost.get("type")
            
            is_boost_relevant = False
            # Verifica se o bônus afeta diretamente 'Wood' ou 'Tree'
            if resource_name_or_list:
                resource_names_to_check = resource_name_or_list if isinstance(resource_name_or_list, list) else [resource_name_or_list]
                if (boost_type in ["YIELD", "RESOURCE_YIELD"] and any(name in yield_names for name in resource_names_to_check)) or \
                   (boost_type in ["RECOVERY_TIME", "GROWTH_TIME", "TREE_RECOVERY_TIME"] and any(name in recovery_names for name in resource_names_to_check)) or \
                   (boost_type == "COST" and any(name in WOOD_RESOURCE_CONDITIONS['cost_resource_names'] for name in resource_names_to_check)) or \
                   (boost_type == "CRITICAL_CHANCE" and any(name in yield_names for name in resource_names_to_check)):
                    is_boost_relevant = True
            
            # Habilidade 'Native' é relevante
            if item_name == "Native":
                is_boost_relevant = True

            if is_boost_relevant:
                is_item_relevant = True
                standardized_boost = boost.copy()
                if boost.get("type") in ["YIELD", "RESOURCE_YIELD"]:
                    standardized_boost['type'] = 'YIELD'
                elif boost.get("type") in ["RECOVERY_TIME", "GROWTH_TIME", "TREE_RECOVERY_TIME"]:
                    standardized_boost['type'] = 'RECOVERY_TIME'
                elif boost.get("type") == "COST":
                    standardized_boost['type'] = 'COST'
                relevant_boosts.append(standardized_boost)

        if is_item_relevant:
            if item_name in skills_domain.LEGACY_BADGES:
                source_type = "skill_legacy"
            elif item_name in skills_domain.BUMPKIN_REVAMP_SKILLS:
                source_type = "skill"
            elif item_name in wearables_domain.WEARABLES_ITEM_BUFFS:
                source_type = "wearable"
            else:
                source_type = "collectible"

            boost_catalogue[item_name] = {
                "boosts": relevant_boosts,
                "source_type": source_type
            }
    return boost_catalogue

def _get_active_player_boosts(player_items: set, wood_boost_catalogue: dict, farm_data: dict) -> list:
    """
    Determina a lista de bônus de madeira ativos para o jogador.
    """
    active_boosts = []
    
    # 1. Processa grupos não cumulativos (beavers)
    for item_name in NON_CUMULATIVE_BOOST_GROUPS["beavers"]:
        if item_name in player_items and item_name in wood_boost_catalogue:
            source_type = wood_boost_catalogue[item_name].get("source_type")
            for boost in wood_boost_catalogue[item_name]["boosts"]:
                active_boosts.append({"source_item": item_name, "source_type": source_type, **boost})
            break # Aplica apenas o melhor e para

    # 2. Processa bônus cumulativos
    beaver_items = set(NON_CUMULATIVE_BOOST_GROUPS["beavers"])
    for item_name in player_items:
        if item_name in wood_boost_catalogue and item_name not in beaver_items:
            source_type = wood_boost_catalogue[item_name].get("source_type")
            item_boosts = wood_boost_catalogue[item_name]["boosts"]
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)

            for boost in item_boosts:
                # Bônus de YIELD de itens de crítico são aplicados apenas no acerto crítico,
                # então não são adicionados à lista de bônus ativos base.
                if is_critical_item and boost.get("type") == "YIELD":
                    continue
                active_boosts.append({"source_item": item_name, "source_type": source_type, **boost})

    # 3. Processa bônus de Buds
    bud_analysis = bud_service.analyze_bud_buffs(farm_data)
    if bud_analysis:
        active_bud_buffs = bud_analysis["internal"]["active_buffs"]
        winning_bud_info = bud_analysis["internal"]["winning_bud_info"]
        
        if 'WOOD_YIELD' in active_bud_buffs:
            source_bud = winning_bud_info.get('WOOD_YIELD')
            source_item_name = f"Bud #{source_bud['bud_id']} ({source_bud['type']}, {source_bud['aura']})" if source_bud else "Buds"
            active_boosts.append({
                "type": "YIELD", "operation": "add",
                "value": active_bud_buffs['WOOD_YIELD'],
                "source_item": source_item_name, "source_type": "bud"
            })
        if 'TREE_RECOVERY_TIME' in active_bud_buffs:
            source_bud = winning_bud_info.get('TREE_RECOVERY_TIME')
            source_item_name = f"Bud #{source_bud['bud_id']} ({source_bud['type']}, {source_bud['aura']})" if source_bud else "Buds"
            active_boosts.append({
                "type": "RECOVERY_TIME", "operation": "percentage",
                "value": active_bud_buffs['TREE_RECOVERY_TIME'],
                "source_item": source_item_name, "source_type": "bud"
            })

    return active_boosts

def _extract_and_process_temporal_boosts(active_boosts: list, farm_data: dict) -> tuple:
    """Separa bônus temporais e anexa seus timestamps de ativação."""
    temporal_boosts_processed = []
    regular_boosts = []
    temporal_item_names = set()

    all_placed_items = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}

    for boost in active_boosts:
        conditions = boost.get("conditions", {})
        duration_hours = conditions.get("duration_hours")
        duration_days = conditions.get("duration_days")

        if duration_hours or duration_days:
            item_name = boost.get("source_item")
            placements = all_placed_items.get(item_name, [])
            if placements:
                activation_ts = placements[0].get("createdAt", 0)
                temporal_boosts_processed.append({"boost": boost, "activation_ts": activation_ts})
                temporal_item_names.add(item_name)
        else:
            regular_boosts.append(boost)
            
    return temporal_boosts_processed, regular_boosts, temporal_item_names

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA ESPECÍFICA)
# ==============================================================================

def _get_wood_drop_amount(active_boosts: list, tree_multiplier: int = 1, tree_tier: int = 1) -> dict:
    """Calcula o rendimento de madeira com base nos bônus ativos."""
    # O rendimento base é multiplicado pelo tier da árvore
    # CORREÇÃO DA ORDEM DE OPERAÇÕES:
    # A base para cálculo de bônus é sempre 1. Bônus multiplicativos são aplicados primeiro, depois os aditivos.
    base = Decimal('1.0')
    additive_bonus = Decimal('0')
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    for boost in active_boosts:
        if boost.get("type") == "YIELD":
            operation = boost["operation"]
            value = Decimal(str(boost["value"]))
            
            if operation == "add":
                additive_bonus += value
            elif operation == "multiply":
                multiplicative_factor *= value
            
            applied_buffs_details.append(boost)

    # Lógica correta de cálculo, espelhando chop.ts:
    # 1. Aplica bônus multiplicativos à base 1, e DEPOIS soma os bônus aditivos.
    yield_with_boosts = (base * multiplicative_factor) + additive_bonus
    # 2. Multiplica o resultado pelo multiplicador do tier da árvore (passo que já estava correto).
    final_deterministic = yield_with_boosts * Decimal(str(tree_multiplier))

    # Adiciona o bônus aditivo específico do tier, conforme a lógica do chop.ts
    if tree_tier == 2:
        final_deterministic += Decimal('0.5')
        applied_buffs_details.append({"source_item": "Tier 2 Tree Bonus", "type": "YIELD", "operation": "add", "value": 0.5, "source_type": "game_mechanic"})
    elif tree_tier == 3:
        final_deterministic += Decimal('2.5')
        applied_buffs_details.append({"source_item": "Tier 3 Tree Bonus", "type": "YIELD", "operation": "add", "value": 2.5, "source_type": "game_mechanic"})



    return {
        "base": float(base * Decimal(str(tree_multiplier))), # A base para exibição considera o multiplicador
        "final_deterministic": float(final_deterministic),
        "applied_buffs": applied_buffs_details
    }

def _get_tree_recovery_time(active_boosts: list) -> dict:
    """Calcula o tempo de recuperação da árvore com base nos bônus ativos."""
    base_time = Decimal(str(TREE_RECOVERY_TIME_SECONDS))
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []
    
    for boost in active_boosts:
        if boost.get("type") == "RECOVERY_TIME":
            operation = boost["operation"]
            value = Decimal(str(boost["value"]))

            if operation == "percentage":
                multiplicative_factor *= (Decimal('1') - abs(value)) # Reduções são negativas
            elif operation == "multiply":
                multiplicative_factor *= value
            elif operation == "subtract_hours":
                base_time -= (value * 3600)

            applied_buffs_details.append(boost)

    final_time_seconds = base_time * multiplicative_factor
    # Calcula a REDUÇÃO de tempo (buff), espelhando a lógica do chop.ts
    time_reduction_seconds = float(base_time - final_time_seconds)

    return {
        "base": float(TREE_RECOVERY_TIME_SECONDS),
        "final": float(final_time_seconds),
        "reduction_seconds": time_reduction_seconds,
        "applied_buffs": applied_buffs_details
    }

def _get_axe_cost_and_quantity_info(active_boosts: list) -> dict:
    """
    Calcula o custo do machado e a quantidade necessária por tier de árvore.
    """
    base_cost = Decimal(str(tools_domain.TOOLS_DATA.get("Axe", {}).get("price", 0)))
    cost_multiplier = Decimal('1')
    cost_buffs = []
    
    # Caso especial: Foreman Beaver zera o custo
    if any(b.get("source_item") == "Foreman Beaver" for b in active_boosts):
        return {
            "cost_per_axe": 0.0,
            "applied_cost_buffs": [{"source_item": "Foreman Beaver", "value": "Custo Zero", "operation": "special", "source_type": "collectible"}],
            "quantity_per_tier": {1: 0, 2: 0, 3: 0}
        }

    # Calcula o multiplicador de custo
    for boost in active_boosts:
        if boost.get("type") == "COST" and boost.get("conditions", {}).get("resource") == "Axe":
            if boost.get("operation") == "multiply":
                cost_multiplier *= Decimal(str(boost["value"]))
                cost_buffs.append(boost)

    final_cost_per_axe = base_cost * cost_multiplier

    # Calcula a quantidade de machados por tier
    base_quantity = Decimal('1')
    quantity_multiplier = Decimal('1')
    if any(b.get("source_item") == "Logger" for b in active_boosts):
        quantity_multiplier = Decimal('0.5')

    final_quantity_base = base_quantity * quantity_multiplier

    return {
        "cost_per_axe": float(final_cost_per_axe),
        "applied_cost_buffs": cost_buffs,
        "quantity_per_tier": {
            1: float(final_quantity_base * 1),
            2: float(final_quantity_base * 4),
            3: float(final_quantity_base * 16),
        }
    }

def _format_buffs_for_display(buff_list: list) -> list:
    """Formata uma lista de bônus para exibição na UI."""
    if not buff_list:
        return []
    
    formatted = []
    for buff in buff_list:
        source_item = buff.get("source_item", "Unknown")
        source_type = buff.get("source_type", "unknown")
        operation = buff.get("operation", "add")

        # Adiciona tratamento para casos especiais onde o valor não é numérico
        if operation == "special":
            effect_str = str(buff.get("value", ""))
            if effect_str:
                formatted.append({"source_item": source_item, "source_type": source_type, "effect_str": effect_str})
            continue
        
        value = Decimal(str(buff.get("value", 0)))
        effect_str = ""
        if operation == "add":
            effect_str = f"+{value:.2f}"
        elif operation == "multiply":
            # Ex: 1.2 -> +20%, 0.8 -> -20%
            percentage = (value - 1) * 100
            effect_str = f"{'+' if percentage >= 0 else ''}{percentage:.0f}%"
        elif operation == "percentage":
            effect_str = f"{'+' if value >= 0 else ''}{value * 100:.0f}%"
        
        if effect_str:
            formatted.append({"source_item": source_item, "source_type": source_type, "effect_str": effect_str})
    return sorted(formatted, key=lambda x: x['source_item'])

def _analyze_farm_summary(player_items: set, wood_boost_catalogue: dict, farm_data: dict) -> dict:
    """
    Realiza a análise de potencial teórico (sumário) da fazenda para madeira.
    Calcula rendimento Min/Avg/Max, custos e tempos de ciclo.
    """
    # Obtém a lista de bônus base (sem YIELD de críticos) para o cálculo do MÍNIMO.
    base_active_boosts = _get_active_player_boosts(player_items, wood_boost_catalogue, farm_data)

    # 1. Análise de Rendimento (Min, Avg, Max) para uma árvore Tier 1.
    min_yield_info = _get_wood_drop_amount(base_active_boosts, tree_multiplier=1, tree_tier=1)
    
    # Constrói a lista de bônus para o cálculo do MÁXIMO.
    potential_crit_boosts = list(base_active_boosts)
    for item_name in player_items:
        if item_name in wood_boost_catalogue:
            item_boosts = wood_boost_catalogue[item_name].get("boosts", [])
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)
            if is_critical_item:
                for boost in item_boosts:
                    if boost.get("type") == "YIELD":
                        potential_crit_boosts.append({"source_item": f"{item_name} (Critical)", **boost})
    
    # Adiciona o bônus de YIELD do "Native" para o cálculo do MÁXIMO, pois ele é um crítico especial.
    if "Native" in wood_boost_catalogue:
        native_boosts = wood_boost_catalogue["Native"].get("boosts", [])
        for boost in native_boosts:
            if boost.get("type") == "YIELD":
                # Verifica se o bônus se aplica a 'Wood'
                resource_list = boost.get("conditions", {}).get("resource", [])
                if "Wood" in resource_list:
                    potential_crit_boosts.append({"source_item": "Native (Critical)", **boost})
    
    max_yield_info = _get_wood_drop_amount(potential_crit_boosts, tree_multiplier=1, tree_tier=1)
    
    # Coleta as chances de crítico da lista de bônus base para o cálculo da MÉDIA.
    crit_chance_boosts = [b for b in base_active_boosts if b.get("type") == "CRITICAL_CHANCE"]
    total_crit_chance = sum(Decimal(str(b.get("value", 0))) for b in crit_chance_boosts)
    avg_yield = (Decimal(str(min_yield_info['final_deterministic'])) * (1 - total_crit_chance)) + (Decimal(str(max_yield_info['final_deterministic'])) * total_crit_chance)

    # 2. Análise de Custo e Tempo de Ciclo
    axe_info = _get_axe_cost_and_quantity_info(base_active_boosts)
    recovery_info = _get_tree_recovery_time(base_active_boosts)

    # 3. Formatação dos bônus para exibição
    yield_buffs_for_display = _format_buffs_for_display(min_yield_info['applied_buffs'])
    time_buffs_for_display = _format_buffs_for_display(recovery_info['applied_buffs'])

    # 4. Cálculo de Métricas de Eficiência
    cycle_time_seconds = recovery_info['final']
    all_trees = farm_data.get("trees", {})
    num_trees = len(all_trees)
    
    # Nova métrica: Rendimento por Ciclo para todas as árvores
    yield_per_cycle = float(avg_yield * num_trees)
    
    # Novas métricas: Custo e Quantidade de Machados por Ciclo
    quantity_per_tier = axe_info['quantity_per_tier']
    total_axes_per_cycle = sum(
        Decimal(str(quantity_per_tier.get(tree_data.get("tier", 1), 0)))
        for tree_data in all_trees.values()
    )
    total_cost_per_cycle = float(total_axes_per_cycle * Decimal(str(axe_info['cost_per_axe'])))

    coins_per_axe = axe_info['cost_per_axe']
    cost_per_wood = float(Decimal(str(coins_per_axe)) / avg_yield) if avg_yield > 0 else 0.0


    # 4. Montagem do dicionário de sumário
    return {
        "yield": {
            "min": min_yield_info['final_deterministic'],
            "avg": float(avg_yield),
            "max": max_yield_info['final_deterministic']
        },
        "cost": {
            "coins_per_axe": axe_info['cost_per_axe'],
            "quantity_per_tier": axe_info['quantity_per_tier']
        },
        "cycle_time_seconds": cycle_time_seconds,
        "efficiency": {
            "yield_per_cycle": float(yield_per_cycle),
            "axes_per_cycle": float(total_axes_per_cycle),
            "cost_per_cycle": total_cost_per_cycle,
            "cost_per_wood": cost_per_wood
        },
        "applied_buffs": {
            "yield": yield_buffs_for_display,
            "time": time_buffs_for_display,
            "cost": _format_buffs_for_display(axe_info['applied_cost_buffs'])
        }
    }

def _analyze_individual_trees(player_items: set, wood_boost_catalogue: dict, farm_data: dict) -> dict:
    """
    Realiza a análise do estado real de cada árvore na fazenda.
    """
    # Obtém a lista de bônus base que se aplica a todas as árvores como ponto de partida.
    base_active_boosts = _get_active_player_boosts(player_items, wood_boost_catalogue, farm_data)
    
    temporal_boosts, regular_base_boosts, temporal_item_names = _extract_and_process_temporal_boosts(
        base_active_boosts, farm_data
    )

    player_wide_recovery_info = _get_tree_recovery_time(regular_base_boosts)

    trees_api_data = farm_data.get("trees", {})
    analyzed_trees = {}
    summary_stats = {"total": 0, "ready": 0, "recovering": 0, "total_yield": Decimal('0')}
    summary_stats['final_recovery_time'] = player_wide_recovery_info.get('final', TREE_RECOVERY_TIME_SECONDS)
    
    critical_hit_stats = defaultdict(int)
    current_timestamp_ms = int(time.time() * 1000)

    for tree_id, tree_data in trees_api_data.items():
        summary_stats["total"] += 1
        
        wood_details = tree_data.get("wood", {})
        chopped_at_ms = wood_details.get("choppedAt", 0)
        critical_hits = wood_details.get("criticalHit", {})
        tree_name = tree_data.get("name", "Tree")
        tree_multiplier = tree_data.get("multiplier", 1)
        tree_tier = tree_data.get("tier", 1)

        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0:
                critical_hit_stats[hit_name] += hit_count

        # Cria uma cópia profunda para garantir que a lista base não seja modificada entre as iterações.
        tree_specific_boosts = copy.deepcopy(regular_base_boosts)

        for temporal_info in temporal_boosts:
            if chopped_at_ms > temporal_info['activation_ts']:
                tree_specific_boosts.append(temporal_info['boost'])

        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0 and hit_name in wood_boost_catalogue:
                source_type = wood_boost_catalogue[hit_name].get("source_type")
                if hit_name == "Native":
                    source_type = "game_mechanic"

                # Encontra o bônus de YIELD específico do item de acerto crítico
                crit_yield_boost = next(
                    (b for b in wood_boost_catalogue[hit_name].get("boosts", []) if b.get("type") == "YIELD"),
                    None
                )

                if crit_yield_boost:
                    source_item_text = "(Critical Hit)" if hit_name == "Native" else f"{hit_name} (Critical Hit)"
                    tree_specific_boosts.append({
                        **crit_yield_boost,
                        "source_item": source_item_text, "source_type": source_type
                    })
        yield_info = _get_wood_drop_amount(tree_specific_boosts, tree_multiplier, tree_tier)
        summary_stats['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        recovery_info = player_wide_recovery_info
        final_recovery_seconds = recovery_info["final"]

        # A lógica do jogo subtrai a redução do tempo de corte para acelerar a recuperação.
        time_reduction_ms = recovery_info.get("reduction_seconds", 0) * 1000
        effective_chopped_at = chopped_at_ms - time_reduction_ms

        # A verificação de prontidão usa o TEMPO BASE, pois a redução já foi aplicada ao choppedAt
        is_ready = not chopped_at_ms or current_timestamp_ms >= (effective_chopped_at + (TREE_RECOVERY_TIME_SECONDS * 1000)) if chopped_at_ms else True
        state_name = "Pronta" if is_ready else "Recuperando"
        summary_stats["ready" if is_ready else "recovering"] += 1
        
        # O tempo de prontidão é sempre o tempo de corte efetivo + o tempo base de recuperação.
        ready_at_ms = effective_chopped_at + (TREE_RECOVERY_TIME_SECONDS * 1000)

        analyzed_trees[tree_id] = {
            "id": tree_id, "name": tree_name, "state_name": state_name,
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "recovery": recovery_info},
            "has_aoe_buff": False,
            "critical_hits": critical_hits
        }

    # Converte o total_yield para float para serialização JSON
    summary_stats['total_yield'] = float(summary_stats['total_yield'])

    return {
        "analyzed_trees": dict(sorted(analyzed_trees.items())),
        "summary_stats": summary_stats,
        "critical_hit_stats": dict(sorted(critical_hit_stats.items())),
        "temporal_item_names": temporal_item_names
    }

def analyze_wood_resources(farm_data: dict) -> dict:
    """
    Orquestrador principal para a análise de madeira.
    Cria um catálogo de bônus e delega a análise de sumário e individual
    para funções especializadas, garantindo o desacoplamento.
    """
    all_item_data = _get_all_item_data()
    wood_boost_catalogue = _filter_boosts_for_wood(all_item_data)
    
    player_items = _get_player_items(farm_data)

    active_boosts = _get_active_player_boosts(
        player_items,
        wood_boost_catalogue,
        farm_data
    )

    active_item_names = {boost['source_item'] for boost in active_boosts}

    # Delega a análise de sumário para a função dedicada.
    summary_analysis = _analyze_farm_summary(player_items, wood_boost_catalogue, farm_data)

    # Delega a análise individual para a função dedicada.
    individual_analysis_result = _analyze_individual_trees(player_items, wood_boost_catalogue, farm_data)

    # Combina os resultados das duas análises para a view
    active_item_names.update(individual_analysis_result["temporal_item_names"])

    view_data = {
        "summary_analysis": summary_analysis,
        "summary": individual_analysis_result["summary_stats"],
        "tree_status": individual_analysis_result["analyzed_trees"],
        "critical_hit_stats": individual_analysis_result["critical_hit_stats"],
        "active_boost_items": sorted(list(active_item_names)),
        "all_catalogued_items": sorted(list(wood_boost_catalogue.keys())),
    }

    return {"view": view_data}