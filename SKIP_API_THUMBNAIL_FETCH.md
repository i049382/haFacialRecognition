# Skip API Thumbnail Fetch - Use Filesystem Only

## Change Summary

**Removed:** API thumbnail fetch attempt (expires too quickly)
**Kept:** Direct filesystem extraction from MP4 videos (reliable)

## Why This Change?

1. **Nest thumbnails expire quickly** (seconds to minutes)
2. **API fetch wastes time/resources** trying to fetch expired URLs
3. **Filesystem extraction works reliably** - videos persist on disk
4. **Simpler code** - one path instead of two

## What Changed

### Before:
```
Event → Try API thumbnail fetch → 404 (expired) → Fallback to filesystem → Extract frame
```

### After:
```
Event → Extract frame from filesystem video → Done
```

## Benefits

- ✅ **Faster**: No wasted time on expired API calls
- ✅ **More reliable**: Videos always available on filesystem
- ✅ **Simpler**: One code path instead of two
- ✅ **Less resource usage**: No unnecessary HTTP requests

## Code Changes

1. Removed API fetch attempt from `_handle_nest_event()`
2. Removed diagnostic code (file type checking, timing)
3. Go straight to `_fetch_nest_image_from_filesystem_by_timestamp()`
4. Kept `_fetch_nest_image_from_api()` method (in case needed later, but not called)

## Next Steps

1. Deploy updated code
2. Test Nest event processing
3. Verify frame extraction works correctly
4. Check logs - should see "Extracting frame from Nest video filesystem"

