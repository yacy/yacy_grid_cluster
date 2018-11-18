sshpass -p raspberry ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no pi@raspberrypi.local 'echo $1 | sudo tee /etc/hostname && rm -Rf .ssh && mkdir .ssh && chmod 700 .ssh'
sshpass -p raspberry scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ~/.ssh/id_rsa.pub pi@raspberrypi.local:~/.ssh/authorized_keys
sshpass -p raspberry ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no pi@raspberrypi.local 'sudo shutdown -r now'
