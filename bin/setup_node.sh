#!/bin/bash
until ping -c1 raspberrypi &>/dev/null; do :; done
sshpass -p raspberry ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no pi@raspberrypi 'echo '$1' | sudo tee /etc/hostname && rm -Rf .ssh && mkdir .ssh && chmod 700 .ssh'
sshpass -p raspberry scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ~/.ssh/id_rsa.pub pi@raspberrypi:~/.ssh/authorized_keys
sshpass -p raspberry ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no pi@raspberrypi 'sudo shutdown -r now'
