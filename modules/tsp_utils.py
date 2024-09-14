# modules/tsp_utils.py

import math, sys

def procesar_tsp(filename):
    tsp_data = {
        'name': None,
        'dimension': None,
        'node_coords': []
    }
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('NAME:'):
                tsp_data['name'] = line.split(':')[1].strip()
            elif line.startswith('DIMENSION:'):
                tsp_data['dimension'] = int(line.split(':')[1].strip())
            elif line.startswith('NODE_COORD_SECTION'):
                continue
            elif line == 'EOF':
                break
            if len(line.split()) == 3:
                _, x, y = line.split()
                tsp_data['node_coords'].append((float(x), float(y)))
    return tsp_data


def calcular_distancia(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def crear_matriz_distancias(node_coords):
    n = len(node_coords)
    distance_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distance = calcular_distancia(node_coords[i], node_coords[j])
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    return distance_matrix


def print_matriz_distancias(matrix):
    max_width = max(len(f"{elem:.2f}") for row in matrix for elem in row) + 2
    for row in matrix:
        print("".join(f"{elem:{max_width}.2f}" for elem in row))


def procesar_archivo_txt(filename):
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