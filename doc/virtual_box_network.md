# Network Simulation with Virtual Box VMs
To simulate a grid computing on several servers, we can use VirtualBox to make VMs.

## VM Configuration
After one single VM is created, we must clone one VM into many instances and set different IP addresses for each VM.
Furthermore each of the node must be able to access not only the internet but also other nodes within the network.
We enable this using two network connections in each nodes. One is a NAT adapter to access the internet, a second
one is a Host-Only adapter to address other nodes within the same network.

* Open the Host Network Manager (File -> Host Network Manager) and create an adaprger named `vboxnet0`:
  * Set IPv4 Address to `192.168.56.1`
  * IPv4 Network Mask `255.255.255.0`
  * IPv6 Prefix Length `0`
  * DHCP activated

* Open your virtual machine settings -> Network
  * Adapter 1 -> Enable, Attached to `NAT`
  * Adapter 2 -> Enable, Attached to `Host-only Adapter`, Name: `vboxnet0`
  
* Within your virtual machine, edit the file `/etc/network/interfaces`
  * set the following content:
```
source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug enp0s3
iface enp0s3 inet dhcp

allow-hotplug enp0s8
iface enp0s8 inet static
address 192.168.56.2
netmask 255.255.255.0
```

* once you start cloning the first node, create different addresses for each of the node

## Node Network
To simulate a node cluster, we want to use the host names `node00.local`, ... `node16.local` to be connected to our cluster.
Therefore we map the host names with IP addresses like
```
192.168.56.100	node00.local
192.168.56.101	node01.local
192.168.56.102	node02.local
.
.
.
192.168.56.116	node16.local
```
