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


# ---> FUNÇÃO PRINCIPAL (COM A CORREÇÃO) ---
@cache.cached(make_cache_key=lambda farm_id: f"farm_data_{farm_id}")
def get_farm_data(farm_id: int):
    """
    Busca todos os dados da fazenda, consolidando a SFL API e a sfl.world API.
    """
    if not isinstance(farm_id, int) or farm_id <= 0:
        return None, "Farm ID deve ser um número inteiro positivo."

    try:
        # 1. Busca os dados principais (que contêm as 'milestones')
        sfl_api_url = f"{SFL_API_BASE_URL}{farm_id}"
        log.info(f"Buscando dados na URL (API SFL): {sfl_api_url}")
        response = requests.get(sfl_api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        farm_data = data.get('farm')

        if farm_data:
            # 2. Busca dados secundários
            sfl_world_data, world_api_error = get_sfl_world_data(farm_id, 'land')
            if world_api_error:
                log.warning("Erro na API secundária não impediu o retorno dos dados principais para a fazenda %s", farm_id)
            else:
                # 3. Adiciona dados de expansão e COMBINA os dados do bumpkin
                farm_data['expansion_data'] = sfl_world_data
                if sfl_world_data and 'bumpkin' in sfl_world_data:
                    # Garante que farm_data['bumpkin'] existe antes de o atualizar
                    if 'bumpkin' not in farm_data:
                        farm_data['bumpkin'] = {}
                    # A CORREÇÃO CRÍTICA: .update() combina os dicionários, preservando as 'milestones'
                    farm_data['bumpkin'].update(sfl_world_data['bumpkin'])
        
        if farm_data:
            log.info(f"Dados consolidados recebidos com sucesso para a fazenda: {farm_id}")
            return farm_data, None
        
        return None, "Não foi possível obter os dados da fazenda."

    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code if http_err.response else "N/A"
        log.warning("Erro HTTP na API principal para a fazenda %s. Status: %s", farm_id, status_code)
        return None, f"Erro na API do Sunflower Land (Status {status_code}). A fazenda existe?"
    except requests.exceptions.RequestException:
        log.error("Erro de conexão na API principal para a fazenda %s.", farm_id, exc_info=True)
        return None, "Erro de conexão. Verifique sua internet."
    except JSONDecodeError:
        log.error("Erro ao decodificar JSON da API principal para a fazenda %s.", farm_id, exc_info=True)
        return None, "Não foi possível ler os dados da fazenda (resposta inválida da API principal)."
    except Exception:
        log.error("Erro genérico em get_farm_data para a fazenda %s.", farm_id, exc_info=True)
        return None, "Um erro inesperado ocorreu ao buscar os dados da fazenda."
# ---> FIM FUNÇÃO PRINCIPAL ---