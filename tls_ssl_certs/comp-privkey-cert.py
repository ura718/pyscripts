#!/usr/bin/python

#
# Author: Yuri Medvinsky
# Date: 1/11/2018
# Info: Use openssl to calculate modulus of certificate and private key and compare resutls
#       If they match then certificate is associated with private key
#       If they dont match then certificate is not associated with private key 
#

from subprocess import Popen, PIPE
import glob
import os


crtlist = (glob.glob("/etc/pki/tls/certs/*edu.crt"))
privkeylist = (glob.glob("/etc/pki/tls/private/*private.key"))



Certs = {}  # create empty dictionary
for c in crtlist:
  # remove .crt extension from filename
  c_noext = '.'.join(os.path.basename(c).split('.')[:-1])

  # remove private.key extention from filename
  for k in privkeylist:
    k_noext = '.'.join(os.path.basename(k).split('.')[:-2])


    # If private key and certificate name match then create a key valu dictionary with those names (e.g: "host.private.key : host.crt" )
    if c_noext == k_noext:
      Certs[k]=c






for key,value in Certs.iteritems():

  # Key 
  # This runs command (e.g: openssl rsa -noout -modulus -in server.key | openssl md5)
  p1 = Popen(['openssl', 'rsa', '-noout', '-modulus', '-in', '%s' % key], stdout=PIPE)
  p2 = Popen(['openssl', 'md5'], stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
  p1.stdout.close()

  k_md5, k_md5err = p2.communicate()
  k_md5 = k_md5.split()[1]



  # CRT
  # This runs command (e.g: openssl x509  -noout -modulus -in server.crt | openssl md5)
  p1 = Popen(['openssl', 'x509', '-noout', '-modulus', '-in', '%s' % Certs[key]], stdout=PIPE)
  p2 = Popen(['openssl', 'md5'], stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
  p1.stdout.close()


  c_md5, c_md5err = p2.communicate()
  c_md5 = c_md5.split()[1]


  if k_md5 == c_md5:
    print "[+] {0:77}: {1:32}  -- match".format(key,k_md5)
    print "[+] {0:77}: {1:32}  -- match".format(value,c_md5)
  elif k_md5 != c_md5:
    print "[-] {0:77}: {1:32}  -- no match".format(key,k_md5)
    print "[-] {0:77}: {1:32}  -- no match".format(value,c_md5)

