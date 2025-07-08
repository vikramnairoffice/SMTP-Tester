# GMAIL IMAP CREDENTIALS CHECKER

### Strictly follow these rules and guidelines

1. **STRICT PROHIBITION**: Under no circumstances should any additional features, functions, or code be autonomously implemented. All development must be explicitly authorized and directed by the project lead. This includes but is not limited to:
   - No automated code generation
   - No feature implementation without explicit instruction
   - No architectural modifications beyond specified requirements
   - No addition of dependencies or libraries without prior approval

2. **MODULAR ARCHITECTURE**: Maintain strict adherence to Single Responsibility Principle (SRP) with the following constraints:
   - Maximum file size: 150 LoC (excluding comments and tests)
   - Each module/class must serve exactly one purpose
   - Interfaces should be clearly defined with minimal coupling
   - Exceptions to line limits require explicit justification in code comments

3. **MINIMUM VIABLE PRODUCT (MVP) SCOPE**:
   - Focus exclusively on core functionality as specified in requirements
   - Security features (authentication, authorization, encryption) are out of scope
   - Deployment configurations and infrastructure code are excluded
   - Performance optimizations are deferred unless critical to MVP functionality

4. **DOCUMENTATION & VERSION CONTROL**:
   - Maintain strict synchronization between code and documentation
   - Document all architectural decisions in ARCHITECTURE.md
   - Update CHANGELOG.md for all modifications following Semantic Versioning
   - Ensure all commits reference relevant documentation updates

5. **DEVELOPMENT WORKFLOW**:
   - Implement one atomic feature/change at a time
   - Write and pass unit tests before proceeding to next task
   - Verify functionality in isolation before integration
   - Obtain explicit confirmation of successful implementation before continuing

6. **LEAN DEVELOPMENT PRINCIPLES**:
   - **Be Lean**: Eliminate all non-essential code and features
   - **Be Intentional**: Every line of code must serve a clear, defined purpose
   - Favor simplicity and readability over clever solutions
   - Remove unused or redundant code immediately
   - Optimize only when performance metrics indicate a need

### Technical Environment Specifications

#### Frontend Implementation
- Frontend components will be implemented with minimal viable functionality
- No UI/UX enhancements beyond basic functionality without explicit requirements
- Interactive elements will be limited to essential user inputs only
- No responsive design implementation unless specifically requested

#### Execution Environment
- Primary target platform: Cloud-based Jupyter environments (Google Colab, Kaggle Kernels, etc.)
- No server-side rendering or backend services required
- All code must be executable in a single runtime environment
- External service dependencies must be clearly documented and kept to a minimum
- Assume stateless execution unless otherwise specified
- Memory and compute constraints typical of free-tier cloud notebook environments apply

## Project Description

A Gmail IMAP credentials validation tool designed for bulk authentication testing and email counting. The application supports both traditional app password authentication and OAuth2 client secret authentication methods, providing a unified interface for checking Gmail account accessibility and retrieving basic email statistics.

**Core Functionality:**
- Bulk validation of Gmail credentials (app passwords and OAuth2 client secrets)
- Email counting from INBOX and Sent folders
- Export functionality for email data
- Web-based interface optimized for Google Colab environment

**Target Audience:** Security professionals, system administrators, and developers who need to validate Gmail account accessibility in bulk operations.

**Key Differentiators:**
- Dual authentication support (app passwords + OAuth2)
- Google Colab optimized OAuth2 flow
- Bulk processing capabilities
- Lightweight, single-session execution model

## Technical Architecture

### Module Structure (Modular Design)

```
gmail_checker/
├── core/
│   ├── __init__.py
│   ├── auth_manager.py          # Authentication abstraction layer
│   ├── app_password_auth.py     # App password authentication
│   ├── oauth2_auth.py           # OAuth2 authentication
│   └── imap_connector.py        # IMAP connection handling
├── utils/
│   ├── __init__.py
│   ├── credential_parser.py     # Credential parsing and validation
│   ├── email_counter.py         # Email counting functionality
│   └── file_handler.py          # File upload/download operations
├── ui/
│   ├── __init__.py
│   ├── gradio_interface.py      # Main UI components
│   └── ui_components.py         # Reusable UI elements
├── models/
│   ├── __init__.py
│   ├── credential_model.py      # Data structures for credentials
│   └── result_model.py          # Result data structures
└── main.py                      # Entry point
```

### Authentication Flow Architecture

#### App Password Authentication
1. Parse `email:password` format
2. Connect via `imaplib.IMAP4_SSL`
3. Authenticate using standard login
4. Count emails and return results

#### OAuth2 Authentication Flow
1. Parse JSON client secret file
2. Initialize `InstalledAppFlow` with Gmail IMAP scope
3. Execute `run_local_server()` for Colab-compatible authentication
4. Extract user email using Google People API
5. Generate XOAUTH2 SASL authentication string
6. Connect to IMAP using OAuth2 tokens
7. Count emails and return results

### Key Technical Components

#### OAuth2 Implementation Details
- **Scope**: `https://mail.google.com/` (full Gmail access)
- **Flow Type**: `InstalledAppFlow` with `run_local_server()`
- **Authentication Method**: XOAUTH2 SASL for IMAP
- **Token Management**: Session-based with automatic refresh
- **User Email Extraction**: Google People API v1

#### IMAP Connection Specifications
- **Server**: `imap.gmail.com:993` (SSL)
- **Authentication Methods**: 
  - Standard LOGIN for app passwords
  - XOAUTH2 SASL for OAuth2 tokens
- **Folder Access**: INBOX, "[Gmail]/Sent Mail"
- **Operation**: Read-only email counting

