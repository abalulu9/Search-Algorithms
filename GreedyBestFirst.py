# An implementation of the greedy best first search (GBFS) algorithm
# Explores the node that is the closest to the goal, in terms of the heuristic function
# Takes in a graph, start vertex, goal vertex and heuristic function and finds a path from the start vertex to the goal vertex
# The heuristic function must take (vertex, graph, start, goal) as its arguments
# Returns the path and cost

from Graphs import Graph, loadGraph

from datetime import datetime as dt 
from time import sleep

def greedyBestFirstSearch(graph, start, goal, heuristic):

	frontier = [(start, heuristic(start, graph, start, goal))]
	explored = []
	paths = {start : [start]}

	# While the frontier is not empty, until the goal has been found
	while True:

		if len(frontier) == 0:
			raise Exception(f"No path exists between {start} and {goal}")

		# Sort by the heuristic cost of each vertex
		frontier.sort(key=lambda tup: tup[1])

		# Get the next vertex to explore
		vertex = frontier.pop(0)[0]

		# If the vertex is the goal
		if vertex == goal:

			# Calculate the cost of the path
			cost = 0
			for i in range(len(paths[vertex])-1):
				cost += graph.edgeWeight(paths[vertex][i], paths[vertex][i+1])

			return (paths[vertex], cost)

		# For each edge of the vertex
		for child in graph.edgesOf(vertex):

			# If the child has not been discovered and the edge is not a loop
			if child != vertex and child not in [f[0] for f in frontier] and child not in explored:

				# Add the child to the frontier and store it's path
				frontier.append((child, heuristic(child, graph, start, goal)))
				paths[child] = paths[vertex] + [child]

		explored.append(vertex)

def heuristic(vertex, graph, start, goal):
	"""
	The heuristic function to be used by the algorithm
	Redefine this as needed
	"""
	
	return abs(int(vertex) - int(goal))

if __name__ == '__main__':

	graph = loadGraph()

	print("Start vertex?")
	start = input("")
	print("Goal vertex?")
	goal = input("")

	print(greedyBestFirstSearch(graph, start, goal, heuristic))