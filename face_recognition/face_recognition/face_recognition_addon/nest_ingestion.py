"""Nest event ingestion for face recognition add-on."""

import logging
import requests
from typing import Optional, Dict, Any
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class NestEventIngestion:
    """Handles ingestion of Nest camera events."""
    
    def __init__(self, config, api_client):
        """Initialize Nest event ingestion.
        
        Args:
            config: Config object
            api_client: HTTP client for fetching images
        """
        self.config = config
        self.api_client = api_client
        self.ha_url = "http://supervisor/core"  # HA Supervisor API URL
        self.image_storage = Path("/data/images")
        self.image_storage.mkdir(parents=True, exist_ok=True)
        
    def process_nest_event(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Process a Nest event and fetch the image.
        
        Args:
            event_data: Nest event data dictionary
            
        Returns:
            Path to saved image, or None if failed
        """
        try:
            # Extract event information
            event_type = event_data.get("type")
            device_id = event_data.get("device_id")
            event_id = event_data.get("event_id")
            
            if not all([event_type, device_id, event_id]):
                logger.warning(f"Incomplete Nest event data: {event_data}")
                return None
            
            # Only process motion/person events
            if event_type not in ["motion", "person"]:
                logger.debug(f"Skipping Nest event type: {event_type}")
                return None
            
            logger.info(f"Processing Nest event: {event_type} on device {device_id}")
            
            # Fetch image from Nest API
            image_path = self._fetch_nest_image(device_id, event_id)
            
            if image_path:
                logger.info(f"Successfully fetched Nest image: {image_path}")
                return str(image_path)
            else:
                logger.warning(f"Failed to fetch Nest image for event {event_id}")
                return None
                
        except Exception as e:
            logger.exception(f"Error processing Nest event: {e}")
            return None
    
    def _fetch_nest_image(self, device_id: str, event_id: str) -> Optional[Path]:
        """Fetch image from Nest event media API.
        
        Args:
            device_id: Nest device ID
            event_id: Nest event ID
            
        Returns:
            Path to saved image, or None if failed
        """
        try:
            # Construct Nest API URL
            # Format: /api/nest/event_media/<device_id>/<event_id>/thumbnail
            api_url = f"{self.ha_url}/api/nest/event_media/{device_id}/{event_id}/thumbnail"
            
            logger.debug(f"Fetching Nest image from: {api_url}")
            
            # Fetch image (with timeout - Nest URLs expire quickly)
            response = self.api_client.get(
                api_url,
                timeout=10,
                headers={"Authorization": f"Bearer {self._get_supervisor_token()}"}
            )
            
            if response.status_code == 200:
                # Generate filename
                timestamp = int(time.time())
                filename = f"nest_{device_id}_{event_id}_{timestamp}.jpg"
                image_path = self.image_storage / filename
                
                # Save image
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"Saved Nest image: {image_path}")
                return image_path
                
            elif response.status_code == 404:
                logger.warning(f"Nest media expired or not found: {event_id}")
                return None
            else:
                logger.error(f"Failed to fetch Nest image: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching Nest image (URL may have expired)")
            return None
        except Exception as e:
            logger.exception(f"Error fetching Nest image: {e}")
            return None
    
    def _get_supervisor_token(self) -> str:
        """Get Supervisor API token.
        
        Returns:
            Supervisor token or empty string
        """
        # Supervisor token is available via environment variable
        import os
        return os.environ.get("SUPERVISOR_TOKEN", "")

