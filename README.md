[![Docker Repository on Quay.io](https://quay.io/repository/donatello/zookeeper/status "Docker Repository on Quay.io")](https://quay.io/repository/donatello/zookeeper)

# Zookeeper in a Docker container #

In this setup, the port configuration is:

* 2181 for client communication
* 2888 for peer servers
* 3888 for elections

They are currently not modifiable.

## Environment Variables ##

The following variables control the configuration for the zookeeper
process in the container. If **ZK\_CLUSTER\_SIZE** is not specified, a
single node cluster is assumed.

* **ZK\_CLUSTER\_SIZE** - Number of instances in this Zookeeper
  ensemble
* **ZK\_SERVER\_ID** - Server ID of the node, must be between 1 and
  ZK\_CLUSTER\_SIZE
* **ZK\_MAX\_SNAPSHOT\_RETAIN\_COUNT** - Number of snapshots to retain
  (default 10)
* **ZK\_PURGE\_INTERVAL** - Snapshot purging interval in hours
  (default 24)
* **ZK\_SERVER\_i\_HOST** - Hostname or IP of the server with ID "i"
  (replace the "i" with the ID of the corresponding server)

For example, the following configuration sets up a 3 node cluster:

    ZK_CLUSTER_SIZE=3
    ZK_SERVER_ID=1
    ZK_SERVER_1_HOST=10.0.0.1
    ZK_SERVER_2_HOST=10.0.0.2
    ZK_SERVER_3_HOST=10.0.0.3

The above is the configuration for the container on `10.0.0.1`. On
`10.0.0.2` and `10.0.0.3`, the `ZK_SERVER_ID` is 2 and 3
respectively. Other variables remain the same.

## Volumes ##

The following volumes may be mounted on the host if desired (with no
existing data on first startup):

* `/var/lib/zookeeper` - Zookeeper data directory
* `/var/log/zookeeper` - Zookeeper logs
