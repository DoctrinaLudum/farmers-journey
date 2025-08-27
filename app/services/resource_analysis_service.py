# app/services/resource_analysis_service.py

import logging
import time
from decimal import Decimal

from ..domain import collectiblesItemBuffs as collectibles_domain
from ..domain import crops as crops_domain
from ..domain import flowers as flower_domain
from ..domain import resources as resources_domain
from ..domain import skills as skills_domain
from ..domain import wearablesItemBuffs as wearables_domain

log = logging.getLogger(__name__)

# ==============================================================================
# FUNÇÕES GENÉRICAS DE ANÁLISE DE RECURSOS
# ==============================================================================

# Define categorias de recursos para simplificar as condições de bônus.
RESOURCE_CATEGORIES = {
    "Mineral": ['Stone', 'Iron', 'Gold'],
    "Flower": list(flower_domain.FLOWER_DATA.keys())
}

def _get_player_items(farm_data: dict) -> set:
    """
    Extrai e unifica todos os itens que um jogador possui (coletáveis,
    vestíveis, habilidades, etc.) em um único conjunto para fácil consulta.
    """
    # Itens colocados na fazenda principal e na casa
    player_items = set(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())
    
    # Itens equipados no Bumpkin principal
    bumpkin = farm_data.get("bumpkin", {})
    player_items.update(bumpkin.get("equipped", {}).values())
    
    # Habilidades do Bumpkin principal
    player_items.update(bumpkin.get("skills", {}).keys())

    # Itens equipados nos Farm Hands
    farm_hands_data = farm_data.get("farmHands", {}).get("bumpkins", {})
    if farm_hands_data:
        for hand in farm_hands_data.values():
            player_items.update(hand.get("equipped", {}).values())

    # Itens no inventário (como a Pitchfork)
    player_items.update(farm_data.get("inventory", {}).keys())

    return player_items

def _get_all_item_data():
    """Unifica todos os dicionários de domínio em um único lugar."""
    return {
        **skills_domain.LEGACY_BADGES,
        **skills_domain.BUMPKIN_REVAMP_SKILLS,
        **wearables_domain.WEARABLES_ITEM_BUFFS,
        **collectibles_domain.COLLECTIBLES_ITEM_BUFFS
    }

