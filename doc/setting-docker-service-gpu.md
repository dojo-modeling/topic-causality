# Summary

Utilizing GPU on docker requires some additional setup, as well as possibly setting up a fresh Ubuntu EC2 instance with no GPU proprietary drivers installed. The following guide describes the steps needed to set this up.
Steps
This guide assumes that the container uses an nvidia-compatible graphics card, with no proprietary drivers installed. On your terminal, run nvidia-smi up-front if you’d like to check if drivers and tools are installed for nvidia.

Add the nvidia container runtime registry, necessary for docker:

```console
$ curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | \
  sudo apt-key add -

$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID)

$ curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
```

Ensure there are no pending OS upgrades, and update package repository:

```console
$ sudo apt update && sudo apt upgrade
```

Esure the latest kernel dev headers are available:

```console
$ sudo apt install linux-headers-$(uname -r)
```


Install the nvidia container runtime, as well as the nvidia proprietary drivers:


```console
$ sudo apt-get install nvidia-container-runtime

$ sudo apt install nvidia-driver-525-server nvidia-dkms-525-server
```

Optional: 525 might not be the latest drivers, you may search through apt or apt-cache by searching for nvidia-driver- and grepping for a match with version digits:

```console
apt-cache search 'nvidia-driver-' | grep '^nvidia-driver-[[:digit:]]*'
```

If you which to debug the availability of graphics card and complete setup of nvidia driver, install:
sudo apt install mesa-utils

You may run:

```console
sudo lshw -c video
```

After installing container runtime and nvidia drivers, reboot your system:

```console
sudo reboot
```

If on a remote machine, you’ll need to wait for the instance to come back up available before re-connecting.

Optional: Rebooting will also restart the docker engine daemon, which would be needed in order to use the nvidia container runtime. If done as separate steps, you’ll likely need to run:

```consoloe
$ sudo systemctl restart docker
```

Debugging: run nvidia-smi on host. It should output a table with GPU device id information. To test that docker can also access the GPU device, you may use this command to pull an ubuntu image and test the same command:


```consoloe
docker run --it --gpus all ubuntu nvidia-smi
```

If all looks good, you may run your container with a similar run command as above (--gpus all) or set up docker-compose with access to GPU. See references linked below for docker compose setup instructions (overlap with the above steps, only difference needed is the docker-compose.yaml file contents themselves).

# References

- https://nvidia.github.io/nvidia-container-runtime/

- https://docs.docker.com/config/containers/resource_constraints/#gpu

- https://docs.docker.com/compose/gpu-support/

- https://www.cyberciti.biz/faq/ubuntu-linux-install-nvidia-driver-latest-proprietary-driver/



