# app/services/bud_service.py

import logging
from collections import defaultdict
from decimal import Decimal

from ..domain import budItemBuffs as bud_domain

log = logging.getLogger(__name__)

def _get_buff_key(buff: dict) -> str:
    """Cria uma chave de identificação única para um tipo de bônus."""
    # Usamos o 'name' padronizado para a chave, que é mais confiável
    return buff.get("name", buff.get("type", "UNKNOWN"))

def analyze_bud_buffs(farm_data: dict) -> dict:
    """
    Analisa os Buds de um jogador, calcula os bônus totais aplicando a aura
    e a regra de "maior bônus prevalece", e retorna um relatório detalhado.
    """
    buds_api_data = farm_data.get("buds")
    if not buds_api_data:
        return None

    # --- ETAPA 1: Calcular o "Poder Final" de cada Bud individualmente ---
    processed_buds = {}
    for bud_id, details in buds_api_data.items():
        # 1a. Soma dos bônus base (Type + Stem) para este Bud
        base_buffs = defaultdict(Decimal)
        
        # Função auxiliar para somar bônus do Type e Stem
        def add_buffs_from_source(source_name):
            source_info = bud_domain.BUD_BUFFS.get(source_name)
            if source_info:
                for buff in source_info.get("boosts", []):
                    key = _get_buff_key(buff)
                    base_buffs[key] += Decimal(str(buff.get("value", 0)))

        add_buffs_from_source(details.get("type"))
        add_buffs_from_source(details.get("stem"))

        # 1b. Obter o multiplicador da Aura deste Bud
        aura_name = details.get("aura", "No Aura")
        aura_multiplier = Decimal('1.0') # Padrão é 1x
        if aura_name and aura_name != "No Aura":
            aura_info = bud_domain.BUD_BUFFS.get(aura_name)
            if aura_info and aura_info.get("boosts"):
                aura_multiplier = Decimal(str(aura_info["boosts"][0]["value"]))

        # 1c. Aplicar a Aura aos bônus base para obter o "Poder Final" do Bud
        final_buffs = {}
        for key, value in base_buffs.items():
            final_buffs[key] = value * aura_multiplier

        processed_buds[bud_id] = {
            "id": bud_id,
            "type": details.get("type"),
            "stem": details.get("stem"),
            "aura": aura_name,
            "aura_multiplier": float(aura_multiplier),
            "final_buffs": {k: float(v) for k, v in final_buffs.items()}
        }

    # --- ETAPA 2: Aplicar a regra "O Maior Bônus Prevalece" ---
    # Compara o poder final de todos os buds para cada tipo de bônus
    final_farm_buffs = defaultdict(Decimal)

    for _bud_id, bud_data in processed_buds.items():
        for buff_key, buff_value_float in bud_data["final_buffs"].items():
            buff_value = Decimal(str(buff_value_float))

            # Define se o bônus é de redução (ex: tempo) ou de aumento (ex: rendimento).
            # A convenção é que bônus de tempo são negativos.
            is_reduction_buff = buff_value < 0

            # Se a chave ainda não existe no resultado final, inicializa com o valor atual.
            if buff_key not in final_farm_buffs:
                final_farm_buffs[buff_key] = buff_value
                continue

            current_best = final_farm_buffs[buff_key]

            # A lógica de "maior bônus" muda dependendo do tipo.
            if is_reduction_buff:
                # Para tempo, o "maior" bônus é o número menor (mais negativo). Ex: -0.2 é melhor que -0.1.
                if buff_value < current_best:
                    final_farm_buffs[buff_key] = buff_value
            else:
                # Para rendimento, o "maior" bônus é o número maior. Ex: 0.5 é melhor que 0.2.
                if buff_value > current_best:
                    final_farm_buffs[buff_key] = buff_value

    # --- ETAPA 3: Formatar o resultado final para o dashboard ---
    buff_summary_for_template = []
    # (Opcional) Aqui você pode criar uma função para traduzir as chaves de bônus
    # para descrições amigáveis, como "+0.5 Wood Yield".
    for key, value in final_farm_buffs.items():
        buff_summary_for_template.append(f"{key}: {value:.2f}")

    # DEBUG: Log dos bônus finais calculados antes de serem retornados.
    log.debug(f"Bud service calculated final farm buffs: {dict(final_farm_buffs)}")

    # O resultado é separado em duas chaves principais:
    # 'internal': Contém dados limpos para serem consumidos por outros serviços.
    # 'view': Contém dados formatados e detalhados para serem usados diretamente nos templates.
    return {
        "internal": {
            "active_buffs": {k: float(v) for k, v in final_farm_buffs.items()}
        },
        "view": {
            "individual_buds": processed_buds,
            "summary_list": sorted(buff_summary_for_template)
        }
    }