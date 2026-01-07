"""Face Recognition integration for Home Assistant."""

import logging
import asyncio

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
    _LOGGER.error("=== FACE RECOGNITION INTEGRATION LOADING (CHUNK 3) ===")
    _LOGGER.info("Face Recognition integration loading (Chunk 3)")

    # Debug: Show what config we received
    _LOGGER.error(f"=== DEBUG: Full config received ===")
    _LOGGER.error(f"Config keys: {list(config.keys())}")
    _LOGGER.error(f"Face recognition config in config: {DOMAIN in config}")
    
    try:
        # Set up services
        _LOGGER.error("Setting up services...")
        from . import services
        await services.async_setup_services(hass)
        _LOGGER.error("Services set up successfully")
        
        # Chunk 3: Start Nest event listener if configured
        # For now, we'll start it automatically if Nest integration is available
        # In future chunks, this will be configurable
        
        # Check if Nest integration is available
        # Note: Nest might load after our integration, so we check immediately and also later
        _LOGGER.error(f"Checking for Nest integration. Components: nest in components = {'nest' in hass.config.components}")
        
        async def start_nest_listener():
            """Start Nest listener."""
            from .nest_listener import NestEventListener

            integration_config = config.get(DOMAIN, {})
            _LOGGER.error(f"=== DEBUG: Integration config from YAML ===")
            _LOGGER.error(f"Config keys: {list(integration_config.keys())}")
            _LOGGER.error(f"Full config: {integration_config}")

            api_host = integration_config.get("api_host", "localhost")
            api_port = integration_config.get("api_port", 8080)  # Default matches add-on port (8080)
            api_token = integration_config.get("api_token", "")
            ha_api_token = integration_config.get("ha_api_token", "")  # HA API token for internal API calls
            api_url = f"http://{api_host}:{api_port}"

            _LOGGER.error(f"Connecting to add-on API at {api_url}")
            _LOGGER.error(f"HA API token present: {'ha_api_token' in integration_config}")
            _LOGGER.error(f"HA API token length: {len(ha_api_token) if ha_api_token else 0}")

            if ha_api_token:
                _LOGGER.error("HA API token configured for internal API calls")
            else:
                _LOGGER.warning("No HA API token configured - Nest image fetching may fail")
            
            nest_listener = NestEventListener(hass, api_url, api_token, ha_api_token)
            await nest_listener.async_start()
            
            hass.data.setdefault(DOMAIN, {})["nest_listener"] = nest_listener
            _LOGGER.error("Nest listener started successfully")
        
        if "nest" in hass.config.components:
            _LOGGER.error("Nest integration detected, starting Nest event listener")
            await start_nest_listener()
        else:
            _LOGGER.error("Nest integration not found immediately, will check again in 10 seconds")
            # Check again after a delay (Nest might load after our integration)
            async def delayed_nest_check():
                await asyncio.sleep(10)
                if "nest" in hass.config.components:
                    _LOGGER.error("Nest integration detected (delayed check), starting Nest event listener")
                    await start_nest_listener()
                else:
                    _LOGGER.error("Nest integration still not found after delay - Nest listener will not start")
            
            hass.async_create_task(delayed_nest_check())
        
        _LOGGER.error("Face Recognition integration setup complete")
        return True
    except Exception as e:
        _LOGGER.exception(f"Error setting up Face Recognition integration: {e}")
        return False


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