def filter_boosts_from_domains(resource_conditions: dict):
    """
    Varre todos os domínios e cria um dicionário otimizado contendo
    apenas os itens e bônus que afetam um conjunto específico de recursos.

    Args:
        resource_conditions (dict): Um dicionário de configuração que define
                                    quais recursos e tipos de bônus procurar.
                                    Ex: {'yield_resource_names': ['Wood'], ...}
    """
    boost_catalogue = {}
    log.info(f"Iniciando a catalogação de bônus para as condições: {resource_conditions}")
    all_item_data = _get_all_item_data()

    # Extrai as condições para a filtragem
    yield_names = resource_conditions.get('yield_resource_names', [])
    recovery_names = resource_conditions.get('recovery_resource_names', [])
    skill_tree = resource_conditions.get('skill_tree_name')
    boost_categories = resource_conditions.get('boost_category_names', [])

    for item_name, item_details in all_item_data.items():
        boost_list = item_details.get("boosts") or item_details.get("effects")

        if not item_details or not boost_list or not item_details.get("enabled", True):
            continue

        # --- FILTRO DE ÁRVORE DE HABILIDADES ---
        # Se um `skill_tree` foi especificado (ex: 'Trees' para o wood_service),
        # garante que apenas habilidades dessa árvore (ou habilidades sem árvore definida, como 'Native')
        # sejam consideradas. Isso evita que bônus de outras árvores (ex: 'Fruit Patch')
        # que mencionam 'Wood' sejam incluídos indevidamente.
        if skill_tree and item_name in skills_domain.BUMPKIN_REVAMP_SKILLS and item_details.get("tree") and item_details.get("tree") != skill_tree:
            continue

        # --- Lógica de Relevância do Item ---
        # O item é considerado relevante se corresponder a UMA das lógicas de filtragem.
        is_item_relevant = False

        # Lógica 1: Checa a categoria do item.
        if boost_categories:
            item_category = item_details.get("boost_category")
            if item_category:
                item_category_list = item_category if isinstance(item_category, list) else [item_category]
                if any(cat in boost_categories for cat in item_category_list):
                    is_item_relevant = True

        # Lógica 2: Checa a árvore de habilidades (para revamp skills).
        if not is_item_relevant and skill_tree and item_details.get("tree") == skill_tree:
            is_item_relevant = True

        # Lógica 3: Checa os recursos dentro dos bônus (para todos os outros casos, incluindo legacy skills).
        if not is_item_relevant:
            for boost in boost_list:
                conditions = boost.get("conditions", {})
                resource_name_or_list = conditions.get("resource") or conditions.get("item") or conditions.get("crop")
                if resource_name_or_list:
                    resource_names_to_check = resource_name_or_list if isinstance(resource_name_or_list, list) else [resource_name_or_list]
                    if any(name in yield_names for name in resource_names_to_check) or any(name in recovery_names for name in resource_names_to_check):
                        is_item_relevant = True
                        break

        if not is_item_relevant:
            continue # Pula para o próximo item se não for relevante para este catálogo.

        # --- Se o item for relevante, processa os seus bônus ---
        relevant_boosts = []
        for boost in boost_list:
            # Filtra apenas os tipos de bônus que este serviço analisa (rendimento e tempo).
            # Separa os tipos para uma padronização mais precisa.
            is_direct_yield = boost.get("type") in ["YIELD", "CROP_YIELD", "RESOURCE_YIELD", "CRITICAL_YIELD_BONUS"]
            is_chance_or_other_yield = boost.get("type") in ["BONUS_YIELD_CHANCE", "CRITICAL_CHANCE"]
            is_recovery = boost.get("type") in ["RECOVERY_TIME", "TREE_RECOVERY_TIME", "CROP_GROWTH_TIME", "GROWTH_TIME", "SUPER_TOTEM_TIME_BOOST"]
            is_sale_price = boost.get("type") == "SALE_PRICE"

            if is_direct_yield or is_chance_or_other_yield or is_recovery or is_sale_price:
                standardized_boost = boost.copy()
                # Apenas padroniza os tipos de rendimento direto para 'YIELD'.
                # Mantém os tipos de chance (CRITICAL_CHANCE) intactos para a lógica de filtragem.
                if is_direct_yield:
                    standardized_boost['type'] = 'YIELD'
                elif is_recovery:
                    standardized_boost['type'] = 'RECOVERY_TIME'
                elif is_sale_price:
                    standardized_boost['type'] = 'SALE_PRICE'
                
                relevant_boosts.append(standardized_boost)

        if relevant_boosts: 
            # Determina o tipo de origem de forma mais específica
            if item_name in skills_domain.LEGACY_BADGES:
                source_type = "skill_legacy"
            elif item_name in skills_domain.BUMPKIN_REVAMP_SKILLS:
                source_type = "skill"
            elif item_name in wearables_domain.WEARABLES_ITEM_BUFFS:
                source_type = "wearable"
            else: # Assume que é um coletável por padrão se não for encontrado em outros domínios
                source_type = "collectible"

            boost_catalogue[item_name] = {
                "boosts": relevant_boosts,
                "source_type": source_type,
                "has_aoe": "aoe" in item_details
            }

    return boost_catalogue

