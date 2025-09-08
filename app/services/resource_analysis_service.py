"""
Este módulo centraliza a lógica de análise e aplicação de bônus e modificadores
para diversos recursos e ações dentro do jogo. Ele é projetado para ser genérico
e reutilizável por outros serviços (como `fruit_service`, `chop_service`, etc.),
garantindo consistência na forma como os bônus são calculados.

Principais responsabilidades:
- Unificar dados de bônus de diferentes domínios (habilidades, vestíveis, coletáveis).
- Filtrar bônus relevantes com base em condições específicas (recursos, categorias, árvores de habilidades).
- Processar modificadores de bônus (ex: dobrar o efeito de um item).
- Calcular rendimentos e tempos de recuperação finais, aplicando todos os bônus ativos.
- Lidar com a lógica de acertos críticos e bônus temporais.
"""

import logging
import time
from decimal import Decimal

# Importa os módulos de domínio que contêm as definições de dados brutos
from ..domain import animals as animals_domain
from ..domain import collectiblesItemBuffs as collectibles_domain
from ..domain import crops as crops_domain
from ..domain import flowers as flower_domain
from ..domain import fruits as fruit_domain
from ..domain import resources as resources_domain
from ..domain import skills as skills_domain
from ..domain import wearablesItemBuffs as wearables_domain
from . import bud_service

log = logging.getLogger(__name__)

# ==============================================================================
# FUNÇÕES GENÉRICAS DE ANÁLISE DE RECURSOS
# ==============================================================================

# Define categorias de recursos para simplificar as condições de bônus.
# Esta estrutura de dados centraliza a lógica de categorização para ser usada
# em toda a análise de bônus, especialmente para os Buds e outras condições.
RESOURCE_CATEGORIES = {
    # Categorias de Plantações (agrupadas por tier e uma categoria geral "Crop")
    "Basic Crops": crops_domain.CROP_TIERS["basic"],
    "Medium Crops": crops_domain.CROP_TIERS["medium"],
    "Advanced Crops": crops_domain.CROP_TIERS["advanced"],
    "Crop": (
        crops_domain.CROP_TIERS["basic"]
        + crops_domain.CROP_TIERS["medium"]
        + crops_domain.CROP_TIERS["advanced"]
    ),
    # Categoria de Frutas (lista de todas as frutas)
    "Fruit": list(fruit_domain.FRUIT_DATA.keys()),
    # Categoria de Minerais
    "Minerals": ["Stone", "Iron", "Gold"],
    # Categoria de Flores
    "Flower": list(flower_domain.FLOWER_DATA.keys()),
    # Categoria de Produtos de Animais
    "Animal Produce": ["Egg", "Feather", "Milk", "Leather", "Wool", "Merino Wool"],
}


def _get_player_items(farm_data: dict) -> set:
    """
    Extrai e unifica todos os itens que um jogador possui (coletáveis,
    vestíveis, habilidades, etc.) em um único conjunto para fácil consulta.
    Isso é essencial para determinar quais bônus estão ativos para o jogador.

    Args:
        farm_data (dict): Os dados completos da fazenda do jogador.

    Returns:
        set: Um conjunto contendo os nomes de todos os itens que o jogador possui.
    """
    # Coleta itens colocados na fazenda principal e na casa do jogador.
    player_items = set(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())
    
    # Adiciona itens equipados no Bumpkin principal.
    bumpkin = farm_data.get("bumpkin", {})
    player_items.update(bumpkin.get("equipped", {}).values())
    
    # Adiciona habilidades aprendidas pelo Bumpkin principal.
    player_items.update(bumpkin.get("skills", {}).keys())

    # Adiciona itens equipados nos Farm Hands (ajudantes da fazenda).
    farm_hands_data = farm_data.get("farmHands", {}).get("bumpkins", {})
    if farm_hands_data:
        for hand in farm_hands_data.values():
            player_items.update(hand.get("equipped", {}).values())

    # Adiciona itens no inventário (como ferramentas que podem dar bônus).
    player_items.update(farm_data.get("inventory", {}).keys())

    return player_items

def _get_all_item_data() -> dict:
    """
    Unifica todos os dicionários de domínio que contêm definições de itens
    e seus bônus/efeitos em um único dicionário para fácil acesso.

    Returns:
        dict: Um dicionário consolidado de todos os dados de itens do jogo.
    """
    return {
        **skills_domain.LEGACY_BADGES,          # Habilidades legadas
        **skills_domain.BUMPKIN_REVAMP_SKILLS,  # Habilidades do sistema de revamp
        **wearables_domain.WEARABLES_ITEM_BUFFS,# Bônus de itens vestíveis
        **collectibles_domain.COLLECTIBLES_ITEM_BUFFS, # Bônus de itens coletáveis
        **resources_domain.RESOURCES_DATA       # Dados de recursos (pode incluir bônus)
    }

