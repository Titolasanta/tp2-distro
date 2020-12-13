#!/usr/bin/env python3
import time

import pickle
import json_lines
from datetime import datetime

import middleware as md

time.sleep(60)

PRODUCER_SINK_QUEUE = "producer_sink"
BUSINESS_PRODUCER_QUEUE = "business_producer_queue"

middleware = md.Middleware()


def callback(ch, method, properties, body):
	recived_list = pickle.loads(body)
	for item in recived_list:
		
		if(item == "EOF"):
			middleware.send_to_queue(PRODUCER_SINK_QUEUE,"EOF")
			middleware.flush()		
			break
		else:	
			middleware.send_to_queue(PRODUCER_SINK_QUEUE,item["business_id"]+","+str(item["city"]))


middleware.set_callback_with_ack(callback,BUSINESS_PRODUCER_QUEUE)
middleware.start()