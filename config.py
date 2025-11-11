import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

APP_VERSION = "0.1.0"
FORCE_EVENT = "sunshower" # Nome do evento. Deixe como None para desativar.

# Carrega a chave da API do Sunflower Land a partir de uma variável de ambiente.
SFL_API_KEY = os.getenv("SFL_API_KEY")

if not SFL_API_KEY:
    print("AVISO: A variável de ambiente SFL_API_KEY não está definida no arquivo .env. As chamadas para a API principal do SFL podem falhar.")
