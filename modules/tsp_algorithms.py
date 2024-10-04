# modules/tsp_algorithms.py

import modules.tsp_utils as utils
import numpy as np

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

    Args:
        distance_matrix (np.ndarray): Matriz de distancias entre las ciudades.
        k (int): Número de ciudades a considerar al elegir la siguiente ciudad.
        log_file (file, optional): Archivo de log para registrar el progreso del algoritmo. Por defecto es None.

    Returns:
        tuple: Una tupla que contiene:
            - list: El recorrido (tour) de las ciudades visitadas.
            - float: La distancia total del recorrido.
    """
    # Nº elementos de la matriz
    n = distance_matrix.shape[0]

    visited = np.zeros(n, dtype=bool)  # Usar un array de booleanos para las ciudades visitadas
    tour = []
    total_distance = 0.0

    # Paso 1: Calculamos la suma de distancias para cada ciudad usando numpy
    city_distances = np.sum(distance_matrix, axis=1)

    # Ordenar las ciudades según la suma de sus distancias
    sorted_indices = np.argsort(city_distances)

    # Seleccionar las K ciudades más prometedoras y elegir la primera ciudad aleatoriamente entre ellas
    start_city = random.choice(sorted_indices[:k])
    tour.append(start_city)
    visited[start_city] = True
    current_city = start_city

    # Log de inicio
    utils.registrar_evento(log_file, f"Inicio en ciudad: {start_city}")

    # Construir el tour
    for i in range(n - 1):
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
        total_distance += distance_matrix[current_city, next_city]

        # Marcar la ciudad como visitada y actualizar la ciudad actual
        visited[next_city] = True
        current_city = next_city

        # Registro de cada paso
        utils.registrar_evento(log_file, f"Ejecución {i + 1}: Visitando ciudad {next_city} - Distancia acumulada: {total_distance:.2f}")

    # Sumamos la distancia para volver a la ciudad inicial
    total_distance += distance_matrix[current_city, start_city]
    tour.append(start_city)  # Añadir la ciudad inicial al final del tour para cerrar el ciclo

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
    tamano_entorno = max(1, int(iteraciones * (porcentaje_tamano_entorno / 100.0)))  # (5000*8%) = 400

    # Convertir la lista de visitados a un conjunto
    ciudades_visitadas = set()

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
            ciudades_visitadas.clear()  # Limpiar el conjunto de visitados
            ciudades_visitadas.update(mejor_tour)  # Agregar el nuevo tour al conjunto de visitados

            # Registro de mejora en el log
            if log_file:
                utils.registrar_evento(log_file,f"Iteración {cont_iteraciones}: Mejor distancia = {mejor_distancia:.2f}")
        else:
            # Si no se encuentra una mejor solución, termina el algoritmo
            break

        # Reducir el tamaño del entorno cada % (porcentaje_disminucion_entorno)
        if cont_iteraciones == cuenta + (tamano_entorno // int(porcentaje_disminucion_entorno)) and cont_iteraciones != 0:
            nuevo_tamano = int(tamano_entorno * (1 - (disminucion / 100.0)))
            tamano_entorno = nuevo_tamano  # Reducir el tamaño en un 10%
            cuenta = cont_iteraciones

            if tamano_entorno == 0:
                break

            if log_file:
                utils.registrar_evento(log_file,f"Iteración {cont_iteraciones}: Tamaño del entorno reducido a {tamano_entorno}")

    # Registro final en el log
    if log_file:
        utils.registrar_evento(log_file,f"Búsqueda Local finalizada: Mejor distancia encontrada = {mejor_distancia:.2f}")

    return mejor_tour, mejor_distancia


def algoritmo_tabu(tour, distancia_inicial, iteraciones, porcentaje_tamano_entorno, distance_matrix, porcentaje_disminucion_entorno, disminucion, empeoramiento, k, log_file=None):
    """
    Implementa el algoritmo tabú para el problema del vendedor viajero (TSP).

    Args:
        tour (list): Ruta inicial generada por el algoritmo greedy_random_tsp.
        distancia_inicial (float): Distancia total de la ruta inicial proporcionada.
        iteraciones (int): Número total de iteraciones a realizar.
        porcentaje_tamano_entorno (int): Tamaño inicial del entorno dinámico (% del Total).
        distance_matrix (list[list[float]]): Matriz de distancias entre las ciudades.
        porcentaje_disminucion_entorno (int): Tamaño a partir del cual se reduce el entorno dinámico (% de iteraciones realizadas).
        disminucion(int): Porcentaje de disminución del tamaño del entorno.
        empeoramiento(int): Porcentaje que define el umbral de empeoramientos consecutivos.
        k (int): Número de ciudades a considerar al elegir la siguiente ciudad.
        log_file (file, optional): Archivo de log para registrar el progreso del algoritmo. Por defecto es None.

    Returns:
        tuple: Una tupla que contiene:
            - list: La mejor ruta (tour) encontrada.
            - float: La distancia total de la mejor ruta.
    """
    mejor_tour = tour[:]
    mejor_distancia = distancia_inicial
    mejor_global = mejor_tour[:]  # Inicializar mejor_global con la ruta inicial
    mejor_distancia_global = mejor_distancia  # Inicializar mejor_distancia_global con la distancia inicial
    mejor_momento_actual = mejor_tour[:]  # Inicializar mejor_momento_actual
    mejor_momento_distancia = mejor_distancia  # Inicializar mejor_momento_distancia
    cont_iteraciones = 0
    cuenta = 0
    estancamiento_consecutivo = 0
    max_estancamiento = int(iteraciones * (empeoramiento / 100.0))  # 5% de iteraciones

    # Calculo el tamaño del entorno
    tamano_entorno = int(iteraciones * (porcentaje_tamano_entorno / 100.0))

    # Log inicial
    if log_file:
        utils.registrar_evento(log_file, f"Inicio Algoritmo Tabú: Tamaño inicial del entorno = {tamano_entorno}")

    # Iterar hasta alcanzar el número total de iteraciones
    while cont_iteraciones < iteraciones:
        mejor_vecino, mejor_distancia_vecino, mejora = utils.generar_y_evaluar_vecinos_2opt(mejor_tour, tamano_entorno,
                                                                                            mejor_distancia,
                                                                                            distance_matrix)

        # Si se encuentra una mejora, actualiza la solución actual
        if mejora:
            mejor_tour = mejor_vecino
            mejor_distancia = mejor_distancia_vecino
            estancamiento_consecutivo = 0  # Reiniciar el contador de estancamiento

            # Actualizar mejor global
            if mejor_distancia < mejor_distancia_global:
                mejor_global = mejor_tour[:]
                mejor_distancia_global = mejor_distancia

            cont_iteraciones += 1  # Contar iteración
            mejor_momento_actual = mejor_tour[:]  # Actualizar mejor momento actual
            mejor_momento_distancia = mejor_distancia  # Actualizar distancia mejor momento

            # Registro de mejora en el log
            if log_file:
                utils.registrar_evento(log_file,f"Iteración {cont_iteraciones}: Mejor distancia = {mejor_distancia:.2f}")

        else:
            # No se encontró mejora, utilizar el mejor vecino
            mejor_tour = mejor_vecino
            mejor_distancia = mejor_distancia_vecino
            estancamiento_consecutivo += 1  # Incrementar el contador de estancamiento

            if log_file:
                utils.registrar_evento(log_file,f"Iteración {cont_iteraciones}: Movimiento de empeoramiento, nueva distancia = {mejor_distancia:.2f}")

            # Si se alcanza el límite de estancamiento, reiniciar
            if estancamiento_consecutivo >= max_estancamiento:
                print("mejor d: ", mejor_distancia)
                mejor_tour, mejor_distancia = greedy_random_tsp(distance_matrix, k, log_file=None)  # Nueva solución inicial
                print("mejor d: ", mejor_distancia)

                estancamiento_consecutivo = 0  # Reiniciar el contador de estancamiento
                cont_iteraciones += 1  # Contar como una iteración

                if log_file:
                    utils.registrar_evento(log_file,f"Estancamiento alcanzado. Reiniciando con una nueva solución: Mejor distancia = {mejor_distancia:.2f}")

        # Reducir el tamaño del entorno cada % (porcentaje_disminucion_entorno)
        if cont_iteraciones == cuenta + (tamano_entorno // int(porcentaje_disminucion_entorno)) and cont_iteraciones != 0:
            tamano_entorno = int(tamano_entorno * (1 - (disminucion / 100.0)))  # Reducir el tamaño en un 10%
            cuenta = cont_iteraciones

            if tamano_entorno == 0:
                break

            if log_file:
                utils.registrar_evento(log_file,f"Iteración {cont_iteraciones}: Tamaño del entorno reducido a {tamano_entorno}")

    # Registro final en el log
    if log_file:
        utils.registrar_evento(log_file,f"Algoritmo Tabú finalizado: Mejor distancia encontrada = {mejor_distancia:.2f}")

    return mejor_global, mejor_distancia_global  # Devolver el mejor global