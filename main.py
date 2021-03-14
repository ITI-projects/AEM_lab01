from preparedata import *
from nearest_neighbor_algorithm import *
from greedy_cycle_algorithm import *
from regret_heuristics import *
import random
import numpy as np
from draw import *


def test(matrix, alg):
    algorithm = alg(matrix)

    visited_coordinates = []
    distances = []
    num = int(matrix.shape[0] / 2)
    for n in range(50):
        start = random.randint(0, num * 2 - 1)
        sum_distances, visited = algorithm.run(start)
        distances.append([sum_distances])
        visited_coordinates.append([visited])
    return np.array(distances), np.array(visited_coordinates)


def results(all_distance):
    best = all_distance.argmin(axis=0)
    mean = all_distance.mean(axis=0)
    worst = all_distance.argmax(axis=0)
    return best, worst, mean


def main(path):
    loaded_data = PrepareData(path)
    coordinates = loaded_data.get_coords()
    drawing = DrawPlot(coordinates)
    matrix = loaded_data.calculate_distance_matrix()

    # Nearest Neighbor
    all_distances, all_visited = test(matrix, NearestNeighborAlgorithm)
    best, worst, mean = results(all_distances)
    print("Greedy\nWorst\tBest\tMean")
    print(all_distances[worst[0]], all_distances[best[0]], mean)
    drawing.draw_results(all_visited[best[0]][0], "images/Greed_" + path + ".png",
                "Najlepszy wynik dla algorytmu Nearest Neighbor dla " + path)

    # # Greedy cycle
    all_distances, all_visited = test(matrix, GreedyCycleAlgorithm)
    best, worst, mean = results(all_distances)
    print("Greedy Cycle\nWorst\tBest\tMean")
    print(all_distances[worst[0]], all_distances[best[0]], mean)
    drawing.draw_results(all_visited[best[0]][0], "images/Greed_Cycle_" + path + ".png",
                         "Najlepszy wynik dla algorytmu Greedy Cycle dla " + path)

    # Regret
    all_distances, all_visited = test(matrix, RegretHeuristics)
    best, worst, mean = results(all_distances)
    print("Regret\nWorst\tBest\tMean")
    print(all_distances[worst[0]], all_distances[best[0]], mean)
    drawing.draw_results(all_visited[best[0]][0], "images/Regret_" + path + ".png",
                         "Najlepszy wynik dla algorytmu Regret Heuristics dla " + path)


if __name__ == '__main__':
    print("kroA100")
    main(pathA)
    print("kroB100")
    main(pathB)
