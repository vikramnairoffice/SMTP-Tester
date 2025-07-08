"""
Setup script for Gmail IMAP Credentials Checker.
Designed for Google Colab environment.
"""

import subprocess
import sys
import os


def install_requirements():
    """Install all required packages from requirements.txt."""
    print("📦 Installing requirements...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--quiet'
        ])
        print("✅ Requirements installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        print("Please install manually:")
        print("!pip install -r requirements.txt")
        return False


def check_environment():
    """Check if running in Google Colab environment."""
    try:
        import google.colab
        print("🔍 Detected Google Colab environment")
        return True
    except ImportError:
        print("🔍 Not running in Google Colab")
        return False


def main():
    """Main setup function."""
    print("🚀 Gmail IMAP Credentials Checker - Setup")
    print("=" * 50)
    
    # Check environment
    is_colab = check_environment()
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Environment-specific setup
    if is_colab:
        print("🛠️  Colab-specific setup complete")
        print("📋 OAuth2 authentication will use Colab's JavaScript bridge")
    else:
        print("🛠️  Local environment setup complete")
        print("⚠️  OAuth2 authentication may require manual code entry")
    
    print("\n✅ Setup complete!")
    print("🎯 Run 'python main.py' to start the application")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)