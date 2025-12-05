#!/bin/bash

# Ensure YARN directories have correct permissions
echo "Setting up YARN directories..."
yarn dfs -mkdir -p /tmp/yarn
yarn dfs -chown hadoop-api:hadoop /tmp/yarn

# Start YARN services
echo "Starting YARN NodeManager..."
start-yarn.sh

# Execute the main command (runs 'yarn nodemanager' in this case)
exec "$@"
