# app/services/wood_service.py

import logging
import time
from datetime import datetime
from decimal import Decimal

log = logging.getLogger(__name__)

# Importa todos os "bancos de dados" de regras e bônus dos nossos domínios
from ..domain import collectiblesItemBuffs as collectibles_domain
from ..domain import resources as resources_domain
from ..domain import skills as skills_domain
from ..domain import wearablesItemBuffs as wearables_domain

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO
# ==============================================================================

# HIERARQUIA DE BÔNUS NÃO-CUMULATIVOS
# Para cada grupo, apenas o bônus do item de maior ranking que o jogador possui será aplicado.
# A ordem na lista é do MELHOR para o PIOR.
NON_CUMULATIVE_BOOST_GROUPS = {
    "beaver_boost": ["Foreman Beaver", "Apprentice Beaver","Woody the Beaver"]
}

# ==============================================================================
# ETAPA 1: FILTRAGEM E PREPARAÇÃO DOS DADOS MESTRES
# Esta seção cria um catálogo otimizado apenas com os bônus de madeira.
# ==============================================================================

def _get_all_item_data():
    """Unifica todos os dicionários de domínio em um único lugar."""
    return {
        **skills_domain.LEGACY_BADGES,
        **skills_domain.BUMPKIN_REVAMP_SKILLS,
        **wearables_domain.WEARABLES_ITEM_BUFFS,
        **collectibles_domain.COLLECTIBLES_ITEM_BUFFS
    }

def _filter_wood_boosts_from_domains():
    """
    Varre todos os domínios e cria um dicionário otimizado contendo
    apenas os itens e bônus que afetam a coleta de madeira. Esta versão
    é mais robusta para lidar com inconsistências nos dados de domínio,
    como o uso de 'effects' em vez de 'boosts'.
    """
    wood_boost_catalogue = {}
    log.info("Iniciando a catalogação de bônus de madeira de todos os domínios...")
    all_item_data = _get_all_item_data()

    for item_name, item_details in all_item_data.items():
        # Procura por 'boosts' ou 'effects' para encontrar a lista de bônus.
        boost_list = item_details.get("boosts") or item_details.get("effects")

        if not item_details or not boost_list or not item_details.get("enabled", True):
            continue

        # VERIFICAÇÃO DE RELEVÂNCIA: Se o item for uma habilidade, ele deve pertencer
        # à árvore de habilidades "Trees". Isso evita que habilidades de outras árvores
        # (como "Fruit Patch") que mencionam "Wood" sejam incluídas incorretamente.
        if item_name in skills_domain.BUMPKIN_REVAMP_SKILLS and item_details.get("tree") != "Trees":
            continue

        # CORREÇÃO: "Tough Tree" não é um bônus passivo. É um gatilho para um evento de
        # 'criticalHit'. Excluí-lo do catálogo geral evita que seja aplicado a todas as
        # árvores. A lógica de sua aplicação será tratada individualmente por árvore.
        if item_name == "Tough Tree":
            continue

        relevant_boosts = []
        for boost in boost_list:
            conditions = boost.get("conditions", {})
            
            # Lógica de verificação mais flexível para rendimento (YIELD)
            is_yield_boost = (
                boost.get("type") in ["YIELD", "RESOURCE_YIELD", "BONUS_YIELD_CHANCE"] and
                (conditions.get("resource") == "Wood" or conditions.get("item") == "Wood")
            )
            
            # Lógica de verificação mais flexível para tempo de recuperação (RECOVERY_TIME)
            is_recovery_boost = (
                boost.get("type") in ["RECOVERY_TIME", "TREE_RECOVERY_TIME"] and
                (conditions.get("resource") == "Tree" or conditions.get("item") == "Tree")
            )

            if is_yield_boost or is_recovery_boost:
                # Padroniza o tipo para o que o resto do serviço espera, facilitando os cálculos
                standardized_boost = boost.copy()
                if boost.get("type") in ["YIELD", "RESOURCE_YIELD"]:
                    standardized_boost['type'] = 'YIELD'
                elif boost.get("type") in ["RECOVERY_TIME", "TREE_RECOVERY_TIME"]:
                    standardized_boost['type'] = 'RECOVERY_TIME'
                
                relevant_boosts.append(standardized_boost)

        if relevant_boosts:
            # Adiciona a fonte do item (wearable, collectible, skill)
            source_type = "wearable" if item_name in wearables_domain.WEARABLES_ITEM_BUFFS else \
                          "collectible" if item_name in collectibles_domain.COLLECTIBLES_ITEM_BUFFS else \
                          "skill"
            
            # Log para cada item encontrado
            log.debug(f"Item de madeira catalogado: '{item_name}' (Fonte: {source_type})")
            
            wood_boost_catalogue[item_name] = {
                "boosts": relevant_boosts,
                "source_type": source_type
            }

    log.info(f"Catalogação de bônus de madeira concluída. Total de itens encontrados: {len(wood_boost_catalogue)}")
    return wood_boost_catalogue


