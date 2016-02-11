--------------------------------
TORQUE ROLL DOCUMENTATION
--------------------------------

:Author: Roy Dragseth, roy.dragseth@uit.no


.. contents::

================
Introduction
================

The torque-roll provides a batch system for the Rocks_ Cluster Distribution.

.. _Rocks: http://www.rocksclusters.org

The batch system consists of the Torque resource manager and the Maui scheduler which together provides an alternative to the Sun Grid Engine (SGE) that comes as the default batch system with Rocks.  The torque roll will not work on a system that has an active sge-roll installed.  The best solution is to reinstall your frontend with the torque-roll instead of the sge-roll.

Roll basics
============

Included software
--------------------

The torque roll contains software collected from the following places

============  =======================================================
Torque         http://www.clusterresources.com/products/torque
Maui           http://www.clusterresources.com/products/maui
mpiexec        http://www.osc.edu/~pw/mpiexec/
pbstools       http://www.osc.edu/~troy/pbs/
pbspython      ftp://ftp.sara.nl/pub/outgoing/
============  =======================================================



Links
----------------

========================= ===========================================================================
Homepage                  https://source.uit.no/hpc/torque-roll/wikis/home
Download                  ftp://ftp.uit.no/pub/linux/rocks/torque-roll
Source code               https://source.uit.no/hpc/torque-roll
Rocks PBS Wiki	          https://wiki.rocksclusters.org/wiki/index.php/Roy_Dragseth#PBS_roll_stuff
========================= ===========================================================================

Support
---------------

The `rocks mailing list`_ is the preferred place to get help and discuss the torque-roll as there are a lot of people on this list with hands-on experience from using the torque-roll on Rocks.  Before posting questions to the list you should search the `list archives`_ for the terms pbs or torque, as the answer to your problems might be there already.

.. _`rocks mailing list`: https://lists.sdsc.edu/mailman/listinfo/npaci-rocks-discussion
.. _`list archives`: http://marc.info/?l=npaci-rocks-discussion

Installation
---------------

It is assumed that you know how to install a Rocks roll on a frontend, see the main Rocks documentation for an intro to installation of a Rocks cluster. You can either burn the roll iso on a CD or install from a central server, both methods are equivalent.


=======================
User guide
=======================

When the rocks frontend is installed with the torque-roll it will have a functioning batch system, but you will not be able to run any jobs until you have installed some compute nodes.  As you detect and install new compute nodes with ``insert-ethers`` they will automatically be included in the node list and start receiving jobs as soon as they are up and running.


Running jobs
==============

The normal way of using a batch system is through submitting jobs as scripts that get executed on the compute nodes.  A job script can be any shell (bash, csh, zsh), python, perl or whatever supports the # comment character.  The most common is though to use sh or csh as job script syntax.  The job script is a regular script with some special comments that is meaningful to the batch system.  In torque all lines beginning with ``#PBS`` are interpreted by the batch system.  You submit the job with the ``qsub`` command::

  qsub runscript.sh


A serial job
-------------------

It is useful to give info about expected walltime and the number of cpus the job needs.  Here is how runscript.sh could look like for a single cpu job::

  #!/bin/sh
  #PBS -lwalltime=1:00:00
  #PBS -lnodes=1
  
  ./do-my-work

This script asks for 1 hour runtime and will run on one cpu.  The job will terminate when the script exits or will be terminated by the batch system if it passes the 1 hour runtime limit.  The ``#PBS`` directives can also be given as commandline arguments to ``qsub`` like::

  qsub -lnodes=1,walltime=1:00:00 runscript.sh

Commandline arguments takes precedence over runscript directives. Note that ``#PBS`` must be given exactly like this as the first characters on the line, no extra #s or spaces.  All ``#PBS`` directives must come before any shell statements or else they will be ignored by the batch system.

When the job is finished you will get back two files with the standard output and standard error for the job in the same directory you submitted the job from.  See ``man qsub``.

A parallel job
------------------

If you have a parallel application using MPI_ you can run parallel jobs within the batch system. 
Let us take a look at the following script::

  #!/bin/sh
  #PBS -lwalltime=1:00:00
  #PBS -lnodes=10
  #PBS -lpmem=2gb
  #PBS -N parallel_simulation
  
  mpirun ./do-my-work

