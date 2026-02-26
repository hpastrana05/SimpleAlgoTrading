import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

IS_DEMO = True

#LINKS
DEMO_LINK = "https://demo.trading212.com/api/v0/"
LIVE_LINK = "https://live.trading212.com/api/v0/"

# API KEYS
if IS_DEMO:
    API_KEY=os.getenv("API_KEY_DEMO")
    API_SECRET=os.getenv("API_SECRET_DEMO")
    API_LINK = DEMO_LINK
else:
    API_KEY=os.getenv("API_KEY_LIVE")
    API_SECRET=os.getenv("API_SECRET_LIVE")
    API_LINK = LIVE_LINK


# S
PROJECT_ROOT = Path(__file__).parents[1]
DATA_PATH = PROJECT_ROOT / "data"
STRATEGIES_PATH = PROJECT_ROOT / "strategies"

