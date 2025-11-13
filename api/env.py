from dotenv import load_dotenv
import os
from utils import log_info

# Carrega variáveis de ambiente do arquivo .env.default
dotenv_path = os.path.join(os.getcwd(), '.env.default')
log_info("Carregando variáveis de ambiente...")
log_info(f"  - {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path, verbose=True)