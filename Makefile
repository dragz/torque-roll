#
# $Id: Makefile,v 1.9 2006/09/11 22:49:57 mjk Exp $
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
# Revision 1.9  2006/09/11 22:49:57  mjk
# monkey face copyright
#
# Revision 1.8  2006/08/10 00:11:42  mjk
# 4.2 copyright
#
# Revision 1.7  2005/10/12 18:10:34  mjk
# final copyright for 4.1
#
# Revision 1.6  2005/09/16 01:04:13  mjk
# updated copyright
#
# Revision 1.5  2005/06/13 10:41:25  royd
# Added xmllint to rule out the most obvious xml mistakes.
#
# Revision 1.4  2005/05/24 21:23:29  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2004/11/25 19:46:37  royd
# Turn off compat libs build.
#
# Revision 1.2  2004/07/02 23:31:42  fds
# PBS roll now made with x86 compat libs for opteron.
#
# Revision 1.1  2003/10/29 18:15:26  mjk
# start pbs roll
#
# Revision 1.1  2003/09/11 21:07:50  mjk
# started sge roll
#


# Make the x86 compat libs for opteron.
MAKE.compat = 0

ROLLSROOT = ..
-include $(ROLLSROOT)/etc/Rolls.mk
include Rolls.mk

default: roll

xmllint:
	xmllint $(wildcard nodes/*.xml graphs/*.xml) > /dev/null

buildsetup:
	yum --enablerepo base,updates install readline-devel pam-devel tclx-devel python-docutils

