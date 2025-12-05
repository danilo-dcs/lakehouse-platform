#!/bin/bash

# Start the default Couchbase entrypoint script (included in the image)
# It will start couchbase-server properly
/entrypoint.sh couchbase-server &

# Wait for Couchbase to become available
echo "Waiting for Couchbase Server to become available..."
until curl -s -u admin:admin1234 http://localhost:8091/pools > /dev/null; do
  sleep 5
done

echo "Couchbase is ready. Running initialization script..."
chmod +x /scripts/initialize_couchbase.sh
/scripts/initialize_couchbase.sh

# Keep container running
wait
