ROLL	= torque
NAME    = roll-$(ROLL)-usersguide
RELEASE = 0

SUMMARY_COMPATIBLE      = $(VERSION)
SUMMARY_MAINTAINER      = University of Tromso
SUMMARY_ARCHITECTURE    = i386, x86_64, ia64

ROLL_REQUIRES           = base hpc kernel os1 os2 os3 os4
ROLL_CONFLICTS          = sge

