#!/usr/bin/env python3
"""
Deployment test script for Gmail IMAP Credentials Checker.
Tests all modules and functionality before deployment.
"""

import sys
import os
import traceback
sys.path.insert(0, '.')

def test_imports():
    """Test all module imports."""
    print("📦 Testing module imports...")
    
    try:
        from gmail_checker.models.credential_model import CredentialModel, AuthType
        from gmail_checker.models.result_model import ResultModel, AuthStatus
        from gmail_checker.utils.credential_parser import CredentialParser
        from gmail_checker.utils.file_handler import FileHandler
        from gmail_checker.utils.email_counter import EmailCounter
        from gmail_checker.core.auth_manager import AuthManager
        from gmail_checker.core.app_password_auth import AppPasswordAuthenticator
        from gmail_checker.core.oauth2_auth import OAuth2Authenticator
        from gmail_checker.core.imap_connector import IMAPConnector
        from gmail_checker.ui.ui_components import UIComponents
        from gmail_checker.ui.gradio_interface import GradioInterface
        print("✅ All module imports successful")
        return True
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        traceback.print_exc()
        return False

def test_functionality():
    """Test core functionality."""
    print("\n🔧 Testing core functionality...")
    
    try:
        # Test credential parsing
        from gmail_checker.utils.credential_parser import CredentialParser
        parser = CredentialParser()
        
        # App password parsing
        app_creds = parser.parse_app_password_text("test@gmail.com:testpass123")
        assert len(app_creds) == 1
        assert app_creds[0].email == "test@gmail.com"
        print("✅ App password parsing works")
        
        # OAuth2 parsing
        oauth2_data = {
            'installed': {
                'client_id': 'test-client-id',
                'client_secret': 'test-secret',
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token'
            }
        }
        oauth2_cred = parser.parse_oauth2_json(oauth2_data)
        assert oauth2_cred.get_display_id() == 'test-client-id'
        print("✅ OAuth2 parsing works")
        
        # Test result models
        from gmail_checker.models.result_model import ResultModel
        result = ResultModel.create_success("test@gmail.com", "app_password", 100, 50, 1.5)
        assert result.get_total_emails() == 150
        assert result.is_success()
        print("✅ Result models work")
        
        # Test file operations
        from gmail_checker.utils.file_handler import FileHandler
        file_handler = FileHandler()
        csv_row = result.to_csv_row()
        assert 'Email' in csv_row
        assert csv_row['Email'] == 'test@gmail.com'
        print("✅ File operations work")
        
        # Test UI components
        from gmail_checker.ui.ui_components import UIComponents
        ui = UIComponents()
        status_msg = ui.create_status_message("Test", "success")
        assert "SUCCESS" in status_msg
        print("✅ UI components work")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test full integration."""
    print("\n🔗 Testing integration...")
    
    try:
        from gmail_checker.ui.gradio_interface import GradioInterface
        interface = GradioInterface()
        
        # Test interface creation
        gradio_app = interface.create_interface()
        assert gradio_app is not None
        print("✅ Gradio interface creation works")
        
        # Test credential processing logic (without actual authentication)
        from gmail_checker.core.auth_manager import AuthManager
        auth_manager = AuthManager()
        supported_types = auth_manager.get_supported_auth_types()
        assert 'app_password' in supported_types
        assert 'oauth2' in supported_types
        print("✅ Auth manager works")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 Gmail IMAP Credentials Checker - Deployment Test")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Core Functionality", test_functionality),
        ("Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test PASSED")
        else:
            print(f"❌ {test_name} test FAILED")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for deployment.")
        print("\n🚀 To deploy:")
        print("1. Upload project to Google Colab")
        print("2. Run: !python setup.py")
        print("3. Run: !python main.py")
        print("4. Click the Gradio public link")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)