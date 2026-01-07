#!/usr/bin/env python3
"""Test the add-on endpoint directly to diagnose ServerDisconnectedError."""

import requests
import json
import sys

def test_endpoint():
    """Test POST /event endpoint directly."""
    print("Testing POST /event endpoint directly...")
    print("=" * 60)

    # Test data matching what your integration sends
    test_payload = {
        "event_type": "nest_event",
        "device_id": "65563380bfcf5478f63ff88485eca57e",
        "event_id": "WyIxNzM3MDU5MDcxIiwgIjgwMzQ0OTUxNiJd",
        "event_type_nest": "camera_person",
        "camera": "65563380bfcf5478f63ff88485eca57e",
        "image_size": 62337,
        "timestamp": "2026-01-07T21:15:24.491000+00:00"
    }

    headers = {
        "Content-Type": "application/json"
    }

    url = "http://localhost:8080/event"

    print(f"URL: {url}")
    print(f"Payload: {json.dumps(test_payload, indent=2)}")
    print(f"Headers: {headers}")

    try:
        # First test if server is alive
        print("\n1. Testing server status...")
        status_response = requests.get("http://localhost:8080/status", timeout=5)
        print(f"   Status endpoint: {status_response.status_code}")
        if status_response.status_code == 200:
            print(f"   Status response: {status_response.json()}")
        else:
            print(f"   Status error: {status_response.text}")

        # Test POST request
        print("\n2. Testing POST request...")
        response = requests.post(
            url,
            json=test_payload,
            headers=headers,
            timeout=10
        )

        print(f"   Response status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")

        if response.status_code == 200:
            print(f"   ✅ SUCCESS! Response: {response.json()}")
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response text: {response.text[:500]}")
            return False

    except requests.ConnectionError as e:
        print(f"   ❌ ConnectionError: {e}")
        print("   Check if add-on is running on port 8080")
        return False
    except requests.Timeout as e:
        print(f"   ❌ Timeout: {e}")
        print("   Server not responding within timeout")
        return False
    except requests.exceptions.ServerDisconnectedError as e:
        print(f"   ❌ ServerDisconnectedError: {e}")
        print("   Server disconnected during request - Flask might be crashing")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {type(e).__name__}: {e}")
        return False

def test_with_different_content_type():
    """Test with data= instead of json= (what your integration uses)."""
    print("\n" + "=" * 60)
    print("Testing with data=json.dumps() (like your integration)...")
    print("=" * 60)

    test_payload = {
        "event_type": "nest_event",
        "device_id": "test_device",
        "event_id": "test_event",
        "event_type_nest": "camera_person",
        "camera": "test_camera",
        "image_size": 12345,
        "timestamp": "2026-01-07T21:15:24.491000+00:00"
    }

    headers = {"Content-Type": "application/json"}
    url = "http://localhost:8080/event"

    try:
        # Use data=json.dumps() like your integration does
        response = requests.post(
            url,
            data=json.dumps(test_payload),  # This is what causes issues sometimes
            headers=headers,
            timeout=10
        )

        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ SUCCESS with data=json.dumps()")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("Face Recognition Add-on Endpoint Diagnostic")
    print("=" * 60)

    # Test 1: Normal POST
    if not test_endpoint():
        print("\n💡 TROUBLESHOOTING:")
        print("1. Check add-on logs for '=== POST /event ENDPOINT CALLED ==='")
        print("2. Check for Flask crash/exception logs")
        print("3. Make sure you have updated api.py with better error handling")
        print("4. Check if Flask server is actually running")

    # Test 2: Alternative encoding
    test_with_different_content_type()

    print("\n" + "=" * 60)
    print("Diagnostic complete!")
    print("Check add-on logs for error messages.")