"""Service definitions for face recognition integration."""

from homeassistant.core import ServiceCall
from homeassistant.helpers import config_validation as cv
from datetime import datetime
import logging
import base64
import aiohttp
import voluptuous as vol
from typing import Dict, Any, Optional

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
    
    
    async def recognize_face_service(call: ServiceCall):
        """Service to send image for face recognition.

        Supports:
        - image_url: URL to image (local or remote)
        - image_data: Base64 encoded image data
        - camera: Camera entity ID (optional)
        - entity_id: Camera entity to get image from
        """
        try:
            _LOGGER.error("=== RECOGNIZE_FACE SERVICE CALLED ===")
            _LOGGER.error(f"Service data: {call.data}")

            # Get configuration
            config = hass.data.get(DOMAIN, {}).get("config", {})
            api_host = config.get("api_host", "localhost")
            api_port = config.get("api_port", 8080)
            api_token = config.get("api_token", "")
            api_url = f"http://{api_host}:{api_port}"

            _LOGGER.error(f"Connecting to add-on at: {api_url}")

            # Get image data
            image_url = call.data.get("image_url")
            image_data = call.data.get("image_data")
            camera = call.data.get("camera", "unknown")
            entity_id = call.data.get("entity_id")

            image_bytes = None

            # Method 1: Get image from entity_id (camera entity)
            if entity_id:
                _LOGGER.error(f"Getting image from entity: {entity_id}")
                image_bytes = await _get_image_from_entity(hass, entity_id)

            # Method 2: Get image from URL
            elif image_url:
                _LOGGER.error(f"Getting image from URL: {image_url}")
                image_bytes = await _get_image_from_url(hass, image_url)

            # Method 3: Use provided base64 data
            elif image_data:
                _LOGGER.error(f"Using provided base64 image data ({len(image_data)} chars)")
                try:
                    image_bytes = base64.b64decode(image_data)
                except Exception as e:
                    _LOGGER.error(f"Failed to decode base64 image data: {e}")
                    raise ValueError(f"Invalid base64 image data: {e}")

            else:
                raise ValueError("No image source provided. Use image_url, image_data, or entity_id")

            if not image_bytes:
                raise ValueError("Failed to get image data")

            _LOGGER.error(f"Image size: {len(image_bytes)} bytes")

            # Prepare payload for add-on
            payload = {
                "event_type": "recognition_request",
                "camera": camera,
                "image_data": base64.b64encode(image_bytes).decode('utf-8'),
                "image_size": len(image_bytes),
                "timestamp": datetime.now().isoformat(),
                "source": "service_call"
            }

            if entity_id:
                payload["entity_id"] = entity_id
            if image_url:
                payload["image_url"] = image_url

            # Send to add-on
            headers = {"Content-Type": "application/json"}
            if api_token:
                headers["Authorization"] = f"Bearer {api_token}"

            _LOGGER.error(f"Sending to add-on: {api_url}/event")

            session = aiohttp.ClientSession()
            try:
                timeout = aiohttp.ClientTimeout(total=30)
                async with session.post(
                    f"{api_url}/event",
                    json=payload,
                    headers=headers,
                    timeout=timeout
                ) as response:

                    if response.status == 200:
                        result = await response.json()
                        _LOGGER.error(f"Add-on response: {result}")

                        # Return results to automation
                        return {
                            "success": True,
                            "person_id": result.get("person_id"),
                            "display_name": result.get("display_name"),
                            "confidence": result.get("confidence"),
                            "needs_review": result.get("needs_review", False),
                            "face_count": result.get("face_count", 0),
                            "processing_time_ms": result.get("processing_time_ms", 0),
                            "raw_response": result
                        }
                    else:
                        error_text = await response.text()
                        _LOGGER.error(f"Add-on error: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Add-on returned {response.status}",
                            "error_details": error_text[:200]
                        }

            except aiohttp.ClientError as e:
                _LOGGER.error(f"Connection error to add-on: {e}")
                return {
                    "success": False,
                    "error": f"Connection failed: {str(e)}",
                    "suggestion": "Check if add-on is running and api_host is correct"
                }
            finally:
                await session.close()

        except Exception as e:
            _LOGGER.exception(f"Error in recognize_face service: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _get_image_from_entity(hass, entity_id: str) -> Optional[bytes]:
        """Get image from camera entity."""
        try:
            state = hass.states.get(entity_id)
            if not state:
                raise ValueError(f"Entity {entity_id} not found")

            # Check if it's a camera entity
            if state.domain != "camera":
                raise ValueError(f"Entity {entity_id} is not a camera")

            # Get image URL from camera entity
            image_url = state.attributes.get("entity_picture")
            if not image_url:
                # Try to get snapshot via camera service
                from homeassistant.components.camera import async_get_image
                try:
                    image = await async_get_image(hass, entity_id)
                    return image.content
                except:
                    raise ValueError(f"Camera {entity_id} has no accessible image")

            # Fetch image from URL
            return await _get_image_from_url(hass, image_url)

        except Exception as e:
            _LOGGER.error(f"Failed to get image from entity {entity_id}: {e}")
            raise

    async def _get_image_from_url(hass, image_url: str) -> bytes:
        """Get image from URL."""
        try:
            # Handle local HA URLs
            if image_url.startswith("/"):
                # Convert to full URL
                try:
                    base_url = hass.config.internal_url or "http://homeassistant.local:8123"
                    image_url = f"{base_url}{image_url}"
                except:
                    image_url = f"http://homeassistant.local:8123{image_url}"

            _LOGGER.error(f"Fetching image from: {image_url}")

            session = aiohttp.ClientSession()
            try:
                async with session.get(image_url, timeout=10) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        raise ValueError(f"Failed to fetch image: {response.status}")
            finally:
                await session.close()

        except Exception as e:
            _LOGGER.error(f"Failed to get image from URL {image_url}: {e}")
            raise

    # Define schema for recognize_face service
    # Start with simple schema - we'll add validation in the service function
    RECOGNIZE_FACE_SCHEMA = vol.Schema({
        vol.Required("camera"): cv.string,
        vol.Optional("image_data"): cv.string,
        vol.Optional("image_url"): cv.string,
        vol.Optional("entity_id"): cv.string,
        vol.Optional("display_name"): cv.string,
    })

    # Schema for fire_event service
    FIRE_EVENT_SCHEMA = vol.Schema({
        vol.Required("person_id"): cv.string,
        vol.Required("display_name"): cv.string,
        vol.Required("confidence"): vol.Coerce(float),
        vol.Required("camera"): cv.string,
        vol.Optional("image_id"): cv.string,
        vol.Optional("face_id"): cv.string,
        vol.Optional("timestamp"): cv.string,
        vol.Optional("model_version"): cv.string,
    })


    hass.services.async_register(
        DOMAIN,
        "fire_event",
        fire_event_service,
        schema=FIRE_EVENT_SCHEMA
    )


    hass.services.async_register(
        DOMAIN,
        "recognize_face",
        recognize_face_service,
        schema=RECOGNIZE_FACE_SCHEMA
    )

    _LOGGER.info("Face Recognition services registered")

