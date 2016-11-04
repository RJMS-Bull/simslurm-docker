# Use Simunix to simulate a full HPC cluster managed by Slurm

This tutorial shows how to use docker and Simunix to simulate a full HPC cluster managed by Slurm. 

## Prerequisites

* You need to have Docker installed, and an internet connection for at least the first deployment. 
    * In case you already have the simunix-docker image no internet connection is needed.
* You need to download or clone the Simunix repository to build its docker.

## 1. Download and install Simunix docker

```bash
git clone https://github.com/RJMS-Bull/simunix
cd simunix
docker build -t simunix-docker .
```

## 2. Download the repository which contains the experimentation

```bash
git clone https://github.com/RJMS-Bull/simslurm-docker
cd simunix
docker build -t simslurm .
```

## 3. Run the experimentation

Once you built the simslurm image you can launch the simulation. 
The first thing to do is to run the default simulation with a docker run.

```bash
docker run -t -i  simslurm
```

By default the docker create a simulation of 10 nodes (one slurmctld and 9 slurmd). 

## 4. Launch Simunix manually 

Simunix needs to arguments. The first argument is the platform file which describes the physical platform Simunix needs to simulate. The second argument is the deployment file which describes where process will be run.

The fortunately the image already contains those two files, so you can run the simulation with the following command.

```bash
pwd # /home/root
simunix/bin/simunix_starter.sh slurm/gen_platform.xml slurm/gen_deployment.xml
```

## 5. Configure your simulation

To configure the simulation you can customize:
* The number of nodes
* The workload

### Configure the platform

To create a new platform, you can use the script `slurm/create_platform.py`.

```bash
pwd # home/root
cd slurm && python create_platform.py 100
```

The command above will generate a platform of 100 nodes and the deployment file. In addition, it creates the new Slurm configuration for the simulation.

To launch your new simulation:

```bash
pwd #/home/root
mv -f slurm/slurm.con /usr/local/etc/
simunix/bin/simunix_starter.sh slurm/gen_platform.xml slurm/gen_deployment.xml
```

### Create your workload

You can also configure the jobs you want to submit to slurm. 
the only thing to do is to edit the file `slurm/launcher.sh`

**Be aware that srun does not work yet**