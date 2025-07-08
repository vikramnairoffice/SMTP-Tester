# Gmail IMAP Credentials Checker - Troubleshooting Guide

## 🔧 Debug Features

### Enhanced Logging
The system now includes comprehensive debugging features:

- **Debug Logger**: Detailed logging with function call tracking
- **Error Context**: Full stack traces with contextual information
- **System Information**: Python version, environment, and module versions
- **Log File**: Persistent logging to `/tmp/gmail_checker_debug.log`

### Debug Log Locations
- **Console Output**: Real-time debug information
- **Log File**: `/tmp/gmail_checker_debug.log` (persistent)
- **Colab Output**: Check cell output for OAuth2 authentication links

## 🚨 Common Issues and Solutions

### 1. Import Errors

**Error**: `ModuleNotFoundError: No module named 'google_auth_oauthlib'`

**Solution**:
```python
# In Colab
!pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client gradio pandas tqdm

# Local environment
pip install -r requirements.txt
```

**Debug Info**: Check module versions in debug log

### 2. OAuth2 Authentication Issues

**Error**: `Redirect URI mismatch` or `Invalid client`

**Solution**:
1. Ensure client secret is for "Desktop Application" type
2. Check `redirect_uris` includes `"http://localhost"`
3. Verify Gmail API is enabled in Google Cloud Console

**Debug Info**: OAuth2 flow details logged with full context

**Example Client Secret Format**:
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

### 3. App Password Authentication Issues

**Error**: `Invalid credentials` or `Authentication failed`

**Solution**:
1. Verify 2FA is enabled on Gmail account
2. Generate new 16-character app password
3. Use format: `email@gmail.com:apppasswordhere`
4. Ensure IMAP is enabled in Gmail settings

**Debug Info**: Authentication attempts logged with credential type

### 4. Gradio Interface Issues

**Error**: Interface doesn't load or shows errors

**Solutions**:
- Check console output for detailed error messages
- Verify all dependencies are installed
- Check debug log for UI component creation errors

**Debug Info**: Interface creation and event handling logged

### 5. File Upload Issues

**Error**: OAuth2 JSON files not parsing correctly

**Solution**:
1. Ensure files are valid JSON format
2. Check file contains `"installed"` section
3. Verify all required fields are present

**Debug Info**: File parsing errors logged with file details

## 📋 Debug Information Collection

### For Bug Reports, Provide:

1. **Console Output**: Copy full console output
2. **Debug Log**: Contents of `/tmp/gmail_checker_debug.log`
3. **System Info**: Python version, OS, environment
4. **Steps to Reproduce**: Exact steps that caused the error
5. **Input Data**: Sanitized examples (remove sensitive data)

### Accessing Debug Information

**Console Output**:
```python
# All debug info is printed to console
# Look for timestamps and detailed error messages
```

**Debug Log File**:
```python
# Check log file location
from gmail_checker.utils.debug_logger import debug_logger
print(debug_logger.get_log_file_path())

# Or manually check:
with open('/tmp/gmail_checker_debug.log', 'r') as f:
    print(f.read())
```

**System Information**:
```python
from gmail_checker.utils.debug_logger import debug_logger
debug_logger.log_system_info()
debug_logger.log_module_versions()
```

## 🔍 Debugging Steps

### Step 1: Check Basic Functionality
```python
# Test import and basic functionality
python3 test_deployment.py
```

### Step 2: Check Dependencies
```python
# Verify all modules import correctly
python3 -c "
from gmail_checker.utils.debug_logger import debug_logger
debug_logger.log_module_versions()
"
```

### Step 3: Test with Mock Data
```python
# Run demo with mock data
python3 demo_test.py
```

### Step 4: Enable Debug Mode
```python
# Set environment variable for detailed logging
export DEBUG=1
python3 main.py
```

## 🐛 Known Issues

### Issue 1: Google Colab OAuth2 Popups
**Symptom**: OAuth2 authentication doesn't open browser window
**Solution**: Check Colab cell output for authorization links to click manually

### Issue 2: Large File Uploads in Colab
**Symptom**: Multiple JSON files upload slowly
**Solution**: Upload files in smaller batches (5-10 at a time)

### Issue 3: Token Refresh Errors
**Symptom**: OAuth2 tokens expire during processing
**Solution**: Tokens are automatically refreshed; check debug log for refresh attempts

## 📞 Getting Help

### Before Reporting Issues:

1. **Run Diagnostic Tests**:
   ```python
   python3 test_deployment.py
   python3 demo_test.py
   ```

2. **Check Debug Logs**:
   ```python
   cat /tmp/gmail_checker_debug.log
   ```

3. **Verify Environment**:
   ```python
   python3 -c "
   import sys
   print('Python:', sys.version)
   print('Platform:', sys.platform)
   "
   ```

### Issue Template:

```
**Environment:**
- Platform: [Google Colab/Local/Other]
- Python Version: [3.x.x]
- Browser: [Chrome/Firefox/Safari]

**Issue Description:**
[Detailed description of the problem]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages:**
[Copy console output and error messages]

**Debug Log:**
[Contents of /tmp/gmail_checker_debug.log]

**Additional Context:**
[Any other relevant information]
```

## 🛠️ Advanced Debugging

### Enable Verbose Logging:
```python
import logging
from gmail_checker.utils.debug_logger import DebugLogger

# Create debug logger with highest verbosity
debug_logger = DebugLogger(log_level=logging.DEBUG)
```

### Monitor Function Calls:
```python
# All major functions are decorated with @log_function_call
# Check debug log for function entry/exit with timing
```

### Custom Debug Context:
```python
from gmail_checker.utils.debug_logger import debug_logger

# Add custom context to any operation
debug_logger.info("Custom operation", {
    'user_id': 'test_user',
    'operation': 'credential_validation',
    'count': 5
})
```

This comprehensive debugging system ensures that any issues can be quickly identified and resolved with detailed diagnostic information.