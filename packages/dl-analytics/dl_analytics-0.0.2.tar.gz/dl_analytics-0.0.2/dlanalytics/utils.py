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