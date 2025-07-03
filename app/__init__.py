from flask import Flask
from datetime import datetime
from flask_caching import Cache
from . import cache
import config
import os



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