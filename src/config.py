"""
Configuration management module for AutoWater Plant Shop Soil Monitor.

This module handles loading and accessing configuration settings from YAML files.
"""

import os
import yaml
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration from YAML files."""
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize the configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self._config: Dict[str, Any] = {}
        self._secrets: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from YAML files."""
        try:
            # Load main configuration
            config_path = os.path.join(self.config_dir, "config.yaml")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as file:
                    self._config = yaml.safe_load(file) or {}
                logger.info(f"Loaded configuration from {config_path}")
            
            # Load secrets if available
            secrets_path = os.path.join(self.config_dir, "secrets.yaml")
            if os.path.exists(secrets_path):
                with open(secrets_path, 'r', encoding='utf-8') as file:
                    self._secrets = yaml.safe_load(file) or {}
                logger.info("Loaded secrets configuration")
                    
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'sensor.type')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self._get_nested_value(self._config, key, default)
    
    def get_secret(self, key: str, default: Any = None) -> Any:
        """
        Get a secret configuration value.
        
        Args:
            key: Secret key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Secret value or default
        """
        return self._get_nested_value(self._secrets, key, default)
    
    def _get_nested_value(self, data: Dict[str, Any], key: str, default: Any) -> Any:
        """Get nested dictionary value using dot notation."""
        keys = key.split('.')
        value = data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


# Global configuration instance
config = ConfigManager()