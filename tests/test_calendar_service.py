
import json
from datetime import datetime, timezone
import app.services.calendar_service
from app.services.calendar_service import CalendarService

def load_mock_farm_data(filepath):
    """Carrega os dados mock da fazenda a partir de um arquivo JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)

def test_get_active_event_bountiful_harvest(mocker):
    """
    Testa se o evento 'bountifulHarvest' é corretamente identificado em um dia de evento.
    """
    # Carrega os dados da API mockada
    farm_data = load_mock_farm_data('161993-25-09-2025.json')

    # Simula a data atual para ser o dia do evento 'bountifulHarvest'
    mock_date = datetime(2025, 9, 24, 12, 0, 0, tzinfo=timezone.utc)
    mocker.patch('app.services.calendar_service.datetime', autospec=True)
    app.services.calendar_service.datetime.now.return_value = mock_date

    # Inicializa o serviço com os dados mockados
    calendar_service = CalendarService(farm_data['farm'])

    # Chama a função e verifica o resultado
    active_event = calendar_service.get_active_event()
    assert active_event == "bountifulHarvest"

def test_get_active_event_no_event(mocker):
    """
    Testa se nenhum evento é retornado em um dia sem evento.
    """
    farm_data = load_mock_farm_data('161993-25-09-2025.json')

    # Simula uma data onde não há evento agendado
    mock_date = datetime(2025, 9, 25, 12, 0, 0, tzinfo=timezone.utc)
    mocker.patch('app.services.calendar_service.datetime', autospec=True)
    app.services.calendar_service.datetime.now.return_value = mock_date

    calendar_service = CalendarService(farm_data['farm'])
    active_event = calendar_service.get_active_event()
    assert active_event is None

def test_get_active_event_unknown_event(mocker):
    """
    Testa se um evento 'unknown' é ignorado.
    """
    farm_data = load_mock_farm_data('161993-25-09-2025.json')

    # Simula a data de um evento 'unknown'
    mock_date = datetime(2025, 9, 26, 12, 0, 0, tzinfo=timezone.utc)
    mocker.patch('app.services.calendar_service.datetime', autospec=True)
    app.services.calendar_service.datetime.now.return_value = mock_date

    calendar_service = CalendarService(farm_data['farm'])
    active_event = calendar_service.get_active_event()
    assert active_event is None

def test_get_seasonal_boosts_with_guardian(mocker):
    """
    Testa se os boosts sazonais são aplicados corretamente com um guardião ativo.
    """
    farm_data = load_mock_farm_data('161993-25-09-2025.json')

    # Garante que a season seja 'Spring' e o guardião esteja nos itens
    farm_data['farm']['season'] = {'season': 'Spring'}
    farm_data['farm']['home']['collectibles']['Spring Guardian'] = [{
        "coordinates": {"x": 0, "y": 0},
        "readyAt": 1706789120013,
        "createdAt": 1706789120013,
        "id": "spring-guardian"
    }]

    # Simula a data do evento 'bountifulHarvest'
    mock_date = datetime(2025, 9, 24, 12, 0, 0, tzinfo=timezone.utc)
    mocker.patch('app.services.calendar_service.datetime', autospec=True)
    app.services.calendar_service.datetime.now.return_value = mock_date

    calendar_service = CalendarService(farm_data['farm'])
    
    boosts = calendar_service.get_seasonal_boosts()

    assert len(boosts) > 0
    # O esperado é que ambos os boosts de YIELD (Crop e Fruit) tenham o valor 2
    crop_yield_boost = next((b for b in boosts if b['type'] == 'YIELD' and b['item'] == 'Crop'), None)
    fruit_yield_boost = next((b for b in boosts if b['type'] == 'YIELD' and b['item'] == 'Fruit'), None)
    
    assert crop_yield_boost is not None
    assert crop_yield_boost['value'] == 2
    assert 'modifiers' in crop_yield_boost
    assert crop_yield_boost['modifiers'][0]['source_item'] == 'Spring Guardian'

    assert fruit_yield_boost is not None
    assert fruit_yield_boost['value'] == 2
    assert 'modifiers' in fruit_yield_boost
    assert fruit_yield_boost['modifiers'][0]['source_item'] == 'Spring Guardian'

