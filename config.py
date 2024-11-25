import json
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def save_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

config = load_config()

NETWORK_FOLDER = config['NETWORK_FOLDER']
TOKEN = config['TOKEN']
SET_PATH = config['SET_PATH']
ALLOWED_USERS = config['ALLOWED_USERS']
ADMINS = config['ADMINS']
REQUESTS = config['REQUESTS']