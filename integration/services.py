"""Service definitions for face recognition integration."""

from homeassistant.core import ServiceCall
from datetime import datetime
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
    
    async def fire_nest_event_service(call: ServiceCall):
        """Service to manually fire a dummy Nest event for testing.
        
        This allows testing Nest event ingestion and video frame extraction
        without waiting for an actual Nest event.
        """
        # Get parameters or use defaults based on typical Nest event structure
        device_id = call.data.get("device_id", "65563380bfcf5478f63ff88485eca57")  # From your screenshots
        nest_event_id = call.data.get("nest_event_id", None)
        event_type = call.data.get("event_type", "camera_person")  # or "camera_motion"
        
        # Generate a nest_event_id if not provided (use current timestamp)
        if not nest_event_id:
            nest_event_id = str(int(datetime.now().timestamp()))
        
        # Create dummy Nest event data structure matching real Nest events
        # Real Nest events include more fields - we'll include them for realism
        # Note: We're reading from filesystem, so attachment.image isn't strictly needed,
        # but including it makes the event structure match real events
        now = datetime.now()
        nest_event_data = {
            "type": event_type,
            "device_id": device_id,
            "nest_event_id": nest_event_id,
            "timestamp": now.isoformat(),
            # Additional fields that real Nest events typically have
            "event_session_id": f"session_{nest_event_id}",
            "zones": [],  # Motion zones (empty for person events)
            "has_sound": False,
            "has_motion": event_type == "camera_motion",
            "has_person": event_type == "camera_person",
            # Attachment structure (even though we read from filesystem)
            # This makes the event structure match real Nest events
            "attachment": {
                "image": f"/api/nest/event_media/{device_id}/{nest_event_id}/thumbnail",
                # Note: We don't actually use this URL since we read from filesystem,
                # but including it makes the event structure realistic
            },
            # Additional metadata
            "start_time": now.isoformat(),
            "end_time": now.isoformat(),
        }
        
        _LOGGER.error(f"=== FIRING DUMMY NEST EVENT ===")
        _LOGGER.error(f"Event type: nest_event")
        _LOGGER.error(f"Event data: {nest_event_data}")
        
        # Fire the nest_event (this will trigger our NestEventListener)
        hass.bus.async_fire(
            "nest_event",
            nest_event_data
        )
        
        _LOGGER.info(f"Fired dummy nest_event: type={event_type}, device_id={device_id}, nest_event_id={nest_event_id}")
    
    hass.services.async_register(DOMAIN, "fire_event", fire_event_service)
    hass.services.async_register(DOMAIN, "fire_nest_event", fire_nest_event_service)
    _LOGGER.info("Face Recognition services registered")

