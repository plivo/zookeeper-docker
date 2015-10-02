#!/usr/bin/env python

import os
import sys

zk_data_dir = '/var/lib/zookeeper'
zk_config_file = '/opt/zookeeper/conf/zoo.cfg'
zk_log_config_file = '/opt/zookeeper/conf/log4j.properties'

# From the environment, find details about the cluster.
num_servers = int(os.environ.get('ZK_CLUSTER_SIZE', 1))
myid = int(os.environ.get('ZK_SERVER_ID', 1))
servers = {}
for sid in range(1, num_servers + 1):
    servers[sid] = {
        'host': os.environ.get('ZK_SERVER_{}_HOST'.format(sid), '127.0.0.1'),
    }

print("DEBUG: Server List: {}".format(servers))

# build zookeeper node configuration
conf = {
    'tickTime': 2000,
    'initLimit': 10,
    'syncLimit': 5,
    'dataDir': zk_data_dir,
    'clientPort': 2181,
#    'quorumListenOnAllIPs': True,
    'autopurge.snapRetainCount':
        int(os.environ.get('ZK_MAX_SNAPSHOT_RETAIN_COUNT', 10)),
    'autopurge.purgeInterval':
        int(os.environ.get('ZK_PURGE_INTERVAL', 24)),
}

for node_id, props in servers.items():
    k = 'server.{}'.format(node_id)
    if node_id == myid:
        conf[k] = "0.0.0.0:2888:3888".format(**props)
    else:
        conf[k] = "{host}:2888:3888".format(**props)

print("DEBUG: Conf object: {}".format(conf))

# Write out the zookeeper configuration file.
with open(zk_config_file, 'w+') as f:
    for k, v in conf.items():
        f.write("{}={}\n".format(k, v))

LOG_PATTERN = (
    "%d{yyyy'-'MM'-'dd'T'HH:mm:ss.SSSXXX} %-5p [%-35.35t] [%-36.36c]: %m%n")

# Setup the logging configuration.
with open(zk_log_config_file, 'w+') as f:
    f.write("""# Log4j configuration, logs to rotating file
log4j.rootLogger=INFO,R
log4j.appender.R=org.apache.log4j.RollingFileAppender
log4j.appender.R.File=/var/log/zookeeper/zookeeper.log
log4j.appender.R.MaxFileSize=100MB
log4j.appender.R.MaxBackupIndex=10
log4j.appender.R.layout=org.apache.log4j.PatternLayout
log4j.appender.R.layout.ConversionPattern={}
""".format(LOG_PATTERN))

# Write out the 'myid' file in the data directory if in cluster mode.
if num_servers > 1:
    if not os.path.exists(zk_data_dir):
        os.makedirs(zk_data_dir, mode=0750)
    with open(os.path.join(zk_data_dir, 'myid'), 'w+') as f:
        f.write('{}\n'.format(myid))
    sys.stderr.write(
        'Starting node id#{} of a {}-node ZooKeeper cluster...\n'
        .format(myid, num_servers))
else:
    sys.stderr.write('Starting as a single-node ZooKeeper cluster...\n')

# Start ZooKeeper
os.execl('/opt/zookeeper/bin/zkServer.sh', 'zookeeper', 'start-foreground')
