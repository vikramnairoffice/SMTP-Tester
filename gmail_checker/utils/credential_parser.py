"""
Credential parser for both app password and OAuth2 formats.
Maximum 150 LoC as per architecture requirements.
"""

import json
import logging
from typing import List, Union, Dict, Any
from ..models.credential_model import CredentialModel, AuthType


class CredentialParser:
    """
    Parser for handling both app password and OAuth2 credential formats.
    
    Supports:
    - App password format: "email:password"
    - OAuth2 format: JSON client secret files
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_app_password_text(self, text: str) -> List[CredentialModel]:
        """
        Parse app password credentials from text input.
        
        Args:
            text: Multi-line text with email:password format
            
        Returns:
            List of CredentialModel instances
            
        Raises:
            ValueError: If format is invalid
        """
        credentials = []
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        
        for line_num, line in enumerate(lines, 1):
            if ':' not in line:
                raise ValueError(f"Line {line_num}: Invalid format. Expected 'email:password'")
            
            parts = line.split(':', 1)
            if len(parts) != 2:
                raise ValueError(f"Line {line_num}: Invalid format. Expected 'email:password'")
            
            email, password = parts[0].strip(), parts[1].strip()
            
            if not email or not password:
                raise ValueError(f"Line {line_num}: Empty email or password")
            
            if '@' not in email:
                raise ValueError(f"Line {line_num}: Invalid email format")
            
            credentials.append(CredentialModel.from_app_password(email, password))
        
        return credentials
    
    def parse_oauth2_json(self, json_data: Union[str, Dict[str, Any]]) -> CredentialModel:
        """
        Parse OAuth2 client secret JSON data.
        
        Args:
            json_data: JSON string or dictionary containing client secret
            
        Returns:
            CredentialModel instance
            
        Raises:
            ValueError: If JSON format is invalid
        """
        if isinstance(json_data, str):
            try:
                client_secret = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {e}")
        else:
            client_secret = json_data
        
        # Validate required OAuth2 client secret structure
        if 'installed' not in client_secret:
            raise ValueError("Missing 'installed' section in client secret JSON")
        
        installed = client_secret['installed']
        required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
        
        for field in required_fields:
            if field not in installed:
                raise ValueError(f"Missing required field: {field}")
        
        return CredentialModel.from_oauth2_data(client_secret)
    
    def parse_oauth2_files(self, file_objects: List[Any]) -> List[CredentialModel]:
        """
        Parse multiple OAuth2 client secret files.
        
        Args:
            file_objects: List of file objects from Gradio file upload
            
        Returns:
            List of CredentialModel instances
        """
        credentials = []
        
        for file_obj in file_objects:
            try:
                file_content = file_obj.read()
                if isinstance(file_content, bytes):
                    file_content = file_content.decode('utf-8')
                
                credential = self.parse_oauth2_json(file_content)
                credentials.append(credential)
                
            except Exception as e:
                self.logger.error(f"Error parsing file {file_obj.name}: {e}")
                # Create a failed credential for tracking
                failed_credential = CredentialModel.from_oauth2_data({})
                failed_credential.set_failed(f"File parsing error: {e}")
                credentials.append(failed_credential)
        
        return credentials
    
    def detect_credential_type(self, data: Union[str, Dict[str, Any]]) -> AuthType:
        """
        Detect credential type from input data.
        
        Args:
            data: Input data (string or dictionary)
            
        Returns:
            AuthType enum value
        """
        if isinstance(data, dict):
            return AuthType.OAUTH2
        elif isinstance(data, str):
            if ':' in data and not data.strip().startswith('{'):
                return AuthType.APP_PASSWORD
            else:
                # Try to parse as JSON
                try:
                    json.loads(data)
                    return AuthType.OAUTH2
                except json.JSONDecodeError:
                    return AuthType.APP_PASSWORD
        
        return AuthType.APP_PASSWORD
    
    def validate_oauth2_client_secret(self, client_secret: Dict[str, Any]) -> bool:
        """
        Validate OAuth2 client secret structure.
        
        Args:
            client_secret: Client secret dictionary
            
        Returns:
            True if valid, False otherwise
        """
        try:
            if 'installed' not in client_secret:
                return False
            
            installed = client_secret['installed']
            required_fields = ['client_id', 'client_secret', 'auth_uri', 'token_uri']
            
            return all(field in installed for field in required_fields)
            
        except Exception:
            return False