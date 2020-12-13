#!/usr/bin/env python3
import pika
import time
import middleware as md
import os
import pickle

BASIC_SINK_QUEUE = "basic_sink"

STAR_SINK_QUEUE = "star_sink"

TEXT_SINK_QUEUE = "text_sink"

DAY_SINK_QUEUE = "day_sink"

BUSINESS_SINK_QUEUE = "business_sink"

PRODUCER_SINK_QUEUE = "producer_sink"

CLIENT_SINK_QUEUE = "client_sink_queue"

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

time.sleep(20)

middleware = md.Middleware()

business_city = {}

def start_sink():
	basic_eof ={}
	basic_eof["recived"] = 0
	count = {}
	def callback(ch, method, properties, body):
		recived_list = pickle.loads(body)
		for body in recived_list:
			if(body == "EOF"):

				basic_eof["recived"] = basic_eof["recived"]+1
				if basic_eof["recived"] == N_BASIC_CONSUMERS:
					middleware.send_to_queue(CLIENT_SINK_QUEUE,"count_finished"+"\n"+"count_result: " )
					middleware.send_to_queue(CLIENT_SINK_QUEUE,count )
					middleware.flush()
				return


			body = body.split(",")

			if body[0] in count:
				count[body[0]] = count[body[0]]+int(body[1])
			
			else:
				count[body[0]] = int(body[1])
			
			

	middleware.set_callback_with_ack(callback,BASIC_SINK_QUEUE)

	star_count = {}
	star_eof ={}
	star_eof["recived"] = 0


	def callback(ch, method, properties, body):
		recived_list = pickle.loads(body)
		for body in recived_list:
			if(body == "EOF"):
				star_eof["recived"] = star_eof["recived"]+1
				if star_eof["recived"] == N_STAR_CONSUMERS:
					middleware.send_to_queue(CLIENT_SINK_QUEUE,"star_finished"+"\n"+"star_result: " )
					middleware.send_to_queue(CLIENT_SINK_QUEUE,star_count )
					middleware.flush()
				return

			body = body.split(",")

			if body[0] in star_count:
				star_count[body[0]] = star_count[body[0]]+int(body[1])
			
			else:
				star_count[body[0]] = int(body[1])
			

	middleware.set_callback_with_ack(callback,STAR_SINK_QUEUE)

	text_count = {}
	text_eof ={}
	text_eof["recived"] = 0

	def callback(ch, method, properties, body):
		recived_list = pickle.loads(body)
		for body in recived_list:
			if(body == "EOF"):
				text_eof["recived"] = text_eof["recived"]+1
				if text_eof["recived"] == N_TEXT_CONSUMERS:
					middleware.send_to_queue(CLIENT_SINK_QUEUE,"texts_finished"+"\n"+"texts_result: " )
					middleware.send_to_queue(CLIENT_SINK_QUEUE,text_count )
					middleware.flush()
				return
			body = body.split(",")

			if body[0] in text_count:
				text_count[body[0]] = text_count[body[0]]+int(body[1])
			
			else:
				text_count[body[0]] = int(body[1])
			

	middleware.set_callback_with_ack(callback,TEXT_SINK_QUEUE)

	day_count = {}
	day_eof ={}
	day_eof["recived"] = 0

	def callback(ch, method, properties, body):
		recived_list = pickle.loads(body)
		for body in recived_list:
			if(body == "EOF"):
				day_eof["recived"] = day_eof["recived"]+1
				if day_eof["recived"] == N_DAY_CONSUMERS:
					middleware.send_to_queue(CLIENT_SINK_QUEUE,"day_finished"+"\n"+"day_result: " )
					middleware.send_to_queue(CLIENT_SINK_QUEUE,day_count )
					middleware.flush()
				return

			body = body.split(",")

			if body[0] in day_count:
				day_count[body[0]] = day_count[body[0]]+int(body[1])
			
			else:
				day_count[body[0]] = int(body[1])
			

	middleware.set_callback_with_ack(callback,DAY_SINK_QUEUE)

	business_count = {}
	business_eof ={}
	business_eof["recived"] = 0

	def callback(ch, method, properties, body):
		recived_list = pickle.loads(body)
		for body in recived_list:
			if(body == "EOF"):


				business_eof["recived"] = business_eof["recived"]+1
				if business_eof["recived"] == N_BUSINESS_CONSUMERS:

					ordered_by_value = sorted(business_count.items(), key=lambda item: item[1],reverse = True)
					top_10_citys = {}
					for i in range(0,10):
						if i < len(ordered_by_value):
							top_10_citys[ordered_by_value[i][0]] = ordered_by_value[i][1]

					middleware.send_to_queue(CLIENT_SINK_QUEUE,"business_finished"+"\n"+"business_result: " )
					middleware.send_to_queue(CLIENT_SINK_QUEUE,top_10_citys )
					middleware.flush()
				return
			body = body.split(",")

			#turn business id into city
			if body[0] in business_city:
				body[0] = business_city[body[0]]
			else:
				#if unkonw city, skip
				print("skip_business")
				return

			if body[0] in business_count:
				business_count[body[0]] = int(business_count[body[0]])+int(body[1])
			
			else:
				business_count[body[0]] = int(body[1])
		

	middleware.set_callback_with_ack(callback,BUSINESS_SINK_QUEUE)


def callback(ch, method, properties, body):

	recived_list = pickle.loads(body)
	for body in recived_list:
		if(body == "EOF"):
			start_sink()
			return

		body = body.split(",")

		business_city[body[0]] = body[1]
	


middleware.set_callback_with_ack(callback,PRODUCER_SINK_QUEUE)

middleware.start()