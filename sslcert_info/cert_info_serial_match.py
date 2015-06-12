#!/usr/bin/python


# Author: Yuri
# Date: 06-11-2015
# Description: Get certificate serial number from incommon website. Then run this
#  script with inputed serial number from incommon and it will try to match up the 
#  certificate so you can easily locate them on your systems
#

import os
import sys
import subprocess
import glob


##############################################################
# Verify if openssl is present on the system. If not then exit
#
##############################################################
#
BINSSL = subprocess.Popen(['which', 'openssl'],
	stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT)
BINSSL, BINSSLerror = BINSSL.communicate()
BINSSL = BINSSL.rstrip() # strip new line


# does openssl exist? If not exit...

if ( not os.path.isfile(BINSSL)):
	print "%s not found. Exiting" % BINSSL
	sys.exit()
##############################################################








##############################################################
# i_serial is a serial number that is passed as user input 
# parameter. If no serial number provided then script exits
# 
##############################################################
if sys.argv[1:]:						# test if sys.argv has passed value
	i_serial = sys.argv[1]				# user input parameter
	i_serial = i_serial.split(':')		# split by colon (:)
	i_serial = ''.join(i_serial)		# join by spaces
	i_serial = i_serial.strip('\n')		# remove newline
	i_serial = i_serial.upper()			# upper case all characters
else:
	print "Please provide Certificate serial number from incommon site and run against any server"
	print "Example:  "
	print "\t  script.py 3B:80:FD:61:DE:1A:FB:91:8A:54:9A:A8:BF:73:E2:A3"
	sys.exit()








##############################################################
# glob allows you to use shell wildcards when listing files
# grab all certificationes in /etc/pki/tls/certs directory
# and extract their serial number
##############################################################
#
certlist = glob.glob('/etc/pki/tls/certs/*.crt')
for f_file in certlist:
	#print f_file
	CERT_OUT = subprocess.Popen('openssl x509 -in %s -serial -noout' % f_file,
		shell=True, stdout=subprocess.PIPE)
	CERT_OUT = CERT_OUT.communicate()[0]


	# split output by '=' and grab serial number only...
	serial = CERT_OUT.split('=')[1].strip('\n')


	# Do serial numbers match? If so then key is found...
	if i_serial == serial:
		print "%s -- MATCH!" % f_file
		print "cert_serial: %s " % serial
		print "user_serial: %s " % i_serial
		print "\n"






