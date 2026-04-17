import requests
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import os

# https://documents.worldbank.org/en/publication/documents-reports/api


##
# @brief Obtiene los datos del índice GINI desde la API del Banco Mundial usando GET.
#
# Esta función recupera el índice GINI para Argentina entre 2000 y 2025.
# Los valores nulos se reemplazan por cero.
#
# @return Tupla de dos arreglos de NumPy:
#         - years: arreglo de años (float)
#         - values: arreglo de valores del índice GINI (float)
def get_data():
    response = requests.get(
        "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2000:2025"
    )

    if response.ok:
        data = response.json()
        results = data[1]  # El segundo elemento contiene los datos

        year = []
        value = []
        for entry in results:
            # Reemplazar valores None por 0
            year.append(entry['date'])
            if entry['value'] is not None:
                value.append(entry['value'])
            else:
                value.append(0)

        year = np.flip(np.array(year, dtype=float))
        value = np.flip(np.array(value, dtype=float))

        return year, value
    else:
        print("Error al obtener los datos:", response.status_code)
        return None, None

##
# @brief Función wrapper para llamar a la función de conversión de la librería en C.
#
# @param input Puntero float al arreglo de entrada.
# @param output Puntero entero al arreglo de salida.
# @param length Longitud del arreglo.
def convertion(input, output, length):
    main_c.convertion(input, output, length)

# Cargar la librería compartida en C
lib_path = os.path.join(os.path.dirname(__file__), 'main.so')
main_c = ctypes.CDLL(lib_path)

# Definir los tipos de argumentos y retorno para la función en C
main_c.convertion.argtypes = (
    ctypes.POINTER(ctypes.c_float),  # float* entrada
    ctypes.POINTER(ctypes.c_int),    # int* salida
    ctypes.c_int                     # int longitud
)
main_c.convertion.restype = ctypes.c_void_p

# Obtener y procesar los datos
year, value = get_data()

length = len(value)
input_array = (ctypes.c_float * length)(*value)
output_array = (ctypes.c_int * length)()

convertion(input_array, output_array, length)
value_c = np.ctypeslib.as_array(output_array)

# Gráfico
plt.plot(year, value_c, marker='o', label='Índice Gini')
plt.title('Índice Gini en Argentina (2000–2025)')
plt.xlabel('Año')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.ylim(30, 60)
plt.yticks(np.arange(30, 60, 1))
plt.show()
