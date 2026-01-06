# Test Chunk 0 Installation ✅

## Installation Complete!

The add-on has been installed successfully. Now let's test it.

## Step-by-Step Testing

### Step 1: Configure the Add-on

1. **Click:** **Configuration** tab
2. **Set these values:**
   ```yaml
   confidence_threshold: 0.80
   review_threshold: 0.65
   camera_paths: []
   enable_daily_poll: false
   daily_poll_time: "02:00"
   drive_folder_id: ""
   api_port: 8080
   api_token: "test_token_123"
   ```
3. **Important:** Make sure `review_threshold` (0.65) is **less than** `confidence_threshold` (0.80)
4. **Click:** **Save**

### Step 2: Start the Add-on

1. **Click:** **Start** button (top right)
2. **Wait:** A few seconds for add-on to start
3. **Status** should change to: **"Running"** (green)

### Step 3: Verify Logs

1. **Click:** **Logs** tab
2. **You should see:**
   ```
   Starting Face Recognition Add-on
   Configuration loaded successfully
   Add-on ready (Chunk 0 - Configuration only)
   Waiting for future functionality... (Chunk 2+)
   ```

### Step 4: Test Configuration Validation

**Test 1: Invalid Thresholds**
1. **Configuration** tab
2. **Set:** `review_threshold: 0.90` (greater than confidence_threshold)
3. **Click:** **Save**
4. **Try to start** add-on
5. **Expected:** Add-on fails to start with validation error
6. **Fix:** Set `review_threshold: 0.65` again

**Test 2: Invalid Time Format**
1. **Configuration** tab
2. **Set:** `daily_poll_time: "25:00"` (invalid hour)
3. **Click:** **Save**
4. **Try to start** add-on
5. **Expected:** Add-on fails to start with validation error
6. **Fix:** Set `daily_poll_time: "02:00"` again

**Test 3: Valid Configuration**
1. **Set valid values** (as in Step 1)
2. **Save** and **Start**
3. **Expected:** Add-on starts successfully ✅

## Success Criteria

✅ **Add-on installs** without errors  
✅ **Add-on starts** successfully  
✅ **Configuration loads** from HA UI  
✅ **Logs show** "Configuration loaded successfully"  
✅ **Validation works** (rejects invalid values)  
✅ **Add-on stays running** (doesn't crash)

## What to Expect

**Current Functionality (Chunk 0):**
- ✅ Configuration loading
- ✅ Configuration validation
- ✅ Secret handling (non-fatal if missing)
- ✅ Add-on stays running
- ⚠️ **No functionality yet** (waiting for Chunk 2)

**This is Expected!**
- Chunk 0 only handles configuration
- Chunk 2 will add HTTP API
- Chunk 3+ will add face recognition

## Troubleshooting

### Add-on Won't Start

**Check logs for errors:**
- Configuration validation errors
- Missing file errors
- Permission errors

**Common issues:**
- Invalid threshold values (review >= confidence)
- Invalid time format
- Missing required fields

### Logs Show Errors

**If you see errors:**
1. Check the error message
2. Fix configuration values
3. Save and restart

### Add-on Crashes

**If add-on stops:**
1. Check logs for crash reason
2. Verify configuration is valid
3. Try restarting

---

## Next Steps After Testing

Once Chunk 0 is verified working:

1. ✅ **Document** any issues found
2. ✅ **Verify** all success criteria met
3. 🚀 **Proceed** to Chunk 2: IPC & Event Plumbing

---

**Ready to test!** Start the add-on and check the logs. Let me know what you see!

