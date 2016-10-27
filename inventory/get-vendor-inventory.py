#!/usr/bin/python


#
# Author: Yuri M,
# Date: 10-06-2016
# Info: Select vendor related information from the inventory database
#

import MySQLdb as mariadb





class SelectFromDB:

  def __init__(self):

    ''' Class Contains only Select Statements '''



  def selectVendorData(self, cursor):


    ''' SELECT DATA FROM VENDOR COLUMNS ''' 

    print "%-18s %-20s %-16s %-16s %-14s %-15s %-26s %-10s" % ('hostname', 'OS', 'osrelease_major', 'osrelease_minor','serial_number','Product_Name','Manufacturer', 'date') 
    print "%-18s %-20s %-16s %-16s %-14s %-15s %-26s %-10s" % ('-'*18, '-'*20, '-'*16, '-'*16, '-'*14, '-'*15, '-'*26, '-'*10) 
   
    # Execute sql statement
    cursor.execute("select hostname, OS, osrelease_major, osrelease_minor, serial_number, Product_Name, Manufacturer, date from servers join vendor on vendor.vendor_uuid = servers.system_uuid")



    # Process each row
    width=10
    for row in cursor:
 
      # Convert row from tuple to list
      row = list(row)
      
      # Print only rows that are not empty from servers table. The %-NNs are column alignment
      if row is not None:
        print "%-18s %-20s %-16s %-16s %-14s %-15s %-26s %-10s" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])







###################################################################
# main body

def main():

  # Class Assignment
  selectfromdb = SelectFromDB()



  '''  Establish DB Connection '''
  
  # Create new connection to database
  mariadb_connection = mariadb.connect(host='<hostname>', port=<port>, user='<username>', passwd='<password>', db='<database name>')
  cursor = mariadb_connection.cursor()


  selectfromdb.selectVendorData(cursor)



  # Commit changes to database and close connection
  mariadb_connection.commit()
  mariadb_connection.close()

###################################################################
#

if __name__ == '__main__':
  main()
