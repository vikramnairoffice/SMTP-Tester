"""
App password authentication module for Gmail IMAP.
Maximum 150 LoC as per architecture requirements.
"""

import imaplib
import logging
from typing import Optional, Tuple
from ..models.credential_model import CredentialModel
from ..models.result_model import ResultModel, AuthStatus


class AppPasswordAuthenticator:
    """
    Handles Gmail authentication using app passwords.
    
    Provides methods to authenticate and establish IMAP connections
    using Gmail app passwords.
    """
    
    def __init__(self, imap_server: str = "imap.gmail.com", port: int = 993):
        """
        Initialize app password authenticator.
        
        Args:
            imap_server: IMAP server hostname
            port: IMAP server port
        """
        self.imap_server = imap_server
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def authenticate(self, credential: CredentialModel) -> Tuple[bool, Optional[imaplib.IMAP4_SSL], str]:
        """
        Authenticate using app password.
        
        Args:
            credential: CredentialModel with app password data
            
        Returns:
            Tuple of (success, imap_connection, error_message)
        """
        if not credential.is_app_password():
            return False, None, "Invalid credential type for app password authentication"
        
        try:
            # Create IMAP SSL connection
            imap_conn = imaplib.IMAP4_SSL(self.imap_server, self.port)
            
            # Authenticate with email and app password
            imap_conn.login(credential.email, credential.auth_data)
            
            self.logger.info(f"Successfully authenticated {credential.email}")
            return True, imap_conn, ""
            
        except imaplib.IMAP4.error as e:
            error_msg = str(e)
            if "Invalid credentials" in error_msg:
                error_msg = "Invalid credentials. Check email and app password."
            elif "authentication failed" in error_msg.lower():
                error_msg = "Authentication failed. Verify app password."
            else:
                error_msg = f"IMAP authentication error: {error_msg}"
            
            self.logger.error(f"Authentication failed for {credential.email}: {error_msg}")
            return False, None, error_msg
            
        except Exception as e:
            error_msg = f"Connection error: {str(e)}"
            self.logger.error(f"Connection error for {credential.email}: {error_msg}")
            return False, None, error_msg
    
    def test_connection(self, credential: CredentialModel) -> bool:
        """
        Test connection without keeping it open.
        
        Args:
            credential: CredentialModel with app password data
            
        Returns:
            True if connection successful, False otherwise
        """
        success, imap_conn, _ = self.authenticate(credential)
        
        if success and imap_conn:
            try:
                imap_conn.logout()
            except Exception:
                pass  # Ignore logout errors
            return True
        
        return False
    
    def validate_app_password_format(self, password: str) -> bool:
        """
        Validate app password format.
        
        Args:
            password: App password string
            
        Returns:
            True if format appears valid, False otherwise
        """
        # Basic validation: app passwords are typically 16 characters
        # and contain only letters and numbers
        if not password:
            return False
        
        # Remove spaces and check length
        cleaned_password = password.replace(' ', '')
        
        # App passwords are usually 16 characters long
        if len(cleaned_password) != 16:
            return False
        
        # Should contain only alphanumeric characters
        if not cleaned_password.isalnum():
            return False
        
        return True
    
    def get_connection_info(self) -> dict:
        """
        Get connection information.
        
        Returns:
            Dictionary with connection details
        """
        return {
            'server': self.imap_server,
            'port': self.port,
            'encryption': 'SSL',
            'auth_method': 'LOGIN'
        }