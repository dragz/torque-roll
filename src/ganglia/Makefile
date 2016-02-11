# $Id: Makefile,v 1.7 2006/09/11 22:49:59 mjk Exp $
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
# Revision 1.7  2006/09/11 22:49:59  mjk
# monkey face copyright
#
# Revision 1.6  2006/08/10 00:11:44  mjk
# 4.2 copyright
#
# Revision 1.5  2005/10/12 18:10:37  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:04:14  mjk
# updated copyright
#
# Revision 1.3  2005/08/31 19:49:58  bruno
# moved to the foundation
#
# included fix from Emir Imamagic
#
# Revision 1.2  2005/05/24 21:23:32  mjk
# update copyright, release is not any closer
#
# Revision 1.1  2004/02/18 19:46:51  fds
# Added Ganglia Monitoring of PBS.
#
#


PKGROOT = /opt/ganglia
METRICS = $(wildcard metrics/*.py)
GANGLIA_CONFIGS = $(wildcard metrics/*.pyconf)
REDHAT.ROOT = $(PWD)/../../

ROCKSROOT = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

-include $(ROCKSROOT)/etc/python.mk
include python.mk

install:: $(SCRIPTS)
	mkdir -p $(ROOT)/$(PKGROOT)/$(LIBARCH)/ganglia/python_modules/
	install -ma+r $(METRICS) $(ROOT)/$(PKGROOT)/$(LIBARCH)/ganglia/python_modules/
	mkdir -p $(ROOT)/$(PKGROOT)/etc/conf.d/
	install -ma+r $(GANGLIA_CONFIGS) $(ROOT)/$(PKGROOT)/etc/conf.d/

clean::
	rm -f $(SCRIPTS)

