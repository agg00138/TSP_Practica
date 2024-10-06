# algorithms/greedy_aleatorio.py

import numpy as np
import random

from utils.utilidades import registrar_evento


def greedy_aleatorio(matriz_distancias, k, log_file=None):
    """
    Implementa el algoritmo Greedy Aleatorio para resolver el problema del vendedor viajero (TSP).

    Args:
        matriz_distancias (np.ndarray): Matriz de distancias entre las ciudades.
        k (int): Número de ciudades a considerar al elegir la siguiente ciudad.

    Returns:
        tuple: Una tupla que contiene:
            - list: El recorrido (tour) de las ciudades visitadas.
            - float: La distancia total del recorrido.
    """

    # Nº elementos de la matriz
    n = matriz_distancias.shape[0]

    visited = np.zeros(n, dtype=bool)  # Usar un array de booleanos para las ciudades visitadas
    tour = []
    total_distance = 0.0

    # Paso 1: Calculamos la suma de distancias para cada ciudad usando numpy
    city_distances = np.sum(matriz_distancias, axis=1)

    # Ordenar las ciudades según la suma de sus distancias
    sorted_indices = np.argsort(city_distances)

    # Seleccionar las K ciudades más prometedoras y elegir la primera ciudad aleatoriamente entre ellas
    start_city = random.choice(sorted_indices[:k])
    tour.append(start_city)
    visited[start_city] = True
    current_city = start_city

    # Log de inicio
    registrar_evento(log_file, f"Inicio en ciudad: {start_city}\n")

    # Construir el tour
    for _ in range(n - 1):
        # Filtrar las ciudades no visitadas
        unvisited_indices = np.where(~visited)[0]

        # Obtener las K ciudades más prometedoras no visitadas
        k_candidates = sorted_indices[np.isin(sorted_indices, unvisited_indices)][:k]
        if len(k_candidates) == 0:
            break

        # Elegir aleatoriamente la siguiente ciudad entre las K candidatas
        next_city = random.choice(k_candidates)

        # Añadir la siguiente ciudad al tour y actualizar la distancia total
        tour.append(next_city)
        total_distance += matriz_distancias[current_city, next_city]

        # Marcar la ciudad como visitada y actualizar la ciudad actual
        visited[next_city] = True
        current_city = next_city

        # Registro de cada paso
        registrar_evento(log_file, f"Paso {_ + 1}: Visitando ciudad {next_city}, Distancia acumulada: {total_distance:.2f}\n")

    # Sumamos la distancia para volver a la ciudad inicial
    total_distance += matriz_distancias[current_city, start_city]
    tour.append(start_city)  # Añadir la ciudad inicial al final del tour para cerrar el ciclo

    # Registro final
    registrar_evento(log_file, f"Regresando a la ciudad inicial: {start_city}, Distancia total: {total_distance:.2f}\n")
    registrar_evento(log_file, f"Tour completo: {list(map(int, tour))}\n")

    return list(map(int, tour)), total_distance