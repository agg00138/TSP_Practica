# modules/tsp_utils.py

import sys, random, numpy as np
from scipy.spatial.distance import cdist


#   ########################################
#   FUNCIONES PARA PROCESAR: TSP Y CONFIG
#   ########################################


def procesar_config(filename):
    params = {
        'Archivos': [],
        'Semillas': [],
        'Algoritmos': [],
        'K_Ciudades': None,
        'Echo': None,
        'Iteraciones': None,
        'Porcentaje_Tamano_ED': None,
        'Porcentaje_Disminucion_ED': None,
        'Disminucion': None,
        'Porcentaje_Emp': None
    }

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or not line:  # Ignorar comentarios y líneas vacías
                    continue

                if '=' in line:  # Solo procesar líneas que contengan '='
                    key, value = line.split('=', 1)
                    key = key.strip()  # Eliminar espacios en la clave
                    value = value.strip()  # Eliminar espacios en el valor

                    # Usar un diccionario para asignar los valores
                    if key in params:
                        if key in ['K_Ciudades', 'Iteraciones', 'Porcentaje_Tamano_ED', 'Porcentaje_Disminucion_ED', 'Disminucion', 'Porcentaje_Emp']:
                            params[key] = int(value)
                        elif key == 'Echo':
                            params[key] = value  # Asigna directamente como cadena
                        else:
                            params[key] = [item.strip() for item in value.split(',')]

    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no se encuentra.")
        sys.exit(1)
    except ValueError:
        print(f"Error: Valor no válido en '{key}' para '{value}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return params


def procesar_tsp(filename):
    tsp_data = {
        'name': None,          # Nombre del problema TSP
        'dimension': None,     # Número de nodos (ciudades)
        'node_coords': []      # Lista para almacenar las coordenadas de las ciudades
    }

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Elimina espacios en blanco al principio y final de la línea
            if not line or line.startswith('NODE_COORD_SECTION') or line == 'EOF':
                # Saltar líneas vacías, la sección de coordenadas y el indicador de fin del archivo
                continue

            # Procesar cabeceras y coordenadas del archivo
            if line.startswith('NAME:'):
                tsp_data['name'] = line.split(':')[1].strip()
            elif line.startswith('DIMENSION:'):
                tsp_data['dimension'] = int(line.split(':')[1].strip())
            else:
                # Procesar las coordenadas de cada nodo si la línea tiene exactamente 3 valores
                tokens = line.split()
                if len(tokens) == 3:
                    _, x, y = tokens
                    tsp_data['node_coords'].append((float(x), float(y)))

    return tsp_data


#   ########################################
#           FUNCIONES PARA CÁLCULOS
#   ########################################


def crear_matriz_distancias(node_coords):
    """Calcula una matriz de distancias usando scipy para mayor eficiencia."""
    node_coords = np.array(node_coords)
    return cdist(node_coords, node_coords)


def calcular_distancia(coord1, coord2):
    """Calcula la distancia euclidiana entre dos coordenadas."""
    x1, y1 = coord1
    x2, y2 = coord2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def calcular_distancia_total(tour, distance_matrix):
    """
    Calcula la distancia total de un recorrido (tour) basado en la matriz de distancias.

    Args:
        tour (list): Recorrido que representa la secuencia de ciudades a visitar.
        distance_matrix (list[list[float]]): Matriz de distancias entre las ciudades.

    Returns:
        float: Distancia total del recorrido.
    """
    total_distance = 0.0
    n = len(tour)

    # Sumar la distancia entre cada par de ciudades consecutivas en el tour
    for i in range(n - 1):
        total_distance += distance_matrix[tour[i]][tour[i + 1]]

    # Añadir la distancia para regresar a la ciudad inicial
    total_distance += distance_matrix[tour[-1]][tour[0]]

    return total_distance


def calcular_distancia_total_numpy(tour, distance_matrix):
    return np.sum(distance_matrix[tour[:-1], tour[1:]]) + distance_matrix[tour[-1], tour[0]]


def factorizacion(tour_actual, tour_nuevo, distancia_inicial, indices, distance_matrix):
    """
    Calcula la nueva distancia usando la distancia inicial y ajustando por los arcos que desaparecen y aparecen.
    Considera problemas simétricos en la matriz de distancias.

    Args:
        tour_actual (list): Ruta actual.
        tour_nuevo (list): Nueva ruta generada.
        distancia_inicial (float): Distancia total de la ruta actual.
        indices (tuple): Índices de las ciudades que se intercambiaron.
        distance_matrix (list[list[float]]): Matriz de distancias entre las ciudades.

    Returns:
        float: La nueva distancia total del recorrido.
    """
    i, j = indices
    n = len(tour_actual)

    # Identificar los arcos que desaparecen
    arco_1 = distance_matrix[tour_actual[i - 1]][tour_actual[i]]  # Arco antes de i
    arco_2 = distance_matrix[tour_actual[j]][tour_actual[(j + 1) % n]]  # Arco después de j

    # Identificar los nuevos arcos que aparecen tras el intercambio
    arco_nuevo_1 = distance_matrix[tour_nuevo[i - 1]][tour_nuevo[i]]  # Nuevo arco antes de i
    arco_nuevo_2 = distance_matrix[tour_nuevo[j]][tour_nuevo[(j + 1) % n]]  # Nuevo arco después de j

    nueva_distancia = distancia_inicial - (arco_1 + arco_2) + (arco_nuevo_1 + arco_nuevo_2)

    return nueva_distancia


def generar_y_evaluar_vecinos_2opt(tour, tamano_entorno, mejor_distancia, distance_matrix):
    """
    Genera vecinos usando el operador 2-opt y evalúa su calidad respecto a la mejor distancia.

    Args:
        tour (list): Recorrido que representa la secuencia de ciudades a visitar.
        tamano_entorno (int): Número de vecinos a generar.
        mejor_distancia (float): La distancia total del mejor recorrido encontrado hasta el momento.
        distance_matrix (list[list[float]]): Matriz de distancias entre las ciudades.

    Returns:
        tuple: Una tupla que contiene:
            - list: El mejor recorrido (tour) encontrado.
            - float: La distancia total del mejor recorrido.
            - bool: Indica si se encontró una mejora.
    """
    mejor_vecino = None
    mejor_distancia_vecino = float('inf')
    n = len(tour)  # Número de ciudades en el tour
    mejora_encontrada = False  # Bandera para indicar si se encuentra una mejora

    # Generar y evaluar cada vecino en el entorno
    for _ in range(tamano_entorno):
        # Seleccionar dos puntos al azar para intercambiar
        i, j = sorted(random.sample(range(1, n), 2))  # Asegurar que i < j
        # Generar un nuevo vecino aplicando la operación 2-opt
        nuevo_vecino = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]

        # Calcular la distancia del vecino usando factorización
        #distancia_vecino = factorizacion(tour, nuevo_vecino, mejor_distancia, (i, j), distance_matrix)
        #distancia_vecino = calcular_distancia_total(nuevo_vecino, distance_matrix) # Para comprobar
        distancia_vecino = calcular_distancia_total_numpy(nuevo_vecino, distance_matrix)

        # Si encontramos un vecino mejor, actualizar
        if distancia_vecino < mejor_distancia_vecino:
            mejor_vecino = nuevo_vecino
            mejor_distancia_vecino = distancia_vecino

        if distancia_vecino < mejor_distancia:
            mejora_encontrada = True    # Marcar que hemos encontrado una mejora

    # Retornar el mejor vecino encontrado y si hubo o no mejora
    return mejor_vecino, mejor_distancia_vecino, mejora_encontrada


#   ########################################
#   FUNCIONES PARA GENERAR REGISTROS DE LOGS
#   ########################################


def generar_logs(alg_name, tsp_data, seed=None, execution_num=None):
    """Genera el nombre del archivo de log basado en los parámetros proporcionados."""
    log_filename = f"logs/{alg_name}_{tsp_data['name']}"

    if seed is not None and execution_num is not None:
        log_filename += f"_{seed}_ejecucion_{execution_num}.log"
    else:
        log_filename += "_ejecucion.log"

    return log_filename


def registrar_evento(log_file, mensaje):
    """Registra un evento en el archivo de log."""
    if log_file:
        log_file.write(mensaje + '\n')