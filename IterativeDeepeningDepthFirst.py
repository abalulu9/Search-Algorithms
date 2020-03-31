# Implementation of the iterative deepending depth first search (IDDF) algorithm
# IDDF performs limited depth first with an increasing depth limit
# Takes in a graph, start vertex and goal vertex and finds a path from the start vertex to the goal vertex
# Returns the path and cost

from Graphs import Graph, loadGraph
from DepthFirst import depthFirstSearch

def iterativeDeepeningDepthFirstSearch(graph, start, goal):

	limit = 1
	noVertices = graph.noVertices

	# Increment the limit while it is less than the total number of vertices in the graph
	while limit < graph.noVertices:

		# Perform depth first search with the current limit and return the solution and cost is found
		# If a solution is not found it throws an exception
		try:
			return depthFirstSearch(graph, start, goal, limit)

		# Increment the limit
		except:
			limit += 1

	raise Exception(f"No path exists between {start} and {goal}")

if __name__ == '__main__':
	
	graph = loadGraph()

	print("Start vertex?")
	start = input("")
	print("Goal vertex?")
	goal = input("")

	print(iterativeDeepeningDepthFirstSearch(graph, start, goal))