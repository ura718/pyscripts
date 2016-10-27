#!/usr/bin/python

#
# Author: Yuri M,
# Date: 09-08-2016
# Info: Collects information about systems architecture, network, os...etc. 
#       Places the collected data into amazon rds database running mariadb. 
#       The database is called inventory. 
#

# Requirements: 
#   MySQL-python.x86_64



import MySQLdb as mariadb
import subprocess
import dmidecode
import platform
import socket
import time
import re
import os






class InsertIntoDB:

  def __init__(self):

    ''' Class Contains Only Insert Statements '''
  

  def insertIntoServersTable(self, cursor, system_uuid, hostid, hostname, today):

    cursor.execute("INSERT INTO servers (system_uuid, hostid, hostname, date) \
                 VALUES (%s, %s, %s, %s) \
                 ON DUPLICATE KEY UPDATE \
                 system_uuid=VALUES(system_uuid), hostid=VALUES(hostid), hostname=VALUES(hostname), date=VALUES(date)", (system_uuid, hostid, hostname, today))

  

   
  def insertIntoVendorTable(self, cursor, osflavor, osrelease_major, osrelease_minor, Serial_Number, Product_Name, Manufacturer, system_uuid):

    cursor.execute("INSERT INTO vendor (OS, osrelease_major, osrelease_minor, Serial_Number, Product_Name, Manufacturer, vendor_uuid) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s) \
                 ON DUPLICATE KEY UPDATE \
                 OS=VALUES(OS), osrelease_major=VALUES(osrelease_major), osrelease_minor=VALUES(osrelease_minor), Serial_Number=VALUES(Serial_Number), Product_Name=VALUES(Product_Name), \
                 Manufacturer=VALUES(Manufacturer), vendor_uuid=VALUES(vendor_uuid)", \
                 (osflavor, osrelease_major, osrelease_minor, Serial_Number, Product_Name, Manufacturer, system_uuid))




  def insertIntoNetworkTable(self, cursor, interface, ipaddress, macaddress, system_uuid):
    
    cursor.execute("INSERT INTO network (interface, ipaddress, macaddress, network_uuid) \
                 VALUES (%s, %s, %s, %s) \
                 ON DUPLICATE KEY UPDATE \
                 interface=VALUES(interface), ipaddress=VALUES(ipaddress), macaddress=VALUES(macaddress), network_uuid=VALUES(network_uuid)", \
                 (interface, ipaddress, macaddress, system_uuid))














class SelectFromDB:

  def __init__(self):
  
    ''' Class Contains only Select Statements '''

    # Table Servers 
    #
    # Get table servers, column names 
    self.SQLGetColNames = "SHOW columns FROM servers"

    # Get all from table servers
    self.SQLGetAllServers = "SELECT * FROM servers"





  def selectFromTableServers(self, cursor):

    # Execute sql statement
    cursor.execute(self.SQLGetColNames)

    # Extract only column names and exclude their definitions 
    col = [] 
    for column in cursor.fetchall():
      col.append(column[0])


    # Print all column names
    print "%-40s %-10s %-20s %-12s" % (col[0], col[1], col[2], col[3])

    # Print dashed-lines under each column (e.g: ----)
    print "%-40s %-10s %-20s %-12s" % ('-'*40, '-'*10, '-'*20, '-'*12)





    # Execute sql statement
    cursor.execute(self.SQLGetAllServers)

    # Process each row
    for row in cursor:

      # Convert row from tuple to list
      row = list(row)

      # Print only rows that are not empty from servers table. The %-NNs are column alignment
      if row is not None:
        print "%-40s %-10s %-20s %-12s" % (row[0], row[1], row[2], row[3])











