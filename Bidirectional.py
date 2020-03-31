# An implementation of the bidirectional search algorithm
# Bidirectional search acts like two uniform cost searchs, one in each direction (goal -> start), (start -> goal)
# Takes in a graph, start vertex and goal vertex and finds a path from the start vertex to the goal vertex
# Returns the path and cost

from Graphs import Graph, loadGraph

def bidirectionalSearch(graph, start, goal):

	# Check that the graph is bidirectional
	if graph.bidirectional is False:
		print("Graph must be bidirectional")
		return None

	frontier = {0 : [(start, 0)], 1 : [(goal, 0)]}
	explored = {0 : [], 1 : []}
	paths = {0 : {start : [start]}, 1 : {goal : [goal]}}

	# while the frontier is not empty, until the goal is reached
	while True:

		# For each direction
		for i in [0, 1]:

			# If either frontier is empty then failure
			if len(frontier[0]) == 0 or len(frontier[1]) == 0:
				raise Exception(f"No path exists between {start} and {goal}")

			# Sort the current frontier by cost
			frontier[i].sort(key=lambda tup: tup[1], reverse = False)

			# Get the next vertex to explore
			vertex, cost = frontier[i].pop(0)

			# If the vertex is in the opposing direction frontier
			if vertex in [f[0] for f in frontier[(i + 1) % 2]]:
				# Calculate and return the full path and cost 
				return paths[0][vertex] + list(reversed(paths[1][vertex][:-1])), cost + dict(frontier[(i + 1) % 2])[vertex]

			# For each edge of the vertex
			for child in graph.edgesOf(vertex):

				# If the vertex has not yet been discovered
				if child != vertex and child not in explored[i]:

					# If the child is in the frontier
					if child in [f[0] for f in frontier[i]]:				

						oldChildValue = dict(frontier[i])[child]
						newChildValue = cost + graph.edgeWeight(vertex, child)

						# If the new cost is less than the current cost
						if newChildValue < oldChildValue:

							frontier[i].remove((child, oldChildValue))
							frontier[i].append((child, newChildValue))

					else:

						# Add itself to the frontier and store its path
						frontier[i].append((child, cost + graph.edgeWeight(vertex, child)))
						paths[i][child] = paths[i][vertex] + [child]

			explored[i].append(vertex)

if __name__ == '__main__':

	graph = loadGraph()

	print("Start vertex?")
	start = input("")
	print("Goal vertex?")
	goal = input("")

	print(bidirectionalSearch(graph, start, goal))