from collections import defaultdict, deque
from anytree import Node as Nd


class Node:
	def __init__(self, data):
		self.data = data
		self.parent = None
		self.children = [] 

	def add_child(self, obj):
		self.children.append(obj)
		obj.parent = self

	def preorder(self):
		root = self

		root_node = Nd(root.data['id'] + ' ' + root.data['title'])
		def dfs(node: Node, root_node: Nd, parent: Nd) -> None:
			if not node: return
			elif parent is None:
				parent = root_node
			else:
				nd = Nd(node.data['id'] + ' ' + node.data['title'], parent)
				parent = nd
			for c in node.children:
				dfs(c, root_node, parent)

		dfs(root, root_node, None)
		return root_node 
	
	def is_folder(node):
		key = 'contentHandler'
		from bbcli.utils.content_handler import content_handler
		return key in node.data and node.data[key]['id'] == content_handler['folder']

	# This is only getting folders. 
	def preorder2(self):
		root = self
		root_node = Nd(root.data['title'])	
		def dfs(node, root_node, parent):
			if not node: return
			elif parent is None:
				parent = root_node
			elif len(node.children) == 0 and Node.is_folder(node):
				# print("children0", node.data['title'])
				node.parent.children.remove(node)
			else:
				nd = Nd(node.data['title'], parent)
				parent = nd
			for c in node.children:
				dfs(c, root_node, parent)

		if len(root.children) == 0 and Node.is_folder(root):
			return None
		else:
			dfs(root, root_node, None)
			return root_node
		

	def __str__(self, level=0):
		ret = '\t'*level+self.data['title']+'\n'
		for child in self.children:
			ret += child.__str__(level+1)
		return ret
