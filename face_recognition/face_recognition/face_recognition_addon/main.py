"""Main entry point for the face recognition add-on."""

import logging
import sys
from pathlib import Path

from face_recognition_addon.config import ConfigLoader

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
        logger.info("Add-on ready (Chunk 0 - Configuration only)")
        
        # TODO: In future chunks, start HTTP API server here
        # For now, keep running so HA doesn't think it crashed
        # This allows testing add-on installation and config loading
        logger.info("Waiting for future functionality... (Chunk 2+)")
        
        # Keep process alive for HA testing
        import time
        try:
            while True:
                time.sleep(60)  # Sleep for 1 minute, then check again
                logger.debug("Add-on still running (waiting for Chunk 2 implementation)")
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            return 0
        
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please configure the add-on in Home Assistant")
        return 1
        
    except ValueError as e:
        logger.error(f"Configuration validation error: {e}")
        return 1
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