.. _MPI:  http://www.mpi-forum.org

Note: this runscript will probably not work in its current form as different MPI-implementations need different commands to start the application, see below.

The runscript above is a parallel job that asks for 10 cpus and 2 gigabytes of memory per cpu, the scheduler will then make sure these resources are available to the job before it can start.  The runscript will be run on the first node in the nodelist assigned to this job and ``mpirun`` will take care of launching the parallel programme named ``do-my-work`` on all of the cpus assigned to this jobs, possibly on several compute nodes.  If you ask for more resources than is possibly available on a node the job will either be rejected at submit time or will never start.

Different kinds of MPI libraries
---------------------------------------

Since quite a few implementations of the MPI libraries exist, both free and commercial, it  is not possible to cover all possible ways to start any MPI-application in this document.  The focus will be on the ones that ships with Rocks: OpenMPI_ and MPICH2_.

OpenMPI
,,,,,,,,,,,,

Rocks comes with a it's own compilation of OpenMPI_ installed in ``/opt/openmpi/``.  This is the system-wide default and is used by the ``mpicc/mpif90`` compilers in the default path.  Although OpenMPI has support for the torque tm-interface (tm=taskmanager) it is not compiled into the library shipped with Rocks (the reason for this is that the OpenMPI build process needs to have access to libtm from torque to enable the interface).  The best workaround is to recompile OpenMPI on a system with torque installed.  Then the mpirun command can talk directly to the batch system to get the nodelist and start the parallel application using the torque daemon already running on the nodes.  Job startup times for large parallel applications is significantly shorter using the tm-interface that using ssh to start the application on all nodes.  If you recompile OpenMPI you can use the above runscript example as-is.

If however you for some reason do not rebuild the OpenMPI library you can use a workaround provided with the torque-roll.  The torque roll contains a python-wrapper script named ``pbsdsh-wrapper`` that will make ``pbsdsh`` behave like ssh.  ``pbsdsh`` can run arbitratry commands under the taskmanager on remote nodes participating in the job.  

All that is needed is to setup a few environment variables for OpenMPI::

  #!/bin/sh
  #PBS -lwalltime=1:00:00
  #PBS -lnodes=10
  #PBS -lpmem=2gb
  #PBS -N parallel_simulation
  
  cd $PBS_O_WORKDIR

  source /opt/torque/etc/openmpi-setup.sh

  mpirun ./do-my-work

The ``openmpi-setup.sh`` takes care of setting a few enviroment variables to make mpirun use the ``pbsdshwrapper`` to start the application.  The runscript itself can be found here_ and in ``/var/www/html/roll-documentation/torque/runscript.sh`` on the frontend.

.. _OpenMPI: http://www.open-mpi.org/
.. _here: ./runscript.sh

MPICH2
,,,,,,,,,,,,,,,

The basic Rocks installation also contain MPICH2_.  This library has a different startup mechanism than OpenMPI.  MPICH2 is installed in ``/opt/mpich2/gnu/`` and has its own ``mpif90/mpicc`` wrappers.  The torque-roll provides the ``mpiexec`` jobs launcher that provides the tight binding to the taskmanager.  ``mpiexec`` is a stand-alone product installed in ``/opt/mpiexec/`` and must not be confused with ``mpiexec`` from OpenMPI.  The safest way to use it is to use the explicit path in the runscript::


  #!/bin/sh
  #PBS -lwalltime=1:00:00
  #PBS -lnodes=10
  #PBS -lpmem=2gb
  #PBS -N parallel_simulation
  
  cd $PBS_O_WORKDIR

  /opt/mpiexec/bin/mpiexec ./do-my-work

``mpiexec`` can start applications using several other MPI implementations like INTEL MPI and MVAPICH2.

.. _MPICH2: http://www.mcs.anl.gov/research/projects/mpich2/


For more info see the links in the `Included software`_ section.


Inspecting the jobs in the queue
===================================

There are several commands that will give you detailed information about the jobs in the batch system.

