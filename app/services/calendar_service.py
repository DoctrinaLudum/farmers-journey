# app/services/calendar_service.py
"""
Serviço responsável por processar e fornecer informações sobre os bônus de 
eventos de calendário ativos, incluindo a aplicação de modificadores como os Guardiões.
"""

import logging
import time
import copy
from typing import List, Dict, Any, Optional

from ..domain import calendar_events as domain_events
from .resource_analysis_service import _get_player_items, _process_boost_modifiers

log = logging.getLogger(__name__)

# =============================================================================
# FUNÇÕES AUXILIARES (LÓGICA INTERNA)
# =============================================================================

def _get_active_event_name(game_state: Dict[str, Any]) -> Optional[str]:
    """
    Verifica o estado do jogo para encontrar um evento de calendário ativo.

    A lógica espelha a função `getActiveCalendarEvent` do código do jogo,
    verificando se o `startedAt` de um evento ocorreu nas últimas 24 horas.

    Args:
        game_state (Dict[str, Any]): O estado completo do jogo.

    Returns:
        Optional[str]: O nome do evento ativo ou None se nenhum for encontrado.
    """
    calendar_data = game_state.get("calendar", {})
    if not calendar_data:
        return None

    TWENTY_FOUR_HOURS_MS = 24 * 60 * 60 * 1000
    current_time_ms = int(time.time() * 1000)

    for event_name in domain_events.CALENDAR_EVENTS:
        event_info = calendar_data.get(event_name)
        if event_info and "startedAt" in event_info:
            started_at_ms = event_info["startedAt"]
            if current_time_ms - started_at_ms < TWENTY_FOUR_HOURS_MS:
                log.debug(f"Evento de calendário ativo encontrado: '{event_name}'")
                return event_name
    
    return None

# =============================================================================
# SERVIÇO PRINCIPAL DE EVENTOS DE CALENDÁRIO
# =============================================================================

def get_active_event_boosts(game_state: Dict[str, Any], category: str) -> List[Dict[str, Any]]:
    """
    Obtém os bônus de evento de calendário ativos para uma categoria específica,
    já com as modificações de itens (como Guardiões) aplicadas.

    O método agora reutiliza a lógica de `resource_analysis_service` para garantir consistência.

    Args:
        game_state (Dict[str, Any]): O estado completo do jogo do jogador.
        category (str): A categoria de item para a qual os bônus são solicitados
                        (ex: "Crop", "Fruit", "Greenhouse").

    Returns:
        List[Dict[str, Any]]: Uma lista de dicionários de bônus, prontos para serem
                               usados por outros serviços.
    """
    active_event_name = _get_active_event_name(game_state)
    if not active_event_name:
        return []

    base_boosts = []
    event_details = domain_events.CALENDAR_EVENTS[active_event_name]

    # 1. Adicionar bônus base do evento, marcando a origem corretamente.
    for boost in event_details.get("boosts", []):
        if boost.get("item") == category or "item" not in boost:
            processed_boost = copy.deepcopy(boost)
            processed_boost["source_item"] = event_details.get("display_name", active_event_name)
            processed_boost["source_type"] = "event"
            base_boosts.append(processed_boost)

    # 2. Obter itens do jogador para aplicar modificadores.
    player_items = _get_player_items(game_state)

    # 3. Aplicar modificações de itens (Guardiões, etc.) usando o serviço central.
    # A função `_process_boost_modifiers` espera que o `target_item` do modificador
    # corresponda ao `source_item` do bônus. Por isso, o `source_item` foi definido
    # como o nome de exibição do evento.
    modified_boosts = _process_boost_modifiers(base_boosts, player_items)

    log.debug(f"Encontrados {len(modified_boosts)} bônus (com modificações) para a categoria '{category}' do evento '{active_event_name}'.")
    return modified_boosts
