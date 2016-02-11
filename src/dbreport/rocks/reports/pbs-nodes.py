#
# $RCSfile: pbs-nodes.py,v $
#
# Generates a series of PBS qmgr commands that add nodes
# to the pbs server database.
#
# This script must have access to the MySQL server on a Rocks Frontend node.
#
# @Copyright@
# 
# 				Rocks
# 		         www.rocksclusters.org
# 		        version 4.2.1 (Cydonia)
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
# 	"This product includes software developed by the Rocks 
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
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
# $Log: pbs-nodes.py,v $
# Revision 1.7  2006/09/11 22:49:59  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:11:43  mjk
# 4.2 copyright
#
# Revision 1.5  2005/10/28 10:25:11  royd
# Changed domain queries frm self.domain to self.getGlobalVar
#
# Revision 1.4  2005/10/12 18:10:35  mjk
# final copyright for 4.1
#
# Revision 1.3  2005/09/16 01:04:14  mjk
# updated copyright
#
# Revision 1.2  2005/05/24 21:23:31  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2003/10/29 20:35:51  mjk
# moved dbreport into roll
#
# Revision 1.11  2003/08/15 22:34:46  mjk
# 3.0.0 copyright
#
# Revision 1.10  2003/07/16 19:44:45  fds
# Reporting fully-qualified domain names in all cases.
#
# Revision 1.9  2003/05/22 16:39:27  mjk
# copyright
#
# Revision 1.8  2003/02/17 18:43:04  bruno
# updated copyright to 2003
#
# Revision 1.7  2002/12/18 21:01:38  fds
# Correctly tests for first arg now.
#
# Revision 1.6  2002/10/18 21:33:26  mjk
# Rocks 2.3 Copyright
#
# Revision 1.5  2002/10/11 19:54:44  bruno
# fixes for pbs report
#
# Revision 1.4  2002/10/10 22:29:57  bruno
# little tweaks
#
# Revision 1.3  2002/10/09 16:57:49  fds
# Simpler select that does more.
#
# Revision 1.2  2002/10/04 22:33:40  fds
# Better failure mode.
#
# Revision 1.1  2002/10/04 20:04:51  fds
# Original design of report for creating PBS server database.
#

import sys
import os
import rocks.reports.base

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


class Report(rocks.reports.base.ReportBase):
      
   def run(self):
      # Bail out if the user says we shouldn't touch the nodelist.
      if not UPDATE_NODE_LIST:
         return
      try:
         qmgr = self.args[0]
      except IndexError:
         qmgr = "qmgr"

      dn = self.getGlobalVar("Kickstart","PrivateDNSDomain")

      # Query the database for compute node info by doing a killer join.
      # Thanks Bruno!
      query=('select nodes.name, nodes.cpus from nodes, memberships '
        'where (nodes.membership = memberships.id '
        'and memberships.compute = "yes") '
        'order by rack,rank' )
      self.execute(query)
      for name, cpus in self.fetchall():
         # Print the queue manager commands.
         print "%s -c \"delete node %s\" 2> /dev/null" % (qmgr, name)
         print "%s -c \"create node %s np=%d,ntype=cluster\" 2> /dev/null" \
            % (qmgr, name, cpus)

