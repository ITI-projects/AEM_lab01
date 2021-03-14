from preparedata import shortest_next, PrepareData
import numpy as np
from operator import itemgetter


class GreedyCycleAlgorithm:

    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix

    def length_gain(self, vertex_a, vertex_b, new_vertex):
        # Cost = Cost_after - Cost_before
        return self.distance_matrix[vertex_a, new_vertex] + self.distance_matrix[new_vertex, vertex_b] - \
               self.distance_matrix[vertex_a, vertex_b]

    def search(self, unchecked_vertex, visited_vertexes, j):
        list_tuples_vertex_length = []
        for u in unchecked_vertex:
            x = self.length_gain(visited_vertexes[j], visited_vertexes[j + 1], u)
            list_tuples_vertex_length.append((u, x))
        vertex_with_min_length = min(list_tuples_vertex_length, key=itemgetter(1))[0]
        min_length = min(list_tuples_vertex_length, key=itemgetter(1))[1]
        if j < 0:
            return (len(visited_vertexes) - 1, j + 1), (min_length, vertex_with_min_length)
        return (j, j + 1), (min_length, vertex_with_min_length)

    def run(self, starting_vertex):
        vertexes = int(self.distance_matrix.shape[0] / 2)
        visited_vertexes = [starting_vertex]
        next_vertex = shortest_next(self.distance_matrix, visited_vertexes, starting_vertex)
        visited_vertexes.append(next_vertex)

        for i in range(0, vertexes - 2):
            best_value_for_next_cycle = []
            unchecked_vertex = [e for e in range(len(self.distance_matrix)) if e not in visited_vertexes]

            for j in range(len(visited_vertexes) - 1):
                best_value_for_next_cycle.append(self.search(unchecked_vertex, visited_vertexes, j))

            final = self.search(unchecked_vertex, visited_vertexes, -1)
            best_value_for_next_cycle.append(final)

            best_place_to_put = min(best_value_for_next_cycle, key=itemgetter(1))
            visited_vertexes = np.insert(np.array(visited_vertexes), best_place_to_put[0][1], best_place_to_put[1][1])
        sum_of_distance = 0
        for i in range(len(visited_vertexes)-1):
            sum_of_distance += self.distance_matrix[visited_vertexes[i]][visited_vertexes[i+1]]
        sum_of_distance += self.distance_matrix[visited_vertexes[-1]][visited_vertexes[0]]
        return sum_of_distance, visited_vertexes