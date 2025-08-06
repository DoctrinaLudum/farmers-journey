# app/services/mining_service.py

import logging
import time
from decimal import Decimal
from collections import defaultdict

log = logging.getLogger(__name__)

from ..domain import resources as resources_domain
from . import resource_analysis_service

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA MINERAÇÃO
# ==============================================================================

# Define quais recursos e bônus são relevantes para a mineração.
MINING_RESOURCE_CONDITIONS = {
    'yield_resource_names': ['Stone', 'Iron', 'Gold', 'Crimstone', 'Sunstone', 'Oil', 'Obsidian', 'Mineral'],
    'recovery_resource_names': ['Stone Rock', 'Iron Rock', 'Gold Rock', 'Crimstone Rock', 'Sunstone Rock', 'Oil Reserve'],
}

# Itens que não se acumulam (ex: picaretas de níveis diferentes).
# Adicionado como um padrão, mesmo que ainda não existam itens hierárquicos.
NON_CUMULATIVE_BOOST_GROUPS = {
    # "pickaxe_boost": ["Gold Pickaxe", "Stone Pickaxe"]
}

# Mapeamento para bônus de Buds.
BUD_BUFF_TO_MINING_BOOST_MAPPING = {
    'MINERAL_YIELD': {
        'type': 'YIELD',
        'operation': 'add',
        # Aplica o bônus de Bud apenas aos minérios básicos.
        'conditions': {'resource': ['Stone', 'Iron', 'Gold']}
    },
    # Este bônus continuará a ser aplicado a todos os nós de minério.
    'MINERAL_RECOVERY_TIME': {'type': 'RECOVERY_TIME', 'operation': 'percentage'}
}

# O catálogo de bônus de mineração é criado uma única vez.
MINING_BOOST_CATALOGUE = resource_analysis_service.filter_boosts_from_domains(MINING_RESOURCE_CONDITIONS)

