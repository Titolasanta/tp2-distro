#!/usr/bin/env python3
import pika
import time
import middleware as md
import os




TEXT_SINK_QUEUE = "text_sink"


id = ""
try:
	id = os.environ["ID"]
except:
	id = ""


TEXT_COUNTER_QUEUE = "text_counter_queue"

time.sleep(60)

count = {}
ignore_count = {}

middleware = md.Middleware()

def text_dic_to_count(dic):
	for key in dic:
		dic[key] = dic[key][1]

def remit_dic(dic,queue_name):

	for key in dic:
		if dic[key] >= 5:
			msg = str(key) +","+ str(dic[key])

			middleware.send_to_queue(queue_name,msg )

	middleware.send_to_queue(queue_name,"EOF" )


def callback(ch, method, properties, body):
	if(body.decode("utf-8") == "EOF"):
		
		text_dic_to_count(count)
		
		print("entre")
		remit_dic(count,TEXT_SINK_QUEUE)
		return
	else:
		body = body.decode("utf-8")
		body = body.split(",")
		user = body[0]
		text = body[1]

		if user not in ignore_count:
			if(user in count):
				if count[user][0] == text:
					#+1 counter
					count[user] = (text,count[user][1]+1)
				else:
					#add to ignore
					del count[user]
					ignore_count[user] = 1
			else:
				#first aparetion
				count[user] = (text,1)		

		
middleware.set_callback_with_ack(callback,TEXT_COUNTER_QUEUE+id)
middleware.start()