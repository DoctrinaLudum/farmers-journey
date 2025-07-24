import os
import logging
from datetime import datetime

from flask import Flask
from flask_caching import Cache

import config

from . import cache


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    cache.init_app(app)

    # Este processador de contexto injeta variáveis em todos os templates
    @app.context_processor
    def inject_global_vars():
        return {
            'app_version': app.config.get('APP_VERSION'),
            'current_year': datetime.now().year
        }

    from . import routes
    app.register_blueprint(routes.bp)

    return app