class Node2:
	def __init__(self, data):
		self.data = data
		self.parent = None
		self.children = [] 

	def add_child(self, obj):
		self.children.append(obj)
		obj.parent = self.data

	# __repr__ is a way to represent a class object as a string
	# def __repr__(self):
	# 	if self.children:
	# 		out = repr(self.data['title']) + " ↴" + "\n"
	# 		indent = "    "
	# 		for child in self.children:
	# 			for line in repr(child).splitlines():
	# 				out += indent + line + "\n"
	# 		return out
	# 	else:
	# 		return repr(self.data['title'])
				


	def __str__(self, level=0):
		ret = '\t'*level+self.data['title']+'\n'
		for child in self.children:
			ret += child.__str__(level+1)
		return ret