# Criamos o catálogo uma única vez quando o serviço é carregado.
# Isso é muito mais eficiente do que refazer a filtragem a cada chamada.
WOOD_BOOST_CATALOGUE = _filter_wood_boosts_from_domains()

# ==============================================================================
# ETAPA 2: IDENTIFICAÇÃO DOS BÔNUS ATIVOS DO JOGADOR
# ==============================================================================

def get_active_player_wood_boosts(player_items: set) -> list:    
    """
    Pega um conjunto de nomes de itens que o jogador possui e os cruza com o
    catálogo de bônus de madeira para retornar uma lista de bônus ativos,
    respeitando as hierarquias de bônus não-cumulativos.
    """
    active_boosts = []
    
    # Constrói um conjunto de todos os itens que pertencem a um grupo hierárquico
    # para facilitar a exclusão posterior.
    items_in_any_group = set()
    for group_items in NON_CUMULATIVE_BOOST_GROUPS.values():
        items_in_any_group.update(group_items)

    # 1. Processa os grupos hierárquicos
    for group_name, ordered_items in NON_CUMULATIVE_BOOST_GROUPS.items():
        for item_name in ordered_items:  # Itera do melhor para o pior
            if item_name in player_items and item_name in WOOD_BOOST_CATALOGUE:
                # Encontrou o melhor item que o jogador possui neste grupo.
                # Adiciona seus bônus e para de procurar neste grupo.
                log.debug(f"Aplicando bônus hierárquico de '{group_name}': '{item_name}'. Outros no grupo serão ignorados.")
                for boost in WOOD_BOOST_CATALOGUE[item_name]["boosts"]:
                    active_boosts.append({
                        "source_item": item_name,
                        **boost
                    })
                break  # Para de procurar neste grupo e vai para o próximo.

    # 2. Processa todos os outros bônus que não são hierárquicos
    for item_name in player_items:
        if item_name in WOOD_BOOST_CATALOGUE and item_name not in items_in_any_group:
            for boost in WOOD_BOOST_CATALOGUE[item_name]["boosts"]:
                active_boosts.append({
                    "source_item": item_name,
                    **boost
                })

    return active_boosts

# ==============================================================================
# ETAPA 3: CÁLCULO DOS EFEITOS
# As funções abaixo recebem a lista de bônus já filtrada e aplicam os cálculos.
# ==============================================================================

def _calculate_final_yield(base_yield: float, active_boosts: list) -> dict:
    """
    Calcula o rendimento final de madeira, separando bônus determinísticos
    (aditivos/multiplicativos) de bônus baseados em chance.
    """
    base_wood = Decimal(str(base_yield))
    additive_bonus = Decimal('0')
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []
    chance_bonuses = []

    for boost in active_boosts:
        boost_type = boost.get("type")

        if boost_type == "YIELD":
            operation = boost["operation"]
            value = Decimal(str(boost["value"]))

            if operation == "add":
                additive_bonus += value
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
                "description": f"{boost.get('value', 0):.0%} chance of x{boost.get('bonus_multiplier', 1)} yield"
            })
            # Também adiciona aos buffs gerais para transparência
            applied_buffs_details.append(boost)
            
    # CORREÇÃO: A ordem das operações foi ajustada. Os bônus multiplicativos
    # (como Tough Tree) devem ser aplicados diretamente ao valor base, e só
    # depois os bônus aditivos (como Lumberjack) são somados.
    final_deterministic_wood = (base_wood * multiplicative_factor) + additive_bonus
    
    return {
        "base": float(base_wood),
        "final_deterministic": float(final_deterministic_wood),
        "chance_bonuses": chance_bonuses,
        "applied_buffs": applied_buffs_details
    }

