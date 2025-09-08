"""
Este módulo é responsável por analisar o estado dos "fruit patches" (canteiros de frutas)
na fazenda do jogador, calcular o rendimento e o tempo de recuperação das frutas,
e aplicar bônus de itens, habilidades e acertos críticos.

Ele atua como um orquestrador, utilizando funções do `resource_analysis_service`
para a lógica centralizada de cálculo de bônus.
"""

import logging
import time
from collections import defaultdict
from decimal import Decimal

# Imports dos domínios que contêm os dados brutos das frutas e outros recursos
from ..domain import fruits as fruit_domain
from ..domain import resources as resources_domain
# Importa as funções necessárias do serviço de análise centralizado.
# Este serviço é a "fonte da verdade" para como os bônus são processados.
from .resource_analysis_service import (_get_player_items,
                                        calculate_final_recovery_time,
                                        calculate_final_yield,
                                        filter_boosts_from_domains,
                                        get_active_player_boosts)

log = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTES DE REGRAS DE NEGÓCIO PARA FRUTAS
# ==============================================================================

# Define as condições específicas para filtrar bônus relevantes para frutas.
# Estas condições são passadas para o `filter_boosts_from_domains`
# para construir o catálogo de bônus `FRUIT_BOOST_CATALOGUE`.
FRUIT_RESOURCE_CONDITIONS = {
    # Nomes dos recursos de rendimento (frutas) que este serviço se importa.
    'yield_resource_names': list(fruit_domain.FRUIT_SEEDS.keys()),
    # Nomes dos recursos de recuperação (frutas) que este serviço se importa.
    'recovery_resource_names': list(fruit_domain.FRUIT_SEEDS.keys()),
    # Nome da árvore de habilidades à qual as habilidades de fruta pertencem.
    'skill_tree_name': 'Fruit Patch',
    # Categorias de bônus que são relevantes para frutas (ex: "Fruit" para itens).
    'boost_category_names': ['Fruit']
}

# O catálogo de bônus é pré-calculado uma única vez na inicialização do módulo.
# Ele contém todos os bônus (de habilidades, vestíveis, coletáveis, etc.)
# que são relevantes para as condições de frutas definidas acima.
FRUIT_BOOST_CATALOGUE = filter_boosts_from_domains(FRUIT_RESOURCE_CONDITIONS)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _get_fruit_yield_amount(game_state: dict, fruit_name: str, fertiliser: str, active_boosts: list) -> dict:
    """
    Calcula o rendimento final de uma fruta, aplicando todos os bônus ativos.
    Esta função é um orquestrador que delega o cálculo principal ao
    `resource_analysis_service.calculate_final_yield`.

    Args:
        game_state (dict): O estado atual do jogo da fazenda.
        fruit_name (str): O nome da fruta para a qual o rendimento será calculado.
        fertiliser (str): O nome do fertilizante aplicado (se houver).
        active_boosts (list): Uma lista pré-processada de todos os bônus ativos
                               que se aplicam a esta fruta, incluindo bônus de
                               acertos críticos já ocorridos.

    Returns:
        dict: Um dicionário contendo o rendimento base, o rendimento final
              determinístico e detalhes dos bônus aplicados.
    """
    # O rendimento base de uma fruta é 1.0 antes de qualquer bônus.
    base_yield = 1.0

    # Delega o cálculo do rendimento final ao serviço de análise de recursos.
    # Este serviço lida com a aplicação de todos os tipos de bônus (aditivos,
    # multiplicativos, etc.) e a verificação de condições.
    yield_calculation = calculate_final_yield(
        base_yield=base_yield,
        active_boosts=active_boosts, # Usa a lista de bônus já processada
        resource_name=fruit_name
    )

    return yield_calculation

