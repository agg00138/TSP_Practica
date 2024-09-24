# modules/tsp_algorithms.py

import random

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

    total_distance += distance_matrix[current_city][tour[0]]    # Sumamos la distancia de vuelta a la ciudad inicial
    tour.append(tour[0])

    return tour, total_distance


def greedy_random_tsp(distance_matrix, k):
    n = len(distance_matrix)
    visited = [False] * n
    tour = []
    total_distance = 0.0

    # Paso 1: Calculamos la suma de distancias para cada ciudad
    city_distances = [(city, sum(distance_matrix[city])) for city in range(n)]
    city_distances.sort(key=lambda x: x[1])  # Ordenamos las ciudades por suma de distancias

    # Elegir la primera ciudad aleatoriamente entre las K más prometedoras
    current_city = random.choice(city_distances[:k])[0]
    tour.append(current_city)
    visited[current_city] = True

    for _ in range(n - 1):
        # Crear una lista de las ciudades no visitadas ordenadas por la suma de distancias original
        unvisited_cities = [city for city, _ in city_distances if not visited[city]]

        # Elegimos aleatoriamente entre las K primeras ciudades no visitadas
        next_city = random.choice(unvisited_cities[:k])

        # Añadimos la siguiente ciudad al tour
        tour.append(next_city)
        total_distance += distance_matrix[current_city][next_city]

        # Marcamos la ciudad como visitada
        visited[next_city] = True

        # Actualizamos la ciudad actual
        current_city = next_city

        # Sumamos la distancia para volver a la ciudad inicial
    total_distance += distance_matrix[current_city][tour[0]]
    tour.append(tour[0])

    return tour, total_distance