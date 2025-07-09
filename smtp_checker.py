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

if IN_COLAB:
    try:
        from google.colab import auth
    except ImportError:
        print("Attempting to install google.colab.auth, please restart runtime if it fails.")
        os.system("pip install google-colab") # Should be part of Colab's base but just in case
        from google.colab import auth


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

# Global variable to store Colab credentials
colab_credentials = None

def authenticate_colab_user():
    """Authenticates the Colab user and stores credentials."""
    global colab_credentials
    if IN_COLAB:
        try:
            auth.authenticate_user()
            colab_credentials = auth.default()[0] # auth.default() returns (credentials, project_id)
            print("Colab user authenticated successfully.")
            return colab_credentials
        except Exception as e:
            print(f"Error during Colab authentication: {e}")
            colab_credentials = None
            return None
    else:
        print("Not in Colab environment. Skipping Colab authentication.")
        return None

gmail_service = None

def get_gmail_service():
    """Builds and returns a Gmail API service client using Colab credentials."""
    global gmail_service, colab_credentials
    if colab_credentials:
        try:
            if gmail_service is None: # Build only if not already built
                gmail_service = build('gmail', 'v1', credentials=colab_credentials)
                print("Gmail API service built successfully.")
            return gmail_service
        except Exception as e:
            print(f"Error building Gmail API service: {e}")
            return None
    else:
        print("Colab credentials not available. Cannot build Gmail API service.")
        return None

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

def get_email_counts_gmail_api(service, user_id='me'):
    """Gets inbox and sent email counts using Gmail API."""
    inbox_count = 0
    sent_count = 0
    error = ""
    try:
        # Get Inbox count
        inbox_response = service.users().messages().list(userId=user_id, labelIds=['INBOX'], maxResults=1).execute()
        inbox_count = inbox_response.get('resultSizeEstimate', 0)

        # Get Sent count
        sent_response = service.users().messages().list(userId=user_id, labelIds=['SENT'], maxResults=1).execute()
        sent_count = sent_response.get('resultSizeEstimate', 0)

        return True, inbox_count, sent_count, ""
    except Exception as e:
        error_message = f"Gmail API error: {str(e)}"
        # Check if the error is related to permissions or API not enabled
        if "accessNotConfigured" in str(e) or "USER_ACCESS_DENIED" in str(e) or "disabled" in str(e).lower():
            error_message += ("\nPossible reason: Gmail API not enabled for your project in Google Cloud Console, "
                              "or required scopes were not granted during authentication.")
        elif "Invalid grant" in str(e) or "Token has been expired or revoked" in str(e):
             error_message += ("\nPossible reason: Authentication token is invalid or expired. "
                               "Please try re-authenticating.")
        return False, 0, 0, error_message

