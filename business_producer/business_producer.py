#!/usr/bin/env python3
import time

import json_lines
from datetime import datetime

import middleware as md

time.sleep(60)

PRODUCER_SINK_QUEUE = "producer_sink"

middleware = md.Middleware()



with open('data/yelp_academic_dataset_business.json', 'rb') as f:
	i = 0
	for item in json_lines.reader(f):
		#if(i == 10):
		#	middleware.send_to_queue(PRODUCER_SINK_QUEUE,"EOF")
		#	break
		#i = i + 1
		middleware.send_to_queue(PRODUCER_SINK_QUEUE,item["business_id"]+","+str(item["city"]))

middleware.send_to_queue(PRODUCER_SINK_QUEUE,"EOF")