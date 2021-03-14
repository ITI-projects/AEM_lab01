from operator import itemgetter
from preparedata import shortest_next
import numpy as np


class RegretHeuristics:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix

    def length_gain(self, vertex_a, vertex_b, new_vertex):
        # Cost = Cost_after - Cost_before
        return self.distance_matrix[vertex_a, new_vertex] + self.distance_matrix[vertex_b, new_vertex] - \
               self.distance_matrix[vertex_a, vertex_b]

    def search_for_best_vertex(self, unchecked_vertex, visited_vertexes, j):
        list_tuples_vertex_length = []
        for u in unchecked_vertex:
            x = self.length_gain(visited_vertexes[j], visited_vertexes[j + 1], u)
            list_tuples_vertex_length.append((u, x))
        vertex_with_min_length = min(list_tuples_vertex_length, key=itemgetter(1))[0]
        min_length = min(list_tuples_vertex_length, key=itemgetter(1))[1]
        if j < 0:
            return (len(visited_vertexes) - 1, j + 1), (min_length, vertex_with_min_length)
        return (j, j + 1), (min_length, vertex_with_min_length)

    def search_for_best_edge(self, visited_vertexes, vertex_with_biggest_regret):
        min_cost = max(self.distance_matrix[visited_vertexes[0]]) + max(self.distance_matrix[visited_vertexes[1]])
        index_to_insert = 0

        for x in range(len(visited_vertexes)-1):
            cost = self.length_gain(visited_vertexes[x], visited_vertexes[x+1], vertex_with_biggest_regret)
            if cost < min_cost:
                min_cost = cost
                index_to_insert = x
        cost = self.length_gain(visited_vertexes[len(visited_vertexes)-1], visited_vertexes[0], vertex_with_biggest_regret)

        if cost < min_cost:
            index_to_insert = x
        return index_to_insert + 1

    def calculate_distance(self, visited_vertexes):
        sum_of_distance = 0
        for i in range(len(visited_vertexes) - 1):
            sum_of_distance += self.distance_matrix[visited_vertexes[i]][visited_vertexes[i + 1]]
        sum_of_distance += self.distance_matrix[visited_vertexes[-1]][visited_vertexes[0]]
        return sum_of_distance

    def run(self, starting_vertex):
        vertexes = int(self.distance_matrix.shape[0] / 2)
        visited_vertexes = [starting_vertex, shortest_next(self.distance_matrix,
                                                           [starting_vertex], starting_vertex)]

        unchecked_vertex = [e for e in range(len(self.distance_matrix)) if e not in visited_vertexes]

        _, (_, best_vertex) = self.search_for_best_vertex(unchecked_vertex, visited_vertexes, 0)
        visited_vertexes.insert(1, best_vertex)

        for i in range(0, vertexes - 3):
            unchecked_vertex = [e for e in range(len(self.distance_matrix)) if e not in visited_vertexes]

            best_value_for_next_cycle = []

            for e in unchecked_vertex:
                vertex_distance_to_edges = []
                for x in range(len(visited_vertexes)-1):
                    cost = self.length_gain(visited_vertexes[x], visited_vertexes[x+1], e)
                    vertex_distance_to_edges.append(cost)
                cost = self.length_gain(visited_vertexes[-1], visited_vertexes[0], e)
                vertex_distance_to_edges.append(cost)
                best_value_for_next_cycle.append(vertex_distance_to_edges)

            for x in best_value_for_next_cycle:
                x.sort()

            list_regrets = []
            for x in range(len(unchecked_vertex)):
                list_regrets.append(best_value_for_next_cycle[x][1] - best_value_for_next_cycle[x][0])

            vertex_with_biggest_regret = np.argmax(np.array(list_regrets))
            vertex_with_biggest_regret = unchecked_vertex[vertex_with_biggest_regret]

            visited_vertexes.insert(self.search_for_best_edge(visited_vertexes, vertex_with_biggest_regret), vertex_with_biggest_regret)
        return self.calculate_distance(visited_vertexes), visited_vertexes
