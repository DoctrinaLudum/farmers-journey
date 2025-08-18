# app/services/chores_service.py

import logging
import time
from decimal import Decimal

from ..domain import seasons as seasons_domain
from ..domain import tasks as tasks_domain
from ..game_state import GAME_STATE

log = logging.getLogger(__name__)


def _get_chore_ticket_bonuses(farm_data: dict) -> int:
    """
    Calcula os bônus de tickets ADICIONAIS (VIP e itens sazonais) para as chores.
    Esta lógica é mantida separada do delivery_service para garantir independência.
    """
    bonus = 0
    # 1. Bônus VIP
    if farm_data.get("vip", {}).get("expiresAt", 0) > int(time.time() * 1000):
        bonus += 2

    # 2. Bônus de Itens Sazonais
    current_season = GAME_STATE.get("current_season_name", "unknown")
    bonus_items = tasks_domain.SEASONAL_TICKET_BOOST_ITEMS.get(current_season, [])

    player_items = set(farm_data.get("collectibles", {}).keys())
    player_items.update(farm_data.get("home", {}).get("collectibles", {}).keys())
    player_items.update(farm_data.get("bumpkin", {}).get("equipped", {}).values())

    farm_hands_data = farm_data.get("farmHands", {}).get("bumpkins", {})
    if farm_hands_data:
        for hand in farm_hands_data.values():
            player_items.update(hand.get("equipped", {}).values())

    bonus += sum(1 for item in bonus_items if item in player_items)

    return bonus


def _calculate_final_chore_reward(farm_data: dict, chore: dict) -> dict:
    """
    Calcula a recompensa final para uma tarefa (chore), aplicando bônus
    para bilhetes sazonais.
    """
    base_reward = chore.get("reward", {})
    final_reward = {k: v.copy() for k, v in base_reward.items()}

    seasonal_ticket = GAME_STATE.get("current_ticket_name")
    if not seasonal_ticket or seasonal_ticket not in final_reward.get("items", {}):
        return final_reward

    base_tickets = final_reward["items"][seasonal_ticket]
    bonus_tickets = _get_chore_ticket_bonuses(farm_data)
    final_reward["items"][seasonal_ticket] = base_tickets + bonus_tickets

    return final_reward


def analyze_chore_board(farm_data: dict) -> dict | None:
    """
    Analisa os dados do Chore Board, calcula o progresso de cada tarefa e
    retorna um dicionário estruturado com os resultados.

    Args:
        farm_data: O dicionário completo de dados da fazenda da API.

    Returns:
        Um dicionário contendo a análise das tarefas ou None se não houver dados.
    """
    chore_board_data = farm_data.get("choreBoard")
    if not chore_board_data or not chore_board_data.get("chores"):
        return None

    bumpkin_activity = farm_data.get("bumpkin", {}).get("activity", {})
    analyzed_chores = {}

    for npc_name, chore in chore_board_data["chores"].items():
        chore_name = chore.get("name")
        if not chore_name:
            continue

        # Busca a regra da tarefa no nosso domínio
        task_rule = tasks_domain.CHORE_BOARD_TASKS.get(chore_name)
        if not task_rule:
            log.warning(f"Regra não encontrada para a tarefa: '{chore_name}'")
            continue

        activity_name = task_rule.get("activity_name")
        requirement = Decimal(str(task_rule.get("requirement", 0)))

        # Calcula o progresso
        initial_progress = Decimal(str(chore.get("initialProgress", 0)))
        current_activity_value = Decimal(str(bumpkin_activity.get(activity_name, 0)))
        
        current_progress = current_activity_value - initial_progress
        is_complete = current_progress >= requirement
        progress_percent = 0
        if requirement > 0:
            progress_percent = min((current_progress / requirement) * 100, 100)

        # Calcula a recompensa final, aplicando bônus
        final_reward = _calculate_final_chore_reward(farm_data, chore)

        analyzed_chores[npc_name] = {
            "npc_name": npc_name,
            "name": chore_name,
            "reward": chore.get("reward", {}),
            "requirement": float(requirement),
            "final_reward": final_reward,
            "current_progress": float(current_progress),
            "progress_percent": float(progress_percent),
            "is_complete": is_complete,
        }

    return {"chores": analyzed_chores}
