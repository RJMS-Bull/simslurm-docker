#!/bin/sh
#SBATCH -J job_1
#SBATCH -n 250
#SBATCH -t 20:00
#SBATCH -o ./job.sbatch.out


/usr/bin/sleep 200

exit 0
