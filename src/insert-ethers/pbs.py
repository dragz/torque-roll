# -*- coding: utf-8 -*-
#
# PBS hostlist update module.
# 
# @Copyright@
# 
#               Rocks
#                www.rocksclusters.org
#               version 4.2.1 (Cydonia)
# 
# Copyright (c) 2006 The Regents of the University of California. All
# rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
#   "This product includes software developed by the Rocks 
#   Cluster Group at the San Diego Supercomputer Center at the
#   University of California, San Diego and its contributors."
# 
# 4. Neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: pbs.py,v $
# Revision 1.11  2006/09/11 22:50:00  mjk
# monkey face copyright
#
# Revision 1.10  2006/08/10 00:11:44  mjk
# 4.2 copyright
#
# Revision 1.9  2006/01/09 11:26:30  royd
# Added support for --batch and --norestart.
# Added support for --cpus=X.  Using the comment section of the node table
# to contain a static cpucount.  This is preliminary, needs more thinking...
#
# Revision 1.8  2005/11/01 08:08:29  royd
# Added restart of maui to make it pick up node changes.
#
# Revision 1.7  2005/10/27 11:07:06  royd
#
# fix to support private dns domains other than "local".
#
# is_compute(nodename,id) method added.  It checks for Compute = yes membership in the
# db and if not found it checks the output of pbsnodes -a hostname too see if
# the name is in the hostlist.  The latter is needed because on removal the
# host is gone from the database before this module is called.  is_compute is
# used on add and remove to see if it is a compute node, if not ignore it.
# This makes it possible to remove and add non-compute nodes without affecting
# the pbs setup and in addition it is now possible to have compute nodes with
# arbitrary names using --basename.
#
# Revision 1.6  2005/10/12 18:10:38  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:04:15  mjk
# updated copyright
#
# Revision 1.4  2005/06/10 21:53:42  royd
# Removed ugly workaround in update() and inserted a fix for a bug in
# insert-ethers 4.0.0 instead (thanks, Mason).
#
# The logic has changed to modify the hostlist when done() is called as it
# is no way to know the number of cpus until the node has asked for the
# kickstart file.  The added() method just generates a list of nodes to be
# added which is then fed to real_added() in done().
#
# Revision 1.3  2005/06/10 11:51:53  royd
# Change the plugin to use added,removed and update instead of restart.
# The update() method is an ugly hack as I cannot get db queries to work.
#
# It is now possible to add and remove nodes without restarting pbs_server.
#
# Revision 1.3  2005/05/27 22:34:56  fds
# Insert-ethers plugins also get node id for added(), removed().
#
# Revision 1.2  2005/05/24 21:22:01  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2005/03/14 20:25:18  fds
# Plugin architecture: service control is modular. Rolls can add hooks without
# touching insert-ethers itself. Plugins can be ordered relative to each other by
# filename.
#
#

import rocks.sql
from syslog import syslog
import os,sys

# The config setup is replicated in the rocks command remove plugin, eventually this
# will be moved to another place as common setup for all rocks command plugins
# in the torque roll. 
#
# DEFAULT values
UPDATE_NODE_LIST = 1

from ConfigParser import SafeConfigParser, NoOptionError
config = SafeConfigParser()
file = config.read("/etc/torque-roll.conf")
for fname in file:
    config.readfp(open(fname))

try:
    UPDATE_NODE_LIST = config.getint("DEFAULT","update_node_list")
except NoOptionError:
    pass


