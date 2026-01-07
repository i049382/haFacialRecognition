#!/usr/bin/env python3
"""Minimal test endpoint to replace the current one temporarily."""

from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Store config globally (simplified)
class SimpleConfig:
    def __init__(self):
        self.api_token = ""  # No authentication for now

config = SimpleConfig()

@app.route('/status', methods=['GET'])
def get_status():
    """Simple status endpoint."""
    logger.info("GET /status")
    return jsonify({"status": "ready", "version": "0.0.1", "chunk": "3"}), 200

@app.route('/event', methods=['POST'])
def post_event():
    """MINIMAL event endpoint - just log and return success."""
    try:
        logger.error("=" * 60)
        logger.error("=== MINIMAL POST /event CALLED ===")
        logger.error(f"Remote: {request.remote_addr}")

        # Basic request info
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Content-Type: {request.content_type}")

        # Try to get and log data
        if request.data:
            logger.info(f"Data length: {len(request.data)} bytes")
            try:
                # Try to parse as JSON
                import json as json_module
                data = json_module.loads(request.data)
                logger.info(f"Parsed JSON keys: {list(data.keys())}")
                logger.info(f"Event type: {data.get('event_type', 'unknown')}")
            except:
                logger.info("Could not parse JSON, showing raw data:")
                logger.info(request.data[:200])

        # ALWAYS return success
        response = {
            "status": "received",
            "type": "nest_ingestion",
            "minimal": True,
            "message": "Minimal endpoint working"
        }
        logger.error("=== RETURNING SUCCESS ===")
        return jsonify(response), 200

    except Exception as e:
        logger.exception(f"MINIMAL ENDPOINT ERROR: {e}")
        # Still return 200 to prevent client retries
        return jsonify({"status": "error_but_ok", "error": str(e)}), 200

@app.errorhandler(Exception)
def handle_all_errors(error):
    """Catch ALL errors."""
    logger.exception(f"GLOBAL ERROR HANDLER: {error}")
    # Return 200 so client doesn't retry
    return jsonify({"global_error": str(type(error).__name__)}), 200

if __name__ == '__main__':
    logger.info("Starting MINIMAL test server on port 8080")
    logger.info("This will replace the current endpoint temporarily")
    logger.info("Use: curl -X POST http://localhost:8080/event -H 'Content-Type: application/json' -d '{\"test\":true}'")
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)