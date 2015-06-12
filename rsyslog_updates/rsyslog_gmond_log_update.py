#!/usr/bin/python


#
# Author: Yuri Medvinsky
# Date: 11-03-2014
# This script updates /etc/rsyslog.conf file by appending rule set to redirect
# all messages filtered by "metric" from /var/log/messages to /var/log/gmond.log 
#




import sys


def updateSYSLOG(file):
  fo = open(file, "r")			# open file
  syslogfile = fo.readlines()		# assign output of file to syslogfile
  fo.close()  				# close file

  for lines in syslogfile:		
    lines = lines.rstrip()		# remove trailing characters from each line


  fo = open(file, "r+")			# open file for writing
  flag='Flase'
  for i in range(len(syslogfile)):		# create index i loop
    if "# Ganglia log" in syslogfile[i]:
      flag='True'
   
   
    if "#### RULES ####" in syslogfile[i]:
      RULES_array_index = i 
    
 
  if flag == 'True':
    pass
  else:
    try:
      syslogfile.insert(RULES_array_index + 1, '\n# Ganglia log\n')
      syslogfile.insert(RULES_array_index + 2, ':msg, contains, \"metric\" \t\t\t\t/var/log/gmond.log\n') 
      syslogfile.insert(RULES_array_index + 3, '&~\n\n')
      fo.writelines(syslogfile)
    except UnboundLocalError, e:
      print "Did you assign value to RULES_array_index?...Error: %s \n" % e
  fo.close()



def main():
  file = '/var/tmp/ym/syslog.conf'
  try:
    f = open(file,'r')  		# test if file can be opened/exists
    data = f.readlines()
    f.close()
  except IOError, e:
      print "Cant open file " 
      sys.exit(1)
 
 
  updateSYSLOG(file)

  


if __name__ == '__main__':
  main()
