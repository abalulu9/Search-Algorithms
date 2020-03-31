# Implementation of the A* search algorithm
# The frontier is ordered so that the vertex with the lowest sum of cost and heuristic is explored next
# Takes in a graph, start vertex, goal vertex and heuristic function and finds a path from the start vertex to the goal vertex
# The heuristic function must take (vertex, graph, start, goal) as its arguments
# Returns the path and cost

from Graphs import Graph, loadGraph
from math import inf 

def AStarSearch(graph, start, goal, heuristic, limit = inf):

	# frontier is stored as tuples (vertex, path cost, heuristic cost)
	frontier = [(start, 0, heuristic(start, graph, start, goal))]
	explored = []
	paths = {start : [start]}

	while True:

		if len(frontier) == 0:
			raise Exception(f"No path from {start} to {goal}")

		# Sort the frontier into ascending order given the sum of path cost to a vertex and the heuristic function of that vertex
		frontier.sort(key=lambda tup: tup[1] + tup[2])

		vertex, cost, h = frontier.pop(0)

		# If the path cost + heuristic doesn't exceed the limit
		if cost + h <= limit:

			# If at the goal vertex return the path and cost
			if vertex == goal:

				return (paths[vertex], cost)

			# For each child vertex of the given vertex
			for child in graph.edgesOf(vertex):

				# If the edge isn't a loop and the child vertex hasn't been seen seen before 
				if child != vertex and child not in [f[0] for f in frontier] and child not in explored:

					# Append the child vertex to the frontier and store it's path 
					frontier.append((child, cost + graph.edgeWeight(vertex, child), heuristic(child, graph, start, goal)))
					paths[child] = paths[vertex] + [child]

		# Add the vertex to the explored list
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
	print("Limit the total cost of the path? enter 0 for no limit")
	limit = int(input(""))
	if limit == 0:
		limit = inf	

	print(AStarSearch(graph, start, goal, heuristic, limit))