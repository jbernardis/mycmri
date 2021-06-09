import json
import os

class NodeConfig:
	def __init__(self, folder, cfgfn):
		self.cfgfn = cfgfn
		self.cfgfolder = folder
		
	def load(self):
		fn = os.path.join(self.cfgfolder, self.cfgfn)
		if not os.path.isfile(fn):
			fn = os.path.join(self.cfgfolder, "..", self.cfgfn)
			if not os.path.isfile(fn):
				return None
			
		with open(fn, "r") as fp:
			return json.load(fp)
	