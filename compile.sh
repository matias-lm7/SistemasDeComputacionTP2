#!/bin/bash

# Compile the convertion.c file into a shared library
gcc -fPIC -shared -o main.so main.c