def get_active_player_boosts(player_items: set, boost_catalogue: dict, non_cumulative_groups: dict = None, farm_data: dict = None) -> list:
    """
    Pega um conjunto de itens do jogador e os cruza com um catálogo de bônus
    para retornar uma lista de bônus ativos, respeitando hierarquias.
    """
    active_boosts = []
    # Garante que farm_data seja um dicionário para evitar erros com .get()
    farm_data = farm_data or {}
    non_cumulative_groups = non_cumulative_groups or {}
    
    items_in_any_group = set()
    for group_items in non_cumulative_groups.values():
        items_in_any_group.update(group_items)

    # 1. Processa os grupos hierárquicos
    for group_name, ordered_items in non_cumulative_groups.items():
        for item_name in ordered_items:
            if item_name in player_items and item_name in boost_catalogue:
                # --- LÓGICA DE EXPIRAÇÃO ---
                # Verifica se o primeiro bônus do item tem uma condição de duração.
                # Assume que todos os bônus de um mesmo item temporal têm a mesma duração.
                first_boost = boost_catalogue[item_name]["boosts"][0]
                conditions = first_boost.get("conditions", {})
                source_type = boost_catalogue[item_name].get("source_type")
                duration_days = conditions.get("duration_days")
                duration_hours = conditions.get("duration_hours")

                if duration_days or duration_hours:
                    # Busca a data de ativação do item nos dados da fazenda
                    all_placed_items = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}
                    placements = all_placed_items.get(item_name, [])
                    if placements:
                        activation_ts = placements[0].get("createdAt", 0)
                        now_ts = int(time.time() * 1000)
                        duration_ms = (duration_days or 0) * 24 * 60 * 60 * 1000 + (duration_hours or 0) * 60 * 60 * 1000
                        
                        if now_ts > (activation_ts + duration_ms):
                            log.debug(f"Bônus do item '{item_name}' expirou. Ignorando.")
                            continue # Pula para o próximo item no grupo hierárquico
                # --- FIM DA LÓGICA DE EXPIRAÇÃO ---

                # CORREÇÃO: Ignora itens com AOE, pois eles são tratados por posição.
                if boost_catalogue[item_name].get("has_aoe"):
                    log.debug(f"Item hierárquico '{item_name}' tem AOE, será tratado por posição.")
                    continue

                item_boosts = boost_catalogue[item_name]["boosts"]
                # Adiciona a flag 'is_temporal' se o item for temporal, para a função de extração.
                is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)

                log.debug(f"Aplicando bônus hierárquico de '{group_name}': '{item_name}'.")
                for boost in item_boosts:
                    if is_critical_item and boost.get("type") == "YIELD":
                        continue
                    active_boosts.append({"source_item": item_name, "source_type": source_type, **boost})
                break

    # 2. Processa todos os outros bônus que não são hierárquicos
    for item_name in player_items:
        if item_name in boost_catalogue and item_name not in items_in_any_group:
            # --- LÓGICA DE EXPIRAÇÃO (REPETIDA PARA ITENS NÃO HIERÁRQUICOS) ---
            first_boost = boost_catalogue[item_name]["boosts"][0]
            conditions = first_boost.get("conditions", {})
            source_type = boost_catalogue[item_name].get("source_type")
            duration_days = conditions.get("duration_days")
            duration_hours = conditions.get("duration_hours")

            if duration_days or duration_hours:
                all_placed_items = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}
                placements = all_placed_items.get(item_name, [])
                if placements:
                    activation_ts = placements[0].get("createdAt", 0)
                    now_ts = int(time.time() * 1000)
                    duration_ms = (duration_days or 0) * 24 * 60 * 60 * 1000 + (duration_hours or 0) * 60 * 60 * 1000
                    
                    if now_ts > (activation_ts + duration_ms):
                        log.debug(f"Bônus do item '{item_name}' expirou. Ignorando.")
                        continue # Pula para o próximo item
            # --- FIM DA LÓGICA DE EXPIRAÇÃO ---

            # CORREÇÃO: Ignora itens com AOE, pois eles são tratados por posição.
            if boost_catalogue[item_name].get("has_aoe"):
                continue

            item_boosts = boost_catalogue[item_name]["boosts"]
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)
            for boost in item_boosts:
                if is_critical_item and boost.get("type") == "YIELD":
                    continue
                active_boosts.append({"source_item": item_name, "source_type": source_type, **boost})

    return active_boosts

