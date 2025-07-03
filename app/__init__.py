from flask import Flask
from datetime import datetime
from flask_caching import Cache
import config
import os

cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cache-directory')
# Configuração do cache
cache_config = {
    "CACHE_TYPE": "FileSystemCache",  # <<< MUDANÇA PRINCIPAL: Usar o sistema de ficheiros
    "CACHE_DIR": cache_dir,           # <<< O diretório onde os ficheiros de cache serão guardados
    "CACHE_DEFAULT_TIMEOUT": 180      # Tempo padrão de 3 minutos (pode ajustar)
}

# Criar a instância do cache
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    cache.init_app(app, config=cache_config)

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