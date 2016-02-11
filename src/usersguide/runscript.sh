#!/bin/sh
# A job script example for the torque-roll for Rocks
#
# Each directive MUST start with #PBS
#PBS -lwalltime=1:00:00      # One hour runtime
#PBS -lnodes=2:ppn=2         # 2 nodes with 2 cpus each
#PBS -lpmem=1gb              # 1 GB memory per cpu
#PBS -Nmpi-verify-openmpi    # the name of the job

cd $PBS_O_WORKDIR                   # cd to the directory the job was submitted from
                                    # the job is initiated in the users home dir on the compute node

. /opt/torque/etc/openmpi-setup.sh  # set the enviroment vars needed to make OpenMPI work with torque

                                    # We have pre-made an application in the submit dir:
                                    # cp /opt/mpi-tests/src/mpi-verify.c .
                                    # mpicc mpi-verify.c -o mpi-verify.openmpi.x

mpirun ./mpi-verify.openmpi.x

qstat -f $PBS_JOBID | grep -i resource   # List resource usage in the job stdout report

                                    # when the script exits the job is done
