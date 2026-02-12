#!/usr/bin/env bash

# sync-skills.sh - Sync skill directories from this repo to ~/.claude/skills/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.claude/skills"
OWNER_GROUP="$(stat -c '%u:%g' "$HOME")"

echo "Syncing skills from: $SCRIPT_DIR"
echo "Target: $TARGET_DIR"
echo "Ownership: $OWNER_GROUP (inherited from $HOME)"

# Git pull if inside a repo
if git -C "$SCRIPT_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Pulling latest changes..."
    git -C "$SCRIPT_DIR" pull
fi

# If the script already lives in the target, just pull and exit
if [[ "$SCRIPT_DIR" == "$TARGET_DIR" ]]; then
    echo "Script is running from $TARGET_DIR — pull complete, nothing to sync."
    exit 0
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
