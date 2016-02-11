# -*- coding: utf-8 -*-
# $Id: __init__.py,v 1.5 2009/10/14 22:54:05 bruno Exp $
#
# @Copyright@
# 
#               Rocks(r)
#                www.rocksclusters.org
#              version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
#   "This product includes software developed by the Rocks(r)
#   Cluster Group at the San Diego Supercomputer Center at the
#   University of California, San Diego and its contributors."
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
# $Log: __init__.py,v $
# Revision 1.5  2009/10/14 22:54:05  bruno
# need quotes
#
# Revision 1.4  2009/10/07 19:09:17  bruno
# throttle the number of concurrent connections. useful for large clusters.
# thanks to Roy Dragseth for this fix.
#
# Revision 1.3  2009/10/06 22:42:42  bruno
# patch from anoop
#
# Revision 1.2  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.1  2009/03/24 22:24:04  bruno
# moved 'dbreport tentakel' to rocks command line
#
#

import rocks.commands.report
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


class Command(rocks.commands.report.command):
    """
        Create a report that can be used to update the node list by 
    piping this to a shell.
        
        <example cmd='report pbsnodes'>                
        Create commands suitable as input to a shell for updating the node list.
        </example>
    """
    
    def run(self, params, args):
      # Bail out if the user says we shouldn't touch the nodelist.
      if not UPDATE_NODE_LIST:
        return
      qmgr = "qmgr"

#     dn = self.getGlobalVar("Kickstart","PrivateDNSDomain")

      # Query the database for compute node info by doing a killer join.
      # Thanks Bruno!
      query=('select nodes.name, nodes.cpus from nodes, memberships '
        'where (nodes.membership = memberships.id '
        'and memberships.name = "Compute") '
        'order by rack,rank' )
      self.db.execute(query)
      for name, cpus in self.db.fetchall():
        # Print the queue manager commands.
        # self.addText("%s -c \"delete node %s\" 2> /dev/null\n" % (qmgr, name))
        self.addText("%s -c \"create node %s np=%d,ntype=cluster\" 2> /dev/null\n"
        % (qmgr, name, cpus))
      
      # allow job submit from login appliances
      query=('select nodes.name from nodes, memberships '
        'where (nodes.membership = memberships.id '
        'and memberships.name = "Login") '
        'order by rack,rank' )
      self.db.execute(query)
      for (name,) in self.db.fetchall():
        # Print the queue manager commands.
        self.addText("%s -c \"set server submit_hosts-= %s\" 2> /dev/null\n" % (qmgr, name))
        self.addText("%s -c \"set server submit_hosts+= %s\" 2> /dev/null\n" % (qmgr, name))

        

RollName = "torque"
