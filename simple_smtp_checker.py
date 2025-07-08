import imaplib
import email
from email.header import decode_header
import os
import zipfile
import tempfile
import json
from tqdm import tqdm
import gradio as gr
import pandas as pd
import logging
import traceback
import sys
import base64

# OAuth2 imports - install if needed
try:
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import google.auth
except ImportError:
    print("Installing OAuth2 dependencies...")
    os.system("pip install google-auth google-auth-oauthlib google-api-python-client")
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import google.auth

# Constants
IMAP_SERVER = "imap.gmail.com"
PORT = 993
OUTPUT_DIR = "exported_emails"
INBOX_FOLDER = "INBOX"
SENT_FOLDER = '"[Gmail]/Sent Mail"'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

def clean_subject(subject):
    try:
        decoded, charset = decode_header(subject)[0]
        if isinstance(decoded, bytes):
            return decoded.decode(charset if charset else 'utf-8', errors='ignore')
        return decoded
    except Exception as e:
        logging.error(f"Error decoding subject: {e}")
        return "No Subject"

def connect_to_gmail_app_password(email_user, app_password):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, PORT)
        mail.login(email_user, app_password)
        return mail
    except imaplib.IMAP4.error as e:
        if "Invalid credentials" in str(e):
            logging.error(f"Failed to connect to {email_user}: Invalid app password")
            return None
        else:
            logging.error(f"Failed to connect to {email_user}: {e}")
            return None

def connect_to_gmail_oauth2(credentials):
    try:
        # Refresh token if needed
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        
        # Get user email using People API
        service = build('people', 'v1', credentials=credentials)
        profile = service.people().get(resourceName='people/me', personFields='emailAddresses').execute()
        user_email = profile['emailAddresses'][0]['value']
        
        # Create XOAUTH2 string
        xoauth2_string = f"user={user_email}\x01auth=Bearer {credentials.token}\x01\x01"
        xoauth2_string = base64.b64encode(xoauth2_string.encode()).decode()
        
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, PORT)
        mail.authenticate('XOAUTH2', lambda x: xoauth2_string)
        return mail, user_email
    except Exception as e:
        logging.error(f"OAuth2 connection failed: {e}")
        return None, None

def get_mail_count(mail, folder=INBOX_FOLDER):
    try:
        mail.select(folder)
        result, data = mail.search(None, 'ALL')
        if result == 'OK':
            return len(data[0].split())
        else:
            return 0
    except Exception as e:
        logging.error(f"Failed to retrieve email count from {folder}: {e}")
        return 0

def process_account(account, export_emails=False):
    email_user = account.get('email', '')
    app_password = account.get('app_password', '')
    oauth2_data = account.get('oauth2_data', None)

    result = {
        'email': email_user,
        'inbox_count': 0,
        'sent_count': 0,
        'status': 'Success',
        'error': '',
        'auth_type': 'app_password' if app_password else 'oauth2'
    }

    try:
        mail = None
        
        if app_password:
            # App password authentication
            mail = connect_to_gmail_app_password(email_user, app_password)
            if not mail:
                result['status'] = 'Failed to Connect'
                result['error'] = 'Authentication failed. Please check your email and app password.'
                return result
        elif oauth2_data:
            # OAuth2 authentication
            SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/userinfo.email']
            flow = InstalledAppFlow.from_client_config(oauth2_data, SCOPES)
            credentials = flow.run_local_server(port=0, access_type='offline', prompt='consent')
            
            mail, email_user = connect_to_gmail_oauth2(credentials)
            if not mail:
                result['status'] = 'Failed to Connect'
                result['error'] = 'OAuth2 authentication failed.'
                return result
            result['email'] = email_user
        else:
            result['status'] = 'No Credentials'
            result['error'] = 'No app password or OAuth2 data provided.'
            return result

        inbox_count = get_mail_count(mail, INBOX_FOLDER)
        sent_count = get_mail_count(mail, SENT_FOLDER)

        result['inbox_count'] = inbox_count
        result['sent_count'] = sent_count

        mail.logout()
    except Exception as e:
        result['status'] = 'Error'
        result['error'] = f"An error occurred: {str(e)}"
        logging.error(f"Error processing account {email_user}: {str(e)}")

    return result