+----------+--------------------+----------------------------------------+
|Command   |  Task              |     useful flags                       |
+----------+--------------------+----------------------------------------+
|showq     | List jobs in queue |   -r -- only running jobs              |
+          +                    |                                        |
|          |                    |   -i -- only idle jobs                 |
+          +                    |                                        |
|          |                    |   -b -- only blocked jobs              |
+          +                    |                                        |
|          |                    |   -u username -- this user only        |
+----------+--------------------+----------------------------------------+
|qstat     |  List jobs in queue|  -f jobid -- list details              |
+          +                    +                                        +
|          |                    |  -n  -- list nodes assigned to job     |
+----------+--------------------+----------------------------------------+

While both showq and qstat do the same task the output is quite different, ``showq`` has
the nice feature of sorting the jobs with respect to time to completion which makes it
easy to see when resources will become available.

=====================
Administrator guide
=====================


In it's default configuration the batch system is set up as a FIFO system, but it is possible to change this to accomodate almost any scheduling policy.  Maui can schedule on cpus, walltime, memory, disk size, network topology and more.  See the maui and torque documentation for a full in-depth understanding of how to tune the batch system.


Setting node properties.
==========================

Node properties provides the possibility to flag nodes as having special features.  As clusters have a tendency to grow inhomogeneous over time it is useful to have way to group nodes with similar features.  Node properties are only text strings and their names do not need to have any logical resemblance with what they actually describe.  But a user might have a better understanding of what a node with the "fast" property is over a "xyz" property.

Pre torque-roll 5.3
----------------------

As the command ``rocks sync config`` would overwrite the torque node-list the only way to make node properties persistent was to turn off automatic updates of the node list by editing ``/etc/torque-roll.conf``.  This method still works for torque-roll v5.3 and upwards.

Torque-roll 5.3 and onwards
-----------------------------

As of torque-roll v5.3 and up node properties can be set using the rocks concept of node attributes with the rocks command line tool.  This is best illustrated by an example::

  # rocks set host attr compute-0-0  torque_properties fast
  # rocks set host attr compute-0-1  torque_properties slow
  # rocks report pbsnodes | sh

This method will make the node properties sticky and automatic node list updates will still work.

The node properties will now appear in the node info and users can now submit jobs to only run on either fast or slow nodes::

  $ pbsnodes compute-0-0
  $ pbsnodes compute-0-1
  $ qsub -lnodes=1:fast runscript.sh
  $ qsub -lnodes=1:slow runscript.sh

If no flag on the qsub command is given then scheduling will be done as if the node properties were not set.

Each node can have more than one property.  Names are separated by commas, for instance::

   # rocks set host attr compute-0-0  torque_properties fast,highmem


Useful scheduling parameters
==================================

Some answers to often asked questions on the mailing list.

Maui vs torque
----------------

Torque is the resource manager, its task is to collect info about the state of the compute nodes
and jobs.
Maui is the scheduler, its task is to decide when and where to run the jobs submitted to torque.

Most things can be achieved by modifying /opt/maui/maui.cfg. 
Maui needs a restart after changing the config file::

  service maui restart

*Advice:* If you can achieve the same thing by changing either torque or maui, use maui.
Restarting maui is rather lightweight operation, and seldom causes problems for live systems.
Restarting pbs_server can make the system oscillatory for a few minutes as
pbs_server needs to contact all pbs_moms to get back in state.


Needed job info
-------------------

To make the maui scheduler able to make informed decisions on how to prioritize jobs and on what nodes they should be started on it needs info about the jobs.
The minimum requirement is the number of cpus and walltime. Information about memory requirements for the job is also useful.  For instance::

  #PBS -lwalltime=HH:MM:SS
  #PBS -lnodes=10:ppn=8
  #PBS -lpmem=1gb

Memory handling on linux
--------------------------

torque/maui supports two memory specification types, (p)mem and (p)vmem on linux.

* pmem is not enforced, it is used only as information to the scheduler.
* pvmem is enforced, procs that exceed the limit will be terminated.
  The pbs_mom daemon limits vmem size by setting the equivalent of ulimit -v on the processes it controls.

It is currently not possible to limit the amount of physical memory a process can allocate on a linux system.  One can only limit the amount of virtual memory.  Virtual memory is the physical memoroy + swap.   See ``man pbs_resources_linux`` for details.

