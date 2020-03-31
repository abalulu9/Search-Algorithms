# An implementation of the depth first search (DFS) algorithm
# DFS examines the deepest nodes first
# Takes in a graph, start vertex and goal vertex and finds a path from the start vertex to the goal vertex
# Returns the path and cost

from Graphs import Graph, loadGraph
from math import inf


def depthFirstSearch(graph, start, goal, limit = inf):

	frontier = [(start, 0)]
	explored = []
	paths = {start : [start]}

	# while the frontier is not empty, until the goal is reached
	while True:

		if len(frontier) == 0:
			raise Exception(f"No path exist between {start} and {goal} with a depth limit of {limit}")

		# get the next vertex to explore
		vertex, depth = frontier.pop()

		if depth < limit:

			# for each edge of the vertex
			for child in graph.edgesOf(vertex):

				# if the vertex has not yet been discovered
				if child != vertex and child not in [f[0] for f in frontier] and child not in explored:

					# if we have reached the goal vertex then break the loop
					if child == goal:

						solution = paths[vertex] + [child]
									
						cost = 0
						for i in range(len(solution)-1):
							cost += graph.edgeWeight(solution[i], solution[i+1])

						return (solution, cost)

					# add itself to the frontier and store its path
					frontier.append((child, depth + 1))
					paths[child] = paths[vertex] + [child]

		explored.append(vertex)

if __name__ == '__main__':
	
	graph = loadGraph()

	print("Start vertex?")
	start = input("")
	print("Goal vertex?")
	goal = input("")
	print("Limit the depth of the search? enter 0 for no limit")
	limit = int(input(""))
	if limit == 0:
		limit = inf
	

	print(depthFirstSearch(graph, start, goal, limit))


