import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BRAWL_KEY")
DB_CONFIG = {
    "apiKey": os.getenv("DB_KEY"),
    "authDomain": "brawlclubtools.firebaseapp.com",
    "databaseURL": "https://brawlclubtools-default-rtdb.firebaseio.com",
    "projectId": "brawlclubtools",
    "storageBucket": "brawlclubtools.appspot.com",
    "messagingSenderId": "876424576126",
    "appId": "1:876424576126:web:1cc9546a112b4307b86c2f",
    "measurementId": "G-4M0SP5H43L",
}
