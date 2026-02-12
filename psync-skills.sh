c#!/usr/bin/env bash

# sync-project-skills.sh - Sync skill directories from this repo to <cwd>/.claude/skills/
# Ownership is inherited from the directory the script is called from.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CALL_DIR="$(pwd)"
TARGET_DIR="$CALL_DIR/.claude/skills"

# Get owner:group from the calling directory
OWNER_GROUP="$(stat -c '%u:%g' "$CALL_DIR")"

echo "Syncing skills from: $SCRIPT_DIR"
echo "Target: $TARGET_DIR"
echo "Ownership: $OWNER_GROUP (inherited from $CALL_DIR)"

# Git pull if inside a repo
if git -C "$SCRIPT_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Pulling latest changes..."
    git -C "$SCRIPT_DIR" pull
fi

# Create target if needed
mkdir -p "$TARGET_DIR"

# Iterate over directories in the script's location, skipping hidden ones
for dir in "$SCRIPT_DIR"/*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"

    # Skip hidden directories (shouldn't match with */, but guard anyway)
    [[ "$name" == .* ]] && continue

    echo "Syncing: $name"
    rm -rf "${TARGET_DIR:?}/$name"
    cp -r "$dir" "$TARGET_DIR/$name"
    chown -R "$OWNER_GROUP" "$TARGET_DIR/$name"
done

echo "Done. Synced skills to $TARGET_DIR"
