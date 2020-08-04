class NodeException(Exception):
	def __init__(self, message):
		self.message = message

class NodeParameterException(Exception):
	def __init__(self, message):
		self.message = message

class NodeNotConnected(Exception):
	pass

class NodeReadException(Exception):
	pass

class NodeAddressException(Exception):
	def __init__(self, badaddr, addr):
		self.badaddr = badaddr
		self.addr = addr