Tuning the batch system
----------------------------

Torque is installed in ``/opt/torque``. ``qmgr`` is the torque management command

**Friendly advice:** backup your working config before modifying the setup::

  # qmgr -c “print server” > /tmp/pbsconfig.txt

Roll back to escape from a messed up system::

  # qterm; pbs_server -t create
  # qmgr < /tmp/pbsconfig.txt

This will bring you back to where you started.  
**Remark:** this will wipe the whole queue setup and all currently queued and running jobs will be lost!

The default batch configuration from the torque-roll is saved in ``/opt/torque/pbs.default``. Do this to get back the original setup that came with the torque-roll::

  # qterm; pbs_server -t create
  # qmgr < /opt/torque/pbs.default


Prioritizing short jobs
-------------------------

Often it is useful to give shorter jobs higher priority.
It is recommended to use the XFACTOR feature in maui rather than torque queues with different priorites.::

  XFACTORWEIGHT 1000

XFACTOR is defined as::

  XFACTOR=(walltime+queuetime)/walltime

XFACTOR will increase faster for shorter walltimes thus giving higher priorities for short jobs.
Depends on users giving reasonable walltime limits.


Prioritizing large jobs (maui)
----------------------------------

In a cluster with a diverse mix of jobs it is often desirable to prioritize the large jobs and make the smaller ones fill in the gaps.::

   CPUWEIGHT 1000
   MEMWEIGHT 100

This should be combined with fairshare to avoid starving users falling outside this prioritization.

Fairshare (maui)
-----------------

Also known as

   “Keeping all users equally unhappy”

Can be done on several levels
users, groups.....

Set a threshold::

  USERCFG[DEFAULT] FSTARGET=10
  FSWEIGHT 100

Users having used more than 10% will get reduced priority and vice versa.

Adjusting your policy
----------------------

You can play with the weights to fine-tune your scheduling policies::

  XFACTORWEIGHT 100
  FSWEIGHT 1000
  RESWEIGHT 10
  CPUWEIGHT 1000
  MEMWEIGHT 100

Analyze the prioritization with ``diagnose -p``

Job node distribution
------------------------

Default is MINRESOURCE
Run on the nodes which gives the least unused resources.

Spread or pack?::

  NODEALLOCATIONPOLICY PRIORITY

Select the most busy nodes first::

  NODECFG[DEFAULT] PRIORITYF=JOBCOUNT

Select the least busy nodes first::

  NODECFG[DEFAULT] PRIORITYF=-1.0*JOBCOUNT

Node access policy
--------------------

Default access policy is SHARED
Can choose to limit this to SINGLEJOB or SINGLEUSER, for instance::

  NODEACCESSPOLICY SINGLEUSER

Single user access prevents users from stepping on each others toes while allowing good utilization for serial jobs.

Throttling policies
--------------------

Sometimes one needs to limit the user from taking over the system::

  MAXPROC, MAXPE, MAXPS, MAXJOB, MAXIJOB

All can be set for all or individual users and groups::

  USERCFG[DEFAULT], USERCFG[UserA] etc.

Debugging and analyzing
--------------------------

Lot of tools::

  pbsnodes 	-- node status
  qstat -f		-- all details of a job
  diagnose -n	-- node status from maui
  diagnose -p	-- job priority calculation
  showres -n	-- job reservation per node
  showstart	-- obvious
  checkjob/checknode – also pretty obvious..


Example: express queue
=======================

Goal: Supporting development and job script testing, but prevent misuse

Basic philosophy:

* Create a separate queue
* Give it the highest priority
* Throttle it so it is barely usable

Create the queue with qmgr::

  create queue express                     
  set queue express queue_type = Execution 
  set queue express resources_max.walltime = 08:00:00
  set queue express resources_default.nodes = 1:ppn=8
  set queue express resources_default.walltime = 08:00:00
  set queue express enabled = True                       
  set queue express started = True 

Increase the priority and limit the usage::

  CLASSWEIGHT             1000
  CLASSCFG[express] PRIORITY=1000 MAXIJOB=1  MAXJOBPERUSER=1 QLIST=express QDEF=express
  QOSCFG[express] FLAGS=IGNUSER