class ServerInfo:  

  def __init__(self):

    '''Class Extracts Server Architecture Characteristics '''



  def getSYSTEM(self):
    SYSTEMdict = {}
    for v in dmidecode.system().values():
      if type(v) == dict and v['dmi_type'] == 1:
        SYSTEMdict["Manufacturer"] = str((v['data']['Manufacturer']))
        SYSTEMdict["Product_Name"] = str((v['data']['Product Name']))
        SYSTEMdict["Serial_Number"] = str((v['data']['Serial Number']))
        SYSTEMdict["UUID"] = str((v['data']['UUID']))

    return SYSTEMdict["Manufacturer"], SYSTEMdict["Product_Name"], SYSTEMdict["Serial_Number"], SYSTEMdict["UUID"]







  def getHOST(self):

    # Get hostname
    hostname = socket.gethostname()


    # Get hostid
    c1 = subprocess.Popen(['hostid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    c1, c1error = c1.communicate()
    hostid = c1.strip() 


    # Get today date
    today = time.strftime("%Y-%m-%d")

    # Get os flavor (e.g: redhat)
    osflavor = platform.dist()[0]


    # Get os version (e.g: 6.5)
    (osrelease_major, osrelease_minor) = platform.dist()[1].split('.')

    return (hostname, hostid, osflavor, osrelease_major, osrelease_minor, today)








  def getNET(self):

    # Get all registered network interfaces, except loopback
    listinterfaces = os.listdir('/sys/class/net/')

    # Will hold all eth dictionaries in a list form
    ethlist = []



    for intface in listinterfaces:
      

      # Exclude lo loopback devices and make sure intface is directory 
      if intface != 'lo' and os.path.isdir('/sys/class/net/%s' % intface):
    

        try:
          # Record interface state (UP/DOWN)
          fo = open('/sys/class/net/%s/operstate' % intface, 'r')
          int_state = fo.readline().strip()
          fo.close()
        except IOError, e:
          pass
         

        # Record only UP states
        if int_state == 'up':

          try:
            # Record mac address        
            fo = open('/sys/class/net/%s/address' % intface, 'r')
            hwaddr = fo.readline().strip()
            fo.close() 
          except IOError, e:
            pass
    

          try: 
            # Record mtu 
            fo = open('/sys/class/net/%s/mtu' % intface, 'r')
            mtusize = fo.readline().strip()
            fo.close() 
          except IOError, e:
            pass      
  


          # (e.g: ifconfig eth0)
          n1 = subprocess.Popen(['ifconfig', '%s' % intface], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          n1, n1error = n1.communicate()
          n1 = n1.split('\n')


          for line in n1:

            # search for inet within entire line, if found then process that line
            if re.search(r"inet ", line):


              # Find 'addr:<ip>' address
              ipaddr = re.findall("addr:\d+\.\d+\.\d+\.\d+", line)
              if ipaddr:
                # split ipaddr[0] list by colon. The ipaddr[0] is because its first element and only element in list
                ipaddr =  ipaddr[0].split(':')[1]


              # Find 'Bcast:<ip>' address
              bcast = re.findall("Bcast:\d+\.\d+\.\d+\.\d+", line)
              if bcast:
                # Get Broadcast
                broadcast = bcast[0].split(':')[1]




              # Find 'Mask:<ip>' address
              mask = re.findall("Mask:\d+\.\d+\.\d+\.\d+", line)
              if mask:
                # Get NetMask
                netmask = mask[0].split(':')[1]
 
          

  
          # Test if ipaddr, broadcast, netmask have assigned values. If not then zero them out          
          try:
            ipaddr
          except NameError: 
            ipaddr = None          
  

          try:
            broadcast
          except NameError: 
            broadcast = None          


          try:
            netmask
          except NameError: 
            netmask = None          



 
          # Creates a double dictionary. (e.g: intface = eth0..eth9)
          eth = {intface: {'state': int_state, 'mac': hwaddr, 'mtu': mtusize, 'ip': ipaddr, 'bcast': broadcast, 'mask': netmask}}
      
          # Append dictionary to list
          ethlist.append(eth)


    return ethlist





  def getVIPS(self):

    # First identify all available vips
    n1 = subprocess.Popen(['ifconfig', '-a'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    n1, n1error = n1.communicate()
    n1 = n1.split('\n')

    vips = []
    for line in n1:
      if re.search(r"lo:", line):
        vips.append(line.split()[0])



    # Establish empty vip array
    viplist = []

    # Second extract data from each vipintface
    for vipintface in vips:

      # (e.g: ifconfig eth0)
      n1 = subprocess.Popen(['ifconfig', '%s' % vipintface], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      n1, n1error = n1.communicate()
      n1 = n1.split('\n')



      #print "loopback: %s" % vipintface
      for line in n1:


        # search for inet within entire line, if found then process that line
        if re.search(r"inet", line):



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

            #print "netmask: %s" % netmask






        if re.search(r"MTU", line):

          # Check Link State
          int_state = re.findall("UP", line)
          if int_state:
            # Link State is UP
            int_state = int_state[0]


            #print "state: %s" % int_state


          # Find MTU size
          mtu = re.findall("MTU:\d+", line)
          if mtu:
            # Get mtu size
            mtusize = mtu[0].split(':')[1]

            #print "mtu: %s" % mtusize





      # Loopback devices dont have mac's or broadcast. Zero the variables out.
      try:
        hwaddr
      except NameError:
        hwaddr = None
     
      try:  
        broadcast
      except NameError:
        broadcast = None




      # Creates a double dictionary. (e.g: intface = lo:0..lo:9)
      vip = {vipintface: {'state': int_state, 'mac': hwaddr, 'mtu': mtusize, 'ip': ipaddr, 'bcast': broadcast, 'mask': netmask}}
      
      # Append dictionary to list
      viplist.append(vip)


    return viplist








###################################################################
# main body

def main():

  

  # Assign Class functions
  serverinfo = ServerInfo()           # Get information about server (e.g: network, arch, vendor)
  insertintodb = InsertIntoDB()       # Used to insert data into DB
  selectfromdb = SelectFromDB()       # Used to extract data from DB




  # Get Vendor 
  (Manufacturer, Product_Name, Serial_Number, system_uuid) = serverinfo.getSYSTEM() 

  # Get Host 
  (hostname, hostid, osflavor, osrelease_major, osrelease_minor, today) = serverinfo.getHOST()

  # Get Network eth info
  ethlist = serverinfo.getNET()

  # Get Network vip info
  viplist = serverinfo.getVIPS()


  '''

  # Test print output 
  print 
  print "TESTING SERVERS TABLE"
  print "system uuid: %s " % system_uuid 
  print "hostid: %s " % hostid
  print "hostname: %s " % hostname
  print "date: %s " % today
  print
  print "TESTING VENDOR TABLE"
  print "OS: %s " % osflavor
  print "OSrelease_major: %s " % osrelease_major
  print "OSrelease_minor: %s " % osrelease_minor
  print "Serial Number: %s " % Serial_Number 
  print "Product Name: %s " % Product_Name
  print "Manufacturer: %s " % Manufacturer
  print "system uuid: %s " % system_uuid 
  print

  print "TESTING NETWORK TABLE"

  # Iterate through ethlist list array, and then iterate each array element as dictionary 
  for item in ethlist:
    for k,v in item.iteritems():
      print k, v['ip'], v['mac']


  # Iterate through viplist list array, and then iterate each array element as dictionary 
  for item in viplist:
    for k,v in item.iteritems():
      print k, v['ip'], v['mac']

  '''









  '''  Establish DB Connection '''

  # Create new connection to database
  mariadb_connection = mariadb.connect(host='<servername>', port=<port>, user='<username>', passwd='<password>', db='<database name>')
  cursor = mariadb_connection.cursor()


  # Insert data into servers table
  insertintodb.insertIntoServersTable(cursor, system_uuid, hostid, hostname, today)


  # Insert data into vendor table
  insertintodb.insertIntoVendorTable(cursor, osflavor, osrelease_major, osrelease_minor, Serial_Number, Product_Name, Manufacturer, system_uuid)

  # Insert eth interface data into network table
  for item in ethlist:
    for k,v in item.iteritems():
      #print k, v['ip'], v['mac']
      interface=k
      ipaddress=v['ip']
      macaddress=v['mac']
      #print '[+] ', interface, ipaddress, macaddress, system_uuid
      insertintodb.insertIntoNetworkTable(cursor, interface, ipaddress, macaddress, system_uuid)


  # Insert vip interface data into network table
  for item in viplist:
    #print "item: %s" % item
    for k,v in item.iteritems():
      #print k, v['ip'], v['mac']
      interface=k
      ipaddress=v['ip']
      macaddress=v['mac']
      #print '[+] ', interface, ipaddress, macaddress, system_uuid
      insertintodb.insertIntoNetworkTable(cursor, interface, ipaddress, macaddress, system_uuid)




  # Select from DB
  #selectfromdb.selectFromTableServers(cursor)





  # Commit changes to database and close connection
  mariadb_connection.commit()
  mariadb_connection.close()




###################################################################
#

if __name__ == '__main__':
  main()




