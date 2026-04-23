"""
Error Handling and User Feedback Module
Provides comprehensive error handling, logging, and user-friendly messages
"""
import logging
import traceback
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ErrorCategory(Enum):
    """Categories of errors for better handling"""
    API_ERROR = "api_error"
    NETWORK_ERROR = "network_error"
    DATA_ERROR = "data_error"
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    SYSTEM_ERROR = "system_error"


class UserFriendlyError(Exception):
    """Base exception with user-friendly messages"""
    
    def __init__(self, user_message: str, technical_message: Optional[str] = None, 
                 category: ErrorCategory = ErrorCategory.SYSTEM_ERROR, 
                 recovery_suggestion: Optional[str] = None):
        self.user_message = user_message
        self.technical_message = technical_message or user_message
        self.category = category
        self.recovery_suggestion = recovery_suggestion
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.user_message)


class APIError(UserFriendlyError):
    """API-related errors"""
    
    def __init__(self, service: str, user_message: str, technical_message: Optional[str] = None,
                 recovery_suggestion: Optional[str] = None):
        self.service = service
        default_suggestion = f"Check your {service} API key and try again."
        recovery_suggestion = recovery_suggestion or default_suggestion
        super().__init__(user_message, technical_message, ErrorCategory.API_ERROR, recovery_suggestion)


class NetworkError(UserFriendlyError):
    """Network-related errors"""
    
    def __init__(self, user_message: str, technical_message: Optional[str] = None,
                 recovery_suggestion: Optional[str] = None):
        default_suggestion = "Check your internet connection and try again."
        recovery_suggestion = recovery_suggestion or default_suggestion
        super().__init__(user_message, technical_message, ErrorCategory.NETWORK_ERROR, recovery_suggestion)


class DataError(UserFriendlyError):
    """Data-related errors"""
    
    def __init__(self, user_message: str, technical_message: Optional[str] = None,
                 recovery_suggestion: Optional[str] = None):
        default_suggestion = "Please check your data format and try again."
        recovery_suggestion = recovery_suggestion or default_suggestion
        super().__init__(user_message, technical_message, ErrorCategory.DATA_ERROR, recovery_suggestion)


class ValidationError(UserFriendlyError):
    """Validation errors"""
    
    def __init__(self, field: str, user_message: str, technical_message: Optional[str] = None,
                 recovery_suggestion: Optional[str] = None):
        self.field = field
        default_suggestion = f"Please provide a valid {field} and try again."
        recovery_suggestion = recovery_suggestion or default_suggestion
        super().__init__(user_message, technical_message, ErrorCategory.VALIDATION_ERROR, recovery_suggestion)


class AuthenticationError(UserFriendlyError):
    """Authentication errors"""
    
    def __init__(self, service: str, user_message: str, technical_message: Optional[str] = None,
                 recovery_suggestion: Optional[str] = None):
        self.service = service
        default_suggestion = f"Please check your {service} credentials and try again."
        recovery_suggestion = recovery_suggestion or default_suggestion
        super().__init__(user_message, technical_message, ErrorCategory.AUTHENTICATION_ERROR, recovery_suggestion)


class RateLimitError(UserFriendlyError):
    """Rate limit errors"""
    
    def __init__(self, service: str, user_message: str, technical_message: Optional[str] = None,
                 recovery_suggestion: Optional[str] = None):
        self.service = service
        default_suggestion = f"Please wait a few minutes and try again. {service} has rate limits."
        recovery_suggestion = recovery_suggestion or default_suggestion
        super().__init__(user_message, technical_message, ErrorCategory.RATE_LIMIT_ERROR, recovery_suggestion)


