#!/usr/bin/env python3
import time
import os
import json_lines
import pickle
import logging
from datetime import datetime

import middleware as md

logging.basicConfig(level = logging.INFO)

time.sleep(60)

DELIVERY_QUEUE = "basic_delivery_queue"
BUSINESS_PRODUCER_QUEUE = "business_producer_queue"
CLIENT_SINK_QUEUE = "client_sink_queue"


middleware = md.Middleware()

with open('data/yelp_academic_dataset_business.json', 'rb') as f:
	for item in json_lines.reader(f):
		middleware.send_to_queue(BUSINESS_PRODUCER_QUEUE,item)
		
middleware.send_to_queue(BUSINESS_PRODUCER_QUEUE,"EOF")
middleware.flush()

with open('data/yelp_academic_dataset_review.json', 'rb') as f:
	i = 0
	for item in json_lines.reader(f):
		if(i==200000):
			break
			#time.sleep(10)
			
			#print(i)

		middleware.send_to_queue(DELIVERY_QUEUE,item)
		
		i = i + 1
		
	
middleware.send_to_queue(DELIVERY_QUEUE,"EOF")
middleware.flush()

def callback(ch, method, properties, body):


	recived_list = pickle.loads(body)
	for body in recived_list:
		logging.info("{}".format(body))
middleware.set_callback_with_ack(callback,CLIENT_SINK_QUEUE)
middleware.start()