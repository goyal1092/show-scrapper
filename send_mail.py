import smtplib

sender = 'xxxxxxxxxxxx'


def send_mail(message, user="xxxxxxxxxxx"):
	"""
	Send email
	"""
	receivers = [user]
	try:
	   smtpObj = smtplib.SMTP('localhost')
	   smtpObj.sendmail(sender, receivers, message)         
	   print "Successfully sent email"
	except:
	   print "Error: unable to send email"