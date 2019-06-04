
import os
import sys
from time import sleep, time
from threading import Thread
import RPi.GPIO as GPIO
from configure import Configure
import datetime

# initialise GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) 

def run_sprinkler(flag):
  # Get configuration data
	config = Configure()
	section = 'SPConfig'
	pin = int(config.read(section, 'pin'))
	sp_timer = float(config.read(section, 'pihouse/sprinkler/timer'))
  
	# Turn pin on
	print ('Starting sprinkler')
	GPIO.output(pin, GPIO.HIGH)
	os.environ["sp_status"] = "True"
	config.set('SPConfig', 'pihouse/sprinkler/schedule/last', str(datetime.datetime.now().strftime('%H:%M, %a %d/%m/%y')))

  # If flag changes then turn off, otherwise run for config time  
	timer = time() + sp_timer * 60
	while time() < timer:
		if flag == "False":
			print ('Stopping sprinkler (button)')
			GPIO.output(pin, GPIO.LOW)
			os.environ["sp_status"] = "False"
			break
		else:
			sleep(0.1)
			flag = os.environ.get('sp_ctl')   
	else:
		print ('Stopping sprinkler (timer)')
		GPIO.output(pin, GPIO.LOW)
		os.environ["sp_status"] = "False"

def main():
	thread = Thread(target=run_sprinkler, args=[os.environ.get('sp_ctl')])
	thread.start()
  
# execute main() if run from crontab
if os.environ.get('CRONTAB') == 'true':
	main()
	print ('cron')