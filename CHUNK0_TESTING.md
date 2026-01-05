# Chunk 0 Testing Guide

## Success Criteria

1. ✅ Add-on loads configuration successfully
2. ✅ Missing secrets fail gracefully (non-fatal warning)
3. ✅ Configuration validation works correctly

## Manual Testing Steps

### 1. Test Configuration Loading

Create a test `options.json` file:

```json
{
  "confidence_threshold": 0.80,
  "review_threshold": 0.65,
  "camera_paths": ["/data/cameras/cam1"],
  "enable_daily_poll": true,
  "daily_poll_time": "03:00",
  "drive_folder_id": "test_folder_123",
  "api_port": 8080,
  "api_token": "test_token_123"
}
```

Run the test script:
```bash
cd addon
python3 test_config.py
```

Expected: All tests pass ✅

### 2. Test Missing Configuration

Remove or rename the config file and run the add-on:
```bash
python3 -m face_recognition_addon
```

Expected: Graceful error message about missing config ✅

### 3. Test Invalid Thresholds

Create an invalid config with `review_threshold >= confidence_threshold`:
```json
{
  "confidence_threshold": 0.60,
  "review_threshold": 0.75,
  "camera_paths": [],
  "api_port": 8080
}
```

Expected: Validation error raised ✅

### 4. Test Missing Secrets

Run with no `secrets.yaml` file (or missing secret):
- Add-on should start successfully
- Warning logged about missing Drive credentials
- Non-fatal (Drive features disabled until configured)

Expected: Graceful warning, add-on continues ✅

## Integration Testing (Future)

Once add-on is installed in HA:
1. Install add-on → should start without errors
2. Check logs → configuration loaded message
3. Missing secrets → warning logged, add-on continues
4. Invalid config → add-on fails to start with clear error

## Notes

- Configuration is loaded from `/data/options.json` (created by HA from `config.yaml` schema)
- Secrets are loaded from `/config/secrets.yaml` (HA secrets file)
- Missing secrets are non-fatal - Drive features will be disabled
- Invalid configuration values cause startup failure with clear error messages

