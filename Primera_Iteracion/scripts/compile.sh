#!/bin/bash

# Compila el archivo `convertion.c` en una biblioteca compartida
gcc -fPIC -shared -o main.so main.c
