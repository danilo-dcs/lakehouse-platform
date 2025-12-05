# Couchbase structure

- lakehouse # bucket level
  - catalogs # scope level
    - collections # collection level
    - files
  - credentials
    - cloud
  - users
    - info
    - visa
    - access_request

## Comments

When creating couchbase nodes in AWS or any other cloud provider, we must specify the private IP address to appennd new nodes to the master node.
