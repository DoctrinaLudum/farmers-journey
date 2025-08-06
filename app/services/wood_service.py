# app/services/wood_service.py

import logging
import time
from decimal import Decimal

log = logging.getLogger(__name__)

from ..domain import resources as resources_domain
from . import resource_analysis_service

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO
# ==============================================================================

# HIERARQUIA DE BÔNUS NÃO-CUMULATIVOS
# Para cada grupo, apenas o bônus do item de maior ranking que o jogador possui será aplicado.
# A ordem na lista é do MELHOR para o PIOR.
NON_CUMULATIVE_BOOST_GROUPS = {
    "beaver_boost": ["Foreman Beaver", "Apprentice Beaver","Woody the Beaver"]
}

# Configuração específica para o recurso "Madeira"
WOOD_RESOURCE_CONDITIONS = {
    'yield_resource_names': ['Wood'],
    'recovery_resource_names': ['Tree'],
    'skill_tree_name': 'Trees',
    'excluded_items': [] # Não é mais necessário, a lógica agora é automatizada.
}

# Criamos o catálogo uma único vez quando o serviço é carregado.
# Isso é muito mais eficiente do que refazer a filtragem a cada chamada.
WOOD_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(WOOD_RESOURCE_CONDITIONS)

# Mapeamento para traduzir nomes de bônus de Bud para o formato interno do serviço.
# Isso torna a adição de novos bônus de Bud mais fácil no futuro.
BUD_BUFF_TO_WOOD_BOOST_MAPPING = {
    'WOOD_YIELD': {'type': 'YIELD', 'operation': 'add'},
    'TREE_RECOVERY_TIME': {'type': 'RECOVERY_TIME', 'operation': 'percentage'}
}

