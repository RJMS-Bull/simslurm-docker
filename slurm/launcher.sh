#!/bin/bash

/bin/date +%s

echo -e "\e[32m====================LAUNCHER\e[0m"
PATH="/opt/slurm/bin:$PATH"
# PATH="/home/davandg/bull/slurm.inst.1508/bin:$PATH"
# PATH="/home/davandg/bull/slurm.inst.sim/bin:$PATH"

/bin/date +%s
sinfo --version
echo -e "\e[32m$ sinfo\e[0m"
sinfo

echo -e "\e[32mSubmit a job\e[0m"
sbatch /home/root/slurm/job.sbatch

echo -e "\e[32mWait 100...\e[0m"
/bin/sleep 100

date +%s
echo -e "\e[32m$ sinfo\e[0m"
sinfo


echo -e "\e[32m$ squeue\e[0m"
squeue


echo -e "\e[32mWait 101...\e[0m"
sleep 101

date +%s
echo -e "\e[32m$ sinfo\e[0m"
sinfo


echo -e "\e[32m====================LAUNCHER END\e[0m"
