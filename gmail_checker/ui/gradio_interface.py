"""
Main Gradio interface for Gmail IMAP credentials checker.
Maximum 150 LoC as per architecture requirements.
"""

import gradio as gr
import logging
from typing import List, Tuple, Optional
from ..core.auth_manager import AuthManager
from ..utils.credential_parser import CredentialParser
from ..utils.file_handler import FileHandler
from ..utils.email_counter import EmailCounter
from ..utils.debug_logger import debug_logger, log_function_call
from .ui_components import UIComponents


class GradioInterface:
    """
    Main Gradio web interface for the Gmail checker application.
    
    Provides complete UI workflow for credential processing,
    authentication, and results display.
    """
    
    def __init__(self):
        """Initialize interface with required components."""
        self.auth_manager = AuthManager()
        self.credential_parser = CredentialParser()
        self.file_handler = FileHandler()
        self.email_counter = EmailCounter()
        self.ui_components = UIComponents()
        self.logger = logging.getLogger(__name__)
    
    def create_interface(self) -> gr.Blocks:
        """
        Create the main Gradio interface.
        
        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(
            title="Gmail IMAP Credentials Checker",
            theme=gr.themes.Soft(),
            css=self._get_custom_css()
        ) as interface:
            
            # Header and instructions
            self.ui_components.create_header()
            self.ui_components.create_instructions()
            
            # Input sections
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🔑 App Password Authentication")
                    app_password_input = self.ui_components.create_app_password_input()
                
                with gr.Column(scale=1):
                    gr.Markdown("### 🛡️ OAuth2 Authentication")
                    oauth2_files = self.ui_components.create_oauth2_file_input()
            
            # Process button
            process_button = self.ui_components.create_process_button()
            
            # Results section
            gr.Markdown("## 📊 Results")
            progress_display = self.ui_components.create_progress_display()
            results_table = self.ui_components.create_results_display()
            statistics_display = self.ui_components.create_statistics_display()
            
            # Download section
            csv_file, summary_file = self.ui_components.create_download_section()
            
            # Event handlers
            process_button.click(
                fn=self.process_credentials,
                inputs=[app_password_input, oauth2_files],
                outputs=[progress_display, results_table, statistics_display, csv_file, summary_file]
            )
            
        return interface
    
    @log_function_call
    def process_credentials(self, app_password_text: str, oauth2_files: List) -> Tuple:
        """
        Process both app password and OAuth2 credentials.
        
        Args:
            app_password_text: App password credentials text
            oauth2_files: List of OAuth2 JSON files
            
        Returns:
            Tuple of (progress, results_table, statistics, csv_file, summary_file)
        """
        debug_logger.info("Processing credentials started", {
            'app_password_lines': len(app_password_text.split('\n')) if app_password_text else 0,
            'oauth2_files_count': len(oauth2_files) if oauth2_files else 0
        })
        
        try:
            all_credentials = []
            
            # Parse app password credentials
            if app_password_text and app_password_text.strip():
                debug_logger.debug("Parsing app password credentials")
                app_creds = self.credential_parser.parse_app_password_text(app_password_text)
                all_credentials.extend(app_creds)
                debug_logger.info(f"Parsed {len(app_creds)} app password credentials")
            
            # Parse OAuth2 credentials
            if oauth2_files:
                debug_logger.debug("Parsing OAuth2 credentials")
                oauth2_creds = self.credential_parser.parse_oauth2_files(oauth2_files)
                all_credentials.extend(oauth2_creds)
                debug_logger.info(f"Parsed {len(oauth2_creds)} OAuth2 credentials")
            
            if not all_credentials:
                debug_logger.warning("No valid credentials provided")
                return (
                    self.ui_components.create_status_message("No valid credentials provided", "error"),
                    [], "", gr.update(visible=False), gr.update(visible=False)
                )
            
            # Process credentials
            results = []
            debug_logger.info(f"Starting processing of {len(all_credentials)} credentials")
            
            for i, credential in enumerate(all_credentials):
                debug_logger.debug(f"Processing credential {i+1}/{len(all_credentials)}: {credential.get_display_id()}")
                
                current_progress = self.ui_components.create_status_message(
                    f"Processing {i+1}/{len(all_credentials)}: {credential.get_display_id()}",
                    "info"
                )
                
                result = self.auth_manager.authenticate_and_count(credential)
                results.append(result)
                debug_logger.info(f"Credential processed: {result.status.value}")
            
            # Generate outputs
            debug_logger.debug("Generating outputs and reports")
            results_table_data = self.ui_components.format_results_table(
                [r.to_dict() for r in results]
            )
            
            statistics = self._generate_statistics(results)
            csv_path = self.file_handler.export_results_to_csv(results)
            summary_path = self.file_handler.generate_summary_report(results)
            
            final_progress = self.ui_components.create_status_message(
                f"Processing complete! {len(results)} credentials processed.",
                "success"
            )
            
            debug_logger.info("Processing completed successfully", {
                'total_processed': len(results),
                'csv_exported': csv_path is not None,
                'summary_exported': summary_path is not None
            })
            
            return (
                final_progress,
                results_table_data,
                statistics,
                gr.update(value=csv_path, visible=True) if csv_path else gr.update(visible=False),
                gr.update(value=summary_path, visible=True) if summary_path else gr.update(visible=False)
            )
            
        except Exception as e:
            debug_logger.error("Processing failed", e, {
                'app_password_provided': bool(app_password_text),
                'oauth2_files_provided': bool(oauth2_files)
            })
            error_msg = self.ui_components.create_status_message(
                f"Processing failed: {str(e)}", "error"
            )
            return (error_msg, [], "", gr.update(visible=False), gr.update(visible=False))
    
    def _generate_statistics(self, results: List) -> str:
        """Generate statistics markdown from results."""
        stats = self.email_counter.generate_summary_report(results)
        
        return f"""
        ### 📈 Statistics
        
        - **Total Accounts**: {stats['total_accounts']}
        - **Successful**: {stats['successful']}
        - **Failed**: {stats['failed']}
        - **Success Rate**: {stats['success_rate']:.1f}%
        - **Total Emails**: {stats['total_emails']:,}
        - **Average per Account**: {stats['average_emails_per_account']:.1f}
        """
    
    def _get_custom_css(self) -> str:
        """Get custom CSS for interface styling."""
        return """
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    
    def launch(self, **kwargs) -> None:
        """
        Launch the Gradio interface.
        
        Args:
            **kwargs: Additional arguments for gr.launch()
        """
        interface = self.create_interface()
        interface.launch(
            share=True,
            debug=True,
            **kwargs
        )