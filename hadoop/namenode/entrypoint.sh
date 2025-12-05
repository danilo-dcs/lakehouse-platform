#!/bin/bash

# Format the Namenode if it's not already formatted
if [ ! -d /tmp/hadoop-root/dfs/name/current ]; then
  echo "Formatting Namenode..."
  hdfs namenode -format
fi

# Ensure HDFS directories have correct permissions
echo "Setting up HDFS directories..."
hdfs dfs -mkdir -p /tmp/hadoop-root/dfs/name
hdfs dfs -chown hadoop-api:hadoop /tmp/hadoop-root/dfs/name

# Start HDFS services
echo "Starting HDFS..."
start-dfs.sh

# Execute the main command (runs 'hdfs namenode' in this case)
exec "$@"
