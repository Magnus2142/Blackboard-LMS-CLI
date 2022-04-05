from collections import defaultdict, deque
from anytree import Node as Nd


class Node:
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

 
	def levelorder(self, root):
		if not root: return []
		res, queue = [], [root]
		while queue:
			# res.extend([node.data['title'] for node in queue])
			res.extend([node for node in queue])
			level = []
			for node in queue:
				level.extend(node.children)
			queue = level
		return res

	def preorder(self, root):
		q = deque([root])
		out = []

		while q:
			cand = q.popleft()
			out.append(cand.data['title'])
			for c in reversed(cand.children):
				q.appendleft(c)
		
		return out
	
				

	# It's working bby
	def preorder(self, root):
		# l = defaultdict(list) # it is level order when you use dict
		# folder_ids = dict()

		root_node = Nd(root.data['title'])
		def dfs(node, root_node, parent):
			if not node: 
				parent = Nd(node.parent.parent['title']) 
				return
			elif parent is None:
				parent = root_node
			else:
				nd = Nd(node.data['title'], parent)
				parent = nd
			# if len(node.children) > 0: 
				# folder_ids[node.data['title']] = node.data['id'] 
			for c in node.children:
				dfs(c, root_node, parent)

		dfs(root, root_node, None)
		return root_node 
		

	def inorder(self, root):
		out = []
		def dfs(node):
			if not node: return
			sz = len(node.children)
			for i in range(sz-1): # loop through everything except the last child
				dfs(node.children[i])
			out.append(node.data['title'])
			dfs(node.children[-1]) # loop through the last node

		dfs(root)
		return out
	
	def postorder1(self, root):
		out = []
		def dfs(node):
			if not node: return
			for child in node.children:
				dfs(child)
			out.append(node.data['title'])
		dfs(root)
		return out

	def postorder2(self, root):
		if not root:
			return []
		result, stack = [], [root]
		while stack:
			node = stack.pop()
			result.append(node.data['title'])
			for child in node.children:
				if child:
					stack.append(child)
		return result[::-1]


	def __str__(self, level=0):
		ret = '\t'*level+self.data['title']+'\n'
		for child in self.children:
			ret += child.__str__(level+1)
		return ret
