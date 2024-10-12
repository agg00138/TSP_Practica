# utils/procesar_configuracion.py

import sys


def leer_archivo(nombre_archivo):
    """ Lee el contenido del archivo y retorna las líneas. """
    with open(nombre_archivo, 'r') as archivo:
        return archivo.readlines()


def procesar_linea(linea):
    """ Procesa una línea y retorna clave y valor. """
    clave, valor = linea.split('=', 1)
    return clave.strip(), valor.strip()


def procesar_configuracion(nombre_archivo):
    """
    Carga los parámetros desde un archivo .txt.

    :param nombre_archivo: Ruta del archivo de parámetros.
    :return: Diccionario con los parámetros cargados. Las claves incluyen 'Archivos', 'Semillas', etc.
    :raises FileNotFoundError: Si el archivo no se encuentra.
    :raises ValueError: Si un valor en el archivo no es válido para su tipo esperado.
    :raises Exception: Para otros errores generales.
    """
    parametros = {
        'problem_names': [],
        'algorithms': [],
        'K': None,
        'dni': None,
        'executions': None,
        'iterations': None,
        'initial_environment_size': None,
        'size_decrease_rate': None,
        'size_decrease_environment': None,
        'worsening_movement_rate': None,
        'taboo_possesion': None,
        'strategic_oscillation': None,
        'echo': None
    }

    tipos_esperados = {
        'problem_names': list,
        'algorithms': list,
        'K': int,
        'dni': int,
        'executions': int,
        'iterations': int,
        'initial_environment_size': float,
        'size_decrease_rate': float,
        'size_decrease_environment': float,
        'worsening_movement_rate': float,
        'taboo_possesion': int,
        'strategic_oscillation': float,
        'echo': str
    }

    try:
        lineas = leer_archivo(nombre_archivo)
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith('#') or not linea:
                continue

            if '=' in linea:
                clave, valor = procesar_linea(linea)

                if clave in parametros:
                    # Convertir valores a su tipo adecuado
                    if clave == 'problem_names':
                        # Agregar cada problema a la lista
                        parametros[clave] += [item.strip() for item in valor.split(',')]
                    elif clave == 'algorithms':
                        # Agregar cada algoritmo a la lista
                        parametros[clave] += [item.strip() for item in valor.split(',')]
                    else:
                        parametros[clave] = tipos_esperados[clave](valor)

    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encuentra.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Valor no válido en '{clave}' para '{valor}'. Detalle del error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return parametros
