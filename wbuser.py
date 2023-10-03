# wbuser.py
from websocket import create_connection

from wbpositions import CryptoComUser
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# Initialize the class
user = CryptoComUser(api_key, api_secret)

user.subscribe(['balance', 'user.position_balance', 'user.positions', 'user.account_risk'])