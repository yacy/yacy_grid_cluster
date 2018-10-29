# Node Configuration

## Node Image Preparation
We want a basic system configuration for the grid node elements. What we want:
* start up an ssh daemon  
you must add an empty file in `boot/ssh`
* applying SD card overclocking  
To do this, just add the line `dtoverlay=sdhost,overclock_50=100` to `/boot/config.txt`
* reduce the GPU memory because we don't need this for headless operation.
To do this, we add `gpu_mem=16` to `/boot/config.txt`
* reduce the power consumption while the device does nothing. The RPi has a auto-overclocking technology which rises the 
clock speed up to 1400 MHz, but the lower speed during low load is 600 MHz. We want to reduce this furter, to do so,
we add `arm_freq_min=300` to `/boot/config.txt`

All that can be done with commands (like):
```
touch /Volumes/boot/ssh
echo "dtoverlay=sdhost,overclock_50=100" | cat >> /Volumes/boot/config.txt
echo "gpu_mem=16" | cat >> /Volumes/boot/config.txt
echo "arm_freq_min=300" | cat >> /Volumes/boot/config.txt
```
..if the sd card is mounted on /Volumes/boot

* changing the node host name  
to do that, boot up the image with a Raspberry Pi and then edit the file `/etc/hostname`

For our cluster we want different host names for each node. We define that every node shall be named with names like
`node00`, `node01`, `node02`, `node03`, .. `node15` for a 16-node cluster.

Our cluster shall have a management node, one which has the purpose to do a steering of the other nodes.
That node shall be the node `node00`.

## Node Accounts
The Raspberry Pi has the default user `pi` and the default password `raspberry`. We can therefore use this with a clear-text ssh command to do the basic configuration steps. To do so, you need `sshpass`. Install it with
```
apt-get install sshpass
```
or  on a Mac with
```
brew install https://raw.githubusercontent.com/kadwanev/bigboybrew/master/Library/Formula/sshpass.rb
```
You can now log into your Raspberry Pi with the command
```
sshpass -p raspberry ssh pi@raspberrypi.local
```

We do so for node `node00` and configure passwordless access for all other nodes in the cluster.
We create a key pair on `node00` and distribute that key to all other cluster nodes.
Create the key pair with
```
ssh-keygen
```
The created key could be copied to another node `nodeXX` with
```
cat ~/.ssh/id_rsa.pub | ssh pi@nodeXX.local 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
```
Because we want to do this passwordless, call
```
cat ~/.ssh/id_rsa.pub | sshpass -p raspberry ssh pi@nodeXX.local 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
```
This must be done with all nodes.

We will now change the host name from `raspberrypi` to `node00`:
```
ssh pi@raspberrypi.local 'echo node00 | sudo tee /etc/hostname'
ssh pi@raspberrypi.local 'shutdown -r now'
```
or without using the public key with the default password:
```
sshpass -p raspberry ssh pi@raspberrypi.local 'echo node00 | sudo tee /etc/hostname'
```
If you repeat this with several nodes, you will probably get a
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```
This is correct and you must ignore host identification:
```
sshpass -p raspberry ssh -o GlobalKnownHostsFile=/dev/null -o UserKnownHostsFile=/dev/null pi@raspberrypi.local 'echo node00 | sudo tee /etc/hostname'
```

So the whole process to rename the hostname is:
* delete known hosts `rm .ssh/known_hosts`
* wait until host is up: `ping raspberrypi.local`
* boot up and add your public key: `cat ~/.ssh/id_rsa.pub | sshpass -p raspberry ssh -oStrictHostKeyChecking=no pi@raspberrypi.local 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'`
* verify that the key works: `ssh pi@raspberrypi.local`
* write the host name: `ssh pi@raspberrypi.local 'echo nodeXX | sudo tee /etc/hostname'`
* shut down the host: `ssh pi@raspberrypi.local 'sudo shutdown -h now'`
* re-boot and test the host name: `ssh pi@nodeXX.local`

## Node System Configuration
On every node we want some performance tweaks. Here i.e. we switch off swappiness:
```
sudo systemctl disable dphys-swapfile
sudo update-rc.d dphys-swapfile remove
```
Install base libraries for each peer:
```
ssh -o "StrictHostKeyChecking no" pi@nodeXX.local 'sudo apt-get -y install git oracle-java8-jdk gradle'
```