def filter_boosts_from_domains(resource_conditions: dict) -> dict:
    """
    Varre todos os domínios de itens e cria um dicionário otimizado (catálogo)
    contendo apenas os itens e seus bônus que são relevantes para um conjunto
    específico de condições de recurso. Isso evita processar bônus desnecessários.

    Args:
        resource_conditions (dict): Um dicionário de configuração que define
                                    quais recursos e tipos de bônus procurar.
                                    Exemplos de chaves:
                                    - 'yield_resource_names': lista de nomes de recursos de rendimento.
                                    - 'recovery_resource_names': lista de nomes de recursos de recuperação.
                                    - 'skill_tree_name': nome da árvore de habilidades (ex: 'Fruit Patch').
                                    - 'boost_category_names': lista de categorias de bônus (ex: 'Fruit').

    Returns:
        dict: Um catálogo de bônus otimizado, onde as chaves são nomes de itens
              e os valores são seus bônus relevantes e tipo de origem.
    """
    boost_catalogue = {}
    log.info(f"Iniciando a catalogação de bônus para as condições: {resource_conditions}")
    all_item_data = _get_all_item_data()

    # Extrai as condições de filtragem para uso mais fácil.
    yield_names = resource_conditions.get('yield_resource_names', [])
    recovery_names = resource_conditions.get('recovery_resource_names', [])
    skill_tree = resource_conditions.get('skill_tree_name')
    boost_categories = resource_conditions.get('boost_category_names', [])

    for item_name, item_details in all_item_data.items():
        # Bônus podem estar em 'boosts' ou 'effects' dependendo do domínio.
        boost_list = item_details.get("boosts") or item_details.get("effects")

        # Ignora itens sem detalhes, sem bônus ou desabilitados.
        if not item_details or not boost_list or not item_details.get("enabled", True):
            continue

        # --- FILTRO DE ÁRVORE DE HABILIDADES ---
        # Se um `skill_tree` foi especificado (ex: 'Trees' para o wood_service),
        # garante que apenas habilidades dessa árvore (ou habilidades sem árvore definida, como 'Native')
        # sejam consideradas. Isso evita que bônus de outras árvores (ex: 'Fruit Patch')
        # que mencionam 'Wood' sejam incluídos indevidamente no catálogo de outro serviço.
        if skill_tree and item_name in skills_domain.BUMPKIN_REVAMP_SKILLS and item_details.get("tree") and item_details.get("tree") != skill_tree:
            continue

        # --- Lógica de Relevância do Item ---
        # Um item é considerado relevante se corresponder a PELO MENOS UMA das lógicas de filtragem.
        is_item_relevant = False

        # Lógica 1: Checa se a categoria do item (boost_category) está nas categorias desejadas.
        if boost_categories:
            item_category = item_details.get("boost_category")
            if item_category:
                # Converte para lista para lidar com categorias únicas ou múltiplas.
                item_category_list = item_category if isinstance(item_category, list) else [item_category]
                # Verifica se alguma das categorias do item está na lista de categorias desejadas.
                if any(cat in boost_categories for cat in item_category_list):
                    is_item_relevant = True

        # Lógica 2: Checa se a árvore de habilidades do item corresponde à `skill_tree` especificada.
        # (Aplicável principalmente para habilidades do sistema de revamp).
        if not is_item_relevant and skill_tree and item_details.get("tree") == skill_tree:
            is_item_relevant = True

        # Lógica 3: Checa se os recursos mencionados nas condições dos bônus do item
        # são relevantes para os `yield_names` ou `recovery_names` especificados.
        # Isso captura bônus que afetam recursos específicos, independentemente da categoria geral do item.
        if not is_item_relevant:
            for boost in boost_list:
                conditions = boost.get("conditions", {})
                # Tenta obter o nome do recurso/item/cultura da condição.
                resource_name_or_list = conditions.get("resource") or conditions.get("item") or conditions.get("crop")
                if resource_name_or_list:
                    # Converte para lista para lidar com nomes únicos ou múltiplos.
                    resource_names_to_check = resource_name_or_list if isinstance(resource_name_or_list, list) else [resource_name_or_list]
                    # Verifica se algum dos recursos nas condições do bônus está nas listas de rendimento ou recuperação desejadas.
                    if any(name in yield_names for name in resource_names_to_check) or any(name in recovery_names for name in resource_names_to_check):
                        is_item_relevant = True
                        break

        # Se o item não for relevante para nenhuma das lógicas de filtragem, pula para o próximo.
        if not is_item_relevant:
            continue

        # --- Se o item for relevante, processa os seus bônus --- 
        # Filtra e padroniza os bônus relevantes para este serviço.
        relevant_boosts = []
        
        # VERIFICAÇÃO ADICIONAL: Se o item é um modificador de AOE, seus bônus de YIELD
        # são considerados locais para a AOE e não devem ser catalogados como globais.
        is_aoe_modifier = False
        if item_details.get("effects"):
            if any(e.get("name") == "MODIFY_ITEM_AOE" for e in item_details.get("effects")):
                is_aoe_modifier = True

        for boost in boost_list:
            # Se for um modificador de AOE, pula a catalogação de seus bônus de YIELD.
            if is_aoe_modifier and boost.get("type") == "YIELD":
                continue

            # Identifica os tipos de bônus que este serviço está interessado em analisar.
            is_direct_yield = boost.get("type") in ["YIELD", "CROP_YIELD", "RESOURCE_YIELD", "CRITICAL_YIELD_BONUS"]
            is_chance_or_other_yield = boost.get("type") in ["BONUS_YIELD_CHANCE", "CRITICAL_CHANCE"]
            is_recovery = boost.get("type") in ["RECOVERY_TIME", "TREE_RECOVERY_TIME", "CROP_GROWTH_TIME", "GROWTH_TIME", "SUPER_TOTEM_TIME_BOOST"]
            is_sale_price = boost.get("type") == "SALE_PRICE"

            if is_direct_yield or is_chance_or_other_yield or is_recovery or is_sale_price:
                standardized_boost = boost.copy()
                # Padroniza tipos de rendimento direto para 'YIELD' para simplificar o processamento posterior.
                if is_direct_yield:
                    standardized_boost['type'] = 'YIELD'
                # Padroniza tipos de recuperação para 'RECOVERY_TIME'.
                elif is_recovery:
                    standardized_boost['type'] = 'RECOVERY_TIME'
                # Padroniza tipos de preço de venda para 'SALE_PRICE'.
                elif is_sale_price:
                    standardized_boost['type'] = 'SALE_PRICE'
                
                relevant_boosts.append(standardized_boost)

        # Se houver bônus relevantes após a filtragem, adiciona o item ao catálogo.
        if relevant_boosts: 
            # Determina o tipo de origem do item de forma mais específica para categorização.
            if item_name in skills_domain.LEGACY_BADGES:
                source_type = "skill_legacy"
            elif item_name in skills_domain.BUMPKIN_REVAMP_SKILLS:
                source_type = "skill"
            elif item_name in wearables_domain.WEARABLES_ITEM_BUFFS:
                source_type = "wearable"
            elif item_details.get("type") == "Fertiliser": # Verifica se é um fertilizante
                source_type = "fertiliser"
            else: # Assume que é um coletável por padrão se não for encontrado em outros domínios
                source_type = "collectible"

            boost_catalogue[item_name] = {
                "boosts": relevant_boosts,
                "source_type": source_type,
                "has_aoe": "aoe" in item_details # Indica se o item tem Área de Efeito (AOE)
            }

    return boost_catalogue