# Mapeia as chaves da API para os nomes dos recursos e seus ciclos de vida.
API_KEY_TO_RESOURCE_MAP = {
    "stones": "Stone",
    "iron": "Iron",
    "gold": "Gold",
    "crimstones": "Crimstone",
    "sunstones": "Sunstone",
    "oilReserves": "Oil"
}

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================
def analyze_mining_resources(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa todos os nós de mineração (pedra, ferro, etc.), calcula os bônus
    e retorna um relatório completo.
    """
    # Consolida todos os itens do jogador em um único conjunto.
    player_items = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())
    player_items.update(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())
    player_items.update(farm_data.get("inventory", {}).keys())
    player_items.update(farm_data.get("bumpkin", {}).get("equipped", {}).values())
    
    farm_hands_data = farm_data.get("farmHands", {}).get("bumpkins", {})
    if farm_hands_data:
        for hand in farm_hands_data.values():
            player_items.update(hand.get("equipped", {}).values())

    # Identifica os bônus de mineração ativos do jogador.
    active_boosts = resource_analysis_service.get_active_player_boosts(
        player_items,
        MINING_BOOST_CATALOGUE,
        NON_CUMULATIVE_BOOST_GROUPS
    )

    # --- NOVO: Lógica para popular a lista de Bônus Ativos ---
    active_item_names = {item for item in player_items if item in MINING_BOOST_CATALOGUE}
    if active_bud_buffs:
        active_item_names.add("Buds")
    # --- FIM DA NOVA LÓGICA ---

    # Integração dos bônus de Buds.
    if active_bud_buffs:
        log.info("Integrando bônus de Buds na análise de mineração.")
        for bud_buff_name, mapping in BUD_BUFF_TO_MINING_BOOST_MAPPING.items():
            if bud_buff_name in active_bud_buffs and active_bud_buffs[bud_buff_name] != 0:
                # Cria uma cópia do dicionário de mapeamento para não modificar o original.
                boost = mapping.copy()
                # Adiciona as chaves dinâmicas.
                boost["source_item"] = "Buds"
                boost["value"] = active_bud_buffs[bud_buff_name]
                active_boosts.append(boost)

    # Análise individual de cada nó de mineração.
    analyzed_nodes = {}
    summary = defaultdict(lambda: {"total": 0, "ready": 0, "recovering": 0, "total_yield": Decimal('0')})
    placed_collectibles = farm_data.get("collectibles", {})
    player_skills = set(farm_data.get("bumpkin", {}).get("skills", {}).keys())
    critical_hit_stats = {}
    current_timestamp_ms = int(time.time() * 1000)

    for api_key, resource_name in API_KEY_TO_RESOURCE_MAP.items():
        nodes_api_data = farm_data.get(api_key, {})
        
        # Acesso seguro aos dados do recurso e do seu ciclo de vida.
        resource_data = resources_domain.RESOURCES_DATA.get(resource_name, {})
        resource_cycle_data = resource_data.get("details", {}).get("cycle", {})
        
        if not resource_cycle_data:
            log.warning(f"Dados de ciclo não encontrados para o recurso '{resource_name}'. Pulando análise.")
            continue

        # Usa a chave 'source' do domínio para obter o nome correto do nó (ex: "Stone Rock", "Oil Reserve").
        node_state_name = resource_data.get("source")
        if not node_state_name:
            log.warning(f"Nome do nó de origem ('source') não encontrado para o recurso '{resource_name}'. Pulando análise.")
            continue

        for node_id, node_data in nodes_api_data.items():
            summary[resource_name]["total"] += 1
            
            stone_details = node_data.get("stone", {})
            mined_at_ms = stone_details.get("minedAt", 0)
            critical_hits = stone_details.get("criticalHit", {})
            for hit_name, hit_count in critical_hits.items():
                if hit_count > 0:
                    critical_hit_stats[hit_name] = critical_hit_stats.get(hit_name, 0) + hit_count

            # Usa o nome do estado do nó correto (ex: "Stone Rock", "Oil Reserve")
            node_state_data = resource_cycle_data.get(node_state_name, {})
            
            # Cria um contexto específico do nó para passar para o serviço de análise.
            node_context = {
                "minesLeft": node_data.get("minesLeft")
            }

            # Cria uma cópia dos bônus para modificar para este nó específico
            node_specific_boosts = list(active_boosts)
            has_aoe_buff = False

            # Lógica de bônus de AOE
            # CORREÇÃO: Extrai as coordenadas do nível principal do objeto do nó.
            node_position = {"x": node_data.get("x"), "y": node_data.get("y")}
            if node_position["x"] is not None and node_position["y"] is not None:
                aoe_boosts = resource_analysis_service.get_aoe_boosts_for_resource(
                    resource_position=node_position,
                    placed_items=placed_collectibles,
                    player_skills=player_skills
                )
                if aoe_boosts:
                    node_specific_boosts.extend(aoe_boosts)
                    has_aoe_buff = True

            # LÓGICA AUTOMATIZADA: Aplica bônus de critical hits confirmados pela API.
            for hit_name, hit_count in critical_hits.items():
                if hit_count > 0 and hit_name in MINING_BOOST_CATALOGUE:
                    # Valida que o item é um item de "golpe crítico" procurando por um boost do tipo CRITICAL_CHANCE.
                    is_critical_item = any(b.get("type") == "CRITICAL_CHANCE" for b in MINING_BOOST_CATALOGUE[hit_name].get("boosts", []))

                    if is_critical_item:
                        # Aplica o bônus de YIELD associado, se as condições baterem.
                        for boost in MINING_BOOST_CATALOGUE[hit_name].get("boosts", []):
                            if boost.get("type") == "YIELD":
                                conditions = boost.get("conditions", {})
                                required_resource = conditions.get("resource")
                                
                                applies = not required_resource or (isinstance(required_resource, list) and resource_name in required_resource) or required_resource == resource_name
                                
                                if applies:
                                    node_specific_boosts.append({"type": "YIELD", "operation": boost["operation"], "value": boost["value"], "source_item": f"{hit_name} (Critical Hit)"})

            # Lógica específica para o bônus de perfuração de Óleo
            if resource_name == "Oil":
                drilled_count = node_data.get("drilled", 0)
                if (drilled_count + 1) % 3 == 0:
                    log.debug(f"Bônus de perfuração de óleo ativado para o nó #{node_id}.")
                    node_specific_boosts.append({"type": "YIELD", "operation": "add", "value": 20, "source_item": "3rd Drill Bonus"})
            
            # Lógica para o bônus de última mineração de Crimstone.
            # Quando "minesLeft" é 1, o jogador recebe um bônus de +2.
            if resource_name == "Crimstone" and node_data.get("minesLeft") == 1:
                log.debug(f"Bônus de última mineração de Crimstone ativado para o nó #{node_id}.")
                node_specific_boosts.append({
                    "type": "YIELD",
                    "operation": "add",
                    "value": 2,
                    "source_item": "Crimstone Last Mine"
                })

            base_yield = node_state_data.get("yield_amount", 0)
            yield_info = resource_analysis_service.calculate_final_yield(base_yield, node_specific_boosts, resource_name=resource_name, node_context=node_context)
            summary[resource_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

            base_recovery = node_state_data.get("recovery_time_seconds", 0)
            recovery_info = resource_analysis_service.calculate_final_recovery_time(base_recovery, node_specific_boosts, resource_name=node_state_name, node_context=node_context)
            final_recovery_ms = recovery_info["final"] * 1000

            is_ready = not mined_at_ms or current_timestamp_ms >= (mined_at_ms + final_recovery_ms)
            
            if is_ready:
                status = "Ready"
                summary[resource_name]["ready"] += 1
                ready_at_ms = current_timestamp_ms
            else:
                status = "Recovering"
                summary[resource_name]["recovering"] += 1
                ready_at_ms = mined_at_ms + final_recovery_ms
            
            analyzed_nodes[f"{resource_name}-{node_id}"] = {
                "id": node_id, "resource_name": resource_name, "status": status,
                "ready_at_timestamp_ms": int(ready_at_ms),
                "calculations": {"yield": yield_info, "recovery": recovery_info},
                "has_aoe_buff": has_aoe_buff
            }

    # Montagem do Relatório Final.
    view_data = {
        "summary": dict(summary),
        "node_status": dict(sorted(analyzed_nodes.items())),
        "critical_hit_stats": critical_hit_stats,
        # Usa a nova lista que inclui itens com AOE.
        "active_boost_items": sorted(list(active_item_names)),
        "all_catalogued_items": sorted(list(MINING_BOOST_CATALOGUE.keys()))
    }

    internal_data = {
        "analyzed_nodes_raw": analyzed_nodes,
        "active_boosts_raw": active_boosts
    }
    
    return {"internal": internal_data, "view": view_data}