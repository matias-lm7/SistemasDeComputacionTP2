#include <stdio.h>
#include <stdlib.h>

void convertion(float* input, int* output, int length) {
    for (int i = 0; i < length; i++) {
        output[i] = (int)(input[i] + 1.0f);
    }
}