def _process_boost_modifiers(active_boosts: list, player_items: set) -> list:
    """
    Processa os bônus do tipo ITEM_MODIFICATION e COLLECTIBLE_EFFECT_MULTIPLIER.
    Esta função itera através de todos os modificadores potenciais que o jogador possui
    e os aplica aos bônus de base que já estão ativos. Isso permite que um item
    modifique o efeito de outro item (ex: dobrar o bônus de um coletável).

    Args:
        active_boosts (list): A lista de bônus que já estão ativos para o jogador.
        player_items (set): Um conjunto com os nomes de todos os itens que o jogador possui.

    Returns:
        list: A lista de bônus, com os modificadores aplicados.
    """
    all_item_data = _get_all_item_data()
    potential_modifiers = []

    # 1. Coleta todos os efeitos modificadores dos itens que o jogador possui.
    for item_name in player_items:
        item_data = all_item_data.get(item_name)
        if not item_data:
            continue
        
        effects = item_data.get("effects", [])
        for effect in effects:
            effect_type = effect.get("type")
            # Filtra apenas os tipos de efeito que modificam outros itens/bônus.
            if effect_type in ["ITEM_MODIFICATION", "COLLECTIBLE_EFFECT_MULTIPLIER"]:
                # Determina o tipo de origem do próprio modificador para fins de rastreamento.
                source_type = "collectible"
                if item_name in skills_domain.BUMPKIN_REVAMP_SKILLS:
                    source_type = "skill"
                elif item_name in wearables_domain.WEARABLES_ITEM_BUFFS:
                    source_type = "wearable"
                
                potential_modifiers.append({
                    "modifier_source_item": item_name,
                    "modifier_source_type": source_type,
                    **effect
                })

    if not potential_modifiers:
        return active_boosts # Retorna a lista original se não houver modificadores.

    # 2. Itera sobre os bônus ativos e aplica os modificadores relevantes.
    # Cria uma nova lista para evitar problemas de modificação durante a iteração.
    final_boosts = list(active_boosts)

    for i, target_boost in enumerate(final_boosts):
        # O nome do item que gera o bônus (ex: "Macaw", "Fruitful Blend").
        target_item_name = target_boost.get("source_item")
        if not target_item_name:
            continue

        for modifier in potential_modifiers:
            # O nome do item que este modificador afeta (ex: "Macaw", "Fruitful Blend").
            modifier_target_name = modifier.get("target_item")
            if not modifier_target_name:
                # Lida com casos onde o alvo do modificador está nas condições (ex: Loyal Macaw).
                modifier_target_name = modifier.get("conditions", {}).get("resource")

            # Se o modificador afeta o bônus atual.
            if target_item_name == modifier_target_name:
                # Encontrou uma correspondência! Aplica a modificação.
                
                # Verifica se a propriedade do bônus corresponde (ex: YIELD).
                target_property = modifier.get("target_property")
                if target_property and target_boost.get("type") != target_property:
                    continue

                mod_operation = modifier.get("operation")
                mod_value = Decimal(str(modifier.get("value", 1)))
                original_value = Decimal(str(target_boost.get("value", 0)))

                new_value = original_value
                if mod_operation == "multiply":
                    new_value *= mod_value
                elif mod_operation == "add":
                    new_value += mod_value
                
                # Atualiza o bônus alvo com o novo valor calculado.
                final_boosts[i]["value"] = float(new_value)

                # Adiciona os detalhes do modificador para a interface do usuário (UI).
                if "modifiers" not in final_boosts[i]:
                    final_boosts[i]["modifiers"] = []
                
                display_value = f"x{mod_value}" if mod_operation == "multiply" else f"+{mod_value}"
                final_boosts[i]["modifiers"].append({
                    "source_item": modifier["modifier_source_item"],
                    "value": display_value,
                    "operation": "special",
                    "source_type": modifier["modifier_source_type"]
                })

    return final_boosts

