# app/services/exchange_service.py
import logging
from decimal import Decimal, InvalidOperation

from .. import sunflower_api

log = logging.getLogger(__name__)

def get_exchange_rates():
    """
    Processa as taxas de câmbio obtidas pelo cliente de API.

    Esta função consome os dados da API, calcula o melhor custo-benefício para Coins e Gems,
    retornando uma estrutura de dados simplificada para uso no aplicativo.

    Returns:
        dict: Um dicionário com as taxas processadas. Ex:
              {
                  'sfl': {'usd': 0.09, 'brl': 0.52},
                  'coin': {'sfl': 0.00625},
                  'gem': {'sfl': 0.067}
              }
        Retorna um dicionário vazio em caso de erro.
    """
    log.info("Processando taxas de câmbio...")
    data, error = sunflower_api.get_exchange_data()

    if error or not data:
        log.error(f"Não foi possível obter dados de cotação do API client: {error}")
        return {}

    try:
        processed_rates = {'sfl': {}, 'coin': {}, 'gem': {}}

        # 1. Processar cotações diretas do SFL
        if 'sfl' in data and data['sfl']:
            # Converte para Decimal para precisão e depois para float para serialização JSON
            processed_rates['sfl']['usd'] = float(Decimal(str(data['sfl'].get('usd', 0))))
            processed_rates['sfl']['brl'] = float(Decimal(str(data['sfl'].get('brl', 0))))

        # 2. Calcular melhor cotação para Coins (SFL por Coin)
        if 'coins' in data and data['coins']:
            rates = []
            for pkg in data['coins'].values():
                try:
                    coin_val = Decimal(str(pkg.get('coin', 0)))
                    sfl_val = Decimal(str(pkg.get('sfl', 0)))
                    if coin_val > 0:
                        rates.append(sfl_val / coin_val)
                except (InvalidOperation, TypeError):
                    log.warning(f"Valor inválido para coin/sfl no pacote: {pkg}")
                    continue
            if rates:
                # Converte o resultado final para float
                processed_rates['coin']['sfl'] = float(min(rates))

        # 3. Calcular melhor cotação para Gems (SFL por Gem)
        if 'gems' in data and data['gems']:
            rates = []
            for pkg in data['gems'].values():
                try:
                    sfl1_val = Decimal(str(pkg.get('sfl1', 0)))
                    if sfl1_val > 0:
                        rates.append(sfl1_val)
                except (InvalidOperation, TypeError):
                    log.warning(f"Valor inválido para sfl1 no pacote: {pkg}")
                    continue
            if rates:
                # Converte o resultado final para float
                processed_rates['gem']['sfl'] = float(min(rates))

        log.info(f"Taxas de câmbio processadas com sucesso: {processed_rates}")
        return processed_rates

    except (KeyError, ValueError, ZeroDivisionError, InvalidOperation) as e:
        log.error(f"Erro ao processar dados da API de câmbio: {e}", exc_info=True)

    return {}
