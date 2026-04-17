import requests
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import os

# https://documents.worldbank.org/en/publication/documents-reports/api

##
# @brief Fetches the GINI index data from the World Bank API using GET.
#
# This function retrieves the GINI index for Argentina between 2000 and 2025.
# Null values are replaced by zero.
#
# @return Tuple of two NumPy arrays:
#         - years: float array of years
#         - values: float array of GINI index values
def get_data():
    response = requests.get(
        "https://api.worldbank.org/v2/en/country/ARG/indicator/SI.POV.GINI?format=json&date=2000:2025"
    )

    if response.ok:
        data = response.json()
        results = data[1]  # Second element contains the data

        year = []
        value = []
        for entry in results:
            # Replace None values with 0
            year.append(entry['date'])
            if entry['value'] is not None:
                value.append(entry['value'])
            else:
                value.append(0)

        year = np.flip(np.array(year, dtype=float))
        value = np.flip(np.array(value, dtype=float))

        return year, value
    else:
        print("Failed to fetch data:", response.status_code)
        return None, None

##
# @brief Wrapper function to call the C library's conversion function.
#
# @param input Float pointer to the input array.
# @param output Integer pointer to the output array.
# @param length Length of the array.
def convertion(input, output, length):
    main_c.convertion(input, output, length)

# Load the shared C library
lib_path = os.path.join(os.path.dirname(__file__), 'main.so')
main_c = ctypes.CDLL(lib_path)

# Define argument and return types for the C function
main_c.convertion.argtypes = (
    ctypes.POINTER(ctypes.c_float),  # float* input
    ctypes.POINTER(ctypes.c_int),    # int* output
    ctypes.c_int                     # int length
)
main_c.convertion.restype = ctypes.c_void_p

# Fetch and process the data
year, value = get_data()

length = len(value)
input_array = (ctypes.c_float * length)(*value)
output_array = (ctypes.c_int * length)()

convertion(input_array, output_array, length)
value_c = np.ctypeslib.as_array(output_array)

# Plotting
plt.plot(year, value_c, marker='o', label='Gini Index')
plt.title('Gini Index in Argentina (2000–2025)')
plt.xlabel('Year')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.ylim(30, 60)
plt.yticks(np.arange(30, 60, 1))
plt.show()
