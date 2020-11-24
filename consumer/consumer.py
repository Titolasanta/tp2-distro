#!/usr/bin/env python3
import pika
import time
import middleware as md
import os

BASIC_SINK_QUEUE = "basic_sink"

BASIC_COUNTER_QUEUE = "basic_counter_queue"

id = ""
try:
	id = os.environ["ID"]
except:
	id = ""

time.sleep(60)

count = {}

middleware = md.Middleware()

def remit_dic(dic,queue_name):

	
	for key in dic:
		if dic[key] >= 50:
			msg = str(key) +","+ str(dic[key])
			middleware.send_to_queue(queue_name,msg )

	middleware.send_to_queue(queue_name,"EOF" )

def callback(ch, method, properties, body):
	if(body.decode("utf-8") == "EOF"):
		print("entre")
		remit_dic(count,BASIC_SINK_QUEUE)
		return
	else:
		body = body.decode("utf-8")
		
		if body in count:
			count[body] = count[body]+1
		else:
			count[body] = 1

middleware.set_callback_with_ack(callback,BASIC_COUNTER_QUEUE+id)
middleware.start()