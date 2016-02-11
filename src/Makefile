# $Id: Makefile,v 1.15 2006/09/11 22:49:57 mjk Exp $
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
# $Log: Makefile,v $
# Revision 1.15  2006/09/11 22:49:57  mjk
# monkey face copyright
#
# Revision 1.14  2006/09/06 13:23:58  royd
# Added pbstools.
#
# Revision 1.13  2006/08/10 00:11:43  mjk
# 4.2 copyright
#
# Revision 1.12  2005/10/12 18:10:35  mjk
# final copyright for 4.1
#
# Revision 1.11  2005/09/16 01:04:13  mjk
# updated copyright
#
# Revision 1.10  2005/06/10 11:40:37  royd
# Added insert-ethers plugin
#
# Revision 1.9  2005/06/07 11:26:50  royd
# Added pbs_python to the build structure.
#
# Revision 1.6  2004/04/14 09:22:57  royd
# Mods needed for 3.2.6p6-snap.1079990700.
#
# Revision 1.5  2004/01/28 22:43:31  royd
# added mpiexec to the list of dirs.
#
# Revision 1.4  2004/01/27 20:07:49  royd
# Changes to use torque instead of storm.
#
# Revision 1.3  2004/01/19 14:21:06  royd
# Changes for storm setup.
#
# Revision 1.2  2004/01/15 22:07:42  royd
# Drop the build of openpbs
#
# Revision 1.1  2003/10/29 18:15:27  mjk
# start pbs roll
#
# Revision 1.1  2003/09/15 22:43:56  mjk
# *** empty log message ***
#
# Revision 1.2  2003/08/27 23:10:55  mjk
# - copyright update
# - rocks-dist uses getArch() fix the i686 distro bug
# - ganglia-python spec file fixes (bad service start code)
# - found some 80col issues while reading code
# - WAN ks support starting
#
# Revision 1.1  2003/07/30 22:24:25  mjk
# *** empty log message ***
#



SRCDIRS = dbreport insert-ethers usersguide torque pbs_python ganglia pbstools rocks-command torque-openmpi

default:	rpm

copyright rpm clean::
	for i in $(SRCDIRS) ; do \
		(cd $$i ; make $@ ) ; \
	done
