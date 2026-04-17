#include <stdio.h>
#include <stdlib.h>

/**
 * @param value Valor sobre el cual se realiza la operación.
 * @brief Esta función convierte el valor a entero e incrementa su valor en 1.
 */
extern int convert(float value);

/**
 * @brief Convierte un arreglo de números de punto flotante a un arreglo de enteros.
 *
 * Esta función toma un arreglo de entrada de números de punto flotante y convierte
 * cada elemento a un entero utilizando la función `convert`. Los enteros convertidos
 * se almacenan en el arreglo de salida.
 *
 * @param input Puntero al arreglo de números de punto flotante de entrada.
 * @param output Puntero al arreglo donde se almacenarán los enteros convertidos.
 * @param length La cantidad de elementos en los arreglos de entrada y salida.
 */
void convertion(float* input, int* output, int length) {
    for (int i = 0; i < length; i++) {
        output[i] = convert(input[i]);
    }
}
