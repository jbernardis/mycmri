import json
import os

class NodeConfig:
	def __init__(self, cfgfn):
		self.cfgfn = cfgfn
		
	def load(self):
		fn = self.cfgfn
		if not os.path.isfile(fn):
			fn = "../%s" % self.cfgfn
			if not os.path.isfile(fn):
				return None
			
		with open(fn, "r") as fp:
			return json.load(fp)
	