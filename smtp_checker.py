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

def test_oauth2(client_secret_data):
    """Test OAuth2 authentication"""
    try:
        # OAuth2 flow
        SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/userinfo.email']
        flow = InstalledAppFlow.from_client_config(client_secret_data, SCOPES)
        
        # Use different flow for Colab vs local
        if IN_COLAB:
            credentials = flow.run_console()
        else:
            credentials = flow.run_local_server(port=0, access_type='offline', prompt='consent')
        
        # Get user email
        service = build('people', 'v1', credentials=credentials)
        profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
        email = profile['emailAddresses'][0]['value']
        
        # Create XOAUTH2 string
        xoauth2_string = f"user={email}\x01auth=Bearer {credentials.token}\x01\x01"
        xoauth2_string = base64.b64encode(xoauth2_string.encode()).decode()
        
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.authenticate('XOAUTH2', lambda x: xoauth2_string)
        
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
    except Exception as e:
        return False, "", 0, 0, str(e)

def process_credentials(app_passwords_text, oauth2_files):
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
    
    # Process OAuth2 files
    if oauth2_files:
        for file in tqdm(oauth2_files, desc="Testing OAuth2"):
            try:
                # Handle file differently in Colab vs local
                if IN_COLAB:
                    if hasattr(file, 'name'):
                        with open(file.name, 'r') as f:
                            client_secret_data = json.load(f)
                    else:
                        # Direct file content
                        client_secret_data = json.loads(file.decode('utf-8'))
                else:
                    with open(file.name, 'r') as f:
                        client_secret_data = json.load(f)
                
                success, email, inbox_count, sent_count, error = test_oauth2(client_secret_data)
                
                results.append({
                    'Email': email if email else 'Unknown',
                    'Auth Type': 'OAuth2',
                    'Status': 'Success' if success else 'Failed',
                    'Inbox Count': inbox_count,
                    'Sent Count': sent_count,
                    'Error': error
                })
            except Exception as e:
                results.append({
                    'Email': file.name,
                    'Auth Type': 'OAuth2',
                    'Status': 'Failed',
                    'Inbox Count': 0,
                    'Sent Count': 0,
                    'Error': f"File error: {str(e)}"
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
        
        with gr.Tab("OAuth2"):
            oauth2_files = gr.File(
                label="OAuth2 JSON Files",
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
        
        def test_all(app_passwords_text, oauth2_files):
            try:
                if not app_passwords_text.strip() and not oauth2_files:
                    return pd.DataFrame([{
                        'Email': 'Error',
                        'Auth Type': '',
                        'Status': 'No credentials provided',
                        'Inbox Count': '',
                        'Sent Count': '',
                        'Error': 'Please provide app passwords or OAuth2 files'
                    }])
                
                return process_credentials(app_passwords_text, oauth2_files)
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
            inputs=[app_passwords_input, oauth2_files],
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