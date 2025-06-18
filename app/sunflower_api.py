import logging
import requests
import time

log = logging.getLogger(__name__)

SFL_API_BASE_URL = "https://api.sunflower-land.com/community/farms/"
SFL_WORLD_API_URL = "https://sfl.world/api/v1.1/"

api_cache = {}
CACHE_DURATION_SECONDS = 180

# ---> FUNÇÃO AUXILIAR DADOS LAND ---
def get_sfl_world_data(farm_id: int, endpoint: str):
    """
    Busca dados de um endpoint específico da API sfl.world.
    """
    cache_key = f"sfl_world_{endpoint}_{farm_id}"
    current_time = time.time()

    if cache_key in api_cache:
        cached_data, timestamp = api_cache[cache_key]
        if current_time - timestamp < CACHE_DURATION_SECONDS:
            log.info(f"Retornando dados para '{cache_key}' do cache.")
            return cached_data, None

    try:
        full_api_url = f"{SFL_WORLD_API_URL}{endpoint}/{farm_id}"
        log.info(f"Buscando dados na API sfl.world: {full_api_url}")
        
        response = requests.get(full_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        api_cache[cache_key] = (data, current_time)
        
        return data, None
    except Exception as e:
        log.error(f"Erro ao buscar dados do endpoint '{endpoint}' para a fazenda {farm_id}: {e}")
        return {}, f"Não foi possível buscar os dados de '{endpoint}' em sfl.world."
# ---> FIM FUNÇÃO AUXILIAR DADOS LAND ---


# ---> FUNÇÃO PRINCIPAL ---
def get_farm_data(farm_id: int):
    """
    Busca todos os dados da fazenda, consolidando a SFL API e a sfl.world API.
    """
    cache_key = f"sfl_api_{farm_id}"
    current_time = time.time()

    if cache_key in api_cache:
        cached_data, timestamp = api_cache[cache_key]
        if current_time - timestamp < CACHE_DURATION_SECONDS:
            log.info(f"Retornando dados para farm_id {farm_id} do cache principal.")
            return cached_data, None

    if not isinstance(farm_id, int) or farm_id <= 0:
        return None, "Farm ID deve ser um número inteiro positivo."

    try:
        # 1. Busca os dados principais da API do Sunflower Land
        sfl_api_url = f"{SFL_API_BASE_URL}{farm_id}"
        log.info(f"Buscando dados na URL (API SFL): {sfl_api_url}")
        response = requests.get(sfl_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        farm_data = data.get('farm')

        # 2. Busca os dados da expansão usando a função genérica auxiliar
        if farm_data:
            sfl_world_land_data, expansion_error = get_sfl_world_data(farm_id, 'land')
            if expansion_error:
                log.warning(expansion_error)
            
            # Adiciona os dados da expansão ao nosso objeto principal
            farm_data['expansion_data'] = sfl_world_land_data
        
        if farm_data:
            api_cache[cache_key] = (farm_data, current_time)
        
        log.info(f"Dados consolidados recebidos com sucesso para a fazenda: {farm_id}")
        return farm_data, None

    except requests.exceptions.HTTPError as http_err:
        return None, f"Erro na API do Sunflower Land (Status {response.status_code}). A fazenda existe?"
    except requests.exceptions.RequestException as req_err:
        return None, "Erro de conexão. Verifique sua internet."
    except Exception as e:
        return None, "Um erro inesperado ocorreu."
    
# ---> FIM FUNÇÃO PRINCIPAL ---