def get_aoe_boosts_for_resource(resource_position: dict, placed_items: dict, player_skills: set, farm_data: dict = None) -> list:
    """
    Calcula os bônus de Área de Efeito (AOE) que se aplicam a uma posição específica,
    considerando modificações de skills e o estado do jogo (sem cooldowns).

    Args:
        resource_position: As coordenadas {'x': int, 'y': int} do recurso a ser verificado.
        placed_items: Um dicionário de todos os itens colocados na fazenda (ex: farm_data['collectibles']).
        player_skills: Um conjunto com os nomes de todas as habilidades que o jogador possui.
        farm_data (opcional): Os dados completos da fazenda, necessários para verificações de estado.

    Returns:
        Uma lista de dicionários de bônus que se aplicam àquela posição.
    """
    active_aoe_boosts = []
    farm_data = farm_data or {}

    if not resource_position or resource_position.get('x') is None or resource_position.get('y') is None:
        return active_aoe_boosts

    rx, ry = resource_position['x'], resource_position['y']

    # Unifica todos os itens que podem ter AOE para consulta.
    all_aoe_items = {**collectibles_domain.COLLECTIBLES_ITEM_BUFFS}

    for item_name, placements in placed_items.items():
        item_details = all_aoe_items.get(item_name)
        if not item_details or "aoe" not in item_details:
            continue
        
        # --- Lógica de Modificação de AOE por Skills (replicando boostedDistance()) ---
        final_aoe = item_details["aoe"]
        for skill_name in player_skills:
            skill_details = skills_domain.BUMPKIN_REVAMP_SKILLS.get(skill_name)
            if not skill_details: continue
            
            for effect in skill_details.get("effects", []):
                if effect.get("name") == "MODIFY_ITEM_AOE" and effect.get("target_item") == item_name:
                    final_aoe = effect["new_aoe"]
                    break

        # Itera sobre cada instância do item colocada na fazenda.
        for placement in placements:
            placement_coords = placement.get("coordinates", {})
            ax, ay = placement_coords.get("x"), placement_coords.get("y")
            if ax is None or ay is None: continue

            is_within_range = False
            shape = final_aoe.get("shape")

            # Lógica para formas de AOE personalizadas (retângulos, etc.)
            if shape == "custom":
                for plot in final_aoe.get("plots", []):
                    if rx == (ax + plot["x"]) and ry == (ay + plot["y"]):
                        is_within_range = True
                        break
            
            # Lógica para formas de AOE circulares
            elif shape == "circle":
                radius = final_aoe.get("radius", 0)
                dx = abs(rx - ax)
                dy = abs(ry - ay)
                # O jogo verifica se está dentro de um quadrado (distância de Manhattan)
                # e não em um círculo verdadeiro.
                if dx <= radius and dy <= radius and not (dx == 0 and dy == 0):
                    is_within_range = True
            
            if is_within_range:
                for boost in item_details.get("boosts", []):
                    active_aoe_boosts.append({"source_item": f"{item_name} (AOE)", "source_type": "collectible", **boost})
                break

    return active_aoe_boosts

def get_crop_tier(crop_name: str) -> str | None:
    """
    Retorna o tier ('basic', 'medium', 'advanced') de uma cultura específica.
    Consulta as listas de tiers pré-calculadas no domínio de culturas.
    Retorna None se a cultura não for encontrada em nenhum tier.
    """
    if crop_name in crops_domain.CROP_TIERS["basic"]:
        return "basic"
    if crop_name in crops_domain.CROP_TIERS["medium"]:
        return "medium"
    if crop_name in crops_domain.CROP_TIERS["advanced"]:
        return "advanced"
    return None

