from flask_caching import Cache

# 1. Cria a instância do Cache, mas sem associá-la a uma aplicação ainda.
cache = Cache(config={
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "cache_dir",
    "CACHE_DEFAULT_TIMEOUT": 300  # Tempo padrão de 5 minutos (em segundos)
})

# 2. Cria uma função que será chamada para associar o cache à aplicação Flask.
def init_app(app):
    """
    Associa a instância do cache com a aplicação Flask.
    Isto é chamado a partir da factory da aplicação em __init__.py.
    """
    cache.init_app(app)