This will allow users to test job scripts and run interactive jobs with good turnaround by submitting to the express queue, ``qsub -q express .......``.  At the same time misuse is prevented since only 1 running job is allowed per user.

=============
Appendix.
=============

Building the roll from source
==============================

This is only relevant if you want to change something in how the torque-roll is built.  The default build should cover most needs.

Clone the repository into the rocks build tree on a frontend::

  cd /opt/rocks/share/devel/roll/src/
  git clone git@source.uit.no:hpc/torque-roll.git torque

Building::

  cd torque
  make buildsetup
  cd src/torque
  make rpm
  cd ../..
  rpm -i RPMS/x86_64/torque*.rpm
  make roll

You should now have a torque iso file that you can install on a frontend::

  cp torque*.iso /tmp
  cd /export/rocks/install
  rocks add roll /tmp/torque*.iso
  rocks enable roll torque
  rocks create distro
  rocks run roll torque | sh
  reboot

After boot you can insert compute nodes insert-ethers or run rocks sync config to populate the nodelist in torque with existing compute nodes.  (Remember that you need to reinstall the compute nodes to install rocks on them.)

A complete job session.
===============================

A hands on session including compiling the program and running it in the queue.

Log in and prepare the source::

  [royd@hpc2 ~]$ cp /opt/mpi-tests/src/mpi-verify.c .                               
  [royd@hpc2 ~]$ mpicc mpi-verify.c -o mpi-verify.openmpi.x                         

We have a runscript ready with the correct setup for OpenMPI::

  [royd@hpc2 ~]$ cat run-openmpi.sh
  #!/bin/sh
  #PBS -lnodes=2:ppn=2,walltime=1000
  
  # list the name of the nodes participating in the job. pbsdsh can run
  # any command in parallel
  pbsdsh uname -n
  
  . /opt/torque/etc/openmpi-setup.sh
  
  mpirun mpi-verify.openmpi.x

  date

Submit the job with ``qsub``, it will print the jobid upon successful submission::

  [royd@hpc2 ~]$ qsub run-openmpi.sh                                                
  15.hpc2.cc.uit.no                                                               

List the jobs in the queue, as you can see the job has already started::
  
  [royd@hpc2 ~]$ showq
  ACTIVE JOBS--------------------
  JOBNAME            USERNAME      STATE  PROC   REMAINING            STARTTIME
  
  15                     royd    Running     4    00:16:40  Tue Jan 26 10:11:32
  
       1 Active Job        4 of    6 Processors Active (66.67%)
                           2 of    3 Nodes Active      (66.67%)

  IDLE JOBS----------------------
  JOBNAME            USERNAME      STATE  PROC     WCLIMIT            QUEUETIME
  
  
  0 Idle Jobs
  
  BLOCKED JOBS----------------
  JOBNAME            USERNAME      STATE  PROC     WCLIMIT            QUEUETIME
  
  
  Total Jobs: 1   Active Jobs: 1   Idle Jobs: 0   Blocked Jobs: 0

You can also use ``qstat`` to view the jobs in the queue::

  [royd@hpc2 ~]$ qstat
  Job id                    Name             User            Time Use S Queue
  ------------------------- ---------------- --------------- -------- - -----
  15.hpc2                   run-openmpi.sh   royd                   0 R default


When the job finishes you will get two files back to where you submitted the job from. One with 
stdout and one for stderr of the job.  Very useful for debugging jobscripts::


  [royd@hpc2 ~]$ ls
  mpi-verify.c  mpi-verify.openmpi.x  run-openmpi.sh  run-openmpi.sh.e15  run-openmpi.sh.o15
  [royd@hpc2 ~]$ cat run-openmpi.sh.e15
  Process 0 on compute-0-2.local
  Process 1 on compute-0-2.local
  Process 2 on compute-0-1.local
  Process 3 on compute-0-1.local
  [royd@hpc2 ~]$ cat run-openmpi.sh.o15
  compute-0-2.local
  compute-0-2.local
  compute-0-1.local
  compute-0-1.local
  Tue Jan 26 10:11:33 CET 2010
  [royd@hpc2 ~]$

Now, try this yourself...


