"""
Enhanced debugging and logging utility.
Maximum 150 LoC as per architecture requirements.
"""

import logging
import traceback
import sys
import os
from datetime import datetime
from typing import Any, Dict, Optional


class DebugLogger:
    """
    Enhanced debugging logger with detailed error tracking.
    
    Provides comprehensive logging for troubleshooting and error analysis.
    """
    
    def __init__(self, log_level: int = logging.DEBUG):
        """
        Initialize debug logger.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.logger = logging.getLogger('gmail_checker')
        self.logger.setLevel(log_level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler with detailed formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for persistent logging
        try:
            log_file = '/tmp/gmail_checker_debug.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.log_file_path = log_file
        except Exception:
            self.log_file_path = None
    
    def debug(self, message: str, context: Dict[str, Any] = None):
        """Log debug message with optional context."""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.debug(message)
    
    def info(self, message: str, context: Dict[str, Any] = None):
        """Log info message with optional context."""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.info(message)
    
    def warning(self, message: str, context: Dict[str, Any] = None):
        """Log warning message with optional context."""
        if context:
            message = f"{message} | Context: {context}"
        self.logger.warning(message)
    
    def error(self, message: str, exception: Exception = None, context: Dict[str, Any] = None):
        """Log error message with exception details and context."""
        error_details = []
        error_details.append(f"ERROR: {message}")
        
        if exception:
            error_details.append(f"Exception Type: {type(exception).__name__}")
            error_details.append(f"Exception Message: {str(exception)}")
            error_details.append(f"Traceback: {traceback.format_exc()}")
        
        if context:
            error_details.append(f"Context: {context}")
        
        full_message = " | ".join(error_details)
        self.logger.error(full_message)
    
    def log_function_entry(self, func_name: str, args: tuple = None, kwargs: dict = None):
        """Log function entry with parameters."""
        params = []
        if args:
            params.append(f"args={args}")
        if kwargs:
            params.append(f"kwargs={kwargs}")
        
        param_str = ", ".join(params) if params else "no parameters"
        self.debug(f"ENTERING {func_name} with {param_str}")
    
    def log_function_exit(self, func_name: str, result: Any = None, duration: float = None):
        """Log function exit with result and duration."""
        details = []
        if result is not None:
            details.append(f"result_type={type(result).__name__}")
        if duration is not None:
            details.append(f"duration={duration:.3f}s")
        
        detail_str = ", ".join(details) if details else "no details"
        self.debug(f"EXITING {func_name} with {detail_str}")
    
    def log_system_info(self):
        """Log system information for debugging."""
        system_info = {
            'python_version': sys.version,
            'platform': sys.platform,
            'working_directory': os.getcwd(),
            'python_path': sys.path[:3],  # First 3 entries
            'environment_vars': {
                k: v for k, v in os.environ.items() 
                if k.startswith(('PYTHON', 'PATH', 'COLAB'))
            }
        }
        
        self.info("System Information", system_info)
    
    def log_module_versions(self):
        """Log versions of key modules."""
        modules_to_check = [
            'gradio', 'google.auth', 'pandas', 'imaplib'
        ]
        
        versions = {}
        for module_name in modules_to_check:
            try:
                module = __import__(module_name)
                version = getattr(module, '__version__', 'unknown')
                versions[module_name] = version
            except ImportError:
                versions[module_name] = 'not installed'
            except Exception as e:
                versions[module_name] = f'error: {str(e)}'
        
        self.info("Module Versions", versions)
    
    def get_log_file_path(self) -> Optional[str]:
        """Get path to log file if available."""
        return self.log_file_path


# Global debug logger instance
debug_logger = DebugLogger()


def log_debug(message: str, context: Dict[str, Any] = None):
    """Convenience function for debug logging."""
    debug_logger.debug(message, context)


def log_error(message: str, exception: Exception = None, context: Dict[str, Any] = None):
    """Convenience function for error logging."""
    debug_logger.error(message, exception, context)


def log_function_call(func):
    """Decorator for automatic function call logging."""
    def wrapper(*args, **kwargs):
        func_name = f"{func.__module__}.{func.__name__}"
        debug_logger.log_function_entry(func_name, args, kwargs)
        
        start_time = datetime.now()
        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            debug_logger.log_function_exit(func_name, result, duration)
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            debug_logger.error(f"Function {func_name} failed after {duration:.3f}s", e)
            raise
    
    return wrapper