# Carregando valores nos registradores e testando instruções
LUI $t0, 10        # Coloca 0xFFFF0000 no $t0
ADDI $t1, $t0, 42      # Soma 42 a $t0 e armazena em $t1
ADD $t2, $t0, $t1      # Soma $t0 e $t1, resultado em $t2
SUB $t3, $t1, $t0      # Subtrai $t0 de $t1, resultado em $t3
AND $t4, $t0, $t1      # Realiza operação AND entre $t0 e $t1
OR $t5, $t0, $t1       # Realiza operação OR entre $t0 e $t1
SLL $t6, $t1, 2        # Desloca $t1 2 bits para a esquerda, resultado em $t6
SLT $t7, $t0, $t1      # Verifica se $t0 é menor que $t1

# Testando Load e Store
LUI $t8, 10        # Carrega 0x12340000 em $t8
SW $t8, 0($sp)         # Armazena o valor de $t8 na memória no endereço do stack pointer
LW $t9, 0($sp)         # Carrega o valor da memória para $t9

# Testando saída e comparação imediata
SLTI $s0, $t1, 10    # Verifica se $t1 é menor que 1000
IMPRIMIR INTEIRO $s0   # Imprime o resultado (1 ou 0)
IMPRIMIR INTEIRO $t9   # Imprime o valor de $t9

# Testando impressão de string
LUI $a0, 10        # Supõe que uma string começa no endereço 0x10000000
IMPRIMIR STRING 10 # Imprime a string armazenada na memória

# Finalizando o programa
SAIR

