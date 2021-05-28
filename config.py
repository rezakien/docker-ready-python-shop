import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("MY_ID")
ID_E = os.getenv("ID_E")
HOST = os.getenv("HOST")

PRODUCTION = True if os.getenv("PRODUCTION") == '1' else False

PG_HOST = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_CONTAINER_PORT = os.getenv("PG_CONTAINER_PORT")
PG_HOST_PORT = os.getenv("PG_HOST_PORT")
DATABASE = os.getenv("DATABASE")

if PRODUCTION:
    POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_HOST_PORT}/{DATABASE}"
else:
    POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_HOST_PORT}/{DATABASE}"

I18N_DOMAIN = 'shop-bot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
