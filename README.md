# YaCy Grid Raspberry Pi Cluster
Management tools for a Raspberry Pi Demonstration Cluster of the YaCy Grid.

For details of the YaCy Grid ecosystem, star reading at the YaCy Grid MCP component: https://github.com/yacy/yacy_grid_mcp

To use these script, we encourage the following procedure:

- download Raspberry Pi OS (32-bit) Lite (formerly called "raspbian") from https://www.raspberrypi.org/downloads/raspbian/
- put the image on a SD card (i.e. using https://www.balena.io/etcher/ )
- mount the SD card and put an empty file "ssh" on the boot partition, like (in Mac OS) "touch /Volumes/boot/ssh"
- startup a Raspberry Pi with the image and log in with ssh pi@raspberrypi.local - use the password "raspberry"
- sudo apt-get update && sudo apt-get -y upgrade
- sudo apt-get install -y git
- mkdir git
- cd git
- git clone https://github.com/yacy/yacy_grid_cluster.git
- cd yacy_grid_cluster

Now you have access to the scripts within this repository. 
