# Investigate Why Nest Doesn't Deliver Thumbnails Automatically

## What We're Checking

I've added diagnostic code to investigate:

### 1. **What Files Nest Stores**
- Logs all file types in Nest media directory
- Checks if Nest stores separate thumbnail files (.jpg, .jpeg, .png)
- Shows sample filenames

### 2. **Event Processing Timing**
- Measures delay between event timestamp and when we process it
- Measures API fetch duration
- Helps identify if delays cause expiration

### 3. **Thumbnail File Detection**
- Checks for thumbnail files matching event timestamp
- Uses thumbnail files if found (faster than extracting from video)

## Expected Findings

### Scenario 1: Nest Only Stores MP4s
```
File types found: {'.mp4': 10}
No separate thumbnail files found - Nest only stores MP4 videos
```
**Conclusion**: Nest doesn't store thumbnails, only videos. We must extract frames.

### Scenario 2: Nest Stores Thumbnails
```
File types found: {'.mp4': 10, '.jpg': 10}
Found matching thumbnail: 1767801496-camera_person.jpg
```
**Conclusion**: Nest stores thumbnails! We can use them directly.

### Scenario 3: Processing Delay Causes Expiration
```
Event processing delay: 15.23 seconds
API fetch took 0.45 seconds
```
**Conclusion**: Delay causes expiration. Need to process faster.

## Next Steps

1. **Deploy the updated code**
2. **Trigger a Nest event**
3. **Check logs for:**
   - File types found
   - Processing delay
   - Whether thumbnails exist

## Possible Solutions

### If Nest Only Stores MP4s:
- ✅ Current approach (extract frames) is correct
- Could cache extracted thumbnails for reuse
- Could generate thumbnails immediately on event

### If Nest Stores Thumbnails:
- Use thumbnail files directly (faster!)
- Match by timestamp
- Fallback to video extraction if not found

### If Processing Delay is High:
- Optimize event processing
- Fetch thumbnail immediately (before other processing)
- Consider async processing

## What to Look For in Logs

After deploying, check for:
```
Nest media directory contents: X files
File types found: {...}
Event processing delay: X.XX seconds
API fetch took X.XX seconds
```

This will tell us:
- What Nest actually stores
- How quickly we process events
- Why thumbnails expire

