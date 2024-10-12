import numpy as np
import matplotlib.pyplot as plt


# Función para graficar los resultados
def generar_graficos(resultados, algoritmo, tsp_file):
    distancias = [res['distancia'] for res in resultados]
    tiempos = [res['tiempo'] for res in resultados]
    semillas = [res['semilla'] for res in resultados]

    # Crear gráfico de distancia
    plt.figure()
    plt.plot(semillas, distancias, marker='o')
    plt.title(f'Distancia total - {algoritmo} - {tsp_file}')
    plt.xlabel('Semilla')
    plt.ylabel('Distancia total')
    plt.grid(True)
    plt.savefig(f'result/{algoritmo}_{tsp_file}_distancia.png')
    plt.close()

    # Crear gráfico de tiempos
    plt.figure()
    plt.plot(semillas, tiempos, marker='o', color='orange')
    plt.title(f'Tiempo de ejecución - {algoritmo} - {tsp_file}')
    plt.xlabel('Semilla')
    plt.ylabel('Tiempo (segundos)')
    plt.grid(True)
    plt.savefig(f'result/{algoritmo}_{tsp_file}_tiempo.png')
    plt.close()


# Función para guardar estadísticas generales en un archivo
def guardar_estadisticas_generales(estadisticas, tsp_file):
    with open(f'result/estadisticas_{tsp_file}.txt', 'w') as f:
        for algoritmo, stats in estadisticas.items():
            f.write(f"Algoritmo: {algoritmo}\n")
            f.write(f"Distancia promedio: {np.mean(stats['distancias']):.2f}\n")
            f.write(f"Distancia mínima: {np.min(stats['distancias']):.2f}\n")
            f.write(f"Distancia máxima: {np.max(stats['distancias']):.2f}\n")
            f.write(f"Tiempo promedio: {np.mean(stats['tiempos']):.4f} segundos\n")
            f.write(f"Tiempo mínimo: {np.min(stats['tiempos']):.4f} segundos\n")
            f.write(f"Tiempo máximo: {np.max(stats['tiempos']):.4f} segundos\n")
            f.write("\n")


# Función para generar boxplots de distancias y tiempos
def generar_boxplot(resultados, algoritmo, tsp_file):
    distancias = [res['distancia'] for res in resultados]
    tiempos = [res['tiempo'] for res in resultados]

    # Boxplot de distancias
    plt.figure()
    plt.boxplot(distancias)
    plt.title(f'Boxplot de Distancias - {algoritmo} - {tsp_file}')
    plt.ylabel('Distancia total')
    plt.savefig(f'result/{algoritmo}_{tsp_file}_boxplot_distancia.png')
    plt.close()

    # Boxplot de tiempos
    plt.figure()
    plt.boxplot(tiempos)
    plt.title(f'Boxplot de Tiempos - {algoritmo} - {tsp_file}')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.savefig(f'result/{algoritmo}_{tsp_file}_boxplot_tiempo.png')
    plt.close()