def get_active_player_boosts(player_items: set, boost_catalogue: dict, non_cumulative_groups: dict = None, farm_data: dict = None) -> list:
    """
    Pega um conjunto de itens que o jogador possui e os cruza com um catálogo de bônus
    para retornar uma lista de todos os bônus ativos. Esta função lida com:
    - Bônus hierárquicos (onde apenas o melhor de um grupo se aplica).
    - Bônus cumulativos (onde todos os bônus se somam).
    - Aplicação de modificadores de bônus.

    Args:
        player_items (set): Um conjunto com os nomes de todos os itens que o jogador possui.
        boost_catalogue (dict): O catálogo de bônus pré-filtrado e padronizado.
        non_cumulative_groups (dict, opcional): Dicionário de grupos de itens onde apenas
                                                o item de maior prioridade (primeiro na lista)
                                                aplica seu bônus. Ex: {"beavers": ["Foreman Beaver", ...]}.
        farm_data (dict, opcional): Os dados completos da fazenda, necessários para
                                    verificações de estado (ex: tempo de ativação de coletáveis).

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um bônus ativo
              com seus detalhes (tipo, operação, valor, item de origem, etc.).
    """
    active_boosts = []
    farm_data = farm_data or {}
    non_cumulative_groups = non_cumulative_groups or {}
    all_item_data = _get_all_item_data() # Necessário para checar os efeitos originais
    
    # Rastreia itens que já foram processados por grupos não cumulativos.
    items_in_any_group = set()
    for group_items in non_cumulative_groups.values():
        items_in_any_group.update(group_items)

    # 1. Processa os grupos hierárquicos (não cumulativos).
    # Apenas o primeiro item encontrado no `player_items` dentro de cada grupo
    # (baseado na ordem definida em `non_cumulative_groups`) terá seu bônus aplicado.
    for group_name, ordered_items in non_cumulative_groups.items():
        for item_name in ordered_items:
            if item_name in player_items and item_name in boost_catalogue:
                first_boost = boost_catalogue[item_name]["boosts"][0] # Pega o primeiro bônus para verificar condições gerais
                conditions = first_boost.get("conditions", {})
                source_type = boost_catalogue[item_name].get("source_type")
                duration_days = conditions.get("duration_days")
                duration_hours = conditions.get("duration_hours")

                # Verifica a validade de bônus temporais (se aplicável).
                if duration_days or duration_hours:
                    all_placed_items = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}
                    placements = all_placed_items.get(item_name, [])
                    if placements:
                        activation_ts = placements[0].get("createdAt", 0)
                        now_ts = int(time.time() * 1000)
                        duration_ms = (duration_days or 0) * 24 * 60 * 60 * 1000 + (duration_hours or 0) * 60 * 60 * 1000
                        
                        if now_ts > (activation_ts + duration_ms):
                            continue # Bônus temporal expirou, não aplica.
                
                # Ignora bônus AOE aqui, pois são tratados separadamente por posição de recurso.
                if boost_catalogue[item_name].get("has_aoe"):
                    continue

                item_boosts = boost_catalogue[item_name]["boosts"]
                # Verifica se o item tem um bônus de CRITICAL_CHANCE.
                is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)

                for boost in item_boosts:
                    # Se for um item crítico, seu bônus YIELD não é adicionado aqui,
                    # pois será adicionado apenas se o crítico realmente ocorrer (ver `fruit_service`).
                    if is_critical_item and boost.get("type") == "YIELD":
                        continue
                    active_boosts.append({"source_item": item_name, "source_type": source_type, **boost})
                break # Apenas o primeiro item do grupo se aplica, então sai do loop.

    # 2. Processa todos os outros bônus que não são hierárquicos (cumulativos).
    # Estes bônus são adicionados independentemente de outros itens, desde que o jogador os possua.
    for item_name in player_items:
        if item_name in boost_catalogue and item_name not in items_in_any_group:
            # --- NOVO: Checa se o item é puramente um modificador ---
            # Para isso, consultamos a definição original do item, não o catálogo filtrado.
            original_item_details = all_item_data.get(item_name, {})
            original_effects = original_item_details.get("effects", [])
            
            # Um item é considerado "apenas modificador" se TODOS os seus efeitos são tipos de modificação.
            # Se a lista de efeitos estiver vazia, não é um modificador.
            is_modifier_only = False
            if original_effects:
                is_modifier_only = all(
                    b.get("type") in ["MODIFY_ITEM_AOE", "ITEM_MODIFICATION", "COLLECTIBLE_EFFECT_MULTIPLIER"]
                    for b in original_effects
                )
            
            if is_modifier_only:
                continue # Pula itens que são apenas modificadores, pois sua lógica é tratada em outro lugar.

            first_boost = boost_catalogue[item_name]["boosts"][0]
            conditions = first_boost.get("conditions", {})
            source_type = boost_catalogue[item_name].get("source_type")
            duration_days = conditions.get("duration_days")
            duration_hours = conditions.get("duration_hours")

            # Verifica a validade de bônus temporais (se aplicável).
            if duration_days or duration_hours:
                all_placed_items = {**farm_data.get("collectibles", {}), **farm_data.get("home", {}).get("collectibles", {})}
                placements = all_placed_items.get(item_name, [])
                if placements:
                    activation_ts = placements[0].get("createdAt", 0)
                    now_ts = int(time.time() * 1000)
                    duration_ms = (duration_days or 0) * 24 * 60 * 60 * 1000 + (duration_hours or 0) * 60 * 60 * 1000
                    
                    if now_ts > (activation_ts + duration_ms):
                        continue # Bônus temporal expirou, não aplica.
            
            # Ignora bônus AOE aqui, pois são tratados separadamente por posição de recurso.
            if boost_catalogue[item_name].get("has_aoe") or source_type == "fertiliser":
                continue

            item_boosts = boost_catalogue[item_name]["boosts"]
            # Verifica se o item tem um bônus de CRITICAL_CHANCE.
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)
            for boost in item_boosts:
                # Se for um item crítico, seu bônus YIELD não é adicionado aqui,
                # pois será adicionado apenas se o crítico realmente ocorrer (ver `fruit_service`).
                if is_critical_item and boost.get("type") == "YIELD":
                    continue
                active_boosts.append({"source_item": item_name, "source_type": source_type, **boost})

    # 3. Processa e adiciona os bônus de Buds.
    # Buds são tratados separadamente pois sua ativação e valor podem depender de lógicas complexas.
    bud_analysis_result = bud_service.analyze_bud_buffs(farm_data)
    if bud_analysis_result and bud_analysis_result["internal"]["active_buffs"]:
        winning_bud_buffs = bud_analysis_result["internal"]["active_buffs"]
        winning_bud_info = bud_analysis_result["internal"]["winning_bud_info"]

        for buff_key, buff_value_float in winning_bud_buffs.items():
            original_buff_found = False
            original_details = {}
            # Encontra os detalhes originais do bônus do Bud no domínio.
            for bud_type_name, bud_type_data in bud_service.bud_domain.BUD_BUFFS.items():
                for buff in bud_type_data.get("boosts", []):
                    if bud_service._get_buff_key(buff) == buff_key:
                        original_details = buff
                        original_buff_found = True
                        break
                if original_buff_found:
                    break

            if original_buff_found:
                source_bud = winning_bud_info.get(buff_key)
                source_item_name = "Buds"
                if source_bud:
                    source_item_name = f"Bud #{source_bud['bud_id']} ({source_bud['type']}, {source_bud['aura']})" # Nome detalhado do Bud

                active_boosts.append({
                    "source_item": source_item_name,
                    "source_type": "bud",
                    "type": original_details.get("type"),
                    "operation": original_details.get("operation"),
                    "value": Decimal(str(buff_value_float)), # Valor do bônus do Bud
                    "conditions": original_details.get("conditions", {})
                })

    # 4. ETAPA FINAL: Processa todos os modificadores sobre a lista de bônus ativos.
    # Isso garante que bônus que alteram outros bônus sejam aplicados por último.
    final_processed_boosts = _process_boost_modifiers(active_boosts, player_items)

    return final_processed_boosts

