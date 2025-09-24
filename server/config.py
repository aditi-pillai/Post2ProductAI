import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB settings
    MONGODB_URI = os.getenv('MONGODB_URI')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')
    
    # n8n Webhook settings
    N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'change_me_in_production')
    
    # Shopify settings
    SHOPIFY_SHOP_DOMAIN = os.getenv('SHOPIFY_SHOP_DOMAIN')
    SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
    
    # Image processing settings
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    
    # Other settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    @classmethod
    def validate(cls):
        """Validate that all required configuration is present"""
        if not cls.MONGODB_URI:
            raise ValueError("MONGODB_URI must be set in environment variables")
        if not cls.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set in environment variables") 