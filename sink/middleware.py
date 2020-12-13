import pika
import time
import pickle

def make_callback_with_ack(callback):
	def _callback(ch, method, properties, body):
		callback(ch, method, properties, body)
		ch.basic_ack(delivery_tag=method.delivery_tag)
	return _callback

MSG_SIZE = 100

class Middleware():

	def __init__(self):
		self.queues_dic = {}
		self.connection = pika.BlockingConnection(
		    pika.ConnectionParameters(host='rabbitmq'))
		self.channel = self.connection.channel()
		self.lists_dic = {} 
	def send_to_queue(self,name,msg,divide_between_n_queues = 1,divide_key = None):
		if divide_between_n_queues == 1:	
			if name in self.queues_dic:
				self.lists_dic[name].append(msg)
				if( len( self.lists_dic[name] ) == MSG_SIZE):
					self.channel.basic_publish(exchange='', routing_key=name, body=pickle.dumps(self.lists_dic[name]))
					self.lists_dic[name] = []
			else:
				self.lists_dic[name] = []
				
				args = {}
				#args["x-max-length"] = 10
				#args["x-overflow"] = "reject-publish"
				args["x-queue-mode"] = "lazy"
				self.channel.queue_declare(queue=name,arguments= args)
				self.queues_dic[name] = 1
				self.send_to_queue(name,msg)
		else:
			if divide_key == None:
				self.send_to_all(name,msg,divide_between_n_queues)
			else:
				h = hash(divide_key)
				id = h % divide_between_n_queues
				self.send_to_queue(name+str(id),msg)

	def send_to_all(self,name,msg,divide_between_n_queues):
		for i in range (0,int(divide_between_n_queues)):
			self.send_to_queue(name+str(i),msg,1)


	def set_callback(self,callback,name):
		args = {}
		#args["x-max-length"] = 10
		#args["x-overflow"] = "reject-publish"
		args["x-queue-mode"] = "lazy"

		if name in self.queues_dic:
			self.channel.basic_consume(
			    queue=name, on_message_callback=callback,arguments = args)
		else:
			self.channel.queue_declare(queue=name,arguments = args)
			self.queues_dic[name] = 1
			self.set_callback(callback,name)


	def set_callback_with_ack(self,callback,name):
		callback = make_callback_with_ack(callback)
		self.set_callback(callback,name)

	def start(self):
		self.channel.start_consuming()		

	def flush(self):
		for name in self.lists_dic:
			if(len(self.lists_dic[name]) != 0):
				self.channel.basic_publish(exchange='', routing_key=name, body=pickle.dumps(self.lists_dic[name]))
				self.lists_dic[name] = []

	def __del__(self):
		self.flush()
		if(self.connection):
			self.connection.close()