def process_credentials_v2(app_passwords_text, oauth2_credentials, oauth2_files):
    """Process both app passwords and OAuth2 credentials"""
    results = []
    
    # Process app passwords
    if app_passwords_text.strip():
        lines = app_passwords_text.strip().split('\n')
        for line in tqdm(lines, desc="Testing App Passwords"):
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

    # Process Colab Authenticated User (if applicable)
    # This takes precedence over the old "OAuth2 credentials with passwords" if in Colab and authenticated
    if IN_COLAB and colab_credentials:
        # This section is triggered if no app passwords are provided,
        # implying the user wants to test the Colab authenticated account.
        # The `oauth2_credentials` text field is not used for this flow.
        if not app_passwords_text.strip(): # Only run if not also doing app passwords
            print("Processing Colab authenticated user...")
            service = get_gmail_service()
            if service:
                success, inbox_count, sent_count, error = get_email_counts_gmail_api(service)
                # Try to get the user's email for display, might not always be available directly
                user_email = "Authenticated Colab User"
                try:
                    profile = service.users().getProfile(userId='me').execute()
                    user_email = profile.get('emailAddress', user_email)
                except Exception as e:
                    print(f"Could not fetch email address for Colab user: {e}")

                results.append({
                    'Email': user_email,
                    'Auth Type': 'OAuth2 (Colab)',
                    'Status': 'Success' if success else 'Failed',
                    'Inbox Count': inbox_count,
                    'Sent Count': sent_count,
                    'Error': error
                })
            else:
                results.append({
                    'Email': 'Authenticated Colab User',
                    'Auth Type': 'OAuth2 (Colab)',
                    'Status': 'Failed',
                    'Inbox Count': 0,
                    'Sent Count': 0,
                    'Error': 'Gmail service not available. Authenticate first or check errors.'
                })
    
    # Process OAuth2 credentials with passwords (legacy, for non-Colab or if Colab auth not used)
    elif oauth2_credentials.strip(): # Note: 'elif' so it doesn't run if Colab OAuth2 above ran
        lines = oauth2_credentials.strip().split('\n')
        client_secret_data = None # Not used by test_oauth2_with_password as it is
        if oauth2_files: # Retaining file handling logic though not used by current test_oauth2_with_password
            try:
                file = oauth2_files[0]
                if hasattr(file, 'name'): # Gradio file object
                    with open(file.name, 'r') as f:
                        client_secret_data = json.load(f)
                # else: could be BytesIO if file is passed differently, handle if necessary
            except Exception as e:
                print(f"Error reading OAuth2 JSON file: {e}")
                pass # Continue without client_secret_data if file reading fails
        
        for line in tqdm(lines, desc="Testing OAuth2 with Email/Password (IMAP Fallback)"):
            if ':' in line:
                email, password = line.split(':', 1)
                email = email.strip()
                password = password.strip()
                
                # This function currently attempts IMAP login or returns error.
                success, email_result, inbox_count, sent_count, error = test_oauth2_with_password(client_secret_data, email, password)
                
                results.append({
                    'Email': email_result,
                    'Auth Type': 'OAuth2 (Legacy/IMAP)',
                    'Status': 'Success' if success else 'Failed',
                    'Inbox Count': inbox_count,
                    'Sent Count': sent_count,
                    'Error': error
                })
    
    if not results: # If no inputs were processed
        return pd.DataFrame([{
            'Email': 'Info',
            'Auth Type': '',
            'Status': 'No operations performed.',
            'Inbox Count': '',
            'Sent Count': '',
            'Error': 'Provide App Passwords or use Colab Authenticate & Test.'
        }])

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
        gr.Markdown("Test Gmail credentials. For Colab, use the 'Authenticate' button for OAuth2.")

        colab_auth_status = gr.Textbox(label="Colab Auth Status", interactive=False, placeholder="Not authenticated")

        if IN_COLAB:
            with gr.Row():
                colab_auth_button = gr.Button("Authenticate Current Google User (Colab)")
        
        with gr.Tab("App Passwords"):
            app_passwords_input = gr.Textbox(
                label="App Passwords (one per line)",
                placeholder="email1@gmail.com:password1\nemail2@gmail.com:password2",
                lines=10
            )
        
        with gr.Tab("OAuth2 + Passwords"):
            gr.Markdown(
                "**For Colab**: After clicking 'Authenticate Current Google User (Colab)' above, "
                "you can click 'Test Credentials' (with App Passwords empty) to check the authenticated account. "
                "The text box below is for legacy email:password IMAP fallback (non-Colab or if Colab auth not used)."
            )
            oauth2_credentials = gr.Textbox(
                label="Legacy OAuth2 Credentials (email:password format)",
                placeholder="email1@gmail.com:password1\nemail2@gmail.com:password2 (Uses IMAP fallback)",
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

        def colab_auth_and_update_status():
            global colab_credentials, gmail_service
            creds = authenticate_colab_user()
            if creds:
                # Attempt to build the service right after auth
                service = get_gmail_service()
                if service:
                    return "Authenticated and Gmail service ready."
                else:
                    return "Authenticated, but Gmail service failed to build. Check console for errors."
            return "Authentication failed. Check console for errors."

        if IN_COLAB:
            colab_auth_button.click(
                fn=colab_auth_and_update_status,
                inputs=[],
                outputs=[colab_auth_status]
            )
        
        def test_all(app_passwords_text, oauth2_credentials, oauth2_files):
            try:
                # Determine if a Colab OAuth2 test should be run for the authenticated user.
                # This happens if:
                # 1. We are in Colab.
                # 2. Colab credentials exist (user has authenticated).
                # 3. No app passwords are being tested (to avoid mixing test types in one run).
                # The `oauth2_credentials` text box is NOT used for this specific flow's input.
                run_colab_oauth_test = IN_COLAB and colab_credentials and not app_passwords_text.strip()

                # Check if any operation can be performed
                can_perform_app_pass_test = app_passwords_text.strip()
                can_perform_legacy_oauth_test = oauth2_credentials.strip() # For the old email:pass IMAP style

                if not can_perform_app_pass_test and not run_colab_oauth_test and not can_perform_legacy_oauth_test:
                     return pd.DataFrame([{
                        'Email': 'Error',
                        'Auth Type': '',
                        'Status': 'No operation to perform',
                        'Inbox Count': '',
                        'Sent Count': '',
                        'Error': 'Please provide app passwords, or use Colab Authenticate button (then Test Credentials), or provide legacy OAuth2 email:password.'
                    }])
                
                # Call process_credentials_v2. It will internally decide what to do based on inputs
                # and Colab auth state.
                return process_credentials_v2(app_passwords_text, oauth2_credentials, oauth2_files)
            except Exception as e:
                traceback.print_exc() # Print full traceback to console for debugging
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