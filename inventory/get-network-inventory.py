#!/usr/bin/python


#
# Author: Yuri M,
# Date: 10-06-2016
# Info: Select network related information from the inventory database
#


import MySQLdb as mariadb





class SelectFromDB:

  def __init__(self):

    ''' Class Contains only Select Statements '''



  def selectNetworkData(self, cursor):


    ''' SELECT DATA FROM NETWORK COLUMNS ''' 


    # Creates column alignment. Use length from largest entity either from data or column name
    print "%-18s %-10s %-17s %-19s %-10s" % ('hostname', 'interface', 'ipaddress', 'macaddress', 'date') 
    print "%-18s %-10s %-17s %-19s %-10s" % ('-'*18, '-'*10, '-'*17, '-'*19, '-'*10) 
   
    # Execute sql statement
    cursor.execute("select hostname,interface,ipaddress,macaddress,date from servers join network on network.network_uuid = servers.system_uuid")



    # Process each row
    for row in cursor:
 
      # Convert row from tuple to list
      row = list(row)
      
      # Print only rows that are not empty from servers table. The %-NNs are column alignment
      if row is not None:
        print "%-18s %-10s %-17s %-19s %-10s" % (row[0], row[1], row[2], row[3], row[4])







###################################################################
# main body

def main():

  # Class Assignment
  selectfromdb = SelectFromDB()



  '''  Establish DB Connection '''
  
  # Create new connection to database
  mariadb_connection = mariadb.connect(host='<servername>', port=<port>, user='<username>', passwd='<password>', db='<database name>')
  cursor = mariadb_connection.cursor()


  selectfromdb.selectNetworkData(cursor)



  # Commit changes to database and close connection
  mariadb_connection.commit()
  mariadb_connection.close()

###################################################################
#

if __name__ == '__main__':
  main()
