Torque roll info
====================

Build instructions
--------------------

Install:: 

    # yum --enablerepo base,updates install tclx-devel python-docutils readline-devel pam-devel


Build on a rocks frontend::

    # cd /opt/rocks/share/devel/src/roll
    # git clone https://github.com/dragz/torque-roll.git torque
    
    # cd torque/src/torque
    # make rpm

    # cd ../..
    # rpm -i RPMS/x86_64/torque-2.4.11-1.x86_64.rpm 

    # make roll

