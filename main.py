"""
Main entry point for Gmail IMAP Credentials Checker.
Optimized for Google Colab environment.
"""

import sys
import logging
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gmail_checker.ui.gradio_interface import GradioInterface


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )


def install_dependencies():
    """Install required dependencies for Google Colab environment."""
    try:
        import subprocess
        import sys
        
        # Required packages
        packages = [
            'gradio==3.41.2',
            'google-auth',
            'google-auth-oauthlib', 
            'google-auth-httplib2',
            'google-api-python-client',
            'pandas',
            'tqdm'
        ]
        
        print("Installing required dependencies...")
        for package in packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet'])
        
        print("✅ Dependencies installed successfully!")
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        print("Please install manually using:")
        print("!pip install gradio google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pandas tqdm")


def main():
    """Main function to launch the application."""
    try:
        # Setup logging
        setup_logging()
        
        # Import debug logger after logging setup
        from gmail_checker.utils.debug_logger import debug_logger
        
        # Log system information
        debug_logger.log_system_info()
        debug_logger.log_module_versions()
        
        # Install dependencies (for Colab) - Skip if SKIP_INSTALL env var is set
        if os.getenv('SKIP_INSTALL') != '1':
            debug_logger.info("Installing dependencies...")
            install_dependencies()
        else:
            debug_logger.info("Skipping dependency installation (SKIP_INSTALL=1)")
        
        # Create and launch interface
        print("🚀 Starting Gmail IMAP Credentials Checker...")
        print("📋 Configured for Google Colab environment")
        print("🔐 Supports both App Password and OAuth2 authentication")
        
        debug_logger.info("Creating Gradio interface...")
        interface = GradioInterface()
        
        debug_logger.info("Launching Gradio interface...")
        interface.launch()
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        print("Please check the error details above and try again.")
        
        # Try to log error if debug logger is available
        try:
            from gmail_checker.utils.debug_logger import debug_logger
            debug_logger.error("Application startup failed", e)
            log_file = debug_logger.get_log_file_path()
            if log_file:
                print(f"📋 Debug log file: {log_file}")
        except:
            pass


if __name__ == "__main__":
    main()