from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar e registrar o Blueprint das rotas
    from . import routes
    app.register_blueprint(routes.bp)

    
    return app