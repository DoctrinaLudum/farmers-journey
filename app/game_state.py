# app/game_state.py
import logging
from datetime import datetime, timezone

# Importa o módulo de análise para usar a função de obtenção de imagem.
# É seguro, pois 'analysis.py' não importa 'game_state.py', evitando importações circulares.
from . import analysis
from .domain import seasons as seasons_domain

log = logging.getLogger(__name__)

# Variável global para armazenar o estado do jogo, como a temporada atual.
# Será preenchida na inicialização da aplicação.
# CORREÇÃO: Padronizando os nomes das chaves para clareza.
GAME_STATE = {
    "current_season_name": None,
    "current_season_data": None,
    "current_season_start_date": None,
    "current_season_end_date": None,
    "current_ticket_name": None,
    "current_artefact_name": None,
    "current_chapter_fish": None,
    "current_ticket_icon_path": None,
    "current_start_date_gain_ticket": None, # Adiciona o novo campo para a data
}

def _populate_game_state(season_name: str, season_data: dict):
    """
    Função auxiliar para preencher o dicionário GAME_STATE com os dados da temporada.
    Evita a duplicação de código entre a lógica de temporada ativa e a de fallback.
    """
    GAME_STATE["current_season_name"] = season_name
    GAME_STATE["current_season_data"] = season_data
    GAME_STATE["current_season_start_date"] = datetime.fromisoformat(season_data["start_date"].replace("Z", "+00:00"))
    GAME_STATE["current_season_end_date"] = datetime.fromisoformat(season_data["end_date"].replace("Z", "+00:00"))
    
    # Extrai e armazena os detalhes específicos da temporada para acesso rápido
    ticket_name = season_data.get("ticket_name")
    GAME_STATE["current_ticket_name"] = ticket_name
    GAME_STATE["current_artefact_name"] = season_data.get("artefact_name")
    GAME_STATE["current_chapter_fish"] = season_data.get("chapter_fish")
    GAME_STATE["current_ticket_icon_path"] = analysis.get_item_image_path(ticket_name) if ticket_name else None

    # Extrai e processa a data de início para ganhar o ticket
    gain_ticket_date_str = season_data.get("start_date_gain_ticket")
    if gain_ticket_date_str:
        GAME_STATE["current_start_date_gain_ticket"] = datetime.fromisoformat(gain_ticket_date_str.replace("Z", "+00:00"))
    else:
        GAME_STATE["current_start_date_gain_ticket"] = None # Garante que o valor é nulo se não existir
    log.info(f"Estado do jogo populado com os dados da temporada: '{season_name}'")

def initialize_game_state():
    """
    Calcula a temporada atual com base nas datas e a armazena no estado global.
    Esta função deve ser chamada uma única vez na inicialização da aplicação.
    """
    log.info("Inicializando o estado global do jogo...")
    now = datetime.now(timezone.utc)
    
    found_season = False
    for season_name, season_data in seasons_domain.SEASONS_DATA.items():
        try:
            start_date = datetime.fromisoformat(season_data["start_date"].replace("Z", "+00:00"))
            end_date = datetime.fromisoformat(season_data["end_date"].replace("Z", "+00:00"))

            if start_date <= now < end_date:
                _populate_game_state(season_name, season_data)
                found_season = True
                break
        except (ValueError, KeyError) as e:
            log.error(f"Erro ao processar a temporada '{season_name}': {e}")
            continue

    if not found_season:
        log.warning("Nenhuma temporada ativa encontrada. Verifique as configurações em 'seasons.py'.")
        # Define um fallback para a temporada mais recente, se nenhuma estiver ativa
        latest_season_item = max(seasons_domain.SEASONS_DATA.items(), key=lambda item: item[1]['start_date'])
        season_name, season_data = latest_season_item        
        _populate_game_state(season_name, season_data)
        log.info(f"Usando a temporada mais recente como fallback: '{season_name}'")