"""HTTP API server for face recognition add-on."""

import logging
from flask import Flask, request, jsonify
from typing import Optional

logger = logging.getLogger(__name__)


class FaceRecognitionAPI:
    """HTTP API server for IPC between add-on and HA integration."""
    
    def __init__(self, config, event_callback=None):
        """Initialize API server.
        
        Args:
            config: Config object with API settings
            event_callback: Optional callback function for events
        """
        self.config = config
        self.event_callback = event_callback
        self.app = Flask(__name__)
        self.app.config['JSON_SORT_KEYS'] = False
        
        # Register routes
        self._register_routes()
        
    def _register_routes(self):
        """Register API routes."""
        logger.info("Registering API routes...")
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Get add-on status."""
            logger.info("GET /status endpoint called")
            response = {
                "status": "ready",
                "version": "0.0.1",
                "chunk": "3"
            }
            logger.info(f"Returning status response: {response}")
            return jsonify(response), 200
        
        @self.app.route('/event', methods=['POST'])
        def post_event():
            """Receive recognition event from add-on processing."""
            try:
                logger.info("POST /event received")
                
                # Check authentication if token is configured
                if self.config.api_token:
                    auth_header = request.headers.get('Authorization', '')
                    if not auth_header.startswith('Bearer '):
                        logger.warning("Missing or invalid Authorization header")
                        return jsonify({"error": "Missing or invalid Authorization header"}), 401
                    
                    token = auth_header.replace('Bearer ', '')
                    if token != self.config.api_token:
                        logger.warning("Invalid API token")
                        return jsonify({"error": "Invalid API token"}), 401
                else:
                    logger.debug("No API token configured, skipping authentication")
                
                # Validate request body
                if not request.is_json:
                    logger.warning("Request is not JSON")
                    return jsonify({"error": "Request must be JSON"}), 400
                
                data = request.get_json()
                logger.info(f"Received event data: {list(data.keys()) if data else 'None'}")
                
                # Check if this is a Nest ingestion event or recognition event
                if data.get('event_type') == 'nest_event':
                    # Nest ingestion event (Chunk 3)
                    logger.info(f"Nest event received: {data.get('event_type_nest')} on device {data.get('device_id')}")
                    
                    # For Chunk 3, just log the event
                    # In later chunks, we'll process the image for face recognition
                    image_size = data.get('image_size', 0)
                    logger.info(f"Image size: {image_size} bytes")
                    
                    response = jsonify({"status": "received", "type": "nest_ingestion"})
                    logger.info("Sending response for Nest event")
                    return response, 200
                else:
                    # Recognition event (Chunk 2+)
                    # Validate required fields
                    required_fields = ['person_id', 'display_name', 'confidence', 'camera']
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        logger.warning(f"Missing required fields: {missing_fields}")
                        return jsonify({
                            "error": "Missing required fields",
                            "missing": missing_fields
                        }), 400
                    
                    # Log event received
                    logger.info(f"Recognition event received: {data.get('person_id')} detected on {data.get('camera')}")
                    
                    # Call callback if provided (for future use)
                    if self.event_callback:
                        try:
                            self.event_callback(data)
                        except Exception as e:
                            logger.error(f"Error in event callback: {e}")
                    
                    response = jsonify({"status": "received", "type": "recognition"})
                    logger.info("Sending response for recognition event")
                    return response, 200
                    
            except Exception as e:
                logger.exception(f"Error processing /event request: {e}")
                return jsonify({"error": "Internal server error", "message": str(e)}), 500
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors."""
            return jsonify({"error": "Not found"}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 errors."""
            logger.exception("Internal server error")
            return jsonify({"error": "Internal server error"}), 500
        
        logger.info("API routes registered successfully")
    
    def run(self, host='0.0.0.0', port=None, debug=False, threaded=True, use_reloader=False):
        """Run the Flask server.
        
        Args:
            host: Host to bind to
            port: Port to bind to (uses config.api_port if None)
            debug: Enable debug mode
            threaded: Enable threading
            use_reloader: Enable auto-reload (disabled in add-on environment)
        """
        port = port or self.config.api_port
        logger.info(f"Starting HTTP API server on {host}:{port}")
        # Use threaded=True and increase request timeout
        # Also set max_content_length to handle larger payloads
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
        self.app.run(host=host, port=port, debug=debug, threaded=threaded, use_reloader=use_reloader)

