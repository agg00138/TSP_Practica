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
    # Controlamos si encontramos un mejor vecino
    mejora = False
    mejor_vecino = None
    distancia_mejor_vecino = float('inf')

    # Número de ciudades en el tour
    n = len(tour)

    for _ in range(tamanio_entorno):
        # Seleccionar dos puntos al azar para intercambiar
        # Evitamos el primer y el último índice para prevenir errores en la operación 2-opt
        i, j = sorted(random.sample(range(1, n - 1), 2))  # Asegurar que 1 <= i < j <= n-2

        # Aplicar 2-opt
        nuevo_vecino = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]

        # Calcular los arcos que desaparecen en el tour original
        arco_original_1 = matriz_distancias[tour[i - 1]][tour[i]]
        arco_original_2 = matriz_distancias[tour[j]][tour[(j + 1) % n]]

        # Calcular los arcos nuevos en el vecino
        arco_nuevo_1 = matriz_distancias[nuevo_vecino[i - 1]][nuevo_vecino[i]]
        arco_nuevo_2 = matriz_distancias[nuevo_vecino[j]][nuevo_vecino[(j + 1) % n]]

        # Actualizamos la distancia del vecino
        nueva_distancia = distancia - (arco_original_1 + arco_original_2) + (arco_nuevo_1 + arco_nuevo_2)

        # Verificamos si encontramos un vecino mejor
        if nueva_distancia < distancia_mejor_vecino:
            mejor_vecino = nuevo_vecino
            distancia_mejor_vecino = nueva_distancia

        # Verificar que la nueva distancia sea válida
        if distancia_mejor_vecino < distancia:
            mejora = True

    return mejor_vecino, distancia_mejor_vecino, mejora