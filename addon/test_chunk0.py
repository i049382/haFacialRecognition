#!/usr/bin/env python3
"""Comprehensive test suite for Chunk 0: Configuration & Credentials.

This test suite validates all Chunk 0 deliverables:
1. Configuration loading from options.json
2. Secret loading from secrets.yaml
3. Configuration validation
4. Error handling
5. Graceful degradation
"""

import json
import yaml
import tempfile
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from face_recognition_addon.config import ConfigLoader, Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_result(self, test_name: str, passed: bool, message: str = ""):
        """Add a test result."""
        self.tests.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
        if passed:
            self.passed += 1
            logger.info(f"✅ {test_name}: PASSED {message}")
        else:
            self.failed += 1
            logger.error(f"❌ {test_name}: FAILED {message}")
    
    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        logger.info("=" * 70)
        logger.info(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            logger.error("Failed tests:")
            for test in self.tests:
                if not test["passed"]:
                    logger.error(f"  - {test['name']}: {test['message']}")
        logger.info("=" * 70)
        return self.failed == 0


def test_valid_configuration():
    """Test 1: Load valid configuration."""
    logger.info("\n" + "="*70)
    logger.info("TEST 1: Valid Configuration Loading")
    logger.info("="*70)
    
    results = TestResults()
    
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
        
        # Validate all fields
        results.add_result(
            "confidence_threshold",
            config.confidence_threshold == 0.80,
            f"Expected 0.80, got {config.confidence_threshold}"
        )
        
        results.add_result(
            "review_threshold",
            config.review_threshold == 0.65,
            f"Expected 0.65, got {config.review_threshold}"
        )
        
        results.add_result(
            "camera_paths",
            len(config.camera_paths) == 2 and config.camera_paths[0] == "/data/cameras/cam1",
            f"Expected 2 paths, got {len(config.camera_paths)}"
        )
        
        results.add_result(
            "enable_daily_poll",
            config.enable_daily_poll is True,
            f"Expected True, got {config.enable_daily_poll}"
        )
        
        results.add_result(
            "daily_poll_time",
            config.daily_poll_time == "03:00",
            f"Expected '03:00', got {config.daily_poll_time}"
        )
        
        results.add_result(
            "api_port",
            config.api_port == 8080,
            f"Expected 8080, got {config.api_port}"
        )
        
        results.add_result(
            "drive_folder_id",
            config.drive_folder_id == "test_folder_123",
            f"Expected 'test_folder_123', got {config.drive_folder_id}"
        )
        
        results.add_result(
            "api_token",
            config.api_token == "test_token_123",
            f"Expected 'test_token_123', got {config.api_token}"
        )
        
    except Exception as e:
        results.add_result("config_loading", False, f"Exception: {e}")
        logger.exception("Unexpected exception")
    finally:
        Path(config_path).unlink()
    
    return results.summary()


def test_missing_config_file():
    """Test 2: Handle missing configuration file gracefully."""
    logger.info("\n" + "="*70)
    logger.info("TEST 2: Missing Configuration File")
    logger.info("="*70)
    
    loader = ConfigLoader(config_path="/nonexistent/path/options.json")
    
    try:
        config = loader.load()
        logger.error("Should have raised FileNotFoundError")
        return False
    except FileNotFoundError as e:
        if "Configuration file not found" in str(e):
            logger.info("✅ Correctly raises FileNotFoundError with helpful message")
            return True
        else:
            logger.error(f"Wrong error message: {e}")
            return False
    except Exception as e:
        logger.error(f"Unexpected exception: {e}")
        return False


def test_invalid_thresholds():
    """Test 3: Validate threshold values."""
    logger.info("\n" + "="*70)
    logger.info("TEST 3: Threshold Validation")
    logger.info("="*70)
    
    results = TestResults()
    
    # Test 3a: review_threshold >= confidence_threshold
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
        results.add_result("threshold_validation", False, "Should have raised ValueError")
    except ValueError as e:
        if "review_threshold" in str(e) and "confidence_threshold" in str(e):
            results.add_result("threshold_validation", True, "Correctly validates threshold relationship")
        else:
            results.add_result("threshold_validation", False, f"Wrong error: {e}")
    except Exception as e:
        results.add_result("threshold_validation", False, f"Unexpected exception: {e}")
    finally:
        Path(config_path).unlink()
    
    # Test 3b: confidence_threshold out of range
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "confidence_threshold": 1.5,  # Invalid: > 1.0
            "review_threshold": 0.60,
            "camera_paths": [],
            "api_port": 8080
        }
        json.dump(config_data, f)
        config_path = f.name
    
    try:
        loader = ConfigLoader(config_path=config_path)
        config = loader.load()
        results.add_result("threshold_range", False, "Should have raised ValueError")
    except ValueError as e:
        if "confidence_threshold" in str(e) and "0.0 and 1.0" in str(e):
            results.add_result("threshold_range", True, "Correctly validates threshold range")
        else:
            results.add_result("threshold_range", False, f"Wrong error: {e}")
    except Exception as e:
        results.add_result("threshold_range", False, f"Unexpected exception: {e}")
    finally:
        Path(config_path).unlink()
    
    return results.summary()


