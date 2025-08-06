import logging
import os
from datetime import datetime

from flask import Flask
from flask_caching import Cache

import config

from . import cache

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # Habilita a extensão 'do' no Jinja2 para permitir a modificação de variáveis dentro de loops.
    app.jinja_env.add_extension('jinja2.ext.do')
    
    # Importa e inicializa os módulos da aplicação
    from . import game_state
    cache.init_app(app) 

    # Roda a inicialização do estado do jogo uma única vez
    game_state.initialize_game_state()

    # Este processador de contexto injeta variáveis em todos os templates
    @app.context_processor
    def inject_global_vars():
        return {
            'app_version': app.config.get('APP_VERSION'),
            'current_year': datetime.now().year,
            'current_season_name': game_state.GAME_STATE.get('current_season_name'),
            'current_ticket_name': game_state.GAME_STATE.get('current_ticket_name'),
            'current_artefact_name': game_state.GAME_STATE.get('current_artefact_name'),
            'current_chapter_fish': game_state.GAME_STATE.get('current_chapter_fish'),
            'current_ticket_icon_path': game_state.GAME_STATE.get('current_ticket_icon_path'),
            'current_start_date_gain_ticket': game_state.GAME_STATE.get('current_start_date_gain_ticket'),
        }

    from . import routes
    app.register_blueprint(routes.bp)

    return app