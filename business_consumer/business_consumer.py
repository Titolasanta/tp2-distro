#!/usr/bin/env python3
import pika
import time
import middleware as md
import os

BUSINESS_SINK_QUEUE = "business_sink"

BUSINESS_COUNTER_QUEUE = "business_counter_queue"

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
		msg = key +","+ str(dic[key])
		middleware.send_to_queue(queue_name,msg)
	middleware.send_to_queue(queue_name,"EOF" )


def callback(ch, method, properties, body):
	if(body.decode("utf-8") == "EOF"):
		print("entre")
		remit_dic(count,BUSINESS_SINK_QUEUE)
		return
	else:
		body = body.decode("utf-8")
		body = body.split(",")
		if int(body[1]) > 0:
			if body[0] in count:
				count[body[0]] = count[body[0]]+1
			else:
				count[body[0]] = 1


middleware.set_callback_with_ack(callback,BUSINESS_COUNTER_QUEUE+id)
middleware.start()