def _calculate_final_recovery_time(base_time: float, active_boosts: list) -> dict:
    """Calcula o tempo de recuperação final com base nos bônus ativos."""
    base_recovery_time = Decimal(str(base_time))
    multiplicative_factor = Decimal('1')
    applied_buffs_details = []

    for boost in active_boosts:
        if boost.get("type") == "RECOVERY_TIME":
            operation = boost["operation"]
            value = Decimal(str(boost["value"])) # ex: -0.5

            if operation == "percentage":
                multiplicative_factor *= (Decimal('1') + value)

            # Anexa o dicionário de bônus completo para consistência com a função de yield.
            applied_buffs_details.append(boost)

    final_time = base_recovery_time * multiplicative_factor

    return {
        "base": float(base_recovery_time),
        "final": float(final_time),
        "applied_buffs": applied_buffs_details
    }

# Mapeamento para traduzir nomes de bônus de Bud para o formato interno do serviço.
# Isso torna a adição de novos bônus de Bud mais fácil no futuro.
BUD_BUFF_TO_WOOD_BOOST_MAPPING = {
    'WOOD_YIELD': {'type': 'YIELD', 'operation': 'add'},
    'TREE_RECOVERY_TIME': {'type': 'RECOVERY_TIME', 'operation': 'percentage'}
}


# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# Esta é a única função que você precisará chamar de suas rotas.
# ==============================================================================
def analyze_wood_resources(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa os dados das árvores da API, calcula todos os bônus de madeira
    e retorna um relatório completo. Inclui a integração de bônus de Buds.

    Args:
        farm_data: O dicionário de dados da API principal da fazenda.
        active_bud_buffs (opcional): Um dicionário com os bônus de Bud já
                                     processados e ativos para a fazenda.
    """
    # DEBUG: Log para confirmar quais bônus de Bud foram recebidos pela função.
    log.debug(f"Wood service received active_bud_buffs: {active_bud_buffs}")

    # Consolida todos os itens do jogador (e dos seus ajudantes) em um único conjunto.
    
    # 1. Habilidades (Skills) do Bumpkin principal
    player_items = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())

    # 2. Colecionáveis (Collectibles) da fazenda e da casa
    player_items.update(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())

    # 2.5. Itens no Inventário (para bônus de emblemas legados, como 'Lumberjack')
    # Esta linha é crucial para identificar bônus que não são wearables nem skills novas.
    player_items.update(farm_data.get("inventory", {}).keys())

    # 3. Itens Vestíveis (Wearables) do Bumpkin principal e dos Ajudantes (Farm Hands)
    player_items.update(farm_data.get("bumpkin", {}).get("equipped", {}).values())
    
    farm_hands_data = farm_data.get("farmHands", {}).get("bumpkins", {})
    if farm_hands_data:
        for hand in farm_hands_data.values():
            player_items.update(hand.get("equipped", {}).values())

    # ETAPA 1 já foi feita quando o serviço carregou (WOOD_BOOST_CATALOGUE)

    # ETAPA 2: Identifica quais bônus de madeira o jogador tem ativos
    active_boosts = get_active_player_wood_boosts(player_items)

    # Integração dos bônus de Buds, se disponíveis.
    # Esta seção foi atualizada para ser compatível com o novo `bud_service`,
    # que passa diretamente o dicionário de bônus ativos.
    if active_bud_buffs:
        log.info("Integrando bônus de Buds na análise de madeira.")
        for bud_buff_name, mapping in BUD_BUFF_TO_WOOD_BOOST_MAPPING.items():
            if bud_buff_name in active_bud_buffs:
                boost_value = active_bud_buffs[bud_buff_name]
                
                # Adiciona o bônus apenas se o valor for significativo
                if boost_value != 0:
                    boost = {
                        "source_item": "Buds",
                        "type": mapping['type'],
                        "operation": mapping['operation'],
                        "value": boost_value,
                    }
                    active_boosts.append(boost)
                    log.debug(f"Bônus de Bud para '{bud_buff_name}' adicionado: {boost}")

    # ETAPA 3: Análise individual de cada árvore
    trees_api_data = farm_data.get("trees", {})
    analyzed_trees = {}
    summary = {"total": 0, "ready": 0, "growing": 0, "total_yield": Decimal('0')}
    critical_hit_stats = {}
    current_timestamp_ms = int(time.time() * 1000)
    
    wood_cycle_data = resources_domain.RESOURCES_DATA["Wood"]["details"]["cycle"]

    for tree_id, tree_data in trees_api_data.items():
        summary["total"] += 1
        chopped_at_ms = tree_data.get("wood", {}).get("choppedAt", 0)
        
        # Coleta estatísticas de golpes críticos do último corte
        critical_hits = tree_data.get("wood", {}).get("criticalHit", {})
        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0:
                critical_hit_stats[hit_name] = critical_hit_stats.get(hit_name, 0) + hit_count

        # Determina o estado da árvore com base na vida restante (amount)
        remaining_hp = tree_data.get("wood", {}).get("amount", 3)
        if remaining_hp >= 3:
            tree_state_name = "Tree"
        elif remaining_hp == 2:
            tree_state_name = "Stump"
        elif remaining_hp == 1:
            tree_state_name = "Sapling"
        else:
            tree_state_name = "Tree" # Fallback para valores inesperados
            log.warning(f"HP inesperado ({remaining_hp}) para a árvore {tree_id}. Usando 'Tree' como padrão.")

        tree_state_data = wood_cycle_data.get(tree_state_name)

        # Começa com os bônus gerais do jogador.
        tree_specific_boosts = list(active_boosts)

        # CORREÇÃO: Lógica explícita para aplicar bônus garantidos pela API para a próxima colheita.
        # Isso é feito aqui em vez de no catálogo geral para garantir que o bônus seja aplicado
        # apenas à árvore específica que teve o 'criticalHit'.
        if critical_hits.get("Tough Tree") == 1:
            tree_specific_boosts.append({
                "type": "YIELD", "operation": "multiply", "value": 3,
                "source_item": "Tough Tree (Critical Hit)" # Multiplica o rendimento por 3
            })
        
        if critical_hits.get("Native") == 1:
            tree_specific_boosts.append({
                "type": "YIELD", "operation": "add", "value": 1,
                "source_item": "Native (Critical Hit)"
            })

        base_yield = tree_state_data["yield_amount"]
        yield_info = _calculate_final_yield(base_yield, tree_specific_boosts)
        summary['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        base_recovery = tree_state_data["recovery_time_seconds"]
        recovery_info = _calculate_final_recovery_time(base_recovery, tree_specific_boosts)
        
        final_recovery_ms = recovery_info["final"] * 1000

        if not chopped_at_ms or chopped_at_ms == 0:
            status = "Ready"
            summary["ready"] += 1
            ready_at_ms = current_timestamp_ms
        else:
            ready_at_ms = chopped_at_ms + final_recovery_ms
            if current_timestamp_ms >= ready_at_ms:
                status = "Ready"
                summary["ready"] += 1
            else:
                status = "Growing"
                summary["growing"] += 1

        analyzed_trees[tree_id] = {
            "id": tree_id,
            "createdAt": tree_data.get("createdAt", 0), # Adiciona o timestamp de criação para ordenação
            "status": status,
            "state_name": tree_state_name,
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {
                "yield": yield_info,
                "recovery": recovery_info,
            }
        }
    
    # --- ETAPA 4: Montagem do Relatório Final ---
    # A saída é estruturada para separar dados de 'view' (para o template)
    # de dados 'internal' (para possível consumo por outros serviços).

    # Dados para a view, formatados e ordenados.
    view_data = {
        "summary": summary,
        # Ordena as árvores pela data de criação ('createdAt') para garantir uma ordem consistente.
        "tree_status": dict(sorted(analyzed_trees.items(), key=lambda item: item[1].get('createdAt', 0))),
        "critical_hit_stats": critical_hit_stats,
        "active_boost_items": sorted(list(set(b['source_item'] for b in active_boosts))),
        "all_catalogued_items": sorted(list(WOOD_BOOST_CATALOGUE.keys()))
    }

    # Dados internos, mais brutos, para possível uso futuro ou depuração.
    internal_data = {
        "analyzed_trees_raw": analyzed_trees,
        "active_boosts_raw": active_boosts
    }
    return {
        "internal": internal_data,
        "view": view_data
    }