# config.py - Centralized configuration management
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration class following DRY principles"""
    
    # eBay API credentials
    CLIENT_ID = os.getenv("EBAY_CLIENT_ID", "your_client_id_here")
    CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET", "your_client_secret_here")
    APP_ID = os.getenv("EBAY_APP_ID", "your_app_id_here")
    DEV_ID = os.getenv("EBAY_DEV_ID", "your_dev_id_here")
    
    # Database configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "ebay_scanner")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    
    # Application settings
    MARKETPLACE_ID = "EBAY_US"
    UNDERVALUE_RATIO = 0.6  # Notify if current price < 60% of average sold price
    CHECK_INTERVAL = 600  # Polling interval in seconds
    
    @property
    def database_uri(self):
        """Get formatted database URI"""
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @classmethod
    def get_ebay_credentials(cls):
        """Get eBay API credentials as dictionary"""
        return {
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'app_id': cls.APP_ID,
            'dev_id': cls.DEV_ID
        }

# Create global config instance
config = Config()

# Backward compatibility - expose as module-level variables
CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
APP_ID = config.APP_ID
DEV_ID = config.DEV_ID
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_NAME = config.DB_NAME
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
MARKETPLACE_ID = config.MARKETPLACE_ID
UNDERVALUE_RATIO = config.UNDERVALUE_RATIO
CHECK_INTERVAL = config.CHECK_INTERVAL
