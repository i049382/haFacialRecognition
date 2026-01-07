#!/usr/bin/env python3
"""Simple test to check if add-on is running."""

import requests
import sys

def test_addon():
    """Test if add-on API is responding."""
    try:
        print("Testing add-on connection...")

        # Test status endpoint
        response = requests.get("http://localhost:8080/status", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Add-on is RUNNING!")
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Chunk: {data.get('chunk')}")
            return True
        else:
            print(f"❌ Add-on responded with error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False

    except requests.ConnectionError:
        print("❌ Cannot connect to add-on on port 8080")
        print("   Check if add-on is started in HA Supervisor")
        return False
    except requests.Timeout:
        print("❌ Connection timeout - add-on not responding")
        return False
    except Exception as e:
        print(f"❌ Error testing add-on: {e}")
        return False

def test_post():
    """Test POST request to add-on."""
    try:
        print("\nTesting POST request...")

        test_data = {
            "event_type": "test",
            "device_id": "test_device",
            "event_id": "test_event",
            "event_type_nest": "camera_person",
            "camera": "test_camera",
            "image_size": 12345,
            "timestamp": "2026-01-07T21:01:25.006000+00:00"
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            "http://localhost:8080/event",
            json=test_data,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ POST request SUCCESS!")
            print(f"   Response: {data}")
            return True
        else:
            print(f"❌ POST request failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False

    except requests.ConnectionError as e:
        print(f"❌ POST connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ POST test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Face Recognition Add-on Diagnostic Test")
    print("=" * 50)

    # Test 1: Basic connection
    if not test_addon():
        print("\n💡 TROUBLESHOOTING:")
        print("1. Check add-on is STARTED in HA Supervisor")
        print("2. Check add-on logs for errors")
        print("3. Try changing api_port in add-on config")
        print("4. Make sure you have latest __main__.py (Gunicorn disabled)")
        sys.exit(1)

    # Test 2: POST request
    test_post()

    print("\n" + "=" * 50)
    print("Diagnostic complete!")
    print("=" * 50)