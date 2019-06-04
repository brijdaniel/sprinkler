import os
from time import sleep
import paho.mqtt.client as mqtt
import sprinkler
from configure import Configure
import RPi.GPIO as GPIO
import cron, datetime

global config
config = Configure()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	
	subscriptions = config.read('MQTTConfig', 'subscriptions')
	subscriptions = subscriptions.split(',')

	for topic in subscriptions:
		client.subscribe(topic)
		print("Subscribed to "+ topic)

def on_message(client, userdata, msg):

	topic = msg.topic
	payload_decode = str(msg.payload.decode("utf-8"))
	print(topic+": "+payload_decode)

	if topic == 'pihouse/sprinkler/control':
		if payload_decode == "True":
			os.environ["sp_ctl"] = "True"
			sprinkler.main()
		elif payload_decode == "False":
			os.environ["sp_ctl"] = "False"
	else:
		if payload_decode == "request":
			client.publish(topic, config.read('SPConfig', topic))
			if topic == 'pihouse/sprinkler/schedule/next':
				client.publish(topic, str(cron.next().strftime('%H:%M, %a %d/%m/%y')))
		else:
			config.set('SPConfig', topic, str(payload_decode))
			if topic == 'pihouse/sprinkler/schedule':
				sleep(0.1)
				job_string = config.read('SPConfig', topic)
				checkbox = config.read('SPConfig', 'pihouse/sprinkler/schedule/set')
				cron.set(job_string, checkbox)
							
# Create and connect MQTT object
client = mqtt.Client(client_id=config.read('MQTTConfig', 'client_id'), clean_session=False)
client.on_message = on_message
client.on_connect = on_connect
client.connect(config.read('MQTTConfig', 'server'), 1883, 60)
client.loop_start()

# Flag for managing sp_status publishes
flag = False

# Main loop
while True:
	if os.environ.get('sp_status') == "True" and not flag:
		client.publish('pihouse/sprinkler/status', "True")
		flag = True
	if os.environ.get('sp_status') == "False" and  flag:
		client.publish('pihouse/sprinkler/status', "False")
		flag = False
	sleep(0.01)

