# Gmail IMAP Credentials Checker

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-ready-brightgreen.svg)

A comprehensive tool for bulk Gmail credential validation supporting both **App Password** and **OAuth2** authentication methods. Optimized for Google Colab with a modern web interface.

## 🚀 Quick Start

### Google Colab (Recommended)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vikramnairoffice/SMTP-Tester/blob/main/colab_deployment.ipynb)

1. **Clone and Setup**:
   ```python
   !git clone https://github.com/vikramnairoffice/SMTP-Tester.git
   %cd SMTP-Tester
   !python setup.py
   ```

2. **Launch Application**:
   ```python
   !python main.py
   ```

3. **Access Interface**: Click the public Gradio link that appears

### Local Installation

```bash
# Clone repository
git clone https://github.com/vikramnairoffice/SMTP-Tester.git
cd SMTP-Tester

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 📋 Features

- ✅ **Dual Authentication**: App passwords and OAuth2 client secrets
- ✅ **Bulk Processing**: Handle multiple credentials simultaneously  
- ✅ **Google Colab Optimized**: Seamless OAuth2 flow in Colab environment
- ✅ **Email Counting**: Retrieve inbox and sent folder statistics
- ✅ **Export Functionality**: CSV and summary report generation
- ✅ **Real-time Progress**: Live status updates during processing
- ✅ **Comprehensive Logging**: Detailed debug information
- ✅ **Modular Architecture**: Clean, maintainable codebase

## 🔐 Authentication Methods

### App Password Method
```
Format: email@gmail.com:app_password
```

**Setup Steps**:
1. Enable 2FA on Gmail account
2. Generate app password in Google Account settings
3. Use 16-character app password in the tool

### OAuth2 Method
Upload JSON client secret files from Google Cloud Console.

**Setup Steps**:
1. Create project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Gmail API
3. Create OAuth2 Client ID (Desktop Application)
4. Download JSON file and upload to tool

## 📊 Screenshots

### Main Interface
![Main Interface](docs/images/main_interface.png)

### Processing Results
![Results](docs/images/results_table.png)

### OAuth2 Flow
![OAuth2](docs/images/oauth2_flow.png)

## 🛠️ Technical Architecture

```
gmail_checker/
├── core/                    # Authentication modules
│   ├── auth_manager.py     # Authentication abstraction
│   ├── app_password_auth.py # App password handler
│   ├── oauth2_auth.py      # OAuth2 handler
│   └── imap_connector.py   # IMAP operations
├── utils/                   # Utility modules
│   ├── credential_parser.py # Credential parsing
│   ├── email_counter.py    # Email counting
│   ├── file_handler.py     # File operations
│   └── debug_logger.py     # Debug logging
├── ui/                     # User interface
│   ├── gradio_interface.py # Main interface
│   └── ui_components.py    # UI components
├── models/                 # Data models
│   ├── credential_model.py # Credential structures
│   └── result_model.py     # Result structures
└── main.py                 # Entry point
```

## 🔧 Configuration

### Environment Variables
```bash
SKIP_INSTALL=1          # Skip dependency installation
DEBUG=1                 # Enable debug logging
```

### Requirements
- Python 3.8+
- Internet connection
- Google Cloud Console access (for OAuth2)

## 📈 Usage Examples

### Bulk App Password Validation
```
user1@gmail.com:abcdwxyzabcdwxyz
user2@gmail.com:efghijklmnopqrst  
user3@gmail.com:stuvwxyzstuvwxyz
```

### OAuth2 Client Secret
```json
{
  "installed": {
    "client_id": "123456789-abcdef.apps.googleusercontent.com",
    "project_id": "my-gmail-project",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "GOCSPX-abcdefghijklmnop",
    "redirect_uris": ["http://localhost"]
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **OAuth2 Authentication**:
   - Check Colab cell output for authorization links
   - Ensure client secret is for "Desktop Application"
   - Verify Gmail API is enabled

2. **App Password Errors**:
   - Confirm 2FA is enabled
   - Generate new app password
   - Check IMAP settings in Gmail

3. **Import Errors**:
   ```python
   !pip install -r requirements.txt
   ```

### Debug Information
- Console output with detailed logging
- Debug log file: `/tmp/gmail_checker_debug.log`
- System information and module versions

For comprehensive troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [API Reference](docs/api_reference.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## 🧪 Testing

```bash
# Run all tests
python test_deployment.py

# Run demo with mock data
python demo_test.py
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Maximum 150 lines per file
- Add comprehensive tests
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Support

If you find this project helpful, please consider giving it a star! ⭐

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/vikramnairoffice/SMTP-Tester/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vikramnairoffice/SMTP-Tester/discussions)

## 🔗 Related Projects

- [Gmail API Python Client](https://github.com/googleapis/google-api-python-client)
- [Gradio](https://github.com/gradio-app/gradio)
- [Google Auth Library](https://github.com/googleapis/google-auth-library-python)

---

**⚠️ Security Notice**: This tool is for legitimate credential validation only. Always handle credentials securely and comply with applicable laws and regulations.
