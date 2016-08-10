#!/usr/bin/python

import subprocess
import re
import time
import socket

#
# Author: Yuri Medvinsky
# Date: 08-09-2016
# Info: 
#  The script will collect netstat output and identify unique ip addresses that have a large connection count.
#  It will then proceed to block the offending ip through firewall rules and ipset. The ipset and firewall rules
#  work together in conjunction to the netfilter. The script will check and see if a 'blacklist' bucket list 
#  already exists within ipset list. If it does not exist then the script will create one. After the script creates
#  the bucket list it will then check iptables firewall rules to see if there is a rule referencing that bucket list
#  if the rules does not exist it will also create one. Then it will populate the offending ip address with a timeout
#  of 5 minutes into the bucket list. This is used to control and stop spammy ip addresses that hit the servers going
#  into various ports. This damage is usually done by bots or offending scripts that scrape the http web pages.
#






##############################################################
#
def GETNET():

  # Takes output from netstat command and identifies all ip addresses and their count
  # that are connected to port 443 and are not in LISTEN or ESTABLSISHED mode



  netout = subprocess.Popen(['netstat', '-tuna'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
  netout,netouterror = netout.communicate()
 



  """
  Filter out LISTEN and ESTABLISHED and only get :443 port
  Then you split the line and only extract column 4 which is ip:port 
  Split up the output by ':' and take the first element and append it to array 'ip'
  """

  ip = []
  for line in netout.split('\n'):
    # Get only lines matching port 443 and discard LISTEN, ESTABLISHED and everything else
    if ('LISTEN' not in line) and ('ESTABLISHED' not in line) and (':443' in line):
        port443 = line.split()[4]
        ip.append(port443.split(':')[0])





  # Sort the ip addresses inside the array
  ip = sorted(ip)




  """
  Create hash and populate it with data
  If ip address is found then we increment a value by 1. (Stating it already occurred more than once)
  If ip address is not found then we assign value of 1. (Stating it occured at least once)
  """

  ipcount = {}
  for i in ip:
    if ipcount.has_key(i):	
      ipcount[i] += 1		# if ipcount has key with ip address then increment it by 1
    else:
      ipcount[i] = 1		# if ipcount does not have key with ip address then assign 1
 

 

  # Return IP's and count 
  return ipcount












##############################################################
#
def IPSETCreateLIST():
  # Create a blacklist bucket that will hold ip addresses that need to be blocked
  # The ipset works with iptables firewall rules




  # Execute Shell ipset list
  ipsetlist = subprocess.Popen(['ipset', 'list'],
    stdout = subprocess.PIPE,
    stderr = subprocess.STDOUT)
  ipsetlist, ipsetlisterror = ipsetlist.communicate() 
 



 
  # If ipsetlist is empty then create blacklist that will hold spammy/bad IP's... 
  if ipsetlist:
    for i in ipsetlist.split('\n'):
      if 'Name' in i:
        print "ipset list exists: " 
        print "  %s " % i

  else:
    # Execute Shell `ipset create blacklist hash:ip`
    blacklist = subprocess.Popen(['ipset', 'create', 'blacklist', 'hash:ip', 'timeout', '300'],
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT)
    blacklist, blacklisterror = blacklist.communicate()









##############################################################
#
def IPTABLEScheck():
  # Check to see if the iptables rule exists that references the ipset bucket list 'blacklist'
  # If it does not find the rule then it will create one.


  Rules = subprocess.Popen(['iptables', '-L', '-n'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
  Rules, Ruleserror = Rules.communicate()


  flag=0
  for line in Rules.split('\n'):
    if not 'blacklist' in line:
      flag=0
      #print "no blacklist found in iptables"
    else:
      #print "blacklist found in iptables"
      flag=1
      break


  if flag == 0:
    try:

      print "[+] Adding blacklist iptables rule to INPUT Chain "

      AddRule = subprocess.Popen(['iptables', '-I', 'INPUT', '-m', 'set', '--match-set', 'blacklist', 'src', '-p', 'TCP', '-m', 'multiport', '--dport', '80,443', '-j', 'DROP'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
      AddRule, AddRuleerror = AddRule.communicate()

    except:
      print "Error adding iptables rule"
  








##############################################################
#
def IPSETAddToList(key, value):	
  # This is called from the loop in the main body and will run as many times as loop permits
  # Check if the ip address that you want to add to the ipset bucket list already exists
  # If ip address exists then do nothing. Otherwise add the rule with a 5 minute timeout


  # Assign key that holds ip to be blocked
  blockip = key
  count = value


  # check to see if ip address already exists
  CheckList = subprocess.Popen(['ipset', 'list'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
  CheckList,CheckListerror = CheckList.communicate()







  # Do ipset list and find out if ip address is already blocked. If its blocked then do nothing,
  # otherwise add it to the blacklist to block it.


  flag=0
  for ip in CheckList.split('\n'): 
    try:
     
      # Extract only ip address from string
      BlockedIpFound = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip).group()

      
      if BlockedIpFound == blockip:
        # indicates ip address is already blocked
        flag=1
        break
      else:
        flag=0 

    except:
      pass





 
  # The flag=0 indicates a blockip address was not found in blacklist bucket
  # therefore we want to add it so its blocked.

  if flag == 0:

    # Add rule to block ip
    try:
      AddIpToBlackList = subprocess.Popen(['ipset', 'add', 'blacklist', blockip, 'timeout', '300'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
      AddIpToBlackList, AddIpToBlackListerror = AddIpToBlackList.communicate() 


    except: 
      raise



    # Create a log to keep track of what ip addresses got blocked
    HOSTNAME = socket.gethostname()
    DATE = time.strftime("%b  %d %H:%M:%S")
    F_LOG ='/var/log/iptables.log'

    try:
      with open(F_LOG,'a') as f:
        f.write('\n%s  %s: ipset: blocked %s count: %s ' % (DATE, HOSTNAME, blockip, count)) 
      f.close()
    except:
      raise





#------------x->   MAIN   <-x--------------#




  

# Main Program Body
def main():



  # Return IP's and Count
  ipcount = GETNET()


  # Create a blacklist bucket for iptables that will hold blocked ip addresses
  IPSETCreateLIST()		




  # Check if firewall rule exists  
  IPTABLEScheck()




  """
  Print all ip addresses whos count is more than 10
  value equals count
  key equals ip
  """

  for key,value in ipcount.iteritems():
    if value > 300:
      #print value, key 

      # Add bad ip address to list
      IPSETAddToList(key, value)		




 
 








# Entering Main Program Body
if __name__ == "__main__":
  main()