def _conditions_are_met(conditions: dict, resource_name: str, node_context: dict) -> bool:
    """
    Função auxiliar para verificar se todas as condições de um bônus são atendidas.
    """
    context = node_context or {}

    for condition_key, required_value in conditions.items():
        # Condição de Recurso/Item/Cultura
        if condition_key in ["resource", "item", "crop"]:
            required_list = required_value if isinstance(required_value, list) else [required_value]
            if resource_name not in required_list:
                return False
        
        # Condição de Categoria (ex: Mineral)
        elif condition_key == "category":
            if required_value in RESOURCE_CATEGORIES:
                if resource_name not in RESOURCE_CATEGORIES[required_value]:
                    return False
            # Se a categoria não estiver em RESOURCE_CATEGORIES, ela é ignorada por esta verificação
            # e pode ser tratada por outra lógica (como crop_tier).

        # Condição de Minas Restantes (minesLeft)
        elif condition_key == "minesLeft":
            current_value = context.get("minesLeft")
            if current_value != required_value:
                return False
        
        # Condição de Tier da Cultura
        elif condition_key == "crop_tier":
            current_tier = get_crop_tier(resource_name)
            if not current_tier:
                return False # A cultura não tem um tier definido ou não existe
            
            required_list = required_value if isinstance(required_value, list) else [required_value]
            if current_tier not in required_list:
                return False # O tier não corresponde

    return True

def extract_and_process_temporal_boosts(active_boosts: list, farm_data: dict) -> tuple:
    """
    Separa os bônus temporais dos normais e anexa seus timestamps de ativação.
    Bônus temporais são aqueles que só afetam ações iniciadas após sua ativação.

    Args:
        active_boosts: A lista completa de bônus ativos do jogador.
        farm_data: Os dados completos da fazenda para buscar o 'createdAt'.

    Returns:
        Uma tupla contendo:
        - (list) Bônus temporais processados com seus timestamps de ativação.
        - (list) Bônus regulares (não temporais).
        - (set) Nomes dos itens que fornecem bônus temporais.
    """
    temporal_boosts_processed = []
    regular_boosts = []
    temporal_item_names = set()

    all_placed_items = farm_data.get("collectibles", {})
    all_placed_items.update(farm_data.get("home", {}).get("collectibles", {}))

    for boost in active_boosts:
        if boost.get("is_temporal"):
            item_name = boost.get("source_item")
            placements = all_placed_items.get(item_name, [])
            
            if placements:
                # Assume que o primeiro item colocado é o relevante
                activation_ts = placements[0].get("createdAt", 0)
                temporal_boosts_processed.append({"boost": boost, "activation_ts": activation_ts})
                temporal_item_names.add(item_name)
            else:
                log.warning(f"Bônus temporal '{item_name}' encontrado, mas o item não foi localizado nos dados da fazenda.")
        else:
            regular_boosts.append(boost)
            
    return temporal_boosts_processed, regular_boosts, temporal_item_names

