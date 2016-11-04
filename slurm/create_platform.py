from math import *
import sys

#Total number of hosts we want to simulate
num_host = 10

if len(sys.argv) > 1:
        num_host = int(sys.argv[1])

# The name of the plateform file
plat_file   = "gen_platform.xml"

deploy_file = "gen_deploy.xml"

conf_file   = "slurm.conf"


CMAKE_BINARY_DIR = "/home/root/simunix"
SLURM_INST = "/opt/slurm-16.05.4"
CMAKE_SOURCE_DIR = "/home/root/simunix"
workload = CMAKE_SOURCE_DIR+"/slurm/trace_sinfo.swf"

#### //end of config

simunix = CMAKE_BINARY_DIR+"/bin/simunix"
slurmctld = "slurmctld"
slurmd = "slurmd"
launcher = CMAKE_SOURCE_DIR+"/slurm/launcher"
conf_template = "slurm.conf.template"

hosts_id = range(0, num_host)

def host2IP(i):
    return "10.0."+str(int(i/255))+"."+str(i % 255)


def coordCircle(i):
    r = 1000.0
    a = 2.0*pi*float(i)/float(num_host)
    return "0 "+str(r*cos(a))+" "+str(r*sin(a))


header ="""<?xml version='1.0'?>
<!DOCTYPE platform SYSTEM "http://simgrid.gforge.inria.fr/simgrid/simgrid.dtd">
<platform version="4">
  <AS  id="AS0"  routing="Full">
    <host id="localhost" core="4" speed="8095000000f">
      <prop id="ip" value="127.0.0.1"/>
    </host>
  """

hosts = "".join(["""
    <host id="host"""+str(i)+"""" core="4" speed="8095000000f">
      <prop id="ip" value=\""""+host2IP(i)+"""\"/>
    </host>""" for i in hosts_id])

all_hosts = ["host"+str(i) for i in hosts_id]+["localhost"]


def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

routes = """
    <link id="link1" bandwidth="125000000Bps" latency="0.000100ms"/>"""
for (i,j) in combinations(all_hosts,2):
        if i != j:
            routes += """
<route src=\""""+i+"""\" dst=\""""+j+"""\"><link_ctn id="link1"/></route>"""


footer = """
  </AS>
</platform>
"""

#Write the final platform xml file
with open(plat_file, "w") as fp:
    fp.write(header)
    fp.write(hosts)
    fp.write(routes)
    fp.write(footer)
    fp.close()

header = """<?xml version='1.0'?>
<!DOCTYPE platform SYSTEM "http://simgrid.gforge.inria.fr/simgrid/simgrid.dtd">
<platform version="4">"""

localhost = """
  <process host="localhost" function="localhost_slurmctld">
     <argument value=\""""+simunix+"""\"/>
     <argument value=\""""+slurmctld+"""\"/>
     <argument value="-D"/>
     <argument value="-c"/>
  </process>
  <process host="localhost" function="localhost_launcher" start_time="300">
     <argument value=\""""+simunix+"""\"/>
     <argument value="/home/root/slurm/launcher.sh"/>
  </process>
"""

hosts="".join(["""
  <process host="host"""+str(i)+"""" function="slurmd_dummy"""+str(i)+"""">
     <argument value=\""""+simunix+"""\"/>
     <argument value=\""""+slurmd+"""\"/>
     <argument value="-D"/>
     <argument value="-N"/>
     <argument value="dummy"""+str(i)+""""/>
  </process>
""" for i in hosts_id])

footer = """
</platform>
"""

#Write the deployement file.
with open(deploy_file, "w") as fp:
    fp.write(header)
    fp.write( localhost)
    fp.write( hosts)
    fp.write( footer)
    fp.close()


with open(conf_template, "r") as fd:
    template = fd.read()
fd.close()

if num_host > 1:
    partition_template = """NodeName={nodename} Sockets=1 CoresPerSocket=1 ThreadsPerCore=1 NodeAddr={hosts} Port={ports}
PartitionName=debug Nodes={nodes} Default=YES MaxTime=INFINITE State=UP"""

    range_str  = "[" + str(0) + "-" + str(num_host - 1) + "]" 
    node_names = "dummy" + range_str
    node_addr  = "host" + range_str
    nodes_str  = node_names

    port_min = 6820
    port_range = "[" + str(6820) + "-" + str( 6820 + (num_host - 1)) + "]" 

    partition = partition_template.format(nodename = node_names, hosts = node_addr, nodes= nodes_str, ports= port_range)

else:
    partition = """NodeName=dummy1 Sockets=1 CoresPerSocket=1 ThreadsPerCore=1 NodeAddr=peer Port=6821
PartitionName=debug Nodes=dummy1 Default=YES MaxTime=INFINITE State=UP"""

conf = template.format(partition = partition)

with open(conf_file, "w") as fd:
    fd.write(conf)
fd.close()