#!/usr/bin/env python3
"""Test script to demonstrate the new recognize_face service usage."""

import base64
import json

# Example 1: Using image_data (base64 encoded image)
def example_with_base64():
    """Example showing how to use the service with base64 image data."""

    # In a real automation, you would get the image bytes from somewhere
    # For this example, we'll create a minimal base64 string
    # In practice, you would read an image file:
    # with open("test.jpg", "rb") as f:
    #     image_bytes = f.read()
    #     base64_data = base64.b64encode(image_bytes).decode('utf-8')

    # Minimal valid base64 string (1x1 pixel black PNG)
    minimal_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    service_data = {
        "image_data": minimal_png_base64,
        "camera": "front_door_camera",
        "display_name": "Test Image"  # Optional: for logging
    }

    print("Example 1 - Using base64 image data:")
    print(f"Service call: face_recognition.recognize_face")
    print(f"Service data: {json.dumps(service_data, indent=2)}")
    print()

# Example 2: Using image_url
def example_with_url():
    """Example showing how to use the service with image URL."""

    service_data = {
        "image_url": "http://homeassistant.local:8123/api/camera_proxy/camera.front_door",
        "camera": "front_door_camera"
    }

    print("Example 2 - Using image URL:")
    print(f"Service call: face_recognition.recognize_face")
    print(f"Service data: {json.dumps(service_data, indent=2)}")
    print()

# Example 3: Using entity_id (camera entity)
def example_with_entity():
    """Example showing how to use the service with camera entity."""

    service_data = {
        "entity_id": "camera.front_door",
        "camera": "front_door_camera"
    }

    print("Example 3 - Using camera entity:")
    print(f"Service call: face_recognition.recognize_face")
    print(f"Service data: {json.dumps(service_data, indent=2)}")
    print()

# Example 4: Using the service in a Home Assistant automation
def example_automation_yaml():
    """Example YAML for a Home Assistant automation."""

    automation_yaml = """
# Example automation that triggers on motion detection
# and uses the face recognition service
automation:
  - alias: "Recognize face on motion"
    trigger:
      platform: state
      entity_id: binary_sensor.front_door_motion
      to: "on"
    action:
      - service: face_recognition.recognize_face
        data:
          entity_id: camera.front_door
          camera: "front_door_camera"
    # The service returns data that can be used in conditions
    # or to trigger other actions
"""

    print("Example 4 - Home Assistant Automation YAML:")
    print(automation_yaml)

# Example 5: Using service response in automation
def example_with_response():
    """Example showing how to use the service response."""

    # The service returns a dictionary with recognition results
    # Example response structure:
    response_example = {
        "success": True,
        "person_id": "person_123",
        "display_name": "John Doe",
        "confidence": 0.85,
        "needs_review": False,
        "face_count": 1,
        "processing_time_ms": 150,
        "raw_response": {
            "person_id": "person_123",
            "display_name": "John Doe",
            "confidence": 0.85,
            "needs_review": False,
            "face_count": 1,
            "processing_time_ms": 150,
            "status": "processed"
        }
    }

    automation_with_response = """
# Automation that uses the service response
automation:
  - alias: "Handle recognized person"
    trigger:
      platform: event
      event_type: face_recognition_detected
    action:
      # The event data contains the recognition results
      - choose:
          - conditions:
              - "{{ trigger.event.data.person_id == 'person_123' }}"
            sequence:
              - service: notify.mobile_app
                data:
                  message: "John Doe is at the front door"
          - conditions:
              - "{{ trigger.event.data.person_id == 'unknown' }}"
            sequence:
              - service: notify.mobile_app
                data:
                  message: "Unknown person detected at front door"
                  data:
                    image: "{{ trigger.event.data.image_url }}"
    """

    print("Example 5 - Using service response in automation:")
    print("Service returns:", json.dumps(response_example, indent=2))
    print("\nAutomation example using response:")
    print(automation_with_response)

def main():
    print("=" * 60)
    print("FACE RECOGNITION SERVICE USAGE EXAMPLES")
    print("=" * 60)
    print()

    example_with_base64()
    example_with_url()
    example_with_entity()
    example_automation_yaml()
    example_with_response()

    print("=" * 60)
    print("HOW TO TEST THE SERVICE:")
    print("=" * 60)
    print("1. Install the updated integration and add-on")
    print("2. Go to Home Assistant Developer Tools > Services")
    print("3. Select service: face_recognition.recognize_face")
    print("4. Enter service data (use examples above)")
    print("5. Click 'CALL SERVICE'")
    print("6. Check logs for results")
    print()
    print("Expected flow:")
    print("1. Service sends image to add-on")
    print("2. Add-on logs: 'Recognition request received'")
    print("3. Add-on returns simulated response")
    print("4. Service returns results to automation")
    print("=" * 60)

if __name__ == "__main__":
    main()