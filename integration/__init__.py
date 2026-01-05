"""Face Recognition integration for Home Assistant."""

from homeassistant.core import HomeAssistant

DOMAIN = "face_recognition"

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Face Recognition integration.
    
    Args:
        hass: Home Assistant instance
        config: Configuration dictionary
        
    Returns:
        True if setup successful
    """
    # Chunk 0: Just validate integration loads
    # Actual setup will happen in Chunk 2
    return True

