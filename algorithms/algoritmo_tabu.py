from utils.utilidades import generar_vecinos
from algorithms.greedy_aleatorio import greedy_aleatorio
from utils.utilidades import registrar_evento


def algoritmo_tabu(tour_inicial, distancia_inicial, matriz_distancias, params, log_file=None):
    """
        Implementa el algoritmo Tabu Search para resolver el problema del vendedor viajero (TSP).
        Este algoritmo busca mejorar iterativamente la solución actual, permitiendo movimientos que pueden
        empeorar la solución con el fin de evitar caer en óptimos locales.

        Args:
            tour_inicial (list): La solución inicial (recorrido) del problema.
            distancia_inicial (float): La distancia total del recorrido inicial.
            matriz_distancias (numpy.ndarray): Matriz de distancias entre las ciudades.
            params (dict): Parámetros del algoritmo que controlan su comportamiento.
            log_file (file object, optional): Archivo donde se registran los eventos del algoritmo.

        Returns:
            tuple: Un tuple que contiene el mejor recorrido encontrado y su distancia total.
    """

    # Cargar los parámetros
    iteraciones = params['iterations']
    tamanio_inicial_entorno = params['initial_environment_size']
    ratio_disminucion_entorno = params['size_decrease_rate']
    disminucion_tamanio = params['size_decrease_environment']
    ratio_empeoramiento = params['worsening_movement_rate']
    k = params['K']

    # Calculo el tamaño del entorno dinámico
    tamanio = int(iteraciones * tamanio_inicial_entorno)

    # Inicialización
    mejor_global = tour_inicial
    mejor_distancia_global = distancia_inicial
    solucion_actual = tour_inicial
    distancia_actual = distancia_inicial
    mejor_momento_actual = tour_inicial
    distancia_momento_actual = distancia_inicial
    movimientos_empeoramiento = 0
    contador = 0
    iteracion = 0

    # Registrar el estado inicial
    registrar_evento(log_file, f"Estado inicial: distancia_inicial={distancia_inicial:.2f}\n")

    while contador < iteraciones:
        # Generar vecinos con el operador 2-opt
        vecino, distancia_vecino, mejora = generar_vecinos(solucion_actual, distancia_actual, matriz_distancias,tamanio)

        # Registrar vecinos generados
        registrar_evento(log_file,f"Iteración {contador + 1}: Generado vecino con distancia={distancia_vecino:.2f}, mejora={mejora}\n")

        # Si hay mejora
        if mejora and vecino is not None:
            solucion_actual = vecino
            distancia_actual = distancia_vecino
            mejor_momento_actual = solucion_actual
            distancia_momento_actual = distancia_actual
            contador += 1

            # Actualizar mejor global si es necesario
            if distancia_momento_actual < mejor_distancia_global:
                mejor_global = mejor_momento_actual
                mejor_distancia_global = distancia_momento_actual
                movimientos_empeoramiento = 0  # Reiniciar el contador de empeoramientos

            # Registrar mejora
            registrar_evento(log_file,f"Mejora encontrada: distancia_actual={distancia_actual:.2f}\n")

        else:
            # No hay mejora, movernos al mejor vecino (aunque empeore)
            solucion_actual = vecino
            distancia_actual = distancia_vecino
            contador += 1
            movimientos_empeoramiento += 1

            # Registrar empeoramiento
            registrar_evento(log_file,f"Movimiento empeoramiento: distancia_actual={distancia_actual:.2f}\n")

            # Verificar estancamiento
            if movimientos_empeoramiento >= iteraciones * ratio_empeoramiento:
                registrar_evento(log_file, "Algoritmo estancado, reiniciando con una nueva solución.\n")
                solucion_actual, distancia_actual = greedy_aleatorio(matriz_distancias, k)
                movimientos_empeoramiento = 0  # Reiniciar el contador de empeoramientos

        # Reducimos el tamaño del entorno
        if contador == iteracion + int(tamanio * ratio_disminucion_entorno):
            tamanio = int(tamanio * (1 - disminucion_tamanio))
            iteracion = contador

            # Registrar reducción de tamaño del entorno
            registrar_evento(log_file, f"Tamaño del entorno reducido a {tamanio}\n")

            # Si se reduce por debajo del 10% termina
            if tamanio < (disminucion_tamanio * 100):
                registrar_evento(log_file, "Tamaño del entorno demasiado pequeño, finalizando.\n")
                break

    # Registrar el mejor resultado final
    registrar_evento(log_file,f"Mejor solución encontrada: mejor_distancia_global={mejor_distancia_global:.2f}\n")

    return mejor_global, mejor_distancia_global