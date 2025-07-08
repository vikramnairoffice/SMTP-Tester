# Gmail SMTP Checker

Simple tool for bulk testing Gmail credentials using app passwords and OAuth2.

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the checker:
```bash
python smtp_checker.py
```

3. Open the Gradio interface and:
   - **App Passwords**: Enter `email:password` format (one per line)
   - **OAuth2**: Upload JSON client secret files

## Features

- Bulk testing of Gmail credentials
- Support for app passwords and OAuth2
- Email count (inbox/sent)
- CSV export of results
- Simple web interface

## Requirements

- Python 3.6+
- Gmail accounts with 2FA enabled (for app passwords)
- OAuth2 client secrets (for OAuth2 testing)