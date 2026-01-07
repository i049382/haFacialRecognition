#!/usr/bin/env python3
"""Super simple Flask server for testing."""

from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def get_status():
    """Simple status endpoint."""
    logger.info("GET /status")
    return jsonify({"status": "ready", "test": "simple"}), 200

@app.route('/event', methods=['POST'])
def post_event():
    """Simple event endpoint - minimal code."""
    logger.error("=== SIMPLE TEST: POST /event called ===")
    logger.error(f"Remote: {request.remote_addr}")
    logger.error(f"Method: {request.method}")
    logger.error(f"Headers: {dict(request.headers)}")

    try:
        # Try to get data
        if request.data:
            logger.error(f"Data length: {len(request.data)} bytes")
            logger.error(f"Data (first 200 chars): {request.data[:200]}")

        # Try to parse JSON
        try:
            data = request.get_json()
            if data:
                logger.error(f"Parsed JSON keys: {list(data.keys())}")
        except:
            logger.error("Could not parse JSON")

        # Always return success
        response = {"status": "received", "simple": "test"}
        logger.error(f"Returning: {response}")
        return jsonify(response), 200

    except Exception as e:
        logger.exception(f"Error in simple endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(Exception)
def handle_all_errors(error):
    """Catch all errors."""
    logger.exception(f"Global error handler: {error}")
    return jsonify({"error": "Global handler caught error"}), 500

if __name__ == '__main__':
    logger.info("Starting SIMPLE test server on port 8081")
    logger.info("Use: curl -X POST http://localhost:8081/event -H 'Content-Type: application/json' -d '{\"test\":true}'")
    app.run(host='0.0.0.0', port=8081, debug=False, threaded=True)