class Plugin(rocks.sql.InsertEthersPlugin):
    "PBS insert-ethers plugin"
    def __init__(self,app):
        rocks.sql.InsertEthersPlugin.__init__(self,app)
        self.addlist=list()
        self.daemons_need_restart = None
        
        #get the local domain from the database, some might change it.
        query = self.app.execute("select value from global_attributes where attr = 'Kickstart_PrivateDNSDomain';")
        if query:
            syslog(7, 'pbs.py: found domain')
            self.private_dnsdomain = self.app.fetchone()[0]
        else:
            self.private_dnsdomain = "local"
            
        #Get the appliances that has Compute=yes in the memberships table.
        query = self.app.execute("select appliance from memberships where name = 'Compute';")
        self.compute_appliances = list()
        for appliance in self.app.fetchall():
            self.compute_appliances.append(appliance[0])
        #Get login appliances
        query = self.app.execute("select appliance from memberships where name = 'Login';")
        self.login_appliances = list()
        for appliance in self.app.fetchall():
            self.login_appliances.append(appliance[0])
    
    
    def is_compute(self,nodename,id):
        if not UPDATE_NODE_LIST:
            return None
        query = self.app.execute("select membership from nodes where id = %s;"%id)
        
        # We cannot rely on the node being in the database. On --remove it is removed 
        # from the table before we get here.
        if query:
            membership = self.app.fetchone()[0]
            if membership in self.compute_appliances:
                return 1
            else:
                return None
        else:
            #Need to query the nodelist to see if we have a compute node
            pbsnodes = os.popen("/opt/torque/bin/pbsnodes -a %s"%nodename).read()
            if pbsnodes.find(nodename) != -1:
                return 1
            else:
                return None

    def is_login(self,nodename,id):
        if not UPDATE_NODE_LIST:
            return None
        query = self.app.execute("select membership from nodes where id = %s;"%id)
        if query:
            membership = self.app.fetchone()[0]
            if membership in self.login_appliances:
                return 1

        return None
        

    def restart_daemons(self):
        #
        # don't execute this code if we are in 'batch' or 'norestart'
        # mode (copied from sge plugin)
        #
        if '--batch' in self.app.caller_args or \
            '--norestart' in self.app.caller_args:
            return

        syslog(7,"pbs.py: Restarting pbs_server")
        os.system("/sbin/service pbs_server restart < /dev/null >& /dev/null")
        syslog(7,"pbs.py: Restarting maui")
        os.system("/sbin/service maui restart < /dev/null >& /dev/null")
        
    def added(self, nodename, id):
        """This function doesn't do the real addition to the
        hostlist it just generates a list of nodes to be added
        when the done() method is called.  The real adding of
        the node is done in real_added()."""

        self.addlist.append((nodename,id))
        
    def real_added(self, nodename, id):
        """This is where the real addition is done to the
        hostlist. Hopefully we will have the correct number of
        cpus now."""

        # we only add nodes that is a compute appliance
        if self.is_compute(nodename,id):
            m =  "pbs: adding %s to hostlist" % nodename
            query = self.app.execute("select cpus from nodes where id = %s;" % id)
            np = self.app.fetchone()

            np = str(np[0])
            os.system("/opt/torque/bin/qmgr -c"+
                  "'create node %s np=%s'" % (nodename, np))
            self.daemons_need_restart = 1   
        elif self.is_login(nodename, id):
            m = "pbs: adding %s to submit_hosts" % nodename
            os.system("/opt/torque/bin/qmgr -c"+
                  "'set server submit_hosts-=%s'" % (nodename, ))
            os.system("/opt/torque/bin/qmgr -c"+
                  "'set server submit_hosts+=%s'" % (nodename, ))
        else:
            m = "pbs: ignoring node %s" % nodename
        syslog(7,m)


    def removed(self, nodename, id):
        """Remove the node from the list of compute nodes."""
        if self.is_compute(nodename,id):
            m =  "pbs: deleting %s from hostlist" % nodename
            os.system("/opt/torque/bin/qmgr -c"+
                    "'delete node %s'" % nodename)
            self.daemons_need_restart = 1
        elif self.is_login(nodename, id):
            m = "pbs: removing %s from submit_hosts" % nodename
            os.system("/opt/torque/bin/qmgr -c"+
                  "'set server submit_hosts-=%s'" % (nodename, ))
        else:
            m = "pbs: ignoring node %s" % nodename
        syslog(7,m)


    def update(self):
        "Redo the whole compute node list"

        m =  "insert-ethers running pbs update "
        syslog(7,m)
        query = self.app.execute("select name,id from nodes order by rack,rank;")
        for name,id in self.app.fetchall():
        #    self.removed(name,id)
            self.real_added(name,id)
        self.restart_daemons()

    def done(self):
        """Doing the real addition of nodes here because we
        cannot know the number of cpus before the nodes have
        asked for a kickstart file."""

        syslog(7,"pbs.py: done called")
        if self.addlist:
            m =  "pbs: adding the new nodes."
            syslog(7,m)

            for name, id in self.addlist:
                self.real_added(name,id)
        if self.daemons_need_restart:
            self.restart_daemons()      
