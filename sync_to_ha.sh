#!/bin/bash
# Sync integration files to Home Assistant

SOURCE_DIR="integration"
TARGET_DIR="ha_config/custom_components/face_recognition"

echo "=== Syncing Face Recognition Integration ==="
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Target directory not found: $TARGET_DIR"
    echo "   Make sure ha_config symbolic link is working"
    exit 1
fi

# List files to sync
echo "Files to sync:"
ls -la "$SOURCE_DIR/"*.py "$SOURCE_DIR/"*.yaml "$SOURCE_DIR/"*.json 2>/dev/null

echo ""
echo "Copying files..."

# Copy Python files
for file in "$SOURCE_DIR/"*.py; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$TARGET_DIR/$filename"
        echo "✅ $filename"
    fi
done

# Copy YAML files
for file in "$SOURCE_DIR/"*.yaml; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$TARGET_DIR/$filename"
        echo "✅ $filename"
    fi
done

# Copy JSON files
for file in "$SOURCE_DIR/"*.json; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$TARGET_DIR/$filename"
        echo "✅ $filename"
    fi
done

echo ""
echo "=== Sync Complete ==="
echo ""
echo "Next steps:"
echo "1. Restart Home Assistant"
echo "2. Test the integration"
echo ""
echo "To restart HA:"
echo "  - Go to Settings → System → RESTART"
echo "  - Or use: ha core restart (if SSH available)"