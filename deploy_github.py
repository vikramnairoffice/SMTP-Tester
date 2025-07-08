#!/usr/bin/env python3
"""
GitHub deployment script for Gmail IMAP Credentials Checker.
Prepares the project for GitHub repository upload.
"""

import os
import shutil
import json
from pathlib import Path


def create_gitignore():
    """Create .gitignore file for the project."""
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# Project specific
*.log
/tmp/
.DS_Store
*.swp
*.swo
*~

# Gmail checker specific
/exported_emails/
/client_secrets/
*.json
!requirements.txt
!setup.py
!demo_test.py
!test_deployment.py

# Temporary files
gmail_check_*.csv
gmail_check_*.txt
oauth2_tokens/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore")


def create_github_readme():
    """Create GitHub-specific README.md."""
    github_readme = """# Gmail IMAP Credentials Checker

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-ready-brightgreen.svg)

A comprehensive tool for bulk Gmail credential validation supporting both **App Password** and **OAuth2** authentication methods. Optimized for Google Colab with a modern web interface.

## 🚀 Quick Start

### Google Colab (Recommended)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/gmail-imap-checker/blob/main/colab_deployment.ipynb)

1. **Clone and Setup**:
   ```python
   !git clone https://github.com/YOUR_USERNAME/gmail-imap-checker.git
   %cd gmail-imap-checker
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
git clone https://github.com/YOUR_USERNAME/gmail-imap-checker.git
cd gmail-imap-checker

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

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/gmail-imap-checker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/gmail-imap-checker/discussions)

## 🔗 Related Projects

- [Gmail API Python Client](https://github.com/googleapis/google-api-python-client)
- [Gradio](https://github.com/gradio-app/gradio)
- [Google Auth Library](https://github.com/googleapis/google-auth-library-python)

---

**⚠️ Security Notice**: This tool is for legitimate credential validation only. Always handle credentials securely and comply with applicable laws and regulations.
"""
    
    with open('README_GITHUB.md', 'w') as f:
        f.write(github_readme)
    print("✅ Created GitHub README")


