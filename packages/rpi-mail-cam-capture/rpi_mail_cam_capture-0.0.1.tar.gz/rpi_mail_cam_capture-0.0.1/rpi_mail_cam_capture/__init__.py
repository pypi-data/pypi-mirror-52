from picamera import PiCamera
from time import sleep
import smtplib
import time
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO
import time
def send_mail(me, sender_password, toaddr, subject):
	#toaddr = 'receivers mail address'
	#me = 'senders mail address'
	#Subject='security alert'
	P=PiCamera()
	P.resolution= (320,240)
	P.start_preview()
	while_true_var=0
	while while_true_var==0:
		if while_true_var==0:
			time.sleep(2)
			P.capture('rpi_cam_capture.jpg')
			time.sleep(10)
			msg = MIMEMultipart()
			msg['Subject'] = subject
			msg['From'] = me
			msg['To'] = toaddr
			fp= open('rpi_cam_capture.jpg','rb')
			img = MIMEImage(fp.read())
			fp.close()
			msg.attach(img)
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(user = me, password = sender_password)
			server.sendmail(me, toaddr, msg.as_string())
			server.quit()
			P.stop_preview()
			while_true_var=1