#### Data Models

**Credential Model:**
```python
{
    'type': 'app_password' | 'oauth2',
    'email': str,
    'auth_data': str | dict,  # password string or OAuth2 credentials
    'status': 'pending' | 'authenticated' | 'failed'
}
```

**Result Model:**
```python
{
    'email': str,
    'auth_type': str,
    'status': 'success' | 'failed',
    'inbox_count': int,
    'sent_count': int,
    'error_message': str,
    'timestamp': datetime
}
```

### Dependencies

**Core Dependencies:**
- `gradio` - Web interface framework
- `imaplib` - IMAP protocol implementation (built-in)
- `email` - Email parsing utilities (built-in)
- `pandas` - Data manipulation for results

**OAuth2 Dependencies:**
- `google-auth` - Google authentication library
- `google-auth-oauthlib` - OAuth2 flow implementation
- `google-auth-httplib2` - HTTP transport for Google APIs
- `google-api-python-client` - Google APIs client library

**Utility Dependencies:**
- `json` - JSON parsing (built-in)
- `base64` - Base64 encoding for XOAUTH2 (built-in)
- `logging` - Logging framework (built-in)
- `tqdm` - Progress bars

### Error Handling Strategy

**Authentication Errors:**
- Invalid credentials: Clear error message with retry option
- OAuth2 flow failures: Detailed error reporting with troubleshooting steps
- Network connectivity: Timeout handling with retry mechanisms

**IMAP Connection Errors:**
- Connection timeouts: Configurable retry attempts
- Server unavailability: Graceful degradation
- Permission issues: Clear error messages

**File Processing Errors:**
- Invalid JSON format: Validation with specific error messages
- Missing required fields: Field-level validation
- File upload failures: User-friendly error reporting

### Performance Considerations

**Bulk Processing:**
- Sequential OAuth2 authentication to avoid conflicts
- Concurrent IMAP connections for app password validation
- Progress tracking for user feedback
- Memory efficient result storage

**Google Colab Optimizations:**
- Minimal memory footprint
- Session-based token storage
- Efficient file handling for uploads/downloads
- Responsive UI updates during long operations

### Security Considerations

**Credential Handling:**
- No persistent storage of credentials
- Secure token management in memory
- Automatic token cleanup after session
- Clear separation of authentication methods

**Data Privacy:**
- Read-only IMAP operations
- No email content access beyond counting
- Temporary file handling for exports
- Clear data lifecycle management

### Current Implementation Status

**Completed:**
- Basic app password authentication
- IMAP connection and email counting
- Gradio interface framework
- Export functionality

**In Progress:**
- OAuth2 authentication module
- Bulk processing capabilities
- Enhanced error handling

**Planned:**
- Modular architecture refactoring
- Comprehensive testing suite
- Performance optimizations
- Documentation completion

### Development Guidelines

**Code Style:**
- Follow PEP 8 style guidelines
- Maximum line length: 88 characters
- Type hints for all function parameters and return values
- Docstrings for all public functions and classes

**Testing Requirements:**
- Unit tests for each module
- Integration tests for authentication flows
- Mock testing for external API calls
- Error scenario testing

**Documentation Standards:**
- Inline code comments for complex logic
- Module-level docstrings
- API documentation for public interfaces
- User guide for setup and usage

### Deployment Instructions

**Google Colab Setup:**
1. Install required dependencies using `!pip install`
2. Upload client secret JSON files using Colab file upload
3. Run the main application script
4. Access the Gradio interface via the provided public URL

**Local Development:**
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`
4. Access the local Gradio interface

### Troubleshooting Guide

**Common OAuth2 Issues:**
- "Redirect URI mismatch": Ensure client secret is configured for installed app
- "Scope not authorized": Verify Gmail API is enabled in Google Cloud Console
- "Authentication timeout": Check browser popup blockers

**IMAP Connection Issues:**
- "Login failed": Verify 2FA is enabled and app password is correct
- "Connection timeout": Check network connectivity and firewall settings
- "Permission denied": Ensure IMAP is enabled in Gmail settings

### API Reference

**Authentication Manager:**
- `authenticate_app_password(email, password)` → `AuthResult`
- `authenticate_oauth2(client_secret_data)` → `AuthResult`
- `refresh_oauth2_token(credentials)` → `RefreshResult`

**IMAP Connector:**
- `connect_with_app_password(email, password)` → `IMAPConnection`
- `connect_with_oauth2(email, credentials)` → `IMAPConnection`
- `count_emails(connection, folder)` → `int`

**File Handler:**
- `parse_client_secret(json_data)` → `ClientSecretData`
- `export_results(results, format)` → `str`
- `validate_credentials_format(data)` → `bool`

### Version History

**v1.0.0 (Current)**
- Initial implementation with app password support
- Basic Gradio interface
- Email counting functionality
- Export capabilities

**v1.1.0 (Planned)**
- OAuth2 authentication integration
- Modular architecture implementation
- Enhanced error handling
- Bulk processing optimization

### Contributing Guidelines

**Development Process:**
1. Create feature branch from main
2. Implement changes following architecture guidelines
3. Write comprehensive tests
4. Update documentation
5. Submit pull request with detailed description

**Code Review Requirements:**
- All code must pass automated tests
- Documentation must be updated
- Performance impact must be evaluated
- Security implications must be assessed

### License and Legal

**Usage Rights:**
- Internal use only
- No commercial redistribution
- Compliance with Google API Terms of Service
- Respect for user privacy and data protection

**Disclaimer:**
This tool is provided for legitimate credential validation purposes only. Users are responsible for ensuring compliance with applicable laws and regulations regarding email access and authentication testing.