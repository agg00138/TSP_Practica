# utils/semillas.py

import random

def generar_semillas(dni_alumno, cantidad):
    """
    Genera una lista de semillas pseudoaleatorias basadas en el DNI del alumno.

    :param dni_alumno: Número del DNI del alumno que se utilizará como base para las semillas.
    :param cantidad: Cantidad de semillas que se desean generar.
    :return: Lista de semillas generadas.
    """
    random.seed(dni_alumno)  # Inicializa el generador de números aleatorios con el DNI
    semillas = []
    for i in range(cantidad):
        # Generar una semilla pseudoaleatoria
        semillas.append(random.randint(1, 100000))  # Rango ajustable según sea necesario
    return semillas
