# Implementation of the breath first search (BFS) algorithm 
# BFS searches the shallowest nodes first, only moving deeper once all from a given depth have been explored
# Takes in a graph, start vertex and goal vertex and finds a path from the start vertex to the goal vertex
# Returns the path and cost

from Graphs import Graph, loadGraph

def breadthFirstSearch(graph, start, goal):
	"""Given a graph, start node and goal node, this function returns a solution path and cost"""

	frontier = [start]
	explored = []
	paths = {start : [start]}
	solution = None

	# While the frontier is not empty, until the goal is reached
	while solution is None:

		if len(frontier) == 0:
			raise Exception(f"No path exists between {start} and {goal}")

		# Get the next vertex to explore
		vertex = frontier.pop(0)

		# For each edge of the vertex
		for child in graph.edgesOf(vertex):

			# If the vertex has not yet been discovered and the edge is not a loop
			if child != vertex and child not in frontier and child not in explored:

				# If we have reached the goal vertex then break the loop
				if child == goal:

					solution = paths[vertex] + [child]
								
					# Calculate the cost of the path
					cost = 0
					for i in range(len(solution)-1):
						cost += graph.edgeWeight(solution[i], solution[i+1])

					return (solution, cost)

				# Add itself to the frontier and store its path
				frontier.append(child)
				paths[child] = paths[vertex] + [child]

		# Move the current vertex to explored
		explored.append(vertex)

if __name__ == '__main__':
	
	graph = loadGraph()

	print("Start vertex?")
	start = input("")
	print("Goal vertex?")
	goal = input("")

	print(breadthFirstSearch(graph, start, goal))















