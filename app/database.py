# app/database.py
import logging
from google.cloud import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP, FieldFilter
from google.auth.exceptions import DefaultCredentialsError

log = logging.getLogger(__name__)

SNAPSHOTS_COLLECTION = "farm_snapshots"
db = None

try:
    db = firestore.Client()
    log.info(f"Cliente Firestore inicializado com sucesso. Projeto: {db.project}")
except DefaultCredentialsError:
    log.error("Erro de credenciais. Configure o acesso ao Firestore.")
    log.info("Para desenvolvimento local, execute: gcloud auth application-default login")
except Exception as e:
    log.exception(f"Falha CRÍTICA ao inicializar cliente Firestore: {e}")

# (Funções save_farm_snapshot e get_latest_farm_snapshot permanecem as mesmas)
def save_farm_snapshot(farm_id: int, farm_data: dict):
    # ...
    pass

def get_latest_farm_snapshot(farm_id: int):
    # ...
    pass