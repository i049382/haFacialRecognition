# Chunk 0 Testing Guide

## Overview

This guide provides comprehensive testing instructions for **Chunk 0: Configuration & Credentials**.

## Prerequisites

- Python 3.7+ installed
- Required packages: `pyyaml` (install with `pip install pyyaml`)

## Running Tests

### Option 1: Automated Test Suite (Recommended)

Run the comprehensive test suite:

```bash
cd addon
python test_chunk0.py
```

This will run all 7 test suites covering:
1. ✅ Valid configuration loading
2. ✅ Missing configuration file handling
3. ✅ Threshold validation
4. ✅ Time format validation
5. ✅ Missing secrets (non-fatal)
6. ✅ Secrets loading
7. ✅ Default values

**Expected Result:** All tests pass ✅

### Option 2: Individual Unit Tests

Run the simpler unit test script:

```bash
cd addon
python test_config.py
```

## Test Coverage

### Test 1: Valid Configuration Loading
- ✅ Loads all configuration fields correctly
- ✅ Validates threshold values
- ✅ Handles camera paths array
- ✅ Processes boolean flags
- ✅ Validates time format

### Test 2: Missing Configuration File
- ✅ Raises `FileNotFoundError` with helpful message
- ✅ Does not crash silently

### Test 3: Threshold Validation
- ✅ Rejects `review_threshold >= confidence_threshold`
- ✅ Rejects thresholds outside 0.0-1.0 range
- ✅ Provides clear error messages

### Test 4: Time Format Validation
- ✅ Rejects invalid hours (>= 24)
- ✅ Rejects invalid minutes (>= 60)
- ✅ Rejects malformed strings
- ✅ Accepts valid HH:MM format

### Test 5: Missing Secrets (Non-Fatal)
- ✅ Loads configuration successfully without secrets
- ✅ Logs warning about missing secrets
- ✅ Sets `drive_credentials` to `None`
- ✅ Does not prevent add-on startup

### Test 6: Secrets Loading
- ✅ Loads secrets from `secrets.yaml`
- ✅ Correctly extracts secret value
- ✅ Handles YAML format correctly

### Test 7: Default Values
- ✅ Uses defaults when options missing
- ✅ Defaults: `camera_paths=[]`, `enable_daily_poll=False`, `daily_poll_time="02:00"`

## Manual Testing (Home Assistant Environment)

If you have Home Assistant running, you can test the add-on integration:

### 1. Install Add-on
1. Copy `addon/` directory to your HA `addons/` folder
2. Restart Home Assistant
3. Go to **Settings → Add-ons → Face Recognition**
4. Click **Install**

### 2. Test Configuration Loading
1. Configure add-on with valid settings
2. Click **Start**
3. Check logs: Should see "Configuration loaded successfully"

### 3. Test Missing Secrets
1. Start add-on without `face_recognition_drive_credentials` in `secrets.yaml`
2. Check logs: Should see warning but add-on starts
3. Verify: `drive_credentials` is `None` in logs

### 4. Test Invalid Configuration
1. Set `review_threshold` >= `confidence_threshold`
2. Click **Start**
3. Check logs: Should see validation error, add-on fails to start

## Success Criteria

Chunk 0 is considered complete when:

- ✅ All automated tests pass
- ✅ Configuration loads correctly from `options.json`
- ✅ Secrets load correctly from `secrets.yaml`
- ✅ Missing secrets are handled gracefully (non-fatal)
- ✅ Invalid configurations are rejected with clear errors
- ✅ Default values work correctly
- ✅ Error messages are helpful and actionable

## Troubleshooting

### Test Failures

If tests fail:

1. **Check Python version**: Requires Python 3.7+
   ```bash
   python --version
   ```

2. **Check dependencies**: Install required packages
   ```bash
   pip install pyyaml
   ```

3. **Check imports**: Ensure you're running from `addon/` directory
   ```bash
   cd addon
   python test_chunk0.py
   ```

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'face_recognition_addon'`
- **Solution:** Run tests from `addon/` directory

**Issue:** `FileNotFoundError` when loading config
- **Solution:** Tests create temporary files automatically. If this fails, check file permissions.

**Issue:** Secrets not loading
- **Solution:** Ensure `secrets.yaml` exists and has correct format. Test uses temporary file.

## Next Steps

Once all tests pass:

1. ✅ Review test output for any warnings
2. ✅ Document any edge cases discovered
3. ✅ Proceed to **Chunk 2: IPC & Event Plumbing**

---

**Note:** Chunk 1 (Repository & Skeleton Setup) was completed as part of Chunk 0, so we proceed directly to Chunk 2.

