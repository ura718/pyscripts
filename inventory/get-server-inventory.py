#!/usr/bin/python


#
# Author: Yuri M,
# Date: 10-06-2016
# Info: Select server related information from the inventory database
#

import MySQLdb as mariadb





class SelectFromDB:

  def __init__(self):

    ''' Class Contains only Select Statements '''



  def selectServerData(self, cursor):


    ''' SELECT DATA FROM VENDOR COLUMNS ''' 

    print "%-36s %-10s %-16s %-10s" % ('system_uuid', 'hostid', 'hostname', 'date') 
    print "%-36s %-10s %-16s %-10s" % ('-'*36, '-'*10, '-'*16, '-'*10) 
   
    # Execute sql statement
    cursor.execute("select system_uuid, hostid, hostname, date from servers where servers.system_uuid = servers.system_uuid")



    # Process each row
    width=10
    for row in cursor:
 
      # Convert row from tuple to list
      row = list(row)
      
      # Print only rows that are not empty from servers table. The %-NNs are column alignment
      if row is not None:
        print "%-36s %-10s %-16s %-10s" % (row[0], row[1], row[2], row[3])







###################################################################
# main body

def main():

  # Class Assignment
  selectfromdb = SelectFromDB()



  '''  Establish DB Connection '''
  
  # Create new connection to database
  mariadb_connection = mariadb.connect(host='<servername>', port=<port>, user='<username>', passwd='<password>', db='<database name>')
  cursor = mariadb_connection.cursor()


  selectfromdb.selectServerData(cursor)



  # Commit changes to database and close connection
  mariadb_connection.commit()
  mariadb_connection.close()

###################################################################
#

if __name__ == '__main__':
  main()
