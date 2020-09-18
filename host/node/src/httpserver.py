import select
import queue
from threading import Thread
from socketserver import ThreadingMixIn 
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		app = self.server.getApp()

		parsed_path = urlparse(self.path)
		cmdDict = parse_qs(parsed_path.query)
		
		if "cmd" not in cmdDict or len(cmdDict["cmd"]) == 0:
			self.send_response(400)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(b'missing cmd parameter')
			return

		rc, b = app.dispatch(cmdDict)
		try:
			body = b.encode()
		except:
			body = b

		if rc == 200:
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(body)
		else:
			self.send_response(400)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(body)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	def serve_reprap(self):
		self.haltServer = False
		while self.haltServer == False:
			r = select.select([self.socket], [], [], 1)[0]
			if r:
				self.handle_request()

	def setApp(self, app):
		self.app = app

	def getApp(self):
		return self.app

	def shut_down(self):
		self.haltServer = True

class JMRIHTTPServer:
	def __init__(self, ip, port, httpcmdq, httprespq):
		self.server = ThreadingHTTPServer((ip, port), Handler)
		self.server.setApp(self)
		self.httpcmdq = httpcmdq
		self.httprespq = httprespq
		self.thread = Thread(target=self.server.serve_reprap)
		self.thread.start()

	def getThread(self):
		return self.thread

	def getServer(self):
		return self.server

	def dispatch(self, cmd):
		self.httpcmdq.put(cmd)
		
		try:
			rc, body = self.httprespq.get(True, 10)
		except queue.Empty:
			rc = 400
			body = b'bad request'

		return rc, body

	def close(self):
		self.server.shut_down()

