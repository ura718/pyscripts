#!/usr/bin/python


#
# Connect to mariadb database and select information from specified table.
# Then print it out to screen
# 


import MySQLdb as mariadb




mariadb_connection = mariadb.connect(host='<put host here>', port=<put port here>, user='<put username here>', passwd='<put password here>', db='<put database name here>')
cursor = mariadb_connection.cursor()



cursor.execute("select interface, ipaddress, macaddress, network_uuid from network")


for interface, ipaddress, macaddress, network_uuid in cursor:
  #print ("%s, %s, %s, %s" % (interface, ipaddress, macaddress, network_uuid))

  #print "|{0:<{z}} | {1:^{x}}| {2:>{n}}".format(interface,ipaddress,macaddress, z=3,x=20,n=30)
  print "{0:<3} | {1:^20}| {2:>20} | {3:>40}".format(interface,ipaddress,macaddress,network_uuid)



