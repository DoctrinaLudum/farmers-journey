import logging
import requests
from requests.exceptions import JSONDecodeError
from .cache import cache 

log = logging.getLogger(__name__)

SFL_API_BASE_URL = "https://api.sunflower-land.com/community/farms/"
SFL_WORLD_API_URL = "https://sfl.world/api/v1.1/" 
SFL_PRICE_URL = "https://sfl.world/api/v1/prices"

# ---> FUNÇÃO AUXILIAR DADOS LAND ---
@cache.cached(make_cache_key=lambda farm_id, endpoint: f"sfl_world_{farm_id}_{endpoint}")
def get_sfl_world_data(farm_id: int, endpoint: str):
    """
    Busca dados de um endpoint específico da API sfl.world.
    O resultado desta função será guardado em cache.
    """
    try:
        full_api_url = f"{SFL_WORLD_API_URL}{endpoint}/{farm_id}"
        log.info(f"Buscando dados na API sfl.world: {full_api_url}")
        
        response = requests.get(full_api_url, timeout=10)
        response.raise_for_status()
        
        try:
            data = response.json()
        except JSONDecodeError:
            log.warning("A resposta da API sfl.world para '%s' (farm %s) não é um JSON válido.", endpoint, farm_id)
            return {}, f"Resposta inválida da API sfl.world para o endpoint '{endpoint}'."

        if endpoint == 'land' and (not data or 'land' not in data or 'bumpkin' not in data):
            log.warning("Resposta da API sfl.world para '%s' (farm %s) não continha 'land' e 'bumpkin'.", endpoint, farm_id)
            return {}, f"Dados de expansão e bumpkin ('{endpoint}') incompletos recebidos de sfl.world."

        return data, None
        
    except requests.exceptions.HTTPError as http_err:
        log.error("Erro HTTP ao buscar dados de sfl.world para '%s' (farm %s). Status: %s", endpoint, farm_id, http_err.response.status_code, exc_info=True)
        return {}, f"Erro na API sfl.world (Status {http_err.response.status_code}). A fazenda pode não ter dados de expansão."
    except Exception:
        log.error("Erro inesperado ao buscar dados do endpoint '%s' (farm %s).", endpoint, farm_id, exc_info=True)
        return {}, f"Não foi possível buscar os dados de '{endpoint}' em sfl.world."

# ---> FUNÇÃO AUXILIAR PREÇOS ---
@cache.cached(key_prefix='prices')
def get_prices_data():
    """
    Busca os preços de todos os itens da API sfl.world.
    """
    try:
        log.info(f"Buscando dados de preços na API: {SFL_PRICE_URL}")
        response = requests.get(SFL_PRICE_URL, timeout=10)
        response.raise_for_status()
        try:
            data = response.json()
            return data, None
        except JSONDecodeError:
            log.error("Erro ao decodificar JSON da API de preços.", exc_info=True)
            return None, "Não foi possível ler os dados de preços da API (resposta inválida)."
    except requests.exceptions.HTTPError as http_err:
        log.error("Erro HTTP ao buscar dados de preços. Status: %s", http_err.response.status_code, exc_info=True)
        return None, f"Erro na API de preços (Status {http_err.response.status_code})."
    except Exception:
        log.error("Erro inesperado ao buscar dados de preços.", exc_info=True)
        return None, "Um erro inesperado ocorreu ao buscar os dados de preços."
# ---> FIM FUNÇÃO AUXILIAR PREÇOS ---


# ---> FUNÇÃO PRINCIPAL  ---
@cache.cached(make_cache_key=lambda farm_id: f"farm_data_{farm_id}")
def get_farm_data(farm_id: int):
    """
    Busca os dados das duas APIs e os retorna como dicionários separados.
    Esta abordagem evita a "fusão" de dados, prevenindo conflitos e perda de informação.
    
    Retorna:
        - main_data (dict): Dados da API principal (api.sunflower-land.com).
        - secondary_data (dict): Dados da API secundária (sfl.world).
        - error_message (str | None): Uma mensagem de erro, se ocorrer.
    """
    if not isinstance(farm_id, int) or farm_id <= 0:
        return None, None, "Farm ID deve ser um número inteiro positivo."

    main_data = None
    secondary_data = None
    
    try:
        # Etapa 1: Buscar dados da API principal (nossa 'farm_data_main')
        # Esta fonte é a mais completa e contém as 'milestones'.
        sfl_api_url = f"{SFL_API_BASE_URL}{farm_id}"
        log.info(f"Buscando dados principais: {sfl_api_url}")
        response = requests.get(sfl_api_url, timeout=10)
        response.raise_for_status()
        main_data = response.json().get('farm')

        if not main_data:
            return None, None, "Não foi possível obter os dados da fazenda da API principal."

        # Etapa 2: Buscar dados da API secundária (nossa 'farm_data_slave')
        # Esta fonte contém 'level', 'experience' e dados de expansão detalhados.
        secondary_data, world_api_error = get_sfl_world_data(farm_id, 'land')

        if world_api_error:
            log.warning("A API secundária (sfl.world) falhou para a fazenda %s: %s.", farm_id, world_api_error)
            # Mesmo com a falha, retornamos os dados principais para não quebrar a aplicação.
            # Retornamos um dicionário vazio para os dados secundários.
            return main_data, {}, None

        # Etapa 3: Retornar os dois dicionários, separados e puros.
        log.info(f"Dados das duas APIs recebidos com sucesso para a fazenda: {farm_id}")
        return main_data, secondary_data, None

    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code if http_err.response else "N/A"
        error_msg = f"Erro na API do Sunflower Land (Status {status_code}). A fazenda pode não existir."
        log.warning(f"Erro HTTP na API principal para a fazenda {farm_id}. Status: {status_code}")
        return None, None, error_msg
    except Exception as e:
        log.error(f"Erro genérico em get_farm_data para a fazenda {farm_id}: {e}", exc_info=True)
        return None, None, "Um erro inesperado ocorreu ao buscar os dados das APIs."
# ---> FIM FUNÇÃO PRINCIPAL ---