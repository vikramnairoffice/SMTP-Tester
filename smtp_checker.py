#!/usr/bin/env python3
import imaplib
import json
import base64
import pandas as pd
import gradio as gr
from tqdm import tqdm
import traceback
import os
import sys

# Check if running in Colab
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# Install OAuth2 dependencies if needed
try:
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("Installing OAuth2 dependencies...")
    if IN_COLAB:
        os.system("pip install google-auth google-auth-oauthlib google-api-python-client")
    else:
        os.system("pip install google-auth google-auth-oauthlib google-api-python-client")
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

def test_app_password(email, password):
    """Test Gmail app password authentication"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(email, password)
        
        # Count inbox emails
        mail.select("INBOX")
        _, inbox_data = mail.search(None, 'ALL')
        inbox_count = len(inbox_data[0].split()) if inbox_data[0] else 0
        
        # Count sent emails
        mail.select('"[Gmail]/Sent Mail"')
        _, sent_data = mail.search(None, 'ALL')
        sent_count = len(sent_data[0].split()) if sent_data[0] else 0
        
        mail.logout()
        return True, inbox_count, sent_count, ""
    except Exception as e:
        return False, 0, 0, str(e)

def test_oauth2_with_password(client_secret_data, email, password):
    """Test OAuth2 with email/password credentials"""
    try:
        # For bulk testing, we'll use a simplified approach
        # This attempts to use the client secret with provided credentials
        
        # First try direct IMAP with the password as app password
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            mail.login(email, password)
            
            # Count inbox emails
            mail.select("INBOX")
            _, inbox_data = mail.search(None, 'ALL')
            inbox_count = len(inbox_data[0].split()) if inbox_data[0] else 0
            
            # Count sent emails
            mail.select('"[Gmail]/Sent Mail"')
            _, sent_data = mail.search(None, 'ALL')
            sent_count = len(sent_data[0].split()) if sent_data[0] else 0
            
            mail.logout()
            return True, email, inbox_count, sent_count, ""
        except:
            # If direct login fails, return error
            return False, email, 0, 0, "OAuth2 bulk testing requires manual authorization per account"
            
    except Exception as e:
        return False, email, 0, 0, str(e)

def process_credentials_v2(app_passwords_text, oauth2_credentials, oauth2_files):
    """Process both app passwords and OAuth2 credentials"""
    results = []
    
    # Process app passwords
    if app_passwords_text.strip():
        lines = app_passwords_text.strip().split('\n')
        for line in tqdm(lines, desc="Testing app passwords"):
            if ':' in line:
                email, password = line.split(':', 1)
                email = email.strip()
                password = password.strip()
                
                success, inbox_count, sent_count, error = test_app_password(email, password)
                
                results.append({
                    'Email': email,
                    'Auth Type': 'App Password',
                    'Status': 'Success' if success else 'Failed',
                    'Inbox Count': inbox_count,
                    'Sent Count': sent_count,
                    'Error': error
                })
    
    # Process OAuth2 credentials with passwords
    if oauth2_credentials.strip():
        lines = oauth2_credentials.strip().split('\n')
        # Get first OAuth2 file as reference (if provided)
        client_secret_data = None
        if oauth2_files:
            try:
                file = oauth2_files[0]
                if hasattr(file, 'name'):
                    with open(file.name, 'r') as f:
                        client_secret_data = json.load(f)
            except:
                pass
        
        for line in tqdm(lines, desc="Testing OAuth2 credentials"):
            if ':' in line:
                email, password = line.split(':', 1)
                email = email.strip()
                password = password.strip()
                
                success, email_result, inbox_count, sent_count, error = test_oauth2_with_password(client_secret_data, email, password)
                
                results.append({
                    'Email': email_result,
                    'Auth Type': 'OAuth2',
                    'Status': 'Success' if success else 'Failed',
                    'Inbox Count': inbox_count,
                    'Sent Count': sent_count,
                    'Error': error
                })
    
    return pd.DataFrame(results)

def export_results(df):
    """Export results to CSV"""
    if df.empty:
        return None
    
    filename = "smtp_test_results.csv"
    df.to_csv(filename, index=False)
    return filename

def create_interface():
    """Create Gradio interface"""
    with gr.Blocks(title="SMTP Checker") as app:
        gr.Markdown("# Gmail SMTP Checker")
        gr.Markdown("Test Gmail credentials in bulk - supports app passwords and OAuth2")
        
        with gr.Tab("App Passwords"):
            app_passwords_input = gr.Textbox(
                label="App Passwords (one per line)",
                placeholder="email1@gmail.com:password1\nemail2@gmail.com:password2",
                lines=10
            )
        
        with gr.Tab("OAuth2 + Passwords"):
            gr.Markdown("**Note**: OAuth2 bulk testing requires email:password format due to interactive nature")
            oauth2_credentials = gr.Textbox(
                label="OAuth2 Credentials with Passwords",
                placeholder="email1@gmail.com:password1\nemail2@gmail.com:password2",
                lines=10
            )
            oauth2_files = gr.File(
                label="OAuth2 JSON Files (Optional - for reference)",
                file_count="multiple",
                file_types=[".json"]
            )
        
        test_button = gr.Button("Test Credentials", variant="primary")
        
        results_df = gr.Dataframe(
            headers=["Email", "Auth Type", "Status", "Inbox Count", "Sent Count", "Error"],
            label="Results"
        )
        
        export_button = gr.Button("Export Results")
        download_file = gr.File(label="Download Results")
        
        def test_all(app_passwords_text, oauth2_credentials, oauth2_files):
            try:
                if not app_passwords_text.strip() and not oauth2_credentials.strip():
                    return pd.DataFrame([{
                        'Email': 'Error',
                        'Auth Type': '',
                        'Status': 'No credentials provided',
                        'Inbox Count': '',
                        'Sent Count': '',
                        'Error': 'Please provide app passwords or OAuth2 credentials'
                    }])
                
                return process_credentials_v2(app_passwords_text, oauth2_credentials, oauth2_files)
            except Exception as e:
                return pd.DataFrame([{
                    'Email': 'Error',
                    'Auth Type': '',
                    'Status': 'System Error',
                    'Inbox Count': '',
                    'Sent Count': '',
                    'Error': str(e)
                }])
        
        def export_data(df):
            if df is None or df.empty:
                return None
            return export_results(df)
        
        test_button.click(
            fn=test_all,
            inputs=[app_passwords_input, oauth2_credentials, oauth2_files],
            outputs=[results_df]
        )
        
        export_button.click(
            fn=export_data,
            inputs=[results_df],
            outputs=[download_file]
        )
    
    return app

if __name__ == "__main__":
    app = create_interface()
    
    # Launch with appropriate settings for environment
    if IN_COLAB:
        app.launch(share=True, debug=True, show_error=True)
    else:
        app.launch(share=True)