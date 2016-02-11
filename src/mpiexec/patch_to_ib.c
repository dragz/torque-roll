--- trunk/ib.c	2006/11/29 15:22:26	395
+++ trunk/ib.c	2007/05/29 19:24:57	404
@@ -30,6 +30,7 @@
 static int address_size = 0;
 static char *pids = 0;
 static int pids_size = 0;
+static int phase = 0;  /* for two-phase version 5 */
 
 /* state of all the sockets */
 static int num_waiting_to_accept;  /* first accept all numtasks */
@@ -150,6 +151,24 @@
  *   Same as 2 with addition of pid array.  We send back the
  *   entire array of pids (unpersonalized) after the addresses array.
  *
+ * Version 5:
+ *   Added another phase, with socket close/reaccept between the two.  This
+ *   could be very bad for scalability, but is necessary to support multiple
+ *   NICs per node, and multiple network paths, according to OSU.
+ *   First phase distributes hostids:
+ *     version   # 5
+ *     rank      # 0..np-1
+ *     hostidlen # 4 bytes
+ *     hostid    # <hostidlen> bytes
+ *   Write back entire hostid[] array.
+ *   Close fds, go to phase 2.  At each accept, gather:
+ *     rank      # 0..np-1
+ *     addrlen   # 4 bytes, could be 0
+ *     addrs[]   # <addrlen> bytes
+ *     pidlen    # 4 bytes
+ *     pids[]    # <pidlen> bytes
+ *   Write back personalized out_addrs[] and full pids[].
+ *
  * Return negative on error, or new rank number for success.
  */
 static int read_ib_one(int fd)
@@ -159,8 +178,13 @@
     int j, ret = -1;
     pid_t pidlen;
 
-    if (read_full_ret(fd, &testvers, sizeof(int)) != sizeof(int))
-	goto out;
+    if (version == 5 && phase == 1) {
+	/* no version again on second phase */
+	testvers = version;
+    } else {
+	if (read_full_ret(fd, &testvers, sizeof(int)) != sizeof(int))
+	    goto out;
+    }
     if (read_full_ret(fd, &rank, sizeof(int)) != sizeof(int))
 	goto out;
     if (read_full_ret(fd, &addrlen, sizeof(int)) != sizeof(int))
@@ -194,11 +218,11 @@
 
     if (version == -1) {
 	version = testvers;
-	if (!(version == 1 || version == 2 || version == 3)) {
+	if (!(version == 1 || version == 2 || version == 3 || version == 5)) {
 	    warning(
 	      "%s: protocol version %d not known, but might still work",
 	      __func__, version);
-	    version = 3;  /* guess the latest still works */
+	    version = 5;  /* guess the latest still works */
 	}
 	debug(1, "%s: version %d startup%s", __func__, version,
 	  non_versioned_092 ? " (unversioned)" : "");
@@ -238,7 +262,7 @@
 	    goto out;
     }
 
-    if (version >= 3) {
+    if (version == 3 || (version == 5 && phase == 1)) {
 	read_full(fd, &pidlen, sizeof(pidlen));
 	if (!pids) {
 	    pids_size = pidlen;
@@ -291,6 +315,7 @@
     int numleft;
     int ret = 0;
 
+next_phase:
     debug(1, "%s: waiting for checkin: %d to accept, %d to read", __func__,
       num_waiting_to_accept, num_waiting_to_read);
 
@@ -309,17 +334,6 @@
     }
 
     /*
-     * Put listen socket back in blocking, and give it to the stdio listener.
-     */
-    flags = fcntl(mport_fd, F_GETFL);
-    if (flags < 0)
-	error_errno("%s: get socket flags", __func__);
-    if (fcntl(mport_fd, F_SETFL, flags & ~O_NONBLOCK) < 0)
-	error_errno("%s: set listen socket blocking", __func__);
-    close(mport_fd);
-    stdio_msg_parent_say_abort_fd(0);
-
-    /*
      * Now send the information back to all of them.
      */
     if (version == 1) {
@@ -352,10 +366,70 @@
 	    }
 	    free(pids);
 	}
+    } else if (version == 5) {
+	if (phase == 0) {
+	    /* These are actually the hostids, in mvapich parlance.  Next
+	     * phase will be the personalized addresses. */
+	    for (i=0; i<numtasks; i++) {
+		if (write_full(fds[i], address, numtasks * address_size) < 0)
+		    error_errno("%s: write addresses to rank %d", __func__, i);
+	    }
+	    phase = 1;
+	    for (i=0; i<numtasks; i++) {
+		close(fds[i]);
+		fds[i] = -1;
+	    }
+	    address_size = 0;
+	    free(address);
+	    address = NULL;
+	    num_waiting_to_accept = numtasks;
+	    goto next_phase;
+	} else if (phase == 1) {
+	    /*
+	     * Very similar to version 3, but with -1 for i == j in
+	     * outaddrs.  Not sure if that matters.
+	     */
+	    int outsize = 3 * numtasks * sizeof(int);
+	    int *outaddrs = Malloc(outsize);
+	    int *inaddrs = (int *) (unsigned long) address;
+	    int inaddrs_size = address_size / sizeof(int);
+	    /* fill in the common information first: lids, hostids */
+	    for (i=0; i<numtasks; i++)
+		outaddrs[i] = inaddrs[i*inaddrs_size + i];
+	    for (i=0; i<numtasks; i++)
+		outaddrs[2*numtasks+i] = inaddrs[i*inaddrs_size + numtasks];
+	    /* personalize the array with qp info for each */
+	    for (i=0; i<numtasks; i++) {
+		for (j=0; j<numtasks; j++)
+		    outaddrs[numtasks+j] = inaddrs[j*inaddrs_size + i];
+		outaddrs[numtasks + i] = -1;
+		if (write_full(fds[i], outaddrs, outsize) < 0)
+		    error_errno("%s: write addresses to rank %d", __func__, i);
+	    }
+	    free(outaddrs);
+	    for (i=0; i<numtasks; i++) {
+		if (write_full(fds[i], pids, pids_size * numtasks) < 0)
+		    error_errno("%s: write pids to rank %d", __func__, i);
+	    }
+	    free(pids);
+	} else
+	    error("%s: programmer error, unknown version 5 phase %d", __func__,
+		  phase);
     } else
 	error("%s: programmer error, unknown version %d", __func__, version);
 
     /*
+     * Put listen socket back in blocking, and give it to the stdio listener.
+     */
+    flags = fcntl(mport_fd, F_GETFL);
+    if (flags < 0)
+	error_errno("%s: get socket flags", __func__);
+    if (fcntl(mport_fd, F_SETFL, flags & ~O_NONBLOCK) < 0)
+	error_errno("%s: set listen socket blocking", __func__);
+    close(mport_fd);
+    stdio_msg_parent_say_abort_fd(0);
+
+    /*
      * Finally, implement a simple barrier.  Use a select loop to avoid
      * hanging on a sequential read from #0 which is always quite busy and
      * slow to respond.
