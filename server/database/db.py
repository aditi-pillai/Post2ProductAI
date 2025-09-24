import os
from mongoengine import connect, disconnect
from config import Config

def initialize_db(app):
    """Initialize the database connection"""
    try:
        # Get MongoDB URI from Flask config or environment
        mongodb_uri = app.config.get('MONGODB_SETTINGS', {}).get('host') or Config.MONGODB_URI
        db_name = app.config.get('MONGODB_SETTINGS', {}).get('db', 'post2product')
        
        # Connect to MongoDB
        connect(db=db_name, host=mongodb_uri)
        print(f"✅ Connected to MongoDB: {db_name}")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def disconnect_db():
    """Disconnect from MongoDB"""
    try:
        disconnect()
        print("✅ Disconnected from MongoDB")
    except Exception as e:
        print(f"❌ MongoDB disconnect failed: {e}")