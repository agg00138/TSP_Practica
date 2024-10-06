# utils/procesar_tsp.py


def procesar_tsp(nombre_archivo):
    tsp_data = {
        'nombre': None,          # Nombre del problema TSP
        'dimensión': None,       # Número de nodos (ciudades)
        'coordenadas': []        # Lista para almacenar las coordenadas de las ciudades
    }

    with open(nombre_archivo, 'r') as file:
        for line in file:
            line = line.strip()  # Elimina espacios en blanco al principio y final de la línea
            if not line or line.startswith('NODE_COORD_SECTION') or line == 'EOF':
                # Saltar líneas vacías, la sección de coordenadas y el indicador de fin del archivo
                continue

            # Procesar cabeceras y coordenadas del archivo
            if line.startswith('NAME:'):
                tsp_data['nombre'] = line.split(':')[1].strip()
            elif line.startswith('DIMENSION:'):
                tsp_data['dimension'] = int(line.split(':')[1].strip())
            elif line.startswith('EDGE_WEIGHT_TYPE:'):
                continue  # Ignorar esta línea
            elif line[0].isdigit():  # Procesar solo líneas que comienzan con un número
                # Procesar las coordenadas de cada nodo
                tokens = line.split()
                if len(tokens) == 3:
                    ciudad = int(tokens[0])
                    x = float(tokens[1])
                    y = float(tokens[2])
                    tsp_data['coordenadas'].append((ciudad, (float(x), float(y))))

    return tsp_data