# $Id: Makefile,v 1.5 2006/09/11 22:50:01 mjk Exp $
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
# Revision 1.5  2006/09/11 22:50:01  mjk
# monkey face copyright
#
# Revision 1.4  2006/08/10 00:11:45  mjk
# 4.2 copyright
#
# Revision 1.3  2005/10/12 18:10:39  mjk
# final copyright for 4.1
#
# Revision 1.2  2005/09/16 01:04:16  mjk
# updated copyright
#
# Revision 1.1  2005/06/07 11:26:04  royd
# Initial inclusion of pbs_python.
#
# Revision 1.2  2004/12/02 01:00:32  nadya
# update targets so can build a fake roll without a tarball
#
# Revision 1.1  2004/12/01 01:31:56  nadya
# baseline
#
#

PKGROOT = /opt/@template@

REDHAT.ROOT = $(PWD)/../../
ROCKSROOT = ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

SEDSPEC += \
	-e 's%@ROOT@%$(ROOT)%g' \
	-e 's%@PKGROOT@%$(PKGROOT)%g' 

include version.mk

BASENAME = $(NAME)-$(VERSION)
TARBALL = $(BASENAME).tar.gz

$(REDHAT.SOURCES)/$(TARBALL):
	/bin/true

$(REDHAT.SOURCES)/$(TARBALL.GZ): $(REDHAT.SOURCES)/$(TARBALL)
	/bin/true

pretar:: patch
	cp $(BASENAME).tar.gz $(REDHAT.SOURCES)/$(TARBALL)

patch:
	echo "No patches needed"

clean::
	rm -rf $(NAME)-$(VERSION)
