#!/opt/rocks/bin/python
#
# A metric for gmond that publishes some PBS
# (Batch job launcher) metrics through Ganglia.
# For use with Rocks Clusters. 
#
# Output is similar to showq, with one metric per job
# in the queue.
#

# this implementation make use of the same trick as ps.py since
# the number of metrics is not known at initialization.

import os, sys, time
#sys.path.append('/opt/rocks/lib/python2.4/site-packages')
import gmon.Process
# Our MPD-style name list encoder.
import gmon.encoder
# Why is this neccessary???
#sys.path.append('/opt/rocks/lib/python2.4/site-packages/pbs')
from PBSQuery import PBSQuery

def pbs_handler(name):
    pbs = PBSQuery()
    jobs = pbs.getjobs()
    for jobid, jobinfo in jobs.iteritems():
        publish(jobid, jobinfo)
    publish_queue_state(pbs)
    return ""

encoder = gmon.encoder.Encoder("compute-%d-%d")
def compress_nodelist(nodes):
    global encoder
    hostlist = list()
    for n in nodes.split('+'):
        h, _ = n.split('/')
        hostlist.append(h)
    return encoder.encode(hostlist)

def remaining_time(total,used):
    th,tm,ts = map(int,total.split(":"))
    uh,um,us = map(int,used.split(":"))
    rt = (th*3600+tm*60+ts)-(uh*3600+um*60+us)
    rh, rest = divmod(rt,3600)
    rm, rs = divmod(rest,60)
        
    
def compute_cpus(nodes):
    """Compute the number of cpus from a nodes specification."""
    
    cpus = 0
    for n in nodes.split("+"):
        c = 1
        for m in n.split(":"):
            if m.isdigit():
                c *= int(m)
            if m.startswith("ppn="):
                _, ppn = m.split("=",1)
                c *= int(ppn)
        cpus += c
    return cpus

state = { 'R': 'Running', 'Q': 'Queue Wait',
        'E': 'Exiting', 'H': 'Held', 'T': 'Transfering',
        'W': 'Waiting', 'C' : 'Completed', 'S' : 'Suspended'}

def publish(jobid, jobinfo):


    jobinfo['user'] = jobinfo['Job_Owner'][0].split("@")[0]
    if jobinfo.has_key('Resource_List.nodes'):
        jobinfo['procs'] = compute_cpus(jobinfo['Resource_List.nodes'][0])
    else:
        jobinfo['procs'] = 1
    jobinfo['state'] = state[jobinfo['job_state'][0]]
    name = "queue-job-%s" % jobid.split('.')[0]
    val = "user=%(user)s, P=%(procs)s, state=%(state)s" % jobinfo
    
    if jobinfo['job_state'][0] in ["R", "E", "C"]:
        #rt = remaining_time(info.walltime,info.used_time)
        val = val + ", started=%s, name=%s, nodes=%s" % \
            (jobinfo['start_time'][0], jobinfo['Job_Name'][0], compress_nodelist(jobinfo['exec_host'][0]))
    else:
        val = val + ", started=%s"%(jobinfo['qtime'][0])
    #print name,  val
    os.system("/opt/ganglia/bin/gmetric -d 300 -n %s -v '%s' -t string "%(name, val)) 

def publish_queue_state(p):
    nodes = p.getnodes()
    ncpus = 0
    for n, info in nodes.iteritems():
        if info['state'] != 'down':
            ncpus += int(info['np'][0])
    
    os.system("/opt/ganglia/bin/gmetric -d 300 -n 'queue-state' -v 'P=%s' -t string "%(ncpus)) 
    

def metric_init(params):
  global descriptors
  descriptors = list()
  d = {
      'name': 'pbsinfo',
      'call_back': pbs_handler,
      'time_max': 60,
      'value_type': 'string',
      'units': '',
      'slope': 'zero',
      'format': '%s',
      'description': 'PBS Jobs',
      'groups': 'pbs'
      }

  descriptors.append(d)

  return descriptors

def metric_cleanup():
  '''Clean up the metric module.'''
  pass



if __name__ == "__main__":
  metric_init(None)
  for d in descriptors:
    v = d['call_back'](d['name'])
    print 'value for %s is %s' % (d['name'],  v)
