"""Nest event listener for face recognition integration."""

import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.helpers import aiohttp_client as aiohttp_helper
import aiohttp

from .events import DOMAIN, EVENT_DETECTED

_LOGGER = logging.getLogger(__name__)


class NestEventListener:
    """Listens to Nest events and fetches images."""
    
    def __init__(self, hass: HomeAssistant, api_url: str, api_token: str, ha_api_token: str = None):
        """Initialize Nest event listener.
        
        Args:
            hass: Home Assistant instance
            api_url: Add-on API URL
            api_token: API authentication token (for add-on)
            ha_api_token: Home Assistant API token (for internal API calls)
        """
        self.hass = hass
        self.api_url = api_url
        self.api_token = api_token
        self.ha_api_token = ha_api_token
        self._session = None
        self._unsub_listener = None
        self._debug_listener = None
        
    async def async_start(self):
        """Start listening to Nest events."""
        self._session = aiohttp_helper.async_get_clientsession(self.hass)
        
        # Listen to nest_event
        self._unsub_listener = self.hass.bus.async_listen(
            "nest_event",
            self._handle_nest_event
        )
        
        # DEBUG: Also listen to ALL events temporarily to see what Nest fires
        @callback
        async def debug_all_events(event: Event):
            if "nest" in event.event_type.lower() or "camera" in event.event_type.lower():
                _LOGGER.error(f"=== DEBUG: Event detected === Type: {event.event_type}, Data: {event.data}")
        
        self._debug_listener = self.hass.bus.async_listen(
            None,  # Listen to all events
            debug_all_events
        )
        
        _LOGGER.error("=== NEST EVENT LISTENER REGISTERED ===")
        _LOGGER.error(f"Listening for event type: nest_event")
        _LOGGER.error(f"Debug listener also active (all events)")
        _LOGGER.info("Nest event listener started")
        
    async def async_stop(self):
        """Stop listening to Nest events."""
        if self._unsub_listener:
            self._unsub_listener()
            self._unsub_listener = None
        if self._debug_listener:
            self._debug_listener()
            self._debug_listener = None
        _LOGGER.info("Nest event listener stopped")
    
    @callback
    async def _handle_nest_event(self, event: Event):
        """Handle a Nest event.
        
        Args:
            event: Nest event from HA event bus
        """
        _LOGGER.error(f"=== NEST EVENT RECEIVED ===")
        _LOGGER.error(f"Event type: {event.event_type}")
        _LOGGER.error(f"Event origin: {event.origin}")
        _LOGGER.error(f"Event time fired: {event.time_fired}")
        
        event_data = event.data
        _LOGGER.error(f"Event data: {event_data}")
        _LOGGER.error(f"Event data keys: {list(event_data.keys()) if isinstance(event_data, dict) else 'Not a dict'}")
        
        # Extract event information
        # Nest events use: nest_event_id (not event_id), and type like "camera_person" or "camera_motion"
        event_type = event_data.get("type")
        device_id = event_data.get("device_id")
        nest_event_id = event_data.get("nest_event_id")  # Nest uses nest_event_id, not event_id
        
        if not all([event_type, device_id, nest_event_id]):
            _LOGGER.warning(f"Incomplete Nest event data: {event_data}")
            return
        
        # Only process motion/person events
        # Nest uses "camera_person" and "camera_motion" instead of just "person" and "motion"
        if event_type not in ["camera_motion", "camera_person"]:
            _LOGGER.debug(f"Skipping Nest event type: {event_type}")
            return
        
        _LOGGER.error(f"Processing Nest event: type={event_type}, device={device_id}, nest_event_id={nest_event_id}")
        
        # Skip API thumbnail fetch - Nest thumbnails expire too quickly
        # Go straight to filesystem extraction from MP4 videos (reliable and always works)
        # Filesystem structure: /config/nest/event_media/<device_id>/<timestamp>-camera_person.mp4
        _LOGGER.info("Extracting frame from Nest video filesystem (skipping API thumbnail fetch)")
        image_data = await self._fetch_nest_image_from_filesystem_by_timestamp(device_id, event_data)
        
        if image_data:
            # Send to add-on for processing
            await self._send_to_addon(event_data, image_data)
        else:
            _LOGGER.warning(f"Failed to fetch Nest image for event {nest_event_id}")
    
    async def _fetch_nest_image_from_api(self, image_url: str) -> Optional[bytes]:
        """Fetch image from Nest API endpoint.
        
        This is the preferred method as it uses the official Nest API.
        Falls back to filesystem if this fails.
        
        Args:
            image_url: Relative URL path (e.g., /api/nest/event_media/.../thumbnail)
            
        Returns:
            Image bytes (JPEG), or None if failed
        """
        try:
            from homeassistant.helpers import aiohttp_client
            
            # Get a fresh session for internal API calls
            session = aiohttp_client.async_get_clientsession(self.hass)
            
            # Construct full URL
            # Use internal_url if available, otherwise default to localhost
            # hass.config.api doesn't have base_url, use internal_url or default
            try:
                base_url = self.hass.config.internal_url or "http://127.0.0.1:8123"
            except AttributeError:
                # Fallback if internal_url not available
                base_url = "http://127.0.0.1:8123"
            
            full_url = f"{base_url}{image_url}"
            
            _LOGGER.error(f"Fetching Nest image from HA API: {full_url}")
            
            # Add authentication header if we have HA API token
            headers = {}
            if self.ha_api_token:
                headers["Authorization"] = f"Bearer {self.ha_api_token}"
                _LOGGER.error("Using HA API token for authentication")
            else:
                _LOGGER.warning("No HA API token - API request may fail")
            
            # Fetch image (with timeout - Nest URLs expire quickly)
            async with session.get(
                full_url,
                headers=headers if headers else None,
                timeout=10
            ) as response:
                if response.status == 200:
                    image_data = await response.read()
                    _LOGGER.error(f"Successfully fetched Nest image via API ({len(image_data)} bytes)")
                    return image_data
                elif response.status == 404:
                    _LOGGER.warning(f"Nest media expired or not found (404)")
                    return None
                else:
                    response_text = await response.text()
                    _LOGGER.error(f"Failed to fetch Nest image via API: {response.status} - {response_text[:200]}")
                    return None
                    
        except asyncio.TimeoutError:
            _LOGGER.error(f"Timeout fetching Nest image from API (URL may have expired)")
            return None
        except Exception as e:
            _LOGGER.exception(f"Error fetching Nest image from API: {e}")
            return None
    
    async def _fetch_nest_image_from_filesystem_by_timestamp(self, device_id: str, event_data: Dict[str, Any]) -> Optional[bytes]:
        """Fetch image from Nest event media filesystem by matching timestamp.
        
        Nest stores MP4 videos at: /config/nest/event_media/<device_id>/<timestamp>-camera_person.mp4
        We match the event timestamp to find the corresponding video file.
        
        Args:
            device_id: Nest device ID (hash string like "65563380bfcf5478f63ff88485eca57")
            event_data: Full Nest event data (contains timestamp)
            
        Returns:
            Image bytes (JPEG), or None if failed
        """
        try:
            # Get Home Assistant config directory
            config_dir = Path(self.hass.config.config_dir)
            
            # Nest stores media at: /config/nest/event_media/<device_id>/
            # All videos are in the device folder directly (no event ID subfolders)
            nest_media_dir = config_dir / "nest" / "event_media" / device_id
            
            _LOGGER.error(f"Looking for Nest videos in: {nest_media_dir}")
            
            if not nest_media_dir.exists():
                _LOGGER.warning(f"Nest media directory not found: {nest_media_dir}")
                return None
            
            if not nest_media_dir.is_dir():
                _LOGGER.warning(f"Nest media path is not a directory: {nest_media_dir}")
                return None
            
            # Get event timestamp
            event_timestamp = event_data.get("timestamp")
            event_time_fired = event_data.get("time_fired")  # From event object
            
            # Try to parse timestamp
            target_timestamp = None
            if event_timestamp:
                try:
                    from datetime import datetime
                    if isinstance(event_timestamp, str):
                        dt = datetime.fromisoformat(event_timestamp.replace('Z', '+00:00'))
                        target_timestamp = int(dt.timestamp())
                    elif hasattr(event_timestamp, 'timestamp'):
                        target_timestamp = int(event_timestamp.timestamp())
                except Exception as e:
                    _LOGGER.warning(f"Could not parse event timestamp: {e}")
            
            # If we have a timestamp, try to find matching video
            # Video filenames are like: 1767607742-camera_person.mp4 (timestamp prefix)
            video_file = None
            
            if target_timestamp:
                # Look for video with matching timestamp (within 5 seconds tolerance)
                # Videos are named: <timestamp>-camera_person.mp4
                for tolerance in [0, 1, 2, 3, 4, 5]:  # Try exact match first, then widen tolerance
                    for offset in [-tolerance, tolerance]:
                        if offset == 0:
                            continue
                        test_timestamp = target_timestamp + offset
                        test_filename = f"{test_timestamp}-camera_person.mp4"
                        test_path = nest_media_dir / test_filename
                        if test_path.exists():
                            video_file = test_path
                            _LOGGER.error(f"Found matching video by timestamp: {test_filename}")
                            break
                    if video_file:
                        break
                
                # Also try exact match
                exact_filename = f"{target_timestamp}-camera_person.mp4"
                exact_path = nest_media_dir / exact_filename
                if exact_path.exists():
                    video_file = exact_path
                    _LOGGER.error(f"Found exact timestamp match: {exact_filename}")
            
            # If no timestamp match, get the most recent video file
            if not video_file:
                _LOGGER.warning("Could not match by timestamp, using most recent video")
                video_files = list(nest_media_dir.glob("*-camera_person.mp4"))
                if not video_files:
                    video_files = list(nest_media_dir.glob("*.mp4"))
                
                if video_files:
                    # Sort by modification time, get most recent
                    video_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                    video_file = video_files[0]
                    _LOGGER.error(f"Using most recent video: {video_file.name}")
                else:
                    available_files = [f.name for f in nest_media_dir.iterdir() if f.is_file()]
                    _LOGGER.warning(
                        f"No MP4 video file found in {nest_media_dir}. "
                        f"Available files: {available_files}"
                    )
                    return None
            
            if not video_file:
                _LOGGER.error("No video file found")
                return None
            
            _LOGGER.error(f"Found Nest video file: {video_file}")
            
            # Extract frames from video
            image_data = await self._extract_frames_from_video(video_file)
            
            if image_data:
                _LOGGER.error(f"Successfully extracted frame from Nest video ({len(image_data)} bytes)")
                return image_data
            else:
                _LOGGER.warning("Failed to extract frame from video")
                return None
                    
        except Exception as e:
            _LOGGER.exception(f"Error reading Nest video from filesystem: {e}")
            return None
    
    async def _extract_frames_from_video(self, video_path: Path) -> Optional[bytes]:
        """Extract frames from MP4 video file.
        
        Extracts 4 frames evenly spaced throughout the 1-second video:
        - Frame 1: 0.0s (start)
        - Frame 2: 0.25s
        - Frame 3: 0.5s (middle)
        - Frame 4: 0.75s
        
        Returns the middle frame (0.5s) as JPEG, which is usually the clearest.
        
        Args:
            video_path: Path to MP4 video file
            
        Returns:
            JPEG image bytes, or None if failed
        """
        try:
            # Try using ffmpeg first (commonly available in HA environment)
            import subprocess
            import tempfile
            
            # Extract frame at 0.5 seconds (middle of 1-second video)
            # This is usually the clearest frame
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            try:
                # Use ffmpeg to extract frame at 0.5 seconds
                # Command: ffmpeg -i input.mp4 -ss 0.5 -vframes 1 -q:v 2 output.jpg
                cmd = [
                    'ffmpeg',
                    '-i', str(video_path),
                    '-ss', '0.5',  # Extract frame at 0.5 seconds (middle)
                    '-vframes', '1',  # Extract 1 frame
                    '-q:v', '2',  # High quality JPEG (scale 2-31, lower is better)
                    '-y',  # Overwrite output file
                    tmp_path
                ]
                
                _LOGGER.error(f"Extracting frame from video using ffmpeg: {video_path}")
                
                # Run ffmpeg in a thread (blocking I/O)
                process = await asyncio.to_thread(
                    subprocess.run,
                    cmd,
                    capture_output=True,
                    timeout=10
                )
                
                if process.returncode != 0:
                    stderr = process.stderr.decode() if process.stderr else "Unknown error"
                    _LOGGER.warning(f"ffmpeg failed (will try Python library): {stderr}")
                    # Fall through to try Python library
                else:
                    # Read extracted frame
                    frame_path = Path(tmp_path)
                    if frame_path.exists() and frame_path.stat().st_size > 0:
                        image_data = await asyncio.to_thread(frame_path.read_bytes)
                        frame_path.unlink()  # Clean up temp file
                        _LOGGER.error(f"Successfully extracted frame using ffmpeg ({len(image_data)} bytes)")
                        return image_data
                    else:
                        _LOGGER.warning("Extracted frame file is empty or not found")
                        # Fall through to try Python library
                        
            except subprocess.TimeoutExpired:
                _LOGGER.warning("ffmpeg timed out, trying Python library")
            except Exception as e:
                _LOGGER.warning(f"Error running ffmpeg (will try Python library): {e}")
            finally:
                # Clean up temp file if it still exists
                tmp_frame = Path(tmp_path)
                if tmp_frame.exists():
                    try:
                        tmp_frame.unlink()
                    except:
                        pass
            
            # Fallback: Try using Python library (opencv-python or imageio)
            # Note: These libraries need to be added to integration dependencies if used
            try:
                _LOGGER.error("Trying to extract frame using Python library")
                return await self._extract_frame_with_python(video_path)
            except Exception as e:
                _LOGGER.exception(f"Python library extraction also failed: {e}")
                return None
                        
        except Exception as e:
            _LOGGER.exception(f"Error extracting frame from video: {e}")
            return None
    
    async def _extract_frame_with_python(self, video_path: Path) -> Optional[bytes]:
        """Extract frame using Python library (fallback if ffmpeg not available).
        
        Args:
            video_path: Path to MP4 video file
            
        Returns:
            JPEG image bytes, or None if failed
        """
        try:
            # Try opencv-python first (cv2)
            try:
                import cv2
                import io
                
                # Read video file
                video_data = await asyncio.to_thread(video_path.read_bytes)
                
                # Create temporary file-like object
                video_buffer = io.BytesIO(video_data)
                
                # Open video with OpenCV
                # Note: cv2.VideoCapture might need a file path, not BytesIO
                # So we'll use the file path directly
                cap = cv2.VideoCapture(str(video_path))
                
                if not cap.isOpened():
                    _LOGGER.error("Failed to open video with OpenCV")
                    return None
                
                # Get total frames and fps
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
                
                # Extract frame at 0.5 seconds (middle of 1-second video)
                target_frame = int(0.5 * fps)
                cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
                
                ret, frame = cap.read()
                cap.release()
                
                if not ret or frame is None:
                    _LOGGER.error("Failed to read frame from video")
                    return None
                
                # Encode frame as JPEG
                _, jpeg_data = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                
                if jpeg_data is not None:
                    image_bytes = jpeg_data.tobytes()
                    _LOGGER.error(f"Successfully extracted frame using OpenCV ({len(image_bytes)} bytes)")
                    return image_bytes
                else:
                    _LOGGER.error("Failed to encode frame as JPEG")
                    return None
                    
            except ImportError:
                _LOGGER.warning("OpenCV not available, trying imageio")
                # Try imageio as fallback
                import imageio
                import numpy as np
                from PIL import Image
                import io
                
                # Read video
                reader = imageio.get_reader(str(video_path))
                
                # Get frame at middle (assuming 30 fps, frame 15 is at 0.5s)
                try:
                    frame_count = reader.count_frames()
                    target_frame = frame_count // 2  # Middle frame
                    frame = reader.get_data(target_frame)
                    reader.close()
                    
                    # Convert to PIL Image and save as JPEG
                    img = Image.fromarray(frame)
                    jpeg_buffer = io.BytesIO()
                    img.save(jpeg_buffer, format='JPEG', quality=95)
                    image_bytes = jpeg_buffer.getvalue()
                    
                    _LOGGER.error(f"Successfully extracted frame using imageio ({len(image_bytes)} bytes)")
                    return image_bytes
                    
                except Exception as e:
                    _LOGGER.error(f"imageio extraction failed: {e}")
                    return None
                    
        except ImportError as e:
            _LOGGER.error(f"Required Python libraries not available: {e}")
            _LOGGER.error("Please install opencv-python or imageio in Home Assistant environment")
            return None
        except Exception as e:
            _LOGGER.exception(f"Error extracting frame with Python library: {e}")
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
            # Convert timestamp to string if it's a datetime object
            timestamp = event_data.get("timestamp")
            if timestamp and hasattr(timestamp, 'isoformat'):
                timestamp = timestamp.isoformat()
            elif not timestamp:
                timestamp = ""
            
            payload = {
                "event_type": "nest_event",
                "device_id": event_data.get("device_id"),
                "event_id": event_data.get("nest_event_id"),  # Use nest_event_id
                "event_type_nest": event_data.get("type"),
                "camera": event_data.get("device_id"),  # Use device_id as camera identifier
                "image_size": len(image_data),
                "timestamp": timestamp,
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            
            _LOGGER.error(f"Sending Nest event to add-on at: {self.api_url}/event")
            _LOGGER.error(f"Payload keys: {list(payload.keys())}")
            _LOGGER.error(f"Payload: {payload}")
            _LOGGER.error(f"Headers: {headers}")
            
            # Make sure we're using the correct session
            if not self._session:
                _LOGGER.error("Session not initialized!")
                return
            
            try:
                _LOGGER.error(f"Making POST request to {self.api_url}/event")
                _LOGGER.error(f"Request URL: {self.api_url}/event")
                _LOGGER.error(f"Request headers: {headers}")
                _LOGGER.error(f"Payload size: {len(str(payload))} bytes")
                
                # Use explicit timeout and ensure proper connection handling
                timeout = aiohttp.ClientTimeout(total=60, connect=10, sock_read=30, sock_connect=10)
                
                # Send request and handle response separately to catch connection issues
                response = await self._session.post(
                    f"{self.api_url}/event",
                    json=payload,
                    headers=headers,
                    timeout=timeout,
                    allow_redirects=False
                )
                
                _LOGGER.info(f"Response received: status={response.status}")
                _LOGGER.info(f"Response headers: {dict(response.headers)}")
                
                async with response:
                    if response.status == 200:
                        response_data = await response.json()
                        _LOGGER.info(f"Successfully sent Nest event to add-on: {response_data}")
                    else:
                        response_text = await response.text()
                        _LOGGER.error(f"Failed to send event to add-on: {response.status} - {response_text[:200]}")
            except asyncio.TimeoutError:
                _LOGGER.error(f"Timeout connecting to add-on at {self.api_url}/event - is the add-on running?")
            except ConnectionError as e:
                _LOGGER.error(f"Connection error to add-on at {self.api_url}/event: {e}")
                _LOGGER.error("Check if add-on is running and port is correct (default: 8080)")
            except Exception as e:
                _LOGGER.exception(f"Error sending event to add-on at {self.api_url}/event: {e}")
        except Exception as e:
            _LOGGER.exception(f"Unexpected error in _send_to_addon: {e}")

