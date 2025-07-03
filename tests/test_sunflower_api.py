# tests/test_sunflower_api.py
from app import sunflower_api

MOCK_API_RESPONSE = {
    "farm": {
        "balance": "1234.56",
        "username": "Test Farmer1",
        "inventory": {"Wood": "100"}
    },
    "land": {
        "type": "basic",
        "level": 5
    },
    "bumpkin": {
        "level": 10
    }
}

# 1. Adicione 'app' como argumento aqui
def test_get_farm_data_success(mocker, app):
    """
    Testa a função get_farm_data num cenário de sucesso,
    simulando a resposta da API.
    """
    mock_response = mocker.Mock()
    mock_response.json.return_value = MOCK_API_RESPONSE
    mock_response.raise_for_status.return_value = None
    mocker.patch('app.sunflower_api.requests.get', return_value=mock_response)
    mocker.patch('app.sunflower_api.get_sfl_world_data', return_value=({}, None))

    # 2. Execute a função dentro do contexto da aplicação
    with app.app_context():
        farm_data, error = sunflower_api.get_farm_data(123)

    # Asserções
    assert error is None
    assert farm_data is not None
    assert farm_data['username'] == "Test Farmer"

# 3. Adicione 'app' como argumento aqui também
def test_get_farm_data_api_error(mocker, app):
    """
    Testa o que acontece se a API do Sunflower Land retornar um erro.
    """
    mocker.patch(
        'app.sunflower_api.requests.get',
        side_effect=sunflower_api.requests.exceptions.HTTPError("API Error")
    )

    # E execute dentro do contexto aqui também
    with app.app_context():
        farm_data, error = sunflower_api.get_farm_data(999999)

    # Asserções
    assert farm_data is None
    assert error is not None
    assert "Erro na API do Sunflower Land" in error