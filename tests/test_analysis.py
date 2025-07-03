# tests/test_analysis.py
from decimal import Decimal
from app import analysis

MOCK_FARM_DATA = {
    "balance": "1000",
    "coins": "0",
    "inventory": {
        "Wood": "50",
        "Stone": "10"
    },
    "expansion_data": {
        "land": {
            "type": "basic",
            "level": 4
        }
    }
    
}

def test_analyze_expansion_progress():
    """
    Testa se a análise de progresso para a próxima expansão funciona corretamente.
    """
    progress = analysis.analyze_expansion_progress(MOCK_FARM_DATA)

    assert progress is not None
    assert progress['next_level'] == 5
    assert len(progress['resources']) == 2

    wood_req = next(item for item in progress['resources'] if item['name'] == 'Wood')
    assert wood_req['required'] == 5
    assert wood_req['have'] == Decimal('50')
    assert wood_req['percentage'] == 100

    coins_req = next(item for item in progress['resources'] if item['name'] == 'Coins')
    assert coins_req['required'] == 0.25
    
    # O código atribui '0' como padrão, então verificamos isso.
    # Esta asserção agora está correta.
    assert coins_req['have'] == Decimal('0')
    assert coins_req['percentage'] == 0