def get_aoe_boosts_for_resource(resource_position: dict, placed_items: dict, player_skills: set, farm_data: dict = None) -> list:
    """
    Calcula os bônus de Área de Efeito (AOE) que se aplicam a uma posição específica,
    considerando modificações de skills e o estado do jogo (sem cooldowns).

    Args:
        resource_position (dict): As coordenadas {'x': int, 'y': int} do recurso a ser verificado.
        placed_items (dict): Um dicionário de todos os itens colocados na fazenda
                             (ex: farm_data['collectibles'] ou farm_data['home']['collectibles']).
        player_skills (set): Um conjunto com os nomes de todas as habilidades que o jogador possui.
        farm_data (dict, opcional): Os dados completos da fazenda, necessários para verificações de estado.

    Returns:
        list: Uma lista de dicionários de bônus que se aplicam àquela posição específica.
    """
    active_aoe_boosts = []
    farm_data = farm_data or {}

    # Validação básica da posição do recurso.
    if not resource_position or resource_position.get('x') is None or resource_position.get('y') is None:
        return active_aoe_boosts

    rx, ry = resource_position['x'], resource_position['y']

    # Unifica todos os itens que podem ter AOE para consulta (atualmente apenas coletáveis).
    all_aoe_items = {**collectibles_domain.COLLECTIBLES_ITEM_BUFFS}

    for item_name, placements in placed_items.items():
        item_details = all_aoe_items.get(item_name)
        # Ignora itens que não têm detalhes ou não possuem definição de AOE.
        if not item_details or "aoe" not in item_details:
            continue
        
        # --- Lógica de Modificação de AOE por Skills ---
        final_aoe = item_details["aoe"]
        aoe_modifier_skill = None  # Rastreia a skill que modifica a AOE

        for skill_name in player_skills:
            skill_details = skills_domain.BUMPKIN_REVAMP_SKILLS.get(skill_name)
            if not skill_details: continue
            
            for effect in skill_details.get("effects", []):
                if effect.get("name") == "MODIFY_ITEM_AOE" and effect.get("target_item") == item_name:
                    final_aoe = effect["new_aoe"]
                    aoe_modifier_skill = skill_name  # Armazena o nome da skill
                    break
            if aoe_modifier_skill:
                break

        # Itera sobre cada instância do item colocada na fazenda.
        for placement in placements:
            placement_coords = placement.get("coordinates", {})
            ax, ay = placement_coords.get("x"), placement_coords.get("y")
            if ax is None or ay is None: continue

            is_within_range = False
            shape = final_aoe.get("shape")

            if shape == "custom":
                for plot in final_aoe.get("plots", []):
                    if rx == (ax + plot["x"]) and ry == (ay + plot["y"]):
                        is_within_range = True
                        break
            
            elif shape == "circle":
                radius = final_aoe.get("radius", 0)
                dx = abs(rx - ax)
                dy = abs(ry - ay)
                if dx <= radius and dy <= radius and not (dx == 0 and dy == 0):
                    is_within_range = True
            
            if is_within_range:
                # Adiciona todos os bônus do item à lista de bônus AOE ativos.
                for boost in item_details.get("boosts", []):
                    boost_to_add = {"source_item": f"{item_name} (AOE)", "source_type": "collectible", **boost}

                    # Se uma skill modificou a AOE, processa os bônus e modificadores.
                    if aoe_modifier_skill:
                        if "modifiers" not in boost_to_add:
                            boost_to_add["modifiers"] = []
                        
                        skill_yield_bonus = Decimal('0')
                        skill_details = skills_domain.BUMPKIN_REVAMP_SKILLS.get(aoe_modifier_skill)
                        if skill_details:
                            for effect in skill_details.get("effects", []):
                                if effect.get("type") == boost_to_add.get("type") and effect.get("operation") == boost_to_add.get("operation"):
                                    skill_value = Decimal(str(effect.get("value", 0)))
                                    boost_to_add["value"] = float(Decimal(str(boost_to_add.get("value", 0))) + skill_value)
                                    skill_yield_bonus = skill_value
                                    break

                        # Adiciona um único modificador combinado para a UI
                        modifier_text = "Area of Effect"
                        if skill_yield_bonus > 0:
                            modifier_text += f", +{skill_yield_bonus} Yield"

                        boost_to_add["modifiers"].append({
                            "source_item": aoe_modifier_skill,
                            "value": modifier_text,
                            "operation": "special",
                            "source_type": "skill"
                        })
                    
                    active_aoe_boosts.append(boost_to_add)
                break 

    return active_aoe_boosts

