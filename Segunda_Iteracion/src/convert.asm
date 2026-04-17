; ----------------------------
; int convert(float input)
; Versión para x86-64
; ----------------------------

section .text
global convert

convert:
    ; El argumento float llega en XMM0

    ; Cargar el valor 1.0 en XMM1
    movss xmm1, [rel one]

    ; Sumar 1.0 al valor de entrada
    addss xmm0, xmm1

    ; Convertir el resultado a entero (redondeo por truncamiento)
    cvttss2si eax, xmm0

    ret

section .rodata
one: dd 1.0

section .note.GNU-stack noalloc noexec
