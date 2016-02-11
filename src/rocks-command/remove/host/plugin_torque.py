# $Id: plugin_sge.py,v 1.2 2008/04/17 21:59:50 bruno Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
# All rights reserved.	
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
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
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
# $Log: plugin_sge.py,v $
# Revision 1.2  2008/04/17 21:59:50  bruno
# fix host remove SGE plugin
#
# Revision 1.1  2008/04/15 22:17:38  bruno
# use rocks command line to cleanup SGE state for a removed node
#
#

import os
import rocks.commands
from syslog import syslog

# The config setup is replicated in the insert-ethers plugin, eventually this
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

class Plugin(rocks.commands.Plugin):

    def provides(self):
        return 'torque'

    def run(self, host):
        global UPDATE_NODE_LIST
        if not UPDATE_NODE_LIST:
            m = "pbs: not touching the nodelist."
            syslog(7,m)
            return
        m = "pbs: deleting node %s"%host
        syslog(7,m)
        os.system("qmgr -c 'delete node %s'"%host)
        os.system("qmgr -c 'set server submit_hosts-= %s'"%host)

##    cmd = 'cd /opt/gridengine'
##		cmd += ' && echo "" | ./inst_sge -ux -host %s' % (host)
##		cmd += ' > /dev/null 2>&1'
##		os.system(cmd)
##
##		cmd = 'qconf -dh %s > /dev/null 2>&1' % (host)
##		os.system(cmd)