def calculate_final_recovery_time(base_time: float, active_boosts: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o tempo de recuperação final com base nos bônus ativos.
    Filtra os bônus com base no nome do recurso e no contexto do nó.
    """
    base_recovery_time = Decimal(str(base_time))
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    for boost in active_boosts:
        conditions = boost.get("conditions", {})
        if _conditions_are_met(conditions, resource_name, node_context) and boost.get("type") in ["RECOVERY_TIME", "GROWTH_TIME", "SUPER_TOTEM_TIME_BOOST"]:
                operation = boost["operation"]
                value = Decimal(str(boost["value"]))

                if operation == "percentage":
                    multiplicative_factor *= (Decimal('1') + value)

                elif operation == "multiply":
                    multiplicative_factor *= value

                applied_buffs_details.append(boost)

    final_time = base_recovery_time * multiplicative_factor

    return {
        "base": float(base_recovery_time),
        "final": float(final_time),
        "applied_buffs": applied_buffs_details
    }

def calculate_final_yield(base_yield: float, active_boosts: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o rendimento final, separando bônus determinísticos de bônus de chance.
    Filtra os bônus com base no nome do recurso e no contexto do nó.
    """
    base = Decimal(str(base_yield))
    additive_bonus = Decimal('0')
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []
    chance_bonuses = []

    for boost in active_boosts:
        conditions = boost.get("conditions", {})
        if _conditions_are_met(conditions, resource_name, node_context):
            boost_type = boost.get("type")
            if boost_type == "YIELD":
                operation = boost["operation"]
                value = Decimal(str(boost["value"]))

                if operation == "add":
                    additive_bonus += value
                elif operation == "subtract":
                    additive_bonus -= value
                elif operation == "percentage":
                    multiplicative_factor *= (Decimal('1') + value)
                elif operation == "multiply":
                    multiplicative_factor *= value

                applied_buffs_details.append(boost)
            elif boost_type == "BONUS_YIELD_CHANCE":
                chance_bonuses.append({
                    "source_item": boost.get("source_item", "Unknown"),
                    "chance": float(boost.get("value", 0)),
                    "multiplier": float(boost.get("bonus_multiplier", 1)),
                })
                applied_buffs_details.append(boost)

    final_deterministic = (base * multiplicative_factor) + additive_bonus

    return {
        "base": float(base),
        "final_deterministic": float(final_deterministic),
        "chance_bonuses": chance_bonuses,
        "applied_buffs": applied_buffs_details
    }

def analyze_player_min_max_yields(
    player_items: set, 
    active_boosts: list, 
    boost_catalogue: dict, 
    resource_conditions: dict, 
    special_skills: dict = None
) -> dict:
    """
    Analisa os bônus ATIVOS do jogador para calcular o rendimento mínimo (base) e
    o máximo possível para cada tipo de recurso, com base nos itens que ele possui,
    INCLUINDO o potencial de golpes críticos.
    """
    special_skills = special_skills or {}
    all_potential_boosts = list(active_boosts)

    # 1. Adiciona bônus de itens de CRITICAL_CHANCE que o jogador possui
    for item_name in player_items:
        if item_name in boost_catalogue:
            item_boosts = boost_catalogue[item_name].get("boosts", [])
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)
            
            if is_critical_item:
                for boost in item_boosts:
                    if boost.get("type") == "YIELD":
                        all_potential_boosts.append({"source_item": f"{item_name} (Critical)", **boost})

    # 2. Adiciona bônus de skills especiais (inerentes ou de domínio específico)
    # Skill "Native" (comum a madeira e mineração)
    native_skill_data = skills_domain.BUMPKIN_REVAMP_SKILLS.get("Native")
    if native_skill_data:
        for boost in native_skill_data.get("effects", []):
            if boost.get("type") == "YIELD":
                all_potential_boosts.append({"source_item": "Native (Critical)", **boost})
                break 

    # Skills de domínio específico (ex: Greenhouse Gamble)
    for skill_name, skill_data in special_skills.items():
        if skill_name in player_items:
            for boost in skill_data.get("effects", []):
                if boost.get("type") == "YIELD":
                    all_potential_boosts.append({"source_item": f"{skill_name} (Critical)", **boost})
                    break

    min_max_data = {}
    
    affected_resources = set()
    for boost in all_potential_boosts:
        if boost.get("type") == "YIELD":
            conditions = boost.get("conditions", {})
            resource_or_item = conditions.get("resource") or conditions.get("item") or conditions.get("crop")
            if resource_or_item:
                resource_list = resource_or_item if isinstance(resource_or_item, list) else [resource_or_item]
                affected_resources.update(resource_list)

    main_yield_resources = [name for name in affected_resources if name in resource_conditions.get('yield_resource_names', [])]

    for resource_name in sorted(list(set(main_yield_resources))):
        base_yield_logic = resource_conditions.get('base_yield_logic', lambda r: 1)
        base_yield = base_yield_logic(resource_name)
        if base_yield == 0: continue

        player_max_yield_boosts = [b for b in all_potential_boosts if b.get("type") == "YIELD" and _conditions_are_met(b.get("conditions", {}), resource_name, {})]
        max_yield_info = calculate_final_yield(base_yield, player_max_yield_boosts, resource_name)
        max_yield = max_yield_info['final_deterministic']

        if max_yield > base_yield:
            min_max_data[resource_name] = {
                "base": float(base_yield), "max": float(max_yield),
                "contributing_boosts": max_yield_info['applied_buffs']
            }

    return dict(sorted(min_max_data.items()))