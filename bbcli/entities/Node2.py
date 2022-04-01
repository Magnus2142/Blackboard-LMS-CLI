from collections import defaultdict, deque
from anytree import Node as Nd, RenderTree


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

	def preorder(self, root):
		q = deque([root])
		out = []

		while q:
			cand = q.popleft()
			out.append(cand.data['title'])
			for c in reversed(cand.children):
				q.appendleft(c)
		
		return out
	
				

	def level_order(self, root):
		l = defaultdict(list) 

		# root_node = Nd(root.data['title'], None, None)
		# children = [Nd(child.data['title'], root_node, None) for child in root.children]

		out = []
		def dfs(node):
			if not node: return
			out.append(node)
			for c in node.children:
				dfs(c)


		dfs(root)
			
		for o in out:
			print(o.data['title'])
		
		return root 


		
	# def __str__(self, level=0):
	# 	ret = '\t'*level+self.data['title']+'\n'
	# 	for child in self.children:
	# 		ret += child.__str__(level+1)
	# 	return ret