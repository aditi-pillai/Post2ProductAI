#!/usr/bin/env python3
"""
Setup script for Post2Product AI Flask backend
This script will handle all the setup and dependency installation
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Database Configuration
MONGODB_URI=mongodb://localhost:27017/post2product
JWT_SECRET=your_jwt_secret_key_here_change_this_in_production

# Development
DEBUG=true

# Optional: n8n Webhook Configuration
# N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/instagram-to-shopify
# WEBHOOK_SECRET=your_webhook_secret_key_here

# Optional: Shopify Configuration
# SHOPIFY_SHOP_DOMAIN=your-store
# SHOPIFY_ACCESS_TOKEN=your_shopify_access_token_here

# Optional: Image Processing (Cloudinary)
# CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
# CLOUDINARY_API_KEY=your_cloudinary_api_key
# CLOUDINARY_API_SECRET=your_cloudinary_api_secret

# Optional: AI Configuration
# GEMINI_API_KEY=your_gemini_api_key_here
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Post2Product AI Backend Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found. Please run this script from the server directory.")
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = ".\\venv\\Scripts\\activate"
        pip_cmd = ".\\venv\\Scripts\\pip"
        python_cmd = ".\\venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Upgrade pip
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check the error messages above.")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Test the installation
    print("🧪 Testing installation...")
    try:
        result = subprocess.run([python_cmd, "-c", "import flask, mongoengine; print('✅ All imports successful')"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Import test failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your actual configuration")
    print("2. Make sure MongoDB is running (local or Atlas)")
    print("3. Run: python app.py")
    print("\n💡 To start the app:")
    if os.name == 'nt':
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("   python app.py")
    print("\n🌐 The app will be available at: http://localhost:5000")

if __name__ == "__main__":
    main()

