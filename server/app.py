from flask import Flask, jsonify
from database import initialize_db
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure the app
app.config['MONGODB_SETTINGS'] = {
    'host': Config.MONGODB_URI,
    'db': 'post2product'
}
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['DEBUG'] = Config.DEBUG

# Initialize JWT
jwt = JWTManager(app)

# Initialize the database
initialize_db(app)

# Import routes after app initialization
from routes.auth import auth_bp
from routes.instagram import instagram_bp
from routes.amazon import amazon_bp
from routes.analytics import analytics_bp
from routes.shopify import shopify_bp
from insta_connect.routes.instagram_auth import instagram_auth
from insta_connect.routes.media import media_bp
from routes.chatbot import chatbot_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(instagram_bp, url_prefix='/api/instagram')
app.register_blueprint(amazon_bp, url_prefix='/api/amazon')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(shopify_bp, url_prefix='/api/shopify')
app.register_blueprint(instagram_auth, url_prefix='/api/insta-connect/instagram')
app.register_blueprint(media_bp, url_prefix='/api/insta-connect/media')
app.register_blueprint(chatbot_bp)

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Post2ProductAI API is running"
    })

if __name__ == '__main__':
    # Validate configuration before starting
    Config.validate()
    app.run(debug=Config.DEBUG) 

# from database.db import initialize_db
# # from flask_pymongo import PyMongo
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()
# MONGO_URI = os.getenv("MONGO_URI")

# CORS(app) 
# app.config['MONGODB_SETTINGS'] = {
#     'host': MONGO_URI  # Change "your_db_name" to your actual DB name
# }
# app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  # Change this to something strong in production
# # print("DEBUG MONGO_URI:", MONGO_URI)
# # Initialize the database with the Flask app
# initialize_db(app)  
# # Configure MongoDB
# # try:
# #     app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
    
# #     mongo = PyMongo(app)
# #     # Test the connection
# #     mongo.db.command('ping')
# #     print("MongoDB connected successfully!")
# # except Exception as e:
# #     print(f"MongoDB connection error: {e}")
# #     mongo = None
# # print(mongo.db)
# # print(mongo.db.users.find_one()) 
#     # if mongo is None:
#     #     return jsonify({"status": "error", "message": "MongoDB is not connected"}), 500
#     return jsonify({"status": "healthy", "message": "Post2ProductAI API is running"})
#     # if mongo is None:
#     #     print("Warning: Application starting without MongoDB connection!")
#     app.run(debug=True) 