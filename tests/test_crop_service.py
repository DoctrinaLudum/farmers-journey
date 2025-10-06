# tests/test_crop_service.py

import json
import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.services.calendar_service import CalendarService
from app.services.crop_service import analyze_crop_resources

# Carrega o estado da fazenda a partir de um arquivo JSON de teste
@pytest.fixture
def farm_data():
    with open('161993-25-09-2025.json', 'r') as f:
        return json.load(f)['farm']

def test_bountiful_harvest_with_guardian_bonus_applied_to_crops(farm_data, monkeypatch):
    """
    Testa se o bônus de rendimento do evento 'Bountiful Harvest', modificado
    pelo 'Spring Guardian', é corretamente aplicado às culturas.
    """
    # 1. Simula a data do evento "Bountiful Harvest"
    event_date = datetime(2025, 9, 24, 12, 0, 0, tzinfo=timezone.utc)
    monkeypatch.setattr('app.services.calendar_service.datetime', MagicMock(now=lambda tz: event_date))

    # 2. Obtém os bônus sazonais (que devem incluir a modificação do guardião)
    calendar_service = CalendarService(farm_data)
    seasonal_boosts = calendar_service.get_seasonal_boosts()

    # Verifica se o bônus MODIFICADO foi pego (1 do evento + 1 do guardião)
    assert len(seasonal_boosts) > 0
    assert seasonal_boosts[0]['item'] == 'Crop'
    assert seasonal_boosts[0]['value'] == 2
    assert 'modifiers' in seasonal_boosts[0]
    assert seasonal_boosts[0]['modifiers'][0]['source_item'] == 'Spring Guardian'

    # 3. Executa a análise de culturas, passando os bônus do evento
    result = analyze_crop_resources(farm_data, calendar_boosts=seasonal_boosts)

    # 4. Verifica se o bônus foi aplicado corretamente em uma cultura específica
    #    Vamos usar o primeiro plot de Cevada como exemplo ("1")
    barley_plot_id = "1"
    plot_status = result.get("view", {}).get("plot_status", {})
    barley_plot_analysis = plot_status.get(barley_plot_id)

    assert barley_plot_analysis is not None, "Análise para o plot de Cevada não encontrada."

    yield_calcs = barley_plot_analysis.get("calculations", {}).get("yield", {})
    applied_buffs = yield_calcs.get("applied_buffs", [])

    print("Applied Buffs:", applied_buffs)

    # Procura pelo buff do evento na lista de buffs aplicados
    event_buff_found = False
    for buff in applied_buffs:
        if buff.get("source_type") == "event" and "bountifulHarvest" in buff.get("source_item", ""):
            event_buff_found = True
            assert buff.get("value") == 2 # Verifica se o valor do buff aplicado é 2
            break
    
    assert event_buff_found, "O bônus do evento Bountiful Harvest não foi encontrado nos buffs aplicados."

    # 5. Verifica o rendimento final
    # Rendimento esperado: 1 (base) + 2 (Evento + Guardian) = 3. Outros bônus de AOE podem se aplicar.
    final_yield = yield_calcs.get('final_deterministic', 0)
    assert final_yield >= 3.0, f"O rendimento final esperado era >= 3.0, mas foi {final_yield}"

