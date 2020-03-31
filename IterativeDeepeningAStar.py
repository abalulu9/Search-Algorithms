# An implementation of the iterative deepening A* (IDA*) search algorithm
# IDA* performs A* search with a limit on the (cost + heuristic)
# Takes in a graph, start vertex, goal vertex and heuristic function and finds a path from the start vertex to the goal vertex
# The heuristic function must take (vertex, graph, start, goal) as its arguments
# Returns the path and cost

from Graphs import Graph, loadGraph
from AStar import AStarSearch

def iterativeDeepeningAStarSearch(graph, start, goal, heuristic):

	limit = 1
	totalWeight = graph.totalWeight

	# Increment the limit value until it reaches the total weight of the graph
	while limit < graph.totalWeight:

		# Perform A* with the current limit and return the solution and cost if found
		# If a solution is not found it throws an exception
		try:
			return AStarSearch(graph, start, goal, heuristic, limit)


		# Increment the limit
		except:
			limit += 1

	raise Exception(f"No path exists between {start} and {goal}")

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

	print(iterativeDeepeningAStarSearch(graph, start, goal, heuristic))