def parse_credentials(input_text):
    accounts = []
    lines = input_text.strip().split('\n')
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) != 2:
            raise ValueError(f"Line {idx} is malformed. Expected format: email,app_password. Got: {line}")
        email_addr = parts[0].strip()
        app_pwd = parts[1].strip()
        if not email_addr or not app_pwd:
            raise ValueError(f"Line {idx} has empty email or app password. Email: '{email_addr}', Password: '{app_pwd}'")
        if '@' not in email_addr:
            raise ValueError(f"Line {idx} contains an invalid email address: {email_addr}")
        accounts.append({'email': email_addr, 'app_password': app_pwd})
    return accounts

def parse_oauth2_files(files):
    accounts = []
    if not files:
        return accounts
    
    for file in files:
        try:
            with open(file.name, 'r') as f:
                oauth2_data = json.load(f)
            accounts.append({'oauth2_data': oauth2_data})
        except Exception as e:
            logging.error(f"Error parsing OAuth2 file {file.name}: {e}")
    return accounts

def process_accounts_interface(credentials_text, oauth2_files):
    all_accounts = []
    
    # Parse app password credentials
    if credentials_text.strip():
        try:
            app_password_accounts = parse_credentials(credentials_text)
            all_accounts.extend(app_password_accounts)
        except ValueError as ve:
            return {"Error": str(ve)}, None
    
    # Parse OAuth2 files
    oauth2_accounts = parse_oauth2_files(oauth2_files)
    all_accounts.extend(oauth2_accounts)
    
    if not all_accounts:
        return {"Error": "No credentials provided"}, None

    results = []
    for account in all_accounts:
        res = process_account(account)
        account_result = {
            'Email': res['email'],
            'Auth Type': res['auth_type'],
            'Inbox Count': res['inbox_count'],
            'Sent Count': res['sent_count'],
            'Status': res['status'],
            'Error': res['error']
        }
        results.append(account_result)

    return results, None

def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Gmail IMAP Credentials Checker")
        gr.Markdown(
            """
            Test Gmail credentials using either App Passwords or OAuth2 client secrets.
            
            **App Password Format**: email@gmail.com,app_password
            **OAuth2**: Upload JSON client secret files
            """
        )

        with gr.Tab("App Password Credentials"):
            credentials_input = gr.Textbox(
                label="Gmail Credentials",
                placeholder="email1@gmail.com,app_password1\nemail2@gmail.com,app_password2",
                lines=10
            )

        with gr.Tab("OAuth2 Credentials"):
            oauth2_files = gr.File(
                label="Upload OAuth2 JSON Files",
                file_count="multiple",
                file_types=[".json"]
            )

        run_button = gr.Button("Process Credentials")

        output_table = gr.Dataframe(
            headers=["Email", "Auth Type", "Inbox Count", "Sent Count", "Status", "Error"],
            label="Results",
            interactive=False
        )

        def process_accounts(credentials_text, oauth2_files):
            try:
                results, _ = process_accounts_interface(credentials_text, oauth2_files)

                if isinstance(results, dict) and 'Error' in results:
                    error_df = pd.DataFrame([{
                        'Email': 'Error', 
                        'Auth Type': '', 
                        'Inbox Count': '', 
                        'Sent Count': '', 
                        'Status': 'Error', 
                        'Error': results['Error']
                    }])
                    return error_df

                return pd.DataFrame(results)
            except Exception as e:
                error_message = f"An unexpected error occurred: {str(e)}\n{traceback.format_exc()}"
                logging.error(error_message)
                error_df = pd.DataFrame([{
                    'Email': 'Error', 
                    'Auth Type': '', 
                    'Inbox Count': '', 
                    'Sent Count': '', 
                    'Status': 'Error', 
                    'Error': error_message
                }])
                return error_df

        run_button.click(
            fn=process_accounts,
            inputs=[credentials_input, oauth2_files],
            outputs=[output_table]
        )

    return demo

# Launch the Gradio Interface
demo = create_gradio_interface()
demo.launch(share=True)