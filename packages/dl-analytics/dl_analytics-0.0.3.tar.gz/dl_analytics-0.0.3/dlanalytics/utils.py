import numpy as np
import json

class NpEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.integer):
			return int(obj)
		elif isinstance(obj, np.floating):
			return float(obj)
		elif isinstance(obj, np.ndarray):
			return obj.tolist()
		else:
			return super(NpEncoder, self).default(obj)

class Stats(object):
	def __init__(self, d):
		self.dict = d
	def __str__(self):
		return str(self.dict)

def dict2obj(d):
	if isinstance(d, list):
		d = [dict2obj(x) for x in d]
	if not isinstance(d, dict):
		return d
	
	o = Stats(d)
	for k in d:
		o.__dict__[k] = dict2obj(d[k])
	return o