def _get_fruit_patch_recovery_time(game_state: dict, fruit_name: str) -> dict:
    """
    Calcula o tempo de recuperação de um canteiro de frutas após a colheita.

    Args:
        game_state (dict): O estado atual do jogo da fazenda.
        fruit_name (str): O nome da fruta plantada no canteiro.

    Returns:
        dict: Um dicionário contendo o tempo de recuperação final e os bônus aplicados.
    """
    # Obtém o nome da semente associada à fruta.
    seed_name = fruit_domain.FRUIT_DATA.get(fruit_name, {}).get("seed_name")
    if not seed_name:
        log.warning(f"Semente não encontrada para a fruta: {fruit_name}")
        return {"final": 0, "applied_buffs": []}
    
    # Obtém o tempo base de plantio/recuperação da semente.
    base_time = fruit_domain.FRUIT_SEEDS.get(seed_name, {}).get("plantSeconds", 0)
    if base_time == 0:
        log.warning(f"Tempo base de plantio/recuperação zero para a semente: {seed_name}")
        return {"final": 0, "applied_buffs": []}

    # Obtém todos os itens que o jogador possui para calcular os bônus ativos.
    player_items = _get_player_items(game_state)
    active_boosts = get_active_player_boosts(
        player_items=player_items,
        boost_catalogue=FRUIT_BOOST_CATALOGUE,
        farm_data=game_state
    )
    
    # Delega o cálculo do tempo de recuperação final ao serviço de análise de recursos.
    return calculate_final_recovery_time(base_time, active_boosts, fruit_name)

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_fruit_patches(farm_data: dict) -> dict:
    """
    Analisa todos os canteiros de frutas na fazenda do jogador,
    calcula o rendimento e o tempo de recuperação para cada um,
    e agrega um resumo geral.

    Esta é a função principal do serviço de frutas, orquestrando
    a coleta de dados e a aplicação de bônus.

    Args:
        farm_data (dict): Os dados completos da fazenda do jogador.

    Returns:
        dict: Um relatório detalhado do estado dos canteiros de frutas,
              incluindo resumos e cálculos individuais.
    """
    fruit_patches_api_data = farm_data.get("fruitPatches", {})
    analyzed_patches = {}
    # defaultdict para facilitar a agregação de dados de resumo por fruta.
    summary = defaultdict(lambda: {"total": 0, "ready": 0, "growing": 0, "total_yield": Decimal('0')})
    current_timestamp_ms = int(time.time() * 1000)

    for patch_id, patch_data in fruit_patches_api_data.items():
        fruit_details = patch_data.get("fruit")
        if not fruit_details:
            continue # Pula se não houver detalhes da fruta no canteiro

        fruit_name = fruit_details.get("name")
        if not fruit_name:
            continue # Pula se o nome da fruta não for encontrado

        summary[fruit_name]["total"] += 1 # Incrementa o contador total para esta fruta
        
        # Calcula o tempo de recuperação do canteiro
        recovery_info = _get_fruit_patch_recovery_time(farm_data, fruit_name)
        final_recovery_ms = recovery_info["final"] * 1000 # Converte segundos para milissegundos
        
        # Armazena o tempo de recuperação final no resumo, se ainda não estiver lá
        if 'final_recovery_time' not in summary[fruit_name]:
            summary[fruit_name]['final_recovery_time'] = recovery_info.get('final', 0)

        # Determina se a fruta está pronta para colheita
        last_harvested_at = fruit_details.get("harvestedAt", fruit_details.get("plantedAt", 0))
        ready_at_ms = last_harvested_at + final_recovery_ms
        is_ready = current_timestamp_ms >= ready_at_ms

        state_name = "Pronto" if is_ready else "Crescendo"
        summary[fruit_name]["ready" if is_ready else "growing"] += 1 # Atualiza o resumo de estado

        fertiliser_name = patch_data.get("fertiliser", {}).get("name")
        
        # 1. Obtém todos os itens que o jogador possui (habilidades, vestíveis, etc.).
        player_items = _get_player_items(farm_data)
        # Adiciona o fertilizante aplicado ao conjunto de itens do jogador, se houver.
        if fertiliser_name:
            player_items.add(fertiliser_name)

        # 2. Obtém a lista inicial de bônus ativos do jogador, filtrados pelo catálogo de frutas.
        active_boosts = get_active_player_boosts(
            player_items=player_items,
            boost_catalogue=FRUIT_BOOST_CATALOGUE,
            farm_data=farm_data
        )

        # 3. Processa acertos críticos (critical hits) que já ocorreram.
        # A API informa se um acerto crítico ocorreu para uma habilidade específica.
        fruit_specific_boosts = list(active_boosts) # Cria uma cópia para adicionar bônus de crítico
        critical_hits = fruit_details.get("criticalHit", {}) # Obtém dados de acertos críticos da API

        for hit_name, hit_count in critical_hits.items():
            # Se o acerto crítico ocorreu (hit_count > 0) e a habilidade/item está no catálogo de bônus
            if hit_count > 0 and hit_name in FRUIT_BOOST_CATALOGUE:
                source_type = FRUIT_BOOST_CATALOGUE[hit_name].get("source_type")
                # Itera sobre os bônus definidos para a habilidade/item que causou o crítico.
                for boost in FRUIT_BOOST_CATALOGUE[hit_name].get("boosts", []):
                    # Se for um bônus de rendimento (YIELD), adiciona-o à lista de bônus específicos da fruta.
                    if boost.get("type") == "YIELD":
                        fruit_specific_boosts.append({
                            "type": "YIELD",
                            "operation": boost["operation"],
                            "value": boost["value"],
                            "source_item": f"{hit_name} (Critical Hit)", # Marca como acerto crítico para exibição
                            "source_type": source_type
                        })

        # 4. Calcula o rendimento final da fruta, passando a lista de bônus
        #    que agora inclui os acertos críticos já ocorridos.
        yield_info = _get_fruit_yield_amount(
            game_state=farm_data,
            fruit_name=fruit_name,
            fertiliser=fertiliser_name,
            active_boosts=fruit_specific_boosts # Passa a lista de bônus atualizada
        )
        # Adiciona o rendimento determinístico total ao resumo.
        summary[fruit_name]['total_yield'] += Decimal(str(yield_info['final_deterministic']))

        # Armazena os dados analisados para este canteiro específico.
        analyzed_patches[patch_id] = {
            "id": patch_id,
            "fruit_name": fruit_name,
            "state_name": state_name,
            "harvests_left": fruit_details.get("harvestsLeft", 0),
            "ready_at_timestamp_ms": int(ready_at_ms),
            "calculations": {"yield": yield_info, "recovery": recovery_info},
            "fertiliser": patch_data.get("fertiliser"),
            "has_yield_fertiliser": True if fertiliser_name else False
        }

    # Prepara os dados para a visualização (frontend).
    view_data = {
        "summary_by_fruit": dict(sorted(summary.items())),
        "patch_status": dict(sorted(analyzed_patches.items())),
    }

    return {"view": view_data}