def test_invalid_time_format():
    """Test 4: Validate time format."""
    logger.info("\n" + "="*70)
    logger.info("TEST 4: Time Format Validation")
    logger.info("="*70)
    
    results = TestResults()
    
    invalid_times = [
        "25:00",  # Invalid hour
        "12:60",  # Invalid minute
        "12",     # Missing colon
        "12:00:00",  # Too many parts
        "abc",    # Not a number
    ]
    
    for invalid_time in invalid_times:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_data = {
                "confidence_threshold": 0.75,
                "review_threshold": 0.60,
                "daily_poll_time": invalid_time,
                "camera_paths": [],
                "api_port": 8080
            }
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            loader = ConfigLoader(config_path=config_path)
            config = loader.load()
            results.add_result(
                f"time_validation_{invalid_time}",
                False,
                f"Should have raised ValueError for '{invalid_time}'"
            )
        except ValueError as e:
            if "daily_poll_time" in str(e) or "HH:MM" in str(e):
                results.add_result(
                    f"time_validation_{invalid_time}",
                    True,
                    f"Correctly rejects '{invalid_time}'"
                )
            else:
                results.add_result(
                    f"time_validation_{invalid_time}",
                    False,
                    f"Wrong error for '{invalid_time}': {e}"
                )
        except Exception as e:
            results.add_result(
                f"time_validation_{invalid_time}",
                False,
                f"Unexpected exception: {e}"
            )
        finally:
            Path(config_path).unlink()
    
    return results.summary()


def test_missing_secrets():
    """Test 5: Handle missing secrets gracefully."""
    logger.info("\n" + "="*70)
    logger.info("TEST 5: Missing Secrets (Non-Fatal)")
    logger.info("="*70)
    
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
        if config.drive_credentials is None:
            logger.info("✅ Correctly handles missing secrets (non-fatal)")
            return True
        else:
            logger.error(f"Expected None credentials, got: {config.drive_credentials}")
            return False
        
    except Exception as e:
        logger.error(f"Unexpected exception: {e}")
        return False
    finally:
        Path(config_path).unlink()


def test_secrets_loading():
    """Test 6: Load secrets from secrets.yaml."""
    logger.info("\n" + "="*70)
    logger.info("TEST 6: Secrets Loading")
    logger.info("="*70)
    
    # Create temporary secrets.yaml
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as secrets_file:
        secrets_data = {
            "face_recognition_drive_credentials": '{"type": "service_account", "project_id": "test"}'
        }
        yaml.dump(secrets_data, secrets_file)
        secrets_path = secrets_file.name
    
    # Create temporary options.json
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
        loader = ConfigLoader(config_path=config_path)
        loader.secrets_path = Path(secrets_path)
        config = loader.load()
        
        if config.drive_credentials and "service_account" in config.drive_credentials:
            logger.info("✅ Correctly loads secrets from secrets.yaml")
            return True
        else:
            logger.error(f"Failed to load secrets. Got: {config.drive_credentials}")
            return False
        
    except Exception as e:
        logger.error(f"Unexpected exception: {e}")
        return False
    finally:
        Path(config_path).unlink()
        Path(secrets_path).unlink()


def test_default_values():
    """Test 7: Default values when options are missing."""
    logger.info("\n" + "="*70)
    logger.info("TEST 7: Default Values")
    logger.info("="*70)
    
    # Minimal config with only required fields
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "confidence_threshold": 0.75,
            "review_threshold": 0.60,
            "api_port": 8080
        }
        json.dump(config_data, f)
        config_path = f.name
    
    try:
        loader = ConfigLoader(config_path=config_path)
        loader.secrets_path = Path("/nonexistent/secrets.yaml")
        config = loader.load()
        
        # Check defaults
        defaults_correct = (
            config.camera_paths == [] and
            config.enable_daily_poll is False and
            config.daily_poll_time == "02:00" and
            config.drive_folder_id == "" and
            config.api_token == ""
        )
        
        if defaults_correct:
            logger.info("✅ Default values are correct")
            return True
        else:
            logger.error(f"Default values incorrect: camera_paths={config.camera_paths}, "
                        f"enable_daily_poll={config.enable_daily_poll}, "
                        f"daily_poll_time={config.daily_poll_time}")
            return False
        
    except Exception as e:
        logger.error(f"Unexpected exception: {e}")
        return False
    finally:
        Path(config_path).unlink()


def main():
    """Run all tests."""
    logger.info("\n" + "="*70)
    logger.info("CHUNK 0 TEST SUITE: Configuration & Credentials")
    logger.info("="*70)
    
    tests = [
        ("Valid Configuration", test_valid_configuration),
        ("Missing Config File", test_missing_config_file),
        ("Invalid Thresholds", test_invalid_thresholds),
        ("Invalid Time Format", test_invalid_time_format),
        ("Missing Secrets", test_missing_secrets),
        ("Secrets Loading", test_secrets_loading),
        ("Default Values", test_default_values),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.exception(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("TEST SUMMARY")
    logger.info("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("="*70)
    logger.info(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 ALL TESTS PASSED! Chunk 0 is ready.")
        return 0
    else:
        logger.error(f"\n⚠️  {total - passed} test(s) failed. Please fix issues before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

