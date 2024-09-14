import modules.tsp_utils as utils
import modules.tsp_algorithms as algos

import sys, os

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo_nombres.tsp>")
        sys.exit(1)

    txt_filename = sys.argv[1]

    # Obtener los nombres de los archivos .tsp del archivo .txt
    tsp_files = utils.procesar_archivo_txt(txt_filename)

    # Procesar cada archivo .tsp
    for tsp_file in tsp_files:
        tsp_path = os.path.join('data', tsp_file)  # Ruta completa del archivo
        try:
            print(f"\nIntentando procesar archivo: {tsp_path}")

            tsp_data = utils.procesar_tsp(tsp_path)
            print("Nombre:", tsp_data['name'])
            print("Dimensión:", tsp_data['dimension'])

            # Crear y mostrar la matriz de distancias
            distance_matrix = utils.crear_matriz_distancias(tsp_data['node_coords'])
            print("Matriz de Distancias:")
            utils.print_matriz_distancias(distance_matrix)

            tour, total_distance = algos.greedy_tsp(distance_matrix)
            print("\nRuta Encontrada:")
            print(" -> ".join(str(city + 1) for city in tour))  # Añado 1 al ID de la ciudad
            print(f"Distancia Total: {total_distance:.2f}")

        except FileNotFoundError:
            print(f"Error: El archivo '{tsp_path}' no se encuentra.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()