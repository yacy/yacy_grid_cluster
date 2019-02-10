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
