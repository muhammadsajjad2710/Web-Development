#!/usr/bin/env python3
"""
Setup script for Awan Rent A Car project
This script helps set up the Django backend and React frontend
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
        print(f"✓ Python found: {result.stdout.strip()}")
        return True
    except Exception:
        print("✗ Python not found. Please install Python 3.8+")
        return False

def check_node():
    """Check if Node.js is available"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"✓ Node.js found: {result.stdout.strip()}")
        return True
    except Exception:
        print("✗ Node.js not found. Please install Node.js 16+")
        return False

def check_npm():
    """Check if npm is available"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        print(f"✓ npm found: {result.stdout.strip()}")
        return True
    except Exception:
        print("✗ npm not found. Please install npm")
        return False

def setup_backend():
    """Set up the Django backend"""
    print("\n🔧 Setting up Django backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("✗ Backend directory not found")
        return False
    
    # Create virtual environment
    print("Creating virtual environment...")
    success, output = run_command("python -m venv venv", cwd=backend_dir)
    if not success:
        print(f"✗ Failed to create virtual environment: {output}")
        return False
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    print("Installing Python dependencies...")
    success, output = run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir)
    if not success:
        print(f"✗ Failed to install dependencies: {output}")
        return False
    
    print("✓ Backend setup completed successfully!")
    return True

def setup_frontend():
    """Set up the React frontend"""
    print("\n🔧 Setting up React frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("✗ Frontend directory not found")
        return False
    
    print("Installing Node.js dependencies...")
    success, output = run_command("npm install", cwd=frontend_dir)
    if not success:
        print(f"✗ Failed to install dependencies: {output}")
        return False
    
    print("✓ Frontend setup completed successfully!")
    return True

def main():
    """Main setup function"""
    print("🚗 Awan Rent A Car - Project Setup")
    print("=" * 50)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    if not check_python():
        return
    if not check_node():
        return
    if not check_npm():
        return
    
    print("\n✅ All prerequisites are satisfied!")
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed!")
        return
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed!")
        return
    
    print("\n🎉 Project setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Start XAMPP and create database 'awan_rental_db'")
    print("2. Navigate to backend directory: cd backend")
    print("3. Activate virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("4. Run migrations: python manage.py migrate")
    print("5. Populate sample data: python manage.py populate_data")
    print("6. Create superuser: python manage.py createsuperuser")
    print("7. Start Django server: python manage.py runserver")
    print("8. In another terminal, navigate to frontend directory: cd frontend")
    print("9. Start React app: npm start")
    print("\n🌐 Access the application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   Admin Panel: http://localhost:8000/admin")

if __name__ == "__main__":
    main()
