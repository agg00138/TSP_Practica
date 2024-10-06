# main.py

import sys, random, time, os

from utils.procesar_configuracion import procesar_configuracion
from utils.procesar_tsp import procesar_tsp
from utils.semillas import generar_semillas
from utils.utilidades import crear_matriz_distancias_scipy
from utils.utilidades import registrar_evento
from utils.utilidades import generar_logs
from algorithms.greedy_aleatorio import greedy_aleatorio
from algorithms.busqueda_local import busqueda_local_mejor
from algorithms.algoritmo_tabu import algoritmo_tabu


def main():

    if len(sys.argv) != 2:
        print("Uso: python ./main.py ./params.txt")
        sys.exit(1)

    # Cargar parámetros desde el archivo
    archivo_configuracion = sys.argv[1]
    params = procesar_configuracion(archivo_configuracion)

    # Cargar parámetros
    dni = params['dni']
    ejecuciones = params['executions']
    k = params['K']
    echo = params['echo']

    # Generar semillas
    semillas = generar_semillas(dni, ejecuciones)

    # Cargamos los nombres de los problemas .tsp
    tsp_files = params['problem_names']

    # Cargamos los algoritmos
    algoritmos_nombres = params['algorithms']

    # Diccionario de algoritmos
    algoritmos = {
        'greedy_aleatorio': greedy_aleatorio,
        'busqueda_local_mejor': busqueda_local_mejor,
        'algoritmo_tabu': algoritmo_tabu,
        # Agrega más algoritmos aquí
    }

    # Crear directorio para logs
    if echo == 'no':
        os.makedirs('logs', exist_ok=True)

    # Diccionario para almacenar los resultados de greedy_aleatorio
    resultados_greedy = {}

    for tsp_file in tsp_files:
        # Procesamos el archivo .tsp
        tsp_info = procesar_tsp("./data/" + tsp_file)

        print("\n===================================")
        print(f"Problema TSP: {tsp_info['nombre']}")
        print(f"Dimensión: {tsp_info['dimension']}")
        print("===================================")

        # Extraer coordenadas
        coordenadas = [coordenadas for _, coordenadas in tsp_info['coordenadas']]

        # Crear la matriz de distancias
        matriz_distancias = crear_matriz_distancias_scipy(coordenadas)

        for nombre_algoritmo in algoritmos_nombres:

            algoritmo = algoritmos.get(nombre_algoritmo.strip())  # Obtener la función del diccionario

            if algoritmo:  # Verifica si el algoritmo está en el diccionario
                # Ejecutar el algoritmo greedy aleatorio para cada semilla
                for i, semilla in enumerate(semillas):
                    random.seed(semilla)  # Fijar la semilla para reproducibilidad

                    # Generar el archivo de log
                    log_filename = generar_logs(nombre_algoritmo.strip(), tsp_info, seed=semilla, execution_num=i + 1)
                    with open(log_filename, 'w') as log_file:
                        # Registrar el inicio de la ejecución
                        registrar_evento(log_file,f"Iniciando ejecución {i + 1} para el algoritmo {nombre_algoritmo.strip()} con semilla {semilla}")

                        start_time = time.time()

                        # Llama al algoritmo pasando los parámetros correspondientes
                        if nombre_algoritmo.strip() == 'greedy_aleatorio':
                            recorrido, distancia_total = algoritmo(matriz_distancias, k, log_file)

                            # Guardar el resultado en el diccionario
                            resultados_greedy[(tsp_file, semilla)] = (recorrido, distancia_total)
                        elif nombre_algoritmo.strip() == 'busqueda_local_mejor':
                            # Verificar si ya existe el resultado de greedy_aleatorio
                            if (tsp_file, semilla) not in resultados_greedy:
                                recorrido_inicial, distancia_inicial = algoritmos['greedy_aleatorio'](matriz_distancias, k, log_file)

                                resultados_greedy[(tsp_file, semilla)] = (recorrido_inicial, distancia_inicial)
                            else:
                                recorrido_inicial, distancia_inicial = resultados_greedy[(tsp_file, semilla)]

                            # Ejecutar búsqueda local utilizando el resultado de greedy
                            recorrido, distancia_total = algoritmo(recorrido_inicial, distancia_inicial,matriz_distancias, params, log_file)
                        elif nombre_algoritmo.strip() == 'algoritmo_tabu':
                            # Verificar si ya existe el resultado de greedy_aleatorio
                            if (tsp_file, semilla) not in resultados_greedy:
                                recorrido_inicial, distancia_inicial = algoritmos['greedy_aleatorio'](matriz_distancias, k, log_file)

                                resultados_greedy[(tsp_file, semilla)] = (recorrido_inicial, distancia_inicial)
                            else:
                                recorrido_inicial, distancia_inicial = resultados_greedy[(tsp_file, semilla)]

                            # Ejecutar algoritmo tabu utilizando el resultado de greedy
                            recorrido, distancia_total = algoritmo(recorrido_inicial, distancia_inicial,matriz_distancias, params, log_file)

                        execution_time = time.time() - start_time

                        # Registrar los resultados de la ejecución en el archivo de log
                        registrar_evento(log_file,f"Ejecución {i + 1}: Distancia total = {distancia_total:.2f}, Tiempo = {execution_time:.4f} segundos")

                        # Mostrar resultados de cada ejecución en la consola
                        print(f"Ejecución {i + 1} | Algoritmo: {nombre_algoritmo.strip()} | Semilla: {semilla} | Distancia Total: {distancia_total:.2f} | Tiempo = {execution_time:.4f} segundos")
                        print("--------------------------------------------------------------------------------------------------------------------")
            else:
                print(f"Algoritmo '{nombre_algoritmo.strip()}' no reconocido.")

        print("\nProceso completado para todos los problemas y todas las semillas.")

if __name__ == '__main__':
    main()