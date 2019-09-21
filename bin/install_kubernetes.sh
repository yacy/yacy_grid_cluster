# clean up
sudo apt -y remove aufs-dkms
sudo apt -y autoremove

# disable swap
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo update-rc.d dphys-swapfile remove

# install kubeadm, kubelet and kubectl
curl -L --remote-name-all https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/arm/{kubeadm,kubelet,kubectl}
chmod +x {kubeadm,kubelet,kubectl}
sudo mv {kubeadm,kubelet,kubectl} /usr/bin/

# install systemd service
curl -L --remote-name-all https://raw.githubusercontent.com/kubernetes/kubernetes/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/build/debs/{kubelet.service,10-kubeadm.conf}
sudo mkdir -p /etc/systemd/system/kubelet.service.d
sudo mv 10-kubeadm.conf /etc/systemd/system/kubelet.service.d/
sudo mv kubelet.service /etc/systemd/system/

# enable service
sudo systemctl enable --now kubelet
sudo kubeadm init
mkdir -p ~/.kube
sudo cp -i /etc/kubernetes/admin.conf ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
#kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
#kubectl proxy --address='0.0.0.0' --accept-hosts='.*'
