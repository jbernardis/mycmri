class NodeException(Exception):
	def __init__(self, message):
		self.message = message

class BusNotConnected(Exception):
	pass

class BusReadException(Exception):
	pass

class BusTimeoutException(Exception):
	pass
		
		
