# modules/tsp_utils.py

import math, sys

def procesar_tsp(filename):
    tsp_data = {
        'name': None,   # Nombre del problema TSP
        'dimension': None,  # Número de nodos (ciudades)
        'node_coords': []   # Lista para almacenar las coordenadas de las ciudades
    }
    with open(filename, 'r') as file:   # Abrimos el archivo en modo lectura
        for line in file:
            line = line.strip() # Elimina espacios en blanco al principio y final de la línea
            if not line:    # Si la línea está vacía la saltamos
                continue
            if line.startswith('NAME:'):
                tsp_data['name'] = line.split(':')[1].strip()
            elif line.startswith('DIMENSION:'):
                tsp_data['dimension'] = int(line.split(':')[1].strip())
            elif line.startswith('NODE_COORD_SECTION'):
                continue
            elif line == 'EOF': # Finalizamos
                break
            if len(line.split()) == 3:  # Si la línea contiene tres partes, extraemos las coordenadas del nodo
                _, x, y = line.split()  # Ignora el índice y toma sólo las coordenadas
                tsp_data['node_coords'].append((float(x), float(y)))
    return tsp_data


def calcular_distancia(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def crear_matriz_distancias(node_coords):
    n = len(node_coords)

    # Creamos una matriz cuadrada n x n inicializada con 0.0, donde se almacenarán las distancias
    # [0.0] * n : Crea una fila de longitud n llena de ceros decimales (0.0)
    # [[0.0] * n for _ in range(n)] : Lista por compresión
    # _ (placeholder) : Variable que no se usa
    # range(n) : crea una secuencia de números de 0 a n-1. Por lo tanto, el bucle se repite n veces
    distance_matrix = [[0.0] * n for _ in range(n)]

    # Recorremos cada nodo para calcular la distancia con los demás nodos
    for i in range(n):
        for j in range(i + 1, n):
            distance = calcular_distancia(node_coords[i], node_coords[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    return distance_matrix


def print_matriz_distancias(matrix):
    # f"{elem:.2f}" : Convertirá el número flotante en una cadena con 2 decimales
    # max(len(f"{elem:.2f}") : Buscará la cadena con la longitud más larga
    # for row in matrix for elem in row) + 2 : Recorre cada fila y cada elem de esa fila y aplica un margen de +2
    max_width = max(len(f"{elem:.2f}") for row in matrix for elem in row) + 2
    for row in matrix:
        print("".join(f"{elem:{max_width}.2f}" for elem in row))


def procesar_archivo_txt(filename):
    # [line.strip() for line in file.readlines() if line.strip()]
    # line.strip() : Elimina los espacios en blanco al principio y al final de cada línea
    # if line.strip() : Solo incluye en la lista aquellas líneas que no estén vacías (después de aplicar strip())
    try:
        with open(filename, 'r') as file:
            tsp_files = [line.strip() for line in file.readlines() if line.strip()]
        return tsp_files
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no se encuentra.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def procesar_archivo_config(filename):
    params = {
        'Archivos': [],
        'Semillas': [],
        'Algoritmos': [],
        'OtrosParametros1': None
    }
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('Archivos='):
                    params['Archivos'] = [f.strip() for f in line.split('=')[1].split(',')]
                elif line.startswith('Semillas='):
                    params['Semillas'] = line.split('=')[1].split(',')
                elif line.startswith('Algoritmos='):
                    params['Algoritmos'] = [a.strip() for a in line.split('=')[1].split(',')]
                elif line.startswith('OtrosParametros1='):
                    params['OtrosParametros1'] = line.split('=')[1].strip()
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no se encuentra.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    return params