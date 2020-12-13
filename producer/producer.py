#!/usr/bin/env python3
import time
import os
import json_lines
import pickle
from datetime import datetime

import middleware as md

time.sleep(60)


id = ""
try:
	id = os.environ["ID"]
except:
	id = ""

PRODUCER_QUEUE = "basic_producer_queue"
BASIC_COUNTER_QUEUE = "basic_counter_queue"
STAR_COUNTER_QUEUE = "star_counter_queue"
DAY_COUNTER_QUEUE = "day_counter_queue"
TEXT_COUNTER_QUEUE = "text_counter_queue"
BUSINESS_COUNTER_QUEUE = "business_counter_queue"


N_BASIC_CONSUMERS = os.environ['N_BASIC_CONSUMERS']
N_BASIC_CONSUMERS = int(N_BASIC_CONSUMERS)
N_STAR_CONSUMERS = os.environ['N_STAR_CONSUMERS']
N_STAR_CONSUMERS = int(N_STAR_CONSUMERS)
N_DAY_CONSUMERS = os.environ['N_DAY_CONSUMERS']
N_DAY_CONSUMERS = int(N_DAY_CONSUMERS)
N_TEXT_CONSUMERS = os.environ['N_TEXT_CONSUMERS']
N_TEXT_CONSUMERS = int(N_TEXT_CONSUMERS)
N_BUSINESS_CONSUMERS = os.environ['N_BUSINESS_CONSUMERS']
N_BUSINESS_CONSUMERS = int(N_BUSINESS_CONSUMERS)
middleware = md.Middleware()



def callback(ch, method, properties, body):

	#len 100
	recived_list = pickle.loads(body)
	for item in recived_list:
		
		if(item == "EOF"):
			middleware.send_to_queue(STAR_COUNTER_QUEUE,"EOF",N_STAR_CONSUMERS)
			middleware.send_to_queue(BASIC_COUNTER_QUEUE,"EOF",N_BASIC_CONSUMERS)
			middleware.send_to_queue(DAY_COUNTER_QUEUE,"EOF",N_DAY_CONSUMERS)
			middleware.send_to_queue(TEXT_COUNTER_QUEUE,"EOF",N_TEXT_CONSUMERS)
			middleware.send_to_queue(BUSINESS_COUNTER_QUEUE,"EOF",N_BUSINESS_CONSUMERS)
			middleware.flush()
		else:		
			
			middleware.send_to_queue(BASIC_COUNTER_QUEUE,item["user_id"],N_BASIC_CONSUMERS,item["user_id"])
			
			date = datetime.strptime(item["date"], '%Y-%m-%d %H:%M:%S')
			weekday = date.weekday()

			middleware.send_to_queue(STAR_COUNTER_QUEUE,item["user_id"]+","+str(item["stars"]),N_STAR_CONSUMERS,item["user_id"])
			#to do: remplazar repartir tarea entre nodos por hash por roundrobin para day
			middleware.send_to_queue(DAY_COUNTER_QUEUE,str(weekday),N_DAY_CONSUMERS,str(weekday))
			middleware.send_to_queue(TEXT_COUNTER_QUEUE,item["user_id"]+","+str(item["text"]),N_TEXT_CONSUMERS,item["user_id"])
			middleware.send_to_queue(BUSINESS_COUNTER_QUEUE,item["business_id"]+","+str(item["funny"]),N_BUSINESS_CONSUMERS,item["business_id"])


middleware.set_callback_with_ack(callback,PRODUCER_QUEUE+id)
middleware.start()


