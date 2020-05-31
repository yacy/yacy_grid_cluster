# clean up
sudo apt-get update
suso apt-get -y upgrade
sudo apt -y remove aufs-dkms
sudo apt -y autoremove

# disable swap
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo update-rc.d dphys-swapfile remove

# install docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
newgrp docker

# also install docker-compose
sudo apt-get install -y libffi-dev libssl-dev python3 python3-pip
sudo pip3 install docker-compose