# Mapeamento de HP para o estado da árvore para simplificar a lógica.
HP_TO_STATE_MAP = {
    3: "Tree",
    2: "Stump",
    1: "Sapling"
}

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# Esta é a única função que você precisará chamar de suas rotas.
# ==============================================================================
def analyze_wood_resources(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa os dados das árvores da API, calcula todos os bônus de madeira
    e retorna um relatório completo. Usa o serviço genérico de análise de recursos.

    Args:
        farm_data: O dicionário de dados da API principal da fazenda.
        active_bud_buffs (opcional): Um dicionário com os bônus de Bud já
                                     processados e ativos para a fazenda.
    """
    log.debug(f"Wood service received active_bud_buffs: {active_bud_buffs}")

    # Consolida todos os itens do jogador (e dos seus ajudantes) em um único conjunto.
    player_items = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())
    player_items.update(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())
    player_items.update(farm_data.get("inventory", {}).keys())
    player_items.update(farm_data.get("bumpkin", {}).get("equipped", {}).values())
    
    farm_hands_data = farm_data.get("farmHands", {}).get("bumpkins", {})
    if farm_hands_data:
        for hand in farm_hands_data.values():
            player_items.update(hand.get("equipped", {}).values())

    # ETAPA 2: Identifica quais bônus de madeira o jogador tem ativos usando o serviço genérico
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        WOOD_BOOST_CATALOGUE,
        NON_CUMULATIVE_BOOST_GROUPS
    )

    # --- NOVO: Lógica para popular a lista de Bônus Ativos ---
    # Itera sobre todos os itens do jogador e verifica se eles existem no catálogo de bônus de madeira.
    # Isso garante que itens com AOE, que são filtrados dos cálculos globais, ainda apareçam na lista da UI.
    active_item_names = {item for item in player_items if item in WOOD_BOOST_CATALOGUE}
    
    # Adiciona "Buds" à lista se houver algum bônus de bud ativo.
    if active_bud_buffs:
        active_item_names.add("Buds")

    # Integração dos bônus de Buds, se disponíveis.
    if active_bud_buffs:
        log.info("Integrando bônus de Buds na análise de madeira.")
        for bud_buff_name, mapping in BUD_BUFF_TO_WOOD_BOOST_MAPPING.items():
            if bud_buff_name in active_bud_buffs and active_bud_buffs[bud_buff_name] != 0:
                # Cria uma cópia do dicionário de mapeamento para não modificar o original.
                boost = mapping.copy()
                # Adiciona as chaves dinâmicas.
                boost["source_item"] = "Buds"
                boost["value"] = active_bud_buffs[bud_buff_name]
                active_boosts.append(boost)
                log.debug(f"Bônus de Bud para '{bud_buff_name}' adicionado: {boost}")

    # ETAPA 3: Análise individual de cada árvore
    trees_api_data = farm_data.get("trees", {})
    analyzed_trees = {}
    placed_collectibles = farm_data.get("collectibles", {})
    player_skills = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())
    summary = {"total": 0, "ready": 0, "growing": 0, "total_yield": Decimal('0')}
    critical_hit_stats = {}
    current_timestamp_ms = int(time.time() * 1000)
    
    wood_cycle_data = resources_domain.RESOURCES_DATA["Wood"]["details"]["cycle"]

    for tree_id, tree_data in trees_api_data.items():
        summary["total"] += 1
        chopped_at_ms = tree_data.get("wood", {}).get("choppedAt", 0)
        
        critical_hits = tree_data.get("wood", {}).get("criticalHit", {})
        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0:
                critical_hit_stats[hit_name] = critical_hit_stats.get(hit_name, 0) + hit_count

        remaining_hp = tree_data.get("wood", {}).get("amount", 3) # O HP é o 'amount' restante
        tree_state_name = HP_TO_STATE_MAP.get(remaining_hp, "Tree")
        if tree_state_name == "Tree" and remaining_hp not in HP_TO_STATE_MAP:
             log.warning(f"HP inesperado ({remaining_hp}) para a árvore {tree_id}. Usando 'Tree' como padrão.")

        tree_state_data = wood_cycle_data.get(tree_state_name)
        tree_specific_boosts = list(active_boosts)
        has_aoe_buff = False

        # Lógica de bônus de AOE
        # CORREÇÃO: Extrai as coordenadas do nível principal do objeto da árvore.
        tree_position = {"x": tree_data.get("x"), "y": tree_data.get("y")}
        if tree_position.get("x") is not None and tree_position.get("y") is not None:
            aoe_boosts = resource_analysis_service.get_aoe_boosts_for_resource(
                resource_position=tree_position,
                placed_items=placed_collectibles,
                player_skills=player_skills
            )
            if aoe_boosts:
                tree_specific_boosts.extend(aoe_boosts)
                has_aoe_buff = True

        # LÓGICA AUTOMATIZADA: Aplica bônus de critical hits confirmados pela API.
        for hit_name, hit_count in critical_hits.items():
            if hit_count > 0 and hit_name in WOOD_BOOST_CATALOGUE:
                # Valida que o item é um item de "golpe crítico" procurando por um boost do tipo CRITICAL_CHANCE.
                is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in WOOD_BOOST_CATALOGUE[hit_name].get("boosts", []))

                if is_critical_item:
                    # Aplica o bônus de YIELD associado.
                    for boost in WOOD_BOOST_CATALOGUE[hit_name].get("boosts", []):
                        if boost.get("type") == "YIELD":
                            tree_specific_boosts.append({
                                "type": "YIELD", "operation": boost["operation"], "value": boost["value"],
                                "source_item": f"{hit_name} (Critical Hit)"
                            })

        base_yield = tree_state_data["yield_amount"]
        yield_info = resource_analysis_service.calculate_final_yield(base_yield, tree_specific_boosts, resource_name="Wood")
        summary['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        base_recovery = tree_state_data["recovery_time_seconds"]
        recovery_info = resource_analysis_service.calculate_final_recovery_time(base_recovery, tree_specific_boosts, resource_name="Tree")
        
        final_recovery_ms = recovery_info["final"] * 1000

        # Lógica de status refatorada para maior clareza.
        is_ready = not chopped_at_ms or current_timestamp_ms >= (chopped_at_ms + final_recovery_ms)

        if is_ready:
            status = "Ready"
            summary["ready"] += 1
            ready_at_ms = current_timestamp_ms
        else:
            status = "Growing"
            summary["growing"] += 1
            ready_at_ms = chopped_at_ms + final_recovery_ms

        analyzed_trees[tree_id] = {
            "id": tree_id,
            "createdAt": tree_data.get("createdAt", 0),
            "status": status,
            "state_name": tree_state_name,
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {
                "yield": yield_info,
                "recovery": recovery_info,
            },
            "has_aoe_buff": has_aoe_buff
        }
    
    # --- ETAPA 4: Montagem do Relatório Final ---
    # A saída é estruturada para separar dados de 'view' (para o template)
    # de dados 'internal' (para possível consumo por outros serviços).
    view_data = {
        "summary": summary,
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
