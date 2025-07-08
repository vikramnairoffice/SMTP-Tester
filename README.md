# Gmail IMAP Credentials Checker

A modular tool for bulk Gmail credential validation and email counting, supporting both App Password and OAuth2 authentication methods.

## Features

- **Dual Authentication Support**: App passwords and OAuth2 client secrets
- **Bulk Processing**: Handle multiple credentials simultaneously
- **Google Colab Optimized**: OAuth2 flow works seamlessly in Colab environment
- **Email Counting**: Count emails in Inbox and Sent folders
- **Export Functionality**: CSV and summary report generation
- **Modular Architecture**: Clean, maintainable code structure

## Quick Start (Google Colab)

1. **Upload files to Colab:**
   ```python
   # Upload the entire project folder to Colab
   ```

2. **Run setup:**
   ```python
   !python setup.py
   ```

3. **Start the application:**
   ```python
   !python main.py
   ```

4. **Access the interface:**
   - Click the public Gradio link in the output
   - The interface will open in a new tab

## Authentication Methods

### App Password Authentication

1. **Format**: `email@gmail.com:app_password`
2. **Setup**:
   - Enable 2FA on Gmail account
   - Generate app password in Google Account settings
   - Use the 16-character app password

### OAuth2 Authentication

1. **Setup Google Cloud Console**:
   - Create new project or select existing
   - Enable Gmail API
   - Create OAuth2 Client ID (Desktop Application)
   - Download JSON client secret file

2. **Usage**:
   - Upload JSON file(s) through the interface
   - Click "Process Credentials"
   - **Important**: Check Colab cell output for authentication links
   - Click the authorization link and complete OAuth2 flow

## Project Structure

```
gmail_checker/
├── core/                    # Core authentication modules
│   ├── auth_manager.py     # Authentication abstraction layer
│   ├── app_password_auth.py # App password authentication
│   ├── oauth2_auth.py      # OAuth2 authentication
│   └── imap_connector.py   # IMAP connection handling
├── utils/                   # Utility modules
│   ├── credential_parser.py # Credential parsing
│   ├── email_counter.py    # Email counting functionality
│   └── file_handler.py     # File operations
├── ui/                     # User interface modules
│   ├── gradio_interface.py # Main Gradio interface
│   └── ui_components.py    # Reusable UI components
├── models/                 # Data models
│   ├── credential_model.py # Credential data structures
│   └── result_model.py     # Result data structures
└── main.py                 # Application entry point
```

## Usage Examples

### App Password Example
```
user1@gmail.com:abcdwxyzabcdwxyz
user2@gmail.com:efghijklmnopqrst
```

### OAuth2 Client Secret Example
```json
{
  "installed": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

## Dependencies

- `gradio==3.41.2` - Web interface framework
- `google-auth` - Google authentication library
- `google-auth-oauthlib` - OAuth2 flow implementation
- `google-auth-httplib2` - HTTP transport for Google APIs
- `google-api-python-client` - Google APIs client library
- `pandas` - Data manipulation
- `tqdm` - Progress bars

## Troubleshooting

### Common OAuth2 Issues

1. **"Redirect URI mismatch"**:
   - Ensure client secret is configured for "Desktop Application"
   - Check that redirect_uris includes "http://localhost"

2. **"Scope not authorized"**:
   - Verify Gmail API is enabled in Google Cloud Console
   - Check OAuth2 consent screen configuration

3. **"Authentication timeout"**:
   - Check browser popup blockers
   - Ensure stable internet connection

### Common App Password Issues

1. **"Login failed"**:
   - Verify 2FA is enabled on Gmail account
   - Check app password is correct (16 characters)
   - Ensure IMAP is enabled in Gmail settings

2. **"Connection timeout"**:
   - Check network connectivity
   - Verify firewall settings

## Architecture Principles

- **Modular Design**: Each module has single responsibility
- **Maximum 150 LoC**: Per file limit for maintainability
- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging throughout

## Security Considerations

- **No Credential Storage**: Credentials are processed in memory only
- **Secure Token Handling**: OAuth2 tokens are properly managed
- **Read-Only Operations**: Only counts emails, no content access
- **Session-Based**: No persistent data storage

## Development Guidelines

1. **Follow PEP 8**: Python style guidelines
2. **Add Type Hints**: For all function parameters and returns
3. **Document Functions**: Comprehensive docstrings
4. **Test Thoroughly**: Unit and integration tests
5. **Keep Modules Small**: Maximum 150 lines per file

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

## License

This project is licensed under the MIT License. See LICENSE file for details.