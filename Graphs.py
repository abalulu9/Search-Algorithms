# The graphs used by the search algorithms
# All edges are directional
# Loops from a vertex to the same vertex are allowed
# Multiple edges between two nodes are not allowed 

from random import randint
import json

def loadGraph():

	print("Please enter the destination of the graph to use, or 0 for a random graph")
	filePath = input("")

	graph = None

	if filePath != '0':

		with open(filePath, 'r') as fp:
			graph = Graph(json.load(fp))

	else:

		print("How many vertices?")
		noVertices = int(input(""))
		print("How many edges?")
		noEdges = int(input(""))
		print("Minimum edge weight?")
		weightMinimum = int(input(""))
		print("Maximum edge weight?")
		weightMaximum = int(input(""))

		graph = Graph()
		graph.randomlyGenerate(noVertices, noEdges, weightMinimum, weightMaximum)

	return graph

class Graph():
	
	def __init__(self, graphDict = None):
		"""
		Creates a new graph and stores the graph dictionary
		The graph dictionary should be of type:
			{'a' : {'b' : 10, 'c' : 5},
			 'b' : {'a' : 10},
			 'c' : {'a' : 5}}
		Also generates the edges of the graph and test whether the graph is bidirectional
		"""

		if graphDict is not None:
			self.graphDict = graphDict
			self.generateEdges()

		else:
			self.graphDict = {}

		self.testBidirectional()

	def testBidirectional(self):
		"""Tests whether the graph is bidirectional, returns True or False"""

		# Assume it is bidirectional
		self.bidirectional = True

		# For each edge
		for vertex in self.vertices:
			for edge in self.edgesOf(vertex):

				# If opposite direction edge doesn't exist set bidirectional to false and double break from the loop
				if vertex not in self.edgesOf(edge):
					self.bidirectional = False
					break

			if self.bidirectional == False:
				break

	def randomlyGenerate(self, noVertices, noEdges, weightMinimum, weightMaximum, bidirectional = False):
		"""
		Randomly generate a graph with the given noVertices and noEdges
		The weight of each edge is in the closed interval [weightMinimum, weightMaximum]
		"""

		if noVertices == 0:
			raise Exception("Graph must contain at least one vertex")

		# Return None if there are too many edges to fit in the graph without repeating an edge
		if noEdges > noVertices ** 2:
			raise Exception("Too many edges to fit into graph")

		self.graphDict = {str(i) : {} for i in range(noVertices)}

		iterator = iter(range(noEdges))

		# Iterate over the total number of edges
		for i in iterator:

			while True:

				# Randomly select a vertex
				vertex = str(randint(0, noVertices-1))

				# Randomly select an edge destination, if bidirectional and the last edge then a loop must be created
				if int(i) == noEdges - 1:
					edge = vertex
				else:
					edge = str(randint(0, noVertices-1))

				# If the edge doesn't already exist
				if edge not in self.graphDict[vertex].keys():

					# Randomly select an edge weight
					self.graphDict[vertex][edge] = randint(weightMinimum, weightMaximum)

					if bidirectional and vertex != edge:

						# Create the edge in the opposite direction with the same weight
						self.graphDict[edge][vertex] = self.graphDict[vertex][edge]

						# Force a double increment in the iterator as two edges were created
						next(iterator, None)

					break

		self.generateEdges()

		self.bidirectional = bidirectional

	def transformIntoBidirectional(self):
		"""
		Tranform the graph into a bidrectional one
		If two nodes already share one edge then the edge in the opposite direction will have the same weight
		If two nodes already share two edges then the weights will remain as they were originally
		"""

		# If not already bidirectional
		if not self.bidirectional:

			# For each edge
			for vertex, edgeDict in self.graphDict.items():
				for edge, weight in edgeDict.items():

					# If the opposite direction edge doesn't already exist
					if vertex not in self.graphDict[edge].keys():

						# Add the opposite direction edge
						self.graphDict[edge][vertex] = weight
					
			self.generateEdges()

	@property
	def vertices(self):
		"""Return a list of the vertices"""
		return list(self.graphDict.keys())

	def degreeOf(self, vertex, inOutBoth = "BOTH"):
		"""
		Get the degree of a vertex
		inOutBoth specifies whether to assess just edges into or out of a vertex, or both
		"""

		# If the vertex exists
		if vertex in self.vertices:

			if inOutBoth == "OUT":
				return len(self.graphDict[vertex])

			elif inOutBoth == "IN":
				count = 0
				for v in self.graphDict.values():
					if vertex in v.keys():
						count += 1

				return count 

			elif inOutBoth == "BOTH":
				if self.bidirectional: return self.degreeOf(vertex, "OUT")
				else: return self.degreeOf(vertex, "OUT") + self.degreeOf(vertex, "IN") 

		else:
			raise Exception("Vertex not in graph")

	def generateEdges(self):
		"""
		Generate the edges of the graph
		Each bidirectional edge will appear twice in the list, for example ('a', 'b') and ('b', 'a')
		However unidirectional edges will appear only once
		"""

		self.edges = []

		for vertex in self.graphDict.keys():
			for edge in self.graphDict[vertex].keys():
				self.edges.append((vertex, edge))

	def edgeWeight(self, vertex, edge):
		"""Get the weight of an edge from vertex to edge"""

		try:
			return self.graphDict[vertex][edge]
		except IndexError:
			raise Exception("No such edge")

	def edgesOf(self, vertex):
		"""Get a list of all the destinations of the edges leaving a vertex"""

		# if the vertex exists
		if vertex in self.vertices:
			return list(self.graphDict[vertex].keys())
		else:
			raise Exception("No such vertex")

	def sortedEdgesOf(self, vertex):
		"""Get a list of all the destinations of the edges leaving a vertex, ordered by ascending edge weight"""

		# If the vertex exists
		if vertex in self.vertices:
			return list({k: v for k, v in sorted(self.graphDict[vertex].items(), key=lambda item: item[1])}.keys())
		else:
			raise Exception("No such vertex")

	@property
	def noVertices(self):
		"""The number of vertices in the graph"""
		return len(self.vertices)

	@property
	def noEdges(self):
		"""
		The number of edges in the graph
		Bidirectional edges will be counted twice
		"""
		return len(self.edges)

	def addVertex(self, vertex, edges):
		"""
		Check that the vertex is not already in the graph
		Check that the edge destinations are all in the graph
		Add the new vertex to the graph dictionary
		Regenerate the edges
		"""

		if vertex not in self.graphDict.keys():
			if all(edge in self.graphDict.keys() or edge == vertex for edge in edges.keys()):
				self.graphDict[vertex] = edges
				for edge in edges.keys():
					self.graphDict[edge][vertex] = edges[edge]

				self.generateEdges()
			else:
				raise Exception("Edge destination not in graph")
		else:
			raise Exception("Vertex already in graph")

	def addEdge(self, vertex1, vertex2, weight, bidrectional = False):
		"""
		Add an edge from vertex1 to vertex2 with the given weight
		If bidirectional is true then an edge will also be added from vertex2 to vertex1 with the same weight
		"""

		# If both vertices exist
		if vertex1 in self.vertices and vertex2 in self.vertices:

			self.graphDict[vertex1][vertex2] = weight

			if bidrectional:
				self.graphDict[vertex2][vertex1] = weight
			
			self.generateEdges()

	def removeVertex(self, vertex):
		"""Remove a given vertex from the graph"""

		# Remove any edges going into the vertex
		for v in self.vertices:
			if v != vertex:
				try:
					del self.graphDict[v][vertex]
				except:
					pass

		# Remove the vertex itself
		del self.graphDict[vertex]

		self.generateEdges()

	def removeEdge(self, vertex, edgeDestination):
		"""
		Remove the edge from vertex to edgeDestination
		If the edge does not exist it will print "No such edge"
		"""

		try:
			del self.graphDict[vertex][edgeDestination]
			self.generateEdges()
		except:
			raise Exception("No such edge")

	def __str__(self):
		return f"A graph with {self.noVertices} vertices and {self.noEdges} edges"
	





