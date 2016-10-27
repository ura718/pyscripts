#!/usr/bin/python

#
# Author: Yuri Medvinsky
#
# requires python-netaddr.noarch  
# requires python-paramiko.noarch
#


import paramiko
import re
from netaddr import *
#from operator import itemgetter









# define SSH() subroutine
def SSH(server):

# IP Array, declare and empty out on every call
   ifcfgout = []


# SSHClient is high level representation of a session with ssh server
   ssh = paramiko.SSHClient()


# Accept known_host key upon login
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# Open ssh connection and authenticate
   myconn = ssh.connect(server, username='root', key_filename='/root/.ssh/id_rsa')


# stdin, stdout, stderr are part of paramiko module. Creates a session.
   stdin, stdout, stderr = ssh.exec_command('ifconfig -a|grep inet | grep -v \'127.0.0.1\' ')

   for line in stdout.readlines():
     #print line,
     ifcfgout.append(line)

  


# close ssh connection
   ssh.close()


   return ifcfgout





# Create empty iplist array
iplist = []

# Read from 'list' file
myfile = open("list")
for host in myfile.readlines():
  # get rid of newline and empty spaces in the end
  host = host.strip()


    
  # call SSH() subroutine
  try:
    ifcfgout = SSH(host)
    iplist = iplist + ifcfgout


  # The script will proceed to next server if this one is down
  except Exception as err:
    print "Error host %s: %s" % (host,str(err))






# Create empty Netlist to store ip/network as dict
Netlist = {}

# Get ip and mask
for line in iplist:
  line = line.strip()
  

  # Find 'addr:<ip>' address
  ipaddr = re.findall("addr:\d+\.\d+\.\d+\.\d+", line)
  if ipaddr:
    # split ipaddr[0] list by colon. The ipaddr[0] is because its first element and only element in list
    ipaddr =  ipaddr[0].split(':')[1]



  # Find 'Mask:<ip>' address
  mask = re.findall("Mask:\d+\.\d+\.\d+\.\d+", line)
  if mask:
    # Get NetMask
    netmask = mask[0].split(':')[1]


  # Assign key, value for ip and network
  Netlist[ipaddr] = netmask





# Print Network / IP
for key in sorted(Netlist.iterkeys()):
  print str((IPNetwork("%s/%s" % (key,Netlist[key])).cidr)), key



