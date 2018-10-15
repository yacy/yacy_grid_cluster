## Node System Configuration
We want a basic system configuration for the grid node elements. What we want:
* applying SD card overclocking  
To do this, just add the line `dtoverlay=sdhost,overclock_50=100` to `/boot/config.txt`
* start up an ssh daemon  
you must add an empty file in `boot/ssh`
* changing the node host name  
to do that, edit the file `/etc/hostname`



