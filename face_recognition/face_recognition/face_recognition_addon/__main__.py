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
        logger.info("Add-on ready (Chunk 3 - Nest Event Ingestion)")
        
        # Start HTTP API server
        api = FaceRecognitionAPI(config)
        logger.info(f"HTTP API server starting on port {config.api_port}")
        
        # Use gunicorn for production WSGI server (better than Flask dev server)
        # Flask dev server has issues with POST requests and can disconnect
        try:
            import gunicorn.app.base
            import multiprocessing
            
            class StandaloneApplication(gunicorn.app.base.BaseApplication):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super().__init__()
                
                def load_config(self):
                    for key, value in self.options.items():
                        self.cfg.set(key.lower(), value)
                
                def load(self):
                    return self.application.app
            
            # Gunicorn options
            options = {
                'bind': f'0.0.0.0:{config.api_port}',
                'workers': 1,  # Single worker for add-on
                'worker_class': 'sync',
                'timeout': 30,
                'keepalive': 5,
                'accesslog': '-',  # Log to stdout
                'errorlog': '-',   # Log to stderr
                'loglevel': 'info',
            }
            
            logger.info(f"Starting Gunicorn server on 0.0.0.0:{config.api_port}")
            StandaloneApplication(api, options).run()
            
        except ImportError:
            # Fallback to Flask dev server if gunicorn not available
            logger.warning("Gunicorn not available, using Flask dev server (not recommended)")
            logger.info(f"Starting Flask server on 0.0.0.0:{config.api_port}")
            api.run(host='0.0.0.0', port=config.api_port, debug=False, threaded=True)
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
