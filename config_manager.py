"""
Configuration Management Module
Handles loading and managing application configuration from external files
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages application configuration from external files"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        config_path = Path(self.config_file)
        
        if not config_path.exists():
            # Create default configuration if file doesn't exist
            return self._get_default_config()
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Validate configuration structure
            self._validate_config(config)
            return config
            
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            return self._get_default_config()
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return self._get_default_config()
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration structure"""
        required_sections = ['app', 'models', 'api_settings', 'data_settings', 'ui_settings', 'features']
        
        for section in required_sections:
            if section not in config:
                print(f"Warning: Missing required configuration section: {section}")
                config[section] = {}
        
        return True
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "app": {
                "name": "Enhanced Research Assistant",
                "version": "2.0.0",
                "description": "AI-powered research companion"
            },
            "models": {},
            "api_settings": {},
            "data_settings": {
                "data_directory": "data",
                "cache_ttl": 3600
            },
            "ui_settings": {
                "theme": "default",
                "show_progress": True
            },
            "features": {}
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value by dot notation key"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        return self.save_config()
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            config_path = Path(self.config_file)
            config_path.parent.mkdir(exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def get_models(self) -> Dict[str, Any]:
        """Get all models configuration"""
        return self.get('models', {})
    
    def get_enabled_models(self) -> Dict[str, Any]:
        """Get only enabled models"""
        all_models = self.get_models()
        return {k: v for k, v in all_models.items() if v.get('enabled', True)}
    
    def get_model_config(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for specific model"""
        return self.get(f'models.{model_id}')
    
    def get_api_settings(self, service: str) -> Dict[str, Any]:
        """Get API settings for specific service"""
        return self.get(f'api_settings.{service}', {})
    
    def get_feature_config(self, feature: str) -> Dict[str, Any]:
        """Get configuration for specific feature"""
        return self.get(f'features.{feature}', {})
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if feature is enabled"""
        feature_config = self.get_feature_config(feature)
        return feature_config.get('enabled', True)
    
    def get_data_directory(self) -> Path:
        """Get data directory path"""
        data_dir = self.get('data_settings.data_directory', 'data')
        return Path(data_dir)
    
    def reload_config(self) -> bool:
        """Reload configuration from file"""
        try:
            self.config = self._load_config()
            return True
        except Exception as e:
            print(f"Error reloading configuration: {e}")
            return False
    
    def add_custom_model(self, model_id: str, model_config: Dict[str, Any]) -> bool:
        """Add custom model configuration"""
        try:
            models = self.config.setdefault('models', {})
            models[model_id] = model_config
            return self.save_config()
        except Exception as e:
            print(f"Error adding custom model: {e}")
            return False
    
    def remove_model(self, model_id: str) -> bool:
        """Remove model from configuration"""
        try:
            models = self.config.get('models', {})
            if model_id in models:
                del models[model_id]
                return self.save_config()
            return False
        except Exception as e:
            print(f"Error removing model: {e}")
            return False
    
    def update_model_config(self, model_id: str, updates: Dict[str, Any]) -> bool:
        """Update model configuration"""
        try:
            models = self.config.get('models', {})
            if model_id in models:
                models[model_id].update(updates)
                return self.save_config()
            return False
        except Exception as e:
            print(f"Error updating model config: {e}")
            return False


# Global configuration manager instance
config_manager = ConfigManager()