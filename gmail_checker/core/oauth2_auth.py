"""
OAuth2 authentication module for Gmail IMAP with Google Colab support.
Maximum 150 LoC as per architecture requirements.
"""

import base64
import imaplib
import logging
from typing import Optional, Tuple
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from ..models.credential_model import CredentialModel


class OAuth2Authenticator:
    """
    Handles Gmail OAuth2 authentication using InstalledAppFlow.
    
    Optimized for Google Colab environment with automatic user interaction.
    """
    
    SCOPES = ['https://mail.google.com/']
    IMAP_SERVER = "imap.gmail.com"
    PORT = 993
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def authenticate(self, credential: CredentialModel) -> Tuple[bool, Optional[Credentials], str]:
        """
        Perform OAuth2 authentication flow.
        
        Args:
            credential: CredentialModel with OAuth2 client secret data
            
        Returns:
            Tuple of (success, credentials, error_message)
        """
        if not credential.is_oauth2():
            return False, None, "Invalid credential type for OAuth2 authentication"
        
        try:
            # Create OAuth2 flow from client secret
            flow = InstalledAppFlow.from_client_config(
                credential.auth_data, 
                self.SCOPES
            )
            
            # Run local server for Colab-compatible authentication
            # This will open a browser window for user authentication
            creds = flow.run_local_server(
                port=0,
                access_type='offline',
                prompt='consent'
            )
            
            # Get user email from credentials
            user_email = self._get_user_email(creds)
            credential.set_authenticated(user_email)
            
            self.logger.info(f"Successfully authenticated OAuth2 for {user_email}")
            return True, creds, ""
            
        except Exception as e:
            error_msg = f"OAuth2 authentication failed: {str(e)}"
            self.logger.error(error_msg)
            return False, None, error_msg
    
    def _get_user_email(self, credentials: Credentials) -> str:
        """
        Extract user email from OAuth2 credentials using People API.
        
        Args:
            credentials: OAuth2 credentials
            
        Returns:
            User email address
        """
        try:
            service = build('people', 'v1', credentials=credentials)
            profile = service.people().get(
                resourceName='people/me',
                personFields='emailAddresses'
            ).execute()
            
            email_addresses = profile.get('emailAddresses', [])
            if email_addresses:
                return email_addresses[0]['value']
            
            return "unknown@gmail.com"
            
        except Exception as e:
            self.logger.error(f"Failed to get user email: {e}")
            return "unknown@gmail.com"
    
    def create_imap_connection(self, email: str, credentials: Credentials) -> Tuple[bool, Optional[imaplib.IMAP4_SSL], str]:
        """
        Create IMAP connection using OAuth2 credentials.
        
        Args:
            email: User email address
            credentials: OAuth2 credentials
            
        Returns:
            Tuple of (success, imap_connection, error_message)
        """
        try:
            # Refresh credentials if needed
            if credentials.expired:
                credentials.refresh(Request())
            
            # Create XOAUTH2 authentication string
            auth_string = f'user={email}\1auth=Bearer {credentials.token}\1\1'
            auth_string_b64 = base64.b64encode(auth_string.encode()).decode()
            
            # Create IMAP connection
            imap_conn = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.PORT)
            
            # Authenticate using XOAUTH2
            imap_conn.authenticate('XOAUTH2', lambda x: auth_string_b64)
            
            self.logger.info(f"Successfully created IMAP connection for {email}")
            return True, imap_conn, ""
            
        except Exception as e:
            error_msg = f"IMAP OAuth2 connection failed: {str(e)}"
            self.logger.error(error_msg)
            return False, None, error_msg
    
    def test_connection(self, credential: CredentialModel) -> bool:
        """
        Test OAuth2 authentication and IMAP connection.
        
        Args:
            credential: CredentialModel with OAuth2 data
            
        Returns:
            True if authentication and connection successful
        """
        success, creds, _ = self.authenticate(credential)
        
        if not success:
            return False
        
        imap_success, imap_conn, _ = self.create_imap_connection(credential.email, creds)
        
        if imap_success and imap_conn:
            try:
                imap_conn.logout()
            except Exception:
                pass  # Ignore logout errors
            return True
        
        return False
    
    def validate_client_secret(self, client_secret_data: dict) -> bool:
        """
        Validate OAuth2 client secret format.
        
        Args:
            client_secret_data: Client secret dictionary
            
        Returns:
            True if valid format, False otherwise
        """
        try:
            if 'installed' not in client_secret_data:
                return False
            
            installed = client_secret_data['installed']
            required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
            
            return all(field in installed for field in required_fields)
            
        except Exception:
            return False