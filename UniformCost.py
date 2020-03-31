# Implementation of the uniform cost search (UCS) algorithm 
# The frontier is ordered so that the vertex with the lowest path cost is searched first
# Takes in a graph, start vertex and goal vertex and finds a path from the start vertex to the goal vertex
# Returns the path and cost

from Graphs import Graph, loadGraph

def uniformCostSearch(graph, start, goal):

	frontier = [(start, 0)]
	explored = []
	paths = {start : [start]}

	# While the frontier is not empty, until the goal is reached
	while True:


		if len(frontier) == 0:
			raise Exception(f"No path from {start} to {goal}")

		frontier.sort(key=lambda tup: tup[1], reverse = False)

		# Get the next vertex to explore and it's cost
		vertex, cost = frontier.pop(0)

		if vertex == goal:
			return paths[vertex], cost

		# For each edge of the vertex
		for child in graph.edgesOf(vertex):

			# If the vertex has not yet been explored and the edge is not a loop
			if child != vertex and child not in explored:

				# If the child is in the frontier check if there is a cheaper path to it
				if child in [f[0] for f in frontier]:				

					oldChildValue = dict(frontier)[child]
					newChildValue = cost + graph.edgeWeight(vertex, child)

					# If the new cost is less than the current cost replace the child vertex in the frontier
					if newChildValue < oldChildValue:

						frontier.remove((child, oldChildValue))
						frontier.append((child, newChildValue))
						paths[child] = paths[vertex] + [child]

				else:

					# Add the child vertex to the frontier and store its path
					frontier.append((child, cost + graph.edgeWeight(vertex, child)))
					paths[child] = paths[vertex] + [child]

		explored.append(vertex)




if __name__ == '__main__':

	graph = loadGraph()

	print("Start vertex?")
	start = input("")
	print("Goal vertex?")
	goal = input("")

	print(uniformCostSearch(graph, start, goal))