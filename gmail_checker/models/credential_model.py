"""
Data model for credentials with support for both auth types.
Maximum 150 LoC as per architecture requirements.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Union, Dict, Any, Optional
from datetime import datetime


class AuthType(Enum):
    """Authentication type enumeration."""
    APP_PASSWORD = "app_password"
    OAUTH2 = "oauth2"


class CredentialStatus(Enum):
    """Credential processing status."""
    PENDING = "pending"
    AUTHENTICATED = "authenticated"
    FAILED = "failed"


@dataclass
class CredentialModel:
    """
    Unified credential model supporting both authentication types.
    
    Attributes:
        auth_type: Type of authentication (app_password or oauth2)
        email: Email address (for app_password) or extracted from OAuth2
        auth_data: Password string for app_password, dict for OAuth2 credentials
        status: Current processing status
        created_at: Timestamp of creation
        error_message: Error details if authentication fails
    """
    
    auth_type: AuthType
    email: str
    auth_data: Union[str, Dict[str, Any]]
    status: CredentialStatus = CredentialStatus.PENDING
    created_at: datetime = None
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Set creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @classmethod
    def from_app_password(cls, email: str, password: str) -> 'CredentialModel':
        """
        Create credential model from app password format.
        
        Args:
            email: Gmail address
            password: App password
            
        Returns:
            CredentialModel instance
        """
        return cls(
            auth_type=AuthType.APP_PASSWORD,
            email=email,
            auth_data=password
        )
    
    @classmethod
    def from_oauth2_data(cls, client_secret_data: Dict[str, Any]) -> 'CredentialModel':
        """
        Create credential model from OAuth2 client secret data.
        
        Args:
            client_secret_data: OAuth2 client secret JSON data
            
        Returns:
            CredentialModel instance
        """
        return cls(
            auth_type=AuthType.OAUTH2,
            email="",  # Will be filled after OAuth2 flow
            auth_data=client_secret_data
        )
    
    def is_app_password(self) -> bool:
        """Check if this is an app password credential."""
        return self.auth_type == AuthType.APP_PASSWORD
    
    def is_oauth2(self) -> bool:
        """Check if this is an OAuth2 credential."""
        return self.auth_type == AuthType.OAUTH2
    
    def set_authenticated(self, email: str = None):
        """
        Mark credential as authenticated.
        
        Args:
            email: Email address (for OAuth2 flow where email is discovered)
        """
        self.status = CredentialStatus.AUTHENTICATED
        if email:
            self.email = email
    
    def set_failed(self, error_message: str):
        """
        Mark credential as failed with error message.
        
        Args:
            error_message: Description of the failure
        """
        self.status = CredentialStatus.FAILED
        self.error_message = error_message
    
    def get_display_id(self) -> str:
        """
        Get display identifier for this credential.
        
        Returns:
            Email for app_password, client_id for OAuth2
        """
        if self.is_app_password():
            return self.email
        elif self.is_oauth2() and isinstance(self.auth_data, dict):
            client_config = self.auth_data.get('installed', {})
            return client_config.get('client_id', 'Unknown Client')
        return 'Unknown'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'auth_type': self.auth_type.value,
            'email': self.email,
            'auth_data': self.auth_data,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'error_message': self.error_message
        }