"""Configuration management for the face recognition add-on."""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration for the face recognition add-on."""
    
    # Recognition thresholds
    confidence_threshold: float = 0.75
    review_threshold: float = 0.60
    
    # Camera watch directories
    camera_paths: List[str] = None
    
    # Model update polling
    enable_daily_poll: bool = False
    daily_poll_time: str = "02:00"
    
    # Google Drive configuration
    drive_folder_id: str = ""
    
    # API configuration
    api_port: int = 8080
    api_token: str = ""
    
    # Google Drive credentials (from HA secrets)
    drive_credentials: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.camera_paths is None:
            self.camera_paths = []


class ConfigLoader:
    """Loads and validates configuration from HA add-on config."""
    
    def __init__(self, config_path: str = "/data/options.json"):
        """Initialize config loader.
        
        Args:
            config_path: Path to HA add-on options.json file
        """
        self.config_path = Path(config_path)
        self.secrets_path = Path("/config/secrets.yaml")
        
    def load_secret(self, secret_name: str) -> Optional[str]:
        """Load a secret from HA secrets.yaml.
        
        Args:
            secret_name: Name of the secret (without !secret prefix)
            
        Returns:
            Secret value or None if not found
        """
        if not self.secrets_path.exists():
            logger.warning(f"Secrets file not found: {self.secrets_path}")
            return None
            
        try:
            with open(self.secrets_path, 'r') as f:
                secrets = yaml.safe_load(f) or {}
                
            if secret_name not in secrets:
                logger.warning(f"Secret '{secret_name}' not found in secrets.yaml")
                return None
                
            return str(secrets[secret_name])
            
        except Exception as e:
            logger.error(f"Error loading secret '{secret_name}': {e}")
            return None
    
    def load(self) -> Config:
        """Load configuration from options.json and secrets.
        
        Returns:
            Config object with loaded values
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config validation fails
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}. "
                "Make sure the add-on is properly configured in Home Assistant."
            )
        
        # Load options.json (HA stores it as JSON, not YAML)
        import json
        with open(self.config_path, 'r') as f:
            options = json.load(f) or {}
        
        # Load Google Drive credentials from secrets
        drive_credentials = self.load_secret("face_recognition_drive_credentials")
        
        # Validate thresholds
        confidence_threshold = float(options.get("confidence_threshold", 0.75))
        review_threshold = float(options.get("review_threshold", 0.60))
        
        if not (0.0 <= confidence_threshold <= 1.0):
            raise ValueError(
                f"confidence_threshold must be between 0.0 and 1.0, got {confidence_threshold}"
            )
        
        if not (0.0 <= review_threshold <= 1.0):
            raise ValueError(
                f"review_threshold must be between 0.0 and 1.0, got {review_threshold}"
            )
        
        if review_threshold >= confidence_threshold:
            raise ValueError(
                f"review_threshold ({review_threshold}) must be less than "
                f"confidence_threshold ({confidence_threshold})"
            )
        
        # Validate API token
        api_token = options.get("api_token", "")
        if not api_token:
            logger.warning("api_token not configured. API will be unauthenticated.")
        
        # Validate daily poll time format
        daily_poll_time = options.get("daily_poll_time", "02:00")
        if not self._validate_time_format(daily_poll_time):
            raise ValueError(
                f"daily_poll_time must be in HH:MM format, got {daily_poll_time}"
            )
        
        # Build config object
        config = Config(
            confidence_threshold=confidence_threshold,
            review_threshold=review_threshold,
            camera_paths=options.get("camera_paths", []),
            enable_daily_poll=options.get("enable_daily_poll", False),
            daily_poll_time=daily_poll_time,
            drive_folder_id=options.get("drive_folder_id", ""),
            api_port=int(options.get("api_port", 8080)),
            api_token=api_token,
            drive_credentials=drive_credentials,
        )
        
        # Log configuration (without sensitive data)
        logger.info("Configuration loaded:")
        logger.info(f"  confidence_threshold: {config.confidence_threshold}")
        logger.info(f"  review_threshold: {config.review_threshold}")
        logger.info(f"  camera_paths: {config.camera_paths}")
        logger.info(f"  enable_daily_poll: {config.enable_daily_poll}")
        logger.info(f"  daily_poll_time: {config.daily_poll_time}")
        logger.info(f"  api_port: {config.api_port}")
        logger.info(f"  drive_folder_id: {'configured' if config.drive_folder_id else 'not configured'}")
        logger.info(f"  drive_credentials: {'loaded' if config.drive_credentials else 'not found'}")
        
        # Warn if Drive credentials missing (non-fatal for now)
        if not config.drive_credentials:
            logger.warning(
                "Google Drive credentials not found in secrets.yaml. "
                "Drive upload functionality will be disabled until credentials are configured."
            )
        
        return config
    
    @staticmethod
    def _validate_time_format(time_str: str) -> bool:
        """Validate time format HH:MM.
        
        Args:
            time_str: Time string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False
            hour = int(parts[0])
            minute = int(parts[1])
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except (ValueError, AttributeError):
            return False

