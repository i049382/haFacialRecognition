"""Nest event listener for face recognition integration."""

import logging
import asyncio
from typing import Dict, Any
from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.helpers import aiohttp_client as aiohttp_helper

from .events import DOMAIN, EVENT_DETECTED

_LOGGER = logging.getLogger(__name__)


class NestEventListener:
    """Listens to Nest events and fetches images."""
    
    def __init__(self, hass: HomeAssistant, api_url: str, api_token: str):
        """Initialize Nest event listener.
        
        Args:
            hass: Home Assistant instance
            api_url: Add-on API URL
            api_token: API authentication token
        """
        self.hass = hass
        self.api_url = api_url
        self.api_token = api_token
        self._session = None
        self._unsub_listener = None
        
    async def async_start(self):
        """Start listening to Nest events."""
        self._session = aiohttp_helper.async_get_clientsession(self.hass)
        
        # Listen to nest_event
        self._unsub_listener = self.hass.bus.async_listen(
            "nest_event",
            self._handle_nest_event
        )
        
        _LOGGER.info("Nest event listener started")
        
    async def async_stop(self):
        """Stop listening to Nest events."""
        if self._unsub_listener:
            self._unsub_listener()
            self._unsub_listener = None
        _LOGGER.info("Nest event listener stopped")
    
    @callback
    async def _handle_nest_event(self, event: Event):
        """Handle a Nest event.
        
        Args:
            event: Nest event from HA event bus
        """
        event_data = event.data
        
        _LOGGER.error(f"=== NEST EVENT RECEIVED === Data: {event_data}")
        
        # Extract event information
        event_type = event_data.get("type")
        device_id = event_data.get("device_id")
        event_id = event_data.get("event_id")
        
        if not all([event_type, device_id, event_id]):
            _LOGGER.warning(f"Incomplete Nest event data: {event_data}")
            return
        
        # Only process motion/person events
        if event_type not in ["motion", "person"]:
            _LOGGER.debug(f"Skipping Nest event type: {event_type}")
            return
        
        _LOGGER.error(f"Processing Nest event: type={event_type}, device={device_id}, event_id={event_id}")
        
        # Fetch image immediately (Nest URLs expire quickly)
        image_data = await self._fetch_nest_image(device_id, event_id)
        
        if image_data:
            # Send to add-on for processing
            await self._send_to_addon(event_data, image_data)
        else:
            _LOGGER.warning(f"Failed to fetch Nest image for event {event_id}")
    
    async def _fetch_nest_image(self, device_id: str, event_id: str) -> bytes:
        """Fetch image from Nest event media API.
        
        Args:
            device_id: Nest device ID
            event_id: Nest event ID
            
        Returns:
            Image bytes, or None if failed
        """
        try:
            # Construct Nest API URL - use HA internal API
            # The session from async_get_clientsession is configured for HA internal API
            # Format: /api/nest/event_media/<device_id>/<event_id>/thumbnail
            api_url = f"/api/nest/event_media/{device_id}/{event_id}/thumbnail"
            
            _LOGGER.error(f"Fetching Nest image from HA API: {api_url}")
            
            # Fetch image (with timeout - Nest URLs expire quickly)
            async with self._session.get(
                api_url,
                timeout=10
            ) as response:
                if response.status == 200:
                    image_data = await response.read()
                    _LOGGER.info(f"Successfully fetched Nest image ({len(image_data)} bytes)")
                    return image_data
                elif response.status == 404:
                    _LOGGER.warning(f"Nest media expired or not found: {event_id}")
                    return None
                else:
                    _LOGGER.error(f"Failed to fetch Nest image: {response.status}")
                    return None
                    
        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout fetching Nest image (URL may have expired)")
            return None
        except Exception as e:
            _LOGGER.exception(f"Error fetching Nest image: {e}")
            return None
    
    async def _send_to_addon(self, event_data: Dict[str, Any], image_data: bytes):
        """Send event and image to add-on for processing.
        
        Args:
            event_data: Nest event data
            image_data: Image bytes
        """
        try:
            # For Chunk 3, we'll send the event info
            # In later chunks, we'll send the image for face recognition
            payload = {
                "event_type": "nest_event",
                "device_id": event_data.get("device_id"),
                "event_id": event_data.get("event_id"),
                "event_type_nest": event_data.get("type"),
                "camera": event_data.get("device_id"),  # Use device_id as camera identifier
                "image_size": len(image_data),
                "timestamp": event_data.get("timestamp", ""),
            }
            
            headers = {}
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            
            async with self._session.post(
                f"{self.api_url}/event",
                json=payload,
                headers=headers,
                timeout=5
            ) as response:
                if response.status == 200:
                    _LOGGER.info(f"Successfully sent Nest event to add-on")
                else:
                    _LOGGER.error(f"Failed to send event to add-on: {response.status}")
                    
        except Exception as e:
            _LOGGER.exception(f"Error sending event to add-on: {e}")

