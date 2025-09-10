# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

DEMO_KEY = os.getenv("COINGECKO_API_KEY_DEMO")
PRO_KEY = os.getenv("COINGECKO_API_KEY_PRO")
SINGLE_KEY = os.getenv("COINGECKO_API_KEY")

if PRO_KEY:
    ROOT_URL = "https://pro-api.coingecko.com/api/v3"
    API_KEY_HEADER = {"x-cg-pro-api-key": PRO_KEY}
elif DEMO_KEY:
    ROOT_URL = "https://api.coingecko.com/api/v3"
    API_KEY_HEADER = {"x-cg-demo-api-key": DEMO_KEY}
elif SINGLE_KEY:
    # If only one key provided, use public base URL but set pro header (you can change to pro URL if you have pro)
    ROOT_URL = "https://api.coingecko.com/api/v3"
    API_KEY_HEADER = {"x-cg-pro-api-key": SINGLE_KEY}
else:
    ROOT_URL = "https://api.coingecko.com/api/v3"
    API_KEY_HEADER = {}
