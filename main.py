import modules.tsp_utils as utils
import modules.tsp_algorithms as algos

import sys, os, random, time


def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <config.txt>")
        sys.exit(1)

    config_filename = sys.argv[1]

    # Obtener los parámetros desde el archivo de configuración
    config_params = utils.procesar_archivo_config(config_filename)

    tsp_files = config_params['Archivos']
    semillas = [int(seed) for seed in config_params['Semillas']]
    algoritmos = config_params['Algoritmos']
    k = int(config_params['OtrosParametros1'])
    echo = config_params['Echo']

    # Crear directorio para logs si Echo es 'no'
    if echo == 'no':
        os.makedirs('logs', exist_ok=True)

    # Procesar cada archivo .tsp
    for tsp_file in tsp_files:
        tsp_path = os.path.join('data', tsp_file)  # Ruta completa del archivo
        try:
            print(f"\n{'-' * 50}\nIntentando procesar archivo: {tsp_path}\n{'-' * 50}")

            # Obtener el diccionario
            tsp_data = utils.procesar_tsp(tsp_path)
            print("Nombre:", tsp_data['name'])
            print("Dimensión:", tsp_data['dimension'])

            # Crear y mostrar la matriz de distancias
            distance_matrix = utils.crear_matriz_distancias(tsp_data['node_coords'])

            for alg_name in algoritmos:
                print(f"\nEjecutando algoritmo: {alg_name}")

                if alg_name == 'greedy':
                    log_filename = None
                    if echo == 'no':
                        log_filename = f"logs/{alg_name}_{tsp_data['name']}_ejecucion_1.log"

                    # Pasar log_file y echo a la función
                    tour, total_distance = algos.greedy_tsp(distance_matrix, log_file=open(log_filename, 'a') if log_filename else None)
                    result_message = f"Distancia Total: {total_distance:.2f}"
                    print(result_message)

                elif alg_name == 'greedy_random':
                    for i, seed in enumerate(semillas, start=1):
                        random.seed(seed)
                        start_time = time.time()  # Medir tiempo de ejecución del algoritmo
                        log_filename = f"logs/{alg_name}_{seed}_{tsp_data['name']}_ejecucion_{i}.log" if echo == 'no' else None
                        # Pasar log_file y echo a la función
                        tour, total_distance = algos.greedy_random_tsp(distance_matrix, k, log_file=open(log_filename, 'a') if log_filename else None)
                        execution_time = time.time() - start_time  # Calcular el tiempo
                        result_message = f"Ejecución {i} - Semilla: {seed} - Distancia Total: {total_distance:.2f} - Tiempo de ejecución: {execution_time:.4f} segundos"
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