def create_colab_notebook():
    """Create Google Colab deployment notebook."""
    notebook_content = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {
                "provenance": [],
                "collapsed_sections": []
            },
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Gmail IMAP Credentials Checker - Google Colab Deployment\\n",
                    "\\n",
                    "This notebook sets up and runs the Gmail IMAP Credentials Checker in Google Colab.\\n",
                    "\\n",
                    "## 🚀 Features\\n",
                    "- **App Password Authentication**: Validate Gmail app passwords\\n",
                    "- **OAuth2 Authentication**: Use Google Cloud client secrets\\n",
                    "- **Bulk Processing**: Handle multiple credentials at once\\n",
                    "- **Export Results**: Download CSV and summary reports\\n",
                    "\\n",
                    "## 📋 Prerequisites\\n",
                    "- Gmail account with 2FA enabled (for app passwords)\\n",
                    "- Google Cloud Console access (for OAuth2)\\n",
                    "- Valid credentials to test"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Step 1: Clone Repository and Install Dependencies"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Clone the repository\\n",
                    "!git clone https://github.com/YOUR_USERNAME/gmail-imap-checker.git\\n",
                    "%cd gmail-imap-checker\\n",
                    "\\n",
                    "# Install dependencies\\n",
                    "!python setup.py"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Step 2: Launch the Application"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Launch the Gmail IMAP Credentials Checker\\n",
                    "!python main.py"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📋 Usage Instructions\\n",
                    "\\n",
                    "1. **Click the public Gradio link** that appears above\\n",
                    "2. **For App Passwords**: Enter credentials in format `email:password`\\n",
                    "3. **For OAuth2**: Upload JSON client secret files\\n",
                    "4. **Click Process Credentials** to start validation\\n",
                    "5. **For OAuth2**: Check this cell output for authorization links\\n",
                    "6. **Download Results**: Use the download buttons for CSV/summary\\n",
                    "\\n",
                    "## ⚠️ Important Notes\\n",
                    "\\n",
                    "- **OAuth2 Authentication**: Authorization links will appear in this cell output\\n",
                    "- **Security**: Never share your credentials or client secrets\\n",
                    "- **Rate Limits**: Process credentials in reasonable batches\\n",
                    "- **Debug Info**: Check cell output for detailed error messages"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🛠️ Troubleshooting\\n",
                    "\\n",
                    "If you encounter issues, run the diagnostic tests below:"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Run diagnostic tests\\n",
                    "!python test_deployment.py"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Run demo with mock data\\n",
                    "!python demo_test.py"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Check debug logs\\n",
                    "!cat /tmp/gmail_checker_debug.log"
                ]
            }
        ]
    }
    
    with open('colab_deployment.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=2)
    print("✅ Created Colab deployment notebook")


def create_license():
    """Create MIT License file."""
    license_content = """MIT License

Copyright (c) 2025 Gmail IMAP Checker Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open('LICENSE', 'w') as f:
        f.write(license_content)
    print("✅ Created LICENSE file")


def create_contributing_guide():
    """Create contributing guidelines."""
    contributing_content = """# Contributing to Gmail IMAP Credentials Checker

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues
1. Check existing issues to avoid duplicates
2. Use the issue template
3. Provide detailed reproduction steps
4. Include debug logs and system information

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes following our guidelines
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Maximum 150 lines per file
- Use type hints for all functions
- Add comprehensive docstrings

### Architecture Principles
- Single Responsibility Principle
- Modular design with clear interfaces
- Minimal coupling between modules
- Comprehensive error handling

### Testing
- Add unit tests for new features
- Ensure all tests pass
- Include integration tests
- Test in both local and Colab environments

## 🔧 Development Setup

### Local Development
```bash
git clone https://github.com/YOUR_USERNAME/gmail-imap-checker.git
cd gmail-imap-checker
pip install -r requirements.txt
python test_deployment.py
```

### Running Tests
```bash
python test_deployment.py    # Full deployment test
python demo_test.py          # Demo with mock data
```

## 📋 Pull Request Process

1. **Update Documentation**: Ensure README and docs are updated
2. **Add Tests**: Include tests for new functionality
3. **Check Compatibility**: Test in both local and Colab environments
4. **Follow Conventions**: Maintain coding style and architecture
5. **Provide Context**: Explain changes in PR description

## 🐛 Issue Templates

### Bug Report
```
**Environment:**
- Platform: [Colab/Local]
- Python Version: [3.x.x]

**Description:**
[Clear description of the bug]

**Reproduction Steps:**
1. [Step 1]
2. [Step 2]

**Expected vs Actual Behavior:**
[What should happen vs what actually happens]

**Debug Information:**
[Console output and debug logs]
```

### Feature Request
```
**Feature Description:**
[Clear description of the proposed feature]

**Use Case:**
[Why this feature would be useful]

**Proposed Implementation:**
[High-level approach if you have ideas]
```

## 📚 Documentation Standards

- Update README.md for user-facing changes
- Update TROUBLESHOOTING.md for new issues/solutions
- Add docstrings for all new functions
- Include code examples in documentation

## 🔒 Security Guidelines

- Never commit credentials or API keys
- Handle sensitive data securely
- Follow OAuth2 best practices
- Validate all user inputs

## 📞 Getting Help

- **Questions**: Use GitHub Discussions
- **Issues**: Create GitHub Issues
- **Security**: Email maintainers privately

## 🎯 Contribution Areas

We welcome contributions in these areas:

- **Bug Fixes**: Resolve existing issues
- **Features**: Add new authentication methods
- **Documentation**: Improve guides and examples
- **Testing**: Add comprehensive test coverage
- **Performance**: Optimize processing speed
- **UI/UX**: Enhance user interface

## 👥 Recognition

Contributors will be:
- Listed in the repository contributors
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to make this project better! 🚀
"""
    
    with open('CONTRIBUTING.md', 'w') as f:
        f.write(contributing_content)
    print("✅ Created CONTRIBUTING.md")


def main():
    """Main deployment preparation function."""
    print("🚀 Preparing Gmail IMAP Credentials Checker for GitHub deployment...")
    print("=" * 70)
    
    # Create all deployment files
    create_gitignore()
    create_github_readme()
    create_colab_notebook()
    create_license()
    create_contributing_guide()
    
    print("\n" + "=" * 70)
    print("✅ GitHub deployment preparation complete!")
    print("\n📋 Next Steps:")
    print("1. Create new GitHub repository")
    print("2. Upload all project files")
    print("3. Update repository URL in README_GITHUB.md")
    print("4. Update Colab notebook with correct repository URL")
    print("5. Test deployment in Colab")
    
    print("\n📁 Files created for GitHub deployment:")
    files_created = [
        ".gitignore",
        "README_GITHUB.md", 
        "colab_deployment.ipynb",
        "LICENSE",
        "CONTRIBUTING.md"
    ]
    
    for file in files_created:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
    
    print("\n🎯 Ready for GitHub deployment!")


if __name__ == "__main__":
    main()