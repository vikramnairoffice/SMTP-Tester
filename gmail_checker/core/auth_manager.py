"""
Authentication manager - abstraction layer for all auth types.
Maximum 150 LoC as per architecture requirements.
"""

import logging
import time
from typing import Optional, Tuple
from ..models.credential_model import CredentialModel
from ..models.result_model import ResultModel, AuthStatus
from .app_password_auth import AppPasswordAuthenticator
from .oauth2_auth import OAuth2Authenticator
from .imap_connector import IMAPConnector
from ..utils.debug_logger import debug_logger, log_function_call


class AuthManager:
    """
    Unified authentication manager for both app password and OAuth2.
    
    Provides single interface for all authentication types and manages
    the complete authentication -> connection -> email counting flow.
    """
    
    def __init__(self):
        """Initialize authentication manager with all authenticators."""
        self.app_password_auth = AppPasswordAuthenticator()
        self.oauth2_auth = OAuth2Authenticator()
        self.imap_connector = IMAPConnector()
        self.logger = logging.getLogger(__name__)
    
    @log_function_call
    def authenticate_and_count(self, credential: CredentialModel) -> ResultModel:
        """
        Complete authentication and email counting process.
        
        Args:
            credential: CredentialModel to authenticate
            
        Returns:
            ResultModel with authentication and counting results
        """
        start_time = time.time()
        
        debug_logger.info(f"Starting authentication for {credential.get_display_id()}", {
            'auth_type': credential.auth_type.value,
            'email': credential.email
        })
        
        try:
            # Route to appropriate authenticator
            if credential.is_app_password():
                return self._process_app_password(credential, start_time)
            elif credential.is_oauth2():
                return self._process_oauth2(credential, start_time)
            else:
                error_msg = "Unsupported authentication type"
                debug_logger.error(error_msg, context={'auth_type': credential.auth_type.value})
                return ResultModel.create_failure(
                    credential.email,
                    "unknown",
                    error_msg,
                    time.time() - start_time
                )
                
        except Exception as e:
            debug_logger.error("Authentication process failed", e, {
                'credential_id': credential.get_display_id(),
                'auth_type': credential.auth_type.value
            })
            return ResultModel.create_failure(
                credential.email,
                credential.auth_type.value,
                f"Authentication error: {str(e)}",
                time.time() - start_time
            )
    
    def _process_app_password(self, credential: CredentialModel, start_time: float) -> ResultModel:
        """
        Process app password authentication.
        
        Args:
            credential: App password credential
            start_time: Processing start time
            
        Returns:
            ResultModel with results
        """
        success, imap_conn, error_msg = self.app_password_auth.authenticate(credential)
        
        if not success:
            return ResultModel.create_failure(
                credential.email,
                "app_password",
                error_msg,
                time.time() - start_time
            )
        
        # Count emails
        counts = self.imap_connector.get_all_folder_counts(imap_conn)
        
        # Close connection
        self.imap_connector.close_connection(imap_conn)
        
        return ResultModel.create_success(
            credential.email,
            "app_password",
            counts.get('inbox', 0),
            counts.get('sent', 0),
            time.time() - start_time
        )
    
    def _process_oauth2(self, credential: CredentialModel, start_time: float) -> ResultModel:
        """
        Process OAuth2 authentication.
        
        Args:
            credential: OAuth2 credential
            start_time: Processing start time
            
        Returns:
            ResultModel with results
        """
        # Authenticate with OAuth2
        success, creds, error_msg = self.oauth2_auth.authenticate(credential)
        
        if not success:
            return ResultModel.create_failure(
                credential.email or "unknown",
                "oauth2",
                error_msg,
                time.time() - start_time
            )
        
        # Create IMAP connection
        imap_success, imap_conn, imap_error = self.oauth2_auth.create_imap_connection(
            credential.email, creds
        )
        
        if not imap_success:
            return ResultModel.create_failure(
                credential.email,
                "oauth2",
                imap_error,
                time.time() - start_time
            )
        
        # Count emails
        counts = self.imap_connector.get_all_folder_counts(imap_conn)
        
        # Close connection
        self.imap_connector.close_connection(imap_conn)
        
        return ResultModel.create_success(
            credential.email,
            "oauth2",
            counts.get('inbox', 0),
            counts.get('sent', 0),
            time.time() - start_time
        )
    
    def test_credential(self, credential: CredentialModel) -> bool:
        """
        Test credential without full processing.
        
        Args:
            credential: Credential to test
            
        Returns:
            True if credential is valid, False otherwise
        """
        try:
            if credential.is_app_password():
                return self.app_password_auth.test_connection(credential)
            elif credential.is_oauth2():
                return self.oauth2_auth.test_connection(credential)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Credential test failed: {e}")
            return False
    
    def get_supported_auth_types(self) -> list:
        """
        Get list of supported authentication types.
        
        Returns:
            List of supported auth type strings
        """
        return ["app_password", "oauth2"]