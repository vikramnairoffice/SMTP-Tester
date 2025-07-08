"""
Data model for authentication and email counting results.
Maximum 150 LoC as per architecture requirements.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class AuthStatus(Enum):
    """Authentication result status."""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


@dataclass
class ResultModel:
    """
    Result model for credential authentication and email counting.
    
    Attributes:
        email: Email address
        auth_type: Type of authentication used
        status: Authentication result status
        inbox_count: Number of emails in INBOX
        sent_count: Number of emails in Sent folder
        error_message: Error details if authentication fails
        timestamp: When the result was generated
        processing_time: Time taken for processing in seconds
    """
    
    email: str
    auth_type: str
    status: AuthStatus
    inbox_count: int = 0
    sent_count: int = 0
    error_message: Optional[str] = None
    timestamp: datetime = None
    processing_time: Optional[float] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @classmethod
    def create_success(cls, email: str, auth_type: str, inbox_count: int, 
                      sent_count: int, processing_time: float = None) -> 'ResultModel':
        """
        Create successful result.
        
        Args:
            email: Email address
            auth_type: Authentication type used
            inbox_count: Number of emails in INBOX
            sent_count: Number of emails in Sent folder
            processing_time: Processing time in seconds
            
        Returns:
            ResultModel instance
        """
        return cls(
            email=email,
            auth_type=auth_type,
            status=AuthStatus.SUCCESS,
            inbox_count=inbox_count,
            sent_count=sent_count,
            processing_time=processing_time
        )
    
    @classmethod
    def create_failure(cls, email: str, auth_type: str, error_message: str,
                      processing_time: float = None) -> 'ResultModel':
        """
        Create failed result.
        
        Args:
            email: Email address
            auth_type: Authentication type used
            error_message: Error description
            processing_time: Processing time in seconds
            
        Returns:
            ResultModel instance
        """
        return cls(
            email=email,
            auth_type=auth_type,
            status=AuthStatus.FAILED,
            error_message=error_message,
            processing_time=processing_time
        )
    
    def is_success(self) -> bool:
        """Check if result is successful."""
        return self.status == AuthStatus.SUCCESS
    
    def is_failed(self) -> bool:
        """Check if result is failed."""
        return self.status == AuthStatus.FAILED
    
    def get_total_emails(self) -> int:
        """Get total email count (inbox + sent)."""
        return self.inbox_count + self.sent_count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'email': self.email,
            'auth_type': self.auth_type,
            'status': self.status.value,
            'inbox_count': self.inbox_count,
            'sent_count': self.sent_count,
            'total_emails': self.get_total_emails(),
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat(),
            'processing_time': self.processing_time
        }
    
    def to_csv_row(self) -> Dict[str, Any]:
        """Convert to CSV row format."""
        return {
            'Email': self.email,
            'Auth Type': self.auth_type,
            'Status': self.status.value,
            'Inbox Count': self.inbox_count,
            'Sent Count': self.sent_count,
            'Total Emails': self.get_total_emails(),
            'Error': self.error_message or '',
            'Timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Processing Time (s)': self.processing_time or 0
        }
    
    def get_status_emoji(self) -> str:
        """Get emoji representation of status."""
        if self.is_success():
            return "✅"
        elif self.is_failed():
            return "❌"
        else:
            return "⏳"
    
    def get_summary_text(self) -> str:
        """Get human-readable summary."""
        if self.is_success():
            return f"{self.get_status_emoji()} {self.email}: {self.get_total_emails()} emails"
        else:
            return f"{self.get_status_emoji()} {self.email}: {self.error_message}"