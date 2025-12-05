#!/bin/bash

# Ensure YARN directories have correct permissions
echo "Setting up YARN directories..."
yarn dfs -mkdir -p /tmp/yarn
yarn dfs -chown hadoop-api:hadoop /tmp/yarn

# Start YARN ResourceManager
echo "Starting YARN ResourceManager..."
start-yarn.sh

# Execute the main command (runs 'yarn resourcemanager' in this case)
exec "$@"
