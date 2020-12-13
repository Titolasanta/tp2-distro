#!/usr/bin/env python3
import time
import os
import json_lines
import pickle
from datetime import datetime

import middleware as md

time.sleep(60)


PRODUCER_QUEUE = "basic_producer_queue"
DELIVERY_QUEUE = "basic_delivery_queue"


N_PRODUCERS = os.environ['N_PRODUCERS']
N_PRODUCERS = int(N_PRODUCERS)

middleware = md.Middleware()



def callback(ch, method, properties, body):

	#len 100
	recived_list = pickle.loads(body)
	for item in recived_list:
		
		if(item == "EOF"):
			middleware.send_to_queue(PRODUCER_QUEUE,"EOF",N_PRODUCERS)
			middleware.flush()
		else:		
			
			middleware.send_to_queue(PRODUCER_QUEUE,item,N_PRODUCERS,item["user_id"])
			
		

middleware.set_callback_with_ack(callback,DELIVERY_QUEUE)
middleware.start()


