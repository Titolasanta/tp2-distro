#!/usr/bin/env python3
import pika
import time
import middleware as md
import os
import pickle

BASIC_SINK_QUEUE = "basic_sink"

BASIC_COUNTER_QUEUE = "basic_counter_queue"
N_PRODUCERS = os.environ["N_PRODUCERS"]
N_PRODUCERS = int(N_PRODUCERS)

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
	middleware.flush()


eof_recived = [0]
def callback(ch, method, properties, body):


	recived_list = pickle.loads(body)
	for body in recived_list:
		if(body == "EOF"):
			eof_recived[0]=eof_recived[0]+1
			if(eof_recived[0] == N_PRODUCERS):
				remit_dic(count,BASIC_SINK_QUEUE)
			
		else:
			body = body
			
			if body in count:
				count[body] = count[body]+1
			else:
				count[body] = 1

middleware.set_callback_with_ack(callback,BASIC_COUNTER_QUEUE+id)
middleware.start()