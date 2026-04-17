#include <stdio.h>
#include <stdlib.h>

/**
 * @param value valor sobre el que se realiza la operación
 * @brief Esta función convierte el valor a entero y lo incrementa.
 */
extern int convert(float value);

/**
 * @brief Convierte un arreglo de números en punto flotante a un arreglo de enteros.
 *
 * @param input Puntero al arreglo de entrada de números en punto flotante.
 * @param output Puntero al arreglo de salida donde se almacenarán los enteros convertidos.
 * @param length Cantidad de elementos en los arreglos de entrada y salida.
 */
void convertion(float* input, int* output, int length) {
    for (int i = 0; i < length; i++) {
        output[i] = convert(input[i]);
    }
}

int main(void) {
    float  in[1]  = {38.5f};  
    int    out[1] = {0};      

    convertion(in, out, 1);     
    for (int i = 0; i < 1; i++)  
        printf("in[%d]=%f → out[%d]=%d\n", i, in[i], i, out[i]);

    return 0;
}
