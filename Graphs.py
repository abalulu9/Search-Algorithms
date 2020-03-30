# The graphs used by the search algorithms
# All edges are directional
# Loops from a vertex to the same vertex are allowed
# Multiple edges between two nodes are not allowed 

from random import randint



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

		# assume it is bidirectional
		self.bidirectional = True

		# for each edge
		for vertex in self.vertices:
			for edge in self.edgesOf(vertex):

				# if opposite direction edge doesn't exist set bidirectional to false and double break from the loop
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

		self.graphDict = {i : {} for i in range(noVertices)}

		iterator = iter(range(noEdges))

		# Iterate over the total number of edges
		for i in iterator:

			while True:

				# randomly select a vertex
				vertex = randint(0, noVertices-1)

				# randomly select an edge destination, if bidirectional and the last edge then a loop must be created
				if i == noEdges - 1:
					edge = vertex
				else:
					edge = randint(0, noVertices-1)

				# if the edge doesn't already exist
				if edge not in self.graphDict[vertex].keys():

					# randomly select an edge weight
					self.graphDict[vertex][edge] = randint(weightMinimum, weightMaximum)

					if bidirectional and vertex != edge:

						# create the edge in the opposite direction with the same weight
						self.graphDict[edge][vertex] = self.graphDict[vertex][edge]

						# force a double increment in the iterator as two edges were created
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

		# if not already bidirectional
		if not self.bidirectional:

			# for each edge
			for vertex, edgeDict in self.graphDict.items():
				for edge, weight in edgeDict.items():

					# if the opposite direction edge doesn't already exist
					if vertex not in self.graphDict[edge].keys():

						# add the opposite direction edge
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

		# if the vertex exists
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

		# if the vertex exists
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
		if bidirectional is true then an edge will also be added from vertex2 to vertex1 with the same weight
		"""

		# if both vertices exist
		if vertex1 in self.vertices and vertex2 in self.vertices:

			self.graphDict[vertex1][vertex2] = weight

			if bidrectional:
				self.graphDict[vertex2][vertex1] = weight
			
			self.generateEdges()

	def removeVertex(self, vertex):
		"""remove a given vertex from the graph"""

		# remove any edges going into the vertex
		for v in self.vertices:
			if v != vertex:
				try:
					del self.graphDict[v][vertex]
				except:
					pass

		# remove the vertex itself
		del self.graphDict[vertex]

		self.generateEdges()

	def removeEdge(self, vertex, edgeDestination):
		"""
		remove the edge from vertex to edgeDestination
		if the edge does not exist it will print "No such edge"
		"""

		try:
			del self.graphDict[vertex][edgeDestination]
			self.generateEdges()
		except:
			raise Exception("No such edge")

	def __str__(self):
		return f"A graph with {self.noVertices} vertices and {self.noEdges} edges"
	







#### TEST ####

if __name__ == '__main__':

	from datetime import datetime as dt 

	graph = Graph()

	start = dt.now()

	graph.randomlyGenerate(10, 50, 1, 10, False)

	print("Time taken to generate:", (dt.now() - start).microseconds)

	print(graph.edges)
	# print(graph.bidirectional)
	print("Edges:", graph.noEdges)

	graph.removeEdge(graph.edges[0][0], graph.edges[0][1])

	print(graph.edges)
	print(graph.noVertices)

	graph.removeVertex(0)

	print(graph.noVertices)
	print(graph.edges)

	print("")

	print(graph.graphDict)