def get_crop_tier(crop_name: str) -> str | None:
    """
    Retorna o tier ('basic', 'medium', 'advanced') de uma cultura específica.
    Consulta as listas de tiers pré-calculadas no domínio de culturas (`crops_domain`).

    Args:
        crop_name (str): O nome da cultura.

    Returns:
        str | None: O tier da cultura (ex: 'basic', 'medium', 'advanced') ou None se não encontrado.
    """
    if crop_name in crops_domain.CROP_TIERS["basic"]:
        return "basic"
    if crop_name in crops_domain.CROP_TIERS["medium"]:
        return "medium"
    if crop_name in crops_domain.CROP_TIERS["advanced"]:
        return "advanced"
    return None

def _conditions_are_met(conditions: dict, resource_name: str, node_context: dict = None) -> bool:
    """
    Função auxiliar para verificar se todas as condições de um bônus são atendidas
    para um determinado recurso e contexto de nó. Esta função é crucial para
    determinar se um bônus específico deve ser aplicado.

    Args:
        conditions (dict): Um dicionário de condições a serem verificadas (ex: {"resource": "Wood", "faction": "Goblins"}).
        resource_name (str): O nome do recurso atual sendo avaliado (ex: "Apple", "Stone").
        node_context (dict, opcional): Um dicionário com informações adicionais sobre o nó
                                       (ex: {"minesLeft": 1} para minerais).

    Returns:
        bool: True se todas as condições forem atendidas, False caso contrário.
    """
    context = node_context or {}

    for condition_key, required_value in conditions.items():
        # Condição de Recurso/Item/Cultura (ex: "resource": "Wood" ou "resource": ["Crop", "Fruit"])
        if condition_key in ["resource", "item", "crop"]:
            # Garante que `required_value` seja sempre uma lista para iteração consistente.
            required_list = required_value if isinstance(required_value, list) else [required_value]
            
            # Lógica para verificar se o recurso atual pertence a alguma das categorias
            # especificadas na condição (ex: se "Lemon" é uma "Fruit").
            is_met_by_category = False
            for req_val in required_list:
                if req_val in RESOURCE_CATEGORIES: # Verifica se o valor requerido é uma categoria conhecida
                    if resource_name in RESOURCE_CATEGORIES[req_val]: # Verifica se o recurso pertence a essa categoria
                        is_met_by_category = True
                        break
            
            # Se a condição foi atendida por uma categoria, continua para a próxima chave de condição.
            if is_met_by_category:
                continue
            
            # Lógica original: Se não foi atendida por categoria, verifica se o nome do recurso
            # está diretamente na lista de valores requeridos (ex: "Wood" em ["Wood", "Stone"]).
            if resource_name not in required_list:
                return False # Condição não atendida.
        
        # Condição de Categoria (ex: "category": "Fruit" ou "target_category": "BasicCrop")
        elif condition_key in ["category", "target_category"]:
            required_list = required_value if isinstance(required_value, list) else [required_value]
            
            is_met = False
            for category_name in required_list:
                if category_name in RESOURCE_CATEGORIES:
                    if resource_name == category_name or resource_name in RESOURCE_CATEGORIES[category_name]:
                        is_met = True
                        break
                else:
                    log.warning(f"Categoria de bônus desconhecida encontrada: '{category_name}'. A condição será considerada como não atendida.")
            
            if not is_met:
                return False

        # Condição de Minas Restantes (específico para mineração, ex: "minesLeft": 1)
        elif condition_key == "minesLeft":
            current_value = context.get("minesLeft")
            if current_value != required_value:
                return False
        
        # Condição de Tier da Cultura (ex: "crop_tier": "basic")
        elif condition_key == "crop_tier":
            current_tier = get_crop_tier(resource_name)
            if not current_tier:
                return False # A cultura não tem um tier definido ou não existe, então a condição não é atendida.
            
            # Garante que `required_value` seja uma lista para iteração consistente.
            required_list = required_value if isinstance(required_value, list) else [required_value]
            if current_tier not in required_list:
                return False # O tier da cultura não corresponde ao requerido.
        
        # Condição de Exclusão (ex: "exclude_target": ["Apple", "Banana"])
        # Se o `resource_name` estiver na lista de exclusão, a condição NÃO é atendida.
        elif condition_key == "exclude_target":
            excluded_list = required_value if isinstance(required_value, list) else [required_value]
            if resource_name in excluded_list:
                return False
        
        # Condição de Fação (ex: "faction": "Goblins")
        elif condition_key == "faction":
            # Assume que a facção do jogador está no contexto ou em algum lugar acessível.
            # Esta lógica precisaria ser expandida se a facção não estiver no `node_context`.
            player_faction = context.get("player_faction") # Exemplo: obter a facção do jogador do contexto
            if player_faction != required_value:
                return False

    return True # Todas as condições foram atendidas.

