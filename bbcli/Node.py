class Node(object):
	def __init__(self, data, children, parent=None):
		self.data = data
		self.children = children
		self.parent = parent
		self.children = children #bool
		# if children is not None:
		# 	for child in children:
		# 		self.add_child(child)
		
	def add_child(self, node):
		assert isinstance(node, Node)
		self.chilren.append(node)

# class Node(object):
#     def __init__(self, data, children=None):
#         self.data = data
#         self.children = []
#         if children is not None:
#         	for child in children:
#                 self.add_child(child)

#     def __repr__(self):
#         return self.name

#     def add_child(self, node):
#     	assert isinstance(node, Node)
# 		self.children.append(node)
