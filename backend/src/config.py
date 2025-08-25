# Configuration file for eBay Scanner
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# eBay API credentials
CLIENT_ID = os.getenv("EBAY_CLIENT_ID", "your_client_id_here")  # Replace with your actual Client ID
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET", "your_client_secret_here")  # Replace with your actual Client Secret
APP_ID = os.getenv("EBAY_APP_ID", "your_app_id_here")  # Replace with your actual App ID for legacy Finding API
DEV_ID = os.getenv("EBAY_DEV_ID", "your_dev_id_here")  # Replace with your actual Dev ID

# Other configurations
MARKETPLACE_ID = "EBAY_US"  # Default marketplace
UNDERVALUE_RATIO = 0.6  # Notify if current price < 60% of average sold price
CHECK_INTERVAL = 600  # Polling interval in seconds
