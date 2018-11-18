echo "dtoverlay=sdhost,overclock_50=100" | cat >> /Volumes/boot/config.txt
echo "gpu_mem=16" | cat >> /Volumes/boot/config.txt
echo "arm_freq_min=300" | cat >> /Volumes/boot/config.txt
touch /Volumes/boot/ssh
#sed -i '.bak' 's/tty1/tty1 cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory/g' /Volumes/boot/cmdline.txt
