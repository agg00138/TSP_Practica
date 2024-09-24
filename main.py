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

    # Procesar cada archivo .tsp
    for tsp_file in tsp_files:
        tsp_path = os.path.join('data', tsp_file)  # Ruta completa del archivo
        try:
            #print(f"\nIntentando procesar archivo: {tsp_path}")
            print(f"\n{'-' * 50}\nIntentando procesar archivo: {tsp_path}\n{'-' * 50}")

            # Obtener el diccionario
            tsp_data = utils.procesar_tsp(tsp_path)
            print("Nombre:", tsp_data['name'])
            print("Dimensión:", tsp_data['dimension'])

            # Crear y mostrar la matriz de distancias
            distance_matrix = utils.crear_matriz_distancias(tsp_data['node_coords'])
            #print("Matriz de Distancias:")
            #utils.print_matriz_distancias(distance_matrix)

            for alg_name in algoritmos:
                print(f"\nEjecutando algoritmo: {alg_name}")

                if alg_name == 'greedy':
                    tour, total_distance = algos.greedy_tsp(distance_matrix)
                    print(f"Distancia Total: {total_distance:.2f}")

                elif alg_name == 'greedy_random':
                    for i, seed in enumerate(semillas, start=1):
                        random.seed(seed)
                        start_time = time.time()    # Medir tiempo de ejecución del algoritmo
                        tour, total_distance = algos.greedy_random_tsp(distance_matrix, k)
                        execution_time = time.time() - start_time  # Calcular el tiempo
                        print(f"Ejecución {i} - Semilla: {seed} - Distancia Total: {total_distance:.2f} - Tiempo de ejecución: {execution_time:.4f} segundos")

                else:
                    print(f"Algoritmo '{alg_name}' no reconocido.")
                    continue

        except FileNotFoundError:
            print(f"Error: El archivo '{tsp_path}' no se encuentra.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()