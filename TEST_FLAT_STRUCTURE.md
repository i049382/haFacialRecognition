# Test: Try Flat Structure Instead of Nested

## Current Structure (Not Working)
```
face_recognition/
└── face_recognition/
    └── config.yaml
```

## Test Structure (Try This)
```
face_recognition/
└── config.yaml  ← Directly here
```

Some HA versions expect config.yaml directly under the add-on directory, not nested twice.

## Quick Test

Let's copy config.yaml to the parent directory to test:

1. Copy `face_recognition/face_recognition/config.yaml` 
2. To: `face_recognition/config.yaml`
3. Commit and push
4. Remove/re-add repository in HA
5. See if add-on appears

If this works, we know the nested structure is the issue!

