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
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Get add-on status."""
            return jsonify({
                "status": "ready",
                "version": "0.0.1",
                "chunk": "2"
            }), 200
        
        @self.app.route('/event', methods=['POST'])
        def post_event():
            """Receive recognition event from add-on processing."""
            # Check authentication if token is configured
            if self.config.api_token:
                auth_header = request.headers.get('Authorization', '')
                if not auth_header.startswith('Bearer '):
                    return jsonify({"error": "Missing or invalid Authorization header"}), 401
                
                token = auth_header.replace('Bearer ', '')
                if token != self.config.api_token:
                    return jsonify({"error": "Invalid API token"}), 401
            
            # Validate request body
            if not request.is_json:
                return jsonify({"error": "Request must be JSON"}), 400
            
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['person_id', 'display_name', 'confidence', 'camera']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "error": "Missing required fields",
                    "missing": missing_fields
                }), 400
            
            # Log event received
            logger.info(f"Event received: {data.get('person_id')} detected on {data.get('camera')}")
            
            # Call callback if provided (for future use)
            if self.event_callback:
                try:
                    self.event_callback(data)
                except Exception as e:
                    logger.error(f"Error in event callback: {e}")
            
            return jsonify({"status": "received"}), 200
        
        @self.app.errorhandler(404)
        def not_found(error):
            """Handle 404 errors."""
            return jsonify({"error": "Not found"}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """Handle 500 errors."""
            logger.exception("Internal server error")
            return jsonify({"error": "Internal server error"}), 500
    
    def run(self, host='0.0.0.0', port=None, debug=False):
        """Run the Flask server.
        
        Args:
            host: Host to bind to
            port: Port to bind to (uses config.api_port if None)
            debug: Enable debug mode
        """
        port = port or self.config.api_port
        logger.info(f"Starting HTTP API server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, threaded=True)

