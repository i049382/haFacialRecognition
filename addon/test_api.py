#!/usr/bin/env python3
"""Test script for Face Recognition Add-on HTTP API.

This script tests the add-on HTTP API endpoints without requiring
Home Assistant. It starts the API server in a background thread,
sends test requests, and verifies responses.

Usage:
    python test_api.py
"""

import sys
import json
import threading
import time
import requests
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from face_recognition_addon.config import Config, ConfigLoader


class MockConfig(Config):
    """Mock configuration for testing."""
    def __init__(self):
        super().__init__()
        self.api_port = 18080  # Use a different port to avoid conflicts
        self.api_token = "test_token_123"
        self.confidence_threshold = 0.75
        self.review_threshold = 0.60
        self.camera_paths = []
        self.enable_daily_poll = False
        self.daily_poll_time = "02:00"
        self.drive_folder_id = ""
        self.drive_credentials = None


def test_api():
    """Test the add-on HTTP API."""
    print("=== Face Recognition Add-on API Test ===")

    # Create mock config
    config = MockConfig()

    # Import and create API server
    from face_recognition_addon.api import FaceRecognitionAPI
    api = FaceRecognitionAPI(config)

    # Start server in background thread
    def run_server():
        api.run(host='127.0.0.1', port=config.api_port, debug=False, threaded=True, use_reloader=False)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait for server to start
    print(f"Waiting for server to start on 127.0.0.1:{config.api_port}...")
    time.sleep(3)

    base_url = f"http://127.0.0.1:{config.api_port}"

    try:
        # Test 1: GET /status
        print("\n1. Testing GET /status...")
        response = requests.get(f"{base_url}/status", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code != 200:
            print("   [FAIL] FAILED")
            return False
        print("   [OK] PASSED")

        # Test 2: POST /event with recognition_request (no auth)
        print("\n2. Testing POST /event (recognition_request, no auth)...")
        config.api_token = ""
        api.config = config  # Update API config
        payload = {
            "event_type": "recognition_request",
            "image_data": "test_base64_data",
            "camera": "test_camera",
            "source": "test"
        }
        response = requests.post(f"{base_url}/event", json=payload, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code != 200:
            print("   [FAIL] FAILED")
            return False
        print("   [OK] PASSED")

        # Test 3: POST /event with authentication (should fail without token)
        print("\n3. Testing POST /event with authentication (should fail without token)...")
        config.api_token = "test_token_123"
        api.config = config  # Update API config

        payload = {
            "event_type": "recognition_request",
            "image_data": "test_base64_data",
            "camera": "test_camera"
        }
        response = requests.post(f"{base_url}/event", json=payload, timeout=5)
        print(f"   Status: {response.status_code}")

        # Should return 401 because we didn't send token
        if response.status_code == 401:
            print("   [OK] Correctly rejected unauthorized request")
        else:
            print(f"   [FAIL] Expected 401, got {response.status_code}")
            return False

        # Test 4: POST /event with correct authentication
        print("\n4. Testing POST /event with correct authentication...")
        headers = {"Authorization": "Bearer test_token_123"}
        response = requests.post(f"{base_url}/event", json=payload, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code != 200:
            print("   [FAIL] FAILED")
            return False
        print("   [OK] PASSED")

        # Test 5: POST /event with unsupported event type
        print("\n5. Testing POST /event (unsupported event type)...")
        payload = {
            "event_type": "unsupported_event",
            "some_field": "test"
        }
        response = requests.post(f"{base_url}/event", json=payload, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Should return 400 with error about unsupported event type
        if response.status_code != 400:
            print("   [FAIL] FAILED - Expected 400 for unsupported event type")
            return False
        response_data = response.json()
        if "error" not in response_data or "Unsupported event type" not in response_data.get("error", ""):
            print("   [FAIL] FAILED - Expected error about unsupported event type")
            return False
        print("   [OK] PASSED")


        print("\n" + "="*60)
        print("*** All API tests passed!")
        print("="*60)
        return True

    except requests.exceptions.ConnectionError as e:
        print(f"[FAIL] Connection error: {e}")
        print("   Make sure the server started correctly")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Server will stop when thread exits (daemon)
        print("\nTest complete. Server will shut down.")
        # Note: Flask server doesn't have a clean shutdown in this simple test
        # In production, we'd use a proper shutdown mechanism


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)