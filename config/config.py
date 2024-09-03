import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BRAWL_KEY")
DB_KEY = os.getenv("DB_KEY")
