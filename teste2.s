# Programa MIPS que soma 10 + 10

ADDI $t0, $zero, 10   # Carrega 10 em $t0 (sem deslocamento)
ADDI $t1, $zero, 10   # Carrega 10 em $t1 (sem deslocamento)
ADD $t2, $t0, $t1     # Soma $t0 e $t1, resultado em $t2
IMPRIMIR INTEIRO $t2  # Imprime o valor de $t2 (que deve ser 20)

SAIR                  # Finaliza o programa

