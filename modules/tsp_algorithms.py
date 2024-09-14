# modules/tsp_algorithms.py

def greedy_tsp(distance_matrix):
    n = len(distance_matrix)
    visited = [False] * n
    tour = []
    total_distance = 0.0

    current_city = 0
    tour.append(current_city)
    visited[current_city] = True

    for _ in range(n - 1):
        next_city = None
        min_distance = float('inf')
        for city in range(n):
            if not visited[city] and distance_matrix[current_city][city] < min_distance:
                min_distance = distance_matrix[current_city][city]
                next_city = city
        tour.append(next_city)
        total_distance += min_distance
        visited[next_city] = True
        current_city = next_city

    total_distance += distance_matrix[current_city][tour[0]]
    tour.append(tour[0])

    return tour, total_distance