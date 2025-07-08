"""
Email counting utility for IMAP operations.
Maximum 150 LoC as per architecture requirements.
"""

import imaplib
import logging
from typing import Dict, List, Optional
from ..models.result_model import ResultModel


class EmailCounter:
    """
    Utility class for counting emails in various folders.
    
    Provides methods to count emails in different folders and
    generate statistics from IMAP connections.
    """
    
    DEFAULT_FOLDERS = {
        'inbox': 'INBOX',
        'sent': '"[Gmail]/Sent Mail"',
        'drafts': '"[Gmail]/Drafts"',
        'spam': '"[Gmail]/Spam"',
        'trash': '"[Gmail]/Trash"'
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def count_emails_in_folder(self, imap_conn: imaplib.IMAP4_SSL, folder: str) -> int:
        """
        Count emails in a specific folder.
        
        Args:
            imap_conn: Active IMAP connection
            folder: Folder name to count
            
        Returns:
            Number of emails in folder
        """
        try:
            status, messages = imap_conn.select(folder, readonly=True)
            if status == 'OK':
                # messages[0] contains the count as bytes
                count = int(messages[0])
                self.logger.debug(f"Folder {folder}: {count} emails")
                return count
            else:
                self.logger.warning(f"Failed to select folder {folder}: {status}")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error counting emails in folder {folder}: {e}")
            return 0
    
    def count_all_folders(self, imap_conn: imaplib.IMAP4_SSL) -> Dict[str, int]:
        """
        Count emails in all default folders.
        
        Args:
            imap_conn: Active IMAP connection
            
        Returns:
            Dictionary with folder names and counts
        """
        counts = {}
        
        for folder_key, folder_name in self.DEFAULT_FOLDERS.items():
            counts[folder_key] = self.count_emails_in_folder(imap_conn, folder_name)
        
        return counts
    
    def get_folder_statistics(self, imap_conn: imaplib.IMAP4_SSL) -> Dict[str, any]:
        """
        Get detailed statistics for all folders.
        
        Args:
            imap_conn: Active IMAP connection
            
        Returns:
            Dictionary with detailed statistics
        """
        counts = self.count_all_folders(imap_conn)
        
        total_emails = sum(counts.values())
        primary_folders = counts.get('inbox', 0) + counts.get('sent', 0)
        
        return {
            'folder_counts': counts,
            'total_emails': total_emails,
            'primary_folders': primary_folders,
            'inbox_percentage': (counts.get('inbox', 0) / total_emails * 100) if total_emails > 0 else 0,
            'sent_percentage': (counts.get('sent', 0) / total_emails * 100) if total_emails > 0 else 0
        }
    
    def search_emails_by_criteria(self, imap_conn: imaplib.IMAP4_SSL, 
                                folder: str, criteria: str) -> int:
        """
        Search and count emails matching criteria.
        
        Args:
            imap_conn: Active IMAP connection
            folder: Folder to search in
            criteria: Search criteria (e.g., 'UNSEEN', 'FROM gmail.com')
            
        Returns:
            Number of matching emails
        """
        try:
            status, messages = imap_conn.select(folder, readonly=True)
            if status != 'OK':
                return 0
            
            status, search_results = imap_conn.search(None, criteria)
            if status == 'OK':
                # Count the search results
                if search_results[0]:
                    email_ids = search_results[0].split()
                    count = len(email_ids)
                    self.logger.debug(f"Found {count} emails matching criteria '{criteria}' in {folder}")
                    return count
                else:
                    return 0
            else:
                self.logger.warning(f"Search failed in folder {folder}: {status}")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error searching emails in folder {folder}: {e}")
            return 0
    
    def get_unread_counts(self, imap_conn: imaplib.IMAP4_SSL) -> Dict[str, int]:
        """
        Get unread email counts for all folders.
        
        Args:
            imap_conn: Active IMAP connection
            
        Returns:
            Dictionary with folder names and unread counts
        """
        unread_counts = {}
        
        for folder_key, folder_name in self.DEFAULT_FOLDERS.items():
            unread_count = self.search_emails_by_criteria(imap_conn, folder_name, 'UNSEEN')
            unread_counts[folder_key] = unread_count
        
        return unread_counts
    
    def generate_summary_report(self, results: List[ResultModel]) -> Dict[str, any]:
        """
        Generate summary report from multiple results.
        
        Args:
            results: List of ResultModel instances
            
        Returns:
            Summary statistics dictionary
        """
        if not results:
            return {'total_accounts': 0, 'successful': 0, 'failed': 0}
        
        total_accounts = len(results)
        successful = sum(1 for r in results if r.is_success())
        failed = total_accounts - successful
        
        total_inbox = sum(r.inbox_count for r in results if r.is_success())
        total_sent = sum(r.sent_count for r in results if r.is_success())
        total_emails = total_inbox + total_sent
        
        return {
            'total_accounts': total_accounts,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total_accounts * 100) if total_accounts > 0 else 0,
            'total_inbox_emails': total_inbox,
            'total_sent_emails': total_sent,
            'total_emails': total_emails,
            'average_emails_per_account': total_emails / successful if successful > 0 else 0
        }