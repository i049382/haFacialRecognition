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
        
        # Try to use gunicorn first (production WSGI server)
        # Falls back to Flask dev server if gunicorn fails
        logger.info("Checking for Gunicorn availability...")
        use_gunicorn = False
        try:
            import gunicorn.app.base
            logger.info("Gunicorn found! Attempting to start...")
            use_gunicorn = True
            
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
                'workers': 1,
                'worker_class': 'sync',
                'timeout': 120,  # Increased timeout to 120 seconds
                'keepalive': 30,  # Increased keepalive to 30 seconds
                'graceful_timeout': 30,
                'accesslog': '-',
                'errorlog': '-',
                'loglevel': 'info',
                'preload_app': False,  # Don't preload app to avoid initialization issues
                'limit_request_line': 4094,  # Default limit for request line
                'limit_request_fields': 100,  # Default limit for request headers
                'limit_request_field_size': 8190,  # Default limit for header size
                'max_requests': 0,  # No limit on requests per worker
                'max_requests_jitter': 0,  # No jitter
                'worker_connections': 1000,  # Allow more concurrent connections
            }
            
            logger.info(f"Starting Gunicorn server on 0.0.0.0:{config.api_port}")
            StandaloneApplication(api, options).run()
            use_gunicorn = False  # Should never reach here
            
        except ImportError as e:
            logger.warning(f"Gunicorn not available: {e}")
            logger.warning("Falling back to Flask dev server")
            use_gunicorn = False
        except Exception as e:
            logger.error(f"Error starting Gunicorn: {e}")
            logger.exception("Falling back to Flask dev server")
            use_gunicorn = False
        
        # Fallback to Flask dev server
        if not use_gunicorn:
            try:
                logger.info(f"Starting Flask dev server on 0.0.0.0:{config.api_port}")
                logger.warning("Flask dev server is not production-ready - POST requests may disconnect")
                api.run(host='0.0.0.0', port=config.api_port, debug=False, threaded=True, use_reloader=False)
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
