class Node(object):
	def __init__(self, data, has_children, parent=None):
		self.data = data
		self.has_children = has_children #bool
		self.parent = parent
		# if children is not None:
		# 	for child in children:
		# 		self.add_child(child)
		
	def add_child(self, node):
		assert isinstance(node, Node)
		self.chilren.append(node)