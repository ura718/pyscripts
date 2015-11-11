#!/usr/bin/python

#
# What this program does is builds an email message from different parts
# 
#
#

#
# MIMEApplication - used to send raw binary data (attachment)
# MIMEText - used to send ascii formatted text in body
# MIMEMultipart - used to construct email msg (From, TO, Subject)
#

from email.mime.application import MIMEApplication	
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP




msg = MIMEMultipart()
msg['Subject'] = 'Hello'
msg['From'] = 'ym26@nyu.edu'
msg['To'] = 'ym26@nyu.edu'




# This is what you see if you dont have an email reader
msg.preamble = 'Multipart message. \n'



# This is the body of the email
part = MIMEText("Just a test email")
msg.attach(part)



# This is the binary part (Attachment)
part = MIMEApplication(open('junk','rb').read())
part.add_header('Content-Disposition', 'attachment', filename='junk')
msg.attach(part)




# Create an instance in SMTP server
smtp = SMTP('localhost')



# Start the server
smtp.ehlo()


# send email
smtp.sendmail(msg['From'], msg['To'], msg.as_string())



