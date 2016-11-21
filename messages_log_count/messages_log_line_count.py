#!/opt/rh/python27/root/usr/bin/python


#
# Author: Yuri Medvinsky
# Date: 11/21/2016
# Extra: Need python 2.7 because collections.Counter is present starting from this version
# Info: Read the /var/log/messages and print out Month Day Hours:Minutes, number_of_line_occurrences for that minute
#
# e.g:
#    Nov 20 22:35,30
#    Nov 20 22:36,2
#    Nov 20 22:34,2
#    Nov 21 10:38,1
#


import collections


# Read messages file
with open('/var/log/messages', 'r') as f:
  f_lines = f.readlines()  



# Declare empty array
data = []




for i in f_lines:

  # The First join takes a line in list format, removes newline, extracts first 2 columns 0,1 and joins it with spaces (e.g: "Nov 20 22:35:00 somehost snmpd[2334]: Connection from UDP:" -> Nov 20)
  # The Second join takes the same line that is in list format, removes newline, takes a third column (time), splits it by colon (:), extracts first 2 columns (hour,minute), joins them back with a colon(:). (e.g 22:35:00 -> 22:35)
  # The Third join takes the same line that is in list format, removes, newline, takes a fourth column which is application name (e.g: snmpd, xinetd, kernel), split by colon (:) and take only application name. (e.g kernel: -> kernel)
  # Then we take the First join and concatenate it with Second join and Third join. We can concatenate only str() types and so when you do a join it converts a list into a str() automatically.
  
  # Without Applicatioin Name
  #data.append(' '.join(i.strip('\n').split()[0:2]) + ' ' + ':'.join((i.strip('\n').split()[2]).split(':')[0:2]))

  # With Application Name
  data.append(' '.join(i.strip('\n').split()[0:2]) + ' ' + ':'.join((i.strip('\n').split()[2]).split(':')[0:2]) + ' ' + ''.join(i.strip('\n').split()[4]).split(':')[0])



# Count how many elements are similar in data array. We read this (e.g: for l in data do l.strip() count up same elements and assign to counts)
counts = collections.Counter(l.strip() for l in data)



# print count of same elements in the data array per line
''' e.g:
    Nov 20 22:35,30
    Nov 20 22:36,2
    Nov 20 22:34,2
    Nov 21 10:38,1
    Nov 21 10:39,1
'''


print "Date (hr:min), Application, Count"
for line, count in counts.most_common():
  print "%s,%s" % (line,count)


