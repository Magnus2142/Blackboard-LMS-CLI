class Node2:
	def __init__(self, data, children=[]):
		self.data = data
		self.children = children

	def __str__(self, level=0):
		ret = '\t'*level+self.data['title']+'\n'
		for child in self.children:
			ret += child.__str__(level+1)
		return ret