def extract_and_process_temporal_boosts(active_boosts: list, farm_data: dict) -> tuple:
    """
    Separa os bônus temporais dos bônus normais e anexa seus timestamps de ativação.
    Bônus temporais são aqueles que só afetam ações iniciadas após sua ativação
    e que possuem uma duração limitada.

    Args:
        active_boosts (list): A lista completa de bônus ativos do jogador.
        farm_data (dict): Os dados completos da fazenda para buscar o 'createdAt'
                          (timestamp de criação/ativação de coletáveis).

    Returns:
        tuple: Uma tupla contendo:
               - (list) Bônus temporais processados com seus timestamps de ativação.
               - (list) Bônus regulares (não temporais).
               - (set) Nomes dos itens que fornecem bônus temporais.
    """
    temporal_boosts_processed = []
    regular_boosts = []
    temporal_item_names = set()

    # Unifica todos os itens colocados na fazenda (principal e casa) para verificar timestamps.
    all_placed_items = farm_data.get("collectibles", {})
    all_placed_items.update(farm_data.get("home", {}).get("collectibles", {}))

    for boost in active_boosts:
        # Verifica se o bônus é marcado como temporal.
        if boost.get("is_temporal"):
            item_name = boost.get("source_item")
            placements = all_placed_items.get(item_name, [])
            
            if placements:
                # Assume que o primeiro item colocado é o relevante para o timestamp de ativação.
                activation_ts = placements[0].get("createdAt", 0)
                temporal_boosts_processed.append({"boost": boost, "activation_ts": activation_ts})
                temporal_item_names.add(item_name)
            else:
                log.warning(f"Bônus temporal '{item_name}' encontrado, mas o item não foi localizado nos dados da fazenda. Ignorando.")
        else:
            regular_boosts.append(boost)
            
    return temporal_boosts_processed, regular_boosts, temporal_item_names

