# app/services/crop_machine_service.py

import logging
import time
from collections import defaultdict
from decimal import Decimal

from .. import analysis
from . import crop_service

log = logging.getLogger(__name__)

# ==============================================================================
# FUNÇÕES DE CÁLCULO (LÓGICA INTERNA)
# ==============================================================================

def _calculate_pack_yield(game_state: dict, pack: dict) -> dict:
    """
    Calcula o rendimento total de um pacote de sementes na Crop Machine,
    espelhando a lógica de `getPackYieldAmount` de harvestCropMachine.ts.
    """
    total_yield = Decimal('0')
    applied_buffs_details = []
    
    crop_name = pack.get("crop")
    seeds_count = pack.get("seeds", 0)
    
    if not crop_name or seeds_count == 0:
        return {"final_deterministic": 0, "applied_buffs": []}

    # Clona o dicionário de acertos críticos para poder decrementá-lo
    critical_hits_tracker = (pack.get("criticalHit") or {}).copy()

    def critical_drop_simulator(name: str) -> bool:
        """Simula a ocorrência de um acerto crítico, decrementando o contador."""
        if critical_hits_tracker.get(name, 0) > 0:
            critical_hits_tracker[name] -= 1
            return True
        return False

    # Simula a colheita para cada semente no pacote
    for _ in range(seeds_count):
        # Reutiliza a lógica de cálculo de rendimento do crop_service
        # Passando um 'plot' vazio, pois a máquina não tem fertilizante ou abelhas
        single_yield_info = crop_service._get_crop_yield_amount(
            game_state=game_state,
            plot={},
            crop_name=crop_name,
            created_at=int(time.time() * 1000),
            critical_drop=critical_drop_simulator
        )
        total_yield += Decimal(str(single_yield_info['final_deterministic']))
        # Agrega os buffs aplicados para fins de depuração, se necessário
        # applied_buffs_details.extend(single_yield_info['applied_buffs'])

    # Para simplificar, não retornamos a lista gigante de buffs de cada colheita individual
    return {"final_deterministic": float(total_yield), "applied_buffs": []}

# ==============================================================================
# FUNÇÃO PRINCIPAL (ORQUESTRADOR)
# ==============================================================================

def analyze_crop_machine(farm_data: dict, active_bud_buffs: dict = None) -> dict:
    """
    Analisa o estado da Crop Machine, incluindo a fila de produção e o óleo.
    """
    crop_machine_building = farm_data.get("buildings", {}).get("Crop Machine", [])
    if not crop_machine_building:
        return None

    machine_data = crop_machine_building[0]
    queue = machine_data.get("queue", [])
    processed_queue = []
    current_timestamp_ms = int(time.time() * 1000)

    for pack in queue:
        is_ready = current_timestamp_ms >= pack.get("readyAt", float('inf'))
        
        # Usa o rendimento já calculado se disponível, senão calcula
        if "amount" in pack:
            yield_info = {"final_deterministic": pack["amount"], "applied_buffs": []}
        else:
            yield_info = _calculate_pack_yield(farm_data, pack)

        processed_pack = {
            **pack,
            "is_ready": is_ready,
            "yield_info": yield_info,
            "icon_path": analysis.get_item_image_path(pack.get("crop"))
        }
        processed_queue.append(processed_pack)

    return {
        "view": {
            "queue": processed_queue,
            "unallocatedOilTime": machine_data.get("unallocatedOilTime", 0)
        }
    }
