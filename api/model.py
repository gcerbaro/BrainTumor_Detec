import os
from constants import MODEL_NAME
import keras
import gdown
from utils import log_info, log_success

MODEL_REMOTE_URL = os.getenv('MODEL_REMOTE_URL')
MODEL_CACHE_FOLDER = os.path.join(os.getcwd(), '.cache')
MODEL_LOCAL_PATH = os.path.join(MODEL_CACHE_FOLDER, f"{MODEL_NAME}.keras")

os.makedirs(MODEL_CACHE_FOLDER, exist_ok=True)

def download_model():
  if MODEL_REMOTE_URL is None:
    raise ValueError('Faltando variável de ambiente MODEL_REMOTE_URL')
  
  log_info("Fazendo download do modelo...")
  log_info(f"  - {MODEL_REMOTE_URL}")
  gdown.download(url=MODEL_REMOTE_URL, output=MODEL_LOCAL_PATH, fuzzy=True)
  log_success("Download concluído com sucesso!")

def load_model() -> keras.Model:
  if not os.path.exists(MODEL_LOCAL_PATH):
    download_model()
  
  log_info("Carregando modelo em cache...")
  log_info(f"  - {MODEL_LOCAL_PATH}")
  model = keras.models.load_model(MODEL_LOCAL_PATH)
  if not isinstance(model, keras.Model):
    raise TypeError(f"Tipo inválido de modelo: {type(model)}")
  return model
