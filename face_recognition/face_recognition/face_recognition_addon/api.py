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
        
        # Add before_request hook to log all incoming requests
        @self.app.before_request
        def log_request_info():
            logger.info(f"Incoming request: {request.method} {request.path}")
            logger.info(f"Request headers: {dict(request.headers)}")
            logger.info(f"Content-Type: {request.content_type}")
            logger.info(f"Content-Length: {request.content_length}")
        
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
            # Outer try-except to catch ANY crash
            try:
                # Log immediately when endpoint is called
                logger.error("=" * 60)
                logger.error("=== POST /event ENDPOINT CALLED ===")
                logger.error(f"Remote address: {request.remote_addr}")
                logger.error(f"Request method: {request.method}")
                logger.error(f"Request path: {request.path}")
                logger.error("=" * 60)

                # Inner try-except for request processing
                # Log basic request info
                logger.info("POST /event received")
                logger.info(f"Request headers: {dict(request.headers)}")
                logger.info(f"Content-Type: {request.content_type}")
                logger.info(f"Content-Length: {request.content_length}")

                # Check if we have data
                has_data = request.data is not None
                logger.info(f"Request data available: {has_data}")
                if has_data and request.data:
                    data_len = len(request.data)
                    logger.info(f"Request data length: {data_len} bytes")
                    # Log first 200 chars of data for debugging
                    if data_len > 0:
                        try:
                            data_preview = request.data[:200].decode('utf-8', errors='replace')
                            logger.info(f"Request data preview: {data_preview}")
                        except:
                            logger.info("Could not decode request data preview")
                
                # Check if config object exists (might be None)
                logger.info(f"Config object exists: {self.config is not None}")
                if self.config is None:
                    logger.error("CONFIG IS NONE! This will cause crashes.")
                    # Return error but don't crash
                    return jsonify({"error": "Configuration not loaded", "status": "config_error"}), 500

                # Check authentication if token is configured
                has_api_token = hasattr(self.config, 'api_token') and self.config.api_token
                logger.info(f"API token configured: {has_api_token}")

                if has_api_token:
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
                    logger.warning(f"Request is not JSON. Content-Type: {request.content_type}")
                    logger.warning(f"Request data (first 500 chars): {request.data[:500] if request.data else 'None'}")
                    return jsonify({"error": "Request must be JSON"}), 400

                # Try to parse JSON with better error handling
                try:
                    data = request.get_json()
                    if data is None:
                        logger.error("Failed to parse JSON - request.get_json() returned None")
                        logger.error(f"Request data: {request.data[:500] if request.data else 'None'}")
                        return jsonify({"error": "Invalid JSON"}), 400

                    logger.info(f"Received event data: {list(data.keys()) if data else 'None'}")
                except Exception as json_error:
                    logger.exception(f"Failed to parse JSON: {json_error}")
                    logger.error(f"Request data (first 500 chars): {request.data[:500] if request.data else 'None'}")
                    return jsonify({"error": "Invalid JSON format", "message": str(json_error)}), 400
                
                # Check the event type and handle accordingly
                event_type = data.get('event_type')

                if event_type == 'nest_event':
                    # Nest ingestion event (Chunk 3)
                    logger.info(f"Nest event received: {data.get('event_type_nest')} on device {data.get('device_id')}")

                    # For Chunk 3, just log the event
                    # In later chunks, we'll process the image for face recognition
                    image_size = data.get('image_size', 0)
                    logger.info(f"Image size: {image_size} bytes")

                    response = jsonify({"status": "received", "type": "nest_ingestion"})
                    logger.info("Sending response for Nest event")
                    return response, 200

                elif event_type == 'recognition_request':
                    # Service-based recognition request
                    logger.info(f"Recognition request received from source: {data.get('source', 'unknown')}")

                    # Validate required fields for recognition request
                    required_fields = ['image_data', 'camera']
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        logger.warning(f"Missing required fields for recognition request: {missing_fields}")
                        return jsonify({
                            "error": "Missing required fields",
                            "missing": missing_fields
                        }), 400

                    # Log request details
                    image_size = data.get('image_size', 0)
                    logger.info(f"Image size: {image_size} bytes, Camera: {data.get('camera')}")

                    # TODO: In future chunks, process the image_data for face recognition
                    # For now, just acknowledge receipt and simulate a response

                    # Simulate face recognition results (for testing)
                    # In Chunk 4+, this will be replaced with actual face recognition
                    simulated_response = {
                        "person_id": "unknown",
                        "display_name": "Unknown Person",
                        "confidence": 0.0,
                        "needs_review": True,
                        "face_count": 1,
                        "processing_time_ms": 50,
                        "status": "processed",
                        "message": "Recognition request received (simulated response for testing)"
                    }

                    logger.info(f"Sending simulated recognition response: {simulated_response}")
                    return jsonify(simulated_response), 200

                else:
                    # Legacy recognition event (Chunk 2+)
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
                    logger.info(f"Legacy recognition event received: {data.get('person_id')} detected on {data.get('camera')}")

                    # Call callback if provided (for future use)
                    if self.event_callback:
                        try:
                            self.event_callback(data)
                        except Exception as e:
                            logger.error(f"Error in event callback: {e}")

                    response = jsonify({"status": "received", "type": "recognition"})
                    logger.info("Sending response for legacy recognition event")
                    return response, 200
                    
            except Exception as e:
                logger.exception(f"Error processing /event request: {e}")
                return jsonify({"error": "Internal server error", "message": str(e)}), 500

            except Exception as outer_e:
                logger.exception(f"OUTER CATCH: Critical error in post_event: {outer_e}")
                logger.exception("Full traceback:")
                import traceback
                logger.exception(traceback.format_exc())
                return jsonify({"error": "Critical server error", "type": "outer_catch"}), 500
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors."""
            return jsonify({"error": "Not found"}), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 errors."""
            logger.exception("=== INTERNAL SERVER ERROR ===")
            logger.exception(f"Error: {error}")
            return jsonify({"error": "Internal server error"}), 500

        # Catch-all exception handler
        @self.app.errorhandler(Exception)
        def handle_all_exceptions(error):
            """Handle all uncaught exceptions."""
            logger.exception("=== UNCAUGHT EXCEPTION ===")
            logger.exception(f"Error type: {type(error).__name__}")
            logger.exception(f"Error: {error}")
            return jsonify({"error": "Internal server error", "type": type(error).__name__}), 500
        
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

