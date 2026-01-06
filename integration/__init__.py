"""Face Recognition integration for Home Assistant."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .events import DOMAIN, EVENT_DETECTED

_LOGGER = logging.getLogger(__name__)

# Integration version
__version__ = "0.0.1"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Face Recognition integration.
    
    Args:
        hass: Home Assistant instance
        config: Configuration dictionary
        
    Returns:
        True if setup successful
    """
    _LOGGER.info("Face Recognition integration loading (Chunk 3)")
    
    # Set up services
    from . import services
    await services.async_setup_services(hass)
    
    # Chunk 3: Start Nest event listener if configured
    # For now, we'll start it automatically if Nest integration is available
    # In future chunks, this will be configurable
    
    # Check if Nest integration is available
    if "nest" in hass.config.components:
        _LOGGER.info("Nest integration detected, starting Nest event listener")
        from .nest_listener import NestEventListener
        
        # Get add-on API config from integration config or defaults
        # For Chunk 3, use defaults (add-on runs on localhost:8080)
        integration_config = config.get(DOMAIN, {})
        api_host = integration_config.get("api_host", "localhost")
        api_port = integration_config.get("api_port", 8080)
        api_token = integration_config.get("api_token", "")
        api_url = f"http://{api_host}:{api_port}"
        
        _LOGGER.info(f"Connecting to add-on API at {api_url}")
        
        # Create and start Nest listener
        nest_listener = NestEventListener(hass, api_url, api_token)
        await nest_listener.async_start()
        
        # Store listener in hass data
        hass.data.setdefault(DOMAIN, {})["nest_listener"] = nest_listener
    else:
        _LOGGER.info("Nest integration not found, skipping Nest event listener")
    
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Face Recognition from a config entry.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry
        
    Returns:
        True if setup successful
    """
    _LOGGER.info("Setting up Face Recognition integration")
    
    # Get add-on API configuration from entry
    api_host = entry.data.get("api_host", "localhost")
    api_port = entry.data.get("api_port", 8080)
    api_token = entry.data.get("api_token", "")
    
    # Create coordinator to poll add-on API
    from homeassistant.helpers import aiohttp_client as aiohttp_helper
    coordinator = FaceRecognitionCoordinator(hass, api_host, api_port, api_token, aiohttp_helper)
    
    # Store coordinator in hass data
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    # Start coordinator
    await coordinator.async_config_entry_first_refresh()
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Face Recognition config entry.
    
    Args:
        hass: Home Assistant instance
        entry: Config entry
        
    Returns:
        True if unload successful
    """
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.async_shutdown()
    return True


class FaceRecognitionCoordinator:
    """Coordinates communication with face recognition add-on."""
    
    def __init__(self, hass: HomeAssistant, api_host: str, api_port: int, api_token: str, aiohttp_helper):
        """Initialize coordinator.
        
        Args:
            hass: Home Assistant instance
            api_host: Add-on API host
            api_port: Add-on API port
            api_token: API authentication token
            aiohttp_helper: aiohttp_client helper module
        """
        self.hass = hass
        self.api_host = api_host
        self.api_port = api_port
        self.api_token = api_token
        self.api_url = f"http://{api_host}:{api_port}"
        self._session = None
        self._aiohttp_helper = aiohttp_helper
        
    async def async_config_entry_first_refresh(self):
        """Perform initial refresh."""
        self._session = self._aiohttp_helper.async_get_clientsession(self.hass)
        await self._check_status()
        
    async def _check_status(self):
        """Check add-on API status."""
        try:
            async with self._session.get(f"{self.api_url}/status", timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    _LOGGER.info(f"Add-on status: {data.get('status')}")
                else:
                    _LOGGER.warning(f"Add-on status check failed: {response.status}")
        except Exception as e:
            _LOGGER.error(f"Error checking add-on status: {e}")
    
    async def fire_event(self, event_data: dict):
        """Fire a face recognition event in Home Assistant.
        
        Args:
            event_data: Event data dictionary
        """
        _LOGGER.info(f"Firing event: {EVENT_DETECTED} with data: {event_data}")
        self.hass.bus.async_fire(EVENT_DETECTED, event_data)
    
    async def async_shutdown(self):
        """Shutdown coordinator."""
        if self._session:
            await self._session.close()
