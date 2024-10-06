# algorithms/greedy_teoria.py

from utils.utilidades import registrar_evento

def greedy_teoria(matriz_distancias, log_file=None):
    """
        Implementa el algoritmo Greedy para resolver el problema del vendedor viajero (TSP).
        El algoritmo selecciona la ciudad más cercana no visitada en cada paso hasta completar el tour.

        Args:
            matriz_distancias (list[list[float]]): Matriz de distancias entre las ciudades.
            log_file (file object, optional): Archivo donde se registran los eventos del algoritmo.

        Returns:
            tuple: Un tuple que contiene el recorrido (tour) y la distancia total del tour.
    """

    n = len(matriz_distancias)
    visited = [False] * n
    tour = []
    total_distance = 0.0

    current_city = 0
    tour.append(current_city)
    visited[current_city] = True

    # Log de inicio
    registrar_evento(log_file, f"Inicio en ciudad: {current_city}")

    for _ in range(n - 1):
        next_city = None
        min_distance = float('inf')

        # Buscar la ciudad no visitada más cercana
        for city in range(n):
            if not visited[city]:
                distance = matriz_distancias[current_city][city]
                if distance < min_distance:
                    min_distance = distance
                    next_city = city

        # Actualizar el tour y la distancia total
        tour.append(next_city)
        total_distance += min_distance
        visited[next_city] = True
        current_city = next_city

        # Registro de cada paso
        registrar_evento(log_file, f"Visitando ciudad {next_city} - Distancia acumulada: {total_distance:.2f}")

    # Regresar a la ciudad inicial
    total_distance += matriz_distancias[current_city][tour[0]]
    tour.append(tour[0])

    # Registro final
    registrar_evento(log_file, f"Distancia total: {total_distance:.2f}")
    registrar_evento(log_file, f"Tour final: {tour}")

    return tour, total_distance