class ErrorHandler:
    """Central error handling and logging"""
    
    def __init__(self, log_file: str = "error_log.json"):
        self.log_file = log_file
        self.error_history = []
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app_errors.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle an error and return user-friendly response"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "user_message": str(error),
            "technical_message": str(error),
            "category": "system_error",
            "recovery_suggestion": "Please try again or contact support if the problem persists.",
            "context": context or {}
        }
        
        # Handle custom user-friendly errors
        if isinstance(error, UserFriendlyError):
            error_info.update({
                "user_message": error.user_message,
                "technical_message": error.technical_message,
                "category": error.category.value,
                "recovery_suggestion": error.recovery_suggestion
            })
        
        # Log the error
        self.logger.error(f"Error occurred: {error_info}", exc_info=True)
        
        # Add to history
        self.error_history.append(error_info)
        
        # Save to file
        self._save_error_log(error_info)
        
        return error_info
    
    def _save_error_log(self, error_info: Dict[str, Any]):
        """Save error log to file"""
        try:
            import json
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(error_info) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to save error log: {e}")
    
    def get_user_friendly_message(self, error: Exception) -> str:
        """Get user-friendly error message"""
        if isinstance(error, UserFriendlyError):
            message = f"❌ {error.user_message}\n\n"
            if error.recovery_suggestion:
                message += f"💡 {error.recovery_suggestion}"
            return message
        
        # Generic error handling
        return f"❌ An error occurred: {str(error)}\n\n💡 Please try again or contact support if the problem persists."
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics"""
        if not self.error_history:
            return {"total_errors": 0, "by_category": {}, "recent_errors": []}
        
        by_category = {}
        for error in self.error_history:
            category = error.get("category", "unknown")
            by_category[category] = by_category.get(category, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "by_category": by_category,
            "recent_errors": self.error_history[-10:]  # Last 10 errors
        }


class SafeExecutor:
    """Safe execution wrapper with error handling"""
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
    
    def execute(self, func, *args, **kwargs) -> Dict[str, Any]:
        """Execute function with error handling"""
        try:
            result = func(*args, **kwargs)
            return {
                "success": True,
                "data": result,
                "error": None
            }
        except UserFriendlyError as e:
            error_info = self.error_handler.handle_error(e, {"function": func.__name__})
            return {
                "success": False,
                "data": None,
                "error": error_info
            }
        except Exception as e:
            # Convert unexpected errors to user-friendly errors
            error_info = self.error_handler.handle_error(e, {"function": func.__name__})
            return {
                "success": False,
                "data": None,
                "error": error_info
            }
    
    def execute_with_fallback(self, func, fallback_func, *args, **kwargs) -> Dict[str, Any]:
        """Execute function with fallback on error"""
        try:
            result = func(*args, **kwargs)
            return {
                "success": True,
                "data": result,
                "error": None,
                "used_fallback": False
            }
        except Exception as e:
            self.error_handler.logger.warning(f"Primary function failed, using fallback: {e}")
            try:
                fallback_result = fallback_func(*args, **kwargs)
                return {
                    "success": True,
                    "data": fallback_result,
                    "error": None,
                    "used_fallback": True,
                    "fallback_reason": str(e)
                }
            except Exception as fallback_error:
                error_info = self.error_handler.handle_error(fallback_error, {"function": func.__name__})
                return {
                    "success": False,
                    "data": None,
                    "error": error_info,
                    "used_fallback": True,
                    "fallback_failed": True
                }


# Global error handler instance
error_handler = ErrorHandler()
safe_executor = SafeExecutor(error_handler)


def safe_api_call(api_func, *args, service_name: str = "API", **kwargs) -> Dict[str, Any]:
    """Wrapper for safe API calls with standard error handling"""
    try:
        result = api_func(*args, **kwargs)
        return {
            "success": True,
            "data": result,
            "error": None
        }
    except requests.exceptions.Timeout:
        error = NetworkError(
            f"The {service_name} request timed out. Please try again.",
            f"Timeout error calling {service_name}",
            "Check your internet connection and try again later."
        )
        error_info = error_handler.handle_error(error)
        return {"success": False, "data": None, "error": error_info}
    
    except requests.exceptions.ConnectionError:
        error = NetworkError(
            f"Could not connect to {service_name}. Please check your internet connection.",
            f"Connection error calling {service_name}",
            "Check your internet connection and try again."
        )
        error_info = error_handler.handle_error(error)
        return {"success": False, "data": None, "error": error_info}
    
    except Exception as e:
        error = APIError(
            service_name,
            f"An error occurred while calling {service_name}.",
            str(e),
            f"Please check your {service_name} configuration and try again."
        )
        error_info = error_handler.handle_error(error)
        return {"success": False, "data": None, "error": error_info}


def validate_json_input(json_string: str, field_name: str = "input") -> Dict:
    """Validate JSON input and return parsed data or error"""
    try:
        import json
        data = json.loads(json_string)
        return {"success": True, "data": data, "error": None}
    except json.JSONDecodeError as e:
        error = ValidationError(
            field_name,
            f"Invalid JSON format in {field_name}. Please check your syntax.",
            str(e),
            "Please ensure your JSON is properly formatted with valid syntax."
        )
        error_info = error_handler.handle_error(error)
        return {"success": False, "data": None, "error": error_info}


def validate_required_fields(data: Dict, required_fields: list) -> Dict:
    """Validate that required fields are present in data"""
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        error = ValidationError(
            "required fields",
            f"Missing required fields: {', '.join(missing_fields)}",
            f"Missing fields: {missing_fields}",
            f"Please provide all required fields: {', '.join(required_fields)}"
        )
        error_info = error_handler.handle_error(error)
        return {"success": False, "data": None, "error": error_info}
    
    return {"success": True, "data": data, "error": None}