def calculate_final_recovery_time(base_time: float, active_boosts: list, resource_name: str, node_context: dict = None) -> dict:
    """
    Calcula o tempo de recuperação final de um recurso com base nos bônus ativos.
    Filtra os bônus que afetam o tempo de recuperação com base no nome do recurso
    e no contexto do nó.

    Args:
        base_time (float): O tempo de recuperação base do recurso (em segundos).
        active_boosts (list): A lista de bônus ativos do jogador.
        resource_name (str): O nome do recurso para o qual o tempo de recuperação está sendo calculado.
        node_context (dict, opcional): Contexto adicional do nó (ex: para condições específicas).

    Returns:
        dict: Um dicionário contendo o tempo de recuperação base, o tempo final
              e os detalhes dos bônus aplicados.
    """
    base_recovery_time = Decimal(str(base_time))
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    for boost in active_boosts:
        conditions = boost.get("conditions", {})
        # Verifica se o bônus se aplica ao recurso e é um tipo de bônus de tempo de recuperação.
        if _conditions_are_met(conditions, resource_name, node_context) and boost.get("type") in ["RECOVERY_TIME", "GROWTH_TIME", "SUPER_TOTEM_TIME_BOOST"]:
                operation = boost["operation"]
                value = Decimal(str(boost["value"]))

                # Aplica a operação do bônus (multiplicação percentual ou direta).
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
    Calcula o rendimento final de um recurso, aplicando bônus determinísticos e
    identificando bônus de chance (críticos).

    Args:
        base_yield (float): O rendimento base do recurso.
        active_boosts (list): A lista de bônus ativos do jogador.
        resource_name (str): O nome do recurso para o qual o rendimento está sendo calculado.
        node_context (dict, opcional): Contexto adicional do nó (ex: para condições específicas).

    Returns:
        dict: Um dicionário contendo o rendimento base, o rendimento final determinístico,
              detalhes de bônus de chance e os bônus aplicados.
    """
    base = Decimal(str(base_yield))
    additive_bonus = Decimal('0')
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []
    chance_bonuses = []

    for boost in active_boosts:
        conditions = boost.get("conditions", {})
        # Verifica se o bônus se aplica ao recurso atual.
        if _conditions_are_met(conditions, resource_name, node_context):
            boost_type = boost.get("type")
            # Processa bônus de rendimento direto (YIELD).
            if boost_type == "YIELD":
                operation = boost["operation"]
                value = Decimal(str(boost["value"]))

                # Aplica a operação do bônus (aditivo, subtrativo, percentual, multiplicativo).
                boost_to_apply = boost.copy()
                if operation == "add":
                    additive_bonus += value
                elif operation == "subtract":
                    additive_bonus -= value
                    boost_to_apply['value'] = -float(value) # Store as negative for UI
                elif operation == "percentage":
                    multiplicative_factor *= (Decimal('1') + value)
                elif operation == "multiply":
                    multiplicative_factor *= value

                applied_buffs_details.append(boost_to_apply)
            # Processa bônus de chance de rendimento (BONUS_YIELD_CHANCE).
            elif boost_type == "BONUS_YIELD_CHANCE":
                chance_bonuses.append({
                    "source_item": boost.get("source_item", "Unknown"),
                    "chance": float(boost.get("value", 0)),
                    "multiplier": float(boost.get("bonus_multiplier", 1)),
                })
                applied_buffs_details.append(boost)

    # Calcula o rendimento determinístico final.
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

    Args:
        player_items (set): Um conjunto com os nomes de todos os itens que o jogador possui.
        active_boosts (list): A lista de bônus ativos do jogador (sem os bônus de crítico já ocorridos).
        boost_catalogue (dict): O catálogo de bônus pré-filtrado e padronizado.
        resource_conditions (dict): Condições de recurso para filtrar bônus relevantes.
        special_skills (dict, opcional): Dicionário de habilidades especiais que podem afetar o rendimento.

    Returns:
        dict: Um dicionário contendo os rendimentos mínimo e máximo possíveis para cada recurso,
              juntamente com os bônus que contribuem para esses valores.
    """
    special_skills = special_skills or {}
    all_potential_boosts = list(active_boosts) # Começa com os bônus ativos normais.

    # 1. Adiciona bônus de itens que concedem CRITICAL_CHANCE.
    # Estes bônus são considerados para o cálculo do rendimento MÁXIMO potencial.
    for item_name in player_items:
        if item_name in boost_catalogue:
            item_boosts = boost_catalogue[item_name].get("boosts", [])
            is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in item_boosts)
            
            if is_critical_item:
                for boost in item_boosts:
                    # Adiciona o bônus YIELD associado ao CRITICAL_CHANCE para o cálculo do máximo.
                    if boost.get("type") == "YIELD":
                        all_potential_boosts.append({"source_item": f"{item_name} (Critical Potential)", **boost})

    # 2. Adiciona bônus de skills especiais (inerentes ou de domínio específico).
    # Ex: Skill "Native" (comum a madeira e mineração) que pode dar bônus crítico.
    native_skill_data = skills_domain.BUMPKIN_REVAMP_SKILLS.get("Native")
    if native_skill_data:
        for boost in native_skill_data.get("effects", []):
            if boost.get("type") == "YIELD":
                all_potential_boosts.append({"source_item": "Native (Critical Potential)", **boost})
                break 

    # Skills de domínio específico (ex: Greenhouse Gamble) que podem ter bônus YIELD.
    for skill_name, skill_data in special_skills.items():
        if skill_name in player_items:
            for boost in skill_data.get("effects", []):
                if boost.get("type") == "YIELD":
                    all_potential_boosts.append({"source_item": f"{skill_name} (Critical Potential)", **boost})
                    break

    min_max_data = {}
    
    # Identifica todos os recursos que podem ser afetados por bônus de rendimento.
    affected_resources = set()
    for boost in all_potential_boosts:
        if boost.get("type") == "YIELD":
            conditions = boost.get("conditions", {})
            resource_or_item = conditions.get("resource") or conditions.get("item") or conditions.get("crop")
            if resource_or_item:
                resource_list = resource_or_item if isinstance(resource_or_item, list) else [resource_or_item]
                affected_resources.update(resource_list)

    # Filtra os recursos afetados que são relevantes para as condições de rendimento principais.
    main_yield_resources = [name for name in affected_resources if name in resource_conditions.get('yield_resource_names', [])]

    # Calcula o rendimento mínimo e máximo para cada recurso relevante.
    for resource_name in sorted(list(set(main_yield_resources))):
        # Obtém a lógica de rendimento base para o recurso (padrão é 1).
        base_yield_logic = resource_conditions.get('base_yield_logic', lambda r: 1)
        base_yield = base_yield_logic(resource_name)
        if base_yield == 0: continue # Ignora recursos com rendimento base zero.

        # Filtra os bônus YIELD que se aplicam ao recurso atual para o cálculo do rendimento máximo.
        player_max_yield_boosts = [b for b in all_potential_boosts if b.get("type") == "YIELD" and _conditions_are_met(b.get("conditions", {}), resource_name, {})]
        # Calcula o rendimento máximo determinístico.
        max_yield_info = calculate_final_yield(base_yield, player_max_yield_boosts, resource_name)
        max_yield = max_yield_info['final_deterministic']

        # Se o rendimento máximo for maior que o base, adiciona aos dados de min/max.
        if max_yield > base_yield:
            min_max_data[resource_name] = {
                "base": float(base_yield), "max": float(max_yield),
                "contributing_boosts": max_yield_info['applied_buffs']
            }

    return dict(sorted(min_max_data.items()))
