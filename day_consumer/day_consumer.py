#!/usr/bin/env python3
import pika
import time
import middleware as md



import os

DAY_SINK_QUEUE = "day_sink"



id = ""
try:
	id = os.environ["ID"]
except:
	id = ""

DAY_COUNTER_QUEUE = "day_counter_queue"

time.sleep(60)

count = {}

middleware = md.Middleware()

def remit_dic(dic,queue_name):

	for key in dic:
		msg = str(key) +","+ str(dic[key])
		middleware.send_to_queue(queue_name,msg )


	middleware.send_to_queue(queue_name,"EOF" )


def callback(ch, method, properties, body):
	if(body.decode("utf-8") == "EOF"):
		print("entre")
		remit_dic(count,DAY_SINK_QUEUE)
		return
	else:
		body = body.decode("utf-8")
		body = body.split(",")
		body = body[0]
		
		if body in count:
			count[body] = count[body]+1
		else:
			count[body] = 1


middleware.set_callback_with_ack(callback,DAY_COUNTER_QUEUE+id)
middleware.start()