"""
Reusable UI components for Gradio interface.
Maximum 150 LoC as per architecture requirements.
"""

import gradio as gr
from typing import Dict, List, Any


class UIComponents:
    """
    Reusable UI components for the Gmail checker interface.
    
    Provides standardized UI elements and styling for consistent
    user experience across the application.
    """
    
    @staticmethod
    def create_header() -> gr.Markdown:
        """
        Create application header with title and description.
        
        Returns:
            Gradio Markdown component with header content
        """
        header_content = """
        # Gmail IMAP Credentials Checker
        
        A tool for bulk validation of Gmail credentials supporting both **App Passwords** and **OAuth2 Client Secrets**.
        
        **Features:**
        - Bulk credential validation
        - Email counting (Inbox & Sent)
        - CSV export functionality
        - Google Colab optimized OAuth2 flow
        """
        return gr.Markdown(header_content)
    
    @staticmethod
    def create_instructions() -> gr.Markdown:
        """
        Create usage instructions.
        
        Returns:
            Gradio Markdown component with instructions
        """
        instructions = """
        ## How to Use
        
        ### App Password Method
        1. Enter credentials in format: `email@gmail.com:app_password`
        2. One credential per line
        3. Click "Process Credentials"
        
        ### OAuth2 Method
        1. Upload JSON client secret files from Google Cloud Console
        2. Click "Process Credentials"
        3. Follow OAuth2 authentication prompts in Colab output
        4. **Important:** Check Colab cell output for authentication links
        
        ### Setup OAuth2 Client Secrets
        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
        2. Create new project or select existing
        3. Enable Gmail API
        4. Create OAuth2 Client ID (Desktop Application)
        5. Download JSON file and upload here
        """
        return gr.Markdown(instructions)
    
    @staticmethod
    def create_app_password_input() -> gr.Textbox:
        """
        Create app password input textbox.
        
        Returns:
            Gradio Textbox component for app password input
        """
        return gr.Textbox(
            label="App Password Credentials",
            placeholder="email1@gmail.com:app_password1\nemail2@gmail.com:app_password2",
            lines=8,
            max_lines=20
        )
    
    @staticmethod
    def create_oauth2_file_input() -> gr.File:
        """
        Create OAuth2 file upload component.
        
        Returns:
            Gradio File component for OAuth2 JSON uploads
        """
        return gr.File(
            label="OAuth2 Client Secret Files",
            file_count="multiple",
            file_types=[".json"]
        )
    
    @staticmethod
    def create_process_button() -> gr.Button:
        """
        Create main process button.
        
        Returns:
            Gradio Button component for processing
        """
        return gr.Button(
            "🚀 Process Credentials",
            variant="primary",
            size="lg"
        )
    
    @staticmethod
    def create_results_display() -> gr.Dataframe:
        """
        Create results display table.
        
        Returns:
            Gradio Dataframe component for results
        """
        return gr.Dataframe(
            headers=["Email", "Auth Type", "Status", "Inbox Count", "Sent Count", "Total", "Error"],
            label="Processing Results",
            interactive=False,
            wrap=True
        )
    
    @staticmethod
    def create_progress_display() -> gr.Markdown:
        """
        Create progress display component.
        
        Returns:
            Gradio Markdown component for progress updates
        """
        return gr.Markdown(
            value="Ready to process credentials...",
            label="Processing Status"
        )
    
    @staticmethod
    def create_download_section() -> tuple:
        """
        Create download section with CSV and summary files.
        
        Returns:
            Tuple of (csv_file, summary_file) Gradio components
        """
        csv_file = gr.File(
            label="📊 Download CSV Results",
            visible=False
        )
        
        summary_file = gr.File(
            label="📋 Download Summary Report",
            visible=False
        )
        
        return csv_file, summary_file
    
    @staticmethod
    def create_statistics_display() -> gr.Markdown:
        """
        Create statistics display component.
        
        Returns:
            Gradio Markdown component for statistics
        """
        return gr.Markdown(
            value="",
            label="Statistics",
            visible=False
        )
    
    @staticmethod
    def format_results_table(results: List[Dict[str, Any]]) -> List[List[str]]:
        """
        Format results for display in Gradio table.
        
        Args:
            results: List of result dictionaries
            
        Returns:
            List of lists formatted for Gradio Dataframe
        """
        formatted_results = []
        
        for result in results:
            row = [
                result.get('email', ''),
                result.get('auth_type', ''),
                result.get('status', ''),
                str(result.get('inbox_count', 0)),
                str(result.get('sent_count', 0)),
                str(result.get('inbox_count', 0) + result.get('sent_count', 0)),
                result.get('error_message', '')
            ]
            formatted_results.append(row)
        
        return formatted_results
    
    @staticmethod
    def create_status_message(message: str, message_type: str = "info") -> str:
        """
        Create formatted status message.
        
        Args:
            message: Message text
            message_type: Type of message (info, success, error, warning)
            
        Returns:
            Formatted markdown message
        """
        emoji_map = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️"
        }
        
        emoji = emoji_map.get(message_type, "ℹ️")
        return f"{emoji} **{message_type.upper()}**: {message}"