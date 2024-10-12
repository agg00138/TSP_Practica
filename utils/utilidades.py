# utils/utilidades.py

import numpy as np, random

from scipy.spatial.distance import cdist


def registrar_evento(log_file, mensaje):
    """Registra un evento en el archivo de log."""
    if log_file:
        log_file.write(mensaje + '\n')


def generar_logs(alg_name, tsp_data, seed=None, execution_num=None):
    """Genera el nombre del archivo de log basado en los parámetros proporcionados."""
    log_filename = f"logs/{alg_name}_{tsp_data['nombre']}"

    if seed is not None and execution_num is not None:
        log_filename += f"_{seed}_ejecucion_{execution_num}.log"
    else:
        log_filename += "_ejecucion.log"

    return log_filename


def crear_matriz_distancias_scipy(coordenadas):
    """
    Crea una matriz de distancias utilizando scipy a partir de las coordenadas de las ciudades.

    :param coordenadas: Lista de tuplas con las coordenadas de las ciudades [(x1, y1), (x2, y2), ...].
    :return: Matriz de distancias (numpy array).
    """
    # Convertir la lista de coordenadas a un numpy array
    coordenadas_array = np.array(coordenadas)

    # Calcular la matriz de distancias usando cdist
    matriz_distancias = cdist(coordenadas_array, coordenadas_array, metric='euclidean')

    return matriz_distancias


def generar_vecinos(tour, distancia, matriz_distancias, tamanio_entorno):
    """
        Genera vecinos de la solución actual (tour) al intercambiar dos ciudades.

        Parameters:
            tour (list): La solución actual representada como un recorrido de ciudades.
            distancia (float): La distancia total de la solución actual.
            matriz_distancias (numpy.ndarray): Matriz de distancias entre las ciudades.
            tamanio_entorno (int): Número de vecinos a generar.

        Returns:
            mejor_vecino (list): El vecino que tiene la mejor (menor) distancia encontrada.
            distancia_mejor_vecino (float): La distancia del mejor vecino encontrado.
            mejora (bool): Indica si se encontró una mejora en comparación con la solución actual.
            m_i (int): Índice de la primera ciudad intercambiada.
            m_j (int): Índice de la segunda ciudad intercambiada.
    """

    # Variables del vecino
    mejor_vecino = None
    distancia_mejor_vecino = float('inf')

    # Control de la mejora
    mejora = False

    # Control de los índices
    i, j = 0, 0
    m_i, m_j = 0, 0

    # Arcos
    arco_original_1 = arco_original_2 = arco_original_3 = arco_original_4 = 0
    nuevo_arco_1 = nuevo_arco_2 = nuevo_arco_3 = nuevo_arco_4 = 0

    # Número de ciudades en el tour
    n = len(tour)

    for _ in range(tamanio_entorno):
        # Selecciona dos índices al azar (intercambio)
        i, j = sorted(random.sample(range(1, n - 1), 2))

        # Generamos el tour del vecino
        nuevo_vecino = tour[:]
        nuevo_vecino[i], nuevo_vecino[j] = tour[j], tour[i]

        # Calculamos las distancias de los arcos
        if i + 1 == j:
            arco_original_1 = matriz_distancias[tour[i - 1]][tour[i]]
            arco_original_2 = matriz_distancias[tour[j]][tour[j + 1 % n]]
            nuevo_arco_1 = matriz_distancias[tour[i - 1]][tour[j]]
            nuevo_arco_2 = matriz_distancias[tour[i]][tour[j + 1 % n]]
        else:
            arco_original_1 = matriz_distancias[tour[i - 1]][tour[i]]
            arco_original_2 = matriz_distancias[tour[i]][tour[i + 1 % n]]
            arco_original_3 = matriz_distancias[tour[j - 1]][tour[j]]
            arco_original_4 = matriz_distancias[tour[j]][tour[j + 1 % n]]
            nuevo_arco_1 = matriz_distancias[tour[i - 1]][tour[j]]
            nuevo_arco_2 = matriz_distancias[tour[j]][tour[i + 1 % n]]
            nuevo_arco_3 = matriz_distancias[tour[j - 1]][tour[i]]
            nuevo_arco_4 = matriz_distancias[tour[i]][tour[j + 1 % n]]

        # Arcos que DESAPARECEN
        arcos_desaparecen = (arco_original_1 + arco_original_2 + arco_original_3 + arco_original_4)

        # Arcos NUEVOS
        arcos_nuevos = (nuevo_arco_1 + nuevo_arco_2 + nuevo_arco_3 + nuevo_arco_4)

        # Calculo la distancia del vecino generado
        nueva_distancia = distancia - (arcos_desaparecen) + (arcos_nuevos)

        # Verificamos el nuevo vecino encontrado
        if nueva_distancia < distancia_mejor_vecino:
            mejor_vecino = nuevo_vecino
            distancia_mejor_vecino = nueva_distancia
            m_i, m_j = i, j

        # Comprobamos si existe una mejora
        if distancia_mejor_vecino < distancia:
            mejora = True

    return mejor_vecino, distancia_mejor_vecino, mejora, m_i, m_j


def operador_intensificacion(solucion_actual, matriz_distancias):
    """
    Operador de intensificación: Genera una solución basada en la solución actual
    para explorar intensivamente su vecindario.

    Args:
        solucion_actual (list): La solución actual (recorrido).
        matriz_distancias (numpy.ndarray): Matriz de distancias entre las ciudades.

    Returns:
        list, float: Un nuevo tour generado y su distancia.
    """
    # Aquí puedes usar algún metodo como un operador 2-opt intensivo en torno a la mejor solución
    nueva_solucion = solucion_actual.copy()
    np.random.shuffle(nueva_solucion)  # Simple intensificación aleatoria (se puede mejorar)

    # Calcular la distancia total de la nueva solución
    nueva_distancia = calcular_distancia(nueva_solucion, matriz_distancias)

    return nueva_solucion, nueva_distancia


def operador_diversificacion(matriz_distancias):
    """
    Operador de diversificación: Genera una solución completamente nueva
    para explorar otras áreas del espacio de búsqueda.

    Args:
        matriz_distancias (numpy.ndarray): Matriz de distancias entre las ciudades.

    Returns:
        list, float: Un nuevo tour generado y su distancia.
    """
    # Generar una solución completamente nueva aleatoria
    nueva_solucion = np.random.permutation(len(matriz_distancias)).tolist()

    # Calcular la distancia total de la nueva solución
    nueva_distancia = calcular_distancia(nueva_solucion, matriz_distancias)

    return nueva_solucion, nueva_distancia


def calcular_distancia(tour, matriz_distancias):
    """
    Calcula la distancia total de un recorrido dado.

    Args:
        tour (list): Recorrido de las ciudades.
        matriz_distancias (numpy.ndarray): Matriz de distancias entre las ciudades.

    Returns:
        float: Distancia total del recorrido.
    """
    distancia_total = 0
    for i in range(len(tour)):
        distancia_total += matriz_distancias[tour[i]][tour[(i + 1) % len(tour)]]
    return distancia_total
