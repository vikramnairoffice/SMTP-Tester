"""
IMAP connector module for Gmail connections and operations.
Maximum 150 LoC as per architecture requirements.
"""

import imaplib
import logging
from typing import Optional, Dict, Any
from ..models.credential_model import CredentialModel
from ..models.result_model import ResultModel, AuthStatus


class IMAPConnector:
    """
    Handles IMAP connections and basic operations for Gmail.
    
    Provides unified interface for IMAP operations regardless of
    authentication method (app password or OAuth2).
    """
    
    INBOX_FOLDER = "INBOX"
    SENT_FOLDER = '"[Gmail]/Sent Mail"'
    
    def __init__(self, imap_server: str = "imap.gmail.com", port: int = 993):
        """
        Initialize IMAP connector.
        
        Args:
            imap_server: IMAP server hostname
            port: IMAP server port
        """
        self.imap_server = imap_server
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def get_folder_count(self, imap_conn: imaplib.IMAP4_SSL, folder: str) -> int:
        """
        Get email count from specified folder.
        
        Args:
            imap_conn: Active IMAP connection
            folder: Folder name to check
            
        Returns:
            Number of emails in folder
        """
        try:
            status, messages = imap_conn.select(folder, readonly=True)
            if status == 'OK':
                # messages[0] contains the count as bytes
                return int(messages[0])
            else:
                self.logger.warning(f"Failed to select folder {folder}: {status}")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error getting count for folder {folder}: {e}")
            return 0
    
    def get_all_folder_counts(self, imap_conn: imaplib.IMAP4_SSL) -> Dict[str, int]:
        """
        Get email counts from all standard folders.
        
        Args:
            imap_conn: Active IMAP connection
            
        Returns:
            Dictionary with folder names and counts
        """
        folders = {
            'inbox': self.INBOX_FOLDER,
            'sent': self.SENT_FOLDER
        }
        
        counts = {}
        for folder_key, folder_name in folders.items():
            counts[folder_key] = self.get_folder_count(imap_conn, folder_name)
        
        return counts
    
    def test_connection(self, imap_conn: imaplib.IMAP4_SSL) -> bool:
        """
        Test if IMAP connection is valid and responsive.
        
        Args:
            imap_conn: IMAP connection to test
            
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            # Try to get server capabilities
            status, capabilities = imap_conn.capability()
            return status == 'OK'
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def close_connection(self, imap_conn: imaplib.IMAP4_SSL):
        """
        Safely close IMAP connection.
        
        Args:
            imap_conn: IMAP connection to close
        """
        try:
            if imap_conn:
                imap_conn.logout()
                self.logger.debug("IMAP connection closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing IMAP connection: {e}")
    
    def get_connection_info(self, imap_conn: imaplib.IMAP4_SSL) -> Dict[str, Any]:
        """
        Get connection information and server details.
        
        Args:
            imap_conn: Active IMAP connection
            
        Returns:
            Dictionary with connection details
        """
        try:
            # Get server capabilities
            status, capabilities = imap_conn.capability()
            capabilities_str = capabilities[0].decode() if status == 'OK' else 'Unknown'
            
            return {
                'server': self.imap_server,
                'port': self.port,
                'encryption': 'SSL',
                'capabilities': capabilities_str,
                'status': 'Connected'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting connection info: {e}")
            return {
                'server': self.imap_server,
                'port': self.port,
                'encryption': 'SSL',
                'capabilities': 'Unknown',
                'status': f'Error: {str(e)}'
            }
    
    def list_folders(self, imap_conn: imaplib.IMAP4_SSL) -> list:
        """
        List available folders on the server.
        
        Args:
            imap_conn: Active IMAP connection
            
        Returns:
            List of folder names
        """
        try:
            status, folders = imap_conn.list()
            if status == 'OK':
                folder_list = []
                for folder in folders:
                    # Parse folder name from response
                    folder_str = folder.decode() if isinstance(folder, bytes) else folder
                    # Extract folder name (simplified parsing)
                    if '"' in folder_str:
                        folder_name = folder_str.split('"')[-2]
                        folder_list.append(folder_name)
                return folder_list
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error listing folders: {e}")
            return []