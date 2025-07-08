# Contributing to Gmail IMAP Credentials Checker

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
