This applies if you want to install elasticsearch with "apt-get install elasticsearch":

Set the following attributes in the configuration file /etc/elasticsearch/elasticsearch.yml
cluster.name: yacygrid
node.name: node04 (00/01/02/03/04)
node.master: false (for 01/02/03/04, for 00 set this to true)
node.data: true (for 01/02/03/04, for 00 set this to false)
index.number_of_shards: 16
index.number_of_replicas: 1

Memory settings in /etc/init.d/elasticsearch
set the value
ES_HEAP_SIZE=256m
on node00 and
ES_HEAP_SIZE=512m
on node01-node04


The following applies if you wan tot install elasticsearch with the elk tarball:

- consider that you extracted the tarball to /home/pi/elasticsearch
- edit the file /home/pi/elasticsearch/config/elasticsearch.yml and set
 xpack.ml.enabled: false
 cluster.name: yacygrid
 node.name: node04 (00/01/02/03/04)
 node.master: false (for 01/02/03/04, for 00 set this to true)
 node.data: true (for 01/02/03/04, for 00 set this to false)
 index.number_of_shards: 16
 index.number_of_replicas: 1
- edit the file /home/pi/elasticsearch/config/jvm.options and set
 -Xms256m
 -Xmx256m
- copy the file elasticsearch.service to /lib/systemd/system/
 sudo cp ~/git/yacy_grid_cluster/doc/elasticsearch.service /lib/systemd/system/
- run
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service

- finally configure the cluster with
 curl -XPUT 'http://localhost:9200/_all/_settings?preserve_existing=true' -d '{
  "index.number_of_replicas" : "1",
  "index.number_of_shards" : "16"
 }'


We want an elasticsearch cluster on node01-node04. The steps to run elasticsearch is:

- clone the yacy_grid_mcp into the git path
-- mkdir git (or cd git)
-- git clone https://github.com/yacy/yacy_grid_mcp.git

- run git/yacy_grid_mcp/bin/start_elasticsearch.py, this will install elasticsearch on yacy_grid_mcp/data/apps/elasticsearch but it will fail to start because it needs special settings

- edit the file yacy_grid_mcp/data/apps/elasticsearch/config/jvm.options and set
-- -Xms512m and
-- -Xmx512m
instead of -Xms2g and -Xmx2g

- edit the file yacy_grid_mcp/data/apps/elasticsearch/config/elasticsearch.yml and set:
-- cluster.name: yacy-grid
-- node.name: es-node01 (according to your node number)
-- network.bind_host: 0.0.0.0
-- network.host: 0.0.0.0
-- discovery.zen.ping.unicast.hosts: ["node01.local", "node02.local", "node03.local", "node04.local"]
-- bootstrap.system_call_filter: false

- edit the file /etc/sysctl.conf and set
-- vm.max_map_count=262144
-- fs.file-max=65536

- edit the file /etc/security/limits.conf and set
-- * soft nofile 65536
-- * hard nofile 65536

- finally, create a systems service which starts elasticsearch automatically
-- copy the file elasticsearch.service into /lib/systemd/system/elasticsearch.service
-- run sudo systemctl daemon-reload
-- run sudo systemctl enable elasticsearch.service

- finally do a restart
