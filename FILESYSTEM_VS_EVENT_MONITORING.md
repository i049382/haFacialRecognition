# Filesystem Monitoring vs Nest Event Monitoring

## Current Approach: Nest Event Monitoring

### What We Get from Nest Events:
- ✅ **Event type**: `camera_person` vs `camera_motion` (we filter to only process person events)
- ✅ **Rich metadata**: `device_id`, `nest_event_id`, `timestamp`, `zones`
- ✅ **Structured data**: Easy to parse and process
- ✅ **Event filtering**: Only process relevant events (person detection)
- ✅ **Real-time**: Immediate notification when event occurs

### Current Flow:
```
Nest Event → Filter by type → Extract metadata → Find video by timestamp → Extract frame → Process
```

## Alternative: Filesystem Monitoring

### What We'd Get:
- ✅ **Direct file access**: See files as they're created
- ✅ **No API dependency**: Works even if events fail
- ✅ **Catches everything**: Won't miss events

### What We'd Lose:
- ❌ **Event type**: Can't distinguish `camera_person` from `camera_motion` (both create MP4s)
- ❌ **Metadata**: No `nest_event_id`, `zones`, etc.
- ❌ **Filtering**: Would process ALL videos (motion + person)
- ❌ **Duplicate tracking**: Need to track processed files
- ❌ **Inference needed**: Must infer event type from filename pattern

### Filesystem Flow:
```
New MP4 file → Parse filename → Infer event type → Extract frame → Process
```

## Recommendation: Hybrid Approach

**Best of both worlds:**

### Primary: Keep Nest Events
- Use events for metadata and filtering
- Only process `camera_person` events
- Get structured data

### Backup: Add Filesystem Monitoring
- Monitor folder for new files
- Process if event was missed
- Use as safety net

## Implementation Options

### Option 1: Keep Current (Events Only) ✅ Recommended
- **Pros**: Simple, efficient, filters correctly
- **Cons**: Might miss events if Nest integration fails
- **Best for**: Most use cases

### Option 2: Filesystem Only
- **Pros**: More reliable, catches everything
- **Cons**: Processes motion events too, loses metadata, more complex
- **Best for**: If Nest events are unreliable

### Option 3: Hybrid (Events + Filesystem Backup) ⭐ Best
- **Pros**: Best of both worlds, redundant, catches missed events
- **Cons**: More complex, need duplicate detection
- **Best for**: Production systems needing reliability

## My Recommendation

**Keep Nest events as primary** because:
1. We need event type filtering (only process person events)
2. Rich metadata is valuable
3. Events are working reliably
4. Simpler code path

**Add filesystem monitoring as optional backup** if:
- Events are unreliable
- You want to catch missed events
- You need 100% coverage

## Code Changes Needed for Filesystem Monitoring

Would need:
- `watchdog` library (already in requirements per PRD)
- File watcher on `/config/nest/event_media/<device_id>/`
- Duplicate detection (track processed files)
- Event type inference from filename

Would you like me to implement filesystem monitoring as a backup, or keep the current event-based approach?

