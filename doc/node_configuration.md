## Node System Configuration
We want a basic system configuration for the grid node elements. What we want:
* applying SD card overclocking  
To do this, just add the line `dtoverlay=sdhost,overclock_50=100` to `/boot/config.txt`
* start up an ssh daemon  
you must add an empty file in `boot/ssh`

Both can be done with commands (like):
```
touch /Volumes/boot/ssh
echo "dtoverlay=sdhost,overclock_50=100" | cat >> /Volumes/boot/config.txt
```
..if the sd card is mounted on /Volumes/boot

* changing the node host name  
to do that, boot up the image with a Raspberry Pi and then edit the file `/etc/hostname`

For our cluster we want different host names for each node. We define that every node shall be named with names like
`node00`, `node01`, `node02`, `node03`, .. `node15` for a 16-node cluster.

Our cluster shall have a management node, one which has the purpose to do a steering of the other nodes.
That node shall be the node `node00`.



