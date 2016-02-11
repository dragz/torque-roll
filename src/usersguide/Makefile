# 
# $Id: Makefile,v 1.13 2006/09/21 04:16:15 mjk Exp $
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
# Revision 1.13  2006/09/21 04:16:15  mjk
# *** empty log message ***
#
# Revision 1.12  2006/09/21 04:15:39  mjk
# PBS docs work with 4.2.1
#
# Revision 1.11  2006/09/11 22:50:02  mjk
# monkey face copyright
#
# Revision 1.10  2006/08/10 00:11:46  mjk
# 4.2 copyright
#
# Revision 1.9  2005/10/12 18:10:40  mjk
# final copyright for 4.1
#
# Revision 1.8  2005/09/16 01:04:17  mjk
# updated copyright
#
# Revision 1.7  2005/06/07 11:49:31  royd
# Removed the build of the pdf manual because of some bug that makes jw crash.
#
# Revision 1.6  2005/05/24 21:23:35  mjk
# update copyright, release is not any closer
#
# Revision 1.5  2005/04/05 22:09:13  nadya
# move logic of creating rocks.dsl, rocks.css and stylesheet-images to Rules.mk
# Add target predoc in order to make docs in a local directory
#
# Revision 1.4  2004/02/12 00:04:54  nadya
# add png files
#
# Revision 1.3  2004/02/03 01:22:59  nadya
# add css file
# rename ldp.dsl as rocks.dsl
#
# Revision 1.2  2003/10/29 23:13:17  mjk
# roll builds
#
# Revision 1.1  2003/10/29 19:08:06  mjk
# started docs
#
# Revision 1.1  2003/09/16 20:51:18  mjk
# manual
#


PKGROOT		= /var/www/html/roll-documentation/torque/$(VERSION)
REDHAT.ROOT	= $(PWD)/../../
ROCKSROOT	= ../../../../..
-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk


default: $(NAME).spec ../$(NAME)-$(VERSION).tar.gz

html: 
	rst2html -g --time --stylesheet voidspace.css torque-roll-userguide.rst > torque-roll-userguide.html

build: html

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)
	install -ma+r torque-roll-userguide.html $(ROOT)/$(PKGROOT)/torque-roll-userguide.html
	install -ma+r runscript.sh $(ROOT)/$(PKGROOT)/runscript.sh

clean::
	rm -f *.html
	rm -f index.pdf


