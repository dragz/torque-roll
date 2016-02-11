Torque roll info
====================

Build instructions
--------------------

Add this to /etc/yum.conf::

    [CentOS5]
    name=CentOS 5 std distro
    baseurl=http://fedora.uib.no/centos/5/os/x86_64/
    enabled=yes


    [CentOS5-updates]
    name=CentOS 5 std distro
    baseurl=http://fedora.uib.no/centos/5/updates/x86_64/
    enabled=yes

    [EPEL]
    name=EPEL
    baseurl=http://fedora.uib.no/epel/5/x86_64/
    enabled=yes


Install:: 

    # yum install tclx-devel python-docutils readline-devel pam-devel


Build on a rocks frontend::

    # cd /opt/rocks/share/devel/src/roll
    # git clone https://source.uit.no/hpc/torque-roll.git
    
    # cd torque/src/torque
    # make rpm

    # cd ../..
    # rpm -i RPMS/x86_64/torque-2.4.11-1.x86_64.rpm 

    # cd src/mauiweb
    # hg clone http://devsrc.cc.uit.no/mauiweb

    # cd ../..
    # make roll

