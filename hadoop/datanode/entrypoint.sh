#!/bin/bash

# Ensure HDFS directories have correct permissions
echo "Setting up HDFS directories..."
hdfs dfs -mkdir -p /tmp/hadoop-hdfs/datanode
hdfs dfs -chown hadoop-api:hadoop /tmp/hadoop-hdfs/datanode

if [ -n "$DFS_DATANODE_HTTP_ADDRESS" ]; then
    sed -i "s/^dfs.datanode.http.address=.*/dfs.datanode.http.address=${DFS_DATANODE_HTTP_ADDRESS}/" "/etc/hadoop/hdfs-site.xml"
fi

# Start HDFS
echo "Starting HDFS Datanode..."
start-dfs.sh

# Execute the main command (runs 'hdfs datanode' in this case)
exec "$@"