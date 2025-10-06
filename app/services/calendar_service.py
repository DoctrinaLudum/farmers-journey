# app/services/calendar_service.py
import logging
from datetime import datetime, timezone
from app.domain.calendar_events import CALENDAR_EVENTS
from app.domain.collectiblesItemBuffs import COLLECTIBLES_ITEM_BUFFS

log = logging.getLogger(__name__)

class CalendarService:
    """
    Serviço para gerenciar os eventos do calendário e seu impacto no jogo,
    baseado nos dados da fazenda recebidos da API.
    """

    def __init__(self, farm_data: dict):
        """
        Inicializa o CalendarService com os dados atuais da fazenda.

        Args:
            farm_data (dict): O objeto de dados da fazenda, geralmente a resposta
                              JSON da API do jogo. Espera-se que contenha as chaves
                              'season', 'calendar', e 'home'.
        """
        self.farm_data = farm_data
        self.calendar_events = CALENDAR_EVENTS
        self.guardians = {
            name: data for name, data in COLLECTIBLES_ITEM_BUFFS.items()
            if "Guardian" in name
        }

    def get_current_classic_season(self) -> str | None:
        """
        Obtém a estação clássica atual (Spring, Summer, etc.) dos dados da fazenda.

        Returns:
            str | None: O nome da estação com a primeira letra maiúscula, ou None se não for encontrado.
        """
        try:
            season = self.farm_data['season']['season']
            return season.capitalize()
        except (KeyError, TypeError):
            log.warning("Não foi possível encontrar a informação da estação em farm_data['season']['season']")
            return None

    def get_active_guardian(self) -> str | None:
        """
        Determina o guardião sazonal ativo com base na estação atual e nos
        colecionáveis colocados na fazenda (tanto na ilha quanto dentro de casa).

        Returns:
            str | None: O nome do guardião ativo, ou None se não estiver ativo.
        """
        season = self.get_current_classic_season()
        if not season:
            return None

        guardian_name = f"{season} Guardian"
        
        try:
            # Combina colecionáveis da ilha e de dentro de casa
            farm_collectibles = self.farm_data.get('collectibles', {})
            home_collectibles = self.farm_data.get('home', {}).get('collectibles', {})
            all_placed_collectibles = {**farm_collectibles, **home_collectibles}

            if guardian_name in all_placed_collectibles:
                log.info(f"Guardião ativo encontrado: {guardian_name}")
                return guardian_name
        except TypeError:
            log.warning("Erro ao processar listas de colecionáveis. Verifique se são dicionários.")

        return None

    def get_active_event(self) -> str | None:
        """
        Determina o evento de calendário ativo para o dia de hoje.

        Returns:
            str | None: O nome do evento ativo, ou None se nenhum evento estiver ativo hoje.
        """
        try:
            today_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            calendar_dates = self.farm_data.get('calendar', {}).get('dates', [])
            
            for event in calendar_dates:
                if event.get('date') == today_str:
                    event_name = event.get("name")
                    if event_name and event_name != "unknown":
                        log.info(f"Evento ativo para hoje ({today_str}): {event_name}")
                        return event_name
            
            log.info(f"Nenhum evento de calendário ativo para hoje ({today_str}).")
            return None
        except (KeyError, TypeError):
            log.error("Erro ao processar farm_data['calendar']['dates']")
            return None

    def get_seasonal_boosts(self) -> list:
        """
        Calcula e retorna os bônus combinados do evento de calendário ativo
        e do guardião sazonal ativo.

        A lógica de combinação é a seguinte:
        1. Prevenção: Se o guardião previne um evento negativo, nenhum bônus é retornado.
        2. Melhoria: Se o guardião melhora um evento positivo, seu bônus é adicionado
           à lista de bônus do evento base.

        Returns:
            list: Uma lista de objetos de bônus a serem aplicados.
        """
        active_guardian_name = self.get_active_guardian()
        active_event_name = self.get_active_event()

        if not active_event_name:
            return []

        event_data = self.calendar_events.get(active_event_name)
        if not event_data:
            log.warning(f"Evento '{active_event_name}' não encontrado no domínio de eventos.")
            return []

        # Faz uma cópia profunda para evitar modificar os dicionários originais
        final_boosts = [boost.copy() for boost in event_data.get("boosts", [])]
        for boost in final_boosts:
            boost['event_name'] = active_event_name

        if active_guardian_name:
            guardian_data = self.guardians.get(active_guardian_name)
            guardian_boosts = guardian_data.get("boosts", [])

            for guardian_boost in guardian_boosts:
                # Lógica de Prevenção
                if guardian_boost.get("type") == "PREVENT_EVENT" and guardian_boost.get("value") == active_event_name:
                    log.info(f"O guardião '{active_guardian_name}' preveniu o evento '{active_event_name}'.")
                    return [] # Retorna uma lista vazia, pois o evento foi prevenido

                # Lógica de Melhoria (Modificador)
                if guardian_boost.get("conditions", {}).get("calendar_event") == active_event_name:
                    log.info(f"O guardião '{active_guardian_name}' está melhorando o evento '{active_event_name}'.")
                    
                    # Encontra o bônus base correspondente no evento para modificar
                    for base_boost in final_boosts:
                        # Compara o tipo de bônus (ex: YIELD) e a operação (ex: add)
                        if base_boost.get("type") == guardian_boost.get("type") and base_boost.get("operation") == guardian_boost.get("operation"):
                            # 1. Soma o valor do bônus do guardião ao bônus base
                            base_boost["value"] += guardian_boost.get("value", 0)
                            
                            # 2. Adiciona o guardião como um modificador
                            if "modifiers" not in base_boost:
                                base_boost["modifiers"] = []
                            
                            base_boost["modifiers"].append({
                                "source_item": active_guardian_name,
                                "source_type": "collectible"
                            })

        return final_boosts
