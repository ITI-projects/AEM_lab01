from preparedata import shortest_next, PrepareData


class NearestNeighborAlgorithm:

    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix

    def run(self, starting_vertex):

        vertexes = int(self.distance_matrix.shape[0]/2)
        visited_vertexes = [starting_vertex]
        sum_of_distance = 0

        for i in range(0, vertexes-1):
            next_vertex = shortest_next(self.distance_matrix, visited_vertexes, starting_vertex)
            visited_vertexes.append(next_vertex)
            sum_of_distance += self.distance_matrix[starting_vertex][next_vertex]
            starting_vertex = next_vertex

        sum_of_distance += self.distance_matrix[visited_vertexes[0]][visited_vertexes[-1]]
        return sum_of_distance, visited_vertexes