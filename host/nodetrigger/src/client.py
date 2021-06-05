#!/usr/bin/env python3

from listener import Listener
from railroad import Railroad
from server import Server

import json
import queue
import evaluate
			
class ReportQueue:
	def __init__(self, rr):
		self.railroad = rr
				
		self.msgQ = queue.Queue(0)
		self.listener = Listener(self, "192.168.1.142", "8001", self.msgQ)
		self.listener.start()
		
	def serve_forever(self):
		self.forever = True
		while self.forever:
			try:
				msg = self.msgQ.get(True, 0.25)
			except queue.Empty:
				msg = None
			
			if msg:
				#print("(%s)" % msg)
				jdata = json.loads(msg)
							
				if "disconnect" in jdata.keys():
					self.forever = False
					
				else:
					self.railroad.processMsg(jdata)
					
		self.listener.kill()
		self.listener.join()

server = Server()
server.setServerAddress("192.168.1.142", "8000")

rr = Railroad(server)
evaluate.initialize(rr)  # initialize the expression evaluator

rptq = ReportQueue(rr)
rptq.serve_forever()

