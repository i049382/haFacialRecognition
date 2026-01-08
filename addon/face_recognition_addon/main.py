"""Main entry point for the face recognition add-on."""

import logging
import sys
from pathlib import Path

from face_recognition_addon.config import ConfigLoader
from face_recognition_addon.api import FaceRecognitionAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    logger.info("Starting Face Recognition Add-on")

    try:
        # Load configuration
        config_loader = ConfigLoader()
        config = config_loader.load()

        logger.info("Configuration loaded successfully")
        logger.info("Add-on ready (Service-based recognition)")

        # Start HTTP API server
        api = FaceRecognitionAPI(config)
        logger.info(f"HTTP API server starting on port {config.api_port}")

        # Use Flask development server (gunicorn can be enabled later)
        logger.info(f"Starting Flask dev server on 0.0.0.0:{config.api_port}")
        logger.info("Using Flask dev server (Gunicorn temporarily disabled for testing)")
        api.run(host='0.0.0.0', port=config.api_port, debug=False, threaded=True, use_reloader=False)

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please configure the add-on in Home Assistant")
        return 1

    except ValueError as e:
        logger.error(f"Configuration validation error: {e}")
        return 1

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        return 0

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())