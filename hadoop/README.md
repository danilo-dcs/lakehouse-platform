# Hadoop Docker Cluster

## Set Up

To set up the hadoop cluster, modify the [hadoop.conf](./hadoop.conf) file and the [docker-compose.yaml](../docker-compose.yaml) file according to the specifications listed below, or according to your own specifications.

### WebHDFS API

Make sure to set the property `dfs.webhdfs.enabled` with _true_ to enable the WebHDFS Rest API.

### Hostnames

1. Before launching the cluster, double check the property values in the `hadoop.conf` file.

2. Make sure to check if all the hadoop services have assigned hostnames in the docker-compose file.

3. Make sure to allow include the `dfs.datanode.use.datanode.hostname` property for the CORE CONF and HDFS CONF, setting its value to _true_, to allow communication within the hadoop cluster using the hostnames instead of the ip addresses.

4. Map docker datanode hostname as docker host ip address by add an entry in file of etc/hosts, on the container host machine.

```
127.0.0.1	localhost namenode datanode1 datanode2 datanode3 ...
::1             localhost namenode datanode1 datanode2 datanode3 ...
```

If the datanodes are located on external hosts (not localhost), add the external hosts ips for each datanode.

```
<host_1> datanode1
<host_2> datanode2
<host_3> datanode3
<host_4> datanode4
```

Command to modify the hosts files:

```
echo "127.0.0.1 datanode1" | sudo tee -a /etc/hosts
echo "127.0.0.1 datanode2" | sudo tee -a /etc/hosts
# echo "namenode_ip datanode_n" | sudo tee -a /etc/hosts
```

\*OBS: this step has do be done only for the API host

### Users

To disable permissions and make the cluster accessible (but less secure), set the `dfs.permissions` property to _false_
