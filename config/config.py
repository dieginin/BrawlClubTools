import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BRAWL_KEY")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
