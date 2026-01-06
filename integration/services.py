"""Service definitions for face recognition integration."""

from homeassistant.core import ServiceCall
import logging

from .events import DOMAIN, EVENT_DETECTED

_LOGGER = logging.getLogger(__name__)


async def async_setup_services(hass):
    """Set up services for face recognition integration."""
    
    async def fire_event_service(call: ServiceCall):
        """Service to manually fire a recognition event."""
        event_data = {
            "person_id": call.data.get("person_id"),
            "display_name": call.data.get("display_name"),
            "confidence": call.data.get("confidence"),
            "camera": call.data.get("camera"),
            "image_id": call.data.get("image_id", ""),
            "face_id": call.data.get("face_id", ""),
            "timestamp": call.data.get("timestamp", ""),
            "model_version": call.data.get("model_version", "v000"),
        }
        
        _LOGGER.info(f"Service: Firing event {EVENT_DETECTED} with data: {event_data}")
        hass.bus.async_fire(EVENT_DETECTED, event_data)
    
    hass.services.async_register(DOMAIN, "fire_event", fire_event_service)
    _LOGGER.info("Face Recognition services registered")

