# algorithms/busqueda_local.py

from utils.utilidades import generar_vecinos
from utils.utilidades import registrar_evento


def busqueda_local_mejor(tour_inicial, distancia_inicial, matriz_distancias, params, log_file=None):
    """
        Realiza una búsqueda local para mejorar un tour inicial utilizando el operador 2-opt.

        Args:
            tour_inicial (list[int]): El tour inicial propuesto.
            distancia_inicial (float): La distancia total del tour inicial.
            matriz_distancias (list[list[float]]): Matriz de distancias entre las ciudades.
            params (dict): Parámetros de control para la búsqueda local.
            log_file (file object, optional): Archivo donde se registran los eventos de la búsqueda.

        Returns:
            tuple: Un tuple que contiene el mejor recorrido (tour) y la mejor distancia encontrada.
    """

    # Cargar los parámetros
    iteraciones = params['iterations']
    tamanio_inicial_entorno = params['initial_environment_size']
    ratio_disminucion_entorno = params['size_decrease_rate']
    disminucion_tamanio = params['size_decrease_environment']

    # Calculo el tamaño del entorno dinámico
    tamanio = int(iteraciones * tamanio_inicial_entorno)

    # Inicialización
    mejor_tour = tour_inicial
    mejor_distancia = distancia_inicial
    contador = 0
    iteracion = 0

    # Registrar el estado inicial
    registrar_evento(log_file, f"Estado inicial: distancia_inicial={distancia_inicial:.2f}\n")

    while contador < iteraciones:

        # Generar vecinos con el operador 2-opt
        vecino, distancia_vecino, mejora = generar_vecinos(mejor_tour, mejor_distancia, matriz_distancias, tamanio)

        # Registrar vecinos generados
        registrar_evento(log_file,f"Iteración {contador + 1}: Generado vecino con distancia={distancia_vecino:.2f}, mejora={mejora}\n")

        # Si hay mejora
        if mejora and vecino is not None:
            mejor_tour = vecino
            mejor_distancia = distancia_vecino
            contador += 1
            # Registrar mejora
            registrar_evento(log_file, f"Mejora encontrada: distancia_actual={mejor_distancia:.2f}\n")
        else:
            break

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
    registrar_evento(log_file,f"Mejor solución encontrada: mejor_distancia_global={mejor_distancia:.2f}\n")

    return mejor_tour, mejor_distancia