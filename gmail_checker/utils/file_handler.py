"""
File handling utility for uploads, downloads, and CSV operations.
Maximum 150 LoC as per architecture requirements.
"""

import csv
import json
import logging
import os
from typing import List, Dict, Any
from io import StringIO
from ..models.result_model import ResultModel


class FileHandler:
    """
    Handles file operations for the Gmail checker application.
    
    Provides methods for processing uploads, generating CSV exports,
    and managing temporary files.
    """
    
    def __init__(self, temp_dir: str = "/tmp"):
        """
        Initialize file handler.
        
        Args:
            temp_dir: Directory for temporary files
        """
        self.temp_dir = temp_dir
        self.logger = logging.getLogger(__name__)
    
    def process_json_uploads(self, file_objects: List[Any]) -> List[Dict[str, Any]]:
        """
        Process uploaded JSON client secret files.
        
        Args:
            file_objects: List of file objects from Gradio
            
        Returns:
            List of parsed JSON data dictionaries
        """
        processed_files = []
        
        for file_obj in file_objects:
            try:
                # Read file content
                if hasattr(file_obj, 'read'):
                    content = file_obj.read()
                else:
                    with open(file_obj, 'r') as f:
                        content = f.read()
                
                # Decode if bytes
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
                
                # Parse JSON
                json_data = json.loads(content)
                
                processed_files.append({
                    'filename': getattr(file_obj, 'name', 'unknown'),
                    'data': json_data,
                    'status': 'success',
                    'error': None
                })
                
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON parsing error for {file_obj}: {e}")
                processed_files.append({
                    'filename': getattr(file_obj, 'name', 'unknown'),
                    'data': None,
                    'status': 'error',
                    'error': f"Invalid JSON: {str(e)}"
                })
                
            except Exception as e:
                self.logger.error(f"File processing error for {file_obj}: {e}")
                processed_files.append({
                    'filename': getattr(file_obj, 'name', 'unknown'),
                    'data': None,
                    'status': 'error',
                    'error': f"File error: {str(e)}"
                })
        
        return processed_files
    
    def export_results_to_csv(self, results: List[ResultModel]) -> str:
        """
        Export results to CSV format.
        
        Args:
            results: List of ResultModel instances
            
        Returns:
            Path to generated CSV file
        """
        if not results:
            return None
        
        # Generate CSV content
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'Email', 'Auth Type', 'Status', 'Inbox Count', 'Sent Count',
            'Total Emails', 'Error', 'Timestamp', 'Processing Time (s)'
        ])
        
        writer.writeheader()
        for result in results:
            writer.writerow(result.to_csv_row())
        
        # Save to temporary file
        csv_content = output.getvalue()
        csv_path = os.path.join(self.temp_dir, "gmail_check_results.csv")
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                f.write(csv_content)
            
            self.logger.info(f"CSV export saved to {csv_path}")
            return csv_path
            
        except Exception as e:
            self.logger.error(f"Error saving CSV file: {e}")
            return None
    
    def generate_summary_report(self, results: List[ResultModel]) -> str:
        """
        Generate human-readable summary report.
        
        Args:
            results: List of ResultModel instances
            
        Returns:
            Path to generated summary report file
        """
        if not results:
            return None
        
        # Calculate statistics
        total_accounts = len(results)
        successful = sum(1 for r in results if r.is_success())
        failed = total_accounts - successful
        
        total_inbox = sum(r.inbox_count for r in results if r.is_success())
        total_sent = sum(r.sent_count for r in results if r.is_success())
        
        # Generate report content
        report_lines = [
            "Gmail IMAP Credentials Check Summary",
            "=" * 40,
            f"Total Accounts Processed: {total_accounts}",
            f"Successful: {successful}",
            f"Failed: {failed}",
            f"Success Rate: {(successful/total_accounts*100):.1f}%",
            "",
            "Email Statistics:",
            f"Total Inbox Emails: {total_inbox:,}",
            f"Total Sent Emails: {total_sent:,}",
            f"Total Emails: {(total_inbox + total_sent):,}",
            "",
            "Detailed Results:",
            "-" * 20
        ]
        
        for result in results:
            report_lines.append(result.get_summary_text())
        
        # Save report
        report_content = "\n".join(report_lines)
        report_path = os.path.join(self.temp_dir, "gmail_check_summary.txt")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info(f"Summary report saved to {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error saving summary report: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            temp_files = [
                os.path.join(self.temp_dir, "gmail_check_results.csv"),
                os.path.join(self.temp_dir, "gmail_check_summary.txt")
            ]
            
            for file_path in temp_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.logger.debug(f"Cleaned up temporary file: {file_path}")
                    
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def validate_file_format(self, file_path: str, expected_format: str) -> bool:
        """
        Validate file format.
        
        Args:
            file_path: Path to file to validate
            expected_format: Expected format ('json', 'csv', 'txt')
            
        Returns:
            True if format is valid, False otherwise
        """
        try:
            if expected_format == 'json':
                with open(file_path, 'r') as f:
                    json.load(f)
                return True
            elif expected_format == 'csv':
                with open(file_path, 'r') as f:
                    csv.reader(f)
                return True
            elif expected_format == 'txt':
                with open(file_path, 'r') as f:
                    f.read()
                return True
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"File format validation failed: {e}")
            return False