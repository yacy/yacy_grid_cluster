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
