# --------------------------------------------------- -*- Makefile -*- --
# $Id: Makefile,v 1.9 2006/09/11 22:50:02 mjk Exp $
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
# Revision 1.9  2006/09/11 22:50:02  mjk
# monkey face copyright
#
# Revision 1.8  2006/09/06 13:39:34  royd
# Fixes for 2.1.2 which has a new build system
#
# Revision 1.7  2006/08/10 00:11:45  mjk
# 4.2 copyright
#
# Revision 1.6  2005/10/27 11:12:05  royd
# Changes needed for 2.0.0p0
#
# Revision 1.5  2005/10/12 18:10:39  mjk
# final copyright for 4.1
#
# Revision 1.4  2005/09/16 01:04:17  mjk
# updated copyright
#
# Revision 1.3  2005/05/24 21:23:34  mjk
# update copyright, release is not any closer
#
# Revision 1.2  2004/04/14 11:39:24  royd
# Updates for 1.0.1p6.
#
# Revision 1.1  2004/01/27 20:07:50  royd
# Changes to use torque instead of storm.
#
# Revision 1.1  2004/01/19 14:21:07  royd
# Changes for storm setup.
#
# Revision 1.1  2004/01/15 21:04:03  royd
# Initial checkin for SPBS
#
# Revision 1.3  2003/02/05 22:16:52  bruno
# added in patch to mom to recognize machines with greater than 1GB of memory
#
# Revision 1.2  2003/01/24 19:33:59  bruno
# added more info to info section of spec file
#
# Revision 1.1  2002/12/19 15:01:48  bruno
# initial release
#
#

PKGROOT = 
ROCKSROOT = ../../../../..
REDHAT.ROOT = $(PWD)/../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

include version.mk

BASENAME = torque-$(VERSION)
TARBALL = $(BASENAME).tar.gz

default: rpm

pretar:: patch
	cp $(BASENAME).tar.gz $(REDHAT.SOURCES)/$(TARBALL)


patch:
#	tar zxf $(TARBALL) 
#	mv $(BASENAME) $(BASENAME).orig
#	tar zxf $(TARBALL) 
#	cd patch-files/$(BASENAME) && \
#		find . -type f | grep -v CVS | cpio -pduv ../../$(BASENAME)
#	-diff -uNr $(BASENAME).orig $(BASENAME) > $(BASENAME).patch
#	cp $(BASENAME).patch $(REDHAT.SOURCES)


clean::
	rm -rf $(BASENAME) $(BASENAME).orig $(BASENAME).patch 

