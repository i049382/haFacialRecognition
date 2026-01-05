"""Test script for configuration loading (Chunk 0 testing)."""

import json
import tempfile
import logging
from pathlib import Path
from face_recognition_addon.config import ConfigLoader, Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_config_loading():
    """Test configuration loading with valid config."""
    logger.info("Test 1: Valid configuration")
    
    # Create temporary options.json
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "confidence_threshold": 0.80,
            "review_threshold": 0.65,
            "camera_paths": ["/data/cameras/cam1", "/data/cameras/cam2"],
            "enable_daily_poll": True,
            "daily_poll_time": "03:00",
            "drive_folder_id": "test_folder_123",
            "api_port": 8080,
            "api_token": "test_token_123"
        }
        json.dump(config_data, f)
        config_path = f.name
    
    try:
        loader = ConfigLoader(config_path=config_path)
        config = loader.load()
        
        assert config.confidence_threshold == 0.80
        assert config.review_threshold == 0.65
        assert len(config.camera_paths) == 2
        assert config.enable_daily_poll is True
        assert config.daily_poll_time == "03:00"
        assert config.api_port == 8080
        
        logger.info("✅ Test 1 passed: Valid configuration loaded correctly")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test 1 failed: {e}")
        return False
    finally:
        Path(config_path).unlink()


def test_missing_config():
    """Test graceful failure when config file is missing."""
    logger.info("Test 2: Missing configuration file")
    
    loader = ConfigLoader(config_path="/nonexistent/path/options.json")
    
    try:
        config = loader.load()
        logger.error("❌ Test 2 failed: Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        logger.info("✅ Test 2 passed: Gracefully handles missing config file")
        return True
    except Exception as e:
        logger.error(f"❌ Test 2 failed: Unexpected exception: {e}")
        return False


def test_invalid_thresholds():
    """Test validation of threshold values."""
    logger.info("Test 3: Invalid threshold values")
    
    # Test: review_threshold >= confidence_threshold
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "confidence_threshold": 0.60,
            "review_threshold": 0.75,  # Invalid: review >= confidence
            "camera_paths": [],
            "api_port": 8080
        }
        json.dump(config_data, f)
        config_path = f.name
    
    try:
        loader = ConfigLoader(config_path=config_path)
        config = loader.load()
        logger.error("❌ Test 3 failed: Should have raised ValueError")
        return False
    except ValueError as e:
        if "review_threshold" in str(e):
            logger.info("✅ Test 3 passed: Correctly validates threshold relationship")
            return True
        else:
            logger.error(f"❌ Test 3 failed: Wrong validation error: {e}")
            return False
    except Exception as e:
        logger.error(f"❌ Test 3 failed: Unexpected exception: {e}")
        return False
    finally:
        Path(config_path).unlink()


def test_missing_secrets():
    """Test graceful handling of missing secrets."""
    logger.info("Test 4: Missing secrets (non-fatal)")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "confidence_threshold": 0.75,
            "review_threshold": 0.60,
            "camera_paths": [],
            "api_port": 8080
        }
        json.dump(config_data, f)
        config_path = f.name
    
    try:
        # Use nonexistent secrets path
        loader = ConfigLoader(config_path=config_path)
        loader.secrets_path = Path("/nonexistent/secrets.yaml")
        config = loader.load()
        
        # Should load successfully but with None credentials
        assert config.drive_credentials is None
        logger.info("✅ Test 4 passed: Gracefully handles missing secrets")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test 4 failed: {e}")
        return False
    finally:
        Path(config_path).unlink()


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("Chunk 0 Configuration Testing")
    logger.info("=" * 60)
    
    tests = [
        test_config_loading,
        test_missing_config,
        test_invalid_thresholds,
        test_missing_secrets,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            logger.exception(f"Test {test.__name__} crashed: {e}")
            results.append(False)
        logger.info("")
    
    logger.info("=" * 60)
    passed = sum(results)
    total = len(results)
    logger.info(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✅ All tests passed!")
        return 0
    else:
        logger.error("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

