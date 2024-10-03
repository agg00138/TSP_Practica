# modules/tsp_algorithms.py

import modules.tsp_utils as utils


import random

def greedy_tsp(distance_matrix, log_file=None):
    """
    Implementa el algoritmo Greedy para resolver el problema del vendedor viajero (TSP).

    Este algoritmo comienza en una ciudad inicial y en cada paso visita la ciudad no visitada más cercana,
    construyendo un recorrido (tour) que retorna a la ciudad de inicio al final.

    Args:
        distance_matrix (list[list[float]]): Matriz de distancias entre las ciudades.
        log_file (file, optional): Archivo de log para registrar el progreso del algoritmo. Por defecto es None.

    Returns:
        tuple: Una tupla que contiene:
            - list: El recorrido (tour) de las ciudades visitadas.
            - float: La distancia total del recorrido.
    """
    n = len(distance_matrix)
    visited = [False] * n
    tour = []
    total_distance = 0.0

    current_city = 0
    tour.append(current_city)
    visited[current_city] = True

    # Log de inicio
    utils.registrar_evento(log_file, f"Inicio en ciudad: {current_city}")

    for _ in range(n - 1):
        next_city = None
        min_distance = float('inf')

        # Buscar la ciudad no visitada más cercana
        for city in range(n):
            if not visited[city]:
                distance = distance_matrix[current_city][city]
                if distance < min_distance:
                    min_distance = distance
                    next_city = city

        # Actualizar el tour y la distancia total
        tour.append(next_city)
        total_distance += min_distance
        visited[next_city] = True
        current_city = next_city

        # Registro de cada paso
        utils.registrar_evento(log_file, f"Visitando ciudad {next_city} - Distancia acumulada: {total_distance:.2f}")

    # Regresar a la ciudad inicial
    total_distance += distance_matrix[current_city][tour[0]]
    tour.append(tour[0])

    # Registro final
    utils.registrar_evento(log_file, f"Distancia total: {total_distance:.2f}")
    utils.registrar_evento(log_file, f"Tour final: {tour}")

    return tour, total_distance


def greedy_random_tsp(distance_matrix, k, log_file=None):
    """
    Implementa el algoritmo Greedy Aleatorio para resolver el problema del vendedor viajero (TSP).

    Este algoritmo calcula la suma de distancias para cada ciudad, selecciona aleatoriamente
    una ciudad de entre las K más prometedoras, y construye un recorrido (tour) hasta que
    se hayan visitado todas las ciudades.

    Args:
        distance_matrix (list[list[float]]): Matriz de distancias entre las ciudades.
        k (int): Número de ciudades a considerar al elegir la siguiente ciudad.
        log_file (file, optional): Archivo de log para registrar el progreso del algoritmo. Por defecto es None.

    Returns:
        tuple: Una tupla que contiene:
            - list: El recorrido (tour) de las ciudades visitadas.
            - float: La distancia total del recorrido.
    """
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

    # Log de inicio
    utils.registrar_evento(log_file, f"Inicio en ciudad: {current_city}")

    for i in range(n - 1):
        # Crear una lista de las ciudades no visitadas
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

        # Registro de cada paso
        utils.registrar_evento(log_file,
                         f"Ejecución {i + 1}: Visitando ciudad {next_city} - Distancia acumulada: {total_distance:.2f}")

    # Sumamos la distancia para volver a la ciudad inicial
    total_distance += distance_matrix[current_city][tour[0]]
    tour.append(tour[0])

    # Registro final
    utils.registrar_evento(log_file, f"Distancia total: {total_distance:.2f}")
    utils.registrar_evento(log_file, f"Tour final: {tour}")

    return tour, total_distance


def busqueda_local_mejor(tour, distancia_inicial, iteraciones, porcentaje_tamano_entorno, distance_matrix, porcentaje_disminucion_entorno, disminucion, log_file=None):
    """
        Implementa la búsqueda local del mejor para el problema del vendedor viajero (TSP).

        Args:
            tour (list): Ruta inicial generada por el algoritmo greedy_random_tsp.
            distancia_inicial (float): Distancia total de la ruta inicial proporcionada.
            iteraciones (int): Número total de iteraciones a realizar.
            porcentaje_tamano_entorno (int): Tamaño inicial del entorno dinámico (% del Total).
            distance_matrix (list[list[float]]): Matriz de distancias entre las ciudades.
            porcentaje_disminucion_entorno (int): Tamaño a partir del cual se reduce el entorno dinámico (% de iteraciones realizadas)
            disminucion(int): Porcentaje de disminución del tamaño del entorno.
            log_file (file, optional): Archivo de log para registrar el progreso del algoritmo. Por defecto es None.

        Returns:
            tuple: Una tupla que contiene:
                - list: La mejor ruta (tour) encontrada.
                - float: La distancia total de la mejor ruta.
        """
    mejor_tour = tour[:]
    mejor_distancia = distancia_inicial
    cont_iteraciones = 0
    cuenta = 0

    # Calculo el tamaño del entorno
    tamano_entorno = int(iteraciones * (porcentaje_tamano_entorno / 100.0)) # (5000*8%) = 400

    # Log inicial
    if log_file:
        utils.registrar_evento(log_file, f"Inicio Búsqueda Local: Tamaño inicial del entorno = {tamano_entorno}")

    # Iterar hasta alcanzar el número total de iteraciones
    while cont_iteraciones < iteraciones:

        # Generar vecinos y evaluar de inmediato
        mejor_vecino, mejor_distancia_vecino, mejora = utils.generar_y_evaluar_vecinos_2opt(mejor_tour, tamano_entorno,
                                                                                            mejor_distancia,
                                                                                            distance_matrix)

        # Si se encuentra una mejora, actualiza la solución actual
        if mejora:
            mejor_tour = mejor_vecino
            mejor_distancia = mejor_distancia_vecino
            cont_iteraciones += 1  # Solo se cuenta una iteración si se encuentra un mejor vecino

            # Registro de mejora en el log
            if log_file:
                utils.registrar_evento(log_file,
                                       f"Iteración {cont_iteraciones}: Mejor distancia = {mejor_distancia:.2f}")
        else:
            # Si no se encuentra una mejor solución, termina el algoritmo
            break

        # Reducir el tamaño del entorno cada % (porcentaje_disminucion_entorno)
        if cont_iteraciones == cuenta + (tamano_entorno // 10) and cont_iteraciones != 0:
            tamano_entorno = max(1, int(tamano_entorno * (1 - (disminucion / 100.0))))  # Reducir el tamaño en un 10% pero mantener mínimo de 1
            cuenta = cont_iteraciones

            if log_file:
                utils.registrar_evento(log_file,f"Iteración {cont_iteraciones}: Tamaño del entorno reducido a {tamano_entorno}")

    # Registro final en el log
    if log_file:
        utils.registrar_evento(log_file,f"Búsqueda Local finalizada: Mejor distancia encontrada = {mejor_distancia:.2f}")

    return mejor_tour, mejor_distancia