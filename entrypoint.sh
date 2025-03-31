#!/bin/bash
set -e  # Stop script if any command fails

# Generate buildspec.yml
echo "Generating buildspec.yml..."
python3 generate_buildspec.py "$@"

# Check if buildspec.yml was created
if [ ! -f "buildspec.yml" ]; then
    echo "❌ Error: buildspec.yml not found!"
    exit 1
fi

# Debugging: Print contents of buildspec.yml
echo "✅ buildspec.yml contents:"
cat buildspec.yml

# Start AWS CodeBuild
echo "🚀 Starting AWS CodeBuild..."
