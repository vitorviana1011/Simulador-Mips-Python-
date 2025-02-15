    .data
msg1: .asciiz "Soma: "  # String que será impressa

    .text
LUI $t0, 0x0        # Carrega 0 no registrador $t0 (t0 = 0)
ADDI $t0, $t0, 10   # t0 = t0 + 10 (t0 = 10)
LUI $t1, 0x0        # Carrega 0 no registrador $t1 (t1 = 0)
ADDI $t1, $t1, 10   # t1 = t1 + 10 (t1 = 10)

ADD $t2, $t0, $t1   # t2 = t0 + t1 (t2 = 10 + 10 = 20)

SW $t2, 0($sp)      # Armazena o valor de $t2 na pilha (simulando uma "memória")

# Suponhamos que a string "msg1" e o valor de t2 sejam exibidos de alguma maneira:
IMPRIMIR STRING msg1  # Imprime a string "Soma: "
IMPRIMIR INTEIRO $t2  # Imprime o valor de t2 (20)

