import modules.tsp_utils as utils
import modules.tsp_algorithms as algos

import sys, os, random, time

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <config.txt>")
        sys.exit(1)

    config_filename = sys.argv[1]

    # Obtener los parámetros desde el archivo de configuración
    config_params = utils.procesar_config(config_filename)

    tsp_files = config_params['Archivos']
    semillas = [int(seed) for seed in config_params['Semillas']]
    algoritmos = config_params['Algoritmos']
    k = config_params['K_Ciudades']
    echo = config_params['Echo']
    iteraciones = config_params['Iteraciones']
    porcentaje_tamano_entorno = config_params['Porcentaje_Tamano_ED']
    porcentaje_disminucion_entorno = config_params['Porcentaje_Disminucion_ED']
    disminucion = config_params['Disminucion']
    porcentaje_empeoramiento = config_params['Porcentaje_Emp']

    # Crear directorio para logs si Echo es 'no'
    if echo == 'no':
        os.makedirs('logs', exist_ok=True)

    # Almacenar resultados de greedy_random_tsp para cada .tsp en un diccionario
    resultados = {}

    # Procesar cada archivo .tsp
    for tsp_file in tsp_files:
        tsp_path = os.path.join('data', tsp_file)  # Ruta completa del archivo
        try:
            print(f"\n{'-' * 50}\nIntentando procesar archivo: {tsp_path}\n{'-' * 50}")

            # Obtener el diccionario con los datos del TSP
            tsp_data = utils.procesar_tsp(tsp_path)
            print("Nombre:", tsp_data['name'])
            print("Dimensión:", tsp_data['dimension'])

            # Crear la matriz de distancias
            print("Creando matriz de distancias...")
            distance_matrix = utils.crear_matriz_distancias(tsp_data['node_coords'])
            print("Matriz creada con éxito")

            # Inicializar la lista de resultados para este problema
            resultados[tsp_data['name']] = []

            for alg_name in algoritmos:
                print(f"\nEjecutando algoritmo: {alg_name}")

                if alg_name == 'greedy':
                    log_filename = None
                    if echo == 'no':
                        log_filename = utils.generar_logs(alg_name, tsp_data)

                    start_time = time.time()
                    if log_filename:
                        with open(log_filename, 'a') as log_file:
                            tour, total_distance = algos.greedy_tsp(distance_matrix, log_file=log_file)
                    else:
                        tour, total_distance = algos.greedy_tsp(distance_matrix, log_file=None)
                    execution_time = time.time() - start_time

                    result_message = f"Distancia Total: {total_distance:.2f} - Tiempo de ejecución: {execution_time:.4f} segundos"
                    print(result_message)

                elif alg_name == 'greedy_random':
                    for i, seed in enumerate(semillas, start=1):
                        random.seed(seed)
                        log_filename = None

                        if echo == 'no':
                            log_filename = utils.generar_logs(alg_name, tsp_data, seed=seed, execution_num=i)

                        start_time = time.time()
                        if log_filename:
                            with open(log_filename, 'a') as log_file:
                                tour, total_distance = algos.greedy_random_tsp(distance_matrix, k, log_file=log_file)
                        else:
                            tour, total_distance = algos.greedy_random_tsp(distance_matrix, k, log_file=None)
                        execution_time = time.time() - start_time

                        # Almacenar resultados de greedy_random en el diccionario
                        resultados[tsp_data['name']].append((tour, total_distance, tsp_data['name'], seed, i))

                        result_message = f"Ejecución {i} - Semilla: {seed} - Distancia Total: {total_distance:.2f} - Tiempo de ejecución: {execution_time:.4f} segundos"
                        print(result_message)

                elif alg_name == 'busqueda_local':

                    log_filename = None

                    # Ejecución de búsqueda local para cada resultado almacenado
                    for tour, total_distance, problem_name, seed, i in resultados[tsp_data['name']]:
                        random.seed(seed) # Fijar la semilla para cada ejecución
                        print(f"\nEjecutando búsqueda local para {problem_name} con semilla {seed}...")
                        print(f"Valor inicial para Búsqueda Local - Distancia: {total_distance:.2f}")

                        if echo == 'no':
                            log_filename = utils.generar_logs(alg_name, tsp_data, seed=seed, execution_num=i)

                        start_time = time.time()
                        if log_filename:
                            with open(log_filename, 'a') as log_file:
                                mejor_tour, mejor_distancia = algos.busqueda_local_mejor(
                                    tour, total_distance, iteraciones, porcentaje_tamano_entorno, distance_matrix,
                                    porcentaje_disminucion_entorno, disminucion, log_file=log_file
                                )
                        else:
                            mejor_tour, mejor_distancia = algos.busqueda_local_mejor(
                                tour, total_distance, iteraciones, porcentaje_tamano_entorno, distance_matrix,
                                porcentaje_disminucion_entorno, disminucion, log_file=None
                            )
                        execution_time = time.time() - start_time
                        result_message = f"Mejor distancia encontrada con Búsqueda Local para {problem_name} y semilla {seed}: {mejor_distancia:.2f} - Tiempo de ejecución: {execution_time:.4f} segundos"
                        print(result_message)

                elif alg_name == 'tabu':

                    log_filename = None

                    # Ejecutar el algoritmo Tabú para cada resultado almacenado
                    for tour, total_distance, problem_name, seed, i in resultados[tsp_data['name']]:
                        random.seed(seed)  # Fijar la semilla para cada ejecución
                        print(f"\nEjecutando algoritmo Tabú para {problem_name} con semilla {seed}...")
                        print(f"Valor inicial para Tabú - Distancia: {total_distance:.2f}")

                        if echo == 'no':
                            log_filename = utils.generar_logs(alg_name, tsp_data, seed=seed, execution_num=i)

                        start_time = time.time()
                        if log_filename:
                            with open(log_filename, 'a') as log_file:
                                mejor_tour, mejor_distancia = algos.algoritmo_tabu(
                                    tour, total_distance, iteraciones, porcentaje_tamano_entorno, distance_matrix,
                                    porcentaje_disminucion_entorno, disminucion,
                                    porcentaje_empeoramiento, k, log_file=log_file
                                )
                        else:
                            mejor_tour, mejor_distancia = algos.algoritmo_tabu(
                                tour, total_distance, iteraciones, porcentaje_tamano_entorno, distance_matrix,
                                porcentaje_disminucion_entorno, disminucion,
                                porcentaje_empeoramiento, k, log_file=None
                            )
                        execution_time = time.time() - start_time
                        result_message = f"Mejor distancia encontrada con Tabú para {problem_name} y semilla {seed}: {mejor_distancia:.2f} - Tiempo de ejecución: {execution_time:.4f} segundos"
                        print(result_message)

                else:
                    print(f"Algoritmo '{alg_name}' no reconocido.")
                    continue

        except FileNotFoundError:
            print(f"Error: El archivo '{tsp_path}' no se encuentra.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()