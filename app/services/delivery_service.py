# app/services/delivery_service.py

import logging
import time
from datetime import datetime
from decimal import Decimal

from ..domain import fishing as fishing_domain
from ..domain import foods as foods_domain
from ..domain import skills as skills_domain
from ..domain import tasks as tasks_domain
from ..domain import wearablesItemBuffs as wearables_domain
from ..game_state import GAME_STATE

log = logging.getLogger(__name__)

def _get_delivery_ticket_bonuses(farm_data: dict) -> int:
    """
    Calcula os bônus de tickets sazonais para as entregas.
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

def _get_delivery_coin_bonus_multiplier(farm_data: dict, order: dict) -> Decimal:
    """
    Calcula o multiplicador de bônus de moedas para uma entrega específica.
    """
    multiplier = Decimal('1.0')
    bumpkin = farm_data.get("bumpkin", {})
    skills = bumpkin.get("skills", {})
    equipped = bumpkin.get("equipped", {})
    
    faction_name = farm_data.get("faction", {}).get("name")
    if faction_name:
        crown = wearables_domain.WEARABLES_ITEM_BUFFS.get(faction_name, {}).get("crown")
        if crown and crown in equipped.values():
            multiplier += Decimal('0.25')

    if order.get("from") == "betty" and "Betty's Friend" in skills: multiplier += Decimal('0.3')
    if order.get("from") == "victoria" and "Victoria's Secretary" in skills: multiplier += Decimal('0.5')
    if order.get("from") == "blacksmith" and "Forge-Ward Profits" in skills: multiplier += Decimal('0.2')
    if "Nom Nom" in skills and any(item in foods_domain.CONSUMABLES_DATA and item not in fishing_domain.FISHING_DATA for item in order.get("items", {}).keys()):
        multiplier += Decimal('0.1')
            
    return multiplier

def analyze_deliveries(farm_data: dict, game_state: dict) -> dict:
    """
    Analisa a lista completa de entregas/encomendas da API, verifica os 
    requisitos contra o inventário do jogador e retorna um relatório unificado.

    Args:
        farm_data (dict): Os dados completos da fazenda vindos da API.
        game_state (dict): O estado do jogo com a temporada atual.

    Returns:
        dict: Um relatório detalhado sobre o estado das entregas.
    """
    delivery_api_data = farm_data.get("delivery")
    if not delivery_api_data or "orders" not in delivery_api_data:
        log.warning("Dados de 'delivery' ou 'orders' não encontrados na resposta da API.")
        return None

    player_inventory = farm_data.get("inventory", {})
    player_sfl = Decimal(farm_data.get("balance", "0"))
    player_coins = Decimal(str(farm_data.get("coins", "0")))
    
    processed_orders = []
    
    for order in delivery_api_data.get("orders", []):
        npc_name_raw = order.get("from", "Unknown")
        is_completed = "completedAt" in order
        
        # Separa os requisitos em itens, SFL e moedas
        requirements = order.get("items", {})
        required_items = {k: v for k, v in requirements.items() if k not in ["sfl", "coins"]}
        required_sfl = Decimal(str(requirements.get("sfl", "0")))
        required_coins = Decimal(str(requirements.get("coins", "0")))

        # Verifica se o jogador tem os itens, SFL e moedas necessários
        has_required_items = True
        for item, required_amount in required_items.items():
            if Decimal(player_inventory.get(item, "0")) < Decimal(str(required_amount)):
                has_required_items = False
                break
        
        has_required_sfl = player_sfl >= required_sfl
        has_required_coins = player_coins >= required_coins

        can_fulfill = has_required_items and has_required_sfl and has_required_coins and not is_completed

        # Processa as recompensas, aplicando bônus
        raw_reward = order.get("reward", {})
        processed_reward = {}

        # Se a recompensa da API estiver vazia, verifica se é um NPC de ticket
        if not raw_reward and npc_name_raw in tasks_domain.TICKET_NPCS:
            seasonal_ticket_name = game_state.get("current_ticket_name")
            if seasonal_ticket_name:
                base_tickets = tasks_domain.TICKET_DELIVERY_REWARDS.get(npc_name_raw, 0)
                bonus_tickets = _get_delivery_ticket_bonuses(farm_data)
                total_tickets = base_tickets + bonus_tickets
                
                processed_reward = {"tickets": total_tickets}
                log.debug(f"Calculated ticket reward for {npc_name_raw}: base={base_tickets}, bonus={bonus_tickets}, total={total_tickets}")
        
        # Se a recompensa da API não estiver vazia, processa normalmente
        elif raw_reward:
            for key, value in raw_reward.items():
                if key == "coins":
                    coin_bonus_multiplier = _get_delivery_coin_bonus_multiplier(farm_data, order)
                    processed_reward[key] = Decimal(str(value)) * coin_bonus_multiplier
                elif key == "items" and isinstance(value, dict):
                    processed_reward.update(value)
                else:
                    processed_reward[key] = value

        processed_orders.append({
            "id": order.get("id"),
            "npc_name": npc_name_raw.title(),
            "requirements": {"items": required_items, "sfl": required_sfl, "coins": required_coins},
            "reward": processed_reward,
            "is_completed": is_completed,
            "can_fulfill": can_fulfill,
            "completed_at": datetime.fromtimestamp(order["completedAt"] / 1000).strftime('%Y-%m-%d %H:%M:%S') if is_completed else None
        })

    # Compila o resumo final
    summary = {
        "completed_count": sum(1 for order in processed_orders if order["is_completed"]),
        "pending_count": sum(1 for order in processed_orders if not order["is_completed"]),
        "fulfillable_now": sum(1 for order in processed_orders if order["can_fulfill"]),
        "total_available": len(processed_orders)
    }

    return {
        "all_deliveries": sorted(processed_orders, key=lambda x: (x['is_completed'], x['npc_name'])),
        "summary": summary,
        "milestone": delivery_api_data.get("milestone", {}),
        "seasonal_ticket_name": game_state.get